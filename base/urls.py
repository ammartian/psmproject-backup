from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    #login
    path('', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('forgot-password/', views.forgotPassword, name="forgot-password"),
    path('first-time-login/', views.firstTimeLogin, name="first-time-login"),
    path('set-new-password/', views.setNewPassword, name="set-new-password"),


    #reset password with email
    path('reset_password/', auth_views.PasswordResetView.as_view(), name="reset_password"), #submit email form
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"), #email sent success message
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"), #link to password Rest form in mail
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"), #password successfully changed message


    #all
    path('user_profile/<str:pk>/', views.userProfile, name='user-profile'),
    path('dashboard/<str:pk>/', views.adminDashboard , name='admin-dashboard'),
    path('change-email/<str:pk>/', views.changeEmail, name="change-email"),
    #path('change-password/', views.changePassword, name="change-password"),
    #Password reset link (ref: https://github.com/django/django/blob/master/django/contrib/auth/views.py)
    path('change-password/done/', auth_views.PasswordChangeDoneView.as_view(), name="password_change_done"),
    path('change-password/', auth_views.PasswordChangeView.as_view(), name="password_change"),
    path('session/<str:pk>/', views.sessionManagement, name="session-management"),
    path('reenter-email/', views.checkChangeEmail, name="reenter-email"),

    
    #admin
    path('manage-course/', views.manageCourse, name="manage-course"),
    path('update-course/<str:pk>/', views.updateCourse, name="update-course"),
    path('delete-course/<str:pk>/', views.deleteCourse, name="delete-course"),
    path('manage-lecturer/', views.manageLecturer, name="manage-lecturer"),
    path('update-lecturer/<str:pk>/', views.updateLecturer, name="update-lecturer"),
    path('delete-lecturer/<str:pk>/', views.deleteLecturer, name="delete-lecturer"),
    path('manage-student/', views.manageStudent, name="manage-student"),
    path('update-student/<str:pk>/', views.updateStudent, name="update-student"),
    path('delete-student/<str:pk>/', views.deleteStudent, name="delete-student"),

    #lecturer
    path('lecturer-dashboard/<str:pk>/', views.lecturerDashboard, name="lecturer-dashboard"),
    path('lect-learning-material/<str:pk>/', views.lectLearningMaterial, name="lect-learning-material"),
    path('lect-assignment/<str:pk>/', views.lectAssignment, name="lect-assignment"),
    path('lect-assignment-submitted/', views.lectAssignmentSubmitted, name="lect-assignment-submitted"),
    path('lect-quiz/<str:pk>/', views.lectQuiz, name="lect-quiz"),
    path('lect-create-quiz/', views.lectCreateQuiz, name="lect-create-quiz"),
    path('lect-quiz-content/', views.lectQuizContent, name="lect-quiz-content"),
    path('lect-edit-quiz/<', views.lectEditQuiz, name="lect-edit-quiz"),
    path('lect-quiz-answered/', views.lectQuizAnswered, name="lect-quiz-answered"),

    #student
    path('student_dashboard/<str:pk>/', views.studentDashboard, name="student-dashboard" ),
    path('register-course/', views.registerCourse, name="register-course" ),
    path('course-details/', views.courseDetails, name="course-details" ),
    path('stud-assignment-details/', views.studAssignmentDetails, name="stud-assignment-details" ),
    path('stud-quiz-details/', views.studQuizDetails, name="stud-quiz-details" ),

]