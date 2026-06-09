from pydantic import BaseModel
from backend.constants import app_configurations
from backend.utills.mongo_utill import MongoConnect

mongo_obj = MongoConnect(uri=app_configurations.mongo_url)
mongo_client = mongo_obj()

CollectionBaseClass = mongo_obj.get_base_class()


class MongoBaseSchema(BaseModel):
    pass
