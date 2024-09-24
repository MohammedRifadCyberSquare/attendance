from django.urls import path
from . import views

app_name = 'student'
urlpatterns = [
    path('', views.landing, name = 'landing'),
    path('mark/attendance', views.mark_attendance, name = 'mark_attendance')
]