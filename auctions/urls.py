from django.urls import path
from django.contrib import admin
from . import views
from django.conf import settings


urlpatterns = [
    path ('admin/', admin.site.urls),
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createListing", views.createListing, name="create"),
    path("<int:subasta_id>/ofertar/", views.articleBid, name="articleBid"),
    path("<int:subasta_id>/seguir/", views.trackingList, name="trackingList"),
    path("<int:subasta_id>/eliminar/", views.deleteView, name="deleteView"),
    path("<int:subasta_id>/comentarios/", views.comments, name="comments"),
    path("whatchlist", views.whatchlist, name="whatchlist"),
  
] 