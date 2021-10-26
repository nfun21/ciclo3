from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField ,BooleanField, \
    SubmitField
from wtforms.fields.core import DateField, DateTimeField, IntegerField, SelectField
from wtforms_validators import AlphaNumeric, Integer
from wtforms.validators import ValidationError, DataRequired, \
    Email, EqualTo, Length
import json
from datetime import datetime

class frmPublicarReview(FlaskForm):
   review= StringField(label="review",
   validators=[DataRequired(message="Es necesario que escriba un comentario."),Length(min=4, max=500, message='La reseña debe contener minimo %(min)d y %(max)d máximo de caracteres')])
   puntaje= SelectField(label="puntaje",
      choices=[
         ('1'),
         ('2'),
         ('3'),
         ('4'),
         ('5')
         ],
      validate_choice=True,
      validators=[
         DataRequired(message='El campo de puntaje no puede quedar vacío')
      ]
   )
  

   btnEnviar = SubmitField(label="Enviar")

class frmRecuperar(FlaskForm):
   datoRecuperar = StringField(label="recuperacion",
   validators=[DataRequired(),
   Email(message='El correo no es válido'),
   Length(min=6, max=120, message='El correo debe tener mínimo %(min)d caracteres y %(max)d máximo')]
   )
   botonRecuperar = SubmitField(label="Enviar")

class frmBuscarVuelo(FlaskForm):
   ciudadorigen = StringField(label='ciudadorigen', validators=[DataRequired(message ='Es necesario establecer la ciudad de origen'), Length (min=1, max=50, message ='La ciudad debe tener por lo menos %(min)d caracter')])
   ciudaddestino = StringField(label='ciudaddestino',
      validators=[
         DataRequired(message ='Es necesario establecer la ciudad de destino'), Length (min=1, max=50, message ='La ciudad debe tener por lo menos %(min)d caracter')
         ])
   botonEnviar = SubmitField(label='BUSCAR')

class frmCrearEditarVuelo(FlaskForm):
   origenVuelo = StringField(label='ciudadOrigen', validators=[DataRequired(), Length(min = 3, max = 50, message='Campo Ciudad Origen Requerido:Mínimo 2 y máximo 50 caracteres.')])
   destinoVuelo = StringField(label='ciudadDestino', validators=[DataRequired(), Length(min = 3, max = 50, message='Campo Ciudad Origen Requerido:Mínimo 2 y máximo 50 caracteres.')])
   avion = StringField(label='avion', validators=[DataRequired(), Length(min = 5, max = 30,  message='Campo Avión Requerido:Mínimo 5 y máximo 30 caracteres.')])
   capacidad = StringField(label='capacidad', validators=[DataRequired(), Length(min = 1, max = 3, message='Campo Capacidad Requerido:Mínimo 1 y máximo 3 caracteres')])
   estadoVuelo= SelectField(label="estadoVuelo",
   choices=[
      ('Programado'),
      ('Inicializado'),
      ('Abordando'),
      ('En vuelo'),
      ('Aterrizado'),
      ('Finalizado')
   ],
   validate_choice=True,
   validators=[
   DataRequired(message='El campo de Estado Vuelo no puede quedar vacío')
   ]
   )
   
   idPiloto = StringField(label='idPiloto', validators=[DataRequired(), Length(min = 1, max = 150, message='La id del piloto es muy corta o muy larga')])
   idcoPiloto = StringField(label='idCo-Piloto', validators=[DataRequired(), Length(min = 1, max = 150, message='La id del co-piloto es muy corta o muy larga')])
   fecha = StringField(label="fecha", validators=[DataRequired('La fecha no puede quedar vacía.')])
   botonGuardar = SubmitField(label="GUARDAR")

class frmIngreso(FlaskForm):
   correo = StringField(label="correo",
      validators=[DataRequired(),
      Email(message='El correo no es válido'),
      Length(min=2, max=120, message='El correo debe tener mínimo 8 caracteres y máximo 120')]
      )
   password = PasswordField(label='contraseña', 
      validators=[DataRequired(),
      Length(min=2, max=15, message='La contraseña debe tener mínimo 8 caracteres y máximo 15')]
      )
   botonEnviar = SubmitField(label="INGRESAR")
#validación para fecha de nacimiento. 
#No permite que se ingrese una fecha mayor a la actual.
def validate_date(form, field):
   hoy2 = datetime(field.data.year,field.data.month, field.data.day)
   if hoy2 > datetime.today():
      raise ValidationError("La fecha de nacimiento no puede ser mayor que la fecha actual")
def validarNumDoc(form, field):
  if form.tipoDocumento.data != 'PS' and not field.data.isnumeric():
        raise ValidationError("El número del documento de identidad debe ser numérico.")
class frmUsuario(FlaskForm):
   nombres=StringField(label='nombres',
      validators=[
         DataRequired(message='El campo de nombres no puede quedar vacío'),
         Length(min=3, max=50, message='El nombre no puede tener menos de 3 caracteres y más de 50')
      ]
   )

   apellidos=StringField(label='apellidos',
      validators=[
         DataRequired(message='El campo de apellidos no puede quedar vacío'),
         Length(min=3, max=50, message='El apellido no puede tener menos de 3 caracteres y más de 50')
      ]
   )

   tipoDocumento=SelectField(label='tipo doc',
      choices=[
         ('CC', 'Cédula de ciudadanía'),
         ('TI', 'Tarjeta de identidad'),
         ('PS', 'Pasaporte')
         ], 
         validate_choice=True,
         validators=[DataRequired(message='El campo de tipo de documento no puede quedar vacío')]
         )
         
  
   numDocumento = StringField(label='número doc',
      validators=[
         DataRequired(message='El campo de número de documento no puede quedar vacío'),
         Length(min=8, max=50, message="La identificación introducida es muy larga o muy corta"),
         AlphaNumeric(message="El número de identificación contiene caracteres prohibidos."),
         validarNumDoc
         
      ]
   )
   #######################  CAMPO PARA PAISES  #########################
   ###archivo json con los nombres de los  paises que llenan el select de pais
   f = open('static/paises.json',encoding="utf8")
   infoPaises = json.load(f)
   pais = SelectField(label="Pais de nacimiento:",
      choices=[(pais) for pais in infoPaises['nombres']], ##genera los nombres de los paises extraidos del archivo como una opción en el select.
      default="Colombia",
      validate_choice=True,
      validators=[DataRequired(message="Debe escoger un país.")]
   )
   
   #################################
   codigoMarcacion = SelectField(label="Código de marcación",
      choices=[(codigo) for codigo in infoPaises['marcacion']], ##genera los nombres de los paises extraidos del archivo como una opción en el select.
      default="+57",
      validate_choice=True,
      validators=[DataRequired(message="Debe escoger un código de marcación.")]
   )

   f.close()

   telefono=IntegerField(label="telefono",
      validators=[
         DataRequired(message='El campo de teléfono no puede quedar vacío'),
         
      ]
   )

   genero= SelectField(label="Genero:",
      choices=[('Prefiero no decirlo'), ('Masculino'), ('Femenino')], validate_choice=True,validators=[DataRequired(message="Debe escoger un género.")]
   )

   fechaNacimiento = DateField(label="Fecha nacimiento",
      
      validators=[DataRequired(message='El campo de fecha de nacimiento no puede quedar vacío'), validate_date]
      )

   correo = StringField(label="correo",
      validators=[DataRequired(message='El campo de correo no puede quedar vacío'),
      Email(message='El correo no es válido'),
      Length(min=8, max=120, message='El correo debe tener mínimo 8 caracteres y máximo 120')]
      )


class frmRegistro(frmUsuario):
   password = PasswordField(label='contraseña', 
      validators=[DataRequired(message='El campo de contraseña no puede quedar vacío'),
      Length(min=8, max=15, message='La contraseña debe tener mínimo 8 caracteres y máximo 15'),
      EqualTo('passwordConfirmar', message='Las contraseñas no coinciden')
      ]
   )
   passwordConfirmar = PasswordField(label="Confirmar contraseña")
   botonEnviar = SubmitField(label="REGISTRARSE")

class frmCrearEditarUsuario(frmUsuario):
   rol= SelectField(label='Rol',
      choices=[
         (1, 'PASAJERO'),
         (2, 'PILOTO'),
         (3, 'SUPERADMIN')
         ], 
         validate_choice=True,
         validators=[DataRequired(message='El campo de tipo de rol no puede quedar vacío')]
         
   )
   botonEnviar = SubmitField(label="GUARDAR")

class frmBuscarUsuario(FlaskForm):
   idUsuario = StringField(label="idUsuario", validators=[DataRequired(message =' '), Length (min=3, max=120, message ='El ID debe contener por lo menos %(min)d caracter/es y máximo %(max)d')])
   botonEnviar = SubmitField(label='Consultar')

class frmConsVuelo(FlaskForm):
   consvuelo = StringField(label="consvuelo", validators=[DataRequired(message ='Es necesario digitar el codigo de vuelo'), Length (min=1, max=50, message ='el código debe contener por lo menos %(min)d caracter/es y máximo %(max)d')])
   botonEnviar = SubmitField(label='Consultar')