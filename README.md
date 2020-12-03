# reportes_tutoria
Proyecto Final de Sistemas Virtuales


<---Base de Datos--->

Ingrese el archivo sql necesario para crear la BD y tambien sus tablas. 
Sus relaciones y atributos.
Y las tuplas de cada una.

>>> ../BDD/127_0_0_1_tutorias.sql

<---Estilos--->

Se conforma de dos hojas de estilos.

Una es para la plantilla general del archivo.
>>>../static/css/main7.css

Y la otra, es para el formulario de inicio de sesion.
>>>../static/css/main7.css

#NOTA: No modifiquen las carpetas de estilos. Ya que el interprete de Python, lee exactamente esa ruta por Default.

<---Templates HTML--->

Se almacenan los archivos html para la creacion del sitio dinamico.
>>>../templates/*.html

<---Python (backend)--->

Comprende el archivo con todos los metodos, llamadas a templates y conexiones para la operabilidad del sitio. Es el núcleo.
>>>../index.py

<--Python classes-->
Comprende la clase generadora de PDF. Cada instancia de ella, realiza una impresion de PDF.
>>>../PDF.py