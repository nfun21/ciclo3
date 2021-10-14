from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField ,BooleanField, \
    SubmitField
from wtforms.fields.core import DateField, IntegerField, SelectField
from wtforms.validators import ValidationError, DataRequired, \
    Email, EqualTo, Length

class Ingreso(FlaskForm):
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

class Registro(FlaskForm):
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

class BuscarUsuario(FlaskForm):
   nombreUsuario = StringField(label="nombreUsuario", validators=[DataRequired(message ='Es necesario digitar el nombre del usuario'), Length (min=3, max=120, message ='El nombre debe contener por lo menos %(min)d caracter/es y máximo %(max)d')])
   botonEnviar = SubmitField(label='Consultar')

class CrearEditarUsuario(FlaskForm):
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