# Generated by Django 5.0 on 2024-01-06 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotes_app', '0006_alter_quote_quote_alter_tag_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='usage_count',
            field=models.IntegerField(default=0),
        ),
    ]