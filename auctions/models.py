from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=50)
    

    
class Subastas(models.Model):
    
    titulo = models.CharField (max_length=50)
    descripcion = models.CharField (max_length=300)
    imagen = models.CharField(max_length=70, null=True)
    ofertaInicial =  models.IntegerField()
    

    def __str__(self):
        return f"{self.titulo} || oferta inicial: {self.ofertaInicial}::{self.descripcion}"
    

class Oferta(models.Model):
    
   
    articulo = models.ForeignKey(Subastas, on_delete=models.CASCADE, related_name="articulo")
    ofertaActual = models.IntegerField()

    ofertanteActual = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ofertante")

    

    def __str__(self):
        return f"Articulo: {self.articulo} || oferta actual: {self.ofertaActual}. Ofertante: {self.ofertanteActual}"

   
