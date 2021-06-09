from django.shortcuts import render
import numpy as np  
import cv2   
import glob
from .models import user_data

def index(request):      
    return render(request, 'attendance/index.html',{
        "students":user_data.objects.all()
    })

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
            return render(request, 'attendance/index.html',{
                "students":user_data.objects.all()
            })
    return render(request, "attendance/register.html")

def take_attendance(request):
    Camera_matrix=np.array([[976.9729312,0.,524.0006998],[0.,974.93730941,362.12928281],[0.,0.,1.]])
    Distortion_matrix=np.array([[-2.65932795e-01,3.04981994e+00,-1.31423363e-03,-6.12106389e-04,-1.19332537e+01]])
    params =  cv2.aruco.DetectorParameters_create()
    params.cornerRefinementMethod = cv2.aruco.CORNER_REFINE_SUBPIX
    cap=cv2.VideoCapture(0)
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    size = (frame_width, frame_height)

    while(True):

        #FETCHING THE IMAGE FRAME 
        ret, frame = cap.read()
        if ret is not True:
            print("Error in video capture")
            exit()

        #USING INBUILT FUNCTION TO DETECT MARKER AND GET THE CORNERS 
        corners, ids, rejectedImgPoints=cv2.aruco.detectMarkers(frame, cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_50),parameters=params,cameraMatrix=Camera_matrix,distCoeff=Distortion_matrix)

        if ids is not None:
            try:
                user_data.objects.filter(aruco_id=ids[0][0]).update(present=True) 
            except:
                pass 
            cap.release()
            break
             
            
    return render(request, 'attendance/index.html',{
        "students":user_data.objects.all()
    })