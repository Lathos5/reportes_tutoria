from jinja2 import Environment, FileSystemLoader
from flask import Flask, render_template, request, url_for, redirect
from flaskext.mysql import MySQL
from PDF import reportePDF, numeracionPaginas
import os
import pdfkit 

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
      pwd = request.form['pwd']
 
      conn = mysql.connect()
      pointer = conn.cursor()

      pointer.execute('SELECT correo FROM maestros')
      emails = pointer.fetchall()

      for email in emails:
         if correo == email[0]:

            pointer.execute('SELECT id_tutor FROM maestros WHERE correo = %s and password = %s', email[0], pwd)
            id_Tutor = pointer.fetchone()
            
            flag = True
         else:
            pass
      
      if flag :

         pointer.execute('SELECT * FROM alumnos WHERE tutor = %s', id_Tutor[0])
         alumnos = pointer.fetchall()

         pointer.execute('SELECT id_tutor, nombre_tutor, apep_tutor, apem_tutor FROM maestros WHERE id_tutor = %s', id_Tutor[0])
         tutores = pointer.fetchall()

         return render_template('tutor_frame.html', tutelados = alumnos, tutores = tutores)
      else: 
         return 'Error de sesion. Vuelva a ingresar Datos'
      
   
@app.route('/main') #muestra de tutelados >> sera la primera vista una ves ingresadas las credeniales
def home():
   return render_template('tutor_frame.html')


@app.route('/print/', methods = ['GET'])
def print_report():
   conn = mysql.connect()
   pointer = conn.cursor()

   IDT = request.args.get('id_tutor')

   print (IDT)

   pointer.execute('SELECT * FROM alumnos WHERE tutor = %s', str(IDT))
   tutelados = pointer.fetchall()

   atributes = {'Numero', 'Nombre', 'Carrera', 'Semestre', 'Grupo', 'Bachillerato', 'Reprobadas', 'Firma', 'Fecha', 'Horario'}

   return render_template('return.html') 
 
   

@app.route('/about')
def about():
   return render_template('about_frame.html')

if __name__ == '__main__':
   app.run(debug=True, port = 3000)

