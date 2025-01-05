from django import forms
from .models import Subastas



from django import forms
from .models import Subastas

class Crear(forms.ModelForm):
    titulo = forms.CharField(
        label='Título',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'titulo',
            'placeholder': 'Ingresa el título de tu subasta'
        })
    )
    descripcion = forms.CharField(
        label='Descripción',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 6,
            'placeholder': 'Describe el artículo que estás subastando'
        })
    )
    imagen = forms.ImageField(
        label='Seleccionar imagen',
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control',
            'id': 'imagen',
            'placeholder': 'Arrastra tu archivo aquí'
        })
    )
    ofertaInicial = forms.DecimalField(
        label='Oferta Inicial',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa la oferta inicial'
        })
    )
    categoria = forms.ChoiceField(
        label='Categoría',
        choices=[
            ('futbolistas', 'Futbolistas'),
            ('articulosLimpieza', 'Artículos de Limpieza'),
        ],
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )

    class Meta:
        model = Subastas
        fields = ['titulo', 'descripcion', 'imagen', 'ofertaInicial', 'categoria']


class ofertar (forms.Form):
    oferta = forms.DecimalField(min_value=0)

    """def clean_oferta(self):

        oferta = self.cleaned_data.get('oferta')
        if "@" in nombre:
            raise forms.ValidationError("El nombre no puede contener un '@'.")
        return nombre

    <input type="number" id="ofertar" name="ofertar" value="{{ oferta|add:10 }}">
    """



class ComentariosForm(forms.Form):
    comentarios = forms.CharField(
        
        widget=forms.Textarea(attrs={
            'rows': 6,
            'cols': 45,
            'name': 'comentarios',
            'placeholder': "Añadir una opinión"
        })
    )


class Categoria(forms.Form):
    categoria = forms.ChoiceField(
        choices=[
            ('todos', 'Todos los Articulos'),
            ('futbolistas', 'Futbolistas'),
            ('articulosLimpieza', 'Artículos de Limpieza'),
        ],
        widget=forms.Select
    )


        
    
    