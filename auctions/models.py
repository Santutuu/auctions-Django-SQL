from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now
from datetime import timedelta


class User(AbstractUser):
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=50)
    
    listaSeguimiento = models.ManyToManyField('Subastas', through='SeguimientoSubasta')
    

    
class Subastas(models.Model):

    CATEGORIAS = [
        ('futbolistas', 'Futbolistas'),
        ('articulosLimpieza', 'Artículos de Limpieza'),
        ('Accesorios', 'Accesorios y joyas')
        
        
    ]
    
    titulo = models.CharField (max_length=50)
    descripcion = models.CharField (max_length=300)
    imagen = models.ImageField(null=True, upload_to='subastas/')
    ofertaInicial =  models.IntegerField()
    creador = models.ForeignKey (User, on_delete=models.CASCADE, related_name="usuario", default=1)
    activa =  models.BooleanField(default=True)
    ofertaActual= models.IntegerField(default=0)
    categoria = models.CharField(max_length=50, choices=CATEGORIAS, default='futbolistas')
    start_time = models.DateTimeField(default=now)
    
    
    def default_end_time():
        return now() + timedelta(days=1)

    end_time = models.DateTimeField(default=default_end_time)
    def __str__(self):
        return f"{self.titulo} || oferta inicial: {self.ofertaInicial}::{self.descripcion}"
    
class SubastaFinalizada(models.Model):
    articulo = models.ForeignKey(Subastas, on_delete=models.DO_NOTHING)
    ganador = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    monto = models.IntegerField()
    fechaFinalizacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Subasta {self.subasta.id} - {self.ganador.username}"


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





   
