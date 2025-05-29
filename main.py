from typing import Tuple
from helix import Client, Query


class CreateUser(Query):
    
    def __init__(self, user: Tuple[str, int, str, int]):
        super().__init__()
        self.user = user

    def query(self):
        return [{ "name": self.user[0], "age": self.user[1], "email": self.user[2], "now": self.user[3] }]

    def response(self, response):
        print(response)
        return response

class GetUsers(Query):
    def __init__(self):
        super().__init__()

    def query(self):
        return [{}]

    def response(self, response):
        return response

db = Client(local=True)

user = ("John", 21, "john@example.com", 1717000000)

# implement response on Query class
res0 = db.query(CreateUser(user))
print("CreateUser")
print(res0)

# print(db.query(addUser(user)))

res1 = db.query(GetUsers())
print("GetUsers")
print(len(res1[0]['users']))