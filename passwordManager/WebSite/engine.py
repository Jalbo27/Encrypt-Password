from account import Account
from secureEngine import Secure

class Engine:
    
    ### Private Account and Security variables
    __account = None
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
        self.__account = Account()
        self.__security = Secure()
        
        
    ### Stringify the class
    def __str__(self):
        pass
    
    
    ### Ensure password and others fields are corrects using class Secure
    def sanityPassword(self, name: str, username: str, password: str, uri: str):
        return self.__security.passwordValidation(name, username, password, uri)


    ### Manage login operations (new o log a user)
    def account(self, name, password, is_new):
        self.__security.checkInjection(name)
        self.__security.checkInjection(password)
        if(is_new):
            return self.__account.createAccount(name, password)
        else:
            return self.__account.loginAccount(name, password)
        
    ### Call account class to store a new password
    def addPassword(self, username: str, line_password: list) -> bool:
        return self.__account.addPassswordAccount(username, line_password)
    
    
    ### Delete password based by account username and if it exists
    def deletePassword(self, username:str, id: int) -> bool:
        return self.__account.deletePasswordAccount(username, id)
    
    
    ###
    def getAllPasswords(self, username:str) -> list:
        return self.__account.getPasswords(username)
