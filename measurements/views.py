from django.shortcuts import render,get_object_or_404,HttpResponse
# from geopy import distance
from .models import  Measurement
from .forms import MeasurementModelForm

from geopy.geocoders import Photon
from geopy.distance import geodesic
from .utilis import get_geoip,get_center_coordinates,get_zoom

import folium
# Create your views here.


def index(request):
    pass


def calculate_distance(request):

    # initial values
    distance = None
    destination = None


    dis = get_object_or_404(Measurement,id=7)
    form = MeasurementModelForm(request.POST or None)
    geolocator = Photon(user_agent='measurements')

    ip = '72.14.207.99'
    country, city, lat, lon = get_geoip(ip)

    location = geolocator.geocode(city)

#location coordinates
    l_lat = lat
    l_lon = lon

    pointA = (l_lat,l_lon)

    # Intial folium map
    m = folium.Map(width=800, height=500, location=get_center_coordinates(l_lat,l_lon),zoom_start = 8)
    #location marker
    folium.Marker([l_lat,l_lon],tooltip="click here for more",popup=city['city'], icon=folium.Icon(color='purple')).add_to(m)


    if form.is_valid():
        instance = form.save(commit=False)
        destination_ = form.cleaned_data.get('destination')
        destination = geolocator.geocode(destination_)

# destination coordinates
        d_lat = destination.latitude
        d_lon = destination.longitude

        pointB = (d_lat,d_lon)

# distance calculation
        distance= round(geodesic(pointA, pointB).km, 2)


    #folium map modification
        m = folium.Map(width=800, height=500, location=get_center_coordinates(l_lat,l_lon,d_lat,d_lon),zoom_start = get_zoom(distance))
    #location marker
        folium.Marker([l_lat,l_lon],tooltip="click here for more",popup=city['city'], icon=folium.Icon(color='purple')).add_to(m)
    #destination marker
        folium.Marker([d_lat,d_lon],tooltip="click here for more",popup=destination, icon=folium.Icon(color='red',icon='cloud')).add_to(m)

        #draw the line between location and destination
        line = folium.PolyLine(locations=[pointA,pointB],weight=2,color='blue')
        m.add_child(line)


        instance.location = location
        instance.distance = distance
        instance.save()

    m = m._repr_html_()

    context = {
        'distance': distance,
        'destination': destination,
        'form':form,
        'map': m
        }

    return render(request,'measurements/main.html',context)

