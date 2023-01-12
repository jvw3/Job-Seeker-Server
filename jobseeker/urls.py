"""jobseeker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import include
from rest_framework import routers
from jobseekerapi.views import BoardView, CategoryView, CompanyView, QuestionView, register_user, login_user, current_seeker, JobView, InterviewPrepView, CustomPrepView, BoardJobView, InterviewView, SeekerView, TagView, BoardJobTagView, BoardCategoryView, InterviewPrepView, ContactView, PriorityRankView, NetworkMeetingView, MeetingTypeView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="JobSeeker API",
        default_version='v1',
        description="API for JobSeeker Application",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@levelup.local"),
        license=openapi.License(name="BSD License"),
    ),

    public=True,
    permission_classes=[permissions.AllowAny],
)


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'boards', BoardView, 'board')
router.register(r'categories', CategoryView, 'category')
router.register(r'companies', CompanyView, 'company')
router.register(r'questions', QuestionView, 'question')
router.register(r'jobs', JobView, 'job')
router.register(r'preps', InterviewPrepView, 'prep')
router.register(r'custompreps', CustomPrepView, 'customprep')
router.register(r'boardjobs', BoardJobView, 'boardjob')
router.register(r'interviews', InterviewView, 'interview')
router.register(r'interviewpreps', InterviewPrepView, 'interviewprep')
router.register(r'seekers', SeekerView, 'seeker')
router.register(r'tags', TagView, 'tag')
router.register(r'boardjobtags', BoardJobTagView, 'boardjobtag')
router.register(r'boardcategories', BoardCategoryView, 'boardcategory')
router.register(r'contacts', ContactView, 'contact')
router.register(r'priorityranks', PriorityRankView, 'priorityrank')
router.register(r'networkmeetings', NetworkMeetingView, 'networkmeeting')
router.register(r'meetingtypes', MeetingTypeView, 'meetingtype')


urlpatterns = [
    path('register', register_user),
    path('login', login_user),
    path('currentseeker', current_seeker),
    path('admin/', admin.site.urls),
    re_path(r'^swagger/$', schema_view.with_ui('swagger',
            cache_timeout=0), name='schema-swagger-ui'),
    path('', include(router.urls)),
]
