from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
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
    __jwt_db_name = None
    __jwt_connect = None
    __client_connect = None
    
    ### Call the initilizator of class
    def __init__(self):
        self.initDB()

        
    ### INITIALIZE DATABASE CLASS
    def initDB(self): 
        self.__username = os.environ['MONGO_INITDB_ROOT_USERNAME']
        self.__password = os.environ['MONGO_INITDB_ROOT_PASSWORD']
        self.__db_name = os.environ['MONGO_INITDB_DATABASE']
        self.__jwt_db_name = 'MONGO_JWT_DATABASE'
        self.__key = Fernet.generate_key()
        self.__fernet = Fernet(self.__key)
        self.__uri = f"mongodb://{self.__username}:{self.__password}@mongo"
        self.__client_connect = MongoClient(self.__uri)
        self.__jwt_connect = MongoClient(self.__uri)
        try:
            self.__client_connect.admin.command('ping')
            print(currentLine("db"), "Connection success")
            db = self.__client_connect[self.__db_name]
            results = db['User'].find({ "_id":{ '$exists': 'true' }})
            all_results = list(results)
            for document in all_results:
                print(currentLine("db"), document)
            if db["User"] == None:
                self.__createCollection("User", self.__client_connect)
            self.__client_connect.close()

        except ConnectionFailure:
            print("Server not available")
        self.__client_connect.close()
            
    
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
        self.__client_connect = MongoClient(self.__uri)
        try:
            database = self.__client_connect[self.__db_name]
            
            if is_new:
                found = database["User"].find_one({"username": username})
                if found == None:
                    print(currentLine("db"), f"Not found user called {username} and subscribe this new user")
                    result = database["User"].insert_one({"username": username, "password": self.__fernet.encrypt(password.encode())})
            else:
                user = database["User"].find_one({"username": username})
                print(currentLine("db"), user)
                if self.__fernet.decrypt(user["password"]).decode() == password:
                    print(currentLine("db"), "The decripted password is:", self.__fernet.decrypt(user["password"]).decode())
                    result = True
                    print(currentLine("db"), "Le password coincidono")
            self.__client_connect.close()
            return True if result != None else False
        ### Connection is not gone well                        
        except Exception as e:
            print(currentLine("db"), e)
            self.__client_connect.close()
            return False
        
        
    ### GET ALL PASSWORDS OF SPECIFIC ACCOUNT
    def getPasswords(self, username:str) -> list:
        self.__client_connect = MongoClient(self.__uri)
        allItems = []

        try:
            database = self.__client_connect[self.__db_name]
            id_user = database["User"].find_one({"username": username})
            if id_user['_id'] != None:
                collect = database.get_collection(f"Password_{id_user['_id']}")
                ### Check if collection is not None
                if collect != None :
                    cursor = collect.find({}, {"_id": 0})
                    ### Check if there are elements
                    if cursor.alive:
                        allItems = list(cursor)
                    for k,item in enumerate(allItems):
                        print(item["password"])
                        allItems[k]["password"] = self.__fernet.decrypt(item["password"]).decode()
                    
                    cursor.close()
                    self.__client_connect.close()
                    return allItems
            ### There are not passwords or user does not exist
            self.__client_connect.close()
            return []
        ### Connection is not gone well                        
        except Exception as e:
            print(currentLine("db"), e)
            self.__client_connect.close()
            return []

        
    ### INSERT FIELDS IN ANY TABLE 
    def insertFields(self, username: str, document: list) -> bool:
        self.__client_connect = MongoClient(self.__uri)
        result = None
        try:
            self.__client_connect.admin.command("ping")
            print(currentLine("db"), "Connection opened with database")
            database = self.__client_connect[self.__db_name] 
            
            id_user = database["User"].find_one({"username":username})
            if id_user['_id'] != None:
                collect = database.get_collection(f"Password_{id_user['_id']}")
                document["password"] = self.__fernet.encrypt(document["password"].encode())
                if(collect != None):
                    result = collect.insert_one(document, True)
                else:
                    self.__createCollection(f"Password_{id_user['_id']}", self.__client_connect)
                    result = database[f"Password_{id_user['_id']}"].insert_one(document, True)
                
                self.__client_connect.close()
                if result:
                    print(currentLine("db"), "New password inserted")
                    return True
                else: return False
            ### The specified user does not exist
            else: return False
        ### Connection is not gone well                        
        except Exception as e:
            self.__client_connect.close()
            print(currentLine("db"), e)
            return False
        
    
    ### UPDATE PASSWORD
    def updatePassword(self, account:list, document:list) -> list:
        pass


    ### DELETE A SPECIFIC PASSWORD BASED BY ACCOUNT
    def deletePassword(self, account: str, id:int) -> bool:
        self.__client_connect = MongoClient(self.__uri)

        try:
            database = self.__client_connect[self.__db_name]
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
                        print(currentLine("db"), self.getPasswords(account))
                        collect.delete_one({"id": toDelete["id"]})
                        return True if collect.count_documents({}) < old_count else False
            return False 
        except Exception as e:
            print(currentLine("db"), e)
            self.__client_connect.close()
            return False
        
    
    ### ARCHIVE JWT BOUND WITH THE OBJECT ID OF THE USER
    def JWTmanage(self, account: str, JWT: str, csrf: str, lifetime: float, action: str) -> bool:
        """
        Function for manage JWT codes in db:
        RETURNS: True if action is done correctly or False if there's a problem with any actions
        
        PARAMETERS:
            - account: str ---> name of the user
            - JWT: str ---> code of JWT
            - csrf: str ---> token double submitted
            - lifetime: int ---> session validity of jwt token
            - action: str ---> what to do with that in jwt: add - revoke - update (or refresh) token
        """
        self.__client_connect = MongoClient(self.__uri)
        self.__jwt_connect = MongoClient(self.__uri)
        db = self.__client_connect[self.__db_name]
        jwt_db = self.__jwt_connect[self.__jwt_db_name]
        jwt_collect = None
        try:
            id_user = db["User"].find_one({"username": account})
            if action == "add":
                if id_user['_id'] != None:
                    jwt_collect = jwt_db.get_collection("JWT_collection")
                    if(jwt_collect == None):
                        print(currentLine("db"), "JWT_collection does not exist and it will be created...")
                        self.__createCollection("JWT_collection", self.__jwt_connect)

                    jwt_collect.insert_one({"_id": id_user['_id'], "jwt_code": JWT, "lifetime": lifetime, "csrf_token": csrf})
                    documents = jwt_collect.find()
                    for document in documents: 
                        print( currentLine("db"), document)
                    print(currentLine("db"), "JWT inserted in the table successfully!")
                    self.__client_connect.close()
                    self.__jwt_connect.close()
                    print(currentLine("db"), "Connection to database closed.")
                    return True
                else:
                    print(currentLine("db"), f"This user: {account} doesn't exist")
                    return False
            elif action == "revoke":
                if id_user['_id'] != None:
                    jwt_collect = jwt_db.get_collection("JWT_revoke")
                    if(jwt_collect == None):
                        self.__createCollection("JWT_revoke", self.__jwt_connect)
                    
                    jwt_collect.insert_one({"_id_user": id_user['_id'], "jwt_code": JWT, "lifetime": lifetime, "csrf_token": csrf})
                    print(currentLine("db"), "JWT revoked and inserted in the table successfully!")
                    jwt_collect = jwt_db.get_collection("JWT_collection")
                    if  jwt_collect != None:
                        jwt_collect.delete_one({"_id": id_user['_id']})
                        print(currentLine("db"), "JWT token deleted from the table")
                        documents = list(jwt_collect.find())
                        for document in documents: 
                            print( currentLine("db"), document)
                    else: return False
                    self.__client_connect.close()
                    self.__jwt_connect.close()
                    return True
                else:
                    print(currentLine("db"), f"This user: {account} doesn't exist")
                    return False
            else: return False
        except Exception as e:
            print(currentLine("db"), e)
            self.__client_connect.close()
            self.__jwt_connect.close()
            return False
        
    
    def checkJWT(self, JWT:str) -> bool:
        if JWT != None: 
            self.__jwt_connect = MongoClient(self.__uri)
            jwt_db = self.__jwt_connect[self.__jwt_db_name]
            if jwt_db != None: 
                jwt_collect = jwt_db.get_collection("JWT_collection")
                if jwt_collect != None:
                    token = jwt_collect.find_one({"jwt_code": JWT})
                    print(currentLine("db"), token)
                    print(currentLine("db"), token["jwt_code"])
                    return True if token != None else False
            else: return False        
        else: return False    