from jinja2 import Environment, FileSystemLoader
from flask import Flask, render_template, request, url_for, redirect, make_response
from flaskext.mysql import MySQL
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

      print(current_date)
 
      conn = mysql.connect()
      pointer = conn.cursor()

      pointer.execute('SELECT correo FROM maestros')
      emails = pointer.fetchall()

      for email in emails:
         if correo == email[0]:

            pointer.execute('SELECT id_tutor FROM maestros WHERE correo = %s', email[0])
            id_Tutor = pointer.fetchone()

            pointer.execute('SELECT password FROM maestros WHERE correo = %s', email[0])
            _getpass = pointer.fetchone()
            
            if pwd == _getpass[0]:
               flag = True
         else:
            pass
      
      if flag :

         pointer.execute('SELECT * FROM alumnos WHERE tutor = %s', id_Tutor[0])
         alumnos = pointer.fetchall()

         pointer.execute('SELECT id_tutor, nombre_tutor, apep_tutor, apem_tutor FROM maestros WHERE id_tutor = %s', id_Tutor[0])
         tutores = pointer.fetchall()

         return render_template('tutor_frame.html', tutelados = alumnos, tutores = tutores, date = current_date)
      else: 
         return 'Error de sesion. Vuelva a ingresar Datos'
      
   
@app.route('/main') #muestra de tutelados >> sera la primera vista una ves ingresadas las credeniales
def home():
   return render_template('tutor_frame.html')


@app.route('/print/', methods = ['GET'])
def print_report():
   conn = mysql.connect()
   pointer = conn.cursor()

   """
   Al parecer, algunos interpretes no reconocen el PATH, asi que se tiene que especificar la ruta para el modulo que convierte de HTML a PDF
   """
   path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
   config = pdfkit.configuration(wkhtmltopdf = path_wkhtmltopdf)

   IDT = request.args.get('id_tutor')
   current_date = request.args.get('report_date')
   nombre = request.args.get('tutor_name')
   paterno = request.args.get('tutor_apep')
   materno = request.args.get('tutor_apem')


   pointer.execute('SELECT * FROM alumnos WHERE tutor = %s', str(IDT))
   tutelados = pointer.fetchall()

   _getTemplate = render_template('return.html', tutelados = tutelados, current_date = current_date, nombre = nombre, paterno = paterno, materno = materno) 

   _responsestring = pdfkit.from_string(_getTemplate, False, configuration=config)

   response = make_response(_responsestring)

   response.headers['Content-Type'] = 'application/pdf'
   
   response.headers['Content-Disposition'] = 'inline;filename='+current_date+'_'+paterno+'.pdf'

   return response
   

@app.route('/about')
def about():
   return render_template('about_frame.html')

if __name__ == '__main__':
   app.run(debug=True, port = 3000)

