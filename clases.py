from sqlite3.dbapi2 import Cursor
from flask import session, flash, url_for
import sqlite3
from sqlite3 import Error
from datetime import datetime
from werkzeug.utils import redirect
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
def convertirFechas(fecha):
   fecha = datetime.strptime(fecha, '%Y-%m-%dT%H:%M')
   return fecha.strftime('%d/%m/%y %I:%M%p')
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
        sentencia = "SELECT v.tipoVuelo, v.idVuelo, v.avion, v.estadoVuelo, v.origenVuelo, v.capacidad, v.fechaVuelo, p.idUser AS idPiloto,  cp.idUser AS idcoPiloto, p.nombres|| '  ' || p.apellidos AS piloto , cp.nombres|| '  ' || cp.apellidos AS copiloto, (v.capacidad-(SELECT COUNT(*) FROM Reservas WHERE idVuelo = v.idVuelo)) as puestos, (SELECT COUNT(*) FROM Reservas WHERE idUser = ? AND idVuelo = ?) as reservado FROM Vuelo v LEFT JOIN Usuario p on v.idPiloto = p.idUser LEFT JOIN Usuario cp on v.idcoPiloto = cp.idUser WHERE idVuelo = ?"
        cursorObj.execute(sentencia,[idUser, idVuelo, idVuelo])
        con.commit()
        vuelo = cursorObj.fetchone()
        con.close()
        return vuelo

    def consultarVuelos(self):
        db = Database()
        con = db.sql_connection()
        cursorObj = con.cursor()
        sentencia = "SELECT (SELECT COUNT(*) FROM Review WHERE idVuelo = v.idVuelo) as reviews, v.tipoVuelo, v.idVuelo, v.avion, v.estadoVuelo, v.origenVuelo, v.capacidad, v.fechaVuelo, p.idUser AS idPiloto,  cp.idUser AS idcoPiloto, p.nombres|| '  ' || p.apellidos AS piloto , cp.nombres|| '  ' || cp.apellidos AS copiloto, (v.capacidad-(SELECT COUNT(*) FROM Reservas WHERE idVuelo = v.idVuelo)) as puestos FROM Vuelo v LEFT JOIN Usuario p on v.idPiloto = p.idUser LEFT JOIN Usuario cp on v.idcoPiloto = cp.idUser ORDER BY v.fechaVuelo LIMIT 10"
        cursorObj.execute(sentencia)
        con.commit()
        vuelos = cursorObj.fetchall()
        con.close()
        
        for x in range(len(vuelos)):
            vuelos[x]["fechaVuelo"] = convertirFechas(vuelos[x]["fechaVuelo"])
        return vuelos

    def crearVuelo(self, capacidad, origenVuelo,  avion, fecha, idPiloto, idCopiloto, estadoVuelo, tipoVuelo):
        sentencia = "INSERT INTO Vuelo (capacidad, origenVuelo,  avion, fechaVuelo,idPiloto, idcoPiloto, estadoVuelo, tipoVuelo) VALUES (?,?,?,?,?,?,?,?)"
        db = Database()
        con = db.sql_connection()
        cursorObj = con.cursor()
        cursorObj.execute(sentencia,[capacidad, origenVuelo,  avion, fecha,idPiloto,idCopiloto, estadoVuelo, tipoVuelo])
        con.commit()
        vuelo = cursorObj.fetchone()
        con.close()
        return vuelo

    def editarVuelo(self, capacidad, origenVuelo,  avion, fecha, idPiloto, idCopiloto, estadoVuelo,idVuelo, tipoVuelo):
        sentencia = "UPDATE Vuelo SET capacidad = ?, origenVuelo=?, avion=?, fechaVuelo=?,idPiloto=?, idcoPiloto=?, estadoVuelo=?, tipoVuelo=? WHERE idVuelo=?"
        db = Database()
        con = db.sql_connection()
        cursorObj = con.cursor()
        cursorObj.execute(sentencia,[capacidad, origenVuelo,  avion, fecha,idPiloto,idCopiloto, estadoVuelo,tipoVuelo,idVuelo])
        con.commit()
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
    def autocompletarVuelos(self, ciudad, tipoVuelo):
        if ciudad:
            origenVuelo = '%'+ciudad+'%'
            db = Database()
            con = db.sql_connection()
            cursorObj = con.cursor()
            if tipoVuelo=="Ninguno":
                sentencia = "SELECT DISTINCT origenVuelo as vuelo FROM Vuelo WHERE origenVuelo LIKE ?"
                cursorObj.execute(sentencia,[origenVuelo])
            else:
                sentencia = "SELECT DISTINCT origenVuelo as vuelo FROM Vuelo WHERE tipoVuelo = ? AND origenVuelo LIKE ? AND estadoVuelo='Programado'"
                cursorObj.execute(sentencia,[tipoVuelo, origenVuelo])
            con.commit()
            vuelo = cursorObj.fetchall()
            con.close()
            return vuelo
        return False

    def cancelarReservaVuelo(self, idVuelo, idUser):
        sentencia = "DELETE FROM Reservas WHERE idVuelo = ? AND idUser = ?"
        db = Database()
        con = db.sql_connection()
        cursorObj = con.cursor()
        cursorObj.execute(sentencia,[idVuelo, idUser])
        con.commit()
        con.close()

    def buscarVuelos(self,tipoBusqueda="",origenVuelo="", idUser="", busqueda="",tipoVuelo="") :
        
        db = Database()
        con = db.sql_connection()
        cursorObj = con.cursor()
        if tipoBusqueda == "total":##obtiene todos los vuelos basándose en criterios
            busqueda1 = '%'+str(busqueda)+'%'
            
            sentencia = "SELECT (SELECT COUNT(*) FROM Review WHERE idVuelo = v.idVuelo) as reviews, v.tipoVuelo, v.idVuelo, v.avion, v.estadoVuelo, v.origenVuelo, v.capacidad, v.fechaVuelo, p.idUser AS idPiloto,  cp.idUser AS idcoPiloto, p.nombres|| '  ' || p.apellidos AS piloto , cp.nombres|| '  ' || cp.apellidos AS copiloto, (v.capacidad-(SELECT COUNT(*) FROM Reservas WHERE idVuelo = v.idVuelo)) as puestos FROM Vuelo v LEFT JOIN Usuario p on v.idPiloto = p.idUser LEFT JOIN Usuario cp on v.idcoPiloto = cp.idUser WHERE origenVuelo LIKE ? OR idVuelo = ? ORDER BY v.fechaVuelo LIMIT 10 "
            cursorObj.execute(sentencia,[busqueda1, busqueda])
            
        elif tipoBusqueda == "reservas":##obtiene los vuelos reservados por el usuario en particular
            sentencia = "SELECT rv.comment, rv.puntuacion, rv.fechaReview, v.tipoVuelo, v.idVuelo, v.avion, v.estadoVuelo, v.origenVuelo,  v.fechaVuelo, p.idUser AS idPiloto,  cp.idUser AS idcoPiloto, p.nombres|| '  ' || p.apellidos AS piloto , cp.nombres|| '  ' || cp.apellidos AS copiloto, (SELECT COUNT(*) FROM Review WHERE idVuelo = v.idVuelo AND idUser = ?) as review FROM Vuelo v LEFT JOIN Usuario p on v.idPiloto = p.idUser LEFT JOIN Usuario cp on v.idcoPiloto = cp.idUser LEFT JOIN Reservas r on v.idVuelo = r.idVuelo LEFT JOIN Review rv on v.idVuelo = rv.idVuelo and r.idUser = rv.idUser WHERE r.idUser = ?" # AND v.estadoVuelo = 'Finalizado'
            cursorObj.execute(sentencia,[idUser, idUser])
        else:##búsqueda genérica para reservas en buscar-vuelos
            origenVuelo = '%'+origenVuelo+'%'
            if tipoVuelo !="Ninguno":
                sentencia = "SELECT v.idVuelo, v.avion, v.estadoVuelo, v.tipoVuelo, v.origenVuelo,  (v.capacidad-(SELECT COUNT(*) FROM Reservas WHERE idVuelo = v.idVuelo)) as puestos, v.fechaVuelo, p.idUser AS idPiloto,  cp.idUser AS idcoPiloto, p.nombres|| '  ' || p.apellidos AS piloto , cp.nombres|| '  ' || cp.apellidos AS copiloto, (SELECT COUNT(*) FROM Reservas WHERE idUser = ? AND idVuelo = v.idVuelo) as reservado FROM Vuelo v LEFT JOIN Usuario p on v.idPiloto = p.idUser LEFT JOIN Usuario cp on v.idcoPiloto = cp.idUser WHERE v.tipoVuelo = ? AND v.origenVuelo LIKE ? AND puestos > 0 AND v.estadoVuelo ='Programado'"
                cursorObj.execute(sentencia,[idUser,  tipoVuelo, origenVuelo])
            else:
                sentencia = "SELECT v.idVuelo, v.avion, v.estadoVuelo, v.tipoVuelo, v.origenVuelo,  (v.capacidad-(SELECT COUNT(*) FROM Reservas WHERE idVuelo = v.idVuelo)) as puestos, v.fechaVuelo, p.idUser AS idPiloto,  cp.idUser AS idcoPiloto, p.nombres|| '  ' || p.apellidos AS piloto , cp.nombres|| '  ' || cp.apellidos AS copiloto, (SELECT COUNT(*) FROM Reservas WHERE idUser = ? AND idVuelo = v.idVuelo) as reservado FROM Vuelo v LEFT JOIN Usuario p on v.idPiloto = p.idUser LEFT JOIN Usuario cp on v.idcoPiloto = cp.idUser WHERE v.origenVuelo LIKE ? AND puestos > 0 AND v.estadoVuelo ='Programado'"
                cursorObj.execute(sentencia,[idUser,  origenVuelo])
        con.commit()
        resultados = cursorObj.fetchall()
        
        for x in range(len(resultados)):
            resultados[x]['fechaVuelo'] = convertirFechas(resultados[x]['fechaVuelo'])
        con.close()
        return resultados

    def verReviewsVuelo(self, idVuelo):
        sentencia = "SELECT r.comment, r.puntuacion, r.fechaReview, u.nombres || ' ' ||u.apellidos autor,  p.nombres || ' ' ||p.apellidos piloto,  cp.nombres || ' ' ||cp.apellidos copiloto FROM Review r LEFT JOIN Usuario u ON r.idUser = u.idUser LEFT JOIN Vuelo v ON r.idVuelo = v.idVuelo LEFT JOIN Usuario p ON v.idPiloto = p.idUser LEFT JOIN Usuario cp ON v.idcoPiloto = cp.idUser WHERE r.idVuelo = ?"
        db = Database()
        con = db.sql_connection()
        cursorObj = con.cursor()
        cursorObj.execute(sentencia,[idVuelo])
        con.commit()
        reviews = cursorObj.fetchall()
        con.close()
        return reviews

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

    def registrarse(self, nombres, apellidos, tipoDocumento, numDocumento, pais, genero, fechaNacimiento, codigoMarcacion,telefono, correo, pass_enc):
        sentencia = "INSERT INTO Usuario (nombres, apellidos, tipoDocumento, idUser, pais, genero, fechaNacimiento ,codigoMarcacion, telefono, correo, password) VALUES (?,?,?,?,?,?,?,?,?,?,?)"
        db = Database()
        con = db.sql_connection()
        #Crear cursor para manipular la BD
        cursorObj = con.cursor()
        cursorObj.execute(sentencia,[nombres, apellidos, tipoDocumento, numDocumento, pais, genero, fechaNacimiento, codigoMarcacion, telefono, correo, pass_enc])
        con.commit()
        con.close()

    def crearUsuario(self, nombres, apellidos, tipoDocumento, numDocumento, fechaNacimiento, telefono, correo, genero, pais, rol):
        sentencia = "INSERT INTO Usuario (nombres, apellidos, tipoDocumento, idUser, fechaNacimiento, telefono, correo, pais, idRol) VALUES (?,?,?,?,?,?,?,?,?)"
        db = Database()
        con = db.sql_connection()
        #Crear cursor para manipular la BD
        cursorObj = con.cursor()
        cursorObj.execute(sentencia,[nombres, apellidos, tipoDocumento, numDocumento, fechaNacimiento, telefono, correo, genero, pais, rol])
        con.commit()
        con.close()

    def consultarUsuario(self, idUser, tipoConsulta=""):
        sentencia = "SELECT i.nombres, i.correo, i.idUser, i.idRol, t.nombreRol as nombreRol FROM Roles t JOIN Roles itb ON t.idRol = itb.idRol JOIN Usuario i ON itb.idRol = i.idRol WHERE i.idUser = ? "
        db = Database()
        con = db.sql_connection()
        cursorObj = con.cursor()
        
        if tipoConsulta == "correo":
            sentencia = "SELECT nombres FROM Usuario WHERE correo = ? "
            cursorObj.execute(sentencia,[idUser])
        else:
            nombres = '%' + str(idUser) + '%'
            apellidos = '%' + str(idUser) + '%'
            sentencia = "SELECT i.nombres, i.apellidos, i.correo, i.idUser, i.idRol, t.nombreRol as nombreRol FROM Roles t JOIN Roles itb ON t.idRol = itb.idRol JOIN Usuario i ON itb.idRol = i.idRol WHERE i.idUser = ? OR nombres LIKE ? or apellidos LIKE ? "
            cursorObj.execute(sentencia,[idUser, nombres, apellidos])

        con.commit()
        usuarioInfo= cursorObj.fetchall()
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
        sentencia= "SELECT nombres,apellidos,tipoDocumento,idUser,fechaNacimiento,codigoMarcacion,telefono,correo,genero,pais,idRol From Usuario Where idUser = ? "
        db = Database()
        con = db.sql_connection()
        cursorObj = con.cursor()
        cursorObj.execute(sentencia,[idUser])
        con.commit()
        editarUser= cursorObj.fetchone()
        con.close()
        return editarUser
    

    def actualizarUsuario(self,nombres,apellidos,tipoDocumento,fechaNacimiento,pais,codigoMarcacion,telefono,correo,genero,idRol,idUser, nuevaidUser):
        sentencia = "UPDATE Usuario SET nombres = ?, apellidos = ?, tipoDocumento = ?,fechaNacimiento = ?,pais = ?,codigoMarcacion = ?,telefono = ?, correo = ?, genero = ?, idRol = ?, idUser=? WHERE idUser= ?"
        db = Database()
        con = db.sql_connection()
        cursosObj = con.cursor()
        cursosObj.execute(sentencia,[nombres,apellidos,tipoDocumento,fechaNacimiento,pais,codigoMarcacion,telefono,correo,genero,idRol,nuevaidUser, idUser])
        con.commit()
        con.close()
    

class Piloto():
    def consultarVuelos(self, idUser):
        sentencia = "SELECT i.estadoVuelo, i.tipoVuelo, i.capacidad, (SELECT COUNT(*) FROM Reservas WHERE idVuelo = i.idVuelo) as puestos, i.avion, i.fechaVuelo, i.origenVuelo,  i.idVuelo, (SELECT COUNT (*) FROM Review WHERE idVuelo = i.idVuelo) as reviews FROM Vuelo i LEFT JOIN Usuario t ON i.idPiloto = t.idUser WHERE i.idPiloto = ? OR i.idcoPiloto =?"
        db = Database()
        con = db.sql_connection()
        cursorObj = con.cursor()
        cursorObj.execute(sentencia,[idUser, idUser])
        con.commit()
        pilotovuelo = cursorObj.fetchall()
        for x in range(len(pilotovuelo)):
            pilotovuelo[x]['fechaVuelo'] = convertirFechas(pilotovuelo[x]['fechaVuelo'])
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
        apellidoPiloto = '%' + nombrePiloto + '%'
        sentencia = "SELECT nombres, apellidos, idUser FROM Usuario WHERE idRol = 2 AND (nombres LIKE ? OR apellidos LIKE ?)"
        db = Database()
        con = db.sql_connection()
        cursorObj = con.cursor()
        cursorObj.execute(sentencia,[nombrePiloto,apellidoPiloto])
        con.commit()
        piloto = cursorObj.fetchall()
        con.close()
        return piloto
####ojo: donde se usa esto de consultarvuelo?
    def consultarVuelo(self, idUser, idVuelo):
        sentencia = "SELECT * FROM Vuelo WHERE ( idPiloto = ? OR idcoPiloto = ?) AND idVuelo = ?"
        db = Database()
        con = db.sql_connection()
        cursorObj = con.cursor()
        cursorObj.execute(sentencia,[idUser, idUser, idVuelo])
        con.commit()
        vuelo = cursorObj.fetchall()
        con.close()
        return vuelo
####ojo: donde se usa esto de consultarReviewsPi
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
####ojo: donde se usa esto de consultarReviews    
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
####ojo: donde se usa esto de consultarReview
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
    
