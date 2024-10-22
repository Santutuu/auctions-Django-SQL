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


class ofertar (forms.Form):
    oferta = forms.DecimalField(min_value=0)

    """def clean_oferta(self):

        oferta = self.cleaned_data.get('oferta')
        if "@" in nombre:
            raise forms.ValidationError("El nombre no puede contener un '@'.")
        return nombre

    <input type="number" id="ofertar" name="ofertar" value="{{ oferta|add:10 }}">
    """






    




     