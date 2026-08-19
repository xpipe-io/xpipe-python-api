from xpipe_api import Client

if __name__ == "__main__":
    client = Client()

    # Returns an array of UUID strings
    stores = client.store_query(categories="all connections/default")

    # Works in bulk, so it expects an array of stores
    infos = client.store_info(stores)
    # Get the first info
    info = infos[0]

    # The store UUID
    uuid = info["store"]
    # This is an array containing all category hierarchy names
    category = info["category"]
    # This is an array containing all store hierarchy names
    name = info["name"]
    # This is the store type name that you can use in the query
    type = info["type"]
    # There is also some other data for internal state management, e.g. if a tunnel is running for example