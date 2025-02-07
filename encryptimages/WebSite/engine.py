import re
from account import Account

class Engine:
    ###
    __translation_table = str.maketrans("","","<>-- #")
    __translation_pass = str.maketrans("", "", "<>--#")
    __account = Account()
        
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
    
    ### Ensure password and others fields are corrects
    def checkSecurity(self, name: str, username: str, password: str, uri: str):
        if(self.__checkSecurity(name, username, password, uri)):
            name = name.translate(self.__translation_table)
            username = username.translate(username)
            password = password.translate(self.__translation_pass)
            uri = uri.translate(self.__translation_table)

            if(re.fullmatch(r'[A-Za-z0-9@#$%^&+=]{1,}', password)):
                return True
        else:
            return False
        
    def account(self, name, password, is_new):
        if(is_new):
            return self.__account.createAccount(name, password)
        else:
            return self.__account.loginAccount(name, password)