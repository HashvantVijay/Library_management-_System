from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.db.models import Q 
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.db import connection

# Create your views here.
def publicationlisting(request):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM publication")
    publicationlist = dictfetchall(cursor)

    context = {
        "publicationlist": publicationlist
    }
    context['heading'] = "Publication Details";
    return render(request, 'publication-view.html', context)

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
    cursor.execute("SELECT * FROM publication WHERE publication_id = " + id)
    dataList = dictfetchall(cursor)
    return dataList[0];

def update(request, publicationId):
    context = {
        "fn": "update",
        "publicationDetails": getData(publicationId),
        "heading": 'Publication Update',
    }
    if (request.method == "POST"):
        cursor = connection.cursor()
        cursor.execute("""
                   UPDATE publication
                   SET publication_name=%s, publication_contact=%s, publication_address=%s, publication_email=%s 
		   WHERE publication_id = %s
                """, (
            request.POST['publication_name'],
            request.POST['publication_contact'],
            request.POST['publication_address'],
            request.POST['publication_email'],
            publicationId
        ))
        context["publicationDetails"] =  getData(publicationId)
        messages.add_message(request, messages.INFO, "Publication updated succesfully !!!")
        return redirect('publicationlisting')
    else:
        return render(request, 'publication-add.html', context)


def add(request):
    context = {
        "fn": "add",
        "heading": 'Add Publication'
    };
    if (request.method == "POST"):
        cursor = connection.cursor()
        cursor.execute("""
		   INSERT INTO publication
		   SET publication_name=%s, publication_contact=%s, publication_address=%s, publication_email=%s
		""", (
            request.POST['publication_name'],
            request.POST['publication_contact'],
            request.POST['publication_address'],
            request.POST['publication_email']))
        return redirect('publicationlisting')
    return render(request, 'publication-add.html', context)

def delete(request, publicationId):
    cursor = connection.cursor()
    sql = 'DELETE FROM publication WHERE publication_id=' + publicationId
    cursor.execute(sql)
    return redirect('publicationlisting')