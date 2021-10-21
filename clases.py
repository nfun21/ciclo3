from flask import session
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
        
        sentencia = "SELECT i.estadoVuelo, i.capacidad, i.avion, i.fechaVuelo, i.origenVuelo, i.destinoVuelo, i.idVuelo, t.nombres as piloto FROM Usuario t JOIN VueloPilotos itb ON t.idUser = itb.idUser JOIN Vuelo i ON itb.idVuelo = i.idVuelo WHERE i.idVuelo = ?"
        db = Database()
        con = db.sql_connection()

        cursorObj = con.cursor()
        cursorObj.execute(sentencia,[idVuelo])
        con.commit()
        vuelo = cursorObj.fetchone()
        con.close()

        return vuelo

class Usuario():
    # def consultarUsuario(self, correo):

    def login(self, correo, password):
        sentencia = "SELECT nombres, apellidos, idUser, idRol FROM Usuario WHERE correo = ? AND  password = ?"
        db = Database()
        con = db.sql_connection()
        cursorObj = con.cursor()
        cursorObj.execute(sentencia,[correo, password])
        con.commit()
        usuario = cursorObj.fetchone()
        con.close()

        return usuario

    def registrarse(self, nombres, apellidos, tipoDocumento, numDocumento, genero, fechaNacimiento, telefono, correo, pass_enc):
        #usar select para validar
        #Preparar sentencia SQL para registro usuario
        sentencia = "INSERT INTO Usuario (nombres, apellidos, tipoDocumento, idUser, genero, fechaNacimiento, telefono, correo, password) VALUES (?,?,?,?,?,?,?,?,?)"
        db = Database()
        con = db.sql_connection()
        #Crear cursor para manipular la BD
        cursorObj = con.cursor()
        cursorObj.execute(sentencia,[nombres, apellidos, tipoDocumento, numDocumento, genero, fechaNacimiento, telefono, correo, pass_enc])
        con.commit()
        con.close()

        #return ()            
    

class piloto():
    def pilotodata(self):
        sentencia = "SELECT nombres, apellidos, genero, fecha, numdocumento, paisdenacimiento, cargo, numtelefono, email FROM Usuario WHERE idUser =?"
        db = Database()
        con = db.sql_connection()
        cursorObj = con.cursor()
        cursorObj.execute(sentencia,[])
        con.commit()
        usuario = cursorObj.fetchone()
        con.close()

        return piloto
