import json

from xpipe_api import Client

if __name__ == "__main__":
    client = Client()

    # Control the access for synced identities
    scope = ["role1"]

    raw_password_auth = {
        'type': 'prompt'
    }
    encrypted_password_auth = client.secret_encrypt(json.dumps(raw_password_auth), scope)

    # Only available if your password manager supports retrieving SSH keys
    # raw_key = '''{
    #   "type" : "passwordManagerAgent",
    #   "identifier" : "<name of key in password manager>"
    # }'''
    raw_key = '''{
      "type" : "none",
    }'''
    encrypted_key = client.secret_encrypt(raw_key, scope)

    data = {
        "type": "syncedIdentity",
        "username": "User",
        "password": encrypted_password_auth,
        "sshIdentity": encrypted_key,
        "accessScope": scope
    }

    # Synced identities category, only is available when sync is enabled in XPipe
    category = "69aa5040-28dc-451e-b4ff-1192ce5e1e3c"

    client.store_add(name="My Synced Identity", conn_data=data, validate=False, category=category)
