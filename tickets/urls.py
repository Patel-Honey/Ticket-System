from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    path("user/register/",user_register,name='user-register'),
    path('login/', login_view, name='login'),  
    path('staff_dashboard/', staff_dashboard, name='staff_dashboard'),
    path('update_ticket/<int:ticket_id>/', update_ticket, name='update_ticket'),
    path('list-tickets/', list_tickets, name='list_tickets'),  # Add this line
    path('logout/', logout_view, name='logout'),
  
]