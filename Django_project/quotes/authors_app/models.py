from django.db import models

# Create your models here.
class Author(models.Model):
    fullname = models.CharField(max_length = 100, null=False, unique=True, default='Default Fullname')
    born_date = models.CharField(max_length=50, null=False)
    born_location = models.CharField(max_length=150, null=False)
    description = models.CharField()

    def __str__(self):
        return self.fullname