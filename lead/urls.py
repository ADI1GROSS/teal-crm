from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LeadViewSet, ContactViewSet

router = DefaultRouter()
router.register(r'leads', LeadViewSet, basename='lead')
router.register(r'contacts', ContactViewSet, basename='contact')



urlpatterns = [
    path('add-lead/', views.add_lead, name='add_lead'),
    path('add-lead-public/<uuid:invite_token>/', views.add_lead_public, name='add_lead_public'),
    path('', views.leads_list, name='leads_list'),
    path('<int:pk>/delete/', views.leads_delete, name='leads_delete'),
    path('<int:pk>/edit/', views.leads_edit, name='leads_edit'),
    path('<int:pk>/', views.leads_detail, name='leads_detail'),
    path('<int:pk>/add-contact/', views.add_contact, name='add_contact'),
    path('contact/<int:pk>/delete/', views.delete_contact, name='delete_contact'),
    path('contact/<int:pk>/edit/', views.contact_edit, name='contact_edit'),
    path('<int:pk>/pdf/', views.lead_pdf, name='lead_pdf'),
    path('send-client-email/<int:pk>/', views.send_client_email, name='send_client_email'), 
    path('', include(router.urls)),

]