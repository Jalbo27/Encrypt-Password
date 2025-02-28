import re

class Secure:
    __translation_table = str.maketrans("","","<>-- #<")
    __translation_pass = str.maketrans("", "", "<>--#<")
    
    def __init__(self):
        pass
    
    ### Ensure password and others fields are corrects
    def passwordValidation(self, name: str, username: str, password: str, uri: str):
        cpname = name.translate(self.__translation_table)
        cpusername = username.translate(self.__translation_table)
        cppassword = password.translate(self.__translation_pass)
        cpuri = uri.translate(self.__translation_table)
        is_match = re.fullmatch(r'[A-Za-z0-9#$%^&+=]{8,}', password)
        # print(f"cpname - name:          {cpname} - {name}")
        # print(f"cpusername - username:  {cpusername} - {username}")
        # print(f"cppassword - password:  {cppassword} - {password}")
        # print(f"cpuri - uri:            {cpuri} - {uri}")
        
        if(cpname == name and cpusername == username and cppassword == password and cpuri == uri and is_match is not None):
            return True
        else:
            return False
    
    ### Check possible injection inside the field (SQL, PHP, JS, HTML(...))
    def checkInjection(self, field):
        pass

    ### Ensure that password and username (if needed) are secured 
    def makeSecure(self, password, username=None):
        pass