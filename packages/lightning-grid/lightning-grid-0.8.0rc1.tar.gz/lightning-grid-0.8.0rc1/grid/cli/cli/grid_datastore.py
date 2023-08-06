import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional, List

import click
from rich.console import Console
from rich.prompt import Confirm
from yaspin import yaspin

from grid.cli import rich_click
from grid.cli.observables import BaseObservable
from grid.sdk import env
from grid.sdk.client import create_swagger_client
from grid.sdk.datastores import Datastore, list_datastores
from grid.sdk.rest import GridRestClient
from grid.sdk.utils.datastore_uploads import list_incomplete_datastore_uploads, resume_datastore_upload

WARNING_STR = click.style('WARNING', fg='yellow')


@click.group(invoke_without_command=True)
@click.pass_context
@click.option(
    '--global',
    'is_global',
    type=bool,
    is_flag=True,
    default=False,
    show_default=True,
    help='Fetch sessions from everyone in the team when flag is passed'
)
@click.option(
    '--cluster',
    'cluster_id',
    type=str,
    required=False,
    default=env.CONTEXT,
    show_default=True,
    help='The cluster id to list datastores for.',
)
@click.option(
    '--show-incomplete',
    'show_incomplete',
    type=bool,
    is_flag=True,
    default=False,
    show_default=True,
    help=(
        'Show any datastore uploads which were started, but killed or errored before '
        'they finished uploading all data and became "viewable" on the grid datastore '
        'user interface.'
    )
)
def datastore(ctx, cluster_id: str, is_global: bool, show_incomplete: bool) -> None:
    """Manages Datastore workflows."""
    if ctx.invoked_subcommand is None:

        table_rows, table_cols = [], []
        if show_incomplete is True:
            # TODO: Why are we using yaspin when Rich already contains a spinner console instance?
            #       This is literally an additional dependency for no reason...
            spinner = yaspin(text=f"Loading Incomplete Datastores on Local Machine...", color="yellow")
            spinner.start()

            table_cols = ["Datastore ID", "Name", "Cluster ID", "Started At", "Source Path"]
            try:
                for ds in list_incomplete_datastore_uploads(Path(env.GRID_DIR)):
                    created_at = f"{datetime.fromtimestamp(ds.creation_timestamp):%Y-%m-%d %H:%M}"
                    table_rows.append([ds.datastore_id, ds.datastore_name, ds.cluster_id, created_at, ds.source])
            except Exception as e:
                spinner.fail("✘")
                raise click.ClickException(e)
        else:
            spinner = yaspin(text=f"Loading Datastores in {env.CONTEXT}...", color="yellow")
            spinner.start()

            table_cols = ["Name", "Cluster ID", "Version", "Size", "Created At", "Status"]
            try:
                datastores: List[Datastore] = list_datastores(cluster_id=cluster_id, is_global=is_global)
            except Exception as e:
                spinner.fail("✘")
                raise click.ClickException(e)

            for ds in sorted(datastores, key=lambda k: (k.name, k.version)):
                created_at = f'{ds.created_at:%Y-%m-%d %H:%M}'
                size = ds.size
                status = ds.snapshot_status
                table_rows.append([ds.name, ds.cluster_id, str(ds.version), size, created_at, status])

        table = BaseObservable.create_table(columns=table_cols)
        for row in table_rows:
            table.add_row(*row)

        spinner.ok("✔")
        console = Console()
        console.print(table)

    elif is_global:
        click.echo(f"{WARNING_STR}: --global flag doesn't have any effect when invoked with a subcommand")


@datastore.command()
@rich_click.argument(
    'datastore_id',
    nargs=1,
    default=" ",
    required=False,
    type=str,
    help="The datastore id as retrieved from `grid datastore --show-incomplete`."
)
@click.option(
    "--all",
    "-a",
    "all_",
    is_flag=True,
    default=False,
    show_default=True,
    required=False,
    help=(
        "upload all incomplete datastore uploads on the machine, otherwise "
        "only the session referenced by DATASTORE_ID argument is uploaded."
    )
)
@click.pass_context
def resume(ctx, datastore_id: str, all_: bool):
    """Resume uploading a datastore. DATASTORE_ID identifies the datastore upload session to resume.
    """
    if all_:
        for ds_work in list_incomplete_datastore_uploads(Path(env.GRID_DIR)):
            try:
                c = GridRestClient(create_swagger_client())
                resume_datastore_upload(client=c, grid_dir=Path(env.GRID_DIR), work=ds_work)
            except Exception as e:
                raise click.ClickException(e)
        return

    for ds_work in list_incomplete_datastore_uploads(Path(env.GRID_DIR)):
        if ds_work.datastore_id == datastore_id:
            break
    else:  # N.B. for-else loop (ie. "no break")
        raise click.ClickException(
            f"Could not find datastore_id: {datastore_id} session state; Are you "
            f"sure it exists? Try running `grid datastore --incomplete` and verify "
            f"that the DATASTORE_ID argument to this command is correct"
        )
    try:
        c = GridRestClient(create_swagger_client())
        resume_datastore_upload(client=c, grid_dir=Path(env.GRID_DIR), work=ds_work)
    except Exception as e:
        raise click.ClickException(e)


@datastore.command(cls=rich_click.deprecate_grid_options())
@rich_click.argument(
    'source',
    type=str,
    required=True,
    help=(
        "Source to create datastore from. This could either be a local "
        "directory (e.g: /opt/local_folder) a remote http URL pointing "
        "to a TAR or ZIP file (e.g. http://some_domain/data.tar.gz), or "
        "an s3 bucket to copy data from (e.g. s3://ryft-public-sample-data/esRedditJson/)"
    )
)
@click.option('--name', type=str, required=False, help='Name of the datastore')
@click.option(
    '--cluster',
    type=str,
    default=env.CONTEXT,
    show_default=True,
    required=False,
    help='cluster id to create the datastore on. (Bring Your Own Cloud Customers Only).'
)
@click.pass_context
def create(ctx, source: str, cluster: str, name: Optional[str] = None) -> None:
    """Creates a datastore from SOURCE.

    The upload session is referenced by the name. this name
    must be used to resume the upload if it is interupted.
    """
    try:
        current_source = Path(source).absolute()
        for ds_work in list_incomplete_datastore_uploads(Path(env.GRID_DIR)):
            if current_source == Path(ds_work.source) and name == ds_work.datastore_name:
                should_resume = Confirm.ask(
                    "[i]A previous datastore upload created from this directory was "
                    "interrupted before it was able to complete.[/i]\n\n"
                    "[cyan]Do you wish to resume this upload [bold green](yes/y)[reset]? "
                    "If not [bold red](no/n)[reset], then the [u]progress on the "
                    "interrupted upload will be deleted[/u], and you will have to upload "
                    "the dataset in full.\n",
                    default=True
                )
                if should_resume is True:
                    c = GridRestClient(create_swagger_client())
                    resume_datastore_upload(client=c, grid_dir=Path(env.GRID_DIR), work=ds_work)
                    break
                else:
                    # run the loop out until the else clause is hit below
                    continue
        else:  # N.B. for-else loop (ie. no-break)
            dstore = Datastore(name=name, source=source, cluster_id=cluster)
            dstore.upload()
    except Exception as e:
        raise click.ClickException(e)


@datastore.command()
@click.pass_context
def clearcache(ctx) -> None:
    """Clears datastore cache which is saved on the local machine when uploading a datastore to grid.

    This removes all the cached files from the local machine, meaning that resuming an incomplete
    upload is not possible after running this command.
    """
    for f in Path(env.GRID_DIR).joinpath("datastores").iterdir():
        if f.is_file():
            os.remove(str(f.absolute()))
        if f.is_dir():
            shutil.rmtree(str(f.absolute()))
    click.echo("Datastore cache cleared")


@datastore.command(cls=rich_click.deprecate_grid_options())
@click.option('--name', type=str, required=True, help='Name of the datastore')
@click.option('--version', type=int, required=True, help='Version of the datastore')
@click.option(
    '--cluster',
    type=str,
    required=False,
    default=env.CONTEXT,
    show_default=True,
    help='cluster id to delete the datastore from. (Bring Your Own Cloud Customers Only).'
)
@click.pass_context
def delete(ctx, name: str, version: int, cluster: str) -> None:
    """Deletes a datastore with the given name and version tag.

    For bring-your-own-cloud customers, the cluster id of the associated
    resource is required as well.
    """
    try:
        dstore = Datastore(name=name, version=version, cluster_id=cluster)
        dstore.delete()
    except Exception as e:
        raise click.ClickException(str(e))
    click.echo("Done!")
