from django.urls import path
from . import views

app_name = 'teacher'
urlpatterns = [
    path('dashboard', views.dashboard, name = 'dashboard'),
    path('register/student', views.add_student, name = 'add_student'),
    path('students/list', views.view_student_list, name = 'student_list'),
    path('logout', views.logout, name = 'logout'),

     
]