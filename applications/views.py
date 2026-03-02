from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import JobApplication
from jobs.models import Job
from users.models import JobSeekerProfile

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def apply_job(request):
    if request.user.user_type != 'job_seeker':
        return Response({'error': 'Only job seekers can apply for jobs'}, status=403)
    
    job_id = request.data.get('job_id')
    cover_letter = request.data.get('cover_letter', '')
    
    try:
        job = Job.objects.get(id=job_id)
        job_seeker_profile = JobSeekerProfile.objects.get(user=request.user)
        
        # Check if already applied
        if JobApplication.objects.filter(job=job, applicant=job_seeker_profile).exists():
            return Response({'error': 'You have already applied for this job'}, status=400)
        
        # Create application
        application = JobApplication.objects.create(
            job=job,
            applicant=job_seeker_profile,
            cover_letter=cover_letter
        )
        
        return Response({
            'message': 'Application submitted successfully',
            'application_id': application.id
        })
    
    except Job.DoesNotExist:
        return Response({'error': 'Job not found'}, status=404)
    except JobSeekerProfile.DoesNotExist:
        return Response({'error': 'Job seeker profile not found'}, status=404)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_applications(request):
    if request.user.user_type != 'job_seeker':
        return Response({'error': 'Only job seekers can view applications'}, status=403)
    
    try:
        job_seeker_profile = JobSeekerProfile.objects.get(user=request.user)
        applications = JobApplication.objects.filter(applicant=job_seeker_profile)
        
        application_data = []
        for application in applications:
            application_data.append({
                'id': application.id,
                'job_title': application.job.title,
                'company_name': application.job.company.name,
                'applied_date': application.applied_date,
                'status': application.status,
                'cover_letter': application.cover_letter,
            })
        
        return Response(application_data)
    
    except JobSeekerProfile.DoesNotExist:
        return Response({'error': 'Job seeker profile not found'}, status=404)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def job_applications(request, job_id):
    if request.user.user_type != 'employer':
        return Response({'error': 'Only employers can view job applications'}, status=403)
    
    try:
        job = Job.objects.get(id=job_id, posted_by=request.user)
        applications = JobApplication.objects.filter(job=job)
        
        application_data = []
        for application in applications:
            application_data.append({
                'id': application.id,
                'applicant_name': f"{application.applicant.user.first_name} {application.applicant.user.last_name}",
                'applicant_email': application.applicant.user.email,
                'applicant_skills': application.applicant.skills,
                'applicant_experience': application.applicant.experience,
                'applied_date': application.applied_date,
                'status': application.status,
                'cover_letter': application.cover_letter,
            })
        
        return Response(application_data)
    
    except Job.DoesNotExist:
        return Response({'error': 'Job not found or you do not have permission'}, status=404)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_application_status(request, application_id):
    if request.user.user_type != 'employer':
        return Response({'error': 'Only employers can update application status'}, status=403)
    
    try:
        application = JobApplication.objects.get(id=application_id)
        # Check if the employer owns this job
        if application.job.posted_by != request.user:
            return Response({'error': 'You do not have permission to update this application'}, status=403)
        
        new_status = request.data.get('status')
        if new_status not in dict(JobApplication.APPLICATION_STATUS_CHOICES):
            return Response({'error': 'Invalid status'}, status=400)
        
        application.status = new_status
        application.save()
        
        return Response({
            'message': 'Application status updated successfully',
            'application_id': application.id,
            'new_status': application.status
        })
    
    except JobApplication.DoesNotExist:
        return Response({'error': 'Application not found'}, status=404)