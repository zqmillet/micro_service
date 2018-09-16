from utilities.mongo import MongoTable

class MongoDatabase:
    __database = None

    def __init__(self, database):
        self.__database = database

    def fetch_table_name_list(self):
        return self.__database.collection_names()

    def fetch_table(self, table_name):
        # if not table_name in self.fetch_table_name_list():
        #     return None

        return MongoTable(self.__database[table_name])

    def __getitem__(self, table_name):
        return self.fetch_table(table_name)
