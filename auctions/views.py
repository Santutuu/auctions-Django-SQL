from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms
from django.contrib import messages

from . forms import Crear, ComentariosForm

from . models import Subastas, Oferta, SeguimientoSubasta, User, Comentarios


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
            titulo = form.cleaned_data["titulo"]    
            descripcion = form.cleaned_data["descripcion"] 
            imagen = form.cleaned_data["imagen"] 
            oferta = form.cleaned_data["ofertaInicial"] 
            
            nuevo_subasta = Subastas(titulo=titulo, descripcion=descripcion, imagen=imagen, ofertaInicial=oferta, creador=request.user)
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
    



def bidLogic(_articulo, _ofertante, _oferta, _ofertaActual):

    if _oferta >= (_ofertaActual + 10):
            nuevo_oferta = Oferta(articulo=_articulo, ofertaActual=_oferta, ofertanteActual=_ofertante)
            nuevo_oferta.save()

            # Guarda la nueva oferta y ofertante
            ofertaActual = nuevo_oferta.ofertaActual 
            ofertanteActual = nuevo_oferta.ofertanteActual

            return nuevo_oferta
    return None



def articleBid(request, subasta_id):
    nuevo_oferta = None
    nuevo_comentario = None
    boton = False
    message = None  # Inicializar message

    # Manejar mensajes flash
    if messages.get_messages(request):
        for msg in messages.get_messages(request):
            message = msg  # Sobrescribir el mensaje por defecto si hay uno flash

    form = ComentariosForm(request.POST)

    articulo = Subastas.objects.get(pk=subasta_id)
    oferta = Oferta.objects.filter(articulo=articulo).order_by('-ofertaActual').first()  # Busca la oferta más reciente

    if articulo.creador == request.user:
        boton = True

    if oferta:
        ofertaActual = oferta.ofertaActual
        ofertanteActual = oferta.ofertanteActual
    else:
        ofertaActual = articulo.ofertaInicial
        ofertanteActual = "No hay ofertas"

     # Obtener todos los comentarios relacionados con la subasta
    comentariosList = Comentarios.objects.filter(articulo=articulo)[:3]

    if request.method == "POST":
        
        oferta = int(request.POST["ofertar"])  # Obtiene el valor ofertado
        ofertante = request.user
        
        if bidLogic(articulo, request.user, oferta, ofertaActual): # valida que la oferta sea 10$ >
            return redirect('articleBid', subasta_id=subasta_id)  # Redirige a la misma página

        else: 
            #muestra mensaje de error
            return render(request, "auctions/articleBid.html", {
                "oferta": ofertaActual,
                "articulo": articulo,
                "ofertante": ofertanteActual,
                "errorMessage": "La oferta debe ser al menos $10 mayor a la anterior.",
                "boton": boton,
                "form": form,
                "comentariosList": comentariosList
            })


    return render(request, "auctions/articleBid.html", {
        "articulo": articulo,
        "oferta": ofertaActual,
        "ofertante": ofertanteActual,
        "message": message if message else "Añadir a lista de seguimiento",
        "boton": boton, 
        "form": form,
        "comentariosList": comentariosList
    })


def comments(request, subasta_id):
    
    subasta = Subastas.objects.get(pk=subasta_id)
    
    if request.method == "POST":

        form = ComentariosForm(request.POST)
        if form.is_valid():
            comentario = form.cleaned_data["comentarios"]
            nuevo_comentario = Comentarios(nombre=request.user, articulo=subasta, contenido=comentario)
            nuevo_comentario.save()
        return redirect(articleBid, subasta_id=subasta_id)

            


def trackingList(request, subasta_id):
    nuevo_seguimiento = None
    usuario= request.user #guarde el id del usuario
    subasta = Subastas.objects.get(pk=subasta_id)

    if request.method == "POST":

        try:
            seguimiento = SeguimientoSubasta.objects.get(user=usuario, subasta=subasta) #Comprueba si el articulo esta en lista de seguimiento

            
            if (seguimiento.esta_seguido == True):
                message = "Remover de lista de seguimiento"
                seguimiento.esta_seguido = False
                messages.info(request, message)

            else:

                message = "Añadir a lista de seguimiento" 
                seguimiento.esta_seguido = True
            
            seguimiento.save()    
            messages.info(request, message) #Enviar el mensaje flash
                
        except SeguimientoSubasta.DoesNotExist:

            seguimiento = SeguimientoSubasta(user=usuario, subasta=subasta, esta_seguido=True) #Sino esta, lo crea
            seguimiento.save()
            messages.info(request, "Remover de la lista de segumiento")
            


    return redirect('articleBid', subasta_id=subasta_id)

        


def deleteView (request, subasta_id):
     

     
     articulo = Subastas.objects.get(pk=subasta_id)
     if request.method == "POST":
        articulo.delete()
        return redirect('index')
     
     return redirect('articleBid', subasta_id=subasta_id)


def whatchlist (request):
    seguimientos = SeguimientoSubasta.objects.filter(user=request.user, esta_seguido=True)
    subastas = []
    
    for seguimiento in seguimientos:
        subasta = Subastas.objects.get(pk=seguimiento.subasta_id)
        subastas.append(subasta)
        

    return render(request, "auctions/whatchlist.html", 
    
    {"subastas": subastas}
    )


   

 
       
            



     

         






      




