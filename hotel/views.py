from django.shortcuts import render , redirect , get_object_or_404
from .models import Chambre , Reservation , Client , Activite
from django.shortcuts import render
from datetime import datetime

from django.shortcuts import render
from datetime import datetime
from .models import Chambre

from django.shortcuts import render
from datetime import datetime
from .models import Chambre
from .forms import ClientForm

from django.shortcuts import render
from .models import Chambre, Reservation

def chambre_list(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if not start_date or not end_date:
        start_date = '2024-01-01'  # Valeur par défaut
        end_date = '2024-01-07'    # Valeur par défaut

    # Filtrer les chambres disponibles sans utiliser `reservation_set`
    chambres = Chambre.objects.exclude(
        reservations__date_fin_sejour__gte=start_date,
        reservations__date_debut_sejour__lte=end_date
    )

    return render(request, 'hotel/chambre_list.html', {
        'chambres': chambres,
        'start_date': start_date,
        'end_date': end_date,
    })

def reservation_list(request):
    reservations =Reservation.objects.all()
    return render(request,'hotel/reservation_list.html',{'reservations':reservations})
# Create your views here.
def client_list(request):
   clients =Client.objects.all()
   return render(request,'hotel/client_list.html',{'clients':clients})
def activites(request):
    activites = Activite.objects.all()
    return render(request, 'hotel/activites.html', {"activites":activites})

def home(request):
    return render(request, 'hotel/home.html')
def ajouter_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('client_list')  # Redirige vers la liste des clients
    else:
        form = ClientForm()
    return render(request, 'ajouter_client.html', {'form': form})
def changer_lieu_client(request, client_id):
    client = get_object_or_404(Client, id_personne=client_id)
    if request.method == 'POST':
        lieu = request.POST.get('lieu')  
        if lieu in dict(Client.LIEUX):  # Vérifie si le lieu est valide
            client.lieu = lieu
            client.changer_etat_selon_lieu()
            return redirect('client_list')  
    return render(request, 'hotel/changer_lieu_client.html', {'client': client})