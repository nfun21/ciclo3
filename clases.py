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
    def consultarVuelo(self, idVuelo, idUser=""):
        db = Database()
        con = db.sql_connection()
        cursorObj = con.cursor()
        sentencia = "SELECT v.idVuelo, v.avion, v.estadoVuelo, v.origenVuelo, v.destinoVuelo, v.capacidad, v.fechaVuelo, p.idUser AS idPiloto,  cp.idUser AS idcoPiloto, p.nombres|| '  ' || p.apellidos AS piloto , cp.nombres|| '  ' || cp.apellidos AS copiloto, (SELECT COUNT(*) FROM Reservas WHERE idUser = ? AND idVuelo = ?) as reservado FROM Vuelo v JOIN Usuario p on v.idPiloto = p.idUser JOIN Usuario cp on v.idcoPiloto = cp.idUser WHERE idVuelo = ?"
        cursorObj.execute(sentencia,[idUser, idVuelo, idVuelo])
        con.commit()
        vuelo = cursorObj.fetchone()
        
        con.close()
        return vuelo
    def crearVuelo(self, capacidad, origenVuelo, destinoVuelo, avion, fecha, idPiloto, idCopiloto, estadoVuelo):
        sentencia = "INSERT INTO Vuelo (capacidad, origenVuelo, destinoVuelo, avion, fechaVuelo,idPiloto, idcoPiloto, estadoVuelo) VALUES (?,?,?,?,?,?,?,?)"
        db = Database()
        con = db.sql_connection()
        cursorObj = con.cursor()
        cursorObj.execute(sentencia,[capacidad, origenVuelo, destinoVuelo, avion, fecha,idPiloto,idCopiloto, estadoVuelo])
        con.commit()
        vuelo = cursorObj.fetchone()
        con.close()
        return vuelo

    def editarVuelo(self, capacidad, origenVuelo, destinoVuelo, avion, fecha, idPiloto, idCopiloto, estadoVuelo,idVuelo):
        sentencia = "UPDATE Vuelo SET capacidad = ?, origenVuelo=?, destinoVuelo=?, avion=?, fechaVuelo=?,idPiloto=?, idcoPiloto=?, estadoVuelo=? WHERE idVuelo=?"
        db = Database()
        con = db.sql_connection()
        cursorObj = con.cursor()
        cursorObj.execute(sentencia,[capacidad, origenVuelo, destinoVuelo, avion, fecha,idPiloto,idCopiloto, estadoVuelo,idVuelo])
        con.commit()
#        vuelo = cursorObj.fetchone()
        con.close()

    def eliminarVuelo(self,idVuelo):
        sentencia = "DELETE FROM Vuelo WHERE idVuelo=?"
        db = Database()
        con = db.sql_connection()
        cursorObj = con.cursor()
        cursorObj.execute(sentencia,[idVuelo])
        con.commit()
        con.close()

    def reservarVuelo(self, idVuelo, idUser):
        sentencia = "SELECT * FROM Reservas WHERE idVuelo = ? AND idUser = ?"
        db = Database()
        con = db.sql_connection()
        cursorObj = con.cursor()
        cursorObj.execute(sentencia,[idVuelo, idUser])
        con.commit()
        reserva = cursorObj.fetchone()
        con.close()
        if reserva:
            return False
        sentencia = "INSERT INTO Reservas (idVuelo, idUser) VALUES(?,?)"
        db = Database()
        con = db.sql_connection()
        cursorObj = con.cursor()
        cursorObj.execute(sentencia,[idVuelo, idUser])
        con.commit()
        con.close()
        return True

    def cancelarReservaVuelo(self, idVuelo, idUser):
        sentencia = "DELETE FROM Reservas WHERE idVuelo = ? AND idUser = ?"
        db = Database()
        con = db.sql_connection()
        cursorObj = con.cursor()
        cursorObj.execute(sentencia,[idVuelo, idUser])
        con.commit()
        con.close()

    def buscarVuelo():
        pass
    
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
        return usuario

    
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

    def buscarPiloto(self, nombrePiloto):
        nombrePiloto = '%' + nombrePiloto + '%'
        sentencia = "SELECT nombres, apellidos, idUser FROM Usuario WHERE idRol = 2 AND nombres LIKE ?"
        db = Database()
        con = db.sql_connection()
        cursorObj = con.cursor()
        cursorObj.execute(sentencia,[nombrePiloto])
        con.commit()
        piloto = cursorObj.fetchall()
        con.close()
        return piloto
