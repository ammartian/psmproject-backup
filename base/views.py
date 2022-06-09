from datetime import datetime
from distutils.command.upload import upload
from msilib.schema import InstallUISequence
from tkinter import Widget
from unicodedata import name
from xml.etree.ElementTree import tostring
from django.shortcuts import render, redirect
from django.contrib.auth.models import User #for manage user
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout  # django template
from django.contrib.auth.decorators import login_required  # to restrict page/views
from django.contrib.sessions.models import Session
from .models import *
from .forms import * #Can be more specific
from django.views.generic.edit import UpdateView
from django.core.files.storage import FileSystemStorage

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
            return redirect('admin-dashboard', user.id)
        elif user is not None and user.is_lecturer:
            login(request, user) #user line 49 ^
            return redirect('lecturer-dashboard', user.id)
        elif user is not None and user.is_student:
            login(request, user) #user line 49 ^
            return redirect('student-dashboard', user.id)
        else:
            messages.error(request, 'Incorrect username or password')

    context = {}
    return render(request, 'login/login_content.html', context)


#Re-enter Password for Change Email
# @login_required(login_url='login')
# def checkChangeEmail(request, pk):
    
#     users = User.objects.get(id=pk)

#     context = {'users':users}
#     return render(request, 'all/reenter_email.html', context)

@login_required(login_url='login')
def checkChangeEmail(request):

    form = ConfirmPasswordForm()

    context = {'form':form}
    return render(request, 'all/reenter_email.html', context)

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
def userProfile(request, pk):
    currUsers = User.objects.get(id=pk)
    user = request.user
    form = ChangeProfilePicture(instance=user)

    if request.method == 'POST':
        form = ChangeProfilePicture(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()

    context = {'currUsers':currUsers, 'form':form}
    return render(request, 'all/user_profile.html', context)

@login_required(login_url='login')
def changeEmail(request,pk):
    user = User.objects.get(id=pk) 
    form = EmailChangeForm(user=request.user, data=request.POST)
    if request.method=='POST':
        form = EmailChangeForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Form submission successful')
            return redirect("change-email", pk=user.id)
        else:
            messages.error(request,'unsuccessful')
            #return redirect('login')
    
    context = {'form':form, 'user':user}
    return render(request, 'all/change_email.html', context)



@login_required(login_url='login')
def changePassword(request):
    context = {}
    return render(request, 'all/change_password.html', context)



@login_required(login_url='login')
def sessionManagement(request, pk): #how to fetch current user only
    currUser = User.objects.get(id=pk)

    sessions = Session.objects.all() #add count?
    login_logs = User.objects.filter(id=pk) #to fetch current user

    context = {'sessions':sessions, 'login_logs':login_logs, 'currUser':currUser}
    return render(request, 'all/session.html', context)



@login_required(login_url='login')
def reenterPassword(request):
    context = {}
    return render(request, 'all/reenter_password.html', context)

#ALL--------------------------------------------------------


#ADMIN--------------------------------------------------------
@login_required(login_url='login') #if not logged in, cant view dashboard
def adminDashboard(request, pk):
    currAdmin = User.objects.get(id=pk)
    context = {'currAdmin':currAdmin}
    return render(request, 'admin/admin_dashboard.html', context)

@login_required(login_url='login')
def manageCourse(request, pk):
    currAdmin = User.objects.get(id=pk)
    courses = Course.objects.all()

    form = createCourse(initial={'admin_create':currAdmin})
    
    #lecturers = User.objects.filter(lecturer=True) #show only lecturer
    if request.method == "POST":
        #print('Printing POST', request.POST)
        form = createCourse(request.POST)
        if form.is_valid():
            form.save()
            #current: it will simply add to current page
            #redirect to main current page?

    context = {'currAdmin':currAdmin, 'courses':courses, 'form':form}
    return render(request, 'admin/manage_course.html', context)

@login_required(login_url='login')
def updateCourse(request, pk, course_pk,):
    currAdmin = User.objects.get(id=pk)
    course = Course.objects.get(id=course_pk)
    
    form = createCourse(instance=course, initial={'id':course})

    if request.method == 'POST':
        form = createCourse(request.POST, instance=course)

        # if all([form.is_valid(), form_2.is_valid()]):
        if form.is_valid():
            form.save()
            return redirect('manage-course', currAdmin.id)

    context = {'form':form}
    return render(request, 'admin/update_course.html', context)


@login_required(login_url='login')
def deleteCourse(request, pk, course_pk):
    currAdmin = User.objects.get(id=pk)
    course = Course.objects.get(id=course_pk)

    if request.method == "POST":
        course.delete()
        return redirect('manage-course', currAdmin.id)

    context = {'currAdmin':currAdmin, 'course':course}
    return render(request, 'admin/delete_course.html', context)


@login_required(login_url='login')
def assignLecturer(request, pk, course_pk):
    currAdmin = User.objects.get(id=pk)
    course = Course.objects.get(id=course_pk)
    assignedCourses = AssignLecturer.objects.all()

    form = assignLecturertoCourse(instance=course, initial={'course':course})
    
    if request.method == "POST":
        form = assignLecturertoCourse(request.POST)
        if form.is_valid():
            form.save()

    context = {'currAdmin':currAdmin, 'course':course, 'assignedCourses':assignedCourses, 'form':form}
    return render(request, 'admin/assign_lecturer.html', context)

@login_required(login_url='login')
def updateAssignedLecturer(request, pk, course_pk, assign_pk):
    currAdmin = User.objects.get(id=pk)
    course = Course.objects.get(id=course_pk)
    assignedCourses = AssignLecturer.objects.get(id=assign_pk)
    
    form = assignLecturertoCourse(instance=assignedCourses)

    if request.method == 'POST':
        form = assignLecturertoCourse(request.POST, instance=assignedCourses)

        if form.is_valid():
            form.save()
            return redirect('assign-lecturer', currAdmin.id, course.id)

    context = {'form':form, 'assignedCourses':assignedCourses}
    return render(request, 'admin/update_assignedLecturer.html', context)


@login_required(login_url='login')
def deleteAssignedLecturer(request, pk, course_pk, assign_pk):
    currAdmin = User.objects.get(id=pk)
    course = Course.objects.get(id=course_pk)
    assignedCourses = AssignLecturer.objects.get(id=assign_pk)

    if request.method == "POST":
        assignedCourses.delete()
        return redirect('assign-lecturer', currAdmin.id, course.id)

    context = {'currAdmin':currAdmin, 'course':course, 'assignedCourses':assignedCourses}
    return render(request, 'admin/delete_assignedLecturer.html', context)


@login_required(login_url='login')
def manageLecturer(request, pk):
    currAdmin = User.objects.get(id=pk)

    form = createLecturer(initial={'date_created': datetime.now(), 'lecturer': True})
    lecturers = User.objects.filter(lecturer=True) #show only lecturer
    if request.method == 'POST':
        #print('Printing POST', request.POST)
        form = createLecturer(request.POST)
        if form.is_valid():
            form.save()
            #current: it will simply add to current page
            #redirect to main current page?
    context = {'currAdmin':currAdmin, 'lecturers':lecturers, 'form':form}
    return render(request, 'admin/manage_lecturer.html', context)

@login_required(login_url='login')
def updateLecturer(request, pk):
    lecturer = User.objects.get(id=pk)
    form = createLecturer(instance=lecturer)
    if request.method == 'POST':
        form = createLecturer(request.POST, instance=lecturer)
        if form.is_valid():
            form.save()
            return redirect('manage-lecturer')

    context = {'form':form}
    return render(request, 'admin/update_lecturer.html', context)

@login_required(login_url='login')
def deleteLecturer(request, pk):
    lecturer = User.objects.get(id=pk)
    if request.method == "POST":
        lecturer.delete()
        return redirect('manage-lecturer')

    context = {'lecturer':lecturer}
    return render(request, 'admin/delete_lecturer.html', context)


@login_required(login_url='login')
def manageStudent(request, pk):
    currAdmin = User.objects.get(id=pk)

    form = createStudent(initial={'date_created': datetime.now(), 'student': True})
    students = User.objects.filter(student=True)
    if request.method == 'POST':
        #print('Printing POST', request.POST)
        form = createStudent(request.POST)
        if form.is_valid():
            form.save()
            #current: it will simply add to current page
            #redirect to main current page?
    
    context = {'currAdmin':currAdmin, 'students':students, 'form':form}
    return render(request, 'admin/manage_student.html', context)

@login_required(login_url='login')
def updateStudent(request, pk):
    student = User.objects.get(id=pk)
    form = createStudent(instance=student)
    if request.method == 'POST':
        form = createStudent(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('manage-student')

    context = {'form':form}
    return render(request, 'admin/update_student.html', context)

@login_required(login_url='login')
def deleteStudent(request, pk):
    student = User.objects.get(id=pk)
    if request.method == "POST":
        student.delete()
        return redirect('manage-student')

    context = {'student':student}
    return render(request, 'admin/delete_student.html', context)


#ADMIN--------------------------------------------------------

#LECTURER-----------------------------------------------------
@login_required(login_url='login')
def lecturerDashboard(request, pk):
    currLect = User.objects.get(id=pk)
    assignedCourse = Course.objects.get(user_id=currLect.id) #user_id is fk and id is pk
    context = {'currLect':currLect, 'assignedCourse':assignedCourse}
    return render(request, 'lecturer/lecturer_dashboard.html', context)

@login_required(login_url='login')
def lectLearningMaterial(request, pk, course_pk):
    currLect = User.objects.get(id=pk)
    assignedCourse = Course.objects.get(id=course_pk)
    learningMaterials = LearningMaterial.objects.filter(course=assignedCourse) #filter by course but not lecturer
    form = CreateLearningMaterial(initial={'course':assignedCourse})

    if request.method == 'POST':
        form = CreateLearningMaterial(request.POST, request.FILES)
        if form.is_valid():
            form.save()

    context = {'form':form, 'currLect':currLect, 'assignedCourse':assignedCourse, 'learningMaterials':learningMaterials}
    return render(request, 'lecturer/lect_learning_material.html', context)

@login_required(login_url='login')
def deleteLearningMaterial(request, pk, course_pk, learnMat_pk):
    currLect = User.objects.get(id=pk)
    assignedCourse = Course.objects.get(id=course_pk)
    learningMaterials = LearningMaterial.objects.get(id=learnMat_pk)
    if request.method == "POST":
        learningMaterials.delete()
        return redirect('lect-learning-material', currLect.id, assignedCourse.id)

    context = {'currLect':currLect, 'assignedCourse':assignedCourse, 'learningMaterials':learningMaterials}
    return render(request, 'lecturer/delete_learning_material.html', context)


@login_required(login_url='login')
def lectAssignment(request, pk, course_pk):
    currLect = User.objects.get(id=pk)
    assignedCourse = Course.objects.get(id=course_pk)
    assignments = Assignment.objects.all()
    form = CreateAssignment(initial={'course':assignedCourse})

    if request.method == 'POST':
        form = CreateAssignment(request.POST, request.FILES)
        if form.is_valid():
            form.save()

    context = {'form':form, 'assignments':assignments, 'currLect':currLect, 'assignedCourse':assignedCourse}
    return render(request, 'lecturer/lect-assignment.html', context)

@login_required(login_url='login')
def updateAssignment(request, pk, course_pk, assignment_pk):
    currLect = User.objects.get(id=pk)
    assignedCourse = Course.objects.get(id=course_pk)
    assignments = Assignment.objects.get(id=assignment_pk)
    form = CreateAssignment(instance=assignments)
    if request.method == 'POST':
        form = CreateAssignment(request.POST, instance=assignments)
        if form.is_valid():
            form.save()
            return redirect('lect-assignment', currLect.id, assignedCourse.id)

    context = {'form':form, 'currLect':currLect, 'assignedCourse':assignedCourse, 'assignments':assignments}
    return render(request, 'lecturer/update_assignment.html', context)

@login_required(login_url='login')
def deleteAssignment(request, pk, course_pk, assignment_pk):
    currLect = User.objects.get(id=pk)
    assignedCourse = Course.objects.get(id=course_pk)
    assignments = Assignment.objects.get(id=assignment_pk)
    if request.method == "POST":
        assignments.delete()
        return redirect('lect-assignment', currLect.id, assignedCourse.id)

    context = {'currLect':currLect, 'assignedCourse':assignedCourse, 'assignments':assignments}
    return render(request, 'lecturer/delete_assignment.html', context)

@login_required(login_url='login')
def lectAssignmentSubmitted(request, pk, course_pk, assignment_pk):
    currLect = User.objects.get(id=pk)
    assignedCourse = Course.objects.get(id=course_pk)
    assignments = Assignment.objects.get(id=assignment_pk)

    context = {'currLect':currLect, 'assignedCourse':assignedCourse, 'assignments':assignments}
    return render(request, 'lecturer/lect-assignment-submitted.html', context)

@login_required(login_url='login')
def lectQuiz(request, pk):
    currLect = User.objects.get(id=pk)
    assignedCourse = Course.objects.get(user_id=currLect.id)
    context = {'currLect':currLect, 'assignedCourse':assignedCourse}
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
def studentDashboard(request, pk):
    currStudent = User.objects.get(id=pk)
    context = {'currStudent':currStudent}
    context = {}
    return render(request, 'student/student_dashboard.html', context)

@login_required(login_url='login')
def registerCourse(request, pk):
    currStudent = User.objects.get(id=pk)
    courses = Course.objects.all()
    context = {'currStudent':currStudent, 'courses': courses}
    return render(request, 'student/register-course.html', context)


@login_required(login_url='login')
def registerCourseConfirm(request, pk, course_pk):
    currStudent = User.objects.get(id=pk)
    courses = Course.objects.get(id=course_pk)

    # form = selectedCourse(instance=courses)

    # if request.method == "POST":
    #     form = selectedCourse(request.POST, instance=courses)
    #     if form.is_valid():
    #         form.save()

    context = {'currStudent':currStudent, 'courses': courses}
    return render(request, 'student/register_course_confirm.html', context)

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