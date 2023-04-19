from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.db.models import Q 
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.db import connection

# Create your views here.
def languagelisting(request):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM language")
    languagelist = dictfetchall(cursor)

    context = {
        "languagelist": languagelist
    }
    context['heading'] = "Language Details";
    return render(request, 'language-view.html', context)

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
    cursor.execute("SELECT * FROM language WHERE language_id = " + id)
    dataList = dictfetchall(cursor)
    return dataList[0];

def update(request, languageId):
    context = {
        "fn": "update",
        "languageDetails": getData(languageId),
        "heading": 'Language Update',
    }
    if (request.method == "POST"):
        cursor = connection.cursor()
        cursor.execute("""
                   UPDATE language
                   SET language_name=%s, language_description=%s
		   WHERE language_id = %s
                """, (
            request.POST['language_name'],
            request.POST['language_description'],
            languageId
        ))
        context["languageDetails"] =  getData(languageId)
        messages.add_message(request, messages.INFO, "Language updated succesfully !!!")
        return redirect('languagelisting')
    else:
        return render(request, 'language-add.html', context)


def add(request):
    context = {
        "fn": "add",
        "heading": 'Add Language'
    };
    if (request.method == "POST"):
        cursor = connection.cursor()
        cursor.execute("""
		   INSERT INTO language
		   SET language_name=%s, language_description=%s
		""", (
            request.POST['language_name'],
            request.POST['language_description']))
        return redirect('languagelisting')
    return render(request, 'language-add.html', context)

def delete(request, languageId):
    cursor = connection.cursor()
    sql = 'DELETE FROM language WHERE language_id=' + languageId
    cursor.execute(sql)
    return redirect('languagelisting')