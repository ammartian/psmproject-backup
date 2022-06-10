#Create proper form for admin/
from dataclasses import field
from datetime import date, datetime
from urllib import request
from xmlrpc.client import DateTime
from django import forms
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.hashers import check_password
#from django.utils import timezone
#for CRUD
from django.forms import DateTimeInput, HiddenInput, ModelForm
from django.shortcuts import redirect
from .models import *

User = get_user_model()

# Register your models here.

class UserAdminCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    password = forms.CharField(widget=forms.PasswordInput)
    password_2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email'] #required fields

    def clean(self):
        '''
        Verify both passwords match.
        '''
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")
        if password is not None and password != password_2:
            self.add_error("password_2", "Your passwords must match")
        return cleaned_data

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ['email', 'password', 'admin'] #'is_active' is removed

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class ChangeProfilePicture(ModelForm):
    class Meta:
        model = User
        fields = ('profile_picture'),


class createCourse(forms.ModelForm):

    disabled_fields = ('admin_create',)

    class Meta:
        model = Course
        fields = '__all__'
        # exclude = ['name'] <- TO EXCLUDE AN ATTRIBUTE

    #HIDE THE INPUT AND JUST USE <p> TO DISPLAY THE COURSE NAME
    def __init__(self, *args, **kwargs):
        super(createCourse, self).__init__(*args, **kwargs)
        for field in self.disabled_fields:
            self.fields[field].widget = HiddenInput()

class assignLecturertoCourse(forms.ModelForm):

    # disabled_fields = ('course',)
    
    #READ-ONLY FIELD
    #course = forms.CharField(widget = forms.TextInput(attrs={'readonly':'readonly'}))

    class Meta:
        model = AssignLecturer
        fields = ('course', 'lecturer_assigned')
        labels = {
            'lecturer_assigned': ('Lecturer'),
        }

    #HIDE THE INPUT AND JUST USE <p> TO DISPLAY THE COURSE NAME
    # def __init__(self, *args, **kwargs):
    #     super(assignLecturertoCourse, self).__init__(*args, **kwargs)
    #     for field in self.disabled_fields:
    #         # self.fields[field].widget.attrs['disabled'] = 'disabled'
    #         self.fields[field].widget = HiddenInput()

class selectedCourse(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'

class ConfirmPasswordForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('confirm_password', )

    def clean(self):
        cleaned_data = super(ConfirmPasswordForm, self).clean()
        confirm_password = cleaned_data.get('confirm_password')

        if not check_password(confirm_password, self.instance.password):
            messages.error('confirm_password', 'Password does not match.')
        else:
            return redirect('change-email')

    # def save(self, commit=True):
    #     user = super(ConfirmPasswordForm, self).save(commit)
    #     #user.last_login = timezone.now()
    #     if commit:
    #         user.save()
    #     return user

class createLecturer(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    password = forms.CharField(widget=forms.PasswordInput)
    password_2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    lecturer = forms.BooleanField(widget=forms.HiddenInput())

    class Meta:
        model = User
        fields = ['name', 'unique_id', 'email', 'lecturer'] #required fields
        # exclude = ['name'] <- TO EXCLUDE AN ATTRIBUTE

    def clean(self):
        '''
        Verify both passwords match.
        '''
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")
        if password is not None and password != password_2:
            self.add_error("password_2", "Your passwords must match")
        return cleaned_data

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class createStudent(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    password = forms.CharField(widget=forms.PasswordInput)
    password_2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    student = forms.BooleanField(widget=forms.HiddenInput())

    class Meta:
        model = User
        fields = ['name', 'unique_id', 'email', 'student'] #required fields

    def clean(self):
        '''
        Verify both passwords match.
        '''
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")
        if password is not None and password != password_2:
            self.add_error("password_2", "Your passwords must match")
        return cleaned_data

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class EmailChangeForm(forms.Form):
    """
    A form that lets a user change set their email while checking for a change in the 
    e-mail.
    """
    error_messages = {
        'email_mismatch': ("The two email addresses fields didn't match."),
        'not_changed': ("The email address is the same as the one already defined."),
    }

    success_messages = {
        'success': ("Email changed successfully."),
    }

    new_email1 = forms.EmailField(
        label=("New email address"),
        widget=forms.EmailInput,
    )

    new_email2 = forms.EmailField(
        label=("New email address confirmation"),
        widget=forms.EmailInput,
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(EmailChangeForm, self).__init__(*args, **kwargs)

    def clean_new_email1(self):
        old_email = self.user.email
        new_email1 = self.cleaned_data.get('new_email1')
        if new_email1 and old_email:
            if new_email1 == old_email:
                raise forms.ValidationError(
                    self.error_messages['not_changed'],
                    code='not_changed',
                )
        return new_email1

    def clean_new_email2(self):
        new_email1 = self.cleaned_data.get('new_email1')
        new_email2 = self.cleaned_data.get('new_email2')
        if new_email1 and new_email2:
            if new_email1 != new_email2:
                raise forms.ValidationError(
                    self.error_messages['email_mismatch'],
                    code='email_mismatch',
                )
        return new_email2

    def save(self, commit=True):
        email = self.cleaned_data["new_email1"]
        self.user.email = email
        if commit:
            self.user.save()
        return self.user


#Create Learning Material
class CreateLearningMaterial(forms.ModelForm):

    disabled_fields = ('assignedLect',)

    class Meta:
        model = LearningMaterial
        fields = ('assignedLect', 'title', 'file')
        

    #HIDE THE INPUT AND JUST USE <p> TO DISPLAY THE COURSE NAME
    def __init__(self, *args, **kwargs):
        super(CreateLearningMaterial, self).__init__(*args, **kwargs)
        for field in self.disabled_fields:
            self.fields[field].widget = HiddenInput()


#Create Assignment
class CreateAssignment(forms.ModelForm):

    # disabled_fields = ('assignedLect',)

    deadline = forms.DateTimeField(widget=forms.widgets.DateTimeInput(attrs={'type': 'datetime-local'}))

    class Meta:
        model = Assignment
        fields = ['assignedLect', 'name', 'deadline', 'file']
        

    # #HIDE THE INPUT AND JUST USE <p> TO DISPLAY THE COURSE NAME
    # def __init__(self, *args, **kwargs):
    #     super(CreateAssignment, self).__init__(*args, **kwargs)
        
    #     for field in self.disabled_fields:
    #         self.fields[field].widget = HiddenInput()
