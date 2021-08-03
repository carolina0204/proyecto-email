from flask import Flask,render_template,request,redirect,url_for
from flask_bootstrap import Bootstrap
from flask import Flask
from flask_mysqldb import MySQL

from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)

app.config['MYSQL_HOST']= 'localhost'
app.config['MYSQL_USER']= 'root'
app.config['MYSQL_PASSWORD']= ''
app.config['MYSQL_DB']= 'prueba'

mysql = MySQL(app)
app.secret_key = "mysecretkey"

Bootstrap(app)

lstProductos=['LAPTOP','MONITOR','MONITORES']

class frmProducto(FlaskForm):
    categoria = StringField('categoria :' , validators=[DataRequired()])
    nombre = StringField('Nombre :' , validators=[DataRequired()])
    marca = StringField('Marca :' , validators=[DataRequired()])
    modelo = StringField('Modelo :' , validators=[DataRequired()])
    serie = StringField('Nro Serie :' , validators=[DataRequired()])
    ram = StringField('Memoria RAM :' , validators=[DataRequired()])
    procesador = StringField('Procesador :' , validators=[DataRequired()])
    discoduro = StringField('Disco Duro :' , validators=[DataRequired()])
    precio = StringField('Precio :' , validators=[DataRequired()])
    stock = StringField('Stock :' , validators=[DataRequired()])
    submit = SubmitField('Registrar Nuevo Producto')



@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('select nombre,apellido,email,cargo from usuario')
    data = cur.fetchall()
    cur.close()

    print(data)
    context2 ={
        'data':data
    }

 
    """context = {
        'nombre':name,
        'user_ip':user_ip,
        'productos':lstProductos
    }"""
    return render_template('index.html',**context2)

@app.route('/productos', methods=['GET','POST'])

def productos():
    
    cur1 = mysql.connection.cursor()
    cur1.execute('select * from cat_producto')
    datacategoria = cur1.fetchall()
    cur1.close()

    if request.method == 'POST' :
        catId = request.form['categoria']
        sqlProducto = "SELECT * FROM producto where cat_producto_id="+catId
    else:
        sqlProducto = "SELECT * FROM producto"

    cur2 = mysql.connection.cursor()
    cur2.execute(sqlProducto)
    dataproducto = cur2.fetchall()
    cur2.close()

    frmNuevoProducto = frmProducto()
    
    context2 ={
        'datacategoria':datacategoria,
        'dataproducto':dataproducto,
        'frmProducto':frmNuevoProducto
    }

    if frmNuevoProducto.validate_on_submit():
        categoria1 = frmNuevoProducto.categoria.data
        nombre = frmNuevoProducto.nombre.data
        marca = frmNuevoProducto.marca.data
        modelo = frmNuevoProducto.modelo.data
        serie = frmNuevoProducto.serie.data
        ram = frmNuevoProducto.ram.data
        procesador = frmNuevoProducto.procesador.data
        discoduro = frmNuevoProducto.discoduro.data
        precio = frmNuevoProducto.precio.data
        stock = frmNuevoProducto.stock.data

        cursornuevoproducto = mysql.connection.cursor()
        cursornuevoproducto.execute("INSERT INTO PRODUCTO(cat_producto_id,nombre,marca,modelo,nro_serie,mem_ram,procesador,disco_duro,precio,stock) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(categoria1,nombre,marca,modelo,serie,ram,procesador,discoduro,precio,stock))
        mysql.connection.commit()

if __name__ == '__main__':
    app.run(debug=True,port=5000)
