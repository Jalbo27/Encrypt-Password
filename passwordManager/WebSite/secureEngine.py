import re

class Secure:
    #__translation_table = str.maketrans("","","<>--#<")
    
    def __init__(self):
        pass
    
    
    ### Check possible injection inside the field (SQL, PHP, JS, HTML(...))
    def checkInjection(self, field) -> bool:
        return True
    
    
    ### Ensure password and others fields are corrects
    def passwordValidation(self, name: str, username: str, password: str, uri: str) -> bool:
        #cpname = name.translate(self.__translation_table)
        #cpusername = username.translate(self.__translation_table)
        #cppassword = password.translate(self.__translation_table)
        #cpuri = uri.translate(self.__translation_table)
        is_match = re.match('[\w\W]{8,}', password)
        # print(f"cpname - name:          {cpname} - {name}", True if cpname == name else False)
        # print(f"cpusername - username:  {cpusername} - {username}", True if cpusername == username else False)
        # print(f"cppassword - password:  {cppassword} - {password}", True if cppassword == password else False)
        # print(f"cpuri - uri:            {cpuri} - {uri}", True if cpuri == uri else False)
        # print(f"is_match: ", is_match)
        
        # if(cpname == name and cpusername == username and cppassword == password and cpuri == uri and is_match != None):
        #if(is_match != None and check_name and check_pass and check_user and check_uri):    
        return True
        #else:
        return False
        

    ### Ensure that password and username (if needed) are secured 
    def makeSecure(self, password, username=None):
        pass