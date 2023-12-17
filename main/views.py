from django.shortcuts import render,redirect
from .models import Found_img, Profile
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib import auth
from django.contrib.auth.decorators import login_required
import json
from django.contrib.auth.hashers import make_password

from .ml_model import *

# request contains all meta data

def home(request):
    # renders home.html template
    return render(request, 'main/Home.html')


@login_required # Decorator to check if authenticated user is sending request
def lost(request):
    images = Found_img.objects.all() # retrieve all rows from table Found_img
    context = {
        "images": images
    }
    
    
    return render(request, 'main/lost.html',context)



def model_pred(pk):
    ob = Found_img.objects.get(pk=pk) # retrive only row from found_img table having id = pk
    res = pred(str(ob.image)) # predict image
    d = json.loads(res)[0] # convert json to dict
    if len(d)>0:
        name = d['name']
        im_class = d['class']
        confidence = d['confidence']
        box_x1 = d['box']['x1']
        box_x2 = d['box']['x2']
        box_y1 = d['box']['y1']
        box_y2 = d['box']['y2']
        
        """ adding remaining fields into retrived row"""
        ob.name = name
        ob.im_class = im_class
        ob.confidence = confidence
        ob.box_x1 = box_x1
        ob.box_x2 = box_x2
        ob.box_y1 = box_y1
        ob.box_y2 = box_y2
        ob.save()
    else:
        ob.name = 'Unidentified'
        ob.save()


@login_required # Decorator to check if authenticated user is sending request
def found(request):
    if request.method == 'POST': # IF request is POST do this
        
        image = request.FILES['image'] # extracting image file from request
        
        
        img = Found_img(image=image, user=request.user) # adding a row in found_img table with image = extracted image and user = current logged in user
        img.save() # commiting into database
        model_pred(img.pk)  # passing primary key of currently saved row to model_pred function which predicts the image and saves remaining info
        
        
        return redirect('/myapp')  # after successfully saving row into database it redirects to home page
       
    return render(request, 'main/found.html') # if req is GET just render found.html template

def user_login(request):
    if request.method == 'POST': # IF request is POST do this
        
        """Extract username and passwordn from request"""
        username = request.POST.get('username')  
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password) # retrieve row from User table if user and password are present in database 
        
        if user is not None: # if such row exists in User table
            
            login(request, user) # create a session for that user so he didn't have to login again
            
            return redirect('home') # redirect to home page
        
        else:  # if such row does not exist in User table
            context = {
                'error':"Invalid username or password"    # Dictionary contains error message
            }
            return render(request, 'main/index.html', context) # render index.html template and pass context i.e error message
    return render(request, 'main/index.html') # if req is GET just render found.html template

def logout(request):
    auth.logout(request) # logout current user
    return redirect("/myapp") # redirect to home page


def register(request):
    if request.method == 'POST': # IF request is POST do this
        
        """Extract all info from request"""
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        
        user = User(username=username, email=email, password=make_password(password)) #adding a row in User table with username email and password
        user.save() # commit into database
        
        profile = Profile(phone=phone, user=user) #adding a row in User table with username email and password
        profile.save() # Commit into database
        
        return redirect('/myapp/login') #redirect to login page
        
    return render(request, 'main/register.html')