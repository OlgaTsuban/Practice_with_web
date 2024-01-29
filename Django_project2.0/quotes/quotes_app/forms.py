# forms.py in quotes_app
from django import forms
from .models import Quote, Tag
from authors_app.models import Author

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={"class": "form-control", "id": "exampleInputTag"}),
        }


class QuoteForm(forms.ModelForm):
    author = forms.ModelChoiceField(queryset=Author.objects.all(), widget=forms.Select(attrs={"class": "form-control", "id": "exampleInputAuthor"}))
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), widget=forms.SelectMultiple(attrs={"class": "form-control", "id": "exampleInputTags"}))
    quote = forms.CharField(max_length=255, widget=forms.TextInput(attrs={"class": "form-control", "id": "exampleInputQuote"}))
    class Meta:
        model = Quote
        fields = ['author', 'tags', 'quote']
