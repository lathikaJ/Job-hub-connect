import os
import django
import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jobportal.settings')
django.setup()

from users.models import CustomUser, JobSeekerProfile, EmployerProfile
from jobs.models import Company, Job
from applications.models import JobApplication

def create_sample_data():
    print("Creating sample data...")
    
    # Create companies
    company1, created = Company.objects.get_or_create(
        name="Tech Solutions Inc",
        defaults={
            'description': "Leading technology company specializing in software development",
            'industry': "Information Technology",
            'employee_count': 500,
            'founded_year': 2010,
            'website': "https://techsolutions.com"
        }
    )
    
    company2, created = Company.objects.get_or_create(
        name="Global Finance Corp",
        defaults={
            'description': "International financial services company",
            'industry': "Finance",
            'employee_count': 1000,
            'founded_year': 2005,
            'website': "https://globalfinance.com"
        }
    )
    
    company3, created = Company.objects.get_or_create(
        name="Healthcare Plus",
        defaults={
            'description': "Healthcare and medical services provider",
            'industry': "Healthcare",
            'employee_count': 300,
            'founded_year': 2015,
            'website': "https://healthcareplus.com"
        }
    )
    
    print("Companies created!")
    
    # Get or create a test user for posting jobs
    try:
        test_user = CustomUser.objects.get(email='admin@test.com')
    except CustomUser.DoesNotExist:
        test_user = CustomUser.objects.create_user(
            username='admin@test.com',
            email='admin@test.com',
            password='testpass123',
            first_name='Admin',
            last_name='User',
            user_type='employer'
        )
        EmployerProfile.objects.create(
            user=test_user,
            company_name="Test Company",
            position="HR Manager"
        )
    
    # Create sample jobs
    jobs_data = [
        {
            'title': "Python Developer",
            'company': company1,
            'description': "We are looking for a skilled Python developer to join our dynamic team. You will be responsible for developing and maintaining Python applications, working with Django framework, and collaborating with cross-functional teams.",
            'requirements': "Bachelor's degree in Computer Science or related field, 3+ years of Python development experience, strong knowledge of Django framework, experience with REST APIs, familiarity with PostgreSQL",
            'skills_required': "Python, Django, REST APIs, PostgreSQL, Git, Docker",
            'location': "New York, NY",
            'job_type': "full_time",
            'salary_min': 80000,
            'salary_max': 120000,
            'experience_min': 3,
            'experience_max': 6,
            'vacancies': 2,
            'posted_by': test_user,
            'application_deadline': datetime.date.today() + datetime.timedelta(days=30)
        },
        {
            'title': "Frontend Developer",
            'company': company1,
            'description': "Join our frontend team to build amazing user interfaces. We're looking for a React expert who can create responsive and interactive web applications.",
            'requirements': "2+ years of frontend development experience, proficiency in React.js, strong JavaScript skills, experience with modern CSS frameworks",
            'skills_required': "JavaScript, React, HTML5, CSS3, Redux, Webpack",
            'location': "Remote",
            'job_type': "remote",
            'salary_min': 70000,
            'salary_max': 100000,
            'experience_min': 2,
            'experience_max': 5,
            'vacancies': 3,
            'posted_by': test_user,
            'application_deadline': datetime.date.today() + datetime.timedelta(days=45)
        },
        {
            'title': "Financial Analyst",
            'company': company2,
            'description': "We are seeking a Financial Analyst to provide financial planning and analysis support. You will work closely with the finance team to analyze financial data and create reports.",
            'requirements': "Bachelor's degree in Finance or Accounting, 2+ years of financial analysis experience, strong Excel skills, knowledge of financial modeling",
            'skills_required': "Financial Analysis, Excel, Accounting, Financial Modeling, Data Analysis",
            'location': "Chicago, IL",
            'job_type': "full_time",
            'salary_min': 65000,
            'salary_max': 90000,
            'experience_min': 2,
            'experience_max': 4,
            'vacancies': 1,
            'posted_by': test_user,
            'application_deadline': datetime.date.today() + datetime.timedelta(days=25)
        },
        {
            'title': "Data Scientist",
            'company': company3,
            'description': "Join our data science team to analyze healthcare data and build predictive models. You will work with large datasets to derive insights and support decision-making.",
            'requirements': "Master's degree in Data Science or related field, 3+ years of data science experience, proficiency in Python and ML libraries, experience with SQL",
            'skills_required': "Python, Machine Learning, SQL, Pandas, NumPy, Scikit-learn",
            'location': "Boston, MA",
            'job_type': "full_time",
            'salary_min': 90000,
            'salary_max': 130000,
            'experience_min': 3,
            'experience_max': 7,
            'vacancies': 2,
            'posted_by': test_user,
            'application_deadline': datetime.date.today() + datetime.timedelta(days=35)
        },
        {
            'title': "Marketing Manager",
            'company': company2,
            'description': "We're looking for a Marketing Manager to develop and execute marketing strategies. You will lead marketing campaigns and analyze their performance.",
            'requirements': "Bachelor's degree in Marketing or related field, 4+ years of marketing experience, digital marketing expertise, strong analytical skills",
            'skills_required': "Digital Marketing, SEO, Social Media, Google Analytics, Content Strategy",
            'location': "San Francisco, CA",
            'job_type': "full_time",
            'salary_min': 75000,
            'salary_max': 110000,
            'experience_min': 4,
            'experience_max': 8,
            'vacancies': 1,
            'posted_by': test_user,
            'application_deadline': datetime.date.today() + datetime.timedelta(days=20)
        },
        {
            'title': "DevOps Engineer",
            'company': company1,
            'description': "Join our DevOps team to build and maintain our cloud infrastructure. You will work on CI/CD pipelines, containerization, and cloud services.",
            'requirements': "3+ years of DevOps experience, strong knowledge of AWS, experience with Docker and Kubernetes, CI/CD pipeline development",
            'skills_required': "AWS, Docker, Kubernetes, Jenkins, Terraform, Linux",
            'location': "Austin, TX",
            'job_type': "full_time",
            'salary_min': 95000,
            'salary_max': 140000,
            'experience_min': 3,
            'experience_max': 6,
            'vacancies': 2,
            'posted_by': test_user,
            'application_deadline': datetime.date.today() + datetime.timedelta(days=40)
        }
    ]
    
    for job_data in jobs_data:
        job, created = Job.objects.get_or_create(
            title=job_data['title'],
            company=job_data['company'],
            defaults=job_data
        )
        if created:
            print(f"Created job: {job.title}")
        else:
            print(f"Job already exists: {job.title}")
    
    print("Sample data creation completed!")
    print(f"Total companies: {Company.objects.count()}")
    print(f"Total jobs: {Job.objects.count()}")
if __name__ == "__main__":
    create_sample_data()