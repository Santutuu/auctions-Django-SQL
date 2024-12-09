from django import forms
from .models import Subastas



class Crear(forms.ModelForm):
     
    titulo = forms.CharField(
        label='Título',
        widget=forms.TextInput(attrs={
            'class': 'publicacion',
            'id': 'titulo'
        })
    )
    
    descripcion = forms.CharField(
        label='Descripción',
        widget=forms.Textarea(attrs={
            'rows': 6,
            'cols': 50,
            'name': 'descripcion'
        })
    )
    
    imagen = forms.ImageField(
        label='Seleccionar imagen',
        widget=forms.ClearableFileInput(attrs={
            'class': 'publicacion',
            'id': 'imagen',
            'placeholder': 'Arrastra tu archivo aqui',
            'name': 'imagen'
        })
    )
    
    ofertaInicial = forms.DecimalField(
        label='Oferta Inicial',
        
        widget=forms.NumberInput(attrs={
            'class': 'publicacion',
            'name': 'ofertaInicial'
        })
    )

    categoria = forms.ChoiceField(
        choices=[
            ('futbolistas', 'Futbolistas'),
            ('articulosLimpieza', 'Artículos de Limpieza'),
        ],
        widget=forms.Select
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


        
    
    