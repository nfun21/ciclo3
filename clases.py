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
    def consultarVuelo(self, idVuelo, idUser=""):
        db = Database()
        con = db.sql_connection()
        cursorObj = con.cursor()
        sentencia = "SELECT v.idVuelo, v.avion, v.estadoVuelo, v.origenVuelo, v.destinoVuelo, v.capacidad, v.fechaVuelo, p.idUser AS idPiloto,  cp.idUser AS idcoPiloto, p.nombres|| '  ' || p.apellidos AS piloto , cp.nombres|| '  ' || cp.apellidos AS copiloto, (SELECT COUNT(*) FROM Reservas WHERE idUser = ? AND idVuelo = ?) as reservado FROM Vuelo v LEFT JOIN Usuario p on v.idPiloto = p.idUser LEFT JOIN Usuario cp on v.idcoPiloto = cp.idUser WHERE idVuelo = ?"
        cursorObj.execute(sentencia,[idUser, idVuelo, idVuelo])
        con.commit()
        vuelo = cursorObj.fetchone()
        con.close()
        return vuelo

    def consultarVuelos(self):
        db = Database()
        con = db.sql_connection()
        cursorObj = con.cursor()
        sentencia = "SELECT v.idVuelo, v.avion, v.estadoVuelo, v.origenVuelo, v.destinoVuelo, v.capacidad, v.fechaVuelo, p.idUser AS idPiloto,  cp.idUser AS idcoPiloto, p.nombres|| '  ' || p.apellidos AS piloto , cp.nombres|| '  ' || cp.apellidos AS copiloto, (v.capacidad-(SELECT COUNT(*) FROM Reservas WHERE idVuelo = v.idVuelo)) as puestos FROM Vuelo v LEFT JOIN Usuario p on v.idPiloto = p.idUser LEFT JOIN Usuario cp on v.idcoPiloto = cp.idUser ORDER BY v.fechaVuelo LIMIT 10"
        cursorObj.execute(sentencia)
        con.commit()
        vuelos = cursorObj.fetchall()
        con.close()
        return vuelos

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

    def buscarVuelos(self,tipoBusqueda="",origenVuelo="", destinoVuelo="",idUser="", busqueda="") :
        db = Database()
        con = db.sql_connection()
        cursorObj = con.cursor()
        if tipoBusqueda == "total":
            busqueda1 = '%'+str(busqueda)+'%'
            busqueda2 = '%'+str(busqueda)+'%'

            sentencia = "SELECT v.idVuelo, v.avion, v.estadoVuelo, v.origenVuelo, v.destinoVuelo, v.capacidad, v.fechaVuelo, p.idUser AS idPiloto,  cp.idUser AS idcoPiloto, p.nombres|| '  ' || p.apellidos AS piloto , cp.nombres|| '  ' || cp.apellidos AS copiloto, (v.capacidad-(SELECT COUNT(*) FROM Reservas WHERE idVuelo = v.idVuelo)) as puestos FROM Vuelo v LEFT JOIN Usuario p on v.idPiloto = p.idUser LEFT JOIN Usuario cp on v.idcoPiloto = cp.idUser WHERE origenVuelo LIKE ? OR destinoVuelo LIKE ? OR idVuelo = ? ORDER BY v.fechaVuelo LIMIT 10 "
            cursorObj.execute(sentencia,[busqueda1, busqueda2, busqueda])
        else:
            origenVuelo = '%'+origenVuelo+'%'
            destinoVuelo = '%'+destinoVuelo+'%'
            sentencia = "SELECT v.idVuelo, v.avion, v.estadoVuelo, v.origenVuelo, v.destinoVuelo, (v.capacidad-(SELECT COUNT(*) FROM Reservas WHERE idVuelo = v.idVuelo)) as puestos, v.fechaVuelo, p.idUser AS idPiloto,  cp.idUser AS idcoPiloto, p.nombres|| '  ' || p.apellidos AS piloto , cp.nombres|| '  ' || cp.apellidos AS copiloto, (SELECT COUNT(*) FROM Reservas WHERE idUser = ? AND idVuelo = v.idVuelo) as reservado FROM Vuelo v LEFT JOIN Usuario p on v.idPiloto = p.idUser LEFT JOIN Usuario cp on v.idcoPiloto = cp.idUser WHERE v.origenVuelo LIKE ? AND v.destinoVuelo LIKE ? AND puestos > 0"
            cursorObj.execute(sentencia,[idUser, origenVuelo, destinoVuelo])
        con.commit()
        resultados = cursorObj.fetchall()
        print(resultados)
        con.close()
        return resultados

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
        
    def consultarUsuario(self, idUser):
        sentencia = "SELECT i.nombres, i.correo, i.idUser, i.idRol, t.nombreRol as nombreRol FROM Roles t JOIN Roles itb ON t.idRol = itb.idRol JOIN Usuario i ON itb.idRol = i.idRol WHERE i.idUser = ? "
        db = Database()
        con = db.sql_connection()
        cursorObj = con.cursor()
        cursorObj.execute(sentencia,[idUser])
        con.commit()
        usuarioInfo= cursorObj.fetchone()
        con.close()
        return usuarioInfo

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

        """ if usuario == "":
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

            flash("Datos incorrectos")
            #return redirect(url_for('ingresar'))
            #return "Usuario ya Existe"          

            return "Usuario ya Existe"   """       

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
        sentencia = "SELECT nombres, apellidos, idUser FROM Usuario WHERE idRol = 2 AND nombres LIKE ?"
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