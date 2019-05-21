from django import forms
from django.forms import SelectDateWidget

from .models import Menu, Item, Ingredient

class MenuForm(forms.ModelForm):

    class Meta:
        model = Menu
        exclude = ('created_date',)