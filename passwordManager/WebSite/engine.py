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
    def account(self, name: str, password: str, is_new):
        self.__security.checkInjection(name)
        self.__security.checkInjection(password)
        return self.__db.account(name, password, is_new)
        
    ### Call account class to store a new password
    def addPassword(self, username: str, line_password: list) -> bool:
        return self.__db.insertFields(username, line_password)
    
    
    ### Delete password based by account username and if it exists
    def deletePassword(self, username:str, id: int) -> bool:
        return self.__db.deletePassword(username, id)
    
    
    ### RETRIEVE ALL PASSWORDS
    def getAllPasswords(self, username:str) -> list:
        return self.__db.getPasswords(username)
    
    
    ### ADD JWT TO THE DATABASE
    def JWT_action(self, account: str, JWT: str, csrf: str, lifetime: float, action:str) -> bool:
        """
        Function for manage JWT codes in db:
        RETURNS: True if action is done correctly or False if there's a problem with any actions
        
        PARAMETERS:
            - account:str ---> name of the user
            - JWT: str ---> code of JWT
            - csrf: str ---> token double submitted
            - lifetime: int ---> session validity of jwt token
            - action: str ---> what to do with that in jwt: add - revoke - update (or refresh) token
        """
        return self.__db.JWTRevoke(account, JWT, csrf, lifetime, action)


    ### CHECK JWT 
    def checkJWT(self, JWT):
        """
        Function to check the existence and validity of jwt passed by user
        RETURN: True if jwt exists and it's valid otherwise False
        
        PARAMETERS: 
            - JWT: str ---> JWT token
        """
        return self.__db.checkJWT(JWT)