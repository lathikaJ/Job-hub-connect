from django.urls import path
from . import views

urlpatterns = [
    path('apply/', views.apply_job, name='apply-job'),
    path('my-applications/', views.my_applications, name='my-applications'),
    path('job/<int:job_id>/applications/', views.job_applications, name='job-applications'),
    path('<int:application_id>/update-status/', views.update_application_status, name='update-application-status'),
]