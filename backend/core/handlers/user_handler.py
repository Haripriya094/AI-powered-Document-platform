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
                res = self.user_collection.insert_one({"name": name, "password": password})
                print(f"Inserted new user: {res}")
            return True
        except Exception as error:
            print(f"Error: {error}")

    def register(self, input_data):
        try:
            name = input_data.username
            password = input_data.password
            department = input_data.department
            salary = input_data.salary
            print(f"Attempting registration for: {name}")

            existing_user = self.user_collection.find_one({"name": name})
            if existing_user:
                print(f"User already exists: {name}")
                return False

            res = self.user_collection.insert_one({
                "name": name,
                "password": password,
                "department": department,
                "salary": salary
            })
            print(f"Inserted new user: {res}")
            return True
        except Exception as error:
            print(f"Error: {error}")
            return False