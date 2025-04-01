from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms
from django.contrib import messages
import json




from . forms import Crear, ComentariosForm, Categoria, OfertaForm

from . models import Subastas, Oferta, SeguimientoSubasta, User, Comentarios, SubastaFinalizada


from .models import User


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
        next_url = request.GET.get('next', 'index')  # Redirige a la página inicial si no hay `next`
        return redirect(next_url)
    else:
        return render(request, "auctions/register.html")
    





def index(request, categoria=None):

    if categoria and categoria != 'todos':
        subastas = Subastas.objects.filter(activa=True, categoria=categoria)
    else:
        subastas = Subastas.objects.filter(activa=True)

   
    
        
    

    form = Categoria(initial={'categoria': categoria or 'todos'})  # Si no hay categoría, usar 'todos'
    
    return render(request, "auctions/index.html", 
                  {
        "form": form,
        "subastas": subastas,
      })


@login_required
def createListing(request):
    
    if request.method == "POST":  #comprueba que se trata de un form 

        form = Crear(request.POST, request.FILES)  # chequea toda la data que se subio en el form y la guarda en la variable form 

        if form.is_valid():
            
            
            subasta = form.save(commit=False) #Guarda una instancia temporal de los datos que se envien al formulario, en el campo del model correspondiente especificado en el form
        
            # Asignar el creador desde el usuario autenticado
            subasta.creador = request.user
            
            # Guardar el objeto completo en la base de datos
            subasta.save()

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
            _articulo.ofertaActual=_oferta
            
            nuevo_oferta.save()
            _articulo.save()

            # Guarda la nueva oferta y ofertante
            ofertaActual = nuevo_oferta.ofertaActual 
            ofertanteActual = nuevo_oferta.ofertanteActual

            return nuevo_oferta
    return None


@login_required
def articleBid(request, subasta_id):
    nuevo_oferta = None
    nuevo_comentario = None
    message = None
    boton = False

    seguidos=SeguimientoSubasta.objects.filter(subasta_id=subasta_id, user=request.user)

    for seguido in seguidos:
        
        if seguido and seguido.esta_seguido==True:
            message= "Remover de la lista de seguimiento"
        else: message = "Añadir a lista de seguimiento"

    ofertaForm = OfertaForm(request.POST)
    if ofertaForm.is_valid():
        ofertaValida = ofertaForm.cleaned_data["oferta"]


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



    # Definir el formulario con la oferta actual + 10
    oferta_form = OfertaForm(request.POST or None, ofertaActual=ofertaActual)

    comentariosList = Comentarios.objects.filter(articulo=articulo).order_by('-id')[:3]

    
    if request.method == "POST":
        if ofertaForm.is_valid():
            ofertaValida = ofertaForm.cleaned_data["oferta"]
            ofertante = request.user

            # Lógica de validación de la oferta
            if ofertaValida >= (ofertaActual + 10):  # Asegúrate de que la oferta sea mayor o igual a ofertaActual + 10
                nuevo_oferta = Oferta(articulo=articulo, ofertaActual=ofertaValida, ofertanteActual=ofertante)
                articulo.ofertaActual = ofertaValida

                # Guarda la nueva oferta y el artículo
                nuevo_oferta.save()
                articulo.save()

                return redirect('articleBid', subasta_id=subasta_id)  # Redirige si la oferta es válida
            else:
                # Si la oferta no es válida, muestra un mensaje de error
                return render(request, "auctions/articleBid.html", {
                    "oferta": ofertaActual,
                    "articulo": articulo,
                    "ofertante": ofertanteActual,
                    "errorMessage": "La oferta debe ser al menos $10 mayor a la anterior.",
                    "boton": boton,
                    "form": form,
                    "ofertaForm": ofertaForm,
                    "comentariosList": comentariosList,
                    "message": message or "Añadir a lista de seguimiento",
                })

    return render(request, "auctions/articleBid.html", {
        "articulo": articulo,
        "oferta": ofertaActual,
        "ofertante": ofertanteActual,
        "message": message if message else "Añadir a lista de seguimiento",
        "boton": boton, 
        "form": form,
        "comentariosList": comentariosList,
        "inicio": articulo.start_time,
        "finalizacion": articulo.end_time,
        "ofertaForm": ofertaForm,  # Asegúrate de pasar el formulario a la plantilla
    })



def trackingList(request, subasta_id):
    nuevo_seguimiento = None
    usuario= request.user #guarde el id del usuario
    subasta = Subastas.objects.get(pk=subasta_id)
     

    if request.method == "POST":

        try:
            seguimiento = SeguimientoSubasta.objects.get(user=usuario, subasta=subasta) #Comprueba si el articulo esta en lista de seguimiento

            if (seguimiento.esta_seguido == True):
                seguimiento.esta_seguido = False
            else:
                seguimiento.esta_seguido = True
            
            seguimiento.save()    
                
        except SeguimientoSubasta.DoesNotExist:

            seguimiento = SeguimientoSubasta(user=usuario, subasta=subasta, esta_seguido=True) #Sino esta, lo crea
            seguimiento.save()

    return redirect('articleBid', subasta_id=subasta_id)
                

def deleteView (request, subasta_id):
    articulo = Subastas.objects.get(pk=subasta_id)
    ofertaActual = Oferta.objects.filter(articulo=articulo).order_by('-ofertaActual').first()
    """oferta = ofertaActual or articulo.ofertaInicial
    ofertanteActual = ofertaActual.ofertanteActual """

    if request.method == "POST":
        
        articulo.activa=False
        articulo.save()
        
    return redirect('articleBid', subasta_id=subasta_id)



def comments(request, subasta_id):
    
    subasta = Subastas.objects.get(pk=subasta_id)
    
    if request.method == "POST":

        form = ComentariosForm(request.POST)
        if form.is_valid():
            comentario = form.cleaned_data["comentarios"]
            nuevo_comentario = Comentarios(nombre=request.user, articulo=subasta, contenido=comentario)
            nuevo_comentario.save()
        return redirect(articleBid, subasta_id=subasta_id)

@login_required
def whatchlist (request):
    seguimientos = SeguimientoSubasta.objects.filter(user=request.user, esta_seguido=True)
    subastas = []
    
    for seguimiento in seguimientos:
        subasta = Subastas.objects.get(pk=seguimiento.subasta_id)
        subastas.append(subasta)
        

    return render(request, "auctions/whatchlist.html", 
    
    

    {"subastas": subastas}
    )


def filterByCategory(request):
    if request.method=="POST":

        eleccionCategoria = request.POST["categoria"]  # chequea la data seleccionada en categoria y la guarda en la variable 
        
        return redirect('indexFiltrado', categoria=eleccionCategoria)


def endBid(request):
    if request.method == "POST":

        try:
            data = json.loads(request.body)
            articuloId = data.get("articuloId")
            subasta = Subastas.objects.get (pk=articuloId) 
            oferta = Oferta.objects.filter(articulo=subasta).order_by('-ofertaActual').first()
            montoFinal = oferta.ofertaActual
            ganador = oferta.ofertanteActual

            if not montoFinal:

                return JsonResponse({"error": "No se encontraron ofertas para esta subasta"}, status=404)


            subasta.activa=False

            subasta.save()

            nuevaSubastaFinalizada = SubastaFinalizada(monto=montoFinal, articulo = subasta, ganador = ganador)
            nuevaSubastaFinalizada.save()
            
            return JsonResponse({"message": "Subasta finalizada"}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Error en el formato del JSON"}, status=400)
        
    return JsonResponse({"error": "Método no permitido"}, status=405)


 
       
            



 
         






      




