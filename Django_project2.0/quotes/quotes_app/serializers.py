from rest_framework import serializers
from .models import Quote
from django.contrib.auth.models import User

class QouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quote
        fields = '__all__'


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']