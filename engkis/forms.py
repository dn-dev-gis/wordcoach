from django.forms import ModelForm
from .models import Word
from django import forms

class AddForm(ModelForm):
    class Meta:
        model = Word
        fields = ['english','kiswahili']

class CheckForm(forms.Form):
    inputword = forms.CharField(label='', max_length=150)
