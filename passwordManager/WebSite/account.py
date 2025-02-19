from db import DataBase

class Account:
    __db = None

    ### Initialize the database each time
    def __init__(self):
        self.__db = DataBase()
    
    ### List all users authenticated on the web page
    def __listUsers(self):
        query = "SELECT * FROM User;"
        print(self.__db.makeQuery(query))

    ### List all passwords saved on the web page
    def __listPasswords(self):
        query = "SELECT * FROM Password;"
        print(self.__db.makeQuery(query))

        
    ### Create a new account and add to db
    def createAccount(self, username, password) -> bool:
        query = f"INSERT INTO User (username, password) VALUES(\'{username}\', \'{password}\');"
        if (self.__db.makeQuery(query) != []):
            self.__listUsers()
            return True
        
        self.__listUsers()
        return False
    
    ### Check login of account and login to homepage
    def loginAccount(self, username, password) -> bool:
        query = f"SELECT name, password FROM User WHERE \'{username}\' = username AND \'{password}\' = password;"
        if(self.__db.makeQuery(query) != []):
            return True
        
        return False
    
    ### Delete an account from database
    def deleteAccount(self, username, password) -> bool:
        return True
    
    ### Add a new password to database based by user id
    def addPassswordAccount(self, username: str, password_line: dict) -> bool:
        id_user = self.__db.makeQuery(f"SELECT id FROM User WHERE username = \'{username}\';")
        query = f"INSERT INTO Password(name, username, password, uri, id_user) \
                VALUES (\'{password_line['name']}\',\
                        \'{password_line['username']}\',\
                        \'{password_line['password']}\',\
                        \'{password_line['uri']}\',\
                        \'{id_user[0]}\');"
        if(self.__db.makeQuery(query) != []):
            self.__listPasswords()
            return True
        
        return False
    
    ### Delete an existing password from database based by user id
    def deletePasswordAccount(self, username: str, password_line: list) -> bool:
        pass
        