from flask import Flask,render_template,request,redirect,url_for
from flask_bootstrap import Bootstrap
from flask import Flask
from flask_mysqldb import MySQL

from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField
from wtforms.validators import DataRequired
from flask import Blueprint


app = Flask(__name__)
mod = Blueprint('users', __name__)

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

class frmEmail(FlaskForm):
    to = StringField('To :' , validators=[DataRequired()])
    subject = StringField('Subject :' , validators=[DataRequired()])
    body = TextAreaField('Body :' , validators=[DataRequired()])
    submit = SubmitField('Enviar email')


@app.route('/', methods=['GET','POST'])
def index():
    
    cur = mysql.connection.cursor()
    cur.execute('SELECT nombre,apellido,email,cargo FROM usuario')
    data = cur.fetchall()
    cur.close()

    if request.method == 'POST' :
        cargoId = request.form['cargo']
        sqlProducto = "SELECT id,nombre,apellido,email,cargo FROM usuario where cargo like '%"+cargoId+"%'"
    else:
        sqlProducto = "SELECT id,nombre,apellido,email,cargo FROM usuario"
    
    cur2 = mysql.connection.cursor()
    cur2.execute(sqlProducto)
    data = cur2.fetchall()
    cur2.close()
    
    context2 ={
        'data': data
    }   
    """context = {
        'nombre':name,
        'user_ip':user_ip,
        'productos':lstProductos
    }"""
    return render_template('index.html',**context2)

@app.route('/eliminar', methods=['POST'])
def eliminar():
    id = request.form['eid']
    curEliminarProducto = mysql.connection.cursor()
    curEliminarProducto.execute("DELETE FROM usuario WHERE id=%s",(id))
    mysql.connection.commit()
    curEliminarProducto.close()
    
    return redirect(url_for('index'))

@app.route('/email', methods=['GET','POST'])
def email():
    
 
    '''     
    id = request.form['eid']
    cur1 = mysql.connection.cursor()
    cur1.execute('SELECT id,nombre,apellido,email,cargo FROM usuario WHERE id=%s',(id))
    data = cur1.fetchall()
    cur1.close() '''
    
    if request.method == 'POST' :
        id = request.form['eid']
        print(id)
        '''    sqlEmail = ("SELECT * FROM usuario where id=''",(id)) '''
        sqlEmail = ("SELECT id,nombre,apellido,email FROM usuario where id="+id)
        print('ENTROOOOOOOOOOOOOOOO AQUIIIIIIIIIIIIIIIII')
    
    cur2 = mysql.connection.cursor()
    cur2.execute(sqlEmail)
    data = cur2.fetchall()
    cur2.close()
    
    
    frmEmail1 = frmEmail()
    
    context ={
        'data':data,
        'id':id,
        'frmEmail':frmEmail1
    }
    
    if frmEmail1.validate_on_submit():
        to = frmEmail1.email.data
        subject = frmEmail1.nombre.data
        body = frmEmail1.nombre.data
        
        print(frmEmail1)
        
        return redirect(url_for('index'))
            
    return render_template('email.html',**context) 


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
