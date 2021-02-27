from django.shortcuts import render
from .models import *
from django.http import JsonResponse
from geopy.distance import great_circle

# Create your views here.
def home(request):
    return render(request, 'home.html')

def api(request):
    restaurants=Restaurant.objects.all()
    pincode=request.GET.get('pincode')
    km=request.GET.get('km')
    user_long=None
    user_lat=None
    if pincode:
        geolocator= Nominatim(user_agent="geoapiExercises")
        location=geolocator.geocode(int(pincode))
        user_lat=location.latitude
        user_long=location.longitude

    payload=[]
    for restaurant in restaurants:
        result={}
        result['name'] = restaurant.name
        result['image'] = restaurant.image
        result['description'] = restaurant.description
        result['pincode'] = restaurant.pincode
        if pincode:
            first = (float(user_lat) , float(user_long))
            second = (float(restaurant.lat) , float(restaurant.lon))
            result['distance'] = int( great_circle(first , second).miles)
        
        payload.append(result)
        
        if km:
            if result['distance'] > int(km):
                payload.pop()

    return JsonResponse(payload, safe= False)

