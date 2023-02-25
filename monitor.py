import mss.tools
import pytesseract as tess
import pyautogui as pg
from PIL import Image
import time as tp
import mysql.connector
import cv2
import numpy as np
import re
from datetime import datetime, timedelta

tess.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'


""" summary for monitor

pruebas para capturar el segundo monitor para sacar datos que utilizare
"""


def captura_varias_pantallas(x,y,ancho,largo,pantalla,nombre):
    """AI is creating summary for captura_varias_pantallas

    Args:
        x ([int]): [el punto x en donde se encuentra el punto inicial de la segunda pantalla]
        y ([int]): [el punto y en donde se encuentra el punto inicial de la segunda pantalla]
        ancho ([int]): [el ancho de lo que va a capturar]
        largo ([int]): [el largo de la imagen que va a capturar]
        pantalla ([int]): [a que pantalla va dirigida]
        nombre ([string]): [nombre de la imagen ]

    Returns:
        [string]: [devuelve lo que hay escrito en la imagen que capturo]
    """
    with mss.mss() as sct:
        monitor_number = pantalla
        mon = sct.monitors[monitor_number]
        monitor = {
            "top": mon["top"] + y,  
            "left": mon["left"] + x,  
            "width": ancho,
            "height": largo,
            "mon": monitor_number,
        }       
        # Grab the data
        sct_img = sct.grab(monitor)

        # Save to the picture file
        mss.tools.to_png(sct_img.rgb, sct_img.size, output='imagenes/'+nombre+'.png')
        my_image = Image.open('imagenes/'+nombre+'.png')
        invact = tess.image_to_string(my_image)
        return invact


def captura_varias_pantallas_ampl(x,y,ancho,largo,pantalla,nombre,dimension):
    """AI is creating summary for captura_varias_pantallas_ampl

    Args:
        x ([int]): [el punto x en donde se encuentra el punto inicial de la segunda pantalla]
        y ([int]): [el punto y en donde se encuentra el punto inicial de la segunda pantalla]
        ancho ([int]): [el ancho de lo que va a capturar]
        largo ([int]): [el largo de la imagen que va a capturar]
        pantalla ([int]): [a que pantalla va dirigida]
        nombre ([string]): [nombre de la imagen ]
        dimension ([int]): [x cuanto quiere ampliar la imagen ]

    Returns:
        [string]: [devuelve lo que hay escrito en la imagen que capturo]
    """
    with mss.mss() as sct:
        monitor_number = pantalla
        mon = sct.monitors[monitor_number]
        monitor = {
            "top": mon["top"] + y,  
            "left": mon["left"] + x,  
            "width": ancho,
            "height": largo,
            "mon": monitor_number,
        }       
        # Grab the data
        sct_img = sct.grab(monitor)

        # Save to the picture file
        mss.tools.to_png(sct_img.rgb, sct_img.size, output='imagenes/'+nombre+'.png')
        img = cv2.imread('imagenes/'+nombre+'.png')
        lar = (largo*dimension)
        anc = (ancho*dimension)
        imgresize = cv2.resize(img, (anc,lar))
        cv2.imwrite('imagenes/'+nombre+'Amplificada.png',imgresize)
        my_image = Image.open('imagenes/'+nombre+'.png')
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


def escala_grises(img,name):
    """AI is creating summary for escala_grises


    Args:
        img ([string]): [direccion de la imagen que se quiere cambiar a blanco y negro]
        name ([type]): [renombrar la imagen]

    Returns:
        [string]: [lo que hay escrito en la imagen ]
    """
    im=cv2.imread(img)
    gris = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    img2 = cv2.equalizeHist(gris,cv2.COLOR_BGR2GRAY)
    cv2.imwrite("imagenes/"+name+".png",img2)
    my_image = Image.open("imagenes/"+name+".png")
    invact = tess.image_to_string(my_image)
    return invact

# capital_quotex = [(818),290,80,25]
# #capital_quotex_img = captura_varias_pantallas(capital_quotex[0],capital_quotex[1],capital_quotex[2],capital_quotex[3],2,"segundaimagen")
# reg_amp_seg = captura_varias_pantallas_ampl(capital_quotex[0],capital_quotex[1],capital_quotex[2],capital_quotex[3],2,"segundaimagen",3)
# gris = escala_grises('imagenes/segundaimagenAmplificada.png', 'pgris')
# img_mod = gris.replace(",","").replace("\n","")
# array_saldo_quotex = [int(s) for s in re.findall(r'-?\d+\.?\d*', img_mod)]
# saldo_quotex = array_saldo_quotex[0]
# print(saldo_quotex)


capital_quotex = [818,281,80,25]
capital_quotex_img = captura_varias_pantallas(capital_quotex[0],capital_quotex[1],capital_quotex[2],capital_quotex[3],2,"capital_quotex_img")
gris = escala_grises('imagenes/capital_quotex_img.png', 'pgris')
img_mod = gris.replace(",","").replace("\n","")
array_saldo_quotex = [float(s) for s in re.findall(r'-?\d+\.?\d*', img_mod)]
saldo_quotex = array_saldo_quotex[0]

print(saldo_quotex)
