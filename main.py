from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, \
    SubmitField
from wtforms.validators import InputRequired, ValidationError, DataRequired, \
    Email, EqualTo, Length



app = Flask(__name__)
app.config['SECRET_KEY']="skkakjasdlkasoiq123123sdajkadskl"

@app.route("/", methods = ["GET"])
def paginaprincipal():
   return render_template("pagina-principal.html")

class Ingresar(FlaskForm):
   correo = StringField(label="correo",
      validators=[DataRequired(),
      Email(message='El correo no es válido'),
      Length(min=8, max=120, message='El correo debe tener mínimo 8 caracteres y máximo 120')]
      )
   password = PasswordField(label='contraseña', 
      validators=[DataRequired(),
      Length(min=8, max=15, message='La contraseña debe tener mínimo 8 caracteres y máximo 15')]
      )
   botonEnviar = SubmitField(label="INGRESAR")

@app.route("/ingresar", methods = ["GET", "POST"])
def ingresar():
   formularioIngreso = Ingresar()
   formularioIngreso.validate_on_submit()
   return render_template("ingresar.html", formularioIngreso = formularioIngreso)

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

class CrearVuelo(FlaskForm):
    ciudadOrigen = StringField(label='ciudadOrigen', validators=[DataRequired(), Length(min = 5, max = 50, message='Ciudad Origen Requerida. ')])
   #  ciudadDestino = StringField(label='ciudadDestino', validators=[DataRequired(), Length(min = 5, message='Ciudad Destino Requerida.')])
   #  codigo = StringField(label='codigo', validators=[DataRequired(), Length(min = 5, message='Código Requerido.')])
   #  avion = StringField(label='avion', validators=[DataRequired(), Length(min = 5, message='Tipo de Avión Requerido.')])
   #  capacidad = StringField(label='capacidad', validators=[DataRequired(), Length(min = 5, message='Capacidad de Avión Requerida.')])
   #  hora = StringField(label='hora', validators=[DataRequired(), Length(min = 5, message='Hora Requerida.')])
    botonGuardar = SubmitField(label="GUARDAR")

@app.route("/crear-vuelo", methods = ["GET", "POST"])
def crearvuelo():
   formularioCrearVuelo = CrearVuelo()
   formularioCrearVuelo.validate_on_submit()
   return render_template("crear-vuelo.html", formularioCrearVuelo = formularioCrearVuelo)

@app.route("/editar-vuelo", methods = ["GET", "POST"])
def editarvuelo():
   return render_template("editar-vuelo.html")

@app.route("/piloto", methods = ["GET", "POST"])
def piloto():
   return render_template("piloto.html")

@app.route("/pasajeros", methods = ["GET", "POST"])
def pasajeros():
   return render_template("pasajeros.html")



