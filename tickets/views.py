from django.contrib.auth.models import User
from .models import *
from .form import *
from rest_framework.views import APIView
from django.contrib.auth import login,logout,authenticate
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            try:
                staff_user = StaffUser.objects.get(user=user)
                if staff_user.is_active:
                    login(request, user)
                    return redirect('staff_dashboard')
                else:
                    messages.error(request, "Your account is inactive. Contact admin for more information.")
            except StaffUser.DoesNotExist:
                messages.error(request, "You are not authorized as a staff user.")
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'registration/login.html')

def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            staff_user = StaffUser(
                user=user, 
                email=form.cleaned_data['email'],  
                name=user.username,  
                is_active=True  
            )
            staff_user.save()
            return redirect('login') 
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def staff_dashboard(request):
    try:
        staff_user = StaffUser.objects.get(user=request.user)
    except StaffUser.DoesNotExist:
        # If the StaffUser does not exist, log out the user
        logout(request)
        return redirect('login')
    
    if not staff_user.is_active:
        logout(request)
        return redirect('login')
    
    tickets = Ticket.objects.filter(assigned_to=staff_user)
    
    ticket_counts = {
        'draft': tickets.filter(status='draft').count(),
        'ongoing': tickets.filter(status='ongoing').count(),
        'completed': tickets.filter(status='completed').count(),
    }
    
    return render(request, 'tickets/staff_dashboard.html', {'tickets': tickets, 'ticket_counts': ticket_counts})


@login_required
def update_ticket(request, ticket_id):
    staff_user = get_object_or_404(StaffUser, user=request.user)

    if not staff_user.is_active:
        return redirect('login')
    
    ticket = get_object_or_404(Ticket, id=ticket_id)
    
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in ['ongoing', 'completed']:
            ticket.status = status
            ticket.save()
            return redirect('staff_dashboard')
    
    return render(request, 'tickets/update_ticket.html', {'ticket': ticket})

@login_required
def list_tickets(request):
    staff_user = StaffUser.objects.get(user=request.user)

    if not staff_user.is_active:
        return redirect('login')
    
    tickets = Ticket.objects.filter(assigned_to=staff_user)
    status_filter = request.GET.get('status')
    
    if status_filter in ['draft', 'ongoing', 'completed']:
        tickets = tickets.filter(status=status_filter)

    context = {
        'tickets': tickets,
        'status_filter': status_filter, 
    }
    return render(request, 'tickets/list_tickets.html', context)

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')