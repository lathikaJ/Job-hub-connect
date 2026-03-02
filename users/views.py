from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model
from .models import JobSeekerProfile, EmployerProfile

User = get_user_model()

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')
        first_name = request.data.get('first_name', '')
        last_name = request.data.get('last_name', '')
        user_type = request.data.get('user_type')
        phone_number = request.data.get('phone_number', '')
        
        if User.objects.filter(email=email).exists():
            return Response({'error': 'User with this email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            user_type=user_type,
            phone_number=phone_number
        )
        
        # Create profile based on user type
        if user_type == 'job_seeker':
            JobSeekerProfile.objects.create(
                user=user,
                skills=request.data.get('skills', ''),
                experience=request.data.get('experience', 0)
            )
        elif user_type == 'employer':
            EmployerProfile.objects.create(
                user=user,
                company_name=request.data.get('company_name', '')
            )
        
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'user_type': user.user_type,
            },
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')
        
        user = authenticate(username=email, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'user_type': user.user_type,
                },
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class UserProfileView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        return Response({
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'user_type': user.user_type,
            'phone_number': user.phone_number,
        })

class JobSeekerProfileView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            profile = JobSeekerProfile.objects.get(user=request.user)
            return Response({
                'skills': profile.skills,
                'experience': profile.experience,
                'education': profile.education,
                'current_salary': profile.current_salary,
                'expected_salary': profile.expected_salary,
                'location': profile.location,
            })
        except JobSeekerProfile.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)

class EmployerProfileView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            profile = EmployerProfile.objects.get(user=request.user)
            return Response({
                'company_name': profile.company_name,
                'company_description': profile.company_description,
                'company_website': profile.company_website,
                'position': profile.position,
            })
        except EmployerProfile.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
        

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user_profile(request):
    try:
        user = request.user
        data = request.data
        
        # Update basic user information
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        if 'phone_number' in data:
            user.phone_number = data['phone_number']
        
        user.save()
        
        return Response({
            'message': 'Profile updated successfully',
            'user': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'user_type': user.user_type,
                'phone_number': user.phone_number,
            }
        })
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_jobseeker_profile(request):
    try:
        if request.user.user_type != 'job_seeker':
            return Response({'error': 'Only job seekers can update this profile'}, status=403)
        
        profile = JobSeekerProfile.objects.get(user=request.user)
        data = request.data
        
        # Update job seeker profile fields
        if 'skills' in data:
            profile.skills = data['skills']
        if 'experience' in data:
            profile.experience = data['experience']
        if 'education' in data:
            profile.education = data['education']
        if 'current_salary' in data:
            profile.current_salary = data['current_salary']
        if 'expected_salary' in data:
            profile.expected_salary = data['expected_salary']
        if 'location' in data:
            profile.location = data['location']
        
        profile.save()
        
        return Response({
            'message': 'Job seeker profile updated successfully',
            'profile': {
                'skills': profile.skills,
                'experience': profile.experience,
                'education': profile.education,
                'current_salary': profile.current_salary,
                'expected_salary': profile.expected_salary,
                'location': profile.location,
            }
        })
        
    except JobSeekerProfile.DoesNotExist:
        return Response({'error': 'Job seeker profile not found'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_employer_profile(request):
    try:
        if request.user.user_type != 'employer':
            return Response({'error': 'Only employers can update this profile'}, status=403)
        
        profile = EmployerProfile.objects.get(user=request.user)
        data = request.data
        
        # Update employer profile fields
        if 'company_name' in data:
            profile.company_name = data['company_name']
        if 'company_description' in data:
            profile.company_description = data['company_description']
        if 'company_website' in data:
            profile.company_website = data['company_website']
        if 'position' in data:
            profile.position = data['position']
        
        profile.save()
        
        return Response({
            'message': 'Employer profile updated successfully',
            'profile': {
                'company_name': profile.company_name,
                'company_description': profile.company_description,
                'company_website': profile.company_website,
                'position': profile.position,
            }
        })
        
    except EmployerProfile.DoesNotExist:
        return Response({'error': 'Employer profile not found'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)