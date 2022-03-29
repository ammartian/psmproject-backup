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

    # django required fields
    active = models.BooleanField(default=True) # so can login
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
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_admin(self): #superuser
        return self.admin

    @property
    def is_active(self): #active
        return self.active

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
#class Admins(models.Model):
#    user = models.OneToOneField(User)
