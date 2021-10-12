from flask import Flask, render_template

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



