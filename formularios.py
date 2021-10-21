from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField ,BooleanField, \
    SubmitField
from wtforms.fields.core import DateField, IntegerField, SelectField
from wtforms.validators import ValidationError, DataRequired, \
    Email, EqualTo, Length

class frmPublicarReview(FlaskForm):
   review= StringField(label="review",
   validators=[DataRequired(message="Es necesario que escriba un comentario."),Length(min=4, max=750, message='La reseña debe contener minimo %(min)d y %(max)d máximo de caracteres')])
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
   ciudadorigen = StringField(label='ciudadorigen', validators=[DataRequired(message ='Es necesario establecer la ciudad de origen'), Length (min=1, max=120, message ='La ciudad debe tener por lo menos %(min)d caracter')])
   ciudaddestino = StringField(label='ciudaddestino',
      validators=[
         DataRequired(message ='Es necesario establecer la ciudad de destino'), Length (min=1, max=120, message ='La ciudad debe tener por lo menos %(min)d caracter')
         ])
   botonEnviar = SubmitField(label='BUSCAR')

class frmEditarVuelo(FlaskForm):
    ciudadOrigen = StringField(label='ciudadOrigen', validators=[DataRequired(), Length(min = 5, max = 50, message='Campo Ciudad Origen Requerido:Mínimo 2 y máximo 50 caracteres.')])
    ciudadDestino = StringField(label='ciudadDestino', validators=[DataRequired(), Length(min = 5, max = 50, message='Campo Ciudad Origen Requerido:Mínimo 2 y máximo 50 caracteres.')])
    codigo = StringField(label='codigo', validators=[DataRequired(), Length(min = 2, max = 10, message='Campo Código Requerido:Mínimo 2 y máximo 10 caracteres.')])
    avion = StringField(label='avion', validators=[DataRequired(), Length(min = 5, max = 30,  message='Campo Avión Requerido:Mínimo 5 y máximo 30 caracteres.')])
    capacidad = StringField(label='capacidad', validators=[DataRequired(), Length(min = 1, max = 3, message='Campo Capacidad Requerido:Mínimo 1 y máximo 3 caracteres')])
    hora = StringField(label='hora', validators=[DataRequired(), Length(min = 9 , max = 9,  message='Campo Hora Requerido:Escribir formato: HH:MM:SS.')])
    estadoVuelo= SelectField(label="estadoVuelo",
      choices=[
         ('Inicializado'),
         ('Abordando'),
         ('En Vuelo'),
         ('Aterrizado')
      ],
      validate_choice=True,
      validators=[
      DataRequired(message='El campo de Estado Vuelo no puede quedar vacío')
      ]
    )
    botonGuardar = SubmitField(label="GUARDAR")

class frmCrearVuelo(FlaskForm):
    ciudadOrigen = StringField(label='ciudadOrigen', validators=[DataRequired(), Length(min = 5, max = 50, message='Campo Ciudad Origen Requerido:Mínimo 2 y máximo 50 caracteres.')])
    ciudadDestino = StringField(label='ciudadDestino', validators=[DataRequired(), Length(min = 5, max = 50, message='Campo Ciudad Origen Requerido:Mínimo 2 y máximo 50 caracteres.')])
    codigo = StringField(label='codigo', validators=[DataRequired(), Length(min = 2, max = 10, message='Campo Código Requerido:Mínimo 2 y máximo 10 caracteres.')])
    avion = StringField(label='avion', validators=[DataRequired(), Length(min = 5, max = 30,  message='Campo Avión Requerido:Mínimo 5 y máximo 30 caracteres.')])
    capacidad = StringField(label='capacidad', validators=[DataRequired(), Length(min = 1, max = 3, message='Campo Capacidad Requerido:Mínimo 1 y máximo 3 caracteres')])
    hora = StringField(label='hora', validators=[DataRequired(), Length(min = 9 , max = 9,  message='Campo Capacidad Requerido:Escribir formato: HH:MM:SS.')])
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

class frmRegistro(FlaskForm):
   nombres=StringField(label='nombres',
      validators=[
         DataRequired(message='El campo de nombres no puede quedar vacío'),
         Length(min=3, max=120, message='El nombre no puede tener menos de 3 caracteres y más de 120')
      ]
   )

   apellidos=StringField(label='apellidos',
      validators=[
         DataRequired(message='El campo de apellidos no puede quedar vacío'),
         Length(min=3, max=120, message='El apellido no puede tener menos de 3 caracteres y más de 120')
      ]
   )
   CC ='Cédula de ciudadania'
   TI ='Tarjeta de identidad'
   PS = 'Pasaporte'
   
   tipoDocumento=SelectField(label='tipo doc',
      choices=[
         (CC),
         (TI),
         (PS)
         ], 
         validate_choice=True,
         validators=[DataRequired(message='El campo de tipo de documento no puede quedar vacío')]
         )
         
  
   numDocumento = StringField(label='número doc',
      validators=[
         DataRequired(message='El campo de número de documento no puede quedar vacío'),
         Length(min=8, max=70, message="La identificación introducida es muy larga o muy corta")
      ]
   )
   
   

   genero= SelectField(label="género",
      choices=[
         ('Masculino'),
         ('Femenino'),
         ('Prefiero no decirlo')
         ],
      validate_choice=True,
      validators=[
         DataRequired(message='El campo de genero no puede quedar vacío')
      ]
   )

   fechaNacimiento = DateField(label="Fecha nacimiento",
      
      validators=[DataRequired(message='El campo de fecha de nacimiento no puede quedar vacío')]
      )

   telefono=StringField(label="telefono",
      validators=[
         DataRequired(message='El campo de teléfono no puede quedar vacío'),
         Length(min=6,max=20, message='El número de teléfono es muy corto o muy largo')
      ]
   )
   correo = StringField(label="correo",
      validators=[DataRequired(message='El campo de correo no puede quedar vacío'),
      Email(message='El correo no es válido'),
      Length(min=8, max=120, message='El correo debe tener mínimo 8 caracteres y máximo 120')]
      )
   password = PasswordField(label='contraseña', 
      validators=[DataRequired(message='El campo de contraseña no puede quedar vacío'),
      Length(min=8, max=15, message='La contraseña debe tener mínimo 8 caracteres y máximo 15'),
      EqualTo('passwordConfirmar', message='Las contraseñas no coinciden')
      ]
   )
   passwordConfirmar = PasswordField(label="Confirmar contraseña")
   botonEnviar = SubmitField(label="REGISTRARSE")

class frmBuscarUsuario(FlaskForm):
   nombreUsuario = StringField(label="nombreUsuario", validators=[DataRequired(message ='Es necesario digitar el nombre del usuario'), Length (min=3, max=120, message ='El nombre debe contener por lo menos %(min)d caracter/es y máximo %(max)d')])
   botonEnviar = SubmitField(label='Consultar')

class frmCrearEditarUsuario(FlaskForm):
   nombres=StringField(label='nombres',
      validators=[
         DataRequired(message='El campo de nombres no puede quedar vacío'),
         Length(min=3, max=120, message='El nombre no puede tener menos de 3 caracteres y más de 120')
      ]
   )

   apellidos=StringField(label='apellidos',
      validators=[
         DataRequired(message='El campo de apellidos no puede quedar vacío'),
         Length(min=3, max=120, message='El apellido no puede tener menos de 3 caracteres y más de 120')
      ]
   )
   cedula ='Cédula de ciudadania'
   tarjetaId ='Tarjeta de identidad'
   pasaporte = 'Pasaporte'
   
   tipoDocumento=SelectField(label='tipo doc',
      choices=[
         (cedula),
         (tarjetaId),
         (pasaporte)
         ], 
         validate_choice=True,
         validators=[DataRequired(message='El campo de tipo de documento no puede quedar vacío')]
         )
         
  
   numDocumento = StringField(label='número doc',
      validators=[
         DataRequired(message='El campo de número de documento no puede quedar vacío'),
         Length(min=8, max=70, message="La identificación introducida es muy larga o muy corta")
      ]
   )
   
   

   genero= SelectField(label="género",
      choices=[
         ('Masculino'),
         ('Femenino'),
         ('Prefiero no decirlo')
         ],
      validate_choice=True,
      validators=[
         DataRequired(message='El campo de genero no puede quedar vacío')
      ]
   )
   rol= SelectField(label="rol",
      choices=[
         ('Pasajero'),
         ('Piloto'),
         ('Superadministrador')
         ],
      validate_choice=True,
      validators=[
         DataRequired(message='El campo de rol no puede quedar vacío')
      ]
   )

   fechaNacimiento = DateField(label="Fecha nacimiento",
      
      validators=[DataRequired(message='El campo de fecha de nacimiento no puede quedar vacío')]
      )

   telefono=StringField(label="telefono",
      validators=[
         DataRequired(message='El campo de teléfono no puede quedar vacío'),
         Length(min=6,max=20, message='El número de teléfono es muy corto o muy largo')
      ]
   )
   correo = StringField(label="correo",
      validators=[DataRequired(message='El campo de correo no puede quedar vacío'),
      Email(message='El correo no es válido'),
      Length(min=8, max=120, message='El correo debe tener mínimo 8 caracteres y máximo 120')]
      )
   
   botonEnviar = SubmitField(label="GUARDAR")

class frmConsVuelo(FlaskForm):
   consvuelo = StringField(label="consvuelo", validators=[DataRequired(message ='Es necesario digitar el codigo de vuelo'), Length (min=1, max=6, message ='el código debe contener por lo menos %(min)d caracter/es y máximo %(max)d')])
   botonEnviar = SubmitField(label='Consultar')