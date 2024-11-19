from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('', views.home, name='home'),  # Page d'accueil générale
    path('clients/', views.client_list, name='client_list'),  # Liste des clients
    path('reservations/', views.reservation_list, name='reservation_list'),  # Liste des réservations
    path('chambres/', views.chambre_list, name='chambre_list'),
    path('activites/', views.activites ,name = 'activites') , # Liste des chambres
    path('ajouter_client/', views.ajouter_client, name='ajouter_client'),
    path('changer_lieu/<int:client_id>/', views.changer_lieu_client, name='changer_lieu_client'),
  
   
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)