from db import DataBase
from secureEngine import Secure

class Engine:
    
    ### Private Account and Security variables
    __db = None
    __security = None
        
    ###
    def __init__(self, name, username, password, uri):
        self.name = name
        self.username = username
        self.password = password
        self.uri = uri
    
    ### 
    def __init__(self):
        self.name = ""
        self.username = ""
        self.password = ""
        self.uri = ""
        self.__db = DataBase()
        self.__security = Secure()
        
        
    ### Stringify the class
    def __str__(self):
        pass
    
    
    ### Ensure password and others fields are corrects using class Secure
    def sanityPassword(self, password_list: list):
        return self.__security.passwordValidation(password_list['name'], password_list['username'], password_list['password'], password_list['uri'])


    ### Manage login operations (new o log a user)
    def account(self, name, password, is_new):
        self.__security.checkInjection(name)
        self.__security.checkInjection(password)
        return self.__db.account({"username": name, "password": password}, is_new)
        
    ### Call account class to store a new password
    def addPassword(self, username: str, line_password: list) -> bool:
        return self.__db.insertFields(username, line_password)
    
    
    ### Delete password based by account username and if it exists
    def deletePassword(self, username:str, id: int) -> bool:
        return self.__db.deletePassword(username, id)
    
    
    ###
    def getAllPasswords(self, username:str) -> list:
        return self.__db.getPasswords(username)
