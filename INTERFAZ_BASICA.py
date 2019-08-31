# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 17:21:21 2018

@author: Daniel Delgado Rodrìguez
           
"""
###############################################################################
###############################################################################
        #########           ###########                ###########            
        #        #      @        #                          # 
        #        #               #                          #
        #        #      #        #         #########        #
        #########       #        #        #         #       #
        #        #      #        #        #         #       #
        #        #      #        #        #         #       #
        #        #      #        #        #         #       #
        #########       #   ###########    #########        #
###############################################################################
###############################################################################
        
#-------------------------IMPORTAR LÌBRERIAS-----------------------------------
from statistics import mode
from multiprocessing import Process
from multiprocessing import Queue
from imutils.video import VideoStream
import tkinter
from PIL import Image, ImageTk
import cv2
from datetime import datetime,timedelta
import imutils
from tkinter import ttk
from tkinter import font
from tkinter import Canvas
import numpy as np
import time
#------------------------IMPORTAR SUB-MODULOS----------------------------------

#----------------------DESARROLLO INTERFAZ_GRAFICA-----------------------------
class Interfaz_grafica_usuario(tkinter.Tk):
    def __init__(self,parent):
        tkinter.Tk.__init__(self,parent)
#------------------------INICIALIZACIÒN DE VARIABLES---------------------------
        self.parent = parent
        self.ID_CONTENDOR = "bote0001"
        #-------------------VARIABLES DEL TIEMPO DE ENVIO----------------------
        self.tiempo_envio_datos = 5
        #------------------VARIABLES DE LOS CONTENDORES------------------------
        self.cantidad_contenedor_1 = 0
        self.cantidad_contenedor_2 = 0
        self.cantidad_contenedor_3 = 0
        self.cantidad_contenedor_4 = 0
        self.cantidad_contenedor_5 = 0
        self.cantidad_contenedor_6 = 0
        self.contendor_lleno = "-"        
        #----------------------TIEMPO DE ESPERA--------------------------------
        self.tiempo_espera = 0
#----------------------VARIABLES DE LA INTERFAZ GRAFICA------------------------
        #--------------ALMACENAR DATOS CANTIDAD RESIDUOS-----------------------
        self.contador = 0
        self.datos = []
        self.min_a = 0
        self.min_d = 0
        #self.Leer_datos()
        self.detectado = False
        #--------------DATOS DE INFORMACIÒN DE LA INTERFAZ---------------------
        self.estado_contenedor = tkinter.StringVar()
        self.estado_contenedor.set(u"ESTADO DEL CONTENDOR E INFORMACIÒN DE FALLOS")
        self.residuo_1 = tkinter.StringVar()
        self.residuo_1.set(u"000 %")
        self.residuo_2 = tkinter.StringVar()
        self.residuo_2.set(u"000 %")
        self.residuo_3 = tkinter.StringVar()
        self.residuo_3.set(u"000 %")
        self.residuo_4 = tkinter.StringVar()
        self.residuo_4.set(u"000 %")
        self.residuo_5 = tkinter.StringVar()
        self.residuo_5.set(u"000 %")
        self.residuo_6 = tkinter.StringVar()
        self.residuo_6.set(u"000 %")
        
        hora_actual = datetime.now()
        hora_actual = hora_actual.strftime(""+str(hora_actual.year)+"/%m/%d-%H:%M:%S")
        self.hora = tkinter.StringVar()
        self.hora.set("HORA Y FECHA: "+hora_actual)
        
        self.estado_internet = tkinter.StringVar()
#-----------------------INICIO DE PROCESO DE LOS SUB-MODULOS-------------------
        #Comunicacion_nodo.Conectar_Arduino()
        self.detections = None
        #----------------------CÀMARA USB----------------------------------------------
        try:
            self.vs = VideoStream(src=1).start()
            #---------------------CAMARA DE LA RASPBERRY PI--------------------------------
            #vs = VideoStream(usePiCamera=True).start()
        except:
            self.estado_contenedor.set(u"MALA CONEXIÒN O DAÑO DE LA CÀMARA")
#-----------------------ALMACENAMIENTO APAGADO---------------------------------
        self.initialize()
###############################################################################
###############################################################################
#---------------------------INTERFAZ PRINCIAPL---------------------------------
    def initialize(self):
        #---------------------LETRAS INTERFAZ PRINCIPAL------------------------
        letra_tiempo = font.Font(family='Helvetica', size=25, weight=font.BOLD)
        letra_otros = font.Font(family='Helvetica', size=8, weight=font.BOLD)
        #---------------------FONDO INTERFAZ-----------------------------------
        self.grid()
        self.fondo = tkinter.Frame(self, width=798, height=453, bg = "gray")
        self.fondo.grid(column=0, row = 0, padx=1, pady= 1)
        
        barra_principal = tkinter.Frame(self.fondo, width=793, height=2, bg = "gray")
        barra_principal.grid(column=0, row = 0, padx=1, pady= 0)
        #---------------------BARRA ESTADO CONTENEDOR--------------------------
        barra_estado = tkinter.Frame(barra_principal, width=500, height=2, bg = "gray")
        barra_estado.grid(column=0, row = 0, padx=1, pady= 0)
        subbarra_estado = tkinter.Frame(barra_estado, width=500, height=2, bg = "gray")
        subbarra_estado.grid(column=0, row = 0, padx=0, pady= 0)
        #---------------------ESTADO ACTUAL CONTENDOR--------------------------
        self.vista_estado = tkinter.Label(subbarra_estado,textvariable=self.estado_contenedor,anchor="center",fg="white",bg="blue", width=95,height = 1,font=letra_otros)
        self.vista_estado.grid(column=0,row=0,padx=0, pady=0,sticky='EW')
        #------------------------ID DEL CONTENDOR (UNICO)----------------------
        barra_informacion = tkinter.Frame(subbarra_estado, width=500, height=2, bg = "gray")
        barra_informacion.grid(column=0, row = 1, padx=0, pady= 0)
        
        id_contendor = tkinter.StringVar()
        id_contendor.set("ID: "+self.ID_CONTENDOR)
        identificador_contenedor = tkinter.Label(barra_informacion,textvariable=id_contendor,anchor="center",fg="white",bg="blue", width=30,height = 1,font=letra_otros)
        identificador_contenedor.grid(column=0,row=1,padx=0, pady=0,sticky='EW')
        #------------------------CONEXIÒN A INTERNET---------------------------
        identificador_contenedor = tkinter.Label(barra_informacion,textvariable=self.estado_internet,anchor="center",fg="white",bg="blue", width=30,height = 1,font=letra_otros)
        identificador_contenedor.grid(column=1,row=1,padx=0, pady=0,sticky='EW')
        #------------------------HORA ACTUAL DEL SISTEMA-----------------------
        identificador_contenedor = tkinter.Label(barra_informacion,textvariable=self.hora,anchor="center",fg="white",bg="blue", width=35,height = 1,font=letra_otros,justify="center")
        identificador_contenedor.grid(column=2,row=1,padx=0, pady=0,sticky='EW')
        #------------------------CONFIGURACION SUPER USUARIO-------------------
        barra_configuracion = tkinter.Frame(barra_principal, width=32, height=32, bg = "gray")
        barra_configuracion.grid(column=1, row = 0, padx=0, pady= 0)
        icono_configuracion = tkinter.PhotoImage(file="IMAGENES/CONFIGURACION.png")
        #icono_configuracion = cv2.resize(cv2.imread("IMAGENES/CONFIGURACION.png"), (10,10), interpolation = cv2.INTER_AREA)
        boton_configuracion = tkinter.Button(barra_configuracion, width=30, height=50, image=icono_configuracion, bg='white', command=self.cerrar_interfaz)
        boton_configuracion.grid(column=0,row=0,padx=0, pady=0)
        boton_configuracion.image = icono_configuracion
        #---------------BARRA DE INDICADORES E INFORMACIÒN CONTENDORES---------
        barra_indicador = tkinter.Frame(barra_estado, width=793, height=10, bg = "light gray")
        barra_indicador.grid(column=0, row = 1, padx=0, pady= 0)
        separador = tkinter.Frame(barra_indicador, width=2, height=20, bg = "light gray")
        separador.grid(column=18, row = 0, padx=0, pady= 0)
        #------------------FIGURAS INDICADOR (CÌRCULOS)------------------------
        self.indicador_contendor_1 = Canvas(barra_indicador,width=20, height=20, bg='light gray')
        self.indicador_contendor_1.grid(column=0, row = 0, padx=1, pady= 0)
        self.indicador_contendor_1.create_oval(1, 1, 19, 19, width=1, fill='green')
        
        self.indicador_contendor_2 = Canvas(barra_indicador,width=20, height=20, bg='light gray')
        self.indicador_contendor_2.grid(column=3, row = 0, padx=1, pady= 0)
        self.indicador_contendor_2.create_oval(1, 1, 19, 19, width=1, fill='green')
        
        self.indicador_contendor_3 = Canvas(barra_indicador,width=20, height=20, bg='light gray')
        self.indicador_contendor_3.grid(column=6, row = 0, padx=1, pady= 0)
        self.indicador_contendor_3.create_oval(1, 1, 19, 19, width=1, fill='green')
        
        self.indicador_contendor_4 = Canvas(barra_indicador,width=20, height=20, bg='light gray')
        self.indicador_contendor_4.grid(column=9, row = 0, padx=1, pady= 0)
        self.indicador_contendor_4.create_oval(1, 1, 19, 19, width=1, fill='green')
        
        self.indicador_contendor_5 = Canvas(barra_indicador,width=20, height=20, bg='light gray')
        self.indicador_contendor_5.grid(column=12, row = 0, padx=1, pady= 0)
        self.indicador_contendor_5.create_oval(1, 1, 19, 19, width=1, fill='green')
        
        self.indicador_contendor_6 = Canvas(barra_indicador,width=20, height=20, bg='light gray')
        self.indicador_contendor_6.grid(column=15, row = 0, padx=1, pady= 0)
        self.indicador_contendor_6.create_oval(1, 1, 19, 19, width=1, fill='green')
        #-----------------------TITULOS RESIDUOS-------------------------------
        residuo_contenedor_1 = tkinter.StringVar()
        residuo_contenedor_1.set("PAPEL:")
        nombre_contenedor_1 = tkinter.Label(barra_indicador,textvariable=residuo_contenedor_1,anchor="w",fg="white",bg="blue", width=5,height = 1,font=letra_otros)
        nombre_contenedor_1.grid(column=1,row=0,padx=0, pady=0,sticky='EW')
        
        residuo_contenedor_2 = tkinter.StringVar()
        residuo_contenedor_2.set("CARTON:")
        nombre_contenedor_2 = tkinter.Label(barra_indicador,textvariable=residuo_contenedor_2,anchor="w",fg="white",bg="blue", width=7,height = 1,font=letra_otros)
        nombre_contenedor_2.grid(column=4,row=0,padx=0, pady=0,sticky='EW')
        
        residuo_contenedor_3 = tkinter.StringVar()
        residuo_contenedor_3.set("ORGANICO:")
        nombre_contenedor_3 = tkinter.Label(barra_indicador,textvariable=residuo_contenedor_3,anchor="w",fg="white",bg="blue", width=9,height = 1,font=letra_otros)
        nombre_contenedor_3.grid(column=7,row=0,padx=0, pady=0,sticky='EW')
        
        residuo_contenedor_4 = tkinter.StringVar()
        residuo_contenedor_4.set("PLÀSTICO:")
        nombre_contenedor_4 = tkinter.Label(barra_indicador,textvariable=residuo_contenedor_4,anchor="w",fg="white",bg="blue", width=8,height = 1,font=letra_otros)
        nombre_contenedor_4.grid(column=10,row=0,padx=0, pady=0,sticky='EW')
        
        residuo_contenedor_5 = tkinter.StringVar()
        residuo_contenedor_5.set("VIDRIO:")
        nombre_contenedor_5 = tkinter.Label(barra_indicador,textvariable=residuo_contenedor_5,anchor="w",fg="white",bg="blue", width=6,height = 1,font=letra_otros)
        nombre_contenedor_5.grid(column=13,row=0,padx=0, pady=0,sticky='EW')
        
        residuo_contenedor_6 = tkinter.StringVar()
        residuo_contenedor_6.set("OTROS:")
        nombre_contenedor_6 = tkinter.Label(barra_indicador,textvariable=residuo_contenedor_6,anchor="w",fg="white",bg="blue", width=6,height = 1,font=letra_otros)
        nombre_contenedor_6.grid(column=16,row=0,padx=0, pady=0,sticky='EW')
        #---------------------PORCENTAJES DE LOS RESIDUOS----------------------
        self.valor_contenedor_1 = tkinter.Label(barra_indicador,textvariable=self.residuo_1,anchor="w",fg="white",bg="blue", width=5,height = 1,font=letra_otros)
        self.valor_contenedor_1.grid(column=2,row=0,padx=0, pady=0,sticky='EW')
        
        self.valor_contenedor_2 = tkinter.Label(barra_indicador,textvariable=self.residuo_2,anchor="w",fg="white",bg="blue", width=5,height = 1,font=letra_otros)
        self.valor_contenedor_2.grid(column=5,row=0,padx=0, pady=0,sticky='EW')
        
        self.valor_contenedor_3 = tkinter.Label(barra_indicador,textvariable=self.residuo_3,anchor="w",fg="white",bg="blue", width=5,height = 1,font=letra_otros)
        self.valor_contenedor_3.grid(column=8,row=0,padx=0, pady=0,sticky='EW')
        
        self.valor_contenedor_4 = tkinter.Label(barra_indicador,textvariable=self.residuo_4,anchor="w",fg="white",bg="blue", width=5,height = 1,font=letra_otros)
        self.valor_contenedor_4.grid(column=11,row=0,padx=0, pady=0,sticky='EW')
        
        self.valor_contenedor_5 = tkinter.Label(barra_indicador,textvariable=self.residuo_5,anchor="w",fg="white",bg="blue", width=5,height = 1,font=letra_otros)
        self.valor_contenedor_5.grid(column=14,row=0,padx=0, pady=0,sticky='EW')
        
        self.valor_contenedor_6 = tkinter.Label(barra_indicador,textvariable=self.residuo_6,anchor="w",fg="white",bg="blue", width=5,height = 1,font=letra_otros)
        self.valor_contenedor_6.grid(column=17,row=0,padx=0, pady=0,sticky='EW')
        #-------------------IMAGEN DE CAPTURA DE LOS DATOS---------------------
        barra_secundaria = tkinter.Frame(self.fondo, width=300, height=200, bg = "light gray")
        barra_secundaria.grid(column=0, row = 2, padx=1, pady= 0)
        
        barra_camara = tkinter.Frame(barra_secundaria, width=300, height=200, bg = "light gray")
        barra_camara.grid(column=0, row = 0, padx=0, pady= 0)
        self.imagen_camara_c = tkinter.Label(barra_camara)
        self.imagen_camara_c.grid(column=0, row = 0, padx=0, pady= 0)
        self.actualizar_imagen(cv2.resize(cv2.imread("IMAGENES/LOGO_EMPRESA.png"), (555,420), interpolation = cv2.INTER_AREA),1)
        #-------------------IMAGEN DE RESIDUO CLASIFICADO (ROI)----------------
        barra_residuo = tkinter.Frame(barra_secundaria, width=280, height=380, bg = "light gray")
        barra_residuo.grid(column=1, row = 0, padx=1, pady= 1)
        
        barra_clasificacion = tkinter.Frame(barra_residuo, width=280, height=380, bg = "light gray")
        barra_clasificacion.grid(column=0, row = 0, padx=1, pady= 1)
        
        self.imagen_r = tkinter.Label(barra_clasificacion)
        self.imagen_r.grid(column=0, row = 0, padx=0, pady= 0)
        self.actualizar_imagen(cv2.resize(cv2.imread("IMAGENES/LOGO_EMPRESA.png"), (235,165), interpolation = cv2.INTER_AREA),2)
        #-------------------IMAGEN DEL LOGO DEL RESIDUO------------------------
        barra_logo = tkinter.Frame(barra_residuo, width=280, height=380, bg = "light gray")
        barra_logo.grid(column=0, row = 1, padx=1, pady= 1)
        
        self.imagen_l = tkinter.Label(barra_logo)
        self.imagen_l.grid(column=0, row = 0, padx=0, pady= 0)
        self.actualizar_imagen(cv2.resize(cv2.imread("IMAGENES/LOGO_EMPRESA.png"), (235,165), interpolation = cv2.INTER_AREA),3)
        #--------------------TIEMPO DE ESPERA INGRESO--------------------------
        barra_tiempo = tkinter.Frame(barra_residuo, width=280, height=380, bg = "light gray")
        barra_tiempo.grid(column=0, row = 2, padx=0, pady= 0)
        
        tiempo = tkinter.StringVar()
        tiempo.set("TIEMPO: 00")
        tiempo_espera = tkinter.Label(barra_tiempo,textvariable=tiempo,anchor="w",fg="white",bg="blue", width=10,height = 2,font=letra_tiempo)
        tiempo_espera.grid(column=0,row=0,padx=0, pady=0,sticky='EW')
        #---------------PASAR A LOOP DE ACTUALIZACIÒN DE LA INTERFAZ-----------
        self.actualizar()
###############################################################################
###############################################################################
#---------------------LOOP DE ACTUALIZACIÒN DE LA INTERFAZ---------------------
    def actualizar(self):
        #--------------------ACTUALIZACIÒN DE LA HORA--------------------------
        hora_actual = datetime.now()
        hora_actual = hora_actual.strftime(""+str(hora_actual.year)+"/%m/%d-%H:%M:%S")
        self.hora.set("HORA Y FECHA: "+hora_actual)
        #-------------------VERIFICAR CONEXIÒN A INTERNET----------------------
        #self.verificar_conexion_internet()
        #----------------------------FIN LOOP----------------------------------
        self.after(1, self.actualizar)
###############################################################################
    def leer_configuracion(self):
        f = open("cantidad_fotos.txt")
        linea = f.readline()
        linea_n = linea.split(',')
        self.cantidad_objeto_1 = int(linea_n[0])
        self.cantidad_objeto_2 = int(linea_n[1])
        self.cantidad_objeto_3 = int(linea_n[2])
        self.cantidad_objeto_4 = int(linea_n[3])
        self.cantidad_objeto_5 = int(linea_n[4])
        f.close()
    def guardar_configuracion(self):
        f = open("cantidad_fotos.txt",'w+')
        mensaje = str(self.cantidad_objeto_1)+","+str(self.cantidad_objeto_2)+","+str(self.cantidad_objeto_3)+","+str(self.cantidad_objeto_4)+","+str(self.cantidad_objeto_5)+","
        f.write(mensaje)
        f.close()
#----------------ACTUALIZACIÒN DE IMAGEN EN LA INTERFAZ------------------------
    def actualizar_imagen(self,toma,opcion):
        b,g,r = cv2.split(toma)
        gray_im = cv2.merge((r,g,b))
        a = Image.fromarray(gray_im)
        b = ImageTk.PhotoImage(image=a)
        if(opcion == 1):
            self.imagen_camara_c.configure(image=b)
            self.imagen_camara_c._image_cache = b
        if(opcion == 2):
            self.imagen_r.configure(image=b)
            self.imagen_r._image_cache = b
        if(opcion == 3):
            self.imagen_l.configure(image=b)
            self.imagen_l._image_cache = b

#-----------------------CERRAR INTERFAZ----------------------------------------
    def cerrar_interfaz(self):        
        self.destroy()
#--------------------CREACION DE LA VENTANA PRINCIPAL--------------------------
if __name__ == "__main__":
    app = Interfaz_grafica_usuario(None)
    app.title('Interfaz bàsica')
    ancho_ventana = 800
    alto_ventana = 480
    app.geometry("%dx%d+%d+%d"%(ancho_ventana,alto_ventana,0,0))
    app.resizable(False,False)
    app.overrideredirect(True)
    app.config(bg= "black")
    app.mainloop()
#-------------------------FIN DEL PROGRAMA-------------------------------------
###############################################################################
###############################################################################
        #########           ###########                ###########            
        #        #      @        #                          # 
        #        #               #                          #
        #        #      #        #         #########        #
        #########       #        #        #         #       #
        #        #      #        #        #         #       #
        #        #      #        #        #         #       #
        #        #      #        #        #         #       #
        #########       #   ###########    #########        #
###############################################################################
###############################################################################