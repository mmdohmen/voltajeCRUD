from app import db, app


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


