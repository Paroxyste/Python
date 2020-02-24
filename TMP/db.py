from pymongo import MongoClient

class DB:
    def __init__(self, db_name):
        self.client = MongoClient('localhost', 27017)
        self.db_name = db_name

    def reset(self):
        self.client.drop_database(self.db_name)

    def bulk_insert(self, collection, obj_list):
        obj_dict = [vars(x) for x in obj_list]
        self.client[self.db_name][collection].insert_many(obj_dict)