from django.db import models

from django.db import models
from django.utils.timezone import now

class Chambre(models.Model):
    id_chambre = models.AutoField(primary_key=True)
    id_occupant = models.ForeignKey(
        'Client',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="occupations"
    )
    disponibilite = models.BooleanField(default=True)
    STANDINGS = [
        ('Standard', 'Standard'),
        ('Deluxe', 'Deluxe'),
    ]
    standing = models.CharField(max_length=20, choices=STANDINGS)

    def is_available(self, start_date, end_date):
        # On verifie  si une réservation a chevaucher  la période donnée
        reservations = self.reservation_set.filter(
            date_fin__gte=start_date,
            date_debut__lte=end_date
        )
        return not reservations.exists()

    def occupation(self):
        self.disponibilite = False
        self.save()

    def get_occupant(self):
        return self.id_occupant

    def __str__(self):
        return f"Chambre {self.id_chambre} ({self.standing})"


class Client(models.Model):
    ETATS = [
        ('fatigué', 'Fatigué'),
        ('faim', 'Faim'),
        ('stressé', 'Stressé'),
        ('énergie', 'Énergie'),
        ('détendu', 'Détendu'),
    ]

    LIEUX = [
        ('piscine', 'Piscine'),
        ('jacuzzi', 'Jacuzzi'),
        ('salle de sport', 'Salle de Sport'),
        ('discothèque', 'Discothèque'),
        ('plage', 'Plage'),
        ('restaurant', 'Restaurant'),
        ('chambre', 'Chambre'),
    ]

    id_personne = models.AutoField(primary_key=True)
    email = models.CharField(max_length=150)
    telephone = models.BigIntegerField()
    etat = models.CharField(max_length=50, choices=ETATS, default='fatigué')
    lieu = models.CharField(max_length=100, choices=LIEUX, default='chambre')
    standing = models.CharField(max_length=50)
    date_fin_sejour = models.DateField()
    date_debut_sejour = models.DateField()
    photo = models.ImageField(upload_to='clients_photos/', blank=True, null=True)

    def changer_etat_selon_lieu(self):
        """
        Change l'état du client en fonction du lieu visité.
        """
        etats_par_lieu = {
            'piscine': 'détendu',
            'jacuzzi': 'détendu',
            'salle de sport': 'énergie',
            'discothèque': 'fatigué',
            'plage': 'détendu',
            'restaurant': 'faim',
            'chambre': 'fatigué',
        }

        self.etat = etats_par_lieu.get(self.lieu, 'fatigué')  # Par défaut 'fatigué' si lieu inconnu
        self.save()


    def get_chambre(self):
        reservation = Reservation.objects.filter(personne=self).first()
        if reservation:
            return reservation.chambre
        return None

    def change_lieu(self, lieu):
        LIEUX = ["piscine", "jacuzzi", "salle de sport", "discothèque", "plage", "restaurant", "chambre"]
        if lieu in LIEUX:
            self.lieu = lieu
            self.save()
        else:
            print("Cette localisation n'est pas dans l'hôtel")

    def prolonger_sejour(self, date_fin):
        chambre = self.get_chambre()
        if chambre and chambre.is_available(self.date_debut_sejour, date_fin):
            self.date_fin_sejour = date_fin
            self.save()
        else:
            print("La chambre n'est pas disponible")

    def change_standing(self, standing):
        STANDINGS = ["Deluxe", "Standard"]
        if standing in STANDINGS:
            self.standing = standing
            self.save()
        else:
            print("Nous n'avons pas ce type de chambre dans notre hôtel")

    def __str__(self):
        return f"Client {self.id_personne} - {self.email}"


class Reservation(models.Model):
    chambre = models.ForeignKey(
        Chambre,
        on_delete=models.CASCADE,
        related_name='reservations'
    )
    personne = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='reservations'
    )
    date_debut_sejour = models.DateField()
    date_fin_sejour = models.DateField()

    def reserver(self, debut, fin, standing):
        chambre = Chambre.objects.filter(
            disponibilite=True,
            standing=standing
        ).exclude(
            reservations__date_fin__gte=debut,
            reservations__date_debut__lte=fin
        ).first()

        if chambre:
            self.chambre = chambre
            self.date_debut_sejour = debut
            self.date_fin_sejour = fin
            self.save()
            chambre.occupation()
            print("Réservation réussie !")
        else:
            print("Aucune chambre disponible")
class Activite(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='activites/', blank=True, null=True)  # Champ pour l'image

    def __str__(self):
        return self.nom