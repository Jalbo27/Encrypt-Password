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
        self.__db = self.__con.cursor()
        count_users = self.__db.execute("SELECT COUNT(id) FROM User").fetchall()
        count_pass = self.__db.execute("SELECT COUNT(id) FROM Password").fetchall()
        #print("id user n°: {0}\nid pass n°: {1}".format(count_users, count_pass))
        if(self.__db != None):
            try:
                cur = None
                result = []
                for query in queries:
                    print(currentLine("db"), query)
                    if(query != ''):
                        cur = self.__db.execute(query)
                        cur.commit()
                        if(cur.fetchone() != None):
                            #self.__con.close()
                            return cur.fetchall()
                        
                if(self.__db.execute("SELECT COUNT(id) FROM User").fetchall() > count_users):
                    result = self.__db.execute("SELECT * FROM User").fetchall()[0 - cur.lastrowid]
                elif (self.__db.execute("SELECT COUNT(id) FROM Password").fetchall() > count_pass):
                    result = self.__db.execute("SELECT * FROM Password").fetchall()[0 - cur.lastrowid]
                    
                self.__con.close()
                return result
            except Exception as msg:
                print(currentLine("db"), f"command not executed: {msg}")
                return []
        return []