from rest_framework import routers
from .views import AuthorViewSet
from django.urls import path
from .views import all_authors, add_author, scrape_data_view

router = routers.DefaultRouter()
router.register(r'', AuthorViewSet)

app_name = 'authors_app'
urlpatterns = [
    #path('', include(router.urls)),
    path('add_author/', add_author, name='add_author'),
    path('all_authors/', all_authors, name='all_authors'),
    path('scrape-data/', scrape_data_view, name='scrape_data'),
]