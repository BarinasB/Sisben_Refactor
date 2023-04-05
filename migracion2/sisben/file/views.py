from django.shortcuts import render  
from django.http import HttpResponse
import MySQLdb
from MySQLdb import _mysql 
import datetime
from xlwt import *
import codecs
import csv
from .forms import UploadFileForm

def genfiles(request): 

    db=_mysql.connect(host="192.168.0.6",
                      user="root",
                      password="",
                      database="sisben_migracion") 
    
    vcon = str(db.get_host_info())
    print("Conectado a la BD:", vcon)

    if request.method=='POST':
        formUpFile = UploadFileForm(request.POST, request.FILES)
        if formUpFile.is_valid():
            RegFile=handle_uploaded_file(request.FILES['file'])      
            print ("Cantidad de registros: "+str(RegFile)) 

        load_files(db)                    
        #write_excelfile(db)
        #write_csvfile(db)
        #Genefile=write_csvfile(db)
        Genefile = 1
        db.close()
        
        return render(request, 'FileformUpload.html', {'formUpFile': formUpFile,'nombFile':Genefile,'regFile':RegFile})
    else:
        formUpFile = UploadFileForm()
        namefile = "No seleccionado"
        return render(request, 'FileformUpload.html', {'filePath': namefile,'formUpFile': formUpFile})   


def handle_uploaded_file(f):

    archivo="C:/Users/USER/Desktop/Recaudo Bogota/sisben/migracion2/FiletoRead.csv"
    with open(archivo, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
	
    destination.close()
    doc = open(archivo)
    contador = str(len(doc.readlines ())) 
    
    return (contador)


def load_files(db):
    print ('Proceso Cargue BD inicio '+str(datetime.datetime.now()))

    print ("1 Insertando de datos en la BD tabla tmp_consultaspersonasisben") 

    query_str="""LOAD DATA INFILE 'C:/Users/USER/Desktop/Recaudo Bogota/sisben/migracion2/FiletoRead.csv'
    INTO TABLE `tmp_consulta_personasisben` FIELDS TERMINATED BY ';' 
    IGNORE 1 LINES
    ( ficha,
    tipodocumento_id,
    documen,
    ape1,
    ape2,
    nom1,
    nom2,
    sexo,
    tiponovedad_id,
    placa,
    @fechanto,
    edad,
    nombarrio,
    Direccion,
    Telefono,
    comuna) SET fechanto = str_to_date(@fechanto, '%d/%m/%Y' );"""  
    
    db.query(query_str)
    print ("2 Proceso de cargar realizado satisfactoriamente ") 

    print ("3 Cantidad de registros cargados: "+ str(db.affected_rows())) 



    query_str="""DELETE from tmp_consulta_personasisben where tipodocumento_id=0;""" 
     
    db.query(query_str)

    print ("4 borrados registros con tipodocumento_id=0:  "+ str(db.affected_rows()))


    query_str="""delete from tmp_consulta_personasisben where documen="0"; """

    db.query(query_str)

    print ("5 borrados registros con documen=0  :"+ str(db.affected_rows()))

    query_str="""delete from tmp_consulta_personasisben where documen=""; """

    db.query(query_str)

    print ("6 borrados registros con  documen=''  :"+ str(db.affected_rows()))

    query_str="""drop table eliminar;""" 

    db.query(query_str)

    print ("7 borrar tabla eliminar")

    query_str="""create table eliminar as SELECT documen, tipodocumento_id
     FROM tmp_consulta_personasisben GROUP BY documen, tipodocumento_id HAVING COUNT(*) > 1;"""  

    db.query(query_str) 

    print ("8 Crear tabla eliminar se pobla con los registros repetidos de la tabla tmp_consulta_personasisben: "+ str(db.affected_rows()))

    query_str="""alter table eliminar add index (tipodocumento_id,documen);  """
    
    db.query(query_str) 

    print ("9 creacion del index"+ str(db.affected_rows()))

    #query_str=""" delete from tmp_consulta_personasisben
    #     where exists ( select 1 from eliminar a where
    #     a.tipodocumento_id  = tmp_consulta_personasisben.tipodocumento_id
    #     and a.documen  =  tmp_consulta_personasisben.documen);""" 
    
    db.query(query_str) 

    print ("10 eliminacion de registros repetidos:  "+ str(db.affected_rows()))


    query_str="""update
        tmp_consulta_personasisben a,
        consulta_personasisben b
        set
        a.id=b.id
        where a.tipodocumento_id=b.tipodocumento_id
        and a.documen =b.documen;"""
     
    db.query(query_str)  

    print ("11 actualizando el id de los registros :"+ str(db.affected_rows())) 

    
    # query_str="""select count(distinct(tiponovedad_id)) from consulta_personasisben; """

    # db.query(query_str)  

    # print(" consulta diferente tipo de documento debe haber unicamente 4 y null"+  str(db.affected_rows()) )


    # query_str="""select distinct(tiponovedad_id) from tmp_consulta_personasisben;""" 

    # db.query(query_str)

    # print(" consulta diferente tipo de docomento en la tabla temporal debe ser 0",str(query_str))

    # query_str="""select count(*) from tmp_consulta_personasisben where tiponovedad_id=0;"""

    # db.query(query_str)

    # print(" consulta cantidad de registros con tiponovedad_id=0",str(query_str))

    query_str=""" update  tmp_consulta_personasisben set tiponovedad_id = null where tiponovedad_id = 0;"""

    db.query(query_str) 

    print("12 enviando null a la tabla tmp_consulta_personasisben cunado tiponovedad_id = 0:  "+ str(db.affected_rows()))

    # query_str=""" select count(*) from __tmp_consulta_personasisben where id is null; """

    # db.query(query_str)

    # print(" revisando cuantos registros de la tabla quedaron con id novedad null")

    # query_str="""select count(*) from consulta_personasisben;""" 

    # db.query(query_str)
     
    # print(" tabla permanente antes de la insercion", str(query_str))

    query_str=""" insert into 
    consulta_personasisben 
    select 
        primak,null,ficha,documen,ape1,ape2,nom1,nom2,sexo,placa,fechanto,edad,nombarrio,Direccion,Telefono,comuna,tipodocumento_id,tiponovedad_id
 
    from 
        tmp_consulta_personasisben 
    where
        id is null;"""
     
    db.query(query_str)

    print("13 insertados registros en la tabla permanente consulta_personasisben: "+ str(db.affected_rows()))

    # query_str="""select count(*) from consulta_personasisben;"""

    # db.query(query_str)

    # print("22 nueva cantidad de registros en la tabla consulta_personasisben ",str(query_str))

### revision 
    query_str=""" UPDATE
     consulta_personasisben cp, tmp_consulta_personasisben tcp SET
     cp.ficha=tcp.ficha
     #,cp.fecharegsdm=tcp.fecharegsdm
     ,cp.tipodocumento_id=tcp.tipodocumento_id
     ,cp.documen=tcp.documen
     ,cp.ape1=tcp.ape1
     ,cp.ape2=tcp.ape2
     ,cp.nom1=tcp.nom1
     ,cp.nom2=tcp.nom2
     ,cp.sexo=tcp.sexo
     ,cp.placa=tcp.placa
     ,cp.edad=tcp.edad
     ,cp.fechanto=tcp.fechanto
     #,cp.nombarrio=tcp.nombarrio
     ,cp.Direccion=tcp.Direccion
     ,cp.Telefono=tcp.Telefono
     ,cp.tiponovedad_id = tcp.tiponovedad_id
     ,cp.comuna=tcp.comuna
     WHERE 
     tcp.tipodocumento_id=cp.tipodocumento_id AND
     tcp.documen = cp.documen;"""
     
    db.query(query_str)

    print("14 actualizando valores en datos entre la tabla temporal y permanente: "+ str(db.affected_rows()))

    ## prueba index
    # query_str="""alter table tmp_consulta_personasisben add index (tipodocumento_id,documen);  """ 

    # db.query(query_str) 

    # print ("index de tmp")

    # query_str="""alter table consulta_personasisben add index (tipodocumento_id,documen);  """ 

    # db.query(query_str) 

    # print ("index de per")

    query_str="""UPDATE consulta_personasisben cp SET
    cp.tiponovedad_id=4
    where
        NOT EXISTS(
            SELECT 1 
            FROM tmp_consulta_personasisben tcp
            WHERE
                tcp.tipodocumento_id=cp.tipodocumento_id AND
                tcp.documen = cp.documen) """
     
    db.query(query_str)

    print("15 actualizando los usuarios que ya no se encuentran en la tabla: " + str(db.affected_rows()))

    print("Termina el proceso de cargue exitosamente")



def write_excelfile(db):

    #db = MySQLdb.connect(host="sisbenqa.cfuphjwmez2w.us-east-1.rds.amazonaws.com",user="sisbenrb",passwd="sisbenrb",db = "sisben_local")
    db=_mysql.connect(host="192.168.0.11",
                      user="root",
                      password="",
                      database="sisben_migracion") 
    
    vcon = str(db.get_host_info())
    print("Conectado a la BD:", vcon)

    count=0
    book=0
    title = ['Tipo de Documento','Documento','Estado']
    forma = ['@','0','@']

    print ("Proceso Excel inicio "+str(datetime.datetime.now()))

    wb = Workbook()
    style = XFStyle()
  ## query original 
    query_str = """SELECT distinct consulta_tipodocumento.abrev  AS abrev,  concat(documen) AS documento,
       CASE WHEN (tiponovedad_id  IS NULL ) THEN 'activo' ELSE 'excluido' END AS state 
       FROM `consulta_personasisben` inner join consulta_tipodocumento on consulta_personasisben.tipodocumento_id=consulta_tipodocumento.id"""

    # query_str="""SELECT DISTINCT 'CC' AS abrev, concat(documen),
    #   CASE WHEN (tiponovedad_id  IS NULL ) THEN 'excluido' ELSE 'activo' END AS state 
    #   FROM `tmp_consulta_personasisben`;
    #      """
    # query_str = """SELECT DISTINCT 'CC' AS abrev, concat(documen) AS Documento, 'activo'
    # AS Estado FROM __tmp_consulta_personasisben WHERE tiponovedad_id IS NULL UNION ALL SELECT DISTINCT 'CC'
    # AS abrev, concat(documen) AS Documento, 'excluido' AS Estado FROM __tmp_consulta_personasisben WHERE
    # tiponovedad_id IS NOT NULL AND documen NOT IN (SELECT DISTINCT concat(documen)
    # FROM __tmp_consulta_personasisben WHERE tiponovedad_id IS NULL)"""



    print (query_str)

    db.query(query_str)
    result=db.store_result()

    for row in result.fetch_row(maxrows=0):
            if count==0:
                    sheet = wb.add_sheet("Datos "+str(book))

                    for j in range(3):
                            sheet.write(0,j,title[j])

            count+=1

            for j in range(3):
                    style.num_format_str = forma[j]
                    sheet.write(count,j,str(row[j]),style)

            if count==65000:
                    count=0
                    book+=1

    wb.save('C:/Users/USER/Desktop/Recaudo Bogota/sisben/migracion2/NovedadesSisben.xls')
    print ("Proceso Excel final "+str(datetime.datetime.now()))
    #cursor.close()


def write_csvfile(db):

    file_path = r'C:/Users/USER/Desktop/Recaudo Bogota/sisben/migracion2/SISBEN.csv'

    title = ['abrev','Documento','Estado']

    db = MySQLdb.connect(host="192.168.0.11",user="root",passwd="",db = "sisben_migracion")

    cursor = db.cursor()
    query_str = """SELECT distinct consulta_tipodocumento.abrev  AS abrev,  concat(documen) AS documento,
       CASE WHEN (tiponovedad_id  IS NULL ) THEN 'activo' ELSE 'excluido' END AS state 
       FROM `consulta_personasisben` inner join consulta_tipodocumento on consulta_personasisben.tipodocumento_id=consulta_tipodocumento.id"""
    
    #query_str = "SELECT DISTINCT 'CC' AS abrev, concat(documen) AS Documento, 'activo' AS Estado FROM __tmp_consulta_personasisben WHERE tiponovedad_id IS NULL UNION ALL SELECT DISTINCT 'CC' AS abrev, concat(documen) AS Documento, 'excluido' AS Estado FROM __tmp_consulta_personasisben WHERE tiponovedad_id IS NOT NULL AND documen NOT IN (SELECT DISTINCT concat(documen) FROM __tmp_consulta_personasisben WHERE tiponovedad_id IS NULL)"


    print ("Proceso CSV inicio "+str(datetime.datetime.now()))
    print (query_str)

    cursor.execute(query_str)
    resultado = cursor.fetchall()
    tupla = tuple(resultado)

    with codecs.open(file_path, "wb", "utf-8-sig") as csv_file:

        cells = []

        for header in title:
            cells.append(header)

        cells.append(u'\n')
        cell = cells[:-1]
        csv_file.write(u','.join(cell))
        csv_file.write(u'\n')

        for refund in tupla:
            cells = []
            cells.append((refund[0]))
            cells.append((refund[1]))
            cells.append((refund[2]))
            cells.append(u'\n')
            cell = cells[:-1]
            csv_file.write(u','.join(cell))
            csv_file.write(u'\n')

    print ("Proceso CSV final "+str(datetime.datetime.now()))

    cursor.close()
