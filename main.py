import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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

class frmEmail(FlaskForm):
    to = StringField('To :' , validators=[DataRequired()])
    subject = StringField('Subject :' , validators=[DataRequired()])
    body = TextAreaField('Body :' , validators=[DataRequired()])
    submit = SubmitField('Enviar email')

def enviar_correo(to,subject,body):
    mail_content = body
    #The mail addresses and password
    sender_address = 'binareon.developer@gmail.com'
    sender_pass = '&JJdymr$L5yg'
    receiver_address = to
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = subject   #The subject line
    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.ehlo()
    session.starttls() #enable security
    session.ehlo()
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sentdfdsffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff')

    return redirect(url_for('email'))

@app.route('/', methods=['GET','POST'])
def index():
    
    cur = mysql.connection.cursor()
    cur.execute('SELECT nombre,apellido,email,cargo FROM usuario LIMIT 10')
    data = cur.fetchall()
    cur.close()

    if request.method == 'POST' :
        cargoId = request.form['cargo']
        sqlProducto = "SELECT id,nombre,apellido,email,cargo FROM usuario where cargo like '%"+cargoId+"%'"
    else:
        sqlProducto = "SELECT id,nombre,apellido,email,cargo FROM usuario LIMIT 10"
    
    cur2 = mysql.connection.cursor()
    cur2.execute(sqlProducto)
    data = cur2.fetchall()
    cur2.close()
    
    context2 ={
        'data': data
    }   
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
    
    frmEmail1 = frmEmail()
    
    if frmEmail1.validate_on_submit():
        enviar_correo(frmEmail1.to.data,frmEmail1.subject.data,frmEmail1.body.data)
    else:
        if request.method == 'POST':
            id = request.form['eid']
            print(id)
            sqlEmail = ("SELECT nombre,apellido,email FROM usuario where id="+id)
        
        cursorEmail = mysql.connection.cursor()
        cursorEmail.execute(sqlEmail)
        data = cursorEmail.fetchone()
        cursorEmail.close()
        
        frmEmail1.to.data = data[2]
        frmEmail1.subject.data = "Envio de correo personal"
        frmEmail1.body.data = "Hola sr@ "+ data[0] + " " + data[1] + "Somos una empresa de software"

    context ={'frmEmail':frmEmail1}
       
    return render_template('email.html',**context) 

if __name__ == '__main__':
    app.run(debug=True,port=5000)
