from flask import Flask, render_template
from wtforms import Form

app = Flask(__name__)

@app.route("/", methods = ["GET"])
def paginaprincipal():
   return render_template("pagina-principal.html")

@app.route("/ingresar", methods = ["GET", "POST"])
def ingresar():
   return render_template("ingresar.html")

@app.route("/registrarse", methods = ["GET", "POST"])
def registrarse():
   return render_template("registrarse.html")

@app.route("/consultar-vuelo", methods = ["GET", "POST"])
def consultarvuelo():
   return render_template("consultar-vuelo.html")

@app.route("/recuperar-cuenta", methods = ["GET", "POST"])
def recuperarcuenta():
   return render_template("recuperar-cuenta.html")


