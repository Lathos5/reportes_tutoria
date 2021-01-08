from PDF import reportePDF, numeracionPaginas

def generarReporte(query_tutelados):
        
   def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

   titulo = "LISTADO DE TUTELADOS"

   cabecera = (
      ("fullname_alumno", "Nombre"),
      ("carrera", "Carrera"),
      ("semestre", "Semestre"),
      ("grupo", "Grupo"),
      ("promedio_bach", "Promedio Bachillerato"),
      ("materias_reprobadas", "Materias Reprobadas"),
      ("firma_estudiante", "Firma"),
      ("fecha", "Fecha"),
      ("horario", "Horario")
      )

   nombrePDF = "Tutelados_fecha.pdf"

   reporte = reportePDF(titulo, cabecera, query_tutelados, nombrePDF).Exportar()

   print(reporte)