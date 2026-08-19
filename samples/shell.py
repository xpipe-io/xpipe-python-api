import re
from xpipe_api import Client

if __name__ == "__main__":
    client = Client()

    store = "f0ec68aa-63f5-405c-b178-9a4454556d6b"

    # This will start a shell session for the connection
    # Note that this session is non-interactive, meaning that password prompts are not supported
    shell_info = client.shell_start(store)

    # The shell dialect of the shell. For example cmd, powershell, bash, etc.
    dialect = shell_info["shellDialect"]
    # The operating system type of the system. For example, windows, linux, macos, bsd, solaris
    osType = shell_info["osType"]
    # The display name of the operating system. For example Windows 10 Home 22H2
    osName = shell_info["osName"]

    # Prints {'exitCode': 0, 'stdout': 'hello world', 'stderr': ''}
    print(client.shell_exec(store, "echo hello world"))

    # Prints {'exitCode': 0, 'stdout': '<user>', 'stderr': ''}
    print(client.shell_exec(store, "echo $USER"))

    # Prints {'exitCode': 127, 'stdout': 'invalid: command not found', 'stderr': ''}
    print(client.shell_exec(store, "invalid"))

    # Extract ssh version from system
    version_format = re.compile(r'[0-9.]+')
    ret = client.shell_exec(store, "ssh -V")
    ssh_version = version_format.findall(ret["stderr"])[0]
    print("SSH version: " + ssh_version)

    # Clean up after ourselves by stopping the shell session
    client.shell_stop(store)