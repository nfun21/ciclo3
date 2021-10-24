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
        elif tipoBusqueda == "reservas":
            sentencia = "SELECT rv.comment, rv.puntuacion, rv.fechaReview, v.idVuelo, v.avion, v.estadoVuelo, v.origenVuelo, v.destinoVuelo, v.fechaVuelo, p.idUser AS idPiloto,  cp.idUser AS idcoPiloto, p.nombres|| '  ' || p.apellidos AS piloto , cp.nombres|| '  ' || cp.apellidos AS copiloto, (SELECT COUNT(*) FROM Review WHERE idVuelo = v.idVuelo AND idUser = ?) as review FROM Vuelo v LEFT JOIN Usuario p on v.idPiloto = p.idUser LEFT JOIN Usuario cp on v.idcoPiloto = cp.idUser LEFT JOIN Reservas r on v.idVuelo = r.idVuelo LEFT JOIN Review rv on v.idVuelo = rv.idVuelo and r.idUser = rv.idUser WHERE r.idUser = ?" # AND v.estadoVuelo = 'Finalizado'
            cursorObj.execute(sentencia,[idUser, idUser])
        else:
            origenVuelo = '%'+origenVuelo+'%'
            destinoVuelo = '%'+destinoVuelo+'%'
            sentencia = "SELECT v.idVuelo, v.avion, v.estadoVuelo, v.origenVuelo, v.destinoVuelo, (v.capacidad-(SELECT COUNT(*) FROM Reservas WHERE idVuelo = v.idVuelo)) as puestos, v.fechaVuelo, p.idUser AS idPiloto,  cp.idUser AS idcoPiloto, p.nombres|| '  ' || p.apellidos AS piloto , cp.nombres|| '  ' || cp.apellidos AS copiloto, (SELECT COUNT(*) FROM Reservas WHERE idUser = ? AND idVuelo = v.idVuelo) as reservado FROM Vuelo v LEFT JOIN Usuario p on v.idPiloto = p.idUser LEFT JOIN Usuario cp on v.idcoPiloto = cp.idUser WHERE v.origenVuelo LIKE ? AND v.destinoVuelo LIKE ? AND puestos > 0 AND (v.estadoVuelo ='Inactivo' OR v.estadoVuelo='Inicializado')"
            cursorObj.execute(sentencia,[idUser, origenVuelo, destinoVuelo])
        con.commit()
        resultados = cursorObj.fetchall()
        con.close()
        return resultados

class Usuario():
    def login(self, correo, password):
        sentencia = "SELECT u.nombres, u.apellidos, u.idUser, u.idRol, r.nombreRol FROM Usuario u JOIN Roles r ON u.idRol = r.idRol WHERE correo = ? AND  password = ?"
        db = Database()
        con = db.sql_connection()
        cursorObj = con.cursor()
        cursorObj.execute(sentencia,[correo, password])
        con.commit()
        usuario = cursorObj.fetchone()
        con.close()
        return usuario

    def registrarse(self, nombres, apellidos, tipoDocumento, numDocumento, pais, genero, fechaNacimiento, telefono, correo, pass_enc):
        sentencia = "INSERT INTO Usuario (nombres, apellidos, tipoDocumento, idUser, pais, genero, fechaNacimiento, telefono, correo, password) VALUES (?,?,?,?,?,?,?,?,?,?)"
        db = Database()
        con = db.sql_connection()
        #Crear cursor para manipular la BD
        cursorObj = con.cursor()
        cursorObj.execute(sentencia,[nombres, apellidos, tipoDocumento, numDocumento, pais, genero, fechaNacimiento, telefono, correo, pass_enc])
        con.commit()
        con.close()
        
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
    

    def actualizarUsuario(self,nombres,apellidos,tipoDocumento,fechaNacimiento,pais,telefono,correo,genero,idRol,idUser):
        sentencia = "UPDATE Usuario SET nombres = ?, apellidos = ?, tipoDocumento = ?,fechaNacimiento = ?,pais = ?,telefono = ?, correo = ?, genero = ?, idRol = ? WHERE idUser= ?"
        db = Database()
        con = db.sql_connection()
        cursosObj = con.cursor()
        cursosObj.execute(sentencia,[nombres,apellidos,tipoDocumento,fechaNacimiento,pais,telefono,correo,genero,idRol,idUser])
        con.commit()
        con.close()

class Piloto():
    def consultarVuelo(self, idUser):
        sentencia = "SELECT i.estadoVuelo, i.capacidad, i.avion, i.fechaVuelo, i.origenVuelo, i.destinoVuelo, i.idVuelo FROM Vuelo i JOIN Usuario t ON i.idPiloto = t.idUser WHERE t.idUser = ?"
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

    def consultarReviewsPi(self, idUser):
            
        sentencia = "SELECT i.idReview, i.idVuelo, i.comment, i.puntuacion, i.idUser, i.fechaReview FROM Review i Join Vuelo t ON i.idVuelo = t.idVuelo WHERE t.idPiloto=?"
        db = Database()
        con = db.sql_connection()

        cursorObj = con.cursor()
        cursorObj.execute(sentencia,[idUser])
        con.commit()
        review = cursorObj.fetchall()
        con.close()

        return review

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
    def consultarReview(self, idUser, idVuelo):
        sentencia = "SELECT * FROM Review WHERE idVuelo = ? AND idUser = ?"
        db = Database()
        con = db.sql_connection()
        cursorObj = con.cursor()
        cursorObj.execute(sentencia,[idVuelo, idUser])
        con.commit()
        review = cursorObj.fetchall()
        con.close()
        return review

    def consultarReserva(self, idUser, idVuelo):
        sentencia = "SELECT * FROM Reservas WHERE idVuelo = ? AND idUser = ?"
        db = Database()
        con = db.sql_connection()
        cursorObj = con.cursor()
        cursorObj.execute(sentencia,[idVuelo, idUser])
        con.commit()
        reserva = cursorObj.fetchall()
        con.close()
        return reserva

    def publicarReview(self, idUser, idVuelo, comment, puntuacion, fechaReview):
        sentencia = "INSERT INTO Review (idVuelo, comment, puntuacion, idUser, fechaReview) VALUES (?,?,?,?,?)"
        db = Database()
        con = db.sql_connection()
        cursorObj = con.cursor()
        cursorObj.execute(sentencia,[idVuelo, comment, puntuacion, idUser, fechaReview])
        con.commit()
        con.close()
    
