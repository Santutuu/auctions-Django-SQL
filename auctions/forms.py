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

    def clean_titulo(self):
        titulo = self.cleaned_data.get("titulo")
        return titulo.capitalize() if titulo else titulo

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
            ('Accesorios', 'Accesorios y joyas'),
        ],
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )

    class Meta:
        model = Subastas
        fields = ['titulo', 'descripcion', 'imagen', 'ofertaInicial', 'categoria']


class OfertaForm(forms.Form):
    oferta = forms.IntegerField(min_value=0, label='', required=False,
        widget=forms.NumberInput(attrs={
            'id': 'ofertar',
        })
    )

    def __init__(self, *args, **kwargs):
        # Recibe el valor de oferta_actual desde la vista
        ofertaActual = kwargs.pop('ofertaActual', 0)  
        super().__init__(*args, **kwargs)
        # Establece la oferta actual + 10 como valor inicial
        self.fields['oferta'].initial = ofertaActual + 10  

    def clean_oferta(self):
        oferta = self.cleaned_data.get('oferta')
        
        return oferta  # Asegúrate de devolver el valor correctamente
      


    """

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


        
    
    