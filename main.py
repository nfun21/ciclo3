from typing import Text
from flask import Flask, render_template, request, redirect, url_for, flash, Response
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField ,BooleanField, \
    SubmitField
from wtforms.fields.core import DateField, IntegerField, SelectField
from wtforms.validators import ValidationError, DataRequired, \
    Email, EqualTo, Length
from formularios import*
import os
import json
import hashlib
from werkzeug.utils import escape, redirect
from clases import *
from datetime import datetime



app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route("/", methods = ["GET"])
def paginaprincipal():
   if 'idUser' in session:
      if session['rol']==1:
         return redirect(url_for('pasajeros'))
      elif session['rol']==2:
         return redirect(url_for('piloto'))
      elif session['rol']==3:
         return redirect(url_for('superadmin'))
   return render_template("pagina-principal.html")

@app.route("/ingresar", methods = ["GET", "POST"])
def ingresar():
   #para verificar que el usuario esta logueado
   if 'idUser' in session:#verifica que la llave idUser existe en la sesión. Si existe, quiere decir que el usuario está logueado y no podrá ver /ingresar.
      return redirect(url_for('paginaprincipal'))
   else:
      form = frmIngreso()
      if form.validate_on_submit():
         correo = escape(form.correo.data)
         password = escape(form.password.data)
         enc = hashlib.sha256(password.encode())
         pass_enc = enc.hexdigest()
         usuario = Usuario()
         login = usuario.login(correo, pass_enc)
         if login:
            #se crea la sesión
            session['idUser'] = login['idUser']
            session['nombres'] = login['nombres']
            session['apellidos'] = login['apellidos']
            session['rol'] = login['idRol']
            session['nombreRol'] = login['nombreRol']
            
            #se envía al usuario a su página principal específica
            if session['rol'] == 1:
               return redirect(url_for('pasajeros'))
            elif session['rol'] == 2:
               return redirect(url_for('piloto'))
            elif session['rol'] == 3:
               return redirect(url_for('superadmin'))
            else:
               session.clear()
               return redirect(url_for('paginaprincipal'))
         else:
            flash("Datos incorrectos")
            return redirect(url_for('ingresar'))

         
      return render_template("ingresar.html", form = form)

@app.route('/salir')
def salir():
   session.clear()
   flash('Se cerró la sesión.')
   return redirect(url_for('paginaprincipal'))

#API Rest para registrar al usuario
@app.route("/registrarse", methods = ["GET", "POST"])
def registrarse():
   form = frmRegistro()
   if request.method == "POST":
      #Condicional para asegurar validaciones requeridas
      if form.validate_on_submit():
         #capturar los datos del formulario en variables
         nombres = form.nombres.data
         apellidos = form.apellidos.data
         tipoDocumento = form.tipoDocumento.data
         numDocumento = form.numDocumento.data
         pais = form.pais.data
         genero = form.genero.data
         fechaNacimiento = form.fechaNacimiento.data
         telefono = form.telefono.data
         correo = form.correo.data
         codigoMarcacion = form.codigoMarcacion.data
         password = form.password.data
         #Cifrar el password
         enc = hashlib.sha256(password.encode())
         pass_enc = enc.hexdigest()
         #instanciar clase para acceso a BD
         usuario = Usuario()
         existeCorreo = usuario.consultarUsuario(correo,"correo")
         if existeCorreo:
            flash('El correo utilizado ya se encuentra asociado a una cuenta.')
            return redirect(url_for('registrarse'))
         
         existeId = usuario.consultarUsuario(numDocumento)

         if existeId:
            flash('La identificación utilizada ya se encuentra asociada a una cuenta.')
            return redirect(url_for('registrarse'))
            
         usuario.registrarse(nombres, apellidos, tipoDocumento, numDocumento, pais, genero, fechaNacimiento, codigoMarcacion,telefono, correo, pass_enc)
   #flash('Datos Guardados Exitosamente.')
   return render_template("registrarse.html", form = form)
   

@app.route("/consultar-vuelo", methods = ["GET", "POST"])
def consultarvuelo():
   form = frmConsVuelo()
   consVuelo = ""
   if request.method == "POST":
      idVuelo =request.form.get('consvuelo')
      vuelo = Vuelo()
      if 'idUser' in session:
         consVuelo = vuelo.consultarVuelo(idVuelo, session['idUser'])
      else:
         consVuelo = vuelo.consultarVuelo(idVuelo)
      
   form.validate_on_submit()
   return render_template("consultar-vuelo.html", form = form, consVuelo = consVuelo)

@app.route("/buscar-vuelo", methods = ["GET", "POST"])
def buscarvuelo():
   vuelos=[]
   form = frmBuscarVuelo()
   autenticado = False
   if form.validate_on_submit():
      vuelo = Vuelo()
      origenVuelo =request.form.get('ciudadorigen')
      destinoVuelo =request.form.get('ciudaddestino')
      if 'idUser' in session:
         idUser=session['idUser']
         autenticado = True
         print(idUser)
      else:
         idUser = ""
         
      vuelos = vuelo.buscarVuelos("",origenVuelo,destinoVuelo,idUser,"")
      if vuelos:
         flash('Mostrando resultados para la búsqueda')
      else:
         flash('No se encontraron resultados')
   return render_template("buscar-vuelo.html", form = form, vuelos=vuelos, autenticado = autenticado)

@app.route("/recuperar-cuenta", methods = ["GET", "POST"])
def recuperarcuenta():
   form = frmRecuperar()
   form.validate_on_submit()
   return render_template("recuperar-cuenta.html", form=form)

@app.route("/superadmin", methods = ["GET", "POST"])
def superadmin():
   #verifica que el usuario esté logueado y tenga rol de superadmin
   if 'idUser' in session and session["rol"] == 3:
      return render_template("superadmin.html", session=session)
   else:
      flash('Usted no tiene permisos para acceder a esta página.')
      return redirect(url_for('paginaprincipal'))

@app.route("/gestion-usuarios", methods = ["GET", "POST"])
def gestionusuarios():
      #verifica que el usuario esté logueado y tenga rol de superadmin
   if 'idUser' in session and session["rol"] == 3:
      consUsuarios =""
      form = frmBuscarUsuario()
      if request.method == "GET":
         idUser = ""
      consUsuario = ""
      if request.method == "POST":
         idUser = request.form.get('consUsuario')
         infoUser = Usuario()
         consUsuarios = infoUser.consultarUsuario(idUser)
      form.validate_on_submit()
      return render_template("gestion-usuarios.html", form=form, consUsuarios = consUsuarios,idUser = idUser)
   else:
      flash('Usted no tiene permisos para acceder a esta página.')
      return redirect(url_for('paginaprincipal'))

@app.route("/reviews", methods = ["GET", "POST"])
def reviews():
   if 'idUser' in session and session["rol"] == 1:
      pasajero = Pasajero()
      reviews = pasajero.consultarReviews(session['idUser'])
      return render_template("reviews.html", reviews=reviews)
   elif 'idUser' in session and session["rol"] == 2:
      piloto = Piloto()
      reviews = piloto.consultarReviewsPi(session['idUser'])
      return render_template("reviews.html", reviews=reviews)
     

@app.route("/gestion-vuelos", methods = ["GET", "POST"])
def gestionvuelos():
   #verifica que el usuario esté logueado y tenga rol de superadmin
   if 'idUser' in session and session["rol"] == 3:
      form = frmConsVuelo()
      vuelo = Vuelo()
      if form.validate_on_submit():
         busqueda = request.form.get('consvuelo')
         vuelos = vuelo.buscarVuelos("total","","","",busqueda)
         titulo = "Resultados"
      else:
         titulo = "Últimos vuelos"
         vuelos = vuelo.consultarVuelos()
      
      return render_template("gestion-vuelos.html", form=form, vuelos=vuelos, titulo=titulo)
          
   else:
      flash('Usted no tiene permisos para acceder a esta página.')
      return redirect(url_for('paginaprincipal'))

@app.route("/crear-usuario", methods = ["GET", "POST"])
def crearusuario():
   form =frmCrearEditarUsuario()
   if 'idUser' in session and session["rol"] == 3: 
      if request.method == "POST":        
         
         if form.validate_on_submit():
            nombres = form.nombres.data 
            apellidos = form.apellidos.data 
            tipoDocumento = form.tipoDocumento.data
            numDocumento = form.numDocumento.data 
            fechaNacimiento = form.fechaNacimiento.data
            telefono = form.telefono.data 
            correo = form.correo.data 
            genero = form.genero.data
            pais = form.pais.data  
            rol = form.rol.data 
            codigoMarcacion = form.codigoMarcacion.data
            password = numDocumento
            #Cifrar el password
            enc = hashlib.sha256(password.encode())
            pass_enc = enc.hexdigest()
            usuario = Usuario()
            usuario.registrarse(nombres, apellidos, tipoDocumento, numDocumento, pais, genero, fechaNacimiento, codigoMarcacion,telefono, correo, pass_enc)
            flash('Usuario guardado con éxito.')
      return render_template("crear-usuario.html", form=form, datosUser="")
   else:
      flash('Usted no tiene permisos para acceder a esta página.')
      return redirect(url_for('paginaprincipal'))
 
@app.route("/editar-usuario/<idUser>", methods = ["GET", "POST"])
def editarusuario(idUser):
   if 'idUser' in session and session["rol"] == 3:
      usuario = Usuario()
      datosUser = usuario.editarUsuario(idUser)
      form = frmCrearEditarUsuario(pais=datosUser['pais'], rol=datosUser['idRol'],tipoDocumento=datosUser['tipoDocumento'], genero=datosUser['genero'], codigoMarcacion = datosUser['codigoMarcacion'])
      
      titulo = "Editar Usuario"
      if form.validate_on_submit():
         nombres = request.form.get('nombres') 
         apellidos = request.form.get('apellidos') 
         tipoDocumento = request.form.get('tipoDocumento') 
         fechaNacimiento = request.form.get('fechaNacimiento')
         pais = request.form.get('pais') 
         telefono = request.form.get('telefono') 
         correo = request.form.get('correo') 
         genero = request.form.get('genero') 
         idRol = request.form.get('rol') 
         codigoMarcacion = request.form.get('codigoMarcacion') 
         usuario.actualizarUsuario(nombres,apellidos,tipoDocumento,fechaNacimiento,pais,codigoMarcacion,telefono,correo,genero,idRol,idUser)                                  
         datosUser = usuario.editarUsuario(idUser) 
         flash('Usuario editado con éxito.')
         return render_template("crear-usuario.html", form=form,datosUser=datosUser, titulo=titulo) 
      return render_template("crear-usuario.html", form=form,datosUser=datosUser, titulo=titulo)          
   else:
      flash('Usted no tiene permisos para acceder a esta página.')
      return redirect(url_for('paginaprincipal'))

@app.route("/eliminar-usuario/<idUser>", methods = ["GET", "POST"])
def eliminarusuario(idUser):
   if 'idUser' in session and session["rol"] == 3:
      user = Usuario()
      user.eliminar(idUser)
      return redirect(url_for('gestionusuarios'))           
   else:
      flash('Usted no tiene permisos para acceder a esta página.')
      return redirect(url_for('paginaprincipal'))

@app.route("/crear-vuelo", methods = ["GET", "POST"])
def crearvuelo():
   if 'idUser' in session and session["rol"] == 3:
      
      form = frmCrearEditarVuelo()
      if form.validate_on_submit():
         vuelo = Vuelo()
         capacidad = request.form.get('capacidad')
         origenVuelo = request.form.get('origenVuelo')
         destinoVuelo = request.form.get('destinoVuelo')
         estadoVuelo = request.form.get('estadoVuelo')
         avion =request.form.get('avion')
         fecha = request.form.get('fecha')
         idPiloto = request.form.get('idPiloto')
         idcoPiloto = request.form.get('idcoPiloto')
         if idPiloto == idcoPiloto:
            flash('Piloto y co-piloto no pueden ser iguales.')
            return render_template("crear-vuelo.html", form = form) 
         vuelo.crearVuelo(capacidad, origenVuelo, destinoVuelo, avion, fecha, idPiloto, idcoPiloto,estadoVuelo)
         flash('Se creó el vuelo con éxito')
         return redirect(url_for('gestionvuelos'))
      return render_template("crear-vuelo.html", form = form)        
   else:
      flash('Usted no tiene permisos para acceder a esta página.')
      return redirect(url_for('paginaprincipal'))

@app.route("/editar-vuelo/<idVuelo>", methods = ["GET", "POST"])
def editarvuelo(idVuelo):
   if 'idUser' in session and session["rol"] == 3:
      form = frmCrearEditarVuelo()
      vuelo = Vuelo()
      vueloencontrado = vuelo.consultarVuelo(idVuelo)
      if request.method == "POST":
         form.validate_on_submit()
         capacidad = request.form.get('capacidad')
         origenVuelo = request.form.get('origenVuelo')
         destinoVuelo = request.form.get('destinoVuelo')
         estadoVuelo = request.form.get('estadoVuelo')
         avion =request.form.get('avion')
         fecha = request.form.get('fecha')
         idPiloto = request.form.get('idPiloto')
         idcoPiloto = request.form.get('idcoPiloto')
         if idPiloto == idcoPiloto:
            flash('Piloto y co-piloto no pueden ser iguales.')
            return render_template("crear-vuelo.html", form = form) 
         vuelo.editarVuelo(capacidad, origenVuelo, destinoVuelo, avion, fecha, idPiloto, idcoPiloto,estadoVuelo, idVuelo)
         flash('Se editó el vuelo con éxito')
         return redirect(request.url)
      return render_template("editar-vuelo.html", form = form, vuelo = vueloencontrado)       
   else:
      flash('Usted no tiene permisos para acceder a esta página.')
      return redirect(url_for('paginaprincipal'))

@app.route("/eliminar-vuelo/<idVuelo>")
def eliminarVuelo(idVuelo):
   if 'idUser' in session and session["rol"] == 3:
      vuelo = Vuelo()
      vuelo.eliminarVuelo(idVuelo)
      flash('El vuelo se ha eliminado con éxito.')
      return redirect(url_for('gestionvuelos'))
   else:
      flash('Usted no tiene permisos para acceder a esta página.')
      return redirect(url_for('paginaprincipal'))

@app.route("/reservar-vuelo/<idVuelo>")
def reservarVuelo(idVuelo):
   if 'idUser' in session:
      vuelo = Vuelo()
      vuelo.reservarVuelo(idVuelo, session['idUser'])
      flash('El vuelo se ha reservado con éxito.')
      return redirect(url_for('misvuelos'))
   else:
      flash('Usted no tiene permisos para acceder a esta página.')
      return redirect(url_for('paginaprincipal'))

@app.route("/cancelar-reserva/<idVuelo>")
def cancelarReservaVuelo(idVuelo):
   if 'idUser' in session:
      vuelo = Vuelo()
      vuelo.cancelarReservaVuelo(idVuelo, session['idUser'])
      
      #vuelos = vuelo.buscarVuelos("total","","","",idVuelo)
      flash('La reserva se ha cancelado.')
      return redirect(url_for('buscarvuelo'))
   else:
      flash('¡Debe ingresar al sistema para poder reservar!')
      return redirect(url_for('misvuelos'))
@app.route("/misvuelos", methods=["GET", "POST"])
def misvuelos():
   if 'idUser' in session:
      vuelo = Vuelo()
      ##generar vuelos que el usuario tiene reservados y que han finalizado
      vuelos = vuelo.buscarVuelos("reservas","","",session['idUser'],"")
      form = frmPublicarReview()
      if form.validate_on_submit():
         idVuelo =request.form.get('idVuelo')
         comment =request.form.get('review')
         puntuacion =request.form.get('puntaje')
         fechaReview = datetime.today().strftime('%d-%m-%Y')
         pasajero = Pasajero()
         tieneReserva = pasajero.consultarReserva(session['idUser'],idVuelo)
         if tieneReserva:
            tieneReview = pasajero.consultarReview(session['idUser'], idVuelo)
         else:
            flash('Usted no puede publicar una reseña para este vuelo.')
         if tieneReview:
            flash('Usted ya ha publicado una reseña para este vuelo')
         else:
            pasajero.publicarReview(session['idUser'],idVuelo,comment, puntuacion,fechaReview)
            flash('Se publicó la reseña')
            return redirect(request.url)
      return render_template("reservas.html", vuelos = vuelos, form=form)
   else:
      flash('No tiene permisos para acceder a está página.')
      return redirect(url_for('paginaprincipal'))
@app.route("/piloto", methods = ["GET", "POST"])
def piloto():
   if 'idUser' in session and session["rol"] == 2:
      vueloPiloto = ""
      datosPiloto = ""
      piloto = Piloto()
      vueloPiloto = piloto.consultarVuelos(session["idUser"])
      datosPiloto = piloto.consultarPerfil(session["idUser"])
         
      return render_template("piloto.html", vueloPiloto = vueloPiloto, datosPiloto=datosPiloto)
   else:
      flash('Usted no tiene permisos para acceder a esta página.')
      return redirect(url_for('paginaprincipal'))
# -------------------------------------------------------------------------
@app.route("/buscarpiloto")
def buscarpiloto():
   nombrePiloto = request.args.get('nombre')
   piloto = Piloto()
   resultados = piloto.buscarPiloto(nombrePiloto)
   return Response(json.dumps(resultados), mimetype='application/json')


@app.route("/pasajeros", methods = ["GET", "POST"])
def pasajeros():
          #verifica que el usuario esté logueado y tenga rol de superadmin
   if 'idUser' in session and session["rol"] == 1:
      return render_template("pasajeros.html", session = session)
   else:
      flash('Usted no tiene permisos para acceder a esta página.')
      return redirect(url_for('paginaprincipal'))

@app.route("/vuelo/<idVuelo>/comentarios")
def verreviews(idVuelo):
   idRol = ""
   if 'idUser' in session and (session['rol'] == 2 or session['rol'] == 3):
      idRol = session['rol']
      if idRol == 3:
         puedeVerReview = True
      elif idRol == 2:
         piloto = Piloto()
         puedeVerReview = piloto.consultarVuelo(session['idUser'], idVuelo)
      
      if puedeVerReview:
         vuelo= Vuelo()
         reviewsVuelo = vuelo.verReviewsVuelo(idVuelo)
         infoVuelo =""
         if reviewsVuelo:
            infoVuelo = vuelo.consultarVuelo(idVuelo)
         return render_template('reviews.html', reviewsVuelo = reviewsVuelo, idRol = idRol, infoVuelo=infoVuelo)
      else:
         flash('Usted no tiene permisos para ver esta página')
         return redirect(url_for('paginaprincipal'))
   else:
         flash('Usted no tiene permisos para ver esta página')
         return redirect(url_for('paginaprincipal'))

@app.route("/publicar-review", methods = ["GET", "POST"])
def publicarreview():
   form = frmPublicarReview()
   form.validate_on_submit()
   return render_template("publicar-review.html",form=form)




