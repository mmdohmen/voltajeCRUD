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



# MODELOS (entidades) de la BBDD ***************************************************************************************************
# defino la/s TABLA/s 
class Producto(db.Model):                            # la CLASE Producto hereda de db.Model
    id = db.Column(db.Integer, primary_key=True)     # define los campos de la tabla
    nombre = db.Column(db.String(100))
    precio = db.Column(db.Integer)
    stock = db.Column(db.Integer)
    imagen = db.Column(db.String(450))
    def __init__(self,nombre,precio,stock,imagen):   # crea el CONSTRUCTOR de la clase
        self.nombre = nombre                         # no hace falta el id porque lo crea sola mysql por ser auto_incremento
        self.precio = precio
        self.stock = stock
        self.imagen = imagen
# si hay que crear mas tablas , se hace aqui

with app.app_context():
    db.create_all()       # aqui CREO todas las TABLAS



# CONTROLADORES ********************************************************************************************************************
#from controladores import *

class ProductoSchema(ma.Schema):
    class Meta:
        fields=('id','nombre','precio','stock','imagen')

producto_schema = ProductoSchema()             # El OBJETO producto_schema es para traer UN REGISTRO (producto)
productos_schema = ProductoSchema(many=True)   # El OBJETO productos_schema es para traer MULTIPLES REGISTROS (productos)



# creo los ENDPOINT o rutas (json) *************************************************************************************************
@app.route('/productos', methods=['GET'])
def get_Productos():
    all_productos = Producto.query.all()            # el metodo query.all() lo hereda de db.Model
    result = productos_schema.dump(all_productos)   # el metodo dump() lo hereda de ma.schema y trae todos los registros de la tabla
    return jsonify(result)                          # retorna un JSON de todos los registros de la tabla


@app.route('/productos/<id>', methods=['GET'])
def get_producto(id):
    producto = Producto.query.get(id)
    return producto_schema.jsonify(producto)        # retorna el JSON de un producto recibido como parametro


@app.route('/productos', methods=['POST'])                # CREAR un producto en la BBDD  
def create_producto():                       
    # print(request.json) 
    # # request.json contiene el JSON que envio el cliente
    nombre = request.json['nombre']                       # guardo los datos del JSON en variables                      
    precio = request.json['precio']
    stock = request.json['stock']
    imagen = request.json['imagen']
    new_producto = Producto(nombre,precio,stock,imagen)   # instancio un OBJETO con los datos recibidos en el JSON de la request
    db.session.add(new_producto)                          # agrego ese registro a la BBDD
    db.session.commit()                                   # CONFIRMO la operacion
    return producto_schema.jsonify(new_producto)


@app.route('/productos/<id>', methods=['PUT'])            # ACTUALIZAR un producto en la BBDD
def update_producto(id):
    producto = Producto.query.get(id)                     # RECUPERO el producto con el 'id' detallado en la URL
    producto.nombre = request.json['nombre']              # ACTUALIZO los datos de 'producto' con los datos del JSON recibido en la request
    producto.precio = request.json['precio']
    producto.stock = request.json['stock']
    producto.imagen = request.json['imagen']
    db.session.commit()                                   # CONFIRMO la operacion
    return producto_schema.jsonify(producto)


@app.route('/productos/<id>', methods=['DELETE'])
def delete_producto(id):
    producto = Producto.query.get(id)          # busco el PRODUCTO correspondiente al 'id' de la URL
    db.session.delete(producto)                # BORRO el PRODUCTO 
    db.session.commit()                        # CONFIRMO el request
    return producto_schema.jsonify(producto)   # me devuelve un JSON con el REGISTRO ELIMINADO



# programa principal **************************************************************************************************************
if __name__=='__main__':
    app.run(debug=True, port=5000)   # ejecuta el SERVIDOR Flask en el PUERTO 5000


