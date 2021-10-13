from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField ,BooleanField, \
    SubmitField
from wtforms.fields.core import DateField, IntegerField, SelectField
from wtforms.validators import ValidationError, DataRequired, \
    Email, EqualTo, Length
import formularios as formularios



app = Flask(__name__)
app.config['SECRET_KEY']="skkakjasdlkasoiq123123sdajkadskl"

@app.route("/", methods = ["GET"])
def paginaprincipal():
   return render_template("pagina-principal.html")





@app.route("/ingresar", methods = ["GET", "POST"])
def ingresar():
   formularioIngreso = formularios.Ingreso()
   formularioIngreso.validate_on_submit()
   return render_template("ingresar.html", formularioIngreso = formularioIngreso)

@app.route("/registrarse", methods = ["GET", "POST"])
def registrarse():
   form = formularios.Registro()
   form.validate_on_submit()
   return render_template("registrarse.html", form = form)

class cvueloform(FlaskForm):
   consvuelo = StringField(label="consvuelo", validators=[DataRequired(message ='Es necesario digitar el codigo de vuelo'), Length (min=1, max=6, message ='el código debe contener por lo menos %(min)d caracter/es y máximo %(max)d')])
   botonEnviar = SubmitField(label='Consultar')

@app.route("/consultar-vuelo", methods = ["GET", "POST"])
def consultarvuelo():
   formularioconsultarvuelo = cvueloform()
   formularioconsultarvuelo.validate_on_submit()
   return render_template("consultar-vuelo.html", formularioconsultarvuelo = formularioconsultarvuelo)

class bvueloform(FlaskForm):
   ciudadorigen = StringField(label='ciudadorigen', validators=[DataRequired(message ='Es necesario establecer la ciudad de origen'), Length (min=1, max=120, message ='La ciudad debe tener por lo menos %(min)d caracter')])
   ciudaddestino = StringField(label='ciudaddestino',
      validators=[
         DataRequired(message ='Es necesario establecer la ciudad de destino'),
         ])
   botonEnviar = SubmitField(label="BUSCAR")

@app.route("/buscar-vuelo", methods = ["GET", "POST"])
def buscarvuelo():
   formulariobuscarvuelo = bvueloform()
   formulariobuscarvuelo.validate_on_submit()
   return render_template("buscar-vuelo.html", formulariobuscarvuelo = formulariobuscarvuelo)

class Recuperar(FlaskForm):
   datoRecuperar = StringField(label="recuperacion",
   validators=[DataRequired(),
   Email(message='El correo no es válido'),
   Length(min=6, max=120, message='El correo debe tener mínimo %(min)d caracteres y %(max)d máximo')]
   )
   botonRecuperar = SubmitField(label="Enviar")

@app.route("/recuperar-cuenta", methods = ["GET", "POST"])
def recuperarcuenta():
   datosRecuperacion = Recuperar()
   datosRecuperacion.validate_on_submit()
   return render_template("recuperar-cuenta.html", datosRecuperacion=datosRecuperacion)

@app.route("/superadmin", methods = ["GET", "POST"])
def superadmin():
   return render_template("superadmin.html")

@app.route("/gestion-usuarios", methods = ["GET", "POST"])
def gestionusuarios():
   form = formularios.BuscarUsuario()
   form.validate_on_submit()
   return render_template("gestion-usuarios.html", form=form)

@app.route("/reviews", methods = ["GET", "POST"])
def reviews():
   return render_template("reviews.html")

@app.route("/gestion-vuelos", methods = ["GET", "POST"])
def gestionvuelos():
   form = cvueloform()
   form.validate_on_submit()
   return render_template("gestion-vuelos.html", form=form)



@app.route("/crear-usuario", methods = ["GET", "POST"])
def crearusuario():
   form = formularios.CrearEditarUsuario()
   form.validate_on_submit()
   return render_template("crear-usuario.html", form=form)

@app.route("/editar-usuario", methods = ["GET", "POST"])
def editarusuario():
   form = formularios.CrearEditarUsuario()
   form.validate_on_submit()
   return render_template("editar-usuario.html", form=form)
   
@app.route("/eliminar-usuario", methods = ["GET", "POST"])
def eliminarusuario():
   return render_template("gestion-usuarios.html")  
   # Mensaje de confirmación de accion eliminar PENDIENTE 

class CrearVuelo(FlaskForm):
    ciudadOrigen = StringField(label='ciudadOrigen', validators=[DataRequired(), Length(min = 5, max = 50, message='Campo Ciudad Origen Requerido:Mínimo 2 y máximo 50 caracteres.')])
    ciudadDestino = StringField(label='ciudadDestino', validators=[DataRequired(), Length(min = 5, max = 50, message='Campo Ciudad Origen Requerido:Mínimo 2 y máximo 50 caracteres.')])
    codigo = StringField(label='codigo', validators=[DataRequired(), Length(min = 2, max = 10, message='Campo Código Requerido:Mínimo 2 y máximo 10 caracteres.')])
    avion = StringField(label='avion', validators=[DataRequired(), Length(min = 5, max = 30,  message='Campo Avión Requerido:Mínimo 5 y máximo 30 caracteres.')])
    capacidad = StringField(label='capacidad', validators=[DataRequired(), Length(min = 1, max = 3, message='Campo Capacidad Requerido:Mínimo 1 y máximo 3 caracteres')])
    hora = StringField(label='hora', validators=[DataRequired(), Length(min = 9 , max = 9,  message='Campo Capacidad Requerido:Escribir formato: HH:MM:SS.')])
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

@app.route("/publicar-review", methods = ["GET", "POST"])
def publicarreview():
   return render_template("publicar-review.html")



