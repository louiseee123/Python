from django.shortcuts import render, redirect, get_object_or_404
from .models import Student

# Create your views here.

# Create your views here.
def home(request):
    students = Student.objects.all()
    return render(request, "home.html", {'students': students})

def create_view(request):
    return render(request, "create.html")

def create_student(request):
    if request.method == "POST":
        s_id = request.POST.get("s_id")
        s_name = request.POST.get("s_name")
        s_dept = request.POST.get("s_dept")

        if s_id and s_name and s_dept:
            Student.objects.create(s_id=s_id, s_name=s_name, s_dept=s_dept)
            return redirect("/")
    return render(request, "create.html")

def update_view(request, s_id):
    student = get_object_or_404(Student, s_id=s_id)
    return render(request, "update.html", {'student': student})

def update_student(request, s_id):
    student = get_object_or_404(Student, s_id=s_id)
    if request.method == "POST":
        s_name = request.POST.get("s_name")
        s_dept = request.POST.get("s_dept")

        if s_name and s_dept:
            student.s_name = s_name
            student.s_dept = s_dept
            student.save()
            return redirect("/")
    return render(request, "update.html", {'student': student})

def delete_student(request, s_id):
    student = get_object_or_404(Student, s_id=s_id)
    student.delete()
    return redirect("/")
