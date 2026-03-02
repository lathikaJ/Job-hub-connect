from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('profile/jobseeker/', views.JobSeekerProfileView.as_view(), name='jobseeker-profile'),
    path('profile/employer/', views.EmployerProfileView.as_view(), name='employer-profile'),
    # Add these new endpoints for profile updates
    path('profile/update/', views.update_user_profile, name='update-user-profile'),
    path('profile/jobseeker/update/', views.update_jobseeker_profile, name='update-jobseeker-profile'),
    path('profile/employer/update/', views.update_employer_profile, name='update-employer-profile'),
]