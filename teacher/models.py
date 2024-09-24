from django.db import models
from django.utils import timezone
from datetime import datetime
# Create your models here.

class Teacher(models.Model):
    staff_id = models.IntegerField()
    teacher_name = models.CharField(max_length = 50)
    teacher_class = models.IntegerField()
    division = models.CharField(max_length = 10)
    # last_active = models.DateTimeField(default=timezone.now, null=True)
    password = models.CharField(max_length = 100)

    class Meta:
        db_table = "teacher"

class Students(models.Model):
    admission_no = models.IntegerField()
    student_name = models.CharField(max_length = 100)
    student_class = models.IntegerField()
    division = models.CharField(max_length = 10)
    pic = models.ImageField(upload_to = 'students/')
    face_encoding = models.TextField() 

    class Meta:
        db_table = "student"

class Attendance(models.Model):
    student = models.ForeignKey(Students, on_delete = models.CASCADE)
    date = models.DateField()
    time = models.CharField(default = '')
    status = models.CharField(default = 'present')
    
    def save(self, *args, **kwargs):
        # If the date is provided in string format, convert it to YYYY-MM-DD
        if isinstance(self.date, str):
            try:
                # Convert DD/MM/YYYY format to a Python date object
                self.date = datetime.strptime(self.date, '%d/%m/%Y').date()
                print(self.date,'////////')
            except ValueError:
                raise ValueError("Incorrect date format, should be DD/MM/YYYY")

        # Continue with the normal save process
        super().save(*args, **kwargs)

    class Meta:
        db_table = "attendance"