
from django.contrib import admin
from django.urls import path,include
from InvApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', views.logout_view, name='logout'),
    
    path('', views.dashboard, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('feature/', views.feature, name='feature'),
    path('contact-success', views.contact_success, name='contact-success'),
    

    path('add-client/', views.add_client, name='add-client'),
    path('account-details-review/<int:id>/', views.account_details_review, name='account-details-review'),
    path('delete-account-details/<int:id>/', views.delete_account_details, name='delete-account-details'),
    path('update-account-details/<int:id>/', views.update_account_details, name='update-account-details'),
   
    path('assign-service/', views.assign_service, name='assign-service'),
    path('assign-service-list/<int:id>/', views.assign_service_list, name='assign-service-list'),
    path('delete-assign-service/<int:id>/', views.delete_assign_service, name='delete-assign-service'),
    path('update-assign-service/<int:id>/', views.update_assign_service, name='update-assign-service'),
    path('assign-service-report-printing-list/', views.report_print_list, name='report-printing-list'),
    path('assign-service-pdf-report/<int:id>/', views.pdf_report, name='pdf-report'),

    
    path('create-account/', views.create_free_account, name='create-free-account'),




]
