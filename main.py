from typing import Text
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField ,BooleanField, \
    SubmitField
from wtforms.fields.core import DateField, IntegerField, SelectField
from wtforms.validators import ValidationError, DataRequired, \
    Email, EqualTo, Length
from formularios import*
import os
from clases import *


app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route("/", methods = ["GET"])
def paginaprincipal():
   return render_template("pagina-principal.html")

@app.route("/ingresar", methods = ["GET", "POST"])
def ingresar():
   form = frmIngreso()
   form.validate_on_submit()
   return render_template("ingresar.html", form = form)

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
      #debes consultar con el id del Vuelo en la tabla de VueloPilotos
      #debes consultar cons los ids de los pilotos, los nombres en a tabla de Usuario
      #luego, debes unir esos nombres en la variable de consVuelo
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
   return render_template("superadmin.html")

@app.route("/gestion-usuarios", methods = ["GET", "POST"])
def gestionusuarios():
   form = frmBuscarUsuario()
   form.validate_on_submit()
   return render_template("gestion-usuarios.html", form=form)

@app.route("/reviews", methods = ["GET", "POST"])
def reviews():
   return render_template("reviews.html")

@app.route("/gestion-vuelos", methods = ["GET", "POST"])
def gestionvuelos():
   form = frmConsVuelo()
   form.validate_on_submit()
   return render_template("gestion-vuelos.html", form=form)

@app.route("/crear-usuario", methods = ["GET", "POST"])
def crearusuario():
   form = frmCrearEditarUsuario()
   form.validate_on_submit()
   return render_template("crear-usuario.html", form=form)

@app.route("/editar-usuario", methods = ["GET", "POST"])
def editarusuario():
   form = frmCrearEditarUsuario()
   form.validate_on_submit()
   return render_template("editar-usuario.html", form=form)
   
@app.route("/eliminar-usuario", methods = ["GET", "POST"])
def eliminarusuario():
   return render_template("gestion-usuarios.html")  
   
@app.route("/crear-vuelo", methods = ["GET", "POST"])
def crearvuelo():
   form = frmCrearVuelo()
   form.validate_on_submit()
   return render_template("crear-vuelo.html", form = form)

@app.route("/editar-vuelo", methods = ["GET", "POST"])
def editarvuelo():
   form = frmEditarVuelo()
   form.validate_on_submit()
   return render_template("editar-vuelo.html", form = form)
   
@app.route("/piloto", methods = ["GET", "POST"])
def piloto():
   return render_template("piloto.html")

@app.route("/pasajeros", methods = ["GET", "POST"])
def pasajeros():
   return render_template("pasajeros.html")

@app.route("/publicar-review", methods = ["GET", "POST"])
def publicarreview():
   form = frmPublicarReview()
   form.validate_on_submit()
   return render_template("publicar-review.html",form=form)




