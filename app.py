# BACKEND TP Integrador Final
# API que consulta a un SERVIDOR de BBDD

from flask import Flask ,jsonify ,request   # p/ crear APLICACIONES WEB
from flask_cors import CORS                 # configuracion y manejo de CABECERAS HTTP
from flask_sqlalchemy import SQLAlchemy     # biblioteca de MAPEO Objeto Relacional (ORM)
from flask_marshmallow import Marshmallow   # biblioteca de SERIALIZACION y Validacion de OBJETOS


app = Flask(__name__)   # crear el OBJETO app de la clase Flask
CORS(app)               # Clase CORS que permite acceder desde el frontend al backend


# configuro la BBDD
# con el nombre el usuario 'root', la contraseña 'root', el servidor 'localhost' y la BBDD 'cacpython'
#app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://usuario:contraseña@servidor/nombreBBDD
#                                                    //usuario:contraseña@servidor/nombreBBDD
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:root@localhost/cacpython'
# URI de la BBDD driver de la BD user:clave@URLBBDD/nombreBBDD
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False   #none

db = SQLAlchemy(app)                                   #crea el OBJETO 'db' de la clase SQLAlquemy
ma = Marshmallow(app)                                  #crea el OBJETO 'ma' de de la clase Marshmallow



# CONTROLADORES ********************************************************************************************************************
from controladores import *



# programa principal **************************************************************************************************************
if __name__=='__main__':
    app.run(debug=True, port=5000)   # ejecuta el SERVIDOR Flask en el PUERTO 5000


