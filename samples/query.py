from xpipe_api import Client

if __name__ == "__main__":
    client = Client()

    # store_query accepts glob-based filters on the category, store name, and store type

    # Find all stores in the default category and all its subcategories
    stores = client.store_query(categories="all connections/default**")

    # Find all stores in the subcategories of default
    stores = client.store_query(categories="all connections/default/**")

    # Find all stores in the default category without any subcategories
    stores = client.store_query(categories="all connections/default")

    # Find all top level stores in the default category
    stores = client.store_query(categories="all connections/default", stores="*")

    # Find all stores in the default category, including any children
    stores = client.store_query(categories="all connections/default", stores="**")

    # Find all SSH config stores on the local machine
    stores = client.store_query(categories="all connections/default", stores="Local Machine/SSH user config/*")

    # Find only ssh config host stores in the "MyCategory" category that has the word "MyCompany" in its name
    # - Searching for strings is case-insensitive here
    # - This will not include subcategories of "MyCategory"
    # - You can find all the available store type names by just querying all stores and taking a look add the individual type names of the stores.
    stores = client.store_query(categories="**/MyCategory", types="sshConfigHost", stores="*MyCompany*")

    # Query a specific store by name in a category
    # This will only return one element, so we can just access that
    store = client.store_query(categories="**/MyCategory", stores="MyConnectionName")[0]

    # Query the local machine connection
    store = client.store_query(stores="Local Machine")[0]

    # A store reference is just a UUID string, so you can also specify it fixed
    store = "f0ec68aa-63f5-405c-b178-9a4454556d6b"