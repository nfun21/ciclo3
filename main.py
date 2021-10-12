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
#
@app.route("/registrarse", methods = ["GET", "POST"])
def registrarse():
   return render_template("registrarse.html")

@app.route("/consultar-vuelo", methods = ["GET", "POST"])
def consultarvuelo():
   return render_template("consultar-vuelo.html")

@app.route("/recuperar-cuenta", methods = ["GET", "POST"])
def recuperarcuenta():
   return render_template("recuperar-cuenta.html")

@app.route("/superadmin", methods = ["GET", "POST"])
def superadmin():
   return render_template("superadmin.html")

@app.route("/gestion-usuarios", methods = ["GET", "POST"])
def gestionusuarios():
   return render_template("gestion-usuarios.html")

@app.route("/reviews", methods = ["GET", "POST"])
def reviews():
   return render_template("reviews.html")

@app.route("/gestion-vuelos", methods = ["GET", "POST"])
def gestionvuelos():
   return render_template("gestion-vuelos.html")

@app.route("/crear-usuario", methods = ["GET", "POST"])
def crearusuario():
   return render_template("crear-usuario.html")

@app.route("/editar-usuario", methods = ["GET", "POST"])
def editarusuario():
   return render_template("editar-usuario.html")
   
@app.route("/eliminar-usuario", methods = ["GET", "POST"])
def eliminarusuario():
   return render_template("gestion-usuarios.html")  
   # Mensaje de confirmación de accion eliminar PENDIENTE 

@app.route("/crear-vuelo", methods = ["GET", "POST"])
def crearvuelo():
   return render_template("crear-vuelo.html")

@app.route("/editar-vuelo", methods = ["GET", "POST"])
def editarvuelo():
   return render_template("editar-vuelo.html")

@app.route("/piloto", methods = ["GET", "POST"])
def piloto():
   return render_template("piloto.html")

@app.route("/pasajeros", methods = ["GET", "POST"])
def pasajeros():
   return render_template("pasajeros.html")



