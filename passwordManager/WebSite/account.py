from db import DataBase
from __inspection__ import currentLine


class Account:
    __db = None

    ### Initialize the database each time
    def __init__(self):
        print(currentLine("account"))
        self.__db = DataBase()
        
    
    ### List all users authenticated on the web page
    def __listUsers(self):
        pass


    ### List all passwords saved on the web page
    def __listPasswords(self):
        pass
     
        
    ### Create a new account and add to db
    def createAccount(self, username, password) -> bool:
        return self.__db.account({'username': username, 'password': password}, True)

    
    ### Check login of account and login to homepage
    def loginAccount(self, username, password) -> bool:
        return self.__db.account({'username': username, 'password': password}, False)
    
    
    ### Delete an account from database
    def deleteAccount(self, username, password) -> bool:
        return True
    
    
    ### Add a new password to database and create a new table password based by user account id
    def addPassswordAccount(self, username: str, password_line: list) -> bool:
        return self.__db.insertFields({"username": username}, password_line)
                
    
    ### Delete an existing password from database based by user id
    def deletePasswordAccount(self, username: str, password_line: list) -> bool:
        return self.__db.modifyFields({"username": username}, password_line)
