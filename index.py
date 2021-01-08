from jinja2 import Environment, FileSystemLoader
from flask import Flask, render_template, request, url_for, redirect, make_response, session
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

@app.before_request
def session_management():
   session.permanent = True

@app.route('/') #formulario de inicio de sesion >> debe ser la inicial
def login():
   return render_template('home.html')

@app.route('/log_attempt', methods = ['POST'])
def loggin():

   session.clear()

   flag = False
   if request.method == 'POST':

      correo = request.form['correo']
      current_date = request.form['current_date']
      pwd = request.form['pwd']

      session['date'] = current_date


      conn = mysql.connect()
      pointer = conn.cursor()

      pointer.execute('SELECT correo FROM maestros')
      emails = pointer.fetchall()

      for email in emails:
         if correo == email[0]:

            pointer.execute('SELECT id_tutor FROM maestros WHERE correo = %s', email[0])
            id_Tutor = pointer.fetchone()

            session["auth"] = id_Tutor

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

         for tutor in tutores:
            session['user'] = correo        

         return render_template('tutor_frame.html', tutelados = alumnos, tutores = tutores, date = current_date)
      else: 
         return 'Error de sesion. Vuelva a ingresar Datos'
      
   
@app.route('/main') #muestra de tutelados >> sera la primera vista una ves ingresadas las credeniales
def home():
   try:
      user = session['user']
      auth = session['auth']
      current_date = session['date']
   except:
      user = "Unknown"
      auth = 0
      current_date = None

   if auth == 0:
      return 'Fallo en la sesion'
   else:
      conn = mysql.connect()
      pointer = conn.cursor()

      pointer.execute('SELECT * FROM alumnos WHERE tutor = %s', auth)
      alumnos = pointer.fetchall()

      pointer.execute('SELECT id_tutor, nombre_tutor, apep_tutor, apem_tutor FROM maestros WHERE id_tutor = %s', auth)
      tutores = pointer.fetchall()
      
      return render_template('tutor_frame.html', tutelados = alumnos, tutores = tutores, date = current_date)


@app.route('/new')
def _new():
   carreras = ['ITI','LAG','LMKT','ISTI','ITMA','ITEM']
   semestres = ['PRIMER','SEGUNDO','TERCER','CUARTO','QUINTO','SEXTO','SÉPTIMO','OCTAVO','NOVENO']
   grupos = ['UPSLP1', 'UPSLP2', 'UPSLP3', 'UPSLP4', 'UPSLP5', 'UPSLP6', 'T-800', 'T-300']
   return render_template('nuevo_reg.html', carreras = carreras, semestres = semestres, grupos = grupos)


@app.route('/insert', methods=['POST'])
def _insert():
   if request.method == 'POST':

      tutelado = request.form['nombre']
      carrera = request.form['carrera_select']
      semestre = request.form['semestre_select']
      grupo = request.form['grupo_select']
      bachillerato = request.form['promedio']
      reprobadas = str(request.form['reprobadas'])
      firma = request.form['firma']
      fecha = request.form['fecha_tutoria']
      hora = request.form['hora_tutoria']

      try:
         user = session['user']
         auth = session['auth']
         current_date = session['date']
      except:
         user = "Unknown"
         auth = 0
         current_date = None

      if auth == 0:

         return 'Error. Sesion Fallida'
      
      else:

         conn = mysql.connect()
         pointer = conn.cursor()

         pointer.execute('SELECT * FROM alumnos WHERE tutor = %s', auth)
         alumnos = pointer.fetchall()

         pointer.execute('SELECT id_tutor, nombre_tutor, apep_tutor, apem_tutor FROM maestros WHERE id_tutor = %s', auth)
         tutores = pointer.fetchall()

         pointer.execute('INSERT INTO alumnos (fullname_alumno, carrera, semestre, grupo, promedio_bach, materias_reprobadas, firma_estudiante, fecha, horario, tutor) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',( tutelado, carrera, semestre, grupo, bachillerato, reprobadas, firma, fecha, hora, auth))
         conn.commit()
  

   return render_template('tutor_frame.html', tutelados = alumnos, tutores = tutores, date = current_date)


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
   try:
      user = session['user']
      auth = session['auth']
      current_date = session['date']
   except:
      user = "Unknown"
      auth = 0
      current_date = None

   if auth == 0:
      return 'Fallo en la sesion'
   else:
      
      return render_template('about_frame.html')

if __name__ == '__main__':
   app.run(debug=True, port = 3000)

