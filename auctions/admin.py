from django.contrib import admin
from .models import User, Subastas, Oferta

# Register your models here.

admin.site.register(User)
admin.site.register(Subastas)
admin.site.register(Oferta)
