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
from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from jobseekerapi.views import BoardView, CategoryView, CompanyView, QuestionView, register_user, login_user, current_seeker, JobView, InterviewPrepView, CustomPrepView, BoardJobView, InterviewView, SeekerView, TagView, BoardJobTagView, BoardCategoryView


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'boards', BoardView, 'board')
router.register(r'categories', CategoryView, 'category')
router.register(r'companies', CompanyView, 'company')
router.register(r'questions', QuestionView, 'question')
router.register(r'jobs', JobView, 'job')
router.register(r'preps', InterviewPrepView, 'prep')
router.register(r'customs', CustomPrepView, 'custom')
router.register(r'boardjobs', BoardJobView, 'boardjob')
router.register(r'interviews', InterviewView, 'interview')
router.register(r'seekers', SeekerView, 'seeker')
router.register(r'tags', TagView, 'tag')
router.register(r'boardjobtags', BoardJobTagView, 'boardjobtag')
router.register(r'boardcategories', BoardCategoryView, 'boardcategory')


urlpatterns = [
    path('register', register_user),
    path('login', login_user),
    path('currentseeker', current_seeker),
    path('admin/', admin.site.urls),
    path('', include(router.urls))
]
