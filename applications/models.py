from django.db import models
from users.models import JobSeekerProfile
from jobs.models import Job

class JobApplication(models.Model):
    APPLICATION_STATUS_CHOICES = (
        ('applied', 'Applied'),
        ('under_review', 'Under Review'),
        ('shortlisted', 'Shortlisted'),
        ('rejected', 'Rejected'),
        ('hired', 'Hired'),
    )
    
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    applicant = models.ForeignKey(JobSeekerProfile, on_delete=models.CASCADE)
    applied_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=APPLICATION_STATUS_CHOICES, default='applied')
    cover_letter = models.TextField(blank=True)
    
    class Meta:
        unique_together = ['job', 'applicant']
        ordering = ['-applied_date']

    def __str__(self):
        return f"{self.applicant.user.get_full_name()} - {self.job.title}"