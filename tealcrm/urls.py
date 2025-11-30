
from django.contrib import admin
from django.contrib.auth import views
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from core.views import index, about
from userprofile.views import signup
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render

handler400 = "core.views.error_400"
handler403 = "core.views.error_403"
handler404 = "core.views.error_404"
handler500 = "core.views.error_500"


urlpatterns = [
    path('',index, name='index'),
    path('leads/', include('lead.urls')),
    path('deal/', include('deal.urls')),
    path('about/', about, name='about'),
    path('sign-up/', signup, name='signup'),
    path('log-in/', views.LoginView.as_view(template_name='userprofile/login.html'),name='login'),
    path('log-out/', LogoutView.as_view(next_page='', http_method_names=['get', 'post']), name='logout'),
    path('admin/', admin.site.urls),
    path('profile/', include('userprofile.urls')),
    path('api/', include('lead.urls')),
    path('api-auth/', include('rest_framework.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
