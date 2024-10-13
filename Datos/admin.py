from django.contrib import admin
from .models import Tonner, Persona, Area, Retiro_Tonner,Tabla_T_Toners,Tabla_T_Toners_Municipios, Toner_M_Recargados

admin.site.register(Tonner)
admin.site.register(Persona)
admin.site.register(Area)
admin.site.register(Retiro_Tonner)
admin.site.register(Tabla_T_Toners)
admin.site.register(Tabla_T_Toners_Municipios)
admin.site.register(Toner_M_Recargados)

# Register your models here.
