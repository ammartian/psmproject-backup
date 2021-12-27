from django.urls import path
from . import views

urlpatterns = [
    #login
    path('', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),


    #base
    path('dashboard/', views.dashboard , name='dashboard'),
    path('change-email/', views.changeEmail, name="change-email"),
    path('change-password/', views.changePassword, name="change-password"),
    path('session/', views.sessionManagement, name="session-management"),

    
    #admin
    path('manage-course/', views.manageCourse, name="manage-course"),
    path('manage-lecturer/', views.manageLecturer, name="manage-lecturer"),
    path('manage-student/', views.manageStudent, name="manage-student"),

    #lecturer


    #student
]