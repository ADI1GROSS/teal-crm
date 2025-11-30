from django.urls import path
from . import views

urlpatterns = [
    path('edit-template/<str:field_name>/', views.edit_deal_template, name="edit_deal_template"),
    path("deal_list/", views.deal_list, name="deal_list"),
    path("deal-template/add/", views.add_deal_template_field, name="add_deal_template_field"),
    path("deal-template/delete/<str:field_name>/", views.delete_deal_template_field, name="delete_deal_template_field"),
]
