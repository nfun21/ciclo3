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



app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route("/", methods = ["GET"])
def paginaprincipal():
   if 'idUser' in session:
      if session['rol']==1:
         return redirect(url_for('pasajero'))
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
         password = form.password.data
         #Cifrar el password
         enc = hashlib.sha256(password.encode())
         pass_enc = enc.hexdigest()
         #instanciar clase para acceso a BD
         usuario = Usuario()
         usuario.registrarse(nombres, apellidos, tipoDocumento, numDocumento, pais, genero, fechaNacimiento, telefono, correo, pass_enc)
   flash('Datos Guardados Exitosamente.')
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
      form = frmBuscarUsuario()
      if request.method == "GET":
         idUser = ""
      consUsuario = ""
      if request.method == "POST":
         idUser = request.form.get('consUsuario')
         infoUser = Usuario()
         consUsuario = infoUser.consultarUsuario(idUser)
      form.validate_on_submit()
      return render_template("gestion-usuarios.html", form=form, consUsuario = consUsuario,idUser = idUser)
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
def crearsuario():
   if 'idUser' in session and session["rol"] == 3:         
      form = frmCrearEditarUsuario()
      form.validate_on_submit()
      return render_template("crear-usuario.html", form=form)
   else:
      flash('Usted no tiene permisos para acceder a esta página.')
      return redirect(url_for('paginaprincipal'))
""" -------------------------------------------------------------------------------------------- """   
@app.route("/editar-usuario/<idUser>", methods = ["GET", "POST"])
def editarusuario(idUser):
   if 'idUser' in session and session["rol"] == 3:
      form = frmCrearEditarUsuario()      
      datosUser = ""
      usuario = Usuario()
      datosUser = usuario.editarUsuario(idUser) 
      form.validate_on_submit()
      if request.method == "POST":
         nombres = request.form.get('nombres') 
         apellidos = request.form.get('apellidos') 
         tipoDocumento = request.form.get('tipoDocumento') 
         fechaNacimiento = request.form.get('fechaNacimiento') 
         telefono = request.form.get('telefono') 
         correo = request.form.get('correo') 
         genero = request.form.get('genero') 
         idRol = request.form.get('rol') 
         usuario.actualizarUsuario(nombres,apellidos,tipoDocumento,fechaNacimiento,telefono,correo,genero,idRol,idUser)                                  
      return render_template("editar-usuario.html", form=form,datosUser=datosUser)        
   
   
   else:
      flash('Usted no tiene permisos para acceder a esta página.')
      return redirect(url_for('paginaprincipal'))
""" -------------------------------------------------------------------------------------------- """
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
         return redirect(url_for('paginaprincipal'))
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
      return redirect(url_for('buscarvuelo'))
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
      return redirect(url_for('consultarvuelo'))

@app.route("/piloto", methods = ["GET", "POST"])
def piloto():
   if 'idUser' in session and session["rol"] == 2:
      vueloPiloto = ""
      datosPiloto = ""
      piloto = Piloto()
      vueloPiloto = piloto.consultarVuelo(session["idUser"])
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


@app.route("/publicar-review", methods = ["GET", "POST"])
def publicarreview():
   form = frmPublicarReview()
   form.validate_on_submit()
   return render_template("publicar-review.html",form=form)




