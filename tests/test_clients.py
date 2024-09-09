import os
from pathlib import Path

import pytest
from aiohttp.client_exceptions import ClientResponseError
from requests.exceptions import HTTPError
from xpipe_api.clients import AsyncClient, Client


@pytest.fixture
def sync_local_client():
    ptb = True if os.environ.get("XPIPE_USE_PTB", None) == '1' else False
    return Client(raise_errors=True, ptb=ptb)


@pytest.fixture
def async_local_client():
    ptb = True if os.environ.get("XPIPE_USE_PTB", None) == '1' else False
    return AsyncClient(raise_errors=True, ptb=ptb)


def test_sync_local_login(sync_local_client: Client):
    assert sync_local_client.session is None
    sync_local_client.renew_session()
    assert sync_local_client.session is not None


async def test_async_local_login(async_local_client: AsyncClient):
    assert async_local_client.session is None
    await async_local_client.renew_session()
    assert async_local_client.session is not None


def test_sync_apikey_login():
    apikey = os.environ.get("XPIPE_APIKEY", None)
    ptb = True if os.environ.get("XPIPE_USE_PTB", None) == '1' else False
    assert apikey is not None, "XPIPE_APIKEY must be defined to test ApiKey login"
    client = Client(token=apikey, ptb=ptb)
    assert client.session is None
    client.renew_session()
    assert client.session is not None


async def test_async_apikey_login():
    apikey = os.environ.get("XPIPE_APIKEY", None)
    ptb = True if os.environ.get("XPIPE_USE_PTB", None) == '1' else False
    assert apikey is not None, "XPIPE_APIKEY must be defined to test ApiKey login"
    client = AsyncClient(token=apikey, ptb=ptb)
    assert client.session is None
    await client.renew_session()
    assert client.session is not None


def test_connection_query(sync_local_client: Client):
    connections = sync_local_client.connection_query(connections="local machine")
    assert len(connections) > 0, "No connections returned"
    assert len(connections[0]) == 36, "Connection returned is not a UUID"


async def test_async_connection_query(async_local_client: AsyncClient):
    connections = await async_local_client.connection_query(connections="local machine")
    assert len(connections) > 0, "No connections returned"
    assert len(connections[0]) == 36, "Connection returned is not a UUID"


def test_connection_info(sync_local_client: Client):
    local_connection = sync_local_client.connection_query(connections="local machine")[0]
    local_info = sync_local_client.connection_info(local_connection)[0]
    assert local_info["type"] == "local"
    assert local_info["usageCategory"] == "shell"


async def test_async_connection_info(async_local_client: AsyncClient):
    local_connection = (await async_local_client.connection_query(connections="local machine"))[0]
    local_info = (await async_local_client.connection_info(local_connection))[0]
    assert local_info["type"] == "local"
    assert local_info["usageCategory"] == "shell"


def test_connection_add_remove(sync_local_client: Client):
    local_conn = sync_local_client.connection_query(connections="local machine")[0]
    if response := sync_local_client.connection_query(connections="services/xpipe_api_test"):
        sync_local_client.connection_remove(response[0])
        assert not sync_local_client.connection_query(connections="services/xpipe_api_test")
    conn_data = {"type": "customService", "remotePort": 65535, "localPort": 65535, "host": {"storeId": local_conn}}
    test_uuid = sync_local_client.connection_add("xpipe_api_test", conn_data)
    assert sync_local_client.connection_query(connections="services/xpipe_api_test")
    sync_local_client.connection_remove(test_uuid)
    assert not sync_local_client.connection_query(connections="services/xpipe_api_test")


async def test_async_connection_add_remove(async_local_client: AsyncClient):
    local_conn = (await async_local_client.connection_query(connections="local machine"))[0]
    if response := (await async_local_client.connection_query(connections="services/xpipe_api_test")):
        await async_local_client.connection_remove(response[0])
        assert not (await async_local_client.connection_query(connections="services/xpipe_api_test"))
    conn_data = {"type": "customService", "remotePort": 65535, "localPort": 65535, "host": {"storeId": local_conn}}
    test_uuid = await async_local_client.connection_add("xpipe_api_test", conn_data)
    assert (await async_local_client.connection_query(connections="services/xpipe_api_test"))
    await async_local_client.connection_remove(test_uuid)
    assert not (await async_local_client.connection_query(connections="services/xpipe_api_test"))


def test_connection_browse(sync_local_client: Client):
    # We don't want to actually cause the GUI to change, so we're just going to test that it
    # throws the proper exception when passed a bad connection UUID
    fake_conn = 'ffffffff-ffff-ffff-ffff-ffffffffffff'
    with pytest.raises(HTTPError, match="Unknown connection"):
        sync_local_client.connection_browse(fake_conn)


async def test_async_connection_browse(async_local_client: AsyncClient):
    # We don't want to actually cause the GUI to change, so we're just going to test that it
    # throws the proper exception when passed a bad connection UUID
    fake_conn = 'ffffffff-ffff-ffff-ffff-ffffffffffff'
    with pytest.raises(ClientResponseError, match="Unknown connection"):
        await async_local_client.connection_browse(fake_conn)


def test_connection_terminal(sync_local_client: Client):
    # We don't want to actually cause the GUI to change, so we're just going to test that it
    # throws the proper exception when passed a bad connection UUID
    fake_conn = 'ffffffff-ffff-ffff-ffff-ffffffffffff'
    with pytest.raises(HTTPError, match="Unknown connection"):
        sync_local_client.connection_terminal(fake_conn)


async def test_async_connection_terminal(async_local_client: AsyncClient):
    # We don't want to actually cause the GUI to change, so we're just going to test that it
    # throws the proper exception when passed a bad connection UUID
    fake_conn = 'ffffffff-ffff-ffff-ffff-ffffffffffff'
    with pytest.raises(ClientResponseError, match="Unknown connection"):
        await async_local_client.connection_terminal(fake_conn)


def test_connection_toggle(sync_local_client: Client):
    local_conn = sync_local_client.connection_query(connections="local machine")[0]
    conn_data = {"type": "customService", "remotePort": 65535, "localPort": 65535, "host": {"storeId": local_conn}}
    conn_uuid = sync_local_client.connection_add(name="xpipe_api_test", conn_data=conn_data)
    sync_local_client.connection_toggle(conn_uuid, True)
    assert sync_local_client.connection_info(conn_uuid)[0]["cache"]["sessionEnabled"]
    sync_local_client.connection_toggle(conn_uuid, False)
    assert not sync_local_client.connection_info(conn_uuid)[0]["cache"]["sessionEnabled"]
    sync_local_client.connection_remove(conn_uuid)


async def test_sync_connection_toggle(async_local_client: AsyncClient):
    local_conn = (await async_local_client.connection_query(connections="local machine"))[0]
    conn_data = {"type": "customService", "remotePort": 65535, "localPort": 65535, "host": {"storeId": local_conn}}
    conn_uuid = await async_local_client.connection_add(name="xpipe_api_test", conn_data=conn_data)
    await async_local_client.connection_toggle(conn_uuid, True)
    assert (await async_local_client.connection_info(conn_uuid))[0]["cache"]["sessionEnabled"]
    await async_local_client.connection_toggle(conn_uuid, False)
    assert not (await async_local_client.connection_info(conn_uuid))[0]["cache"]["sessionEnabled"]
    await async_local_client.connection_remove(conn_uuid)


def test_connection_refresh(sync_local_client: Client):
    local_conn = sync_local_client.connection_query(connections="local machine")[0]
    # We just want to make sure we don't get any HTTP errors when refreshing the connection
    sync_local_client.connection_refresh(local_conn)


async def test_async_connection_refresh(async_local_client: AsyncClient):
    local_conn = (await async_local_client.connection_query(connections="local machine"))[0]
    # We just want to make sure we don't get any HTTP errors when refreshing the connection
    await async_local_client.connection_refresh(local_conn)


def test_get_connections(sync_local_client: Client):
    local_info = sync_local_client.get_connections(connections="local machine")[0]
    assert local_info["type"] == "local"
    assert local_info["usageCategory"] == "shell"


async def test_async_get_connections(async_local_client: AsyncClient):
    local_info = (await async_local_client.get_connections(connections="local machine"))[0]
    assert local_info["type"] == "local"
    assert local_info["usageCategory"] == "shell"


def test_daemon_version(sync_local_client: Client):
    version_info = sync_local_client.daemon_version()
    assert set(version_info.keys()) == {"version", "canonicalVersion", "buildVersion", "pro", "jvmVersion"}


async def test_async_daemon_version(async_local_client: AsyncClient):
    version_info = await async_local_client.daemon_version()
    assert set(version_info.keys()) == {"version", "canonicalVersion", "buildVersion", "pro", "jvmVersion"}


def test_shell_start(sync_local_client: Client):
    local_connection = sync_local_client.connection_query(connections="local machine")[0]
    response = sync_local_client.shell_start(local_connection)
    assert set(response.keys()) == {"shellDialect", "osType", "osName", "ttyState", "temp"}


async def test_async_shell_start(async_local_client: AsyncClient):
    connections = await async_local_client.connection_query(connections="local machine")
    local_connection = connections[0]
    response = await async_local_client.shell_start(local_connection)
    assert set(response.keys()) == {"shellDialect", "osType", "osName", "ttyState", "temp"}


def test_shell_stop(sync_local_client: Client):
    local_connection = sync_local_client.connection_query(connections="local machine")[0]
    sync_local_client.shell_start(local_connection)
    sync_local_client.shell_stop(local_connection)


async def test_async_shell_stop(async_local_client: AsyncClient):
    connections = await async_local_client.connection_query(connections="local machine")
    local_connection = connections[0]
    await async_local_client.shell_start(local_connection)
    await async_local_client.shell_stop(local_connection)


def test_shell_exec(sync_local_client: Client):
    local_connection = sync_local_client.connection_query(connections="local machine")[0]
    sync_local_client.shell_start(local_connection)
    retval = sync_local_client.shell_exec(local_connection, "echo hello world")
    assert retval == {'exitCode': 0, "stdout": "hello world", "stderr": ""}
    sync_local_client.shell_stop(local_connection)


async def test_async_shell_exec(async_local_client: AsyncClient):
    local_connection = (await async_local_client.connection_query(connections="local machine"))[0]
    await async_local_client.shell_start(local_connection)
    retval = await async_local_client.shell_exec(local_connection, "echo hello world")
    assert retval == {'exitCode': 0, "stdout": "hello world", "stderr": ""}
    await async_local_client.shell_stop(local_connection)


def test_fs_blob(sync_local_client: Client):
    blob_id = sync_local_client.fs_blob("test")
    assert blob_id


async def test_async_fs_blob(async_local_client: AsyncClient):
    blob = await async_local_client.fs_blob("test")
    assert blob


def test_fs_write(sync_local_client: Client):
    connection = sync_local_client.connection_query(connections="local machine")[0]
    blob = sync_local_client.fs_blob("test")
    system_info = sync_local_client.shell_start(connection)
    testfile_path = Path(system_info["temp"]) / "xpipe_testfile"
    try:
        sync_local_client.fs_write(connection, blob, str(testfile_path.resolve()))
        sync_local_client.shell_stop(connection)
        assert testfile_path.read_text() == "test"
    finally:
        testfile_path.unlink(missing_ok=True)


async def test_async_fs_write(async_local_client: AsyncClient):
    connection = (await async_local_client.connection_query(connections="local machine"))[0]
    blob = await async_local_client.fs_blob("test")
    system_info = await async_local_client.shell_start(connection)
    testfile_path = Path(system_info["temp"]) / "xpipe_testfile"
    try:
        await async_local_client.fs_write(connection, blob, str(testfile_path.resolve()))
        await async_local_client.shell_stop(connection)
        assert testfile_path.read_text() == "test"
    finally:
        testfile_path.unlink(missing_ok=True)


def test_fs_script(sync_local_client: Client):
    connection = sync_local_client.connection_query(connections="local machine")[0]
    system_info = sync_local_client.shell_start(connection)
    if system_info["osType"] == "Windows":
        script = "@echo off\necho hello world"
    else:
        script = "#!/bin/sh\necho hello world"
    blob = sync_local_client.fs_blob(script)
    script_path = sync_local_client.fs_script(connection, blob)
    try:
        assert Path(script_path).read_text().strip() == script
        output = sync_local_client.shell_exec(connection, f'"{script_path}"')
        assert output["stdout"].strip() == "hello world"
        sync_local_client.shell_stop(connection)
    finally:
        Path(script_path).unlink(missing_ok=True)


async def test_async_fs_script(async_local_client: AsyncClient):
    connection = (await async_local_client.connection_query(connections="local machine"))[0]
    system_info = await async_local_client.shell_start(connection)
    if system_info["osType"] == "Windows":
        script = "@echo off\necho hello world"
    else:
        script = "#!/bin/sh\necho hello world"
    blob = await async_local_client.fs_blob(script)
    script_path = await async_local_client.fs_script(connection, blob)
    try:
        assert Path(script_path).read_text().strip() == script
        output = await async_local_client.shell_exec(connection, f'"{script_path}"')
        assert output["stdout"].strip() == "hello world"
        await async_local_client.shell_stop(connection)
    finally:
        Path(script_path).unlink(missing_ok=True)


def test_fs_read(sync_local_client: Client):
    connection = sync_local_client.connection_query(connections="local machine")[0]
    system_info = sync_local_client.shell_start(connection)
    testfile_path = Path(system_info["temp"]) / "xpipe_testfile"
    try:
        testfile_path.write_text("test")
        file_bytes = sync_local_client.fs_read(connection, str(testfile_path.resolve()))
        assert file_bytes.decode('utf-8') == "test"
        sync_local_client.shell_stop(connection)
    finally:
        testfile_path.unlink(missing_ok=True)


async def test_async_fs_read(async_local_client: AsyncClient):
    connection = (await async_local_client.connection_query(connections="local machine"))[0]
    system_info = await async_local_client.shell_start(connection)
    testfile_path = Path(system_info["temp"]) / "xpipe_testfile"
    try:
        testfile_path.write_text("test")
        file_bytes = await async_local_client.fs_read(connection, str(testfile_path.resolve()))
        assert file_bytes.decode('utf-8') == "test"
        await async_local_client.shell_stop(connection)
    finally:
        testfile_path.unlink(missing_ok=True)