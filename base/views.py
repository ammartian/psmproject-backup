from unicodedata import name
from django.shortcuts import render, redirect
from django.contrib.auth.models import User #for manage user
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout  # django template
from django.contrib.auth.decorators import login_required  # to restrict page/views
from .models import *


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
        if user is not None and user.is_staff:
            login(request, user) #user line 49 ^
            return redirect('admin-dashboard')
        elif user is not None and user.is_lecturer:
            login(request, user) #user line 49 ^
            return redirect('lecturer-dashboard')
        elif user is not None and user.is_student:
            login(request, user) #user line 49 ^
            return redirect('student-dashboard')
        else:
            messages.error(request, 'Incorrect username or password')

    context = {}
    return render(request, 'login/login_content.html', context)



# Logout, destroy session id
def logoutUser(request):
    logout(request)
    return redirect('login')


#Forgot password
def forgotPassword(request):
    context = {}
    return render(request, 'login/forgot_password.html', context)


#First time login
def firstTimeLogin(request):
    context = {}
    return render(request, 'login/first_time_login.html', context)


def setNewPassword(request):
    context = {}
    return render(request, 'login/set_new_password.html', context)

#LOGIN--------------------------------------------------------


#ALL--------------------------------------------------------

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



@login_required(login_url='login')
def reenterPassword(request):
    context = {}
    return render(request, 'all/reenter_password.html', context)

#ALL--------------------------------------------------------


#ADMIN--------------------------------------------------------
@login_required(login_url='login') #if not logged in, cant view dashboard
def adminDashboard(request):
    context = {}
    return render(request, 'admin/admin_dashboard.html', context)

@login_required(login_url='login')
def manageCourse(request):
    courses = Course.objects.all()
    # assigned = User.objects.filter(lecturer=True).values('name')
    lecturers = User.objects.filter(lecturer=True) #show only lecturer

    context = {'courses': courses, 'lecturers':lecturers,}
    return render(request, 'admin/manage_course.html', context)


@login_required(login_url='login')
def manageLecturer(request):
    context = {}
    return render(request, 'admin/manage_lecturer.html', context)


@login_required(login_url='login')
def manageStudent(request):
    context = {}
    return render(request, 'admin/manage_student.html', context)


#ADMIN--------------------------------------------------------

#LECTURER-----------------------------------------------------
@login_required(login_url='login')
def lecturerDashboard(request):
    context = {}
    return render(request, 'lecturer/lecturer_dashboard.html', context)

@login_required(login_url='login')
def lectLearningMaterial(request):
    context = {}
    return render(request, 'lecturer/lect_learning_material.html', context)

@login_required(login_url='login')
def lectAssignment(request):
    context = {}
    return render(request, 'lecturer/lect-assignment.html', context)

@login_required(login_url='login')
def lectAssignmentSubmitted(request):
    context = {}
    return render(request, 'lecturer/lect-assignment-submitted.html', context)

@login_required(login_url='login')
def lectQuiz(request):
    context = {}
    return render(request, 'lecturer/lect-quiz.html', context)

@login_required(login_url='login')
def lectCreateQuiz(request):
    context = {}
    return render(request, 'lecturer/lect-create-quiz.html', context)

@login_required(login_url='login')
def lectQuizContent(request):
    context = {}
    return render(request, 'lecturer/lect-quiz-content.html', context)

@login_required(login_url='login')
def lectEditQuiz(request):
    context = {}
    return render(request, 'lecturer/lect-edit-quiz.html', context)

@login_required(login_url='login')
def lectQuizAnswered(request):
    context = {}
    return render(request, 'lecturer/lect-quiz-answered.html', context)

#LECTURER-----------------------------------------------------

#Student-----------------------------------------------------
@login_required(login_url='login')
def studentDashboard(request):
    context = {}
    return render(request, 'student/student_dashboard.html', context)

@login_required(login_url='login')
def registerCourse(request):
    context = {}
    return render(request, 'student/register-course.html', context)

@login_required(login_url='login')
def courseDetails(request):
    context = {}
    return render(request, 'student/course-details.html', context)

@login_required(login_url='login')
def studAssignmentDetails(request):
    context = {}
    return render(request, 'student/stud-assignment-details.html', context)

@login_required(login_url='login')
def studQuizDetails(request):
    context = {}
    return render(request, 'student/stud-quiz-details.html', context)


#STUDENT-----------------------------------------------------