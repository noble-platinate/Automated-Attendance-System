from django.shortcuts import render
import numpy as np  
import cv2   
import glob
from .models import user_data


def index(request):
    return render(request, 'attendance/index.html')

def register(request="GET"):
    if request.method == "POST":
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        roll=request.POST["roll"]
        aruco=request.POST["aruco"]
        try:
            x=user_data.objects.get(aruco_id=aruco)
            return render(request, "attendance/register.html", {
                "message": "Tag already used!"
            })
        except:
            x=user_data(fname=fname, lname=lname, rno=roll, present=False,aruco_id=aruco)
            x.save()
            return render(request, "attendance/index.html")
    return render(request, "attendance/register.html")