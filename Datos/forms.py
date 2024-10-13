from typing import Any
from django import forms
from .models import Area, Persona, Tonner, Retiro_Tonner, Tabla_T_Toners, Tabla_T_Toners_Municipios, Recargar_Toner
import base64
from django.core.files.base import ContentFile

class FormArea(forms.ModelForm):
    class Meta:
        model = Area
        fields = '__all__'

class FormPersona(forms.ModelForm):
    firma_imagen = forms.CharField(widget=forms.HiddenInput(), required=False)
    class Meta:
        model = Persona
        fields = ['nombre', 'area', 'firma_imagen']

    def save(self, commit=True):
        persona = super().save(commit=False)
        firma_imagen = self.cleaned_data.get('firma_imagen')

        if firma_imagen:
            format, imgstr = firma_imagen.split(';base64,')
            ext = format.split('/')[-1]
            persona.firma.save(f'firma_{persona.nombre}.{ext}', ContentFile(base64.b64decode(imgstr)), save=False)

        if commit:
            persona.save()

        return persona
    

class FormTonner(forms.ModelForm):
    class Meta:
        model = Tonner
        fields = '__all__'

class FormsRetiroTonner(forms.ModelForm):
    class Meta:
        model = Retiro_Tonner
        fields = ['r_persona', 'cantidad_retirada', 'caso_GLPI', 'descripcion']

class FormsTabla_Toners(forms.ModelForm):
    class Meta:
        model = Tabla_T_Toners
        fields = '__all__'

class FormsTabla_Toners_Municipios(forms.ModelForm):
    class Meta:
        model = Tabla_T_Toners_Municipios
        fields = '__all__'

class formsRecargando(forms.ModelForm):
    class Meta:
        model = Recargar_Toner
        fields = '__all__'

        