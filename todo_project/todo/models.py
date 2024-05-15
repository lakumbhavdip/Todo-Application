from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Permission

class Users(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=120)
    is_verified = models.BooleanField(default=False)
    
    USERNAME_FIELD = "email"
    
class Todo(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    description = models.TextField()
    duedate = models.DateTimeField(null=True)

    def __str__(self):
        return self.title