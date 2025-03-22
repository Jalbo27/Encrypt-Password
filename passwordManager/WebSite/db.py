from pymongo import MongoClient
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus
from __inspection__ import currentLine


class DataBase:
    __username = None
    __password = None
    __cluster = None
    
    ### Call the initilizator of class
    def __init__(self):
        self.initDB()
        
    
    ### Initializa the Database class 
    def initDB(self): 
        self.__username = quote_plus('alberto')
        self.__password = quote_plus('PzwX6aZW4gbhTnh')
        self.__cluster = 'pmcluster' 
        uri = f"mongodb+srv://{self.__username}:{self.__password}@{self.__cluster}.blpv7.mongodb.net/?retryWrites=true&w=majority&appName={self.__cluster}"
        client = MongoClient(uri, server_api=ServerApi(version="1", strict=True, deprecation_errors=True))
        # Send a ping to confirm a successful connection
        try:
            client.admin.command('ping')
            print(currentLine("db"), "connection opened")
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)
        finally:
            client.close()
            print(currentLine("db"), "connection closed")
            
    
    ### CREATE COLLECTION IN ATLAS
    def __createCollection(self, name: str, con: MongoClient) -> bool:
        print(con.admin.command("ping"))
        con["passwordManager"].create_collection(name)
        return True
    
    
    ### Check if the user exists or not
    def account(self, user:list, is_new) -> bool:
        uri = f"mongodb+srv://{self.__username}:{self.__password}@{self.__cluster}.blpv7.mongodb.net/?retryWrites=true&w=majority&appName={self.__cluster}"
        client = MongoClient(uri, server_api=ServerApi(version="1", strict=True, deprecation_errors=True))
        result = None

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
        uri = f"mongodb+srv://{self.__username}:{self.__password}@{self.__cluster}.blpv7.mongodb.net/?retryWrites=true&w=majority&appName={self.__cluster}"
        client = MongoClient(uri, server_api=ServerApi(version="1", strict=True, deprecation_errors=True))
        result = None
        
        try:
            database = client["passwordManager"]
            id_user = database["User"].find_one(account)
            if id_user['_id'] != None:
                collect = database.get_collection(f"Password_{id_user['_id']}")
                if collect != None :
                    print(collect)
                    return collect
            client.close()
            return True if result != None else False
        ### Connection is not gone well                        
        except Exception as e:
            print(currentLine("db"), e)
            client.close()
            return False

        
    ### INSERT FIELDS IN ANY TABLE 
    def insertFields(self, *fields) -> bool:
        uri = f"mongodb+srv://{self.__username}:{self.__password}@{self.__cluster}.blpv7.mongodb.net/?retryWrites=true&w=majority&appName={self.__cluster}"
        client = MongoClient(uri, server_api=ServerApi(version="1", strict=True, deprecation_errors=True))
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
                    result = database[f"Password_{id_user['_id']}"].insert_one(fields[1], True)
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