from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.db import connection
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request,'login.html')

# Create your views here.
def employeelisting(request):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM employee_employee")
    employeelist = dictfetchall(cursor)

    context = {
        "employeelist": employeelist
    }
    context['heading'] = "All Employee Record";
    return render(request,'employee-record.html', context)

def getData(id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM employee_employee WHERE employee_id = " + id)
    dataList = dictfetchall(cursor)
    return dataList[0];

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def update(request, employeeId):
    context = {
        "fn": "update",
        "employeedetails": getData(employeeId),
        "heading": 'Employee Update',
    }
    if (request.method == "POST"):
        cursor = connection.cursor()
        cursor.execute("""
                   UPDATE employee_employee
		   SET employee_user=%s, employee_password=%s, employee_first_name=%s, employee_middle_name=%s,
		   employee_last_name=%s, employee_gender=%s, employee_address=%s, employee_village=%s, employee_mobile=%s,
		   employee_email=%s, employee_dob=%s, employee_nationalty=%s
		 WHERE employee_id=%s""", (
            request.POST['employee_user'],
            request.POST['employee_password'],
            request.POST['employee_first_name'],
            request.POST['employee_middle_name'],            
            request.POST['employee_last_name'],
            request.POST['employee_gender'],
            request.POST['employee_address'],
            request.POST['employee_village'],
            request.POST['employee_mobile'],
            request.POST['employee_email'],
            request.POST['employee_dob'],
            request.POST['employee_nationalty'],
            employeeId
        ))
        context["employeedetails"] =  getData(employeeId)
        messages.add_message(request, messages.INFO, "Employee updated succesfully !!!")
        return redirect('employeelisting')
    else:
        return render(request, 'employee-add.html', context)

def add(request):
    context = {
        "fn": "add",
        "heading": 'Add Employee'
    };
    if (request.method == "POST"):
        cursor = connection.cursor()
        cursor.execute("""
		   INSERT INTO employee_employee
		   SET employee_user=%s, employee_password=%s, employee_first_name=%s, employee_middle_name=%s,
		   employee_last_name=%s, employee_gender=%s, employee_address=%s, employee_village=%s, employee_mobile=%s,
		   employee_email=%s, employee_dob=%s, employee_nationalty=%s
		""", (
            request.POST['employee_user'],
            request.POST['employee_password'],
            request.POST['employee_first_name'],
            request.POST['employee_middle_name'],            
            request.POST['employee_last_name'],
            request.POST['employee_gender'],
            request.POST['employee_address'],
            request.POST['employee_village'],
            request.POST['employee_mobile'],
            request.POST['employee_email'],
            request.POST['employee_dob'],
            request.POST['employee_nationalty']))
        return redirect('employeelisting')
    return render(request, 'employee-add.html', context)



def delete(request, id):
    cursor = connection.cursor()
    sql = 'DELETE FROM employee_employee WHERE employee_id=' + id
    cursor.execute(sql)
    return redirect('employeelisting')
