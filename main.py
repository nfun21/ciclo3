from typing import Text
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField ,BooleanField, \
    SubmitField
from wtforms.fields.core import DateField, IntegerField, SelectField
from wtforms.validators import ValidationError, DataRequired, \
    Email, EqualTo, Length
from formularios import*
import os
import hashlib
from werkzeug.utils import escape, redirect
from clases import *


app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route("/", methods = ["GET"])
def paginaprincipal():
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

@app.route("/registrarse", methods = ["GET", "POST"])
def registrarse():
   form = frmRegistro()
   form.validate_on_submit()
   return render_template("registrarse.html", form = form)

@app.route("/consultar-vuelo", methods = ["GET", "POST"])
def consultarvuelo():
   form = frmConsVuelo()
   consVuelo = ""
   if request.method == "POST":
      idVuelo =request.form.get('consvuelo')
      vuelo = Vuelo()
      consVuelo = vuelo.consultarVuelo(idVuelo)
      
   form.validate_on_submit()
   return render_template("consultar-vuelo.html", form = form, consVuelo = consVuelo)

@app.route("/buscar-vuelo", methods = ["GET", "POST"])
def buscarvuelo():
   form = frmBuscarVuelo()
   form.validate_on_submit()
   return render_template("buscar-vuelo.html", form = form)

@app.route("/recuperar-cuenta", methods = ["GET", "POST"])
def recuperarcuenta():
   form = frmRecuperar()
   form.validate_on_submit()
   return render_template("recuperar-cuenta.html", form=form)

@app.route("/superadmin", methods = ["GET", "POST"])
def superadmin():
   #verifica que el usuario esté logueado y tenga rol de superadmin
   if 'idUser' in session and session["rol"] == 3:
      return render_template("superadmin.html")
   else:
      flash('Usted no tiene permisos para acceder a esta página.')
      return redirect(url_for('paginaprincipal'))

@app.route("/gestion-usuarios", methods = ["GET", "POST"])
def gestionusuarios():
      #verifica que el usuario esté logueado y tenga rol de superadmin
   if 'idUser' in session and session["rol"] == 3:
      form = frmBuscarUsuario()
      form.validate_on_submit()
      return render_template("gestion-usuarios.html", form=form)
   else:
      flash('Usted no tiene permisos para acceder a esta página.')
      return redirect(url_for('paginaprincipal'))

@app.route("/reviews", methods = ["GET", "POST"])
def reviews():
   return render_template("reviews.html")

@app.route("/gestion-vuelos", methods = ["GET", "POST"])
def gestionvuelos():
   #verifica que el usuario esté logueado y tenga rol de superadmin
   if 'idUser' in session and session["rol"] == 3:
      form = frmConsVuelo()
      form.validate_on_submit()
      return render_template("gestion-vuelos.html", form=form)
          
   else:
      flash('Usted no tiene permisos para acceder a esta página.')
      return redirect(url_for('paginaprincipal'))

@app.route("/crear-usuario", methods = ["GET", "POST"])
def crearusuario():
   if 'idUser' in session and session["rol"] == 3:         
      form = frmCrearEditarUsuario()
      form.validate_on_submit()
      return render_template("crear-usuario.html", form=form)
   else:
      flash('Usted no tiene permisos para acceder a esta página.')
      return redirect(url_for('paginaprincipal'))

@app.route("/editar-usuario", methods = ["GET", "POST"])
def editarusuario():
   if 'idUser' in session and session["rol"] == 3:
      form = frmCrearEditarUsuario()
      form.validate_on_submit()
      return render_template("editar-usuario.html", form=form)        
   else:
      flash('Usted no tiene permisos para acceder a esta página.')
      return redirect(url_for('paginaprincipal'))
   
@app.route("/eliminar-usuario", methods = ["GET", "POST"])
def eliminarusuario():
   if 'idUser' in session and session["rol"] == 3:
      return render_template("gestion-usuarios.html")  
              
   else:
      flash('Usted no tiene permisos para acceder a esta página.')
      return redirect(url_for('paginaprincipal'))
   
@app.route("/crear-vuelo", methods = ["GET", "POST"])
def crearvuelo():
   if 'idUser' in session and session["rol"] == 3:
      form = frmCrearVuelo()
      form.validate_on_submit()
      return render_template("crear-vuelo.html", form = form)        
   else:
      flash('Usted no tiene permisos para acceder a esta página.')
      return redirect(url_for('paginaprincipal'))

@app.route("/editar-vuelo", methods = ["GET", "POST"])
def editarvuelo():
   if 'idUser' in session and session["rol"] == 3:
      form = frmEditarVuelo()
      form.validate_on_submit()
      return render_template("editar-vuelo.html", form = form)       
   else:
      flash('Usted no tiene permisos para acceder a esta página.')
      return redirect(url_for('paginaprincipal'))
   
@app.route("/piloto", methods = ["GET", "POST"])
def piloto():
   return render_template("piloto.html")

@app.route("/pasajeros", methods = ["GET", "POST"])
def pasajeros():
          #verifica que el usuario esté logueado y tenga rol de superadmin
   if 'idUser' in session and session["rol"] == 1:
      return render_template("pasajeros.html")
   else:
      flash('Usted no tiene permisos para acceder a esta página.')
      return redirect(url_for('paginaprincipal'))


@app.route("/publicar-review", methods = ["GET", "POST"])
def publicarreview():
   form = frmPublicarReview()
   form.validate_on_submit()
   return render_template("publicar-review.html",form=form)




