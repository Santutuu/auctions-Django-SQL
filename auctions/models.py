from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=50)
    
    listaSeguimiento = models.ManyToManyField('Subastas', through='SeguimientoSubasta')
    

    
class Subastas(models.Model):
    
    titulo = models.CharField (max_length=50)
    descripcion = models.CharField (max_length=300)
    imagen = models.ImageField(null=True, upload_to='subastas/')
    ofertaInicial =  models.IntegerField()
    creador = models.ForeignKey (User, on_delete=models.CASCADE, related_name="usuario", default=1)
    activa =  models.BooleanField(default=True)

    def __str__(self):
        return f"{self.titulo} || oferta inicial: {self.ofertaInicial}::{self.descripcion}"
    


class Comentarios(models.Model):

    nombre= models.ForeignKey(User, on_delete=models.DO_NOTHING)
    articulo=models.ForeignKey(Subastas, on_delete=models.CASCADE)
    contenido=models.CharField(max_length=300)

class SeguimientoSubasta(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subasta = models.ForeignKey(Subastas, on_delete=models.CASCADE)
    esta_seguido = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'subasta')

class Oferta(models.Model):
    articulo = models.ForeignKey(Subastas, on_delete=models.CASCADE, related_name="articulo")
    ofertaActual = models.IntegerField()
    ofertanteActual = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ofertante")

  

    def __str__(self):
        return f"Articulo: {self.articulo} || oferta actual: {self.ofertaActual}. Ofertante: {self.ofertanteActual}"





   
