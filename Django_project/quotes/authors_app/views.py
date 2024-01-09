# Create your views here.
from rest_framework import viewsets
from .models import Author
from .serializers import AuthorSerializer

from .utils import scrape_data
from django.core.paginator import Paginator
from .forms import AuthorForm, ScrapeDataForm
from quotes_app.forms import Quote
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

# --------------------------- ---------------------------
# ---------------------------add a new author ---------------------------
@login_required
def add_author(request):
    print("View is being executed!")
    if request.method == 'POST':
        print(request.POST)
        form = AuthorForm( request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='authors_app:add_author')  # Replace with the actual success URL
    else:
        form = AuthorForm()
    return render(request, 'authors_app/add_author.html', context={"form": form})


# --------------------------- ---------------------------
# ---------------------------show on page all authors ---------------------------
def all_authors(request):
    author = Author.objects.all()
    paginator = Paginator(author, 10)  # Show 10 quotes per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'authors_app/all_authors.html', {'page_obj': page_obj})

# --------------------------- ---------------------------
# ---------------------------work with parcing the data and write to json ---------
def scrape_data_view(request):
    if request.method == 'POST':
        form = ScrapeDataForm(request.POST)
        if form.is_valid() and form.cleaned_data['scrape_button']:
            # Виклик функції для скрапінгу даних
            scrape_data()
            return render(request, 'authors_app/success_page.html')
    # Відображення форми на сторінці
    form = ScrapeDataForm()
    return render(request, 'authors_app/scrape_data_page.html', {'form': form})