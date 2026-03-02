from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from .models import Job, Company
import datetime
import json

@api_view(['GET'])
@permission_classes([AllowAny])
def job_list(request):
    jobs = Job.objects.filter(is_active=True)
    
    # Simple search
    search = request.GET.get('search', '')
    if search:
        jobs = jobs.filter(title__icontains=search) | jobs.filter(description__icontains=search) | jobs.filter(company__name__icontains=search)
    
    # Simple filter by location
    location = request.GET.get('location', '')
    if location:
        jobs = jobs.filter(location__icontains=location)
    
    # Simple filter by job type
    job_type = request.GET.get('job_type', '')
    if job_type:
        jobs = jobs.filter(job_type=job_type)
    
    job_data = []
    for job in jobs:
        job_data.append({
            'id': job.id,
            'title': job.title,
            'company_name': job.company.name,
            'location': job.location,
            'job_type': job.job_type,
            'salary_min': float(job.salary_min) if job.salary_min else None,
            'salary_max': float(job.salary_max) if job.salary_max else None,
            'experience_min': job.experience_min,
            'experience_max': job.experience_max,
            'posted_date': job.posted_date.strftime('%Y-%m-%d') if job.posted_date else None,
        })
    
    return Response(job_data)

@api_view(['GET'])
@permission_classes([AllowAny])
def job_detail(request, job_id):
    try:
        job = Job.objects.get(id=job_id)
        job_data = {
            'id': job.id,
            'title': job.title,
            'company_name': job.company.name,
            'company_description': job.company.description,
            'description': job.description,
            'requirements': job.requirements,
            'skills_required': job.skills_required,
            'location': job.location,
            'job_type': job.job_type,
            'salary_min': float(job.salary_min) if job.salary_min else None,
            'salary_max': float(job.salary_max) if job.salary_max else None,
            'experience_min': job.experience_min,
            'experience_max': job.experience_max,
            'vacancies': job.vacancies,
            'posted_date': job.posted_date.strftime('%Y-%m-%d') if job.posted_date else None,
            'application_deadline': job.application_deadline.strftime('%Y-%m-%d') if job.application_deadline else None,
        }
        return Response(job_data)
    except Job.DoesNotExist:
        return Response({'error': 'Job not found'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_job(request):
    if request.user.user_type != 'employer':
        return Response({'error': 'Only employers can post jobs'}, status=403)
    
    try:
        # Get or create company based on employer's profile
        employer_profile = request.user.employerprofile
        company, created = Company.objects.get_or_create(
            name=employer_profile.company_name,
            defaults={
                'description': employer_profile.company_description or f"Company profile for {employer_profile.company_name}",
                'industry': 'Technology',  # Default industry
                'employee_count': 50,  # Default value
                'founded_year': 2020,  # Default value
                'website': employer_profile.company_website or ''
            }
        )
        
        # Create the job
        job = Job.objects.create(
            title=request.data.get('title'),
            company=company,
            description=request.data.get('description'),
            requirements=request.data.get('requirements'),
            skills_required=request.data.get('skills_required'),
            location=request.data.get('location'),
            job_type=request.data.get('job_type'),
            salary_min=request.data.get('salary_min'),
            salary_max=request.data.get('salary_max'),
            experience_min=request.data.get('experience_min', 0),
            experience_max=request.data.get('experience_max', 5),
            vacancies=request.data.get('vacancies', 1),
            posted_by=request.user,
            application_deadline=request.data.get('application_deadline')
        )
        
        return Response({
            'message': 'Job posted successfully!',
            'job_id': job.id,
            'job_title': job.title
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def employer_jobs(request):
    if request.user.user_type != 'employer':
        return Response({'error': 'Only employers can access this'}, status=403)
    
    jobs = Job.objects.filter(posted_by=request.user)
    job_data = []
    for job in jobs:
        job_data.append({
            'id': job.id,
            'title': job.title,
            'company_name': job.company.name,
            'location': job.location,
            'job_type': job.job_type,
            'salary_min': job.salary_min,
            'salary_max': job.salary_max,
            'is_active': job.is_active,
            'posted_date': job.posted_date,
            'application_count': job.jobapplication_set.count()
        })
    
    return Response(job_data)