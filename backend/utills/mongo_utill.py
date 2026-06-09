import logging
from typing import Dict, List, Optional, Union

from pymongo import MongoClient
from pymongo.cursor import Cursor


class MongoException(Exception):
    ...


class MongoConnect:
    def __init__(self, uri):
        try:
            self.uri = uri
            self.client = MongoClient(self.uri, connect=False)
        except Exception as e:
            raise MongoException() from e

    def __call__(self, *args, **kwargs):
        return self.client

    def __repr__(self):
        return f"Mongo Client(uri:{self.uri}, server_info={self.client.server_info()})"

    @staticmethod
    def get_base_class():
        return MongoCollectionBaseClass


class MongoCollectionBaseClass:
    def __init__(self, mongo_client, database, collection):
        self.client = mongo_client
        self.database = database
        self.collection = collection
        # Variable to preserve initiated database
        # (if  database name changes during runtime)
        self.__database = None
        self.hierarchy = ""

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(database="
            f"{self.database}, collection={self.collection})"
        )

    @property
    def project_id(self):
        return self.project_id

    def insert_one(self, data: Dict):
        """
        The function is used to inserting a document
         to a collection in a Mongo Database.
        :param data: Data to be inserted
        :return: Insert ID
        """
        try:
            database_name = self.database
            collection_name = self.collection
            db = self.client[database_name]
            collection = db[collection_name]
            response = collection.insert_one(data)
            return response.inserted_id
        except Exception as e:
            raise MongoException() from e

    def insert_many(self, data: List):
        """
        The function is used to inserting documents to a collection in a Mongo Database.
        :param data: List of Data to be inserted
        :return: Insert IDs
        """
        try:
            database_name = self.database
            collection_name = self.collection
            db = self.client[database_name]
            collection = db[collection_name]
            response = collection.insert_many(data)
            return response.inserted_ids
        except Exception as e:
            raise MongoException() from e

    def find(
            self,
            query: Dict,
            filter_dict: Optional[Dict] = None,
            sort=None,
            skip: Optional[int] = 0,
            collation: Optional[bool] = False,
            limit: Optional[int] = None,
    ) -> Cursor:
        """
        The function is used to query documents
        from a given collection in a Mongo Database
        :param query: Query Dictionary
        :param filter_dict: Filter Dictionary
        :param sort: List of tuple with key and direction. [(key, -1), ...]
        :param skip: Skip Number
        :param collation: Boolean
        :param limit: Limit Number
        :return: List of Documents
        """
        if sort is None:
            sort = []
        if filter_dict is None:
            filter_dict = {"_id": 0}
        database_name = self.database
        collection_name = self.collection
        try:
            db = self.client[database_name]
            collection = db[collection_name]
            if len(sort) > 0:
                cursor = (
                    collection.find(
                        query,
                        filter_dict,
                    )
                    .sort(sort)
                    .skip(skip)
                )
            else:
                cursor = collection.find(
                    query,
                    filter_dict,
                ).skip(skip)
            if limit:
                cursor = cursor.limit(limit)
            if collation:
                cursor = cursor.collation({"locale": "en"})

            return cursor
        except Exception as e:
            raise MongoException(str(e)) from e

    def find_one(self, query: Dict, filter_dict: Optional[Dict] = None):
        try:
            database_name = self.database
            collection_name = self.collection
            if filter_dict is None:
                filter_dict = {"_id": 0}
            db = self.client[database_name]
            collection = db[collection_name]
            return collection.find_one(query, filter_dict)
        except Exception as e:
            raise MongoException() from e

    def find_last_inserted_row(self):
        try:
            database_name = self.database
            collection_name = self.collection
            db = self.client[database_name]
            collection = db[collection_name]
            return collection.find_one(sort=[('_id', -1)])
        except Exception as e:
            raise MongoException() from e

    def get_tree_view(self, parent_id: str = "0", project_id: str = ""):
        try:
            database_name = self.database
            collection_name = self.collection
            db = self.client[database_name]
            collection = db[collection_name]
            query = {"parent_id": parent_id}
            if project_id:
                query["project_id"] = project_id
            cursor = collection.find(query, {"_id": 0})
            tree = []
            ab = {"children": [], "value": ""}
            for document in cursor:
                name = document["name"]
                node_id = document["node_id"]
                parent_id = document["parent_id"]
                if parent_id != "0":
                    self.hierarchy += f"{ab.get('value')}/{node_id}"
                else:
                    self.hierarchy = node_id
                ab = {"label": name, "value": self.hierarchy, "children": self.get_tree_view(parent_id=node_id)}
                tree.append(ab)
            return tree
        except Exception as e:
            logging.info(f"ERR IS : {str(e)}")
            return False

    def update_one(
            self,
            query: Dict,
            data: Dict,
            op: str = "$set",
            upsert: bool = False,
    ):
        """
        :param upsert:
        :param query:
        :param data:
        :param op:
        :return:
        """
        try:
            database_name = self.database
            collection_name = self.collection
            db = self.client[database_name]
            collection = db[collection_name]
            response = collection.update_one(query, {op: data}, upsert=upsert)
            return response.modified_count
        except Exception as e:
            raise MongoException() from e

    def update_many(self, query: Dict, data: Dict, op: str = "$set", upsert: bool = False):
        """

        :param upsert:
        :param query:
        :param data:
        :param op:
        :return:
        """
        try:
            database_name = self.database
            collection_name = self.collection
            db = self.client[database_name]
            collection = db[collection_name]
            response = collection.update_many(query, {op: data}, upsert=upsert)
            return response.modified_count
        except Exception as e:
            raise MongoException() from e

    def delete_many(self, query: Dict):
        """
        :param query:
        :return:
        """
        try:
            database_name = self.database
            collection_name = self.collection
            db = self.client[database_name]
            collection = db[collection_name]
            response = collection.delete_many(query)
            return response.deleted_count
        except Exception as e:
            raise MongoException() from e

    def delete_one(self, query: Dict):
        """
        :param query:
        :return:
        """
        try:
            database_name = self.database
            collection_name = self.collection
            db = self.client[database_name]
            collection = db[collection_name]
            response = collection.delete_one(query)
            return response.deleted_count
        except Exception as e:
            raise MongoException() from e

    def distinct(self, query_key: str, filter_json: Optional[Dict] = None):
        """
        :param query_key:
        :param filter_json:
        :return:
        """
        try:
            database_name = self.database
            collection_name = self.collection
            db = self.client[database_name]
            collection = db[collection_name]
            return collection.distinct(query_key, filter_json)
        except Exception as e:
            raise MongoException() from e

    def aggregate(self, pipelines: List):
        try:
            database_name = self.database
            collection_name = self.collection
            db = self.client[database_name]
            collection = db[collection_name]
            return collection.aggregate(pipelines)
        except Exception as e:
            raise MongoException() from e

    def find_count(self, doc_filter=None):
        """\
        :param doc_filter:
        :return:
        """
        try:
            if doc_filter is None:
                doc_filter = {}
            db = self.client[self.database]
            return db[self.collection].count_documents(doc_filter)
        except Exception as e:
            raise MongoException() from e

    def bulk_write(self, operation):
        try:
            database_name = self.database
            collection_name = self.collection
            database_connection = self.client[database_name]
            database_connection[collection_name].bulk_write(operation)
            return "success"
        except Exception as e:
            raise MongoException() from e

    def create_mongo_index(self, index_list: Union[str, list], **kwargs):
        """
        params: index_list - ([("key1", -1),("key2", 1)])
        Returns:
            object:
        """
        try:
            database_name = self.database
            collection_name = self.collection
            db = self.client[database_name]
            collection = db[collection_name]
            collection.create_index(keys=index_list, **kwargs)
            return True
        except Exception as e:
            raise MongoException() from e

    def list_mongo_indexes(self):
        """
        Returns:
            object:
        """
        try:
            database_name = self.database
            collection_name = self.collection
            db = self.client[database_name]
            collection = db[collection_name]
            return list(collection.list_indexes())
        except Exception as e:
            raise MongoException() from e


class MongoAggregateBaseClass:
    def __init__(
            self,
            mongo_client,
            database,
    ):
        self.client = mongo_client
        self.database = database

    def aggregate(self, collection, pipelines: List):
        try:
            database_name = self.database
            collection_name = collection
            db = self.client[database_name]
            collection = db[collection_name]
            return collection.aggregate(pipelines)
        except Exception as e:
            raise MongoException() from e
