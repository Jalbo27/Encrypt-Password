from account import Account
from secureEngine import Secure

class Engine:
    ###

    __account = Account()
    __security = Secure()
        
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
        
    ### Stringify the class
    def __str__(self):
        pass
    
    ### Ensure password and others fields are corrects using class Secure
    def sanityPassword(self, name: str, username: str, password: str, uri: str):
        if(self.__security.passwordValidation(name, username, password, uri)):
            return True
        else:
            return False
        
    def account(self, name, password, is_new):
        if(is_new):
            return self.__account.createAccount(name, password)
        else:
            return self.__account.loginAccount(name, password)