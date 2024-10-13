from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse,JsonResponse, Http404
from .models import Area, Persona, Tonner, Retiro_Tonner, Tabla_T_Toners, Tabla_T_Toners_Municipios, Toner_M_Recargados
from .forms import FormArea, FormPersona, FormTonner, FormsRetiroTonner,FormsTabla_Toners, FormsTabla_Toners_Municipios
import base64
from django.core.files.base import ContentFile
from collections import Counter
from django.db.models import Sum
from django.utils import timezone
from datetime import datetime
from django.http import FileResponse
from django.conf import settings
import os
from django.db.models import Q
from django.urls import resolve
import openpyxl
import signal
import psutil
from psutil import AccessDenied
import subprocess
from django.contrib import messages
import logging


def Inicio(request):
    title = 'BIENVENIDO'
    return render(request, 'inicio.html', {
        'title':title,
    })


def Area_U(request):

    if request.method == 'POST':
        form = FormArea(request.POST)
        if form.is_valid():
            form.save()

    else:
        form = FormArea()
    return render(request, 'registro/R_Area.html',{
        'form': form,
    })

def Persona_U(request):
    areas = Area.objects.all()
    if request.method == 'POST':
        form = FormPersona(request.POST, request.FILES)  
        if form.is_valid():  
            firma_data = request.POST.get('firma_imagen') 
            persona = form.save(commit=False) 
            if firma_data:
                format, imgstr = firma_data.split(';base64,')  
                ext = format.split('/')[-1]  
                
                persona.firma.save(f'firma_{persona.nombre}.{ext}', ContentFile(base64.b64decode(imgstr)), save=False)
                persona.save()  
    else:
        form = FormPersona()  

    return render(request, 'registro/R_Persona.html', {
        'areas':areas,
        'form': form,
    })

def Tonner_U(request):

    if request.method == 'POST':
        form = FormTonner(request.POST, request.FILES)
        if form.is_valid():
            form.save()

    else:
        form = FormTonner()
    return render(request, 'registro/R_Tonner.html',{
        'form': form,
    })


def Editar_Tonner(request, producto_id):
    producto = get_object_or_404(Tonner, pk=producto_id)

    if request.method == 'POST':
        form = FormTonner(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('Tonners')  
    else:
        form = FormTonner(instance=producto)

    return render(request, 'vista/Editar_Tonner.html', {
        'form': form
    })

def RetiroTonner(request, producto_id):
    producto = get_object_or_404(Tonner, pk=producto_id)
    usuarios = Persona.objects.all()  # Consulta para obtener todos los usuarios

    if request.method == 'POST':
        form = FormsRetiroTonner(request.POST)
        if form.is_valid():
            cantidad_retirada = form.cleaned_data['cantidad_retirada']
            if cantidad_retirada <= producto.cantidad:
                producto.cantidad -= cantidad_retirada
                producto.save()

                retiro = form.save(commit=False)
                retiro.r_tonner = producto
                retiro.cantidad_disponible = producto.cantidad
                retiro.save()

                return render(request, 'vista/retiro_success.html', {'producto': producto, 'retiro': retiro})
            else:
                form.add_error('cantidad_retirada', 'La cantidad a retirar es mayor que la disponible')
    else:
        form = FormsRetiroTonner()

    return render(request, 'vista/Retirar_Tonner.html', {'form': form, 'producto': producto, 'usuarios': usuarios})


def E_Recarga(request):
    r_tonner = Tonner.objects.filter(Estado='Recargando')
    return render(request, 'vista/T_Recargando.html', {'REtonner': r_tonner})

def E_Ocupado(request):
    r_tonner = Tonner.objects.filter(Estado='En Uso')
    return render(request, 'vista/T_Ocupado.html', {'OCtonner': r_tonner})

def E_Libre(request):
    r_tonner = Tonner.objects.filter(Estado='Disponible')
    return render(request, 'vista/T_Libre.html', {'LItonner': r_tonner})


def Editar_Tonner(request, producto_id):
    producto = get_object_or_404(Tonner, pk=producto_id)
    if request.method == 'POST':
        form = FormTonner(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('L_Tonner')  
    else:
        form = FormTonner(instance=producto)
    return render(request, 'vista/editar_tonner.html', {'form': form})

def Tabla_D_Toners(request):

    if request.method == 'POST':
        form = FormTonner(request.POST, request.FILES)
        if form.is_valid():
            form.save()

    else:
        form = FormTonner()
    return render(request, 'registro/R_Tonner.html',{
        'form': form,
    })

    return render(request, 'vista/T_Ocupado.html', {'producto': producto})
    

def Tabla_D_Toners_Municipios(request):

    if request.method == 'POST':
        form = FormsTabla_Toners_Municipios(request.POST)
        if form.is_valid():
            form.save()
        return redirect('Ver_Tabla_Municipios')
    else:
        form = FormsTabla_Toners_Municipios()
    return render(request, 'Tablas/añadir_municipio.html',{
        'form': form,
    })

def ver_tabla_municipios(request):
    producto = Tabla_T_Toners_Municipios.objects.all()


    return render(request, 'Tablas/tabla_municipios.html', {
        'producto':producto,
    })

def Tabla_Impresoras_OFC(request):

    if request.method == 'POST':
        form = FormsTabla_Toners(request.POST)
        if form.is_valid():
            form.save()

    else:
        form = FormsTabla_Toners()
    return render(request, 'Tablas/añadir_oficina.html',{
        'form': form,
    })

def Ver_Tabla_OFP(request):
    tabla = Tabla_T_Toners.objects.all()
    return render(request, 'Tablas/tabla_OFP.html', {
        'tabla':tabla,
    })

def detalle_retiro_toner(request, producto_id):
    retiro_toner = get_object_or_404(Retiro_Tonner, pk=producto_id)

    return render(request, 'vista/ver_T_EnUso.html', {'retiro_toner': retiro_toner})


def Listado_Personas(request):
    producto = Persona.objects.all()
    return render(request, 'vista/lista_personas.html', {
        'producto':producto,
    })


def Editar_Persona(request, producto_id):
    producto = get_object_or_404(Persona, pk=producto_id)
    if request.method == 'POST':
        form = FormPersona(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
    else:
        form = FormPersona(instance=producto)
    return render(request, 'Edit/editar_persona.html', {'form': form,})

def buscar_Persona(request):
    query = request.GET.get('q', '')  

    personas = Persona.objects.all()
    if query:
        personas = personas.filter(
            Q(nombre__icontains=query) |
            Q(area__nombre__icontains=query)
        )
    return render(request, 'vista/lista_personas.html', {'producto': personas})

def buscar_T_OFP(request):
    query = request.GET.get('q', '')  

    tabla = Tabla_T_Toners.objects.filter(oficina__icontains=query)

    return render(request, 'Tablas/tabla_OFP.html', {'tabla': tabla})

def buscar_Tabla_T_Toners_Municipios(request):
    query = request.GET.get('q', '')  

    producto = Tabla_T_Toners_Municipios.objects.filter(oficina__icontains=query)

    return render(request, 'Tablas/tabla_municipios.html', {'producto': producto})

def buscar_toners(request):
    query = request.GET.get('q')
    LItonner = Tonner.objects.filter(nombre__icontains=query) if query else []
    return render(request, 'vista/T_Libre.html', {'LItonner': LItonner})

def editar_t_municipios(request, producto_id):
    producto = get_object_or_404(Tabla_T_Toners_Municipios, id=producto_id)

    if request.method == 'POST':
        form = FormsTabla_Toners_Municipios(request.POST, instance=producto)
        if form.is_valid():
            form.save()
        return redirect('Ver_Tabla_Municipios')
    else:
        form = FormsTabla_Toners_Municipios(instance=producto)
    return render(request, 'Edit/Editar_T_Municipios.html', {'form': form,})

def Tabla_T_Toners_OFP(request, producto_id):
    producto = get_object_or_404(Tabla_T_Toners, id=producto_id)

    if request.method == 'POST':
        form = FormsTabla_Toners(request.POST, instance=producto)
        if form.is_valid():
            form.save()
    else:
        form = FormsTabla_Toners(instance=producto)
    return render(request, 'Edit/Editar_T_OFP.html', {'form': form,})



## LO COMPLICADO ⬇

def Toner_Recarga(request):
    Toner = Tonner.objects.all()
    return render(request, 'carrito/Toner_Recargar.html', {
        'toner':Toner,
    })

def buscar_toners_R(request):
    query = request.GET.get('q')
    toner = Tonner.objects.filter(nombre__icontains=query) if query else []
    return render(request, 'carrito/Toner_Recargar.html', {'toner': toner})

def add_Lista_de_Recarga(request, producto_id):
    producto = get_object_or_404(Tonner, pk=producto_id)

    carrito = request.COOKIES.get('carrito')
    if carrito:
        carrito = carrito.split(',') 
    else:
        carrito = []

    carrito.append(str(producto_id))

    response = redirect('/Toner_Recarga', producto_id=producto_id)
    response.set_cookie('carrito', ','.join(carrito)) 

    return response

def eliminar_de_lista_recarga(request, producto_id):
    producto = get_object_or_404(Tonner, pk=producto_id)

    carrito = request.COOKIES.get('carrito')

    if carrito:
        carrito = carrito.split(',')
    else:
        carrito = []

    if str(producto_id) in carrito:
        carrito.remove(str(producto_id))

    response = redirect('ver_carrito')

    response.set_cookie('carrito', ','.join(carrito))

    return response

def ver_carrito(request):
    carrito = request.COOKIES.get('carrito')
    productos_en_carrito = []
    productos = Tonner.objects.all()

    if carrito:
        carrito = carrito.split(',')  
        carrito_count = Counter(carrito)  
        producto_ids = carrito_count.keys() 
        productos = Tonner.objects.filter(id__in=producto_ids)  

        for producto in productos:
            cantidad = carrito_count[str(producto.id)]  
            productos_en_carrito.append({'producto': producto, 'cantidad': cantidad})

    return render(request, 'carrito/carrito.html', {'productos_en_carrito': productos_en_carrito, 'productos':productos })




## LO COMPLICADO ⬆

def detalles_T_OFP(request):
    marcas = Tabla_T_Toners.objects.values_list('marca', flat=True).distinct()
    tipos_toner = Tabla_T_Toners.objects.values_list('toner_de_impresora', flat=True).distinct()

    impresoras_por_marca_toner = {}
    total_general = 0

    for marca in marcas:
        impresoras_por_marca_toner[marca] = {}
        for toner in tipos_toner:
            cantidad_total = Tabla_T_Toners.objects.filter(marca=marca, toner_de_impresora=toner).aggregate(Sum('numero_impresoras'))['numero_impresoras__sum']
            cantidad = cantidad_total if cantidad_total else 0
            impresoras_por_marca_toner[marca][toner] = cantidad
            total_general += cantidad

    return render(request, 'detalles/detalles_T_OFP.html', {
        'impresoras_por_marca_toner': impresoras_por_marca_toner,
        'tipos_toner': tipos_toner,
        'total_general': total_general,
    })

def detalles_T_Municipios(request):
    marcas = Tabla_T_Toners_Municipios.objects.values_list('marca', flat=True).distinct()
    tipos_toner = Tabla_T_Toners_Municipios.objects.values_list('toner_de_impresora', flat=True).distinct()

    impresoras_por_marca_toner = {}
    total_general = 0

    for marca in marcas:
        impresoras_por_marca_toner[marca] = {}
        for toner in tipos_toner:
            cantidad_total = Tabla_T_Toners_Municipios.objects.filter(marca=marca, toner_de_impresora=toner).aggregate(Sum('numero_impresoras'))['numero_impresoras__sum']
            cantidad = cantidad_total if cantidad_total else 0
            impresoras_por_marca_toner[marca][toner] = cantidad
            total_general += cantidad

    return render(request, 'detalles/detalles_T_Municipios.html', {
        'impresoras_por_marca_toner': impresoras_por_marca_toner,
        'tipos_toner': tipos_toner,
        'total_general': total_general,
    })

def detalles_toner(request, producto_id):
    producto = get_object_or_404(Tonner, pk=producto_id)

    return render(request, 'detalles/detalles_toner.html', {
        'producto':producto,
    })

def guardar_recargas(request):
    if request.method == 'POST':
        for key in request.POST:
            if key.startswith('recargas_'):
                toner_id = key.split('_')[1]
                cantidad_recarga = int(request.POST[key])
                toner = Tonner.objects.get(id=toner_id)
                
                recarga = Toner_M_Recargados.objects.create(
                    toner=toner,
                    cantidad=cantidad_recarga,
                    estado='RECARGANDO',
                    fecha_entrega=timezone.now()
                )

        response = redirect('pagina_exitosa')
        response.delete_cookie('carrito')  
        return response

    return redirect('Toner_Recarga')

def pagina_exitosa(request):
    return render(request, 'exito/pagina_exitosa.html')


def recibir_toner(request, toner_recargado_id):
    if request.method == 'POST':
        toner_recargado = get_object_or_404(Toner_M_Recargados, pk=toner_recargado_id)
        toner_recargado.estado = 'ENTREGADO'
        toner_recargado.fecha_recibido = datetime.now()
        toner_recargado.save()
        return JsonResponse({'message': 'Recibido exitosamente.'})
    else:
        return JsonResponse({'error': 'Método no permitido.'}, status=405)


def download_pdf(request):
    pdf_file_path = os.path.join(settings.STATIC_ROOT, 'tonner', 'ManualdeUsuario.pdf')
    
    # Debug: Imprimir la ruta completa para verificar
    print(f"Ruta del archivo: {pdf_file_path}")
    
    if os.path.exists(pdf_file_path):
        with open(pdf_file_path, 'rb') as pdf_file:
            response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="ManualdeUsuario.pdf"'
            return response
    else:
        raise Http404("El archivo PDF no se encontró")
    

def Buscar_Retiro(request):
    query = request.GET.get('q', '')

    retiradas = Retiro_Tonner.objects.all().order_by('-fecha_retiro')

    if query:
        retiradas = retiradas.filter(
            Q(r_persona__area__nombre__icontains=query) |
            Q(r_tonner__nombre__icontains=query) |
            Q(caso_GLPI__icontains=(query))
        )


    return render(request, 'vista/T_Ocupado.html', {'retiradas': retiradas, 'query': query})

def Lista_Areas(request):
    item = Area.objects.all()
    return render(request, 'vista/lista_Areas.html', {
        'item':item,
    })

def Buscar_Area(request):
    query = request.GET.get('q', '')
    item = Area.objects.filter(nombre__icontains=query) if query else []
    
    return render(request, 'vista/lista_Areas.html', {
        'item':item,
    })

def Editar_Area(request, producto_id):
    producto = get_object_or_404(Area, id=producto_id)

    if request.method == 'POST':
        form = FormArea(request.POST, instance=producto)
        if form.is_valid():
            form.save()
    else:
        form = FormArea(instance=producto)
    return render(request, 'Edit/editar_Area.html', {'form': form,})

def generar_reporte_excel(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Reporte de Retiros de Tonner"

    headers = [
        'Tonner', 'Persona', 
        'Cantidad Retirada', 'Caso GLPI', 'Descripción', 'Fecha de Retiro'
    ]
    ws.append(headers)

    retiros = Retiro_Tonner.objects.all()

    for retiro in retiros:
        ws.append([
            str(retiro.r_tonner),
            str(retiro.r_persona),
            retiro.cantidad_retirada,
            retiro.caso_GLPI,
            retiro.descripcion,
            retiro.fecha_retiro.strftime('%Y-%m-%d %H:%M:%S')
        ])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=reporte_retiros_tonner.xlsx'
    
    wb.save(response)

    return response

def OFF_SERVER(request):
    titulo = 'Sin conexión'
    return render(request, 'OFF_S/OFF_SERVER.html', {
        'titulo': titulo,
    })

def cerrar_servidor(request):
    os.kill(os.getpid(), signal.SIGTERM)
    return HttpResponse('')

def Lista_T_Pendientes(request):
    pendiente = Toner_M_Recargados.objects.order_by('-fecha_entrega')
    query = request.GET.get('q', '')
    if query:
        items = Toner_M_Recargados.objects.filter(toner__nombre__icontains=query).order_by('-fecha_entrega')
    else:
        items = pendiente  

    combined_items = list(pendiente) + list(set(items) - set(pendiente))

    return render(request, 'carrito/pendientes.html', {
        'items': combined_items,
    })

def Buscar_T_Recargando(request):
    query = request.GET.get('q', '')
    if query:
        items = Toner_M_Recargados.objects.filter(toner__nombre__icontains=query, estado='RECARGANDO').order_by('-fecha_entrega')
    else:
        items = Toner_M_Recargados.objects.all().order_by('-fecha_entrega')
    
    return render(request, 'carrito/pendientes.html', {
        'items': items,
    })
