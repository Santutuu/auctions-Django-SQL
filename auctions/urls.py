from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createListing", views.createListing, name="create"),
    path("<int:subasta_id>/ofertar/", views.articleBid, name="articleBid"),
    path("<int:subasta_id>/eliminar/", views.trackingList, name="trackingList"),
    path("<int:subasta_id>/seguir/", views.deleteView, name="deleteView")
]
