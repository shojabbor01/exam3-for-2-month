from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Trip
from datetime import datetime

def home(request):
    trips = Trip.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'trips': trips})

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return render(request, 'register.html')
            
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'register.html')
            
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return render(request, 'register.html')

        user = User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, 'Registration successful. Please login.')
        return redirect('login')
        
    return render(request, 'register.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'login.html')

@login_required
def logout_view(request):
    auth_logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')

@login_required
def create_trip(request):
    if request.method == 'POST':
        try:
            trip = Trip(
                user=request.user,
                start_location=request.POST['start_location'],
                end_location=request.POST['end_location'], 
                date=request.POST['date'],
                seats_available=request.POST['seats_available'],
                description=request.POST['description']
            )
            trip.save()
            messages.success(request, 'Trip created successfully!')
            return redirect('trip_detail', trip_id=trip.id)
        except Exception as e:
            messages.error(request, f'Error creating trip: {str(e)}')
            return render(request, 'create_trip.html')

    return render(request, 'create_trip.html')

def search_trips(request):
    trips = Trip.objects.all()
    start_location = request.GET.get('start_location', '')
    end_location = request.GET.get('end_location', '')
    date = request.GET.get('date', '')
    
    if start_location:
        trips = trips.filter(start_location__icontains=start_location)
    if end_location:
        trips = trips.filter(end_location__icontains=end_location)
    if date:
        try:
            search_date = datetime.strptime(date, '%Y-%m-%d').date()
            trips = trips.filter(date__date=search_date)
        except ValueError:
            messages.error(request, 'Invalid date format')
        
    context = {
        'trips': trips,
        'start_location': start_location,
        'end_location': end_location,
        'date': date
    }
    return render(request, 'search_trips.html', context)

def trip_detail(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    return render(request, 'trip_detail.html', {'trip': trip})

@login_required
def delete_trip(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id, user=request.user)
    
    if request.method == 'POST':
        trip.delete()
        messages.success(request, 'Trip deleted successfully!')
        return redirect('home')
        
    return render(request, 'confirm_delete.html', {'trip': trip})

@login_required
def edit_trip(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id, user=request.user)
    
    if request.method == 'POST':
        try:
            trip.start_location = request.POST['start_location']
            trip.end_location = request.POST['end_location']
            trip.date = request.POST['date']
            trip.seats_available = request.POST['seats_available']
            trip.description = request.POST['description']
            trip.save()
            messages.success(request, 'Trip updated successfully!')
            return redirect('trip_detail', trip_id=trip.id)
        except Exception as e:
            messages.error(request, f'Error updating trip: {str(e)}')
            
    return render(request, 'edit_trip.html', {'trip': trip})
