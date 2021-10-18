import sqlite3
from sqlite3 import Error

class Database():
    def sql_connection(self):
        try:
            con=sqlite3.connect('database/database.db')
            # para que genere un diccionario cuando trae los resultados
            con.row_factory = sqlite3.Row
            return con
        except Error:
            print(Error)

class Vuelo():
    def consultarVuelo(self, idVuelo):
        
        sentencia = "SELECT * FROM Vuelo WHERE idVuelo= ?"
        db = Database()
        con = db.sql_connection()

        cursorObj = con.cursor()
        cursorObj.execute(sentencia,[idVuelo])
        con.commit()
        vuelo = cursorObj.fetchone()
        con.close()

        return vuelo