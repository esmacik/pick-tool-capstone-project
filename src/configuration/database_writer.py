import pymongo


class DatabaseWriter:

    # Possible connection names
    COLLECTION_TEAM = "team"
    COLLECTION_EVENT = "event"
    COLLECTION_DIRECTORY = "directory"
    COLLECTION_VECTOR = "vectors"
    COLLECTION_ICON = "icons"

    # Get the database
    @staticmethod
    def connect_to_database():
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        database = client["pick_tool"]
        return database

    # Write the given dictionary to the given collection name.
    @staticmethod
    def write_dict_to_collection(dict_to_write, collection_name):
        database = DatabaseWriter.connect_to_database()
        collection = database[collection_name]
        if (collection_name == DatabaseWriter.COLLECTION_TEAM or
                collection_name == DatabaseWriter.COLLECTION_EVENT or
                collection_name == DatabaseWriter.COLLECTION_DIRECTORY):
            collection.delete_many({})
        collection.insert_one(dict_to_write)
        print("After write of " + str(dict_to_write) + " in collection " + str(collection_name) + "...")
        DatabaseWriter.print_collection(collection_name)

    # Given a query, delete one object from the database.
    @staticmethod
    def delete_one_from_collection(query, collection_name):
        database = DatabaseWriter.connect_to_database()
        collection = database[collection_name]
        collection.delete_one(query)
        print("After deletion query "+ str(query) + " in collection " + str(collection_name) + "...")
        DatabaseWriter.print_collection(collection_name)

    # Given a collection name, return a list of all documents in the collection in the database.
    @staticmethod
    def get_all_documents_in_collection(collection_name):
        return [document for document in DatabaseWriter.connect_to_database()[collection_name].find()]

    # Given a collection name, print all documents in that collection.
    @staticmethod
    def print_collection(collection_name):
        print("Documents in " + collection_name + " collection:")
        for document in DatabaseWriter.connect_to_database()[collection_name].find():
            print(document)
