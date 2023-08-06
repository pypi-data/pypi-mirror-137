import concurrent.futures
import datetime
import math
import os
import signal
import time
import warnings
from collections import defaultdict
from dataclasses import dataclass, field, asdict
from pathlib import Path
from threading import Event
from typing import List, Optional, TYPE_CHECKING, Dict, Iterator
from uuid import uuid4

import requests
import ujson
from dataclasses_json import dataclass_json
from requests.adapters import HTTPAdapter
from rich.live import Live
from rich.panel import Panel
from rich.progress import Progress, TextColumn, BarColumn, DownloadColumn, TaskID, TransferSpeedColumn
from rich.status import Status
from urllib3 import Retry

try:
    from rich.console import RenderGroup as Group
except ImportError:
    from rich.console import Group

from grid.metadata import __version__
from grid.sdk import env
from grid.sdk.rest.datastores import (
    datastore_upload_object_from_data_file,
    create_presigned_urls,
    complete_presigned_url_upload,
    mark_datastore_upload_complete,
)

if TYPE_CHECKING:
    from grid.sdk.rest import GridRestClient

_SEC = 1
_MIN = 60 * _SEC
_HOUR = 60 * _MIN
_DAY = 24 * _HOUR

_MAX_FILE_SIZE = 10_000 * env.GRID_DATASTORE_MAX_BYTES_PER_FILE_PART_UPLOAD  # s3 limit is 10,000 parts

# -------------- interrupt handling ---------------

done_event = Event()


def handle_termination_signal(signum, frame):
    done_event.set()


signal.signal(signal.SIGINT, handle_termination_signal)
signal.signal(signal.SIGTERM, handle_termination_signal)

# ----------------- data structures ----------------


@dataclass
class PBar:
    p_upload_bytes: Progress
    p_upload_files: Progress
    p_finalize: Progress

    progress_group: Group

    upload_bytes_beginning_advance: int
    upload_bytes_total: int
    upload_files_beginning_advance: int
    upload_files_total: int
    finalize_beginning_advance: int
    finalize_total: int

    upload_bytes_task_id: TaskID
    upload_files_task_id: TaskID
    finalize_task_id: TaskID

    action_status: Status
    status_text_uploading: str = "[bold blue] Uploading Data"
    status_text_saving: str = "[bold yellow] Checkpointing Current Upload Progress"
    status_text_finalizing: str = "[bold blue] Finalizing Upload"
    status_text_done: str = "[bold green] Done!"


@dataclass_json
@dataclass
class UploadTask:
    data_file_local_id: str
    part_number: str
    read_offset_bytes: int  # beginning position to seek to in the file
    read_range_bytes: int  # how many bytes to read after the starting position
    url: str
    etag: Optional[str] = None


@dataclass_json
@dataclass
class DataFile:
    absolute_path: str  # path to file to upload on client
    relative_file_name: str  # key of the object in the datastore (relative path from datastore source at creation)
    size_bytes: int  # total size of the file in bytes
    local_id: str  # uuid generated when the file contents are first read.

    part_count: Optional[int] = None
    upload_id: Optional[str] = None
    expiry_time: Optional[int] = None  # unix timestamp when presigned url will expire.
    tasks: List[UploadTask] = field(default_factory=list)

    is_uploaded: bool = False
    is_marked_complete: bool = False


@dataclass_json
@dataclass
class Work:
    datastore_id: str
    datastore_name: str
    datastore_version: str
    cluster_id: str
    source: str
    creation_timestamp: int  # unix timestamp of the initial creation time
    grid_cli_version: str = __version__
    files: Dict[str, DataFile] = field(default_factory=dict)  # files contained in the datastore


# ------------------ serialization / de-serialization --------------------


def _load_work_state(grid_dir: Path, datastore_id: str) -> Work:
    state_file = grid_dir.joinpath("datastores", f"{datastore_id}.json")
    if not state_file.exists():
        raise FileNotFoundError(f"work state file does not exist at: {state_file}")
    work = Work.from_dict(ujson.loads(state_file.read_text()))
    if work.grid_cli_version != __version__:
        raise RuntimeError(
            "Cannot resume an upload which was started with a different version "
            "of the grid. Please restart the upload to use this datastore. "
        )
    return work


def _save_work_state(grid_dir: Path, work: Work) -> None:
    datastores_dir = grid_dir.joinpath("datastores")
    os.makedirs(str(datastores_dir), exist_ok=True)
    state_file = datastores_dir.joinpath(f"{work.datastore_id}.json")
    state_file.touch()
    state_file.write_text(ujson.dumps(asdict(work)))


def _remove_work_state(grid_dir: Path, datastore_id: str) -> None:
    state_file = grid_dir / "datastores" / f"{datastore_id}.json"
    if not state_file.exists():
        raise FileNotFoundError(f"could not find / remove work state file: {state_file}")
    os.remove(str(state_file.absolute()))


def list_incomplete_datastore_uploads(grid_dir: Path) -> Iterator[Work]:
    datastores_dir = grid_dir.joinpath("datastores")
    os.makedirs(str(datastores_dir), exist_ok=True)

    for work_state_file in list(datastores_dir.iterdir()):
        if not work_state_file.is_file() or not work_state_file.name.endswith(".json"):
            continue
        datastore_id = work_state_file.name.rstrip(".json")
        try:
            state = _load_work_state(grid_dir=grid_dir, datastore_id=datastore_id)
            yield state
        except RuntimeError:
            _remove_work_state(grid_dir=grid_dir, datastore_id=datastore_id)
            continue


def _clear_expired_datastore_upload_work(grid_dir: Path):
    for work_piece in list_incomplete_datastore_uploads(grid_dir):
        if time.time() > work_piece.creation_timestamp + (10 * _DAY):
            os.remove(str(grid_dir / "datastores" / f"{work_piece.datastore_id}.json"))
    return


# ----------------------- initialization ------------------------------


def initialize_upload_work(
    name: str, datastore_id: str, cluster_id: str, creation_timestamp: int, source_path: str, version: str
) -> Work:
    rel_path = Path(source_path)
    abs_path = rel_path.absolute()
    if not abs_path.exists():
        raise OSError(f"the datastore upload source path: {source_path} does not exist")

    all_work = Work(
        datastore_name=name,
        datastore_id=datastore_id,
        cluster_id=cluster_id,
        creation_timestamp=creation_timestamp,
        source=str(abs_path),
        datastore_version=version,
    )

    # handle a single file upload case.
    if abs_path.is_file():
        local_id = str(uuid4())
        file_size = abs_path.stat().st_size
        if file_size >= _MAX_FILE_SIZE:
            raise RuntimeError(
                f"file {abs_path.absolute()} exceeds the maximum file size for "
                f"uploads to grid datastores. please contact support @grid.ai"
                f"for assistance"
            )
        all_work.files[local_id] = DataFile(
            absolute_path=str(abs_path.resolve()),
            relative_file_name=abs_path.name,
            size_bytes=file_size,
            local_id=local_id,
            part_count=max(1, math.ceil(file_size / env.GRID_DATASTORE_MAX_BYTES_PER_FILE_PART_UPLOAD))
        )
        return all_work

    # if the source_path is a directory...
    for f in abs_path.glob("**/*"):
        if f.is_dir():
            continue

        if f.is_symlink():
            warnings.warn(f"Cannot upload symlinked files. Skipping: {str(f)}", category=UserWarning)
            continue

        local_id = str(uuid4())
        file_size = f.stat().st_size
        if file_size >= _MAX_FILE_SIZE:
            raise RuntimeError(
                f"file {f.absolute()} exceeds the maximum file size for "
                f"uploads to grid datastores. please contact support @grid.ai"
                f"for assistance."
            )

        all_work.files[local_id] = DataFile(
            absolute_path=str(f.resolve()),
            relative_file_name=str(f.relative_to(abs_path)),
            size_bytes=file_size,
            local_id=local_id,
            part_count=max(1, math.ceil(file_size / env.GRID_DATASTORE_MAX_BYTES_PER_FILE_PART_UPLOAD))
        )

    return all_work


def initialize_progress_bar(work: Work) -> PBar:
    current_part_progress, total_part_count = 0, 0
    current_byte_progress, total_byte_count = 0, 0
    current_finalize_progress, total_finalize_files = 0, 0

    for file in work.files.values():
        total_byte_count += file.size_bytes
        total_part_count += int(file.part_count)
        total_finalize_files += 1

        if file.is_uploaded:
            current_byte_progress += file.size_bytes
            current_part_progress += int(file.part_count)
        if file.is_marked_complete:
            current_finalize_progress += 1

    upload_progress_bytes = Progress(
        TextColumn("[progress.description]{task.description}", justify="right"),
        BarColumn(bar_width=None),
        "[progress.percentage]{task.percentage:>3.1f}%",
        "•",
        DownloadColumn(),
        "•",
        TransferSpeedColumn(),
    )

    upload_progress_files = Progress(
        TextColumn("[progress.description]{task.description}", justify="right"),
        BarColumn(bar_width=None),
        "{task.completed} / {task.total} Parts Completed",
    )

    finalize_progress = Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=None),
        TextColumn("{task.completed} / {task.total} File Parts"),
    )

    action_status = Status("[bold yellow] Initializing Upload")

    # group of progress bars;
    # some are always visible, others will disappear when progress is complete
    progress_group = Group(
        Panel(Group(upload_progress_files, upload_progress_bytes, finalize_progress)),
        action_status,
    )

    upload_p_bytes_id = upload_progress_bytes.add_task("Upload Progress (Data Bytes)")
    upload_p_files_id = upload_progress_files.add_task("Upload Progress (File Parts)")
    finalize_p_id = finalize_progress.add_task("Finalizing Upload", visible=False)

    upload_progress_bytes.refresh()
    upload_progress_files.refresh()
    finalize_progress.refresh()

    return PBar(
        p_upload_bytes=upload_progress_bytes,
        p_upload_files=upload_progress_files,
        p_finalize=finalize_progress,
        upload_bytes_beginning_advance=current_byte_progress,
        upload_bytes_total=total_byte_count,
        upload_files_beginning_advance=current_part_progress,
        upload_files_total=total_part_count,
        finalize_beginning_advance=current_finalize_progress,
        finalize_total=total_finalize_files,
        progress_group=progress_group,
        upload_files_task_id=upload_p_files_id,
        upload_bytes_task_id=upload_p_bytes_id,
        finalize_task_id=finalize_p_id,
        action_status=action_status
    )


# ----------------------- perform upload -----------------------------


def _get_next_upload_batch(work: Work) -> List[DataFile]:
    num_bytes, num_files = 0, 0
    next_batch = []
    for file in work.files.values():
        if file.is_uploaded:
            continue
        next_batch.append(file)
        num_bytes += file.size_bytes
        num_files += 1
        # ordering is important here in case there is a very large
        # files which exceeds the MAX_BYTES_PER_BATCH_UPLOAD limit.
        if num_bytes > env.GRID_DATASTORE_MAX_BYTES_PER_BATCH_UPLOAD or num_files >= env.GRID_DATASTORE_MAX_FILES_PER_UPLOAD_BATCH:
            break

    return next_batch


def _do_upload(session: requests.Session, file_path: Path, task: UploadTask, progress_bar: PBar) -> UploadTask:
    """Do upload, fill ETag value in UploadTask
    """
    if done_event.is_set():
        return task

    with file_path.open("rb") as file:
        file.seek(task.read_offset_bytes)
        data = file.read(task.read_range_bytes)
        bytes_read = len(data)

    response = session.put(task.url, data=data)
    if 'ETag' not in response.headers:
        raise ValueError(f"Unexpected response from S3, response: {response.content}")
    task.etag = str(response.headers['ETag']).strip('"')

    progress_bar.p_upload_bytes.update(progress_bar.upload_bytes_task_id, advance=bytes_read)
    progress_bar.p_upload_files.update(progress_bar.upload_files_task_id, advance=1)
    return task


def _upload_next_batch(c: 'GridRestClient', work: Work, progress_bar: PBar) -> Dict[str, DataFile]:
    upload_objects = []
    batch = _get_next_upload_batch(work)
    if len(batch) == 0:
        return {}

    for file in batch:
        up_obj = datastore_upload_object_from_data_file(file)
        upload_objects.append(up_obj)

    responses = create_presigned_urls(
        c=c,
        cluster_id=work.cluster_id,
        datastore_id=work.datastore_id,
        upload_objects=upload_objects,
    )

    batch_files = {}
    for resp, file in zip(responses, batch):
        file.upload_id = resp.upload_id
        file.expiry_time = resp.expiry_time
        file.part_count = resp.part_count
        for idx, url in enumerate(resp.urls):
            offset = idx * env.GRID_DATASTORE_MAX_BYTES_PER_FILE_PART_UPLOAD
            file.tasks.append(
                UploadTask(
                    data_file_local_id=file.local_id,
                    part_number=url.part_number,
                    url=url.url,
                    read_offset_bytes=offset,
                    read_range_bytes=env.GRID_DATASTORE_MAX_BYTES_PER_FILE_PART_UPLOAD,
                )
            )
        batch_files[file.local_id] = file

    # We can use a with statement to ensure threads are cleaned up promptly
    retries = Retry(total=5, status_forcelist=[500, 503])
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor, requests.Session() as s:
        s.mount('https://', HTTPAdapter(pool_connections=20, pool_maxsize=20, max_retries=retries))

        futures = []
        uploaded_file_tasks: Dict[str, List[UploadTask]] = defaultdict(list)
        for file in batch_files.values():
            file_path = Path(file.absolute_path)
            for task in file.tasks:
                futures.append(executor.submit(_do_upload, s, file_path, task, progress_bar))

        for future in concurrent.futures.as_completed(futures):
            res = future.result()
            uploaded_file_tasks[res.data_file_local_id].append(res)

    for k in list(uploaded_file_tasks.keys()):
        uploaded_file_tasks[k] = sorted(uploaded_file_tasks[k], key=lambda x: int(x.part_number))

    completed_files: Dict[str, DataFile] = {}
    for data_file_local_id, completed_tasks in uploaded_file_tasks.items():
        completed_file = batch_files[data_file_local_id]
        completed_file.tasks = completed_tasks
        completed_file.is_uploaded = True
        completed_files[data_file_local_id] = completed_file

    return completed_files


def _start_upload(c: 'GridRestClient', grid_dir: Path, work: Work, progress_bar: PBar) -> Work:
    """Entrypoint to begin processing file uploads.
    """
    while True:
        if done_event.is_set():
            # stop progression since we're in trouble.
            raise RuntimeError("Termination signal (ie. SIGINT, SIGTERM, or SIGKILL) received")

        progress_bar.action_status.update(progress_bar.status_text_uploading)

        completed_files = _upload_next_batch(c=c, work=work, progress_bar=progress_bar)
        if done_event.is_set():
            # don't save if we're not sure that everything completed uploading.
            raise RuntimeError("Termination signal (ie. SIGINT, SIGTERM, or SIGKILL) received")

        if len(completed_files) == 0:
            break
        for file_id, file in completed_files.items():
            work.files[file_id] = file

        progress_bar.action_status.update(progress_bar.status_text_saving)
        _save_work_state(grid_dir, work)

    return work


# ---------------------------- perform finalize ---------------------------


def _get_next_finalize_batch(work: Work) -> List[DataFile]:
    next_batch = []
    num_tasks = 0
    for file in work.files.values():
        if file.is_marked_complete:
            continue
        next_batch.append(file)
        num_tasks += len(file.tasks)
        # ordering is important here in case this value is somehow set to 0.
        if num_tasks >= env.GRID_DATASTORE_MAX_FILES_PER_FINALIZE_BATCH:
            break

    return next_batch


def _start_finalize(c: 'GridRestClient', grid_dir: Path, work: Work, progress_bar: PBar) -> Work:
    """Entrypoint to finalize uploaded files.
    """
    progress_bar.p_finalize.update(progress_bar.finalize_task_id, visible=True)

    while True:
        if done_event.is_set():
            raise RuntimeError("Termination signal (ie. SIGINT, SIGTERM, or SIGKILL) received")

        progress_bar.action_status.update(progress_bar.status_text_finalizing)
        completed_batch = _get_next_finalize_batch(work)
        if len(completed_batch) == 0:
            break

        complete_presigned_url_upload(
            c=c, cluster_id=work.cluster_id, datastore_id=work.datastore_id, data_files=completed_batch
        )
        completed_parts = 0
        for completed_file in completed_batch:
            work.files[completed_file.local_id].is_marked_complete = True
            completed_parts += int(work.files[completed_file.local_id].part_count)

        progress_bar.p_finalize.update(progress_bar.finalize_task_id, advance=completed_parts)
        progress_bar.action_status.update(progress_bar.status_text_saving)
        _save_work_state(grid_dir=grid_dir, work=work)

    return work


# ------------------------- module user methods ---------------------------


def resume_datastore_upload(client: 'GridRestClient', grid_dir: Path, work: Work):
    pbar = initialize_progress_bar(work)
    with Live(pbar.progress_group):
        pbar.p_upload_bytes.update(
            pbar.upload_bytes_task_id, advance=pbar.upload_bytes_beginning_advance, total=int(pbar.upload_bytes_total)
        )
        pbar.p_upload_files.update(
            pbar.upload_files_task_id, advance=pbar.upload_files_beginning_advance, total=pbar.upload_files_total
        )
        pbar.p_finalize.update(
            pbar.finalize_task_id, advance=pbar.finalize_beginning_advance, total=pbar.finalize_total, visible=False
        )

        _start_upload(c=client, grid_dir=grid_dir, work=work, progress_bar=pbar)
        _start_finalize(c=client, grid_dir=grid_dir, work=work, progress_bar=pbar)
        mark_datastore_upload_complete(c=client, cluster_id=work.cluster_id, datastore_id=work.datastore_id)
        pbar.action_status.update(pbar.status_text_done)
        _remove_work_state(grid_dir=grid_dir, datastore_id=work.datastore_id)
    return True


def begin_new_datastore_upload(
    client: 'GridRestClient', grid_dir: Path, source_path: Path, cluster_id: str, datastore_id: str,
    datastore_name: str, datastore_version: str, creation_timestamp: datetime.datetime
):
    creation_timestamp = int(time.mktime(creation_timestamp.timetuple()))  # convert to unix time

    work = initialize_upload_work(
        name=datastore_name,
        version=datastore_version,
        datastore_id=datastore_id,
        cluster_id=cluster_id,
        creation_timestamp=creation_timestamp,
        source_path=str(source_path),
    )
    pbar = initialize_progress_bar(work)

    with Live(pbar.progress_group):
        pbar.p_upload_bytes.update(
            pbar.upload_bytes_task_id, advance=pbar.upload_bytes_beginning_advance, total=int(pbar.upload_bytes_total)
        )
        pbar.p_upload_files.update(
            pbar.upload_files_task_id, advance=pbar.upload_files_beginning_advance, total=pbar.upload_files_total
        )
        pbar.p_finalize.update(
            pbar.finalize_task_id, advance=pbar.finalize_beginning_advance, total=pbar.finalize_total, visible=False
        )

        _start_upload(c=client, grid_dir=grid_dir, work=work, progress_bar=pbar)
        _start_finalize(c=client, grid_dir=grid_dir, work=work, progress_bar=pbar)
        mark_datastore_upload_complete(c=client, cluster_id=cluster_id, datastore_id=datastore_id)
        pbar.action_status.update(pbar.status_text_done)
        _remove_work_state(grid_dir=grid_dir, datastore_id=datastore_id)

    return True
