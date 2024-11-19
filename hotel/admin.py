from django.contrib import admin
from .models import Chambre , Reservation , Client , Activite
admin.site.register(Chambre)
admin.site.register(Reservation)
admin.site.register(Client)
admin.site.register(Activite)