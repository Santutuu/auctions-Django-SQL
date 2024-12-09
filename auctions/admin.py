from django.contrib import admin
from .models import User, Subastas, Oferta, Comentarios

# Register your models here.

admin.site.register(User)
admin.site.register(Subastas)
admin.site.register(Oferta)
admin.site.register(Comentarios)


