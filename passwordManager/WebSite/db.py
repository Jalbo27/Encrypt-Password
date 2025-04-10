from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import ConnectionFailure
import hashlib
from urllib.parse import quote_plus

from werkzeug import Client
from __inspection__ import currentLine


class DataBase:
    __username = None
    __password = None
    __cluster = None
    __uri = None
    
    ### Call the initilizator of class
    def __init__(self):
        self.initDB()

        
    ### INITIALIZE DATABASE CLASS
    def initDB(self): 
        self.__uri = f"mongodb://root:password@mongo"
        #self.__uri = "mongodb://127.0.0.1:27017/"
        myclient = MongoClient(self.__uri)
        try:
            myclient.admin.command('ping')
            print(currentLine("db"), "Connection success")
            db = myclient["passwordManager"]
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
    def __createCollection(self, name: str, con: MongoClient) -> bool:
        try:
            print(con.admin.command("ping"))
            con["passwordManager"].create_collection(name)
            return True
        except ConnectionFailure as e:
            print(e)
            return False
    
    ### CHECK IF THE USER EXISTS OR NOT
    def account(self, user:list, is_new) -> bool:
        result = None
        client = MongoClient(self.__uri)
        try:
            database = client["passwordManager"]
            
            if is_new:
                found = database["User"].find_one(user)
                if found == None:
                    print(currentLine("db"), f"Not found user called {user['username']} and subscribe this new user")
                    result = database["User"].insert_one(user)
            else:
                result = database["User"].find_one(user)
            
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
            database = client["passwordManager"]
            id_user = database["User"].find_one({"account": username})
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
    def insertFields(self, *fields) -> bool:
        client = MongoClient(self.__uri)
        result = None
        try:
            client.admin.command("ping")
            print(currentLine("db"), "Connection opened")
            database = client["passwordManager"] 
            
            print(currentLine("db"), fields[0])
            print(currentLine("db"), fields[1])
            id_user = database["User"].find_one({"username":fields[0]})
            if id_user['_id'] != None:
                collect = database.get_collection(f"Password_{id_user['_id']}")
                if(collect != None):
                    result = collect.insert_one(fields[1], True)
                else:
                    self.__createCollection(f"Password_{id_user['_id']}", client)
                    result = database[f"Password_{id_user['_id']}"].insert_one(fields[1], True)
                
                client.close()
                return True if result != None else False
            ### The specified user does not exist
            else:
                return False
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
        result = None

        try:
            database = client["passwordManager"]
            id_user = database["User"].find_one({"username": account})
            if id_user['_id'] != None:
                collect = database.get_collection(f"Password_{id_user['_id']}")
                old_count = collect.count_documents({})
                if collect != None:
                    toDelete = collect.find({"id": id})
                    if toDelete != None:
                        cur_updated = toDelete.next()
                        for element in list(collect.find({"id": { "$exists": "true", "$gt": cur_updated["id"]}})):
                            print(element['id'])
                            cur_updated = collect.find_one_and_update({"id": element["id"]}, {"$set": {"id": int(element["id"]) - 1}})
                            print(currentLine("db"), cur_updated)
                            cur_updated["id"] = element["id"] + 1
                        
                        result = collect.delete_one({"id": id})
                        print(currentLine("db"), self.getPasswords(account))
                        print(currentLine("db"), collect.count_documents({}))
                        client.close()
                        return True if collect.count_documents({}) < old_count else False
            return False 
        except Exception as e:
            print(e)
            client.close()
            return False