from django.shortcuts import render,redirect
import face_recognition
import json

from teacher.decorator import login_required
from .models import *
# Create your views here.

@login_required
def dashboard(request):
    student_count = Students.objects.filter(student_class = request.session['class'],
                                         division = request.session['division']).count()
    
    return render(request,'teacher/dashboard.html',{'student_count':student_count})

@login_required
def view_student_list(request):
    students = Students.objects.filter(student_class = request.session['class'],
                                         division = request.session['division'])
    return render(request,'teacher/student_list.html',{'students':students})

@login_required
def add_student(request):
    message = ''
    if request.method == 'POST':
        student_name = request.POST['student_name']
        admission_no = request.POST['admission_no']
        student_pic = request.FILES['pic']

        student_class = request.session['class']
        student_division = request.session['division']

        student = Students(student_name = student_name, 
                           admission_no = admission_no, student_class = student_class, 
                           division = student_division, pic = student_pic )
        
        student.save()
        student_image = face_recognition.load_image_file(student.pic.path)

        # Get face encodings
        face_encodings = face_recognition.face_encodings(student_image)
        face_encoding = face_encodings[0]
        student.face_encoding = json.dumps(face_encoding.tolist())  # Convert to JSON string

        # Save the updated student record with the face encoding
        student.save()
        message = 'Student Registered Succesfully'
    return render(request,'teacher/add_student.html', {'message': message,})

def logout(request):
    del request.session['class']  
    del request.session['division']  
    del request.session['teacher_name'] 
    request.session.flush()
    return redirect('student:landing')
             