from django.shortcuts import render, redirect
from django.contrib.auth.models import User #for manage user
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout  # django template
from django.contrib.auth.decorators import login_required  # to restrict page/views


# Create your views here.

#LOGIN--------------------------------------------------------

#Login
def loginPage(request):

    #get username and password in db
    if request.method == 'POST':
        username = request.POST.get('username').lower() #to lowercase all request
        password = request.POST.get('password')
        
        #check if user exist
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        #authentication
        user = authenticate(request, username=username, password=password)

        #log user in and send to home
        if user is not None:
            login(request, user) #user line 49 ^
            return redirect('dashboard')
        else:
            messages.error(request, 'Incorrect username or password')

    context = {}
    return render(request, 'login/login_content.html', context)



# Logout, destroy session id
def logoutUser(request):
    logout(request)
    return redirect('login')

#LOGIN--------------------------------------------------------


#ALL--------------------------------------------------------

@login_required(login_url='login') #if not logged in, cant view dashboard
def dashboard(request):
    context = {}
    return render(request, 'all/dashboard.html', context)



@login_required(login_url='login')
def changeEmail(request):
    context = {}
    return render(request, 'all/change_email.html', context)



@login_required(login_url='login')
def changePassword(request):
    context = {}
    return render(request, 'all/change_password.html', context)



@login_required(login_url='login')
def sessionManagement(request):
    context = {}
    return render(request, 'all/session.html', context)

#ALL--------------------------------------------------------


#ADMIN--------------------------------------------------------

def manageCourse(request):
    context = {}
    return render(request, 'admin/manage_course.html', context)



def manageLecturer(request):
    context = {}
    return render(request, 'admin/manage_lecturer.html', context)



def manageStudent(request):
    context = {}
    return render(request, 'admin/manage_student.html', context)


#ADMIN--------------------------------------------------------

