from rest_framework import serializers
from . models import *
from rest_framework.authtoken.models import Token
from django.contrib.auth import password_validation
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.password_validation import validate_password
from rest_framework.response import Response

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = "__all__"
        

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'
    
   
class ApplicantSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    class Meta:
        model = Applicant
        fields = '__all__'

class ApplicationSerializer(serializers.ModelSerializer):
    resume = serializers.FileField(required=False)
    class Meta:
        model = Application
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['role', 'email', "password"]
    
class AuthUserSerializer(serializers.ModelSerializer):
    jwt_token = serializers.SerializerMethodField()

    class Meta:
         model = CustomUser
         fields = ["email" , "jwt_token", "role", "password"]

    def get_jwt_token(self, obj):
        refresh = RefreshToken.for_user(obj)
        return {"access": str(refresh.access_token), "refresh": str(refresh)}

class EmptySerializer(serializers.Serializer):
    pass

class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=300, required=True)
    password = serializers.CharField(required=True, write_only=True)

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['role', 'email', 'password']

    def validate(self, value):
        role = value.get('role', 'applicant')  
        user_email = value.get('email')

        if CustomUser.objects.filter(email=user_email).exists():
            raise serializers.ValidationError("Email is already taken")
        
        return value

    def validate_password(self, value):
        password_validation.validate_password(value)
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser.objects.create_user(password=password, **validated_data)
        return user
    
class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):

        instance.set_password(validated_data['password'])
        instance.save()
        return {"Password Updated Successfully !"}