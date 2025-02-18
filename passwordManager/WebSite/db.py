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
                if(command != ''):
                    print("[db.py] 22:", command)
                    self.__db.execute(command)
            except Exception as msg:
                print('[db.py] 25: Command not executed', msg)
        
        cur = self.__db.execute("SELECT * FROM User;")
        for row in cur.fetchall():
            print(row)

        print("[db.py] 31: database created")
        self.__con.close()
    
    ### GET PARAMETERS FROM QUERY 
    def makeQuery(self, *queries) -> list:
        self.__con = sqlite3.connect("account.db")
        self.__db = self.__con.cursor()
        if(self.__db != None):
            try:
                for query in queries:
                    print("[db.py] 41: QUERY:", query)
                    if(query != ''):
                        self.__db.execute(query)
                        self.__con.commit()

                result = self.__db.execute("SELECT * FROM User;").fetchall()
                print("[db.py] 50", result)
                self.__con.close()
                return result
            except Exception as msg:
                print('[db.py] 54: Command not executed', msg)
                return []
        return []