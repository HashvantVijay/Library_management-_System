from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.db.models import Q 
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.db import connection

# Create your views here.
def categorylisting(request):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM category")
    categorylist = dictfetchall(cursor)

    context = {
        "categorylist": categorylist
    }
    context['heading'] = "Category Details";
    return render(request, 'category-view.html', context)

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
    cursor.execute("SELECT * FROM category WHERE category_id = " + id)
    dataList = dictfetchall(cursor)
    return dataList[0];

def update(request, categoryId):
    context = {
        "fn": "update",
        "categoryDetails": getData(categoryId),
        "heading": 'Category Update',
    }
    if (request.method == "POST"):
        cursor = connection.cursor()
        cursor.execute("""
                   UPDATE category
                   SET category_name=%s, category_description=%s
		   WHERE category_id = %s
                """, (
            request.POST['category_name'],
            request.POST['category_description'],
            categoryId
        ))
        context["categoryDetails"] =  getData(categoryId)
        messages.add_message(request, messages.INFO, "Category updated succesfully !!!")
        return redirect('categorylisting')
    else:
        return render(request, 'category-add.html', context)


def add(request):
    context = {
        "fn": "add",
        "heading": 'Add Category'
    };
    if (request.method == "POST"):
        cursor = connection.cursor()
        cursor.execute("""
		   INSERT INTO category
		   SET category_name=%s, category_description=%s
		""", (
            request.POST['category_name'],
            request.POST['category_description']))
        return redirect('categorylisting')
    return render(request, 'category-add.html', context)

def delete(request, categoryId):
    cursor = connection.cursor()
    sql = 'DELETE FROM category WHERE category_id=' + categoryId
    cursor.execute(sql)
    return redirect('categorylisting')