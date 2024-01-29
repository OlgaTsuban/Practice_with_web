from django.db import models
from authors_app.models import Author

class Tag(models.Model):
    name = models.CharField(max_length=80, unique=True,)
    usage_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name

# Create your models here.
class Quote(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='quotes', blank=False)
    tags = models.ManyToManyField(Tag, blank=False)
    quote = models.CharField(blank=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        for tag in self.tags.all():
            tag.usage_count += 1
            tag.save()
            
    def __str__(self):
        return f'{self.quote} - {self.author.fullname}'