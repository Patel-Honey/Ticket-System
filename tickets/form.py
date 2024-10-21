from django import forms 
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)  

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']  
        
class UserLoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','password']   
        
class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['name', 'description', 'assigned_to', 'status', 'attachments']