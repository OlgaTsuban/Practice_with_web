#from django.forms import ModelForm, HiddenInput, ModelChoiceField
from django.forms import ModelForm, CharField, Form, TextInput, BooleanField 

from .models import Author


class AuthorForm(ModelForm):
    fullname = CharField(max_length=100, min_length=3,
            widget=TextInput(attrs={"class": "form-control", "id": "exampleInputEmail1"}))
    born_date = CharField(widget=TextInput(attrs={"class": "form-control", "id": "exampleInputEmail"}))
    born_location = CharField(max_length=255, widget=TextInput(attrs={"class": "form-control", "id": "exampleInputLocation"}))
    description = CharField(widget=TextInput(attrs={"class": "form-control", "id": "exampleInputDescription"}))
    class Meta:
        model = Author
        fields = ['fullname', 'born_date', 'born_location', 'description']


class ScrapeDataForm(Form):
    scrape_button = BooleanField(label='Scrape Data', required=False)