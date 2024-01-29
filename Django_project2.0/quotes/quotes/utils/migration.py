import os
import django
from pymongo import MongoClient

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "quotes.settings")
django.setup()

from authors_app.models import Author
from quotes_app.models import Tag, Quote

uri = "mongodb+srv://tsubanolga:O1904@cluster0.yiefpq6.mongodb.net/Cluster0?retryWrites=true&w=majority"
client = MongoClient(uri)

db = client.Cluster0

authors = db.authors.find()

for author in authors:
    #print(author)
    Author.objects.get_or_create(
        fullname = author['fullname'],
        born_date = author['born_date'],
        born_location = author['born_location'],
        description = author['description'],
    )

quotes = db.quotes.find()

for quote in quotes:
    tags = []
    for tag in quote['tags']:
        try:
            t, *_ = Tag.objects.get_or_create(name=tag)
        except Tag.MultipleObjectsReturned:
            # Handle the case where multiple tags with the same name exist.
            # Here, we're simply using the first one.
            t = Tag.objects.filter(name=tag).first()
        tags.append(t)
    #print(tags)
    exist_quote = bool(len(Quote.objects.filter(quote=quote['quote'])))
    if not exist_quote:
        author = db.authors.find_one({'_id': quote['author']})
        a = Author.objects.get(fullname=author['fullname'])
        q = Quote.objects.create(
            quote=quote['quote'],
            author=a
        )
        for tag in tags:
            q.tags.add(tag)