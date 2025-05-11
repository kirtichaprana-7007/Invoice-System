from django.db import models
from django.utils import timezone
# Create your models here.
class Account_Details(models.Model):
    provider_name = models.CharField(max_length=50)
    provider_address = models.CharField(max_length=100)
    provider_phone_number = models.CharField(max_length=15)
    provider_email = models.EmailField()
    provider_account_no = models.PositiveIntegerField()
    provider_ifsc_code = models.CharField(max_length=50)
    provider_bannk_name = models.CharField(max_length=50)
    provider_bank_branch =models.CharField(max_length=50)
    provider_gst_no = models.CharField(max_length=50)

    client_name = models.CharField(max_length=50)
    client_address = models.CharField(max_length=100)
    client_phone_number = models.CharField(max_length=15)
    client_email = models.EmailField()
    client_account_no = models.PositiveIntegerField()
    client_ifsc_code = models.CharField(max_length=50)
    client_bannk_name = models.CharField(max_length=50)
    client_bank_branch =models.CharField(max_length=50)
    client_gst_no = models.CharField(max_length=50)
    
    
    def __str__(self):
        return f"{self.provider_name} - {self.client_name}"
    
class Services(models.Model):
    account_details = models.ForeignKey(Account_Details, on_delete=models.CASCADE)
    service_name = models.CharField(max_length=100)
    service_description = models.TextField()
    service_price = models.DecimalField(max_digits=10, decimal_places=2)
    service_quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True) 

    def __str__(self):
        return f"{self.service_name} - {self.account_details.client_name}"
    
    

class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"


class User(models.Model):
    client_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, unique=True)
    contact_number = models.CharField(max_length=15)
    address = models.TextField()
    account_type = models.CharField(
        max_length=20, 
        choices=[('free', 'Free'), ('premium', 'Premium')], 
        default='free'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.client_name






