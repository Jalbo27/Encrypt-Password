import sqlite3
from db import DataBase

class Account:
    __db = DataBase()

    ###
    def __init__(self):
        pass
    
    ###
    def __listUsers(self):
        query = "SELECT * FROM User;"
        self.__db.makeQuery(query)
        
    ### Create a new account and add to db
    def createAccount(self, username, password) -> bool:
        query = f"INSERT INTO User(username, password) VALUES({username}, {password});"
        self.__db.makeQuery(query)
        self.__listUsers()
        return True
    
    ### Check login of account and login to homepage
    def loginAccount(self, name, password) -> bool:
        return True
    
    ###
    def deleteAccount(self, username, password):
        return True