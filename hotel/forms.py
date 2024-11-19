from django import forms
from .models import Client

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = [
            'email', 
            'telephone', 
            'etat', 
            'lieu', 
            'standing', 
            'date_debut_sejour', 
            'date_fin_sejour', 
            'photo'
        ]
