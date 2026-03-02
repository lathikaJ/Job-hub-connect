from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_list, name='job-list'),
    path('<int:job_id>/', views.job_detail, name='job-detail'),
    path('post/', views.post_job, name='post-job'),
    path('employer/my-jobs/', views.employer_jobs, name='employer-jobs'),
]