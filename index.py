from flask import Flask, render_template, request, url_for, redirect
from flaskext.mysql import MySQL 

app = Flask(__name__)

#mysql connection
app.config['MYSQL_DATABASE_USER'] = 'root' 
app.config['MYSQL_DATABASE_PASSWORD'] = 'password' 
app.config['MYSQL_DATABASE_DB'] = 'tutorias' 
app.config['MYSQL_DATABASE_HOST'] = 'localhost' 

#creando instacia de mysql
mysql = MySQL(app)

#ajustes
app.secret_key = 'mysecretkey'

@app.route('/') #formulario de inicio de sesion >> debe ser la inicial
def login():
   return render_template('home.html')

@app.route('/log_attempt', methods = ['POST'])
def logging():
   flag = False
   if request.method == 'POST':

      correo = request.form['correo']
      current_date = request.form['current_date']

      #correo = "('"+correo+"',)"
 
      conn = mysql.connect()
      pointer = conn.cursor()

      pointer.execute('SELECT correo FROM maestros')
      emails = pointer.fetchall()

      for email in emails:
         if correo == email[0]:
            pointer.execute('SELECT id_tutor FROM maestros WHERE correo = %s', email[0])
            id_Tutor = pointer.fetchone()
            print(id_Tutor)
            flag = True
         else:
            pass
      
      if flag :
         pointer.execute('SELECT * FROM alumnos WHERE tutor = %s', id_Tutor[0])
         alumnos = pointer.fetchall()
         pointer.execute('SELECT nombre_tutor, apep_tutor, apem_tutor FROM maestros WHERE id_tutor = %s', id_Tutor[0])
         tutores = pointer.fetchall()
         print (tutores)
         return render_template('tutor_frame.html', tutelados = alumnos, tutores = tutores)
      else: 
         return 'Error de sesion. Vuelva a ingresar Datos'
      
   
@app.route('/main') #muestra de tutelados >> sera la primera vista una ves ingresadas las credeniales
def home():
   return render_template('tutor_frame.html')


@app.route('/print')
def print_report():
   return 'Print function'

@app.route('/about')
def about():
   return render_template('about_frame.html')

if __name__ == '__main__':
   app.run(debug=True, port = 3000)

