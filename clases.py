from sqlite3.dbapi2 import Cursor
from flask import session
import sqlite3
from sqlite3 import Error

from werkzeug.utils import redirect
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
    def crearVuelo(self, capacidad, origenVuelo, destinoVuelo, avion, fecha):
        estado = "EN ESPERA"
        sentencia = "INSERT INTO Vuelo (capacidad, origenVuelo, destinoVuelo, avion, fecha, estado) VALUES (?,?,?,?,?,?)"
        db = Database()
        con = db.sql_connection()
        cursorObj = con.cursor()
        cursorObj.execute(sentencia,[capacidad, origenVuelo, destinoVuelo, avion, fecha,estado])
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

    def registrarse(self, nombres, apellidos, tipoDocumento, numDocumento, pais, genero, fechaNacimiento, telefono, correo, pass_enc):
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

<<<<<<< HEAD
    def eliminar(self,idUser):
        sentencia = "DELETE FROM Usuario WHERE idUser = ?"
        db = Database()
        con = db.sql_connection()
        cursorObj = con.cursor()
        cursorObj.execute(sentencia,[idUser])
        con.commit()
        con.close()

    def editarUsuario(self,idUser):
        sentencia= "SELECT nombres,apellidos,tipoDocumento,idUser,fechaNacimiento,telefono,correo,genero,pais,idRol From Usuario Where idUser = ? "
        db = Database()
        con = db.sql_connection()
        cursorObj = con.cursor()
        cursorObj.execute(sentencia,[idUser])
        con.commit()
        editarUser= cursorObj.fetchone()
        con.close()
        return editarUser
=======
    
        if usuario == "":
        #Preparar sentencia SQL para registro usuario
            sentencia = "INSERT INTO Usuario (nombres, apellidos, tipoDocumento, idUser, pais, genero, fechaNacimiento, telefono, correo, password) VALUES (?,?,?,?,?,?,?,?,?,?)"
            db = Database()
            con = db.sql_connection()
            #Crear cursor para manipular la BD
            cursorObj = con.cursor()
            cursorObj.execute(sentencia,[nombres, apellidos, tipoDocumento, numDocumento, pais, genero, fechaNacimiento, telefono, correo, pass_enc])
            con.commit()
            con.close()
        else:
<<<<<<< HEAD
            flash("Datos incorrectos")
            #return redirect(url_for('ingresar'))
            #return "Usuario ya Existe"          
=======
            return "Usuario ya Existe"          
>>>>>>> 574eaef623b402240e1ca70690b2c03c6b27e5e8
>>>>>>> c630353bc9e01da652bfd54eec1969052a053103
    
    """ falta pais """
    def actualizarUsuario(self,nombres,apellidos,tipoDocumento,fechaNacimiento,telefono,correo,genero,idRol,idUser):
        sentencia = "UPDATE Usuario SET nombres = ?, apellidos = ?, tipoDocumento = ?, fechaNacimiento = ?, telefono = ?, correo = ?, genero = ?, idRol = ? WHERE idUser= ?"
        db = Database()
        con = db.sql_connection()
        cursosObj = con.cursor()
        cursosObj.execute(sentencia,[nombres,apellidos,tipoDocumento,fechaNacimiento,telefono,correo,genero,idRol,idUser])
        con.commit
        con.close()


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
        sentencia = "SELECT nombres, apellidos, numdocumento, idUser FROM Usuario WHERE idRol = 2 AND nombre LIKE ?"
        db = Database()
        con = db.sql_connection()
        cursorObj = con.cursor()
        cursorObj.execute(sentencia,[nombrePiloto])
        con.commit()
        piloto = cursorObj.fetchall()
        con.close()
        return piloto

class Pasajero():
    
    def consultarReviews(self, idUser):
            
        sentencia = "SELECT * FROM review WHERE idUser = ?"
        db = Database()
        con = db.sql_connection()

        cursorObj = con.cursor()
        cursorObj.execute(sentencia,[idUser])
        con.commit()
        review = cursorObj.fetchall()
        con.close()

        return review