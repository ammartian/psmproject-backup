from ast import Assign
from django.db import models
from django.contrib.auth.models import ( #to custom our own user model
    AbstractBaseUser, BaseUserManager
)

# Create your models here.

class UserManager(BaseUserManager):
    pass
    def create_user(self, email, password=None, is_active=True, is_admin=False, is_staff=False, is_lecturer=False, is_student=False): # THIS IS A REQUIRED_FIELDS TO CREATE USER
        if not email:
            raise ValueError("Email is required")
        if not password:
            raise ValueError("Password is required")

        user_obj = self.model(
            email = self.normalize_email(email)
        )

        user_obj.set_password(password)
        user_obj.active = is_active
        user_obj.admin = is_admin
        user_obj.staff = is_staff
        user_obj.lecturer = is_lecturer
        user_obj.student = is_student

        user_obj.save(using=self.db)
#         return user_obj
        
    # Create admin
    def create_staffuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
            is_staff=True
        )
        return user

        # Create superuser
    def create_superuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
            is_admin=True,
            is_staff=True
        )
        return user

    # Create lecturer
    def create_lectureruser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
            is_lecturer=True
        )
        return user

    # Create student
    def create_studentuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
            is_student=True
        )
        return user
    


class User(AbstractBaseUser):
    email = models.EmailField(unique=True, max_length=255)
    alt_email = models.EmailField(unique=True, max_length=255, null=True) #KIV: unique can be null?
    unique_id = models.CharField(unique=True, max_length=20) #KIV use in db
    name = models.CharField(max_length=100, blank=True) #boleh blank bila save
    date_created = models.DateTimeField(auto_now_add=True) #capture created time
    profile_picture = models.ImageField(default="default_user.jpg" ,null=True, blank=True)

    # django required fields
    is_active = models.BooleanField(default=True) # so can login
    admin = models.BooleanField(default=False) # for superuser

    # Our user type
    staff = models.BooleanField(default=False) # Django built-in, use it as admin (not superuser)
    lecturer = models.BooleanField(default=False) # for lecturer
    student = models.BooleanField(default=False) # for student

    USERNAME_FIELD ='email' #for login
    # Django built-in: username(email) and password are required by default
    REQUIRED_FIELDS = [] # for create superuser
    # our own required fields for creating superuser

    # To use BaseUserManager (Django built-in)
    objects = UserManager()

    # Important bcs syntax #maybe ni kena property?
    def __str__(self):
        return self.email

    # Django built-in: default method by django (function)
    def get_full_name(self):
        return self.name
    
    def get_short_name(self):
        return self.name

    def has_perm(self, perm, obj=None):
        return True #because we're not using built-in django model

    def has_module_perms(self, app_label):
        return True #because we're not using built-in django model

    @property
    def is_admin(self): #superuser
        return self.admin

    # @property
    # def is_active(self): #active
    #     return self.active

    # Our own return value
    @property
    def is_staff(self): #admin
        return self.staff

    @property
    def is_lecturer(self): #lecturer
        return self.lecturer

    @property
    def is_student(self): #student
        return self.student


#TO EXTENDS EXTRA DATA FOR SPECIFIC USER TYPE
# class Admins(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     staff = models.BooleanField(default=True)

# class Lecturers(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     lecturer = models.BooleanField(default=True)

# class Students(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     student = models.BooleanField(default=True)


#COURSE MODELS
class Course(models.Model):
    admin_create = models.ForeignKey(User, limit_choices_to={'staff': True}, null=True, on_delete=models.SET_NULL)
    course_Name = models.CharField(max_length=200, null=True)
    course_ID = models.CharField(unique=True, max_length=200, null=True)
    course_Credit = models.IntegerField(null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self): 
        return self.course_Name


class AssignLecturer(models.Model):
    lecturer_assigned = models.ForeignKey(User, limit_choices_to={'lecturer': True}, null=True, on_delete=models.SET_NULL)
    course = models.ForeignKey(Course, null=True, on_delete=models.SET_NULL)
    

# LEARNING MATERIAL MODELS
class LearningMaterial(models.Model):
    assignedLect = models.ForeignKey(AssignLecturer, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=200, null=True)
    file = models.FileField(upload_to='learning materials/')

    def __str__(self):
        return self.title

#ASSIGNMENT MODELS
class Assignment(models.Model):
    assignedLect = models.ForeignKey(AssignLecturer, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200, null=True)
    deadline = models.DateTimeField(null=True, blank=True)
    file = models.FileField(upload_to='assignments/')

    def __str__(self):
        return self.name


#REGISTERED COURSE MODELS
# class RegisteredCourse(models.Model):
#     course = models.ForeignKey(Course, unique=True, null=True, on_delete=models.SET_NULL)
#     user = models.ForeignKey(User, unique=True, null=True, on_delete=models.SET_NULL)

#     def __str__(self):
#         return self.course