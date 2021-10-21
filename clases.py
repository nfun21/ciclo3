from flask import session
import sqlite3
from sqlite3 import Error
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class Database():
    def sql_connection(self):
        try:
            con=sqlite3.connect('database/database.db')
            # para que genere un diccionario cuando trae los resultados
            con.row_factory = dict_factory
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
        #Validar que no exista usuario en la tabla con datos ingresados usar select para validar
        sentencia = "SELECT correo FROM Usuario WHERE idUser = ?"
        db = Database()
        con = db.sql_connection()
        cursorObj = con.cursor()
        cursorObj.execute(sentencia,[numDocumento])
        con.commit()
        usuario = cursorObj.fetchone()
        con.close()
        if usuario == "":
            #Preparar sentencia SQL para registro usuario
            sentencia = "INSERT INTO Usuario (nombres, apellidos, tipoDocumento, idUser, genero, fechaNacimiento, telefono, correo, password) VALUES (?,?,?,?,?,?,?,?,?)"
            db = Database()
            con = db.sql_connection()
            #Crear cursor para manipular la BD
            cursorObj = con.cursor()
            cursorObj.execute(sentencia,[nombres, apellidos, tipoDocumento, numDocumento, genero, fechaNacimiento, telefono, correo, pass_enc])
            con.commit()
            con.close()
        else:
            return "Usuario ya Existe"          
    

class Piloto():
    def consultarVuelo(self, idUser):
        sentencia = "SELECT i.estadoVuelo, i.capacidad, i.avion, i.fechaVuelo, i.origenVuelo, i.destinoVuelo, i.idVuelo FROM Vuelo i JOIN VueloPilotos itb ON i.idVuelo = itb.idVuelo JOIN Usuario t ON itb.idUser = t.idUser WHERE t.idUser = ?"
        db = Database()
        con = db.sql_connection()
        cursorObj = con.cursor()
        cursorObj.execute(sentencia,[idUser])
        con.commit()
        pilotovuelo = cursorObj.fetchall()
        con.close()

        return pilotovuelo

    def consultarPerfil(self, idUser):
        sentencia = "SELECT nombres, apellidos, genero, fechaNacimiento, idUser, pais, idRol, telefono, correo FROM Usuario WHERE idUser = ?"
        db = Database()
        con = db.sql_connection()
        cursorObj = con.cursor()
        cursorObj.execute(sentencia,[idUser])
        con.commit()
        pilotodata = cursorObj.fetchone()
        con.close()

        return pilotodata

    
