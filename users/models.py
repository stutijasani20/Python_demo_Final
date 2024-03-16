from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    USER_ROLES = (
        ('applicant', _('applicant')),
        ('recruiter', _('recruiter')),
    )

    email = models.EmailField(_('email address'), unique=True)
    role = models.CharField(_('role'), max_length=20, choices=USER_ROLES)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        if not self.username:
            
            self.username = self.email.split('@')[0]
        while CustomUser.objects.filter(username=self.username).exists():
            self.username += '_'
        super().save(*args, **kwargs)

class Applicant(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10)
    image = models.ImageField(upload_to='applicant/profile')
    gender = models.CharField(max_length=10)
    
    def __str__(self):
        return self.user.first_name

class Company(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10)
    type = models.CharField(max_length=15)
    status = models.CharField(max_length=20)
    company_name = models.CharField(max_length=100)
 
    def __str__ (self):
        return self.user.username
 
class Job(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    salary = models.FloatField()
    description = models.TextField(max_length=400)
    experience = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    skills = models.CharField(max_length=200)
    creation_date = models.DateField()
 
    def __str__ (self):
        return self.title
 
class Application(models.Model):
    company = models.CharField(max_length=200, default="")
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    resume = models.FileField(upload_to="aaplication/resume")
    apply_date = models.DateField()
 
    def __str__ (self):
        return str(self.applicant)