from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField ,BooleanField, \
    SubmitField
from wtforms.fields.core import DateField, DateTimeField, IntegerField, SelectField
from wtforms.validators import ValidationError, DataRequired, \
    Email, EqualTo, Length
import json

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

class frmCrearEditarVuelo(FlaskForm):
   origenVuelo = StringField(label='ciudadOrigen', validators=[DataRequired(), Length(min = 3, max = 50, message='Campo Ciudad Origen Requerido:Mínimo 2 y máximo 50 caracteres.')])
   destinoVuelo = StringField(label='ciudadDestino', validators=[DataRequired(), Length(min = 3, max = 50, message='Campo Ciudad Origen Requerido:Mínimo 2 y máximo 50 caracteres.')])
   avion = StringField(label='avion', validators=[DataRequired(), Length(min = 5, max = 30,  message='Campo Avión Requerido:Mínimo 5 y máximo 30 caracteres.')])
   capacidad = StringField(label='capacidad', validators=[DataRequired(), Length(min = 1, max = 3, message='Campo Capacidad Requerido:Mínimo 1 y máximo 3 caracteres')])
   estadoVuelo= SelectField(label="estadoVuelo",
   choices=[
      ('Inactivo'),
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
   
   idPiloto = StringField(label='idPiloto')
   idcoPiloto = StringField(label='idCo-Piloto')
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

class frmUsuario(FlaskForm):
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
         Length(min=8, max=70, message="La identificación introducida es muy larga o muy corta")
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

   telefono=StringField(label="telefono",
      validators=[
         DataRequired(message='El campo de teléfono no puede quedar vacío'),
         Length(min=6,max=20, message='El número de teléfono es muy corto o muy largo')
      ]
   )

   genero= SelectField(label="Genero:",
      choices=[('Prefiero no decirlo'), ('Masculino'), ('Femenino')], validate_choice=True,validators=[DataRequired(message="Debe escoger un género.")]
   )

   fechaNacimiento = DateField(label="Fecha nacimiento",
      
      validators=[DataRequired(message='El campo de fecha de nacimiento no puede quedar vacío')]
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

class frmCrearUsuario(FlaskForm):
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

   CC = 'CC'
   TI = 'TI'
   PS = 'PS' 

   tipoDocumento=StringField(label='tipo doc',
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

   pais = SelectField(label="pais",
      choices=[
         ('Afganistan'),
         ('Albania'),
         ('Alemania'),
         ('Andorra'),
         ('Angola'),
         ('Anguila'),
         ('Antártida'),
         ('Antigua y Barbuda'),
         ('Antillas holandesas'),
         ('Arabia Saudí'),
         ('Argelia'),
         ('Argentina'),
         ('Armenia'),
         ('Aruba'),
         ('Australia'),
         ('Austria'),
         ('Azerbaiyán'),
         ('Bahamas'),
         ('Bahrein'),
         ('Bangladesh'),
         ('Barbados'),
         ('Bélgica'),
         ('Belice'),
         ('Benín'),
         ('Bermudas'),
         ('Bhután'),
         ('Bielorrusia'),
         ('Birmania'),
         ('Bolivia'),
         ('Bosnia y Herzegovina'),
         ('Botsuana'),
         ('Brasil'),
         ('Brunei'),
         ('Bulgaria'),
         ('Burkina Faso'),
         ('Burundi'),
         ('Cabo Verde'),
         ('Camboya'),
         ('Camerún'),
         ('Canadá'),
         ('Chad'),
         ('Chile'),
         ('China'),
         ('Chipre'),
         ('Ciudad estado del Vaticano'),
         ('Colombia'),
         ('Comores'),
         ('Congo'),
         ('Corea'),
         ('Corea del Norte'),
         ('Costa del Marfíl'),
         ('Costa Rica'),
         ('Croacia'),
         ('Cuba'),
         ('Dinamarca'),
         ('Djibouri'),
         ('Dominica'),
         ('Ecuador'),
         ('Egipto'),
         ('El Salvador'),
         ('Emiratos Arabes Unidos'),
         ('Eritrea'),
         ('Eslovaquia'),
         ('Eslovenia'),
         ('España'),
         ('Estados Unidos'),
         ('Estonia'),
         ('Etiopi'),
         ('Ex-República Yugoslava de Macedonia'),
         ('Filipinas'),
         ('Finlandia'),
         ('Francia'),
         ('Gabón'),
         ('Gambia'),
         ('Georgia'),
         ('Georgia del Sur y las islas Sandwich del Sur'),
         ('Ghana'),
         ('Gibraltar'),
         ('Granada'),
         ('Grecia'),
         ('Groenlandia'),
         ('Guadalupe'),
         ('Guam'),
         ('Guatemala'),
         ('Guayana'),
         ('Guayana francesa'),
         ('Guinea'),
         ('Guinea Ecuatorial'),
         ('Guinea-Bissau'),
         ('Haití'),
         ('Holanda'),
         ('Honduras'),
         ('Hong Kong R. A. E'),
         ('Hungría'),
         ('India'),
         ('Indonesia'),
         ('Irak'),
         ('Irán'),
         ('Irlanda'),
         ('Isla Bouvet'),
         ('Isla Christmas'),
         ('Isla Heard e Islas McDonald'),
         ('Islandia'),
         ('Islas Caimán'),
         ('Islas Cook'),
         ('Islas de Cocos o Keeling'),
         ('Islas Faroe'),
         ('Islas Fiyi'),
         ('Islas Malvinas Islas Falkland'),
         ('Islas Marianas del norte'),
         ('Islas Marshall'),
         ('Islas menores de Estados Unidos'),
         ('Islas Palau'),
         ('Islas Salomón'),
         ('Islas Tokelau'),
         ('Islas Turks y Caicos'),
         ('Islas Vírgenes EE.UU.'),
         ('Islas Vírgenes Reino Unido'),
         ('Israel'),
         ('Italia'),
         ('Jamaica'),
         ('Japón'),
         ('Jordania'),
         ('Kazajistán'),
         ('Kenia'),
         ('Kirguizistán'),
         ('Kiribati'),
         ('Kuwait'),
         ('Laos'),
         ('Lesoto'),
         ('Letonia'),
         ('Líbano'),
         ('Liberia'),
         ('Libia'),
         ('Liechtenstein'),
         ('Lituania'),
         ('Luxemburgo'),
         ('Macao R. A. E'),
         ('Madagascar'),
         ('Malasia'),
         ('Malawi'),
         ('Maldivas'),
         ('Malí'),
         ('Malta'),
         ('Marruecos'),
         ('Martinica'),
         ('Mauricio'),
         ('Mauritania'),
         ('Mayotte'),
         ('México'),
         ('Micronesia'),
         ('Moldavia'),
         ('Mónaco'),
         ('Mongolia'),
         ('Montserrat'),
         ('Mozambique'),
         ('Namibia'),
         ('Nauru'),
         ('Nepal'),
         ('Nicaragua'),
         ('Níger'),
         ('Nigeria'),
         ('Niue'),
         ('Norfolk'),
         ('Noruega'),
         ('Nueva Caledonia'),
         ('Nueva Zelanda'),
         ('Omán'),
         ('Panamá'),
         ('Papua Nueva Guinea'),
         ('Paquistán'),
         ('Paraguay'),
         ('Perú'),
         ('Pitcairn'),
         ('Polinesia francesa'),
         ('Polonia'),
         ('Portugal'),
         ('Puerto Rico'),
         ('Qatar'),
         ('Reino Unido'),
         ('República Centroafricana'),
         ('República Checa'),
         ('República de Sudáfrica'),
         ('República Democrática del Congo Zaire'),
         ('República Dominicana'),
         ('Reunión'),
         ('Ruanda'),
         ('Rumania'),
         ('Rusia'),
         ('Samoa'),
         ('Samoa occidental'),
         ('San Kitts y Nevis'),
         ('San Marino'),
         ('San Pierre y Miquelon'),
         ('San Vicente e Islas Granadinas'),
         ('Santa Helena'),
         ('Santa Lucía'),
         ('Santo Tomé y Príncipe'),
         ('Senegal'),
         ('Serbia y Montenegro'),
         ('Sychelles'),
         ('Sierra Leona'),
         ('Singapur'),
         ('Siria'),
         ('Somalia'),
         ('Sri Lanka'),
         ('Suazilandia'),
         ('Sudán'),
         ('Suecia'),
         ('Suiza'),
         ('Surinam'),
         ('Svalbard'),
         ('Tailandia'),
         ('Taiwán'),
         ('Tanzania'),
         ('Tayikistán'), 
         ('Territorios británicos del océano Indico'),
         ('Territorios franceses del sur'),
         ('Timor Oriental'),
         ('Togo'),
         ('Tonga'),
         ('Trinidad y Tobago'),
         ('Túnez'),
         ('Turkmenistán'),
         ('Turquía'),
         ('Tuvalu'),
         ('Ucrania'),
         ('Uganda'),
         ('Uruguay'),
         ('Uzbekistán'),
         ('Vanuatu'),
         ('Venezuela'),
         ('Vietnam'),
         ('Wallis y Futuna'),
         ('Yemen'),
         ('Zambia'),
         ('Zimbabue')
      ]
   )

   rol= StringField(label="rol",
      choices=[
         ('1'),
         ('2'),
         ('3')
      ],
      validators=[
         DataRequired(message='El campo de rol no puede quedar vacío')]
   )

   botonEnviar = SubmitField(label="GUARDAR")
