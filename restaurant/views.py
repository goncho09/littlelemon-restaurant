# from django.http import HttpResponse
from django.shortcuts import render
from .forms import BookingForm
from .models import Menu
from django.core import serializers
from .models import Booking
from datetime import datetime
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse,JsonResponse


# Create your views here.
def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def reservations(request):
    bookings = Booking.objects.all()
    booking_json = serializers.serialize('json', bookings)
    return render(request, 'bookings.html',{"bookings":booking_json})

def book(request):
    form = BookingForm()
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form':form}
    return render(request, 'book.html', context)

# Add your code here to create new views
def menu(request):
    menu_data = Menu.objects.all()
    main_data = {"menu": menu_data}
    return render(request, 'menu.html', {"menu": main_data})


def display_menu_item(request, pk=None): 
    if pk: 
        menu_item = Menu.objects.get(pk=pk) 
    else: 
        menu_item = "" 
    return render(request, 'menu_item.html', {"menu_item": menu_item}) 

@csrf_exempt
def bookings(request):
    if request.method == 'POST':
        data = json.load(request)
        exist = Booking.objects.filter(reservation_date=data['reservation_date']).filter(
            reservation_slot=data['reservation_slot']).exists()
        if exist==False:
            try:
                booking = Booking(
                    first_name=data['first_name'],
                    reservation_date=data['reservation_date'],
                    reservation_slot=data['reservation_slot'],
                )
                booking.save()
            except Exception as e:
                return HttpResponse({"error":e.args}, content_type='application/json')
        else:
            return HttpResponse("{'error':1}", content_type='application/json')
    
    date = request.GET.get('date',datetime.today().date())
    
    bookings = Booking.objects.all().filter(reservation_date=date).order_by('reservation_slot')
    booking_json = serializers.serialize('json', bookings)
    return JsonResponse({"bookings":booking_json})

@csrf_exempt
def bookingsApi(request):
    bookings = Booking.objects.all()
    booking_json = serializers.serialize('json', bookings)
    return HttpResponse(booking_json, content_type='application/json')

@csrf_exempt
def menuApi(request):
    menu_data = Menu.objects.all()
    menu_json = serializers.serialize('json', menu_data)
    return HttpResponse(menu_json, content_type='application/json')

@csrf_exempt
def menu_item(request,id):
    menu_item = Menu.objects.filter(pk=id)
    if not menu_item:
        return HttpResponse("{'error':'No menu item found'}", content_type='application/json')
    menu_json = serializers.serialize('json', menu_item)
    return HttpResponse(menu_json, content_type='application/json')