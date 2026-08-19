from xpipe_api import Client

if __name__ == "__main__":
    client = Client()

    store = "f0ec68aa-63f5-405c-b178-9a4454556d6b"

    # We need a shell for the file system
    client.shell_start(store)

    # You are responsible for decoding files in the correct file encoding
    file_bytes = client.fs_read(store, "~/.ssh/config")
    file_string = file_bytes.decode('utf-8')

    # Writing files can be done via blobs
    file_write_content = "test\nfile"
    blob_id = client.fs_blob(file_write_content)
    client.fs_write(store, blob_id, "~/test_file.txt")

    # You can do the same with script files as well
    # This will create an executable script in the system's temp directory
    script_write_content = "echo hello\necho world"
    blob_script_id = client.fs_blob(script_write_content)
    script_path = client.fs_script(store, blob_script_id)

    # You can then use this script for your commands
    # Prints {'exitCode': 0, 'stdout': 'hello\nworld', 'stderr': ''}
    print(client.shell_exec(store, "\"" + script_path + "\""))

    # Clean up after ourselves by stopping the shell session
    client.shell_stop(store)