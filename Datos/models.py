from django.db import models, transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError

## USUARIO ⬇ ---------------------------------------------------------------------------------------------
class Area(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.nombre

    def clean(self):
        if Area.objects.filter(nombre=self.nombre).exclude(pk=self.pk).exists():
            raise ValidationError('Ya existe un área con este nombre.')
    
    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper()   
        super(Area, self).save(*args, **kwargs)

class Persona(models.Model):
    nombre = models.CharField(max_length=100)
    firma = models.ImageField(upload_to='firmas/')
    area = models.ForeignKey(Area, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__( self ):
        return self.nombre

    def clean(self):
        if Persona.objects.filter(nombre=self.nombre, area=self.area).exclude(pk=self.pk).exists():
            raise ValidationError('Ya existe una persona con este nombre en esta área.')

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper()   
        super(Persona, self).save(*args, **kwargs)
## USUARIO ⬆ ---------------------------------------------------------------------------------------------

## TONER ⬇ ---------------------------------------------------------------------------------------------
class Tonner(models.Model):
    ESTADO_T = [
        ('Disponible', 'Disponible'),
    
    ]


    nombre = models.CharField(max_length=50)
    cantidad = models.PositiveBigIntegerField()
    Numero_Toner = models.CharField(max_length=20)
    Estado = models.CharField(max_length=10, choices=ESTADO_T, default='Disponible')
    imagen = models.ImageField()
    
    def __str__(self):
        return f"{self.nombre}"


    def is_libre(self):
        return self.Estado == 'Disponible'
    
    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper()   
        super(Tonner, self).save(*args, **kwargs)



class Retiro_Tonner(models.Model):
    r_tonner = models.ForeignKey(Tonner, on_delete=models.SET_NULL, null=True, blank=True)
    r_persona = models.ForeignKey(Persona, on_delete=models.PROTECT, null=False, blank=False)
    cantidad_disponible = models.PositiveIntegerField(default=1)  
    cantidad_retirada = models.PositiveIntegerField(default=1)
    caso_GLPI = models.CharField(max_length=100, default='En Espera')
    descripcion = models.TextField(max_length=500, default='Sin descripción')
    fecha_retiro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.r_persona} - {self.r_tonner}"
    



## TONER ⬆ ---------------------------------------------------------------------------------------------

## RECARGA DE TONER ⬇ ------------------------------------------------------------------------------------

class Recargar_Toner(models.Model):
    toner = models.ForeignKey(Tonner, on_delete=models.SET_NULL, null=True, blank=True)
    cantidad_Recargar = models.PositiveIntegerField()
    fecha_Recarga = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.toner} - Recargando"
    
## RECARGA DE TONER ⬆ ------------------------------------------------------------------------------------


## TABLA TONER OFICINA PRINCIPAL IBAGUE ⬇ ---------------------------------------------------------------------------------------------

class Tabla_T_Toners(models.Model):
    MARCA_I = [
        ('N/A','N/A'),
        ('HP','HP'),
        ('SAMSUNG','SAMSUNG'),
        ('KYOSERA','KYOSERA'),
        ('EPSON','EPSON'),
    ]

    T_TONER = [
        ('105A','105A'),
        ('30A','30A'),
        ('83A','83A'),
        ('136A','136A'),
        ('175A','175A'),
        ('17A','17A'),
        ('19A','19A'),
        ('85A','85A'),
        ('226A','226A'),
        ('D1015','D1015'),
        ('TINTA','TINTA'),
        ('N/A','N/A'),
    ]

    oficina = models.CharField(max_length=50)
    activo = models.CharField(max_length=30)
    numero_impresoras = models.PositiveIntegerField()
    referencia = models.CharField(max_length=100)
    marca = models.CharField(max_length=7, choices=MARCA_I, default='N/A')
    toner_de_impresora = models.CharField(max_length=5, choices=T_TONER, default='N/A')
    otro_toner = models.CharField(max_length=5, choices=T_TONER, default='N/A')
    cantidad_toner = models.PositiveBigIntegerField()

    def __str__(self) -> str:
        return f"{self.oficina} {self.marca}"
    
    def clean(self):
        if Tabla_T_Toners.objects.filter(oficina=self.oficina, activo=self.activo).exclude(pk=self.pk).exists():
            raise ValidationError('Ya existe se encuentra registrada')
        
    def save(self, *args, **kwargs):
        self.oficina = self.oficina.upper()   
        super(Tabla_T_Toners, self).save(*args, **kwargs)

    
## TABLA TONER OFICINA PRINCIPAL IBAGUE ⬆ ---------------------------------------------------------------------------------------------


## TABLA TONER MUNICIPIOS ⬇ ---------------------------------------------------------------------------------------------

class Tabla_T_Toners_Municipios(models.Model):
    MARCA_I = [
        ('N/A','N/A'),
        ('HP','HP'),
        ('SAMSUNG','SAMSUNG'),
        ('KYOSERA','KYOSERA'),
        ('EPSON','EPSON'),
    ]

    T_TONER = [
        ('105A','105A'),
        ('30A','30A'),
        ('83A','83A'),
        ('136A','136A'),
        ('175A','175A'),
        ('17A','17A'),
        ('19A','19A'),
        ('85A','85A'),
        ('226A','226A'),
        ('D1015','D1015'),
        ('MLT-D1018','MLT-D1018'),
        ('101S','101S'),
        ('TINTA','TINTA'),
        ('N/A','N/A'),
    ]

    Y_N = [
        ('SI','SI'),
        ('NO','NO'),
        ('REGISTRAR','REGISTRAR'),
    ]
    
    ZONA = [
        ('SIN DEFINIR', 'SIN DEFINIR'),
        ('SUR', 'SUR'),
        ('NORTE', 'NORTE'),
        ('ALEDAÑOS', 'ALEDAÑOS'),
    ]

    oficina = models.CharField(max_length=50)
    activo = models.CharField(max_length=30)
    numero_impresoras = models.PositiveIntegerField()
    referencia = models.CharField(max_length=100)
    marca = models.CharField(max_length=7, choices=MARCA_I, default='N/A')
    toner_de_impresora = models.CharField(max_length=9, choices=T_TONER, default='N/A')
    otro_toner = models.CharField(max_length=9, choices=T_TONER, default='N/A')
    cantidad_toner = models.PositiveBigIntegerField()
    comprobado = models.CharField(max_length=9, choices=Y_N, default='SI')
    zona = models.CharField(max_length=11, choices=ZONA, default='SIN DEFINIR')

    def __str__(self) -> str:
        return f"{self.oficina} - {self.marca}"
    
    def clean(self):
        if Tabla_T_Toners_Municipios.objects.filter(oficina=self.oficina, activo=self.activo).exclude(pk=self.pk).exists():
            raise ValidationError('Ya existe se encuentra registrada')
        
    def save(self, *args, **kwargs):
        self.oficina = self.oficina.upper()   
        super(Tabla_T_Toners_Municipios, self).save(*args, **kwargs)

## TABLA TONER MUNICIPIOS ⬆ ---------------------------------------------------------------------------------------------

##AÑADIR LOS TONER QUE ESTABAN EN RECARGANDO
class Toner_M_Recargados(models.Model):
    ESTADO = [
        ('ENTREGADO','ENTREGADO'),
        ('RECARGANDO','RECARGANDO'),
        ]
    toner = models.ForeignKey(Tonner, on_delete=models.SET_NULL, null=True, blank=True)
    cantidad = models.PositiveIntegerField()
    estado = models.CharField(max_length=10, choices=ESTADO, default='RECARGANDO')
    fecha_entrega = models.DateTimeField(auto_now_add=True, null=False)
    fecha_recibido = models.DateTimeField(null=True)

    def __str__(self) -> str:
        return f"se añade {self.cantidad} a el Toner {self.toner}"
    
@receiver(post_save, sender=Toner_M_Recargados)
def actualizar_estado_toner(sender, instance, created, **kwargs):
    if instance.estado == 'ENTREGADO':
        toner = instance.toner
        toner.cantidad += instance.cantidad
        toner.save()
##AÑADIR LOS TONER QUE ESTABAN EN RECARGANDO