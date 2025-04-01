from .models import SeguimientoSubasta


def seguidos_context(request):
    
    try:
        seguidos = len(SeguimientoSubasta.objects.filter(user_id = request.user, esta_seguido=1)) #Obtener el numero de los articulos que el usuario sigue
    except:
        seguidos = None
    
    return {"seguidos": seguidos}