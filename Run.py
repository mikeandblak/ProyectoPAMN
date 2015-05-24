#!/usr/bin/env python
# coding=utf-8

from Peticiones.Peticiones import Peticiones
from Instagram.MediaInstagram import BusquedaMedia
from Twitter.MediaTwitter import MediaTwitter
from HTML.GeneradorHTML import GeneradorHTML
from Ordenamiento.Ordenacion import OrdenadorImagenes
from termcolor import *


# Clase Run, combinación de los componenetes y generar el programa
class Run:
    def __init__(self):
        print('Cargando...')  # Mensaje mientras instacia API Instagram y Twitter
        self.lista_imagenes = []  # Lista que guarda cada una de las imágenes
        self.token_instagram = '1750630587.ee26789.814d1f9eef7b47acb90a958dedcb7af7'  # Access Token de Instagram
        self.datos_twitter = {
            'c_key': 'zAS0Nqxy38IybYdvtd5p4UcOB',
            'c_secret': 'JPh1abxusINcSfRlfS0VF1bgPU45iQkYrWlyZh7yFa1JlS9gpx',
            'token': '135695196-oLyFTOofiBnlAc3eO9l3asDbd8aKeCAx8KZHQINb',
            'token_secret': 'gJw2oZmcPQK7tRfItvTntItoQnu8AVTjnF269dEoug2JT'
            }  # Diccionario con los datos de Twitter
        self.search_t = MediaTwitter(self.datos_twitter)  # Instancia de Api Twitter
        self.search_i = BusquedaMedia(self.token_instagram)  # Instancia de Api Instagram

    def menu_busqueda(self):
        Peticiones.limpiar_pantalla()  # "Limpia" la consola
        cprint('\t\t\tGenerador de Galería ordenada', 'yellow', attrs=['bold'])  # Título
        self.__menu_tipo_busqueda__()  # Muestra el menú
        modo_busqueda = Peticiones.pedir_numero('Elige una opcion: ', [1, 3])  # Pide y guarda la opción elegida
        if modo_busqueda is 1:
            self.__busqueda_tag__()
        elif modo_busqueda is 2:
            self.__busqueda_popular__()
        else:
            self.__busqueda_coordenadas__()
        self.generar_html()

    def __busqueda_tag__(self):
        tag = raw_input('Introduce el Hashtag: ')
        print('Espere un momento...')
        self.__agregar_imagenes__(self.search_i.por_tag(tag))
        self.__agregar_imagenes__(self.search_t.buscar_por_tags(tag))

    def __busqueda_popular__(self):
        print('Espere un momento...')
        self.__agregar_imagenes__(self.search_i.media_popular())
        self.__agregar_imagenes__(self.search_t.buscar_popular())

    def __busqueda_coordenadas__(self):
        print('Mapa: http://www.bufa.es/google-maps-latitud-longitud/')
        latitud = float(raw_input('\tLatitud: '))
        longitud = float(raw_input('\tLongitud: '))
        print('Espere un momento...')
        self.__agregar_imagenes__(self.search_i.por_coordenadas(latitud, longitud))
        self.__agregar_imagenes__(self.search_t.buscar_por_cordenadas(latitud, longitud))

    def __agregar_imagenes__(self, lista_datos):
        if lista_datos is not None:
            for datos in lista_datos:
                self.lista_imagenes.append(datos)

    def generar_html(self):
        Peticiones.limpiar_pantalla()
        ordenador = OrdenadorImagenes(self.lista_imagenes)
        print('Se encontraron: {0} imágenes.'.format(len(self.lista_imagenes)))
        respuesta = self.__menu_ordenamiento__()
        respuesta2 = self.__menu_forma_ord__()

        respuesta2 = False if respuesta2 is 1 else True

        lista_ordenada = ordenador.por_fecha(respuesta2) if respuesta is 1 else ordenador.por_usuario(respuesta2)

        nombre = raw_input('Nombre del proyecto: ')
        Peticiones.copiar_archivos_responsive(nombre)
        generador = GeneradorHTML(nombre, lista_ordenada)
        generador.generar_archivo()

    @staticmethod
    def __menu_forma_ord__():
        Peticiones.limpiar_pantalla()
        print('\t1. Ascendente')
        print('\t2. Descendente')
        return Peticiones.pedir_numero('Elige tipo de orden: ', [1, 2])

    @staticmethod
    def __menu_ordenamiento__():
        Peticiones.limpiar_pantalla()
        cprint('\t\tOrdenar Por: ', 'yellow', attrs=['bold'])
        print('\t1. Fecha')
        print('\t2. Nombre de usuario')
        return Peticiones.pedir_numero('Elige una opcion: ', [1, 2])

    @staticmethod
    def __menu_tipo_busqueda__():
        cprint('1. Por hashtag')
        cprint('2. Popular ')
        cprint('3. Por coordenadas')

    def __actualizar_num_imagenes__(self):
        self.numero_imagenes = len(self.lista_imagenes)


run = Run()
run.menu_busqueda()



