# from rest_framework import routers
from django.urls import path
from .views import add_quote, all_quotes, add_tag, author_detail ,TopTagsView, TagQuotesView

app_name = 'quotes_app'
urlpatterns = [
    path('add_quote/', add_quote, name='add_quotes'),
    path('all_quotes/', all_quotes, name='all_quotes'),
    path('top-tags/', TopTagsView.as_view(), name='top_tags'),
    path('add_tag/', add_tag, name='add_tags'),
    path('tag/<str:tag_name>/', TagQuotesView.as_view(), name='tag_quotes'),
    path('author/<str:fullname>/', author_detail, name='author_detail'),
]