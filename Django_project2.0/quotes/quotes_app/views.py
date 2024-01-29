from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Quote, Tag
from authors_app.views import Author
from .serializers import QouteSerializer

from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from .serializers import UserRegistrationSerializer

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import QuoteForm, TagForm
from django.core.paginator import Paginator

from django.views import View
from django.views.generic import ListView


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

# Create your views here.
# --------------------------- ---------------------------
# ---------------------------get all quotes ---------------------------
@api_view(['GET'])
def list_quotes(request):
    queryset = Quote.objects.all()
    serializer = QouteSerializer(queryset, many=True)
    return Response(serializer.data)

# --------------------------- ---------------------------
# ---------------------------add new quote ---------------------------
@login_required
def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            quote = form.save() 
            print("Author:", quote.author)
            
            # add tags
            form.instance.tags.set(form.cleaned_data['tags'])
            
            #print("Tags:", quote.tags.all())
            return redirect(to='quotes_app:add_quotes')  # Redirect to the quotes page or any other desired URL
    else:
        form = QuoteForm()
    return render(request, 'quotes_app/add_quote.html', {'form': form})

# --------------------------- ---------------------------
# ---------------------------add new tag ---------------------------
@login_required
def add_tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.save()
            return redirect(to='quotes_app:add_tags')  # Redirect to the quotes page or any other desired URL
    else:
        form = TagForm()
    return render(request, 'quotes_app/add_tags.html', {'form': form})

# --------------------------- ---------------------------
# ---------------------------get 10 quotes to show on page ---------------------------
def all_quotes(request):
    quote = Quote.objects.all()
    paginator = Paginator(quote, 10) 

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'quotes_app/all_quotes.html', {'page_obj': page_obj})

# --------------------------- ---------------------------
# ---------------------------getting some information about author ---------------------------
def author_detail(request, fullname):
    author = get_object_or_404(Author, pk=fullname)
    return render(request, 'quotes_app/author_detail.html', {'author': author})

class TagQuotesView(ListView):
    template_name = 'quotes_app/tag_quotes_list.html'
    context_object_name = 'tag_quotes'

    def get_queryset(self):
        tag_name = self.kwargs['tag_name']
        return Quote.objects.filter(tags__name__iexact=tag_name)

# --------------------------- ---------------------------
# ---------------------------class for getting top 10 tags ---------------------------
class TopTagsView(View):
    template_name = 'quotes_app/top_ten_tags_page.html'

    def get(self, request, *args, **kwargs):
        Tag.objects.all().update(usage_count=0)
        for quote in Quote.objects.all():
            for tag in quote.tags.all():
                tag.usage_count += 1
                tag.save()
        tags = Tag.objects.order_by('-usage_count')[:10]
        return render(request, self.template_name, {'tags': tags})