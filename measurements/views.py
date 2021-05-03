from django.shortcuts import render,get_object_or_404,HttpResponse
# from geopy import distance
from .models import  Measurement
from .forms import MeasurementModelForm

from geopy.geocoders import Photon
from geopy.distance import geodesic
from .utilis import get_geoip

# Create your views here.


def index(request):
    pass
#     dis = get_object_or_404(Measurement)
#     form = MeasurementModelForm(request.POST or None)


#     context = {
#         'distance': dis,
#         'form':form
#         }

#     return render(request,'measurements/main.html',context)




def calculate_distance(request):
    dis = get_object_or_404(Measurement)
    form = MeasurementModelForm(request.POST or None)
    geolocator = Photon(user_agent='measurements')

    ip = '72.14.207.99'
    country, city, lat, lon = get_geoip(ip)

    # print(f'location country {country}')
    # print(f'location city {city}')
    # print(f'location lat {lat}')
    # print(f'location lon {lon}')

    location = geolocator.geocode(city)
    # print('###', location)

    l_lat = lat
    l_lon = lon

    pointA = (l_lat,l_lon)


    if form.is_valid():
        instance = form.save(commit=False)
        destination_ = form.cleaned_data.get('destination')
        destination = geolocator.geocode(destination_)

        # print(destination)

        d_lat = destination.latitude
        d_lon = destination.longitude

        pointB = (d_lat,d_lon)

        distance= round(geodesic(pointA, pointB).km, 2)

        instance.location = location
        instance.distance = distance
        instance.save()

    context = {
        'distance': dis,
        'form':form
        }

    return render(request,'measurements/main.html',context)

