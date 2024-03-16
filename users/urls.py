from django.urls import path, include
from rest_framework import routers
from  . views import *
from django.conf.urls.static import static
router = routers.DefaultRouter()
router.register('', AuthViewSet, basename="authview")
from django.conf.urls.static import static

urlpatterns = [
    path('jobs/', JobViewSet.as_view(), name="jobview"),
    path('jobs/<int:pk>/', JobIndividualViewSet.as_view(), name="job"),
    path('jobs_add/', JobAdd.as_view(), name="jobadd"),
    path('jobs/detail/<int:pk>/', JobDetailViewSet.as_view(), name="jobdetails"),
    path('jobs/count/', JobCount.as_view(), name='Jobcount'),
    path('company/', CompanyViewSet.as_view(), name="companyview"),
    path('company/<int:pk>/', CompanyIndividualViewSet.as_view(), name="company"),
    path('company_add', CompanyAdd.as_view(), name="companyadd"),
    path('company/detail/<int:pk>/', CompanyDetailViewSet.as_view(), name="companydetails"),
    path('company/count/', CompanyCount.as_view(), name='companycount'),
    path('applicant/', ApplicantViewSet.as_view(), name="applicantview"),
    path('applicant/<int:pk>/', ApplicantIndividualViewSet.as_view(), name="applicant"),
    path('applicant_add', ApplicantAdd.as_view(), name="applicantadd"),
    path('applicant/detail/<int:pk>/', ApplicantDetailViewSet.as_view(), name="applicantdetails"),
    path('applicant/count/', ApplicantCount.as_view(), name='applicantcount'),
    path('application/', ApplicationViewSet.as_view(), name="Applicationview"),
    path('application/<int:pk>', ApplicationIndividualViewSet.as_view(), name="Application"),
    path('application/detail/<int:pk>/', ApplicationDetailViewSet.as_view(), name="applicationdetails"),
    path('application_add', ApplicationAdd.as_view(), name="applicationadd"),
    path('application/count/', ApplicationCount.as_view(), name='applicationcount'),
    path('users/', UserList.as_view(), name="userlist"),
    path('users/<int:pk>/', UserDetailViewSet.as_view(), name="userdetail"),
    path('users/<int:pk>/', UserIndividualViewSet.as_view(), name="userdetail"),
    path('users/count/', UserCount.as_view(), name='usercount'),
    path('change_password/<int:pk>/', ChangePasswordView.as_view(), name='auth_change_password'),
    path('api/', include(router.urls))


]


if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)