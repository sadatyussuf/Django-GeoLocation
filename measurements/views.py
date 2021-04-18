from django.shortcuts import render,get_object_or_404
from .models import  Measurement
from .forms import MeasurementModelForm

# Create your views here.
def calculate_distance(request):
    dis = get_object_or_404(Measurement,id=1)
    form = MeasurementModelForm(request.POST or None)

    context = {
        'distance': dis,
        'form':form
        }

    return render(request,'measurements/main.html',context)

