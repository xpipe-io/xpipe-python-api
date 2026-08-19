import json

from xpipe_api import Client

if __name__ == "__main__":
    client = Client()

    # Opens a terminal session for a connection
    client.action(json.loads('''{
      "id" : "open",
      "ref" : "f0ec68aa-63f5-405c-b178-9a4454556d6b"
    }'''), confirm=False)

    # Toggles the session state for a store. If this store is a tunnel, then this operation will start or stop the tunnel
    client.action(json.loads('''{
      "id" : "toggleStore",
      "ref" : "4dc0c7d4-083e-446e-8a75-7a29490eaec1",
      "enabled" : true
    }'''), confirm=False)

    # Run a file browser action like chmod
    client.action(json.loads('''{
      "id" : "chmod",
      "ref" : "1aa86bc3-9ab8-4b2e-b3bc-dd028d142faf",
      "files" : [ "/home/ubuntu/archive.tar.gz" ],
      "permissions" : "755",
      "recursive" : false
    }'''), confirm=False)

    # The confirm option gives you a GUI dialog to first confirm
    # the action with the parameters before executing it to prevent any mistakes