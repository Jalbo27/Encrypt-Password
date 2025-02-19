import sqlite3
from __inspection__ import currentLine


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
                if(command != ''):
                    print(currentLine("db"), command)
                    self.__db.execute(command)
            except Exception as msg:
                print(currentLine("db"), msg)
        
        cur = self.__db.execute("SELECT * FROM User;")
        for row in cur.fetchall():
            print(row)

        print(currentLine("db"), "database created")
        self.__con.close()
    
    ### GET PARAMETERS FROM QUERY 
    def makeQuery(self, *queries) -> list:
        self.__con = sqlite3.connect("account.db")
        self.__con.autocommit = True
        self.__db = self.__con.cursor()
        count_users = self.__db.execute("SELECT COUNT(id) FROM User").fetchall()
        count_pass = self.__db.execute("SELECT COUNT(id) FROM Password").fetchall()
        if(self.__db != None):
            try:
                cur = None
                result = []
                for query in queries:
                    print(currentLine("db"), query)
                    if(query != ''):
                        cur = self.__db.execute(query)
                        result = cur.fetchall()
                        if(result != []):
                            self.__con.close()
                            return result
                        
                if(self.__db.execute("SELECT COUNT(id) FROM User").fetchall() > count_users):
                    print(currentLine("db"), " current users: ", self.__db.execute("SELECT COUNT(id) FROM User").fetchall())
                    result = self.__db.execute("SELECT * FROM User").fetchall()[0 - cur.lastrowid]
                elif (self.__db.execute("SELECT COUNT(id) FROM Password").fetchall() > count_pass):
                    print(currentLine("db"), " current password: ", self.__db.execute("SELECT COUNT(id) FROM Password").fetchall())
                    result = self.__db.execute("SELECT * FROM Password").fetchall()[0 - cur.lastrowid]
                    
                self.__con.close()
                return result
            except Exception as msg:
                print(currentLine("db"), f"command not executed: {msg}")
                return []
        return []