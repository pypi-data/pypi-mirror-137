from typing import List, Optional

from grid.metadata import __version__
from grid.sdk.client import create_gql_client
from grid.sdk.client.grid_gql import gql_execute


def get_grid_user_id(client) -> str:
    query = """
    query Login ($cliVersion: String!) {
        cliLogin (cliVersion: $cliVersion) {
            userId
            success
            message
        }
    }
    """
    res = gql_execute(client, query, cliVersion=__version__)['cliLogin']
    return res['userId']


def get_user_basic_info():
    client = create_gql_client()
    query = """
    query {
        getUser {
            userId
            isVerified
            completedSignup
            isBlocked
            username
            firstName
            lastName
            email
        }
    }
    """
    return gql_execute(client, query)['getUser']


def get_user_teams() -> List[dict]:
    client = create_gql_client()
    query = """
        query GetUserTeams {
            getUserTeams {
                success
                message
                teams {
                    id
                    name
                    createdAt
                    role
                    members {
                        id
                        username
                        firstName
                        lastName
                    }
                }
            }
        }
    """
    result = gql_execute(client, query)
    if not result['getUserTeams'] or not result['getUserTeams']['success']:
        raise RuntimeError(result['getUserTeams']["message"])
    return result['getUserTeams']['teams']


def get_user_info():
    """Return basic information about a user."""
    client = create_gql_client()
    query = """
        query {
            getUser {
                username
                firstName
                lastName
                email

            }
        }
    """

    result = gql_execute(client, query)
    if not result['getUser']:
        raise RuntimeError(result['getUser']["message"])
    return result['getUser']


def create_datastore(name: str, source: str, cluster: Optional[str] = None):
    """Create datastore in Grids
    """
    # Create Grid datastore directly in Grid without uploading, since Grid will
    # handle extraction and creating a optimizted datastore automatically.
    client = create_gql_client()
    mutation = """
        mutation (
            $name: String!
            $source: String
            $clusterId: String
            ) {
            createDatastore (
                properties: {
                        name: $name
                        source: $source
                        clusterId: $clusterId
                    }
            ) {
            success
            message
            datastoreId
            datastoreVersion
            }
        }
    """

    params = {'name': name, 'source': source, 'clusterId': cluster}
    result = gql_execute(client, mutation, **params)
    success = result['createDatastore']['success']
    message = result['createDatastore']['message']
    if not success:
        raise ValueError(f"Unable to create datastore: {message}")

    res = result['createDatastore']
    res['datastoreVersion'] = int(res['datastoreVersion'])
    return res


def get_user():
    client = create_gql_client()
    query = """
        query {
            getUser {
                isVerified
                completedSignup
                isBlocked
            }
        }
        """
    result = gql_execute(client, query)
    return result["getUser"]
