from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import hashlib
from cryptography.fernet import Fernet
import os
from __inspection__ import currentLine


class DataBase:
    __username = None
    __password = None
    __uri = None
    __db_name = None
    __key = None
    __fernet = None
    
    ### Call the initilizator of class
    def __init__(self):
        self.initDB()

        
    ### INITIALIZE DATABASE CLASS
    def initDB(self): 
        self.__username = os.environ['MONGO_INITDB_ROOT_USERNAME']
        self.__password = os.environ['MONGO_INITDB_ROOT_PASSWORD']
        self.__db_name = os.environ['MONGO_INITDB_DATABASE']
        self.__key = Fernet.generate_key()
        self.__fernet = Fernet(self.__key)
        print(self.__username, self.__password, self.__db_name)
        self.__uri = f"mongodb://{self.__username}:{self.__password}@mongo"
        myclient = MongoClient(self.__uri)
        try:
            myclient.admin.command('ping')
            print(currentLine("db"), "Connection success")
            db = myclient[self.__db_name]
            results = db['User'].find({ "_id":{ '$exists': 'true' }})
            all_results = list(results)
            for document in all_results:
                print(currentLine("db"), document)
            if db["User"] == None:
                self.__createCollection("User", myclient)
            myclient.close()

        except ConnectionFailure:
            print("Server not available")
        myclient.close()
            
    
    ### CREATE COLLECTION IN ATLAS
    def __createCollection(self, username: str, con: MongoClient) -> bool:
        try:
            print(con.admin.command("ping"))
            con[self.__db_name].create_collection(username)
            return True
        except ConnectionFailure as e:
            print(e)
            return False
    
    ### CHECK IF THE USER EXISTS OR NOT
    def account(self, username: str, password: str, is_new: bool) -> bool:
        result = None
        client = MongoClient(self.__uri)
        try:
            database = client[self.__db_name]
            
            if is_new:
                found = database["User"].find_one({"username": username})
                if found == None:
                    print(currentLine("db"), f"Not found user called {username} and subscribe this new user")
                    result = database["User"].insert_one({"username": username, "password": self.__fernet.encrypt(password.encode())})
            else:
                result = database["User"].find_one({"username": username})
            
            client.close()
            return True if result != None else False
        ### Connection is not gone well                        
        except Exception as e:
            print(currentLine("db"), e)
            client.close()
            return False
        
        
    ### GET ALL PASSWORDS OF SPECIFIC ACCOUNT
    def getPasswords(self, username:str) -> list:
        client = MongoClient(self.__uri)
        allItems = []

        try:
            database = client[self.__db_name]
            id_user = database["User"].find_one({"username": username})
            if id_user['_id'] != None:
                collect = database.get_collection(f"Password_{id_user['_id']}")
                ### Check if collection is not None
                if collect != None :
                    cursor = collect.find({}, {"_id": 0})
                    ### Check if there are elements
                    if cursor.alive:
                        allItems = list(cursor)
                    print (allItems)
                    cursor.close()
                    client.close()
                    return allItems
            ### There are not passwords or user does not exist
            client.close()
            return []
        ### Connection is not gone well                        
        except Exception as e:
            print(currentLine("db"), e)
            client.close()
            return []

        
    ### INSERT FIELDS IN ANY TABLE 
    def insertFields(self, username: str, document: list) -> bool:
        client = MongoClient(self.__uri)
        result = None
        try:
            client.admin.command("ping")
            print(currentLine("db"), "Connection opened")
            database = client[self.__db_name] 
            
            id_user = database["User"].find_one({"username":username})
            if id_user['_id'] != None:
                collect = database.get_collection(f"Password_{id_user['_id']}")
                document["password"] = self.__fernet.encrypt(document["password"].encode())
                if(collect != None):
                    result = collect.insert_one(document, True)
                else:
                    self.__createCollection(f"Password_{id_user['_id']}", client)
                    result = database[f"Password_{id_user['_id']}"].insert_one(document, True)
                
                client.close()
                if result:
                    print(currentLine("db"), "New password inserted")
                    return True
                else: return False
            ### The specified user does not exist
            else: return False
        ### Connection is not gone well                        
        except Exception as e:
            client.close()
            print(currentLine("db"), e)
            return False
        
    
    ### UPDATE PASSWORD
    def updatePassword(self, account:list, document:list) -> list:
        pass


    ### DELETE A SPECIFIC PASSWORD BASED BY ACCOUNT
    def deletePassword(self, account: str, id:int) -> bool:
        client = MongoClient(self.__uri)

        try:
            database = client[self.__db_name]
            id_user = database["User"].find_one({"username": account})
            if id_user['_id'] != None:
                collect = database.get_collection(f"Password_{id_user['_id']}")
                old_count = collect.count_documents({})
                if collect != None:
                    toDelete = collect.find_one({"id": id})
                    if toDelete != None:
                        cur_updated = toDelete
                        for element in list(collect.find({"id": { "$exists": "true", "$gt": cur_updated["id"]}})):
                            cur_updated = collect.find_one_and_update({"id": element["id"]}, {"$set": {"id": int(element["id"]) - 1}})
                            cur_updated["id"] = element["id"] + 1

                        collect.delete_one({"id": toDelete["id"]})
                        return True if collect.count_documents({}) < old_count else False
            return False 
        except Exception as e:
            print(e)
            client.close()
            return False
