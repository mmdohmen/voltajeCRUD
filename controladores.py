from flask import Flask, jsonify, request
from app import app, ma
from modelos import *



# defino los REGISTROS de la TABLA Productos
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

