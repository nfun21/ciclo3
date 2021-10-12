from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, \
    SubmitField
from wtforms.validators import ValidationError, DataRequired, \
    Email, EqualTo, Length



app = Flask(__name__)
app.config['SECRET_KEY']="skkakjasdlkasoiq123123sdajkadskl"

@app.route("/", methods = ["GET"])
def paginaprincipal():
   return render_template("pagina-principal.html")

class FIngreso(FlaskForm):
   correo = StringField('correo', 
        validators=[DataRequired(), 
        Email(message='Correo inválido'), 
        Length(min=8, message='lalala')])
   password = PasswordField(label=('Password'), 
        validators=[DataRequired(), 
        Length(min=8, message='La contraseña debe tener mínimo %(min)d caracteres.')])
   submit = SubmitField(label=('INGRESAR'))
@app.route("/ingresar", methods = ["GET", "POST"])
def ingresar():
   form = FIngreso()
   
   if form.validate_on_submit():
      return 'form validated'
   return render_template("ingresar.html", form=form)

@app.route("/registrarse", methods = ["GET", "POST"])
def registrarse():
   return render_template("registrarse.html")

@app.route("/consultar-vuelo", methods = ["GET", "POST"])
def consultarvuelo():
   return render_template("consultar-vuelo.html")

@app.route("/recuperar-cuenta", methods = ["GET", "POST"])
def recuperarcuenta():
   return render_template("recuperar-cuenta.html")


