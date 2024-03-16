from .models import *
from .serializers import *
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, viewsets
from . permissions import *
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from django.contrib.auth import logout
from django.core.exceptions import ImproperlyConfigured
from .utils import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings
from django.core.mail import send_mail
from rest_framework import filters
from rest_framework.parsers import FormParser, MultiPartParser

class JobViewSet(generics.ListAPIView):
    authentication_classes = [JWTAuthentication] 
    permission_classes = [IsApplicant]
    search_fields = ['title']
    filter_backends = (filters.SearchFilter,)
    queryset = Job.objects.all()
    serializer_class = JobSerializer

    def list(self, request, *args, **kwargs):
        search_query = request.query_params.get('title', None)
     
        if search_query:
                queryset = self.filter_queryset(self.get_queryset().filter(**{search_query: search_query}))
                serializer = self.get_serializer(queryset, many=True)
                return Response(serializer.data)
    
        
        return super().list(request, *args, **kwargs)
    
class JobAdd(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication] 
    permission_classes = [IsRecruiter]
    queryset = Job.objects.all()
    serializer_class = JobSerializer

   
class JobIndividualViewSet(generics.RetrieveAPIView):
    authentication_classes = [JWTAuthentication] 
    permission_classes =[IsApplicant]
    queryset = Job.objects.all()
    serializer_class = JobSerializer

    
class JobDetailViewSet(generics.RetrieveUpdateDestroyAPIView):
    search_fields = ['location']
    filter_backends = (filters.SearchFilter,)
    authentication_classes = [JWTAuthentication] 
    permission_classes =[IsRecruiter]
    queryset = Job.objects.all()
    serializer_class = JobSerializer

    def list(self, request, *args, **kwargs):
        search_query = request.query_params.get('location', None)
        
        # Check if the provided field is valid
        if search_query and search_query not in self.search_fields:
            return Response({"error": f"Unknown field: {search_query}"}, status=status.HTTP_400_BAD_REQUEST)
         
        if search_query:
            queryset = self.filter_queryset(self.get_queryset().filter(**{search_query: search_query}))
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        
        
        return super().list(request, *args, **kwargs)

class JobCount(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication] 
    permission_classes =[IsAuthenticated]
    serializer_class = JobSerializer

    def get(self, request, *args, **kwargs):
        job_count = Job.objects.count()
        data = {"job_count":job_count}
        return Response(data)
    
class CompanyViewSet(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication] 
    permission_classes = [IsApplicant]
    search_fields = ['type']
    filter_backends = (filters.SearchFilter,)
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    def list(self, request, *args, **kwargs):
        search_query = request.query_params.get('type', None)
        
        # Check if the provided field is valid
        if search_query and search_query not in self.search_fields:
            return Response({"error": f"Unknown field: {search_query}"}, status=status.HTTP_400_BAD_REQUEST)
         
        if search_query:
            queryset = self.filter_queryset(self.get_queryset().filter(**{search_query: search_query}))
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        
        
        return super().list(request, *args, **kwargs)

class CompanyIndividualViewSet(generics.RetrieveAPIView):
    authentication_classes = [JWTAuthentication] 
    permission_classes =[IsApplicant]
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

class CompanyAdd(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication] 
    permission_classes = [IsRecruiter]
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    
    
class CompanyDetailViewSet(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication] 
    permission_classes = [IsRecruiter]
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    
class CompanyCount(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication] 
    permission_classes =[IsAuthenticated]
    serializer_class = CompanySerializer

    def get(self, request, *args, **kwargs):
        company_count = Company.objects.count()
        data = {"company_count": company_count}
        return Response(data)
    
class ApplicantViewSet(generics.ListAPIView):
    authentication_classes = [JWTAuthentication] 
    permission_classes = [IsRecruiter]
    search_fields = ['gender']
    filter_backends = (filters.SearchFilter,)
    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer

    def list(self, request, *args, **kwargs):
        search_query = request.query_params.get('gender', None)
        
        # Check if the provided field is valid
        if search_query and search_query not in self.search_fields:
            return Response({"error": f"Unknown field: {search_query}"}, status=status.HTTP_400_BAD_REQUEST)
         
        if search_query:
            queryset = self.filter_queryset(self.get_queryset().filter(**{search_query: search_query}))
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        
        
        return super().list(request, *args, **kwargs)
    
class ApplicantIndividualViewSet(generics.RetrieveAPIView):
    authentication_classes = [JWTAuthentication] 
    permission_classes =[IsRecruiter]
    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer

class ApplicantAdd(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication] 
    permission_classes = [IsApplicant]
    queryset = Applicant.objects.all()
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = ApplicantSerializer


    

class ApplicantDetailViewSet(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication] 
    permission_classes = [IsApplicant]
    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer

class ApplicantCount(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication] 
    permission_classes =[IsRecruiter]
    serializer_class = ApplicantSerializer

    def get(self, request, *args, **kwargs):
        applicant_count = Applicant.objects.count()
        data = {"applicant_count":applicant_count}
        return Response(data)


class ApplicationViewSet(generics.ListAPIView):
    authentication_classes = [JWTAuthentication] 
    permission_classes = [IsRecruiter]
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

class ApplicationAdd(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication] 
    permission_classes = [IsApplicant]
    queryset = Application.objects.all()
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = ApplicationSerializer
    


    
class ApplicationDetailViewSet(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication] 
    permission_classes = [IsApplicant]
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

class ApplicationIndividualViewSet(generics.RetrieveAPIView):
    authentication_classes = [JWTAuthentication] 
    permission_classes =[IsRecruiter]
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

class ApplicationCount(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication] 
    permission_classes =[IsRecruiter]
    serializer_class = ApplicationSerializer

    def get(self, request, *args, **kwargs):
        application_count = Application.objects.count()
        data = {"application_count": application_count}
        return Response(data)
    
class UserList(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication] 
    permission_classes = [IsAdminUser]
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
  
class UserCount(generics.GenericAPIView):
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        user_count = CustomUser.objects.count()
        data = {"user_count": user_count}
        return Response(data)
    
class UserIndividualViewSet(generics.RetrieveAPIView):
    authentication_classes = [JWTAuthentication] 
    permission_classes =[IsAdminUser]
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

class UserDetailViewSet(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication] 
    permission_classes = [IsAdminUser]
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

class ChangePasswordView(generics.UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()
    serializer_class = ChangePasswordSerializer

class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    queryset = CustomUser.objects.all() 
    serializer_class = EmptySerializer
    serializer_classes = {
        'login': UserLoginSerializer,
        'register': UserRegisterSerializer,
    }

    @action(methods=['POST'], detail=False)
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_and_authenticate_user(**serializer.validated_data)
        serializer_class = AuthUserSerializer 
        data = serializer_class(user).data
        return Response(data=data, status=status.HTTP_200_OK)
        
    
    
    @action(methods=['POST',], detail=False)
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = create_user_account(**serializer.validated_data)
        data = AuthUserSerializer(user).data


        subject = 'Welcome to Job Portal X'
        message = f"Hi {user.email},\n\nThank you for registering in JOB PORTAL X. This is a system-generated email, please do not reply.\n\nYour Username is {user.email}.\n\nBest regards,\nThe JOB PORTAL X Team"


        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email, ]
        send_mail( subject, message, email_from, recipient_list )
        return Response(data=data, status=status.HTTP_201_CREATED)

    @action(methods=['POST', ], detail=False)
    def logout(self, request):
        logout(request)
        data = {'success': 'Sucessfully logged out'}
        return Response(data=data, status=status.HTTP_200_OK)
    



    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured("serializer_classes should be a dict mapping.")

        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()
    

