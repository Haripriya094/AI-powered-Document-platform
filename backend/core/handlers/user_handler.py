import bcrypt

from backend.core.db.mongo import user_collection


class userManagement:
    def __init__(self):
        self.user_collection = user_collection.UserCollection()

    def login(self, input_data):
        try:
            name = input_data.username
            password = input_data.password
            print(f"Attempting login for: {name}")
            existing_user = self.user_collection.find_one({"name": name})
            print(f"Existing user: {existing_user}")
            if not existing_user:
                hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
                res = self.user_collection.insert_one({"name": name, "password": hashed_password})
                print(f"Inserted new user: {res}")
            return True
        except Exception as error:
            print(f"Error: {error}")
