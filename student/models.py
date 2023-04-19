# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class student(models.Model):
    student_id = models.AutoField(primary_key=True)
    student_roll = models.CharField(max_length=225, default = "")
    student_name = models.CharField(max_length=225, default = "")
    student_email = models.CharField(max_length=255, default = "")
    student_phone = models.EmailField(max_length=255, default = "")
    student_gender = models.CharField(max_length=10, default = "")
    student_dob = models.CharField(max_length=225, default = "")
    student_city = models.CharField(max_length=255, default = "")
    student_state = models.CharField(max_length=255, default = "")
    student_pincode = models.CharField(max_length=255, default = "")
    student_course_id = models.CharField(max_length=255, default = "")
    student_admission_date = models.CharField(max_length=255, default = "")
    student_address = models.TextField(default = "")
    student_photo = models.CharField(max_length=255, null = True)
    def __str__(self):
        return self.student_name

class state(models.Model):
    state_id = models.AutoField(primary_key=True)
    state_name = models.CharField(max_length=255, default = "")
    def __str__(self):
        return self.state_name

class course(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=255, default = "")
    def __str__(self):
        return self.course_name    

class role(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_title = models.CharField(max_length=255, default = "")
    role_description = models.TextField(default = "")
    def __str__(self):
        return self.state_name

class city(models.Model):
    city_id = models.AutoField(primary_key=True)
    city_name = models.CharField(max_length=255, default = "")
    def __str__(self):
        return self.city_name

class country(models.Model):
    country_id = models.AutoField(primary_key=True)
    country_name = models.CharField(max_length=255, default = "")
    def __str__(self):
        return self.country_name
