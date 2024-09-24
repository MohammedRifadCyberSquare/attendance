from django.shortcuts import render,redirect
from teacher.models import Teacher
from io import BytesIO
import json
from django.utils import timezone
import numpy as np
from django.http import JsonResponse
from PIL import Image
from teacher.models import Students,Attendance
import face_recognition



def landing(request):

    message = ''
    if request.method == 'POST':
        staff_id = request.POST['staff_id']
        password = request.POST['password']

        teacher = Teacher.objects.filter(staff_id = staff_id, password = password)

        if teacher:
            request.session['class'] = teacher[0].teacher_class
            request.session['division'] = teacher[0].division
            request.session['teacher_name'] = teacher[0].teacher_name
             
            return redirect('teacher:dashboard')

        else:
            print('here')
            message = 'User Name or Password Incorrect'
    return render(request,'LandingPage.html',{'message': message})

def mark_attendance(request):
    if request.method == 'POST':
        # student = 1
        # current_date = timezone.now().strftime("%d/%m/%Y")
        # current_time = timezone.now().time().strftime("%I:%M:%S %p")

        # print(current_date, current_time)

        # attendance_record = Attendance(
        #     student_id = student,
        #     date = current_date,
        #     time = current_time
        # )
        # print('hhhhhhhh')
        # attendance_record.save()
        # return JsonResponse({'success': True})

        image_file = request.FILES['image']
        print(image_file)
        image_data = image_file.read()
        image = Image.open(BytesIO(image_data))
        image_array = np.array(image)

        try:
            new_face_encodings = face_recognition.face_encodings(image_array)
            new_face_encoding = new_face_encodings[0] 
            print(request.POST['class'], request.POST['division'])
            students = Students.objects.filter(student_class = request.POST['class'],
                        division = request.POST['division']
                        )
            
            for student in students:
                # Decode the stored face encoding from JSON
                stored_face_encoding = json.loads(student.face_encoding)
                matches = face_recognition.compare_faces([stored_face_encoding], new_face_encoding)
                if matches[0]:  # If a match is found
                    return JsonResponse({
                        'success': True,
                        'student_name': student.student_name,
                        'admission_no': student.admission_no,
                    })
        #     print(matches[0],'====')
            return JsonResponse({'success': False, 'error': 'No match found.'})
        except:
            print('hhhhhhhhhhhhhh')
            return JsonResponse({'success': False, 'error': 'Something Went Wrong.....'})

    return render(request,'MarkAttendance.html')