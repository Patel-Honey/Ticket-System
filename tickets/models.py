from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class StaffUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=254,null=True)
    name = models.CharField(max_length=255,null=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.user.username
    
    
class Ticket(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('archived', 'Archived'),
    ]
    
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    assigned_to = models.ForeignKey(StaffUser, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    attachments = models.FileField(upload_to='attachments/', blank=True, null=True)  # for handling multiple files use a related model

    def __str__(self):
        return self.name


    
