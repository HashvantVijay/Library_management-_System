from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.db.models import Q 
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.db import connection

# Create your views here.
def authorlisting(request):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM author")
    authorlist = dictfetchall(cursor)

    context = {
        "authorlist": authorlist
    }
    context['heading'] = "Author Details";
    return render(request, 'author-view.html', context)

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
    cursor.execute("SELECT * FROM author WHERE author_id = " + id)
    dataList = dictfetchall(cursor)
    return dataList[0];

def update(request, authorId):
    context = {
        "fn": "update",
        "authorDetails": getData(authorId),
        "heading": 'Author Update',
    }
    if (request.method == "POST"):
        cursor = connection.cursor()
        cursor.execute("""
                   UPDATE author
                   SET author_name=%s, author_contact=%s, author_email=%s, author_description=%s
		   WHERE author_id = %s
                """, (
            request.POST['author_name'],
            request.POST['author_contact'],
            request.POST['author_email'],
            request.POST['author_description'],
            authorId
        ))
        context["authorDetails"] =  getData(authorId)
        messages.add_message(request, messages.INFO, "Author updated succesfully !!!")
        return redirect('authorlisting')
    else:
        return render(request, 'add.html', context)


def add(request):
    context = {
        "fn": "add",
        "heading": 'Add Author'
    };
    if (request.method == "POST"):
        cursor = connection.cursor()
        cursor.execute("""
		   INSERT INTO author
		   SET author_name=%s, author_contact=%s, author_email=%s, author_description=%s
		""", (
            request.POST['author_name'],
            request.POST['author_contact'],
            request.POST['author_email'],
            request.POST['author_description']))
        return redirect('authorlisting')
    return render(request, 'add.html', context)

def delete(request, authorId):
    cursor = connection.cursor()
    sql = 'DELETE FROM author WHERE author_id=' + authorId
    cursor.execute(sql)
    return redirect('authorlisting')
