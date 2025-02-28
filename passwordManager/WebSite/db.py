from flask import Flask
from numpy import insert
from pymongo import MongoClient
from pymongo.server_api import ServerApi
#import sqlite3
from urllib.parse import quote_plus
from __inspection__ import currentLine


class DataBase:
    __username = None
    __password = None
    __cluster = None
    # __uri = None 
    # __client = None
    # __con = None
    # __db = None
    
    ###
    def __init__(self):
        self.initDB()
        
    
    ###
    def initDB(self): 
        # self.__con = sqlite3.connect("account.db")
        # self.__db = self.__con.cursor()
        # file = open('./sql/schema.sql', 'r')
        # sqlfile = file.read()
        # file.close()
        # commands = sqlfile.split(';')
        # for command in commands:
        #     try:    
        #         if(command != ''):
        #             print(currentLine("db"), command)
        #             self.__db.execute(command)
        #     except Exception as msg:
        #         print(currentLine("db"), msg)
        
        # cur = self.__db.execute("SELECT * FROM User;")
        # for row in cur.fetchall():
        #     print(row)

        # print(currentLine("db"), "database created")
        # self.__con.close()

        self.__username = quote_plus('alberto')
        self.__password = quote_plus('PzwX6aZW4gbhTnh')
        self.__cluster = 'pmcluster' 
        uri = f"mongodb+srv://{self.__username}:{self.__password}@{self.__cluster}.blpv7.mongodb.net/?retryWrites=true&w=majority&appName={self.__cluster}"
        print(currentLine("db"), "database created")
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
    
    
    ###
    def selectOne(self, key: str):
        pass
    
    
    ### INSERT FIELDS IN ANY TABLE 
    def insertFields(self, *fields) -> bool:
        uri = f"mongodb+srv://{self.__username}:{self.__password}@{self.__cluster}.blpv7.mongodb.net/?retryWrites=true&w=majority&appName={self.__cluster}"
        client = MongoClient(uri, server_api=ServerApi(version="1", strict=True, deprecation_errors=True))
        result = None
        try:
            client.admin.command("ping")
            print("Connection opened")
            database = client["passwordManager"] 
            
            if fields[0] == "User":
                database["User"].insert_many(fields[1:])
                return True
            elif fields[0] == "Password":
                id_user = database["User"].find(fields[1])
                print(currentLine('db'), "id: ", id_user._id)
                #result = database.get_collection(f"Password_{id_user.}")
                # if result.cursor_id != None:
                #     self.__createCollection(fields[1], client)
                return True 
            
                                    
        except Exception as e:
            print(e)
            return False
        
        # self.__con = sqlite3.connect("account.db")
        # self.__con.autocommit = True
        # self.__db = self.__con.cursor()
        # count_users = self.__db.execute("SELECT COUNT(id) FROM User").fetchall()
        # count_pass = self.__db.execute("SELECT COUNT(id) FROM Password").fetchall()
        # if(self.__db != None):
        #     try:
        #         cur = None
        #         result = []
        #         for query in queries:
        #             print(currentLine("db"), query)
        #             if(query != ''):
        #                 cur = self.__db.execute(query)
        #                 result = cur.fetchall()
        #                 if(result != []):
        #                     self.__con.close()
        #                     return result
                        
        #         if(self.__db.execute("SELECT COUNT(id) FROM User").fetchall() > count_users):
        #             print(currentLine("db"), " current users: ", self.__db.execute("SELECT COUNT(id) FROM User").fetchall())
        #             result = self.__db.execute("SELECT * FROM User").fetchall()[0 - cur.lastrowid]
        #         elif (self.__db.execute("SELECT COUNT(id) FROM Password").fetchall() > count_pass):
        #             print(currentLine("db"), " current password: ", self.__db.execute("SELECT COUNT(id) FROM Password").fetchall())
        #             result = self.__db.execute("SELECT * FROM Password").fetchall()[0 - cur.lastrowid]
                    
        #         self.__con.close()
        #         return result
        #     except Exception as msg:
        #         print(currentLine("db"), f"command not executed: {msg}")
        #         return []
        # return []