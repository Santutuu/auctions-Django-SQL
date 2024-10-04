from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms


from . forms import Crear
import time
from . models import Subastas, Oferta   


from .models import User


def index(request):

    subastas = Subastas.objects.all()

    return render(request, "auctions/index.html", 
                  {
        "subastas": subastas
      })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def createListing(request):
    
    if request.method == "POST":  #comprueba que se trata de un form 

        form = Crear(request.POST)  # chequea toda la data que se subio en el form y la guarda en la variable form 

        if form.is_valid():
            titulo = form.cleaned_data["titulo"]     #accede y guarda a la variable titulo dentro del form
            descripcion = form.cleaned_data["descripcion"] 
            imagen = form.cleaned_data["imagen"] 
            oferta = form.cleaned_data["ofertaInicial"] 
            
            nuevo_subasta = Subastas(titulo=titulo, descripcion=descripcion, imagen=imagen, ofertaInicial=oferta)
            nuevo_subasta.save()

            return redirect('index')
        
        else:
            return render(request, "auctions/createListing.html",  #si hay un error, se renferiza el archivo de nuevo con los errores 
                          {"form": form 
                           })

    else:

        form = Crear() 

        
   

    return render (request, "auctions/createListing.html",
                   {"form": form})
    

def articleBid(request, subasta_id):

    nuevo_oferta=None
    
    articulo = Subastas.objects.get(pk=subasta_id)
    
    oferta = Oferta.objects.filter(articulo=articulo).order_by('-ofertaActual').first()


    if oferta:
        ofertaActual = oferta.ofertaActual
        ofertanteActual = oferta.ofertanteActual
    else:
        ofertaActual = articulo.ofertaInicial
        ofertanteActual = "No hay ofertas"

    if request.method == "POST":
        oferta = int (request.POST["ofertar"])
        ofertante = request.user
        
        
        if oferta >= (ofertaActual + 10):
            
            nuevo_oferta = Oferta(articulo=articulo, ofertaActual=oferta , ofertanteActual=ofertante )
            nuevo_oferta.save()

            ofertaActual = nuevo_oferta.ofertaActual
            ofertanteActual = nuevo_oferta.ofertanteActual
            
            
        else:

            return render (request, "auctions/articleBid.html", {
            "oferta": ofertaActual,
            "articulo": articulo,
            "ofertante": ofertanteActual,
            "message": "La nueva oferta debe ser al menos 10$ mayor que la anterior"
 })


    return render(request, "auctions/articleBid.html", {

        "articulo": articulo,
        "oferta": ofertaActual,
        "ofertante": ofertanteActual
        
})
    


"""problemas //

como accedo al id del usuario"""


      




