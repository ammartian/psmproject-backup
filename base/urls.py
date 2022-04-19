from django.urls import path
from . import views

urlpatterns = [
    #login
    path('', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('forgot-password/', views.forgotPassword, name="forgot-password"),
    path('first-time-login/', views.firstTimeLogin, name="first-time-login"),
    path('set-new-password/', views.setNewPassword, name="set-new-password"),



    #all
    path('dashboard/', views.adminDashboard , name='admin-dashboard'),
    path('change-email/', views.changeEmail, name="change-email"),
    path('change-password/', views.changePassword, name="change-password"),
    path('session/<str:pk>/', views.sessionManagement, name="session-management"),
    path('reenter-password/', views.reenterPassword, name="reenter-password"),

    
    #admin
    path('manage-course/', views.manageCourse, name="manage-course"),
    path('manage-lecturer/', views.manageLecturer, name="manage-lecturer"),
    path('manage-student/', views.manageStudent, name="manage-student"),

    #lecturer
    path('lecturer-dashboard/', views.lecturerDashboard, name="lecturer-dashboard"),
    path('lect-learning-material/', views.lectLearningMaterial, name="lect-learning-material"),
    path('lect-assignment/', views.lectAssignment, name="lect-assignment"),
    path('lect-assignment-submitted/', views.lectAssignmentSubmitted, name="lect-assignment-submitted"),
    path('lect-quiz/', views.lectQuiz, name="lect-quiz"),
    path('lect-create-quiz/', views.lectCreateQuiz, name="lect-create-quiz"),
    path('lect-quiz-content/', views.lectQuizContent, name="lect-quiz-content"),
    path('lect-edit-quiz/', views.lectEditQuiz, name="lect-edit-quiz"),
    path('lect-quiz-answered/', views.lectQuizAnswered, name="lect-quiz-answered"),

    #student
    path('student_dashboard/', views.studentDashboard, name="student-dashboard" ),
    path('register-course/', views.registerCourse, name="register-course" ),
    path('course-details/', views.courseDetails, name="course-details" ),
    path('stud-assignment-details/', views.studAssignmentDetails, name="stud-assignment-details" ),
    path('stud-quiz-details/', views.studQuizDetails, name="stud-quiz-details" ),

]