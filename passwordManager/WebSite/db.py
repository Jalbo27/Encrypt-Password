import sqlite3

class DataBase:
    __db = None
    __con = None     

    ###
    def __init__(self):
        self.initDB()
    
    ###
    def initDB(self):   
        self.__con = sqlite3.connect("account.db")
        self.__db = self.__con.cursor()
        file = open('./sql/schema.sql', 'r')
        sqlfile = file.read()
        file.close()
        commands = sqlfile.split(';')
        for command in commands:
            try:    
                self.__db.execute(command)
            except Exception as msg:
                print('Command not executed', msg)
        self.__con.close()

    ###
    def makeQuery(self, query) -> bool:
        self.__con = sqlite3.connect("account.db")
        self.__db = self.__con.cursor()
        if(self.__db != None and query != ''):
            try:
                self.__db.execute(query)
                self.__con.commit()
                print(self.__db.fetchall())
                return True
            except Exception as msg:
                print('Command not executed', msg)
                return False
        return False