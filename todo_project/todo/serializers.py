from rest_framework import serializers
from .models import Users,Todo
from django.contrib.auth.hashers import make_password  # Import the password hashing function

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ( 'email', 'password')  

    def create(self, validated_data):
        email = validated_data['email']
        password = validated_data['password']  # Get the password from the validated data
        hashed_password = make_password(password)
        user = Users.objects.create(
            email=email,
            password=hashed_password,  
        )
        return user
    

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('id', 'title', 'description', 'category', 'duedate')
        

class TodoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('title', 'description', 'category', 'duedate')