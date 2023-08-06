from traducteur.lib.model import BaseModel
from traducteur.lib.context import MongoContext
from bson import ObjectId

class BaseModelManager:
    def __init__(self, connection_string: str, database_name):
        self.connection_string = connection_string
        self.database_name = database_name

    def exists(self, col: str, id: str):
        pass

    def insert_one(self, item: BaseModel):
        pass

    def get_one(self, col: str, id: str):
        pass

    def get_many(self, col: str, query, limit: int):
        pass

    def update_one(self, update: BaseModel):
        pass

    def delete_one(self, query):
        pass


class MongoModelManager(BaseModelManager):
    def __init__(self, connection_string: str, database_name):
        super().__init__(connection_string, database_name)

    def exists(self, col: str, id: str):
        with MongoContext(self.connection_string, self.database_name, col) as column:
            return column.count_documents({'_id': ObjectId(id)}) > 0

    def get_one(self, col: str, id: str):
        with MongoContext(self.connection_string, self.database_name, col) as column:
            query = {'_id': ObjectId(id)}
            return column.find_one(query)

    def get_many(self, col: str, query, limit: int):
        with MongoContext(self.connection_string, self.database_name, col) as column:
            return list(column.find(query).limit(limit))

    def insert_one(self, item: BaseModel):
        with MongoContext(self.connection_string, self.database_name, item._col_name) as column:
            result = column.insert_one(item.dict())
            item.id = result.inserted_id
            return item

    def update_one(self, update: BaseModel):
        with MongoContext(self.connection_string, self.database_name, update._col_name) as column:
            query = {'_id': ObjectId(update.id) }
            column.update_one(query, {"$set": update.dict()})
            return update

    def delete_one(self, item: BaseModel):
        with MongoContext(self.connection_string, self.database_name, item._col_name) as column:
            query = {'_id': ObjectId(item.id)}
            column.delete_one(query)
            return item