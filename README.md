# XPipe Python API

[![GitHub license](https://img.shields.io/github/license/xpipe-io/xpipe-python-api.svg)](https://github.com/coandco/python_xpipe_api/blob/master/LICENSE)
[![PyPI version](https://img.shields.io/pypi/v/xpipe_api)](https://pypi.org/project/xpipe_api/)

Python client for the XPipe API. This library is a wrapper for the raw [HTTP API](https://github.com/xpipe-io/xpipe/blob/master/openapi.yaml) and intended to make working with it more convenient.

## Installation
```
python3 -m pip install xpipe_api
```

## Usage

```python
from xpipe_api import Client

# By default, Client() will read an access key from the file xpipe_auth on the local filesystem
# and talk to the XPipe HTTP server on localhost.  To connect to a remote instance with an API
# key, use Client(token="foo", base_url = "http://servername:21721")
client = Client()

# connection_query accepts glob-based filters on the category, connection name, and connection type
all_connections = client.connection_query()

# Each connection includes uuid, category, connection, and type information
first_connection_uuid = all_connections[0]["uuid"]

# Before any shell commands can be run, a shell session must be started on a connection
client.shell_start(first_connection_uuid)

# Prints {'exitCode': 0, 'stdout': 'hello world', 'stderr': ''}
print(client.shell_exec(first_connection_uuid, "echo hello world"))

# Clean up after ourselves by stopping the shell session
client.shell_stop(first_connection_uuid)
```

There's also an async version of the client that can be accessed as AsyncClient:

```python
import asyncio
from xpipe_api import AsyncClient


async def main():
    # By default, Client() will read an access key from the file xpipe_auth on the local filesystem
    # and talk to the XPipe HTTP server on localhost.  To connect to a remote instance with an API
    # key, use Client(token="foo", base_url = "http://servername:21721")
    client = AsyncClient()

    # connection_query accepts glob-based filters on the category, connection name, and connection type
    all_connections = await client.connection_query()

    # Each connection includes uuid, category, connection, and type information
    first_connection_uuid = all_connections[0]["uuid"]

    # Before any shell commands can be run, a shell session must be started on a connection
    await client.shell_start(first_connection_uuid)

    # Prints {'exitCode': 0, 'stdout': 'hello world', 'stderr': ''}
    print(await client.shell_exec(first_connection_uuid, "echo hello world"))

    # Clean up after ourselves by stopping the shell session
    await client.shell_stop(first_connection_uuid)


if __name__ == "__main__":
    asyncio.run(main())
```

This is only a short summary of the library. You can find more supported functionalities in the source itself.

## Tests

To run the test suite, you'll need to define the XPIPE_APIKEY env var.  This will allow the two "log in with the ApiKey 
rather than Local method" tests to work.  Here's the recommended method for running the tests with poetry:

```commandline
cd /path/to/python_xpipe_api
poetry install
XPIPE_APIKEY=<api_key> poetry run pytest
```