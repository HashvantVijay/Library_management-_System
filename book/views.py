from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.db.models import Q 
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.db import connection

# Create your views here.
def booklisting(request):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM book, author, publication WHERE publication_id = book_publication_id AND author_id = book_author_id")
    booklist = dictfetchall(cursor)

    context = {
        "booklist": booklist
    }
    context['heading'] = "Book Details";
    return render(request, 'book-view.html', context)

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
    cursor.execute("SELECT * FROM book WHERE book_id = " + id)
    dataList = dictfetchall(cursor)
    return dataList[0];

def update(request, bookId):
    context = {
        "fn": "update",
        "bookDetails": getData(bookId),
        "authorlist": getDropDown('author', 'author_id'),
        "publicationlist": getDropDown('publication', 'publication_id'),
        "categorylist": getDropDown('category', 'category_id'),
        "languagelist": getDropDown('language', 'language_id'),
        "heading": 'Book Update',
    }
    if (request.method == "POST"):
        cursor = connection.cursor()
        cursor.execute("""
                   UPDATE book
                   SET book_author_id=%s, book_publication_id=%s, book_category_id=%s, book_language_id=%s,
		   book_title=%s, book_isbn=%s, book_edition=%s, book_edition_year=%s, book_number_copies=%s,
		   book_volume=%s, book_date_purchase=%s, book_price=%s, book_description=%s
		   WHERE book_id = %s
                """, (
            request.POST['book_author_id'],
            request.POST['book_publication_id'],
            request.POST['book_category_id'],
            request.POST['book_language_id'],
            request.POST['book_title'],
            request.POST['book_isbn'],
            request.POST['book_edition'],
            request.POST['book_edition_year'],
            request.POST['book_number_copies'],
            request.POST['book_volume'],
            request.POST['book_date_purchase'],
            request.POST['book_price'],
            request.POST['book_description'],
            bookId
        ))
        context["bookDetails"] =  getData(bookId)
        messages.add_message(request, messages.INFO, "Book updated succesfully !!!")
        return redirect('booklisting')
    else:
        return render(request, 'book-add.html', context)


def add(request):
    context = {
        "fn": "add",
        "authorlist": getDropDown('author', 'author_id'),
        "publicationlist": getDropDown('publication', 'publication_id'),
        "categorylist": getDropDown('category', 'category_id'),
        "languagelist": getDropDown('language', 'language_id'),
        "heading": 'Add Book'
    };
    if (request.method == "POST"):
        cursor = connection.cursor()
        cursor.execute("""
		   INSERT INTO book
		   SET book_author_id=%s, book_publication_id=%s, book_category_id=%s, book_language_id=%s,
		   book_title=%s, book_isbn=%s, book_edition=%s, book_edition_year=%s, book_number_copies=%s,
		   book_volume=%s, book_date_purchase=%s, book_price=%s, book_description=%s
		""", (
            request.POST['book_author_id'],
            request.POST['book_publication_id'],
            request.POST['book_category_id'],
            request.POST['book_language_id'],
            request.POST['book_title'],
            request.POST['book_isbn'],
            request.POST['book_edition'],
            request.POST['book_edition_year'],
            request.POST['book_number_copies'],
            request.POST['book_volume'],
            request.POST['book_date_purchase'],
            request.POST['book_price'],
            request.POST['book_description']))
        return redirect('booklisting')
    return render(request, 'book-add.html', context)

def delete(request, id):
    cursor = connection.cursor()
    sql = 'DELETE FROM book WHERE book_id=' + id
    cursor.execute(sql)
    return redirect('booklisting')
