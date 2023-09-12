# accounts/forms.py
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Card

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','first_name','email','password1','password2',]


class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['card_type',
                  'job_name', # czy szuka pracownika/pracownikow czy pracy
                  'work_type', # czy kwota ma byc za godzine czy za cale zlecenie
                  'needed_workers',
                  'rate',
                  'currency',
                  'experiences', # ile wymaga pracownikow jesli szuka pracownikow
                  'skills', # umiejetnosci
                  'description'] # doswiadczenia
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'instance' in kwargs and kwargs['instance'].card_type == 'looking_for_worker':
            self.fields['job_name'].required = True
        else:
            del self.fields['needed_workers']