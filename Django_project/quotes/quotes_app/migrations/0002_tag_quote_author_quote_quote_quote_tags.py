# Generated by Django 5.0 on 2024-01-01 18:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authors_app', '0002_alter_author_fullname'),
        ('quotes_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
            ],
        ),
        migrations.AddField(
            model_name='quote',
            name='author',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='quotes', to='authors_app.author'),
        ),
        migrations.AddField(
            model_name='quote',
            name='quote',
            field=models.CharField(default=None),
        ),
        migrations.AddField(
            model_name='quote',
            name='tags',
            field=models.ManyToManyField(to='quotes_app.tag'),
        ),
    ]
