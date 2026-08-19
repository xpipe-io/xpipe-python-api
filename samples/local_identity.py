import json

from xpipe_api import Client

if __name__ == "__main__":
    client = Client()

    raw_password_auth = {
        'type': 'passwordManager',
        'key': "<identifier of password in password manager>"
    }
    encrypted_password_auth = client.secret_encrypt_default(json.dumps(raw_password_auth))

    raw_key = {
        'type': 'none',
    }
    encrypted_key = client.secret_encrypt_default(json.dumps(raw_key))

    data = {
        "type": "localIdentity",
        "username": "User",
        "password": encrypted_password_auth,
        "sshIdentity": encrypted_key
    }

    # Local Identities category
    category = "e784de4e-abea-4cb8-a839-fc557cd23097"

    client.store_add(name="My Local Identity", conn_data=data, validate=False, category=category)
