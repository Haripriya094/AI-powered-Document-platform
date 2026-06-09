from backend.constants import app_configurations, app_constants
from backend.core.db.mongo import CollectionBaseClass, MongoBaseSchema, mongo_client


class UserCollectionSchema(MongoBaseSchema):
    pass


class UserCollection(CollectionBaseClass):
    def __init__(self):
        super().__init__(
            mongo_client,
            database=app_configurations.mongo_db,
            collection=app_constants.mongo_collection.USER_COLLECTION,
        )
