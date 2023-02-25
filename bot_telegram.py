import pytesseract as tess
import pyautogui as pg
from PIL import Image
import time as tp
import mysql.connector
import cv2
import numpy as np




tess.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
hostt = ''
userr = ''
passw = ''
db = ''



#Entra en compra
def call():
    pg.click(x=1808, y=361)
    
#Entra en venta
def put():
    pg.click(x=1808, y=440)


#Captura las regiones de la pantalla y le da nombre de la imagen
def capturareg(x,y,largo,ancho,name):
    captura_region = pg.screenshot(region=(x, y, largo,ancho,))
    captura_region.save('imagenes_telegram/'+name+'.png')
    my_image = Image.open('imagenes_telegram/'+name+'.png')
    invact = tess.image_to_string(my_image)
    return invact

def escala_grises(img,name):
    im=cv2.imread(img)
    gris = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    img2 = cv2.equalizeHist(gris,cv2.COLOR_BGR2GRAY)
    cv2.imwrite("pruebas/"+name+".png",img2)
    my_image = Image.open("pruebas/"+name+".png")
    invact = tess.image_to_string(my_image)
    return invact


#Captura las regiones de la pantalla y le da nombre de la imagen
def captura_reg_amp(x,y,largo,ancho,imgSave,dimension):
    captura_region = pg.screenshot(region=(x, y, largo,ancho,))
    captura_region.save('imagenes/'+imgSave+'.png')
    img = cv2.imread('imagenes/'+imgSave+'.png')
    lar = (largo*dimension)
    anc = (ancho*dimension)    
    imgresize = cv2.resize(img, (lar,anc))
    cv2.imwrite('imagenes/'+imgSave+'Amplificada.png',imgresize)
    my_images = Image.open('imagenes/'+imgSave+'Amplificada.png')
    ipl = tess.image_to_string(my_images)
    return ipl


#inicio de session del broker
def iniciar_session_broker():
    tp.sleep(1)
    inicio = capturareg(1370,622,120,30,'inicio')
    piniciar = inicio.find('Iniciar')
    if piniciar != -1:
        print (piniciar)
        pg.click(x=1521, y=768)
        tp.sleep(4)
        pg.click(x=1350, y=560)
        return 1
    else:
        return 0


def consultas(seleccion, tabla, complemento):
    conexion =  mysql.connector.connect(host=hostt, user=userr, passwd=passw,database=db)
    cursor=conexion.cursor()
    sql = (f"Select {seleccion} from {tabla} {complemento}")
    cursor.execute(sql)
    Inversion = cursor.fetchall()
    conexion.close()
    return(Inversion)



def operativaprecios():
    arrayparaentradas=[]
    pg.click(x=1810, y=590) 
    tp.sleep(1)
    entrada = capturareg(1736,808,200,20,'entrada')
    print(entrada)
    cierre = capturareg(1736,840,200,20,'cierre')
    print(cierre)
    tp.sleep(1)
    pg.click(x=1810, y=590) 
    purentra = entrada.replace("\n","")
    purcierre = cierre.replace("\n","") 
    arrayparaentradas.append(float(purentra))
    arrayparaentradas.append(float(purcierre))
    return (arrayparaentradas)


def estado():
    con = consultas('*','parametros_binarias','where id=3')
    for fi in con:
        con=fi
    estado = int(con[5])
    return estado



guardar = pg.click(x=1800, y=17)

tp.sleep(1)

bucle = estado()
parainvbot =[1638,112,60,20]
paracaptporcentaje = [1113,170,30, 20]
paracaptporcentajeotc=[1244,170,30, 20]
porcentaje_apostado = [1775,293,70,20]

usua = pg.screenshot(region=(5, 207, 55,55))
usua.save('imagenes_telegram/usu.png')


while bucle == 1 :

    iniciar_session_broker()

    usua2 = pg.screenshot(region=(5, 207, 55,55))
    usua2.save('imagenes_telegram/usu2.png')

    img1 = cv2.imread('imagenes_telegram/usu.png',1)
    img2 = cv2.imread('imagenes_telegram/usu2.png',1)

    def comprobar(img1,img2):
        eva=cv2.subtract(img1,img2) 
        if not np.any(eva):
            return 0
        else:
            return 1

    eval=comprobar(img1,img2)

    actualizacion = capturareg(880,390,80,70,"actualizacion")

    flecha = actualizacion.find("<")


    if(flecha!= -1 or eval==1 ):
        print('condicional')
        pg.click(x=15, y=224)
        pg.click(x=15, y=224)
        tp.sleep(1)
        señal = capturareg(87,156,300,200,"señal")
        print(señal)
        encontrar = señal.find('EUR/USD')
        otc = señal.find('OTC')
        arriba = señal.find('Arriba')
        abajo = señal.find('Abajo')
        señal_orden=""
        mercado ="EUR/USD"

        inverant = capturareg(parainvbot[0], parainvbot[1], parainvbot[2], parainvbot[3],'inver')
        invantsincom = inverant.replace(",","").replace("\n","")
        entinveant = float(invantsincom)

        if(otc!=-1 or encontrar!= -1):
            if(otc!=-1):
                mercado ="EUR/USD (OTC)"
                pg.click(1282,171)
                tp.sleep(1)
                if abajo != -1:
                    put()
                    señal_orden = "PUT"
                if arriba != -1:
                    call()
                    señal_orden = "CALL"
                porcentaje_act_otc = capturareg(paracaptporcentajeotc[0],paracaptporcentajeotc[1],paracaptporcentajeotc[2],paracaptporcentajeotc[3],'porcentajeotc')
                porc_otc = escala_grises('imagenes_telegram/porcentajeotc.png','gris_por_otc')
                Entero_porcentaje = int(porc_otc[0:2])
                tp.sleep(305)



            elif(encontrar!= -1 and otc==-1):
                mercado ="EUR/USD"
                pg.click(1140,167)
                tp.sleep(1)
                porcentaje_actual = captura_reg_amp(paracaptporcentaje[0],paracaptporcentaje[1],paracaptporcentaje[2],paracaptporcentaje[3],'porcentaje',5)
                if abajo != -1:
                    put()
                    señal_orden = "PUT"
                if arriba != -1:
                    call()
                    señal_orden = "CALL"
                capturareg(paracaptporcentaje[0],paracaptporcentaje[1],paracaptporcentaje[2],paracaptporcentaje[3],'porcentaje')
                porcentaje_actual = escala_grises('imagenes_telegram/porcentaje.png','gristprueba')
                Entero_porcentaje = int(porcentaje_actual[0:2])
                tp.sleep(305)

            print('salio condicionales')
            apuesta=captura_reg_amp(porcentaje_apostado[0],porcentaje_apostado[1],porcentaje_apostado[2],porcentaje_apostado[3],'p_apost',2)
            por_apost = apuesta.replace(",","")




            

            inveract = capturareg(parainvbot[0], parainvbot[1], parainvbot[2], parainvbot[3],'inver')
            invactsincom = inveract.replace(",","").replace("\n","") 
            entinveact = float(invactsincom)
            print('inv actual ' ,entinveact)


            opeEtarEnd = operativaprecios()
            vaEntStart  = opeEtarEnd[0]
            vaEntEnd = opeEtarEnd[1]


            try:
                conexion =  mysql.connector.connect(host=hostt, user=userr, passwd=passw,database=db)            
                cursor=conexion.cursor()
                sql = "INSERT INTO reportes_robot (señal, mercado, saldo_inicial, saldo_final,porcentajeregistrado,precio_entrada,precio_salida,porcentaje_apostado,tipo,estado) VALUES (%s, %s, %s, %s,%s,%s,%s,%s,%s,%s)"
                val = [
                (señal_orden, mercado,entinveant,entinveact,Entero_porcentaje,vaEntStart,vaEntEnd,por_apost,3,1),
                ]
                cursor.executemany(sql, val)
                conexion.commit()
                print(cursor.rowcount, "Insercion en la base de datos realizada")
                conexion.close() 

                tp.sleep(20)
            except BaseException as err:
                print(f'error: {err=} \n, {type(err)=}')
    
    bucle = estado()

    

