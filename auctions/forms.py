from django import forms


class Crear(forms.Form):
     
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
    
    imagen = forms.URLField(
        label='URL de la Imagen',
        widget=forms.TextInput(attrs={
            'class': 'publicacion',
            'id': 'imagen',
            'placeholder': 'https://example.com/imagen.jpg',
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

    




     