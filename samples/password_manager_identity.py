import json

from xpipe_api import Client

if __name__ == "__main__":
    client = Client()

    # Control the access for synced identities
    scope = ["role1"]

    data = {
        "type": "passwordManagerIdentity",
        "key": "<Password manager entry identifier>",
        "accessScope": scope
    }

    # Synced identities category, only is available when sync is enabled in XPipe
    category = "69aa5040-28dc-451e-b4ff-1192ce5e1e3c"

    client.store_add(name="My Password Manager Identity", conn_data=data, validate=False, category=category)
