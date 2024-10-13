from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    ## PANTALLA DE INICIO
    path('', views.Inicio, name='Inicio'),

    ## REGISTRAR PERSONA, AREA
    path('R_Area/', views.Area_U, name='R_Area'),
    path('R_Persona/', views.Persona_U, name='R_Persona'),
    path('buscar_Persona/', views.buscar_Persona, name='buscar_Persona'),

    path('Lista/the/personas/', views.Listado_Personas, name='Listado_Personas'),

    path('Edit_Persona/<int:producto_id>/', views.Editar_Persona, name='Editar_Persona'),


    path('E_Tonner/', views.E_Recarga, name='E_Tonner'),    

    ## TONER DISPONIBLE
    path('R_Tonner/', views.Tonner_U, name='R_Tonner'),
    path('L_Tonner/', views.E_Libre, name='L_Tonner'),
    path('buscar_Toners/', views.buscar_toners, name='buscar_Toners'),

    ## EDITAR TONER
    path('ED_Tonner/<int:producto_id>/', views.Editar_Tonner, name='ED_Tonner'),    

    ## TABLAS DE IMPRESORAS
    path('Tabla_Impresoras_OFC/', views.Tabla_Impresoras_OFC, name='Tabla_Impresoras_OFC'),
    path('Tabla/Impresoras/Municipios/', views.Tabla_D_Toners_Municipios, name='Tabla_D_Toners_Municipios'),
    path('Ver_Tabla_OFP/', views.Ver_Tabla_OFP, name='Ver_Tabla'),
    path('Ver_Tabla_Municipios/', views.ver_tabla_municipios, name='Ver_Tabla_Municipios'),
    path('buscar_T_OFP/', views.buscar_T_OFP, name='buscar_T_OFP'),
    path('buscar_Tabla_T_Toners_Municipios/', views.buscar_Tabla_T_Toners_Municipios, name='buscar_Tabla_T_Toners_Municipios'),

    ## EDITAR TABLAS
    path('editar_t_municipios/<int:producto_id>/', views.editar_t_municipios, name='editar_t_municipios'),
    path('Tabla_T_Toners_OFP/<int:producto_id>/', views.Tabla_T_Toners_OFP, name='Tabla_T_Toners_OFP'),

    ## DETALLES E INFORMACION DE TABLAS OFC Y MUNICIPIOS
    path('detalles_T_OFP/', views.detalles_T_OFP, name='detalles_T_OFP'),
    path('detalles_T_Municipios/', views.detalles_T_Municipios, name='detalles_T_Municipios'),



    ## RETIRO DE TONNERS
    path('retirar_Tonner/<int:producto_id>/', views.RetiroTonner, name='retiroTonner'),
    path('toners-retirados/<int:producto_id>/', views.detalle_retiro_toner, name='detalle_retiro_toner'),
    path('V_Toners_R/', views.Buscar_Retiro, name='buscar_retiro'),

    ## Reacargar
    path('add_lista_de_recarga/<int:producto_id>/', views.add_Lista_de_Recarga, name='add_lista_de_recarga'),
    path('eliminar_de_lista_recarga/<int:producto_id>/', views.eliminar_de_lista_recarga, name='eliminar_de_lista_recarga'),
    path('ver_carrito/', views.ver_carrito, name='ver_carrito'),
    path('Toner_Recarga/', views.Toner_Recarga, name='Toner_Recarga'),
    path('detalles_toner/<int:producto_id>/', views.detalles_toner, name='detalles_toner'),

    path('guardar-recargas/', views.guardar_recargas, name='guardar_recargas'),
    path('pagina-exitosa/', views.pagina_exitosa, name='pagina_exitosa'),
    path('buscar_toners_R/', views.buscar_toners_R, name='buscar_toners_R'),

    ## LISTA DE TONERS POR ENTREGAR A SEAPTO
    path('Lista_T_Pendientes/', views.Lista_T_Pendientes, name='Lista_T_Pendientes'),
    path('recibir-toner/<int:toner_recargado_id>/', views.recibir_toner, name='recibir_toner'),

    ## DESCARGAR PDF DE MANUAL DE USUARIO
    path('download-pdf/', views.download_pdf, name='download_pdf'),

    ##Area
    path('Lista_Areas/', views.Lista_Areas, name='Lista_Areas'),
    path('Buscar_Area/', views.Buscar_Area, name='Buscar_Area'),
    path('Editar_Area/<int:producto_id>/', views.Editar_Area, name='Editar_Area'),

    ## Reportes
    path('reporte/excel/', views.generar_reporte_excel, name='generar_reporte_excel'),

    ## Cerrar servidor

    path('cerrar-servidor/', views.cerrar_servidor, name='cerrar_servidor'),


    ## Buscar toner pendientes
    path('Buscar_T_Recargando/', views.Buscar_T_Recargando, name='Buscar_T_Recargando'),

    ## OFF_SERVER.

    path('OFF_SERVER/', views.OFF_SERVER, name='OFF_SERVER'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)