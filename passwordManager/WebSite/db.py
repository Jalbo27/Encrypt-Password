from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import ConnectionFailure
from urllib.parse import quote_plus
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
        myclient = MongoClient(self.__uri)
        print(currentLine("db"), "myclient: ", myclient.server_info())
        try:
            myclient.admin.command('ping')
            print(currentLine("db"), "Connection success")
            db = myclient["passwordManager"]
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
    def getPasswords(self, account:list) -> list:
        client = MongoClient(self.__uri)
        allItems = []

        try:
            database = client["passwordManager"]
            id_user = database["User"].find_one(account)
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
            print("Connection opened")
            database = client["passwordManager"] 
            
            print(currentLine("db"), fields[0])
            id_user = database["User"].find_one(fields[0])
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
    def deletePassword(self, account: list, document:list) -> bool:
        client = MongoClient(self.__uri)
        result = None

        try:
            database = client["passwordManager"]
            id_user = database["User"].find_one(account)
            if id_user['_id'] != None:
                collect = database.get_collection(f"Password_{id_user['_id']}")
                if collect != None:
                    is_active = collect.find(document)
                    if is_active.alive:
                        result = collect.delete_one(document)
                        if result != None:
                            collect.update_many(
                                {"id": 
                                 {"$exists": 
                                  "true", "$gt": document["id"]
                                 }
                                },
                                {"$set":
                                 {"id": document["id"] + 1}
                                }
                            )
                    else:
                        return False    
        except Exception as e:
            print(e)
            return False