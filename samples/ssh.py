import json

from xpipe_api import Client

if __name__ == "__main__":
    client = Client()

    # We can create JSON data either via python dicts
    raw_password_auth = {
      'type': 'inPlace',
      'value': "passw0rd"
    }
    encrypted_password_auth = client.secret_encrypt_default(json.dumps(raw_password_auth))

    # Or we can use raw JSON strings
    raw_key = '''{
      "type" : "file",
      "file" : "C:/Users/User/.ssh/key.pem",
      "password" : {
        "type" : "none"
      }
    }'''
    encrypted_key = client.secret_encrypt_default(raw_key)

    # The connection schema
    data = {
        "type": "ssh",
        "gateway": "f0ec68aa-63f5-405c-b178-9a4454556d6b",
        "host" : "myip.eu-central-1.compute.amazonaws.com",
        "port" : 22,
        "identity" : {
            "type" : "inPlace",
            "identityStore" : {
                "type" : "localIdentity",
                "username" : "User",
                "password" : encrypted_password_auth,
                "sshIdentity" : encrypted_key
            }
        },
        "dontInteractWithSystem" : False,
        "forwardX11" : False,
        "jumpServer" : False,
        "additionalOptions" : None
    }

    # The target category to put this connection into
    category = "97458c07-75c0-4f9d-a06e-92d8cdf67c40"

    # The validate option controls whether XPipe should verify that a connection can be established to the system
    client.store_add(name="My Connection", conn_data=data, validate=False, category=category)
