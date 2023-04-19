from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.db.models import Q 
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.db import connection

# Create your views here.
def issuelisting(request):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM issue, book, student_student WHERE student_id = issue_to_user_id AND book_id = issue_book_id")
    issuelist = dictfetchall(cursor)

    context = {
        "issuelist": issuelist
    }
    context['heading'] = "Book Issue Details";
    return render(request, 'issue-view.html', context)

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def getDropDown(table, condtion):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM " + table + " WHERE " + condtion)
    dropdownList = dictfetchall(cursor)
    return dropdownList;

def getData(id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM issue WHERE issue_id = " + id)
    dataList = dictfetchall(cursor)
    return dataList[0];

def update(request, issueId):
    context = {
        "fn": "update",
        "issueDetails": getData(issueId),
        "userissuelist": getDropDown('student_student', 'student_id'),
        "bookissuelist": getDropDown('book', 'book_id'),
        "heading": 'Book Issue Update',
    }
    if (request.method == "POST"):
        cursor = connection.cursor()
        cursor.execute("""
                   UPDATE issue
                   SET issue_to_user_id=%s, issue_book_id=%s, issue_date=%s, issue_description=%s 
		   WHERE issue_id = %s
                """, (
            request.POST['issue_to_user_id'],
            request.POST['issue_book_id'],
            request.POST['issue_date'],
            request.POST['issue_description'],
            issueId
        ))
        context["issueDetails"] =  getData(issueId)
        messages.add_message(request, messages.INFO, "Book Issue updated succesfully !!!")
        return redirect('issuelisting')
    else:
        return render(request, 'issue-add.html', context)


def add(request):
    context = {
        "fn": "add",
        "userissuelist": getDropDown('student_student', 'student_id'),
        "bookissuelist": getDropDown('book', 'book_id'),
        "heading": 'Add Book Issue'
    };
    if (request.method == "POST"):
        cursor = connection.cursor()
        cursor.execute("""
		   INSERT INTO issue
		   SET issue_to_user_id=%s, issue_book_id=%s, issue_date=%s, issue_description=%s
		""", (
            request.POST['issue_to_user_id'],
            request.POST['issue_book_id'],
            request.POST['issue_date'],
            request.POST['issue_description']))
        return redirect('issuelisting')
    return render(request, 'issue-add.html', context)

def delete(request, id):
    cursor = connection.cursor()
    sql = 'DELETE FROM issue WHERE issue_id=' + id
    cursor.execute(sql)
    return redirect('issuelisting')
