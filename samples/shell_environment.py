import json

from xpipe_api import Client

if __name__ == "__main__":
    client = Client()

    # The connection schema
    data = {
        "type": "shellEnvironment",
        "commands": "echo test",
        "host": "f0ec68aa-63f5-405c-b178-9a4454556d6b",
        "shell": "pwsh",
        "elevated": False,
        "user": None,
        "scripts": None
    }

    # The target category to put this connection into
    category = "97458c07-75c0-4f9d-a06e-92d8cdf67c40"

    # The validate option controls whether XPipe should verify that a connection can be established to the system
    client.store_add(name="My Environment", conn_data=data, validate=False, category=category)
