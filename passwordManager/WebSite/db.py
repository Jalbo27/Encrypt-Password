import sqlite3
from flask import current_app as app, g

class DataBase:
    __db = None
    
    ###
    def __get_db(self):
        with app.app_context():    
            if 'db' not in g:
                g.db = sqlite3.connect(
                    app.config['DATABASE'],
                    detect_types=sqlite3.PARSE_DECLTYPES
                )
                g.db.row_factory = sqlite3.Row

        return g.db

    ###
    def __init__(self):
        self.initDB()
    
    ###
    def initDB(self):
        self.__db = self.__get_db()
        
        with current_app.open_resource("./sql/schema.sql") as f:
            self.__db.executescript(f.read().decode('utf8'))
            
    ###
    def makeQuery(self, query) -> bool:
        if(self.__db != None and query != ''):
            self.__db.executescript(query)