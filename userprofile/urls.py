from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserprofileViewSet

router = DefaultRouter()
router.register(r'userprofiles', UserprofileViewSet, basename='userprofile')

app_name = 'userprofile'

urlpatterns = [
    
    path('edit/', views.edit_profile, name='edit_profile'),
    path('', include(router.urls)),
]
