from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
from .models import student, city, state, country, course
from django.contrib import messages
from django.db import connection


# Create your views here.

def studentlisting(request):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM student_student, student_course WHERE course_id = student_course_id")
    studentlist = dictfetchall(cursor)

    context = {
        "studentlist": studentlist
    }
    context['heading'] = "Student Records";
    return render(request, 'student-listing.html', context)


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def update(request, studentId):
    context = {
    "fn":"update",
    "citylist":city.objects.all(),
    "statelist":state.objects.all(),
    "courselist":course.objects.all(),
    "studentdetails":student.objects.get(student_id=studentId)
    }
    currentStudentDetails = student.objects.get(student_id = studentId)
    if (request.method == "POST"):
        try:
            student_photo = None
            student_photo = currentStudentDetails.student_photo
            if(request.FILES and request.FILES['student_photo']):
                studentImage = request.FILES['student_photo']
                fs = FileSystemStorage()
                filename = fs.save(studentImage.name, studentImage)
                student_photo = fs.url(studentImage)
            
            addStudent = student(
            student_id = studentId,
            student_roll = request.POST['student_roll'],
            student_name = request.POST['student_name'],
            student_email = request.POST['student_email'],
            student_phone = request.POST['student_phone'],
            student_address = request.POST['student_address'],
            student_gender = request.POST['student_gender'],
            student_dob = request.POST['student_dob'],
            student_city = request.POST['student_city'],
            student_state = request.POST['student_state'],
            student_pincode = request.POST['student_pincode'],
            student_course_id = request.POST['student_course_id'],
            student_admission_date = request.POST['student_admission_date'],
            student_photo = student_photo)
            
            addStudent.save()
        except Exception (e):
            return HttpResponse('Something went wrong. Error Message : '+ str(e))    
        context["studentdetails"] = student.objects.get(student_id=studentId)
        messages.add_message(request, messages.INFO, "Student Record Updated Successfully !!!")
        return redirect('studentlisting')
        #return render(request,'student-add.html', context)
    else:
        return render(request,'student-add.html', context)

def add(request):
    context = {
    "fn":"add",
    "citylist":city.objects.all(),
    "heading":'Student Management',
    "sub_heading": 'Students',
    "statelist":state.objects.all(),
    "courselist":course.objects.all(),
    }
    if (request.method == "POST"):
        try:
            student_photo = None

            if(request.FILES and request.FILES['student_photo']):
                studentImage = request.FILES['student_photo']
                fs = FileSystemStorage()
                filename = fs.save(studentImage.name, studentImage)
                student_photo = fs.url(studentImage)

            addStudent = student(student_name = request.POST['student_name'],
            student_roll = request.POST['student_roll'],
            student_email = request.POST['student_email'],
            student_phone = request.POST['student_phone'],
            student_address = request.POST['student_address'],
            student_gender = request.POST['student_gender'],
            student_dob = request.POST['student_dob'],
            student_city = request.POST['student_city'],
            student_state = request.POST['student_state'],
            student_pincode = request.POST['student_pincode'],
            student_course_id = request.POST['student_course_id'],
            student_admission_date = request.POST['student_admission_date'],
            student_photo = student_photo)
            addStudent.save()
        except Exception (e):
            return HttpResponse('Something went wrong. Error Message : '+ str(e))

        return redirect('studentlisting')

    else:
        return render(request,'student-add.html', context)

def delete(request, studentId):
    cursor = connection.cursor()
    sql = 'DELETE FROM student_student WHERE student_id=' + studentId
    cursor.execute(sql)
    return redirect('studentlisting')