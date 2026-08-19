import json

from xpipe_api import Client

if __name__ == "__main__":
    client = Client()

    # The text source can also support external script sources like git repositories
    data = {
        "type": "script",
        "initScript": True,
        "runnableScript": True,
        "shellScript": False,
        "fileScript": False,
        "textSource": {
            "type": "inPlace",
            "dialect": "sh",
            "text": "echo hello\necho from\necho my\necho script"
        }
    }

    # The custom scripts category UUID
    category = "d3496db5-b709-41f9-abc0-ee0a660fbab9"

    # The validate option controls whether XPipe should verify that a connection can be established to the system
    client.store_add(name="My Script", conn_data=data, validate=False, category=category)
