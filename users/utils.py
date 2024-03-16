from django.contrib.auth import authenticate
from rest_framework import serializers
from django.contrib.auth import get_user_model

def get_and_authenticate_user(email, password):
    user = authenticate(username=email, password=password)
    if user is None:
        raise serializers.ValidationError("Invalid username/password. Please try again!")
    return user


def create_user_account(email, password,role, 
                         **extra_fields):
    user = get_user_model().objects.create_user(
        email=email, password=password, role=role, **extra_fields)
    return user