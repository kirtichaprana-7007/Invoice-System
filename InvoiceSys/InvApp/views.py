from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import AccountDetailsModelForm, ServicesModelForm
from .models import Account_Details
from .models import Services
from django.shortcuts import get_object_or_404
from django.contrib.auth import logout
from .forms import ContactForm
from .models import ContactMessage  # Import the model to save messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.utils import timezone

# Create your views here.

def login_view(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            # Handle invalid login
            messages.error(request, 'Invalid credentials!')
            return redirect('login')  # Redirect back to login page

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):

    return render(request, 'home.html')
@login_required
def about(request):
    return render(request, 'about.html')

@login_required
def contact(request):
    return render(request, 'contact.html')

def contact_success(request):
    return render(request, 'contact_success.html')

@login_required
def feature(request):
    return render(request, 'feature.html')


@login_required
def add_client(request):

    try:
        account_details = Account_Details.objects.all()
    except Account_Details.DoesNotExist:
        account_details = None

    if request.method == 'POST':
        form = AccountDetailsModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account details saved successfully!")
            return redirect('add-client')  # Replace 'success-page' with your actual URL name
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = AccountDetailsModelForm()


    return render(request, 'add_client.html', {'form': form, 'account_details':account_details})

@login_required
def account_details_review(request, id):

    try:
        single_account = Account_Details.objects.get(id=id)
    except Account_Details.DoesNotExist:
        single_account = None

    return render(request, 'account_details_review.html', {'single_account': single_account})

@login_required
def delete_account_details(request, id):
    if request.method == 'GET':
        try:
            account_details = get_object_or_404(Account_Details, id=id)
            account_details.delete()
            messages.success(request, "Account details deleted successfully!")
        except Exception as e:
           
            messages.error(request, f"An error occurred: {str(e)}")
    return redirect('add-client') 


@login_required
def update_account_details(request, id):
    account_detail = get_object_or_404(Account_Details, id=id)

    if request.method == 'POST':
        form = AccountDetailsModelForm(request.POST, instance=account_detail)

        if form.is_valid():
            form.save()
            messages.success(request, "Account details updated successfully!")
            return redirect('account-details-review', id=id)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = AccountDetailsModelForm(instance=account_detail)

    return render(request, 'update_account_details.html', {'form': form})



@login_required
def assign_service(request):
    try:
        assigned_service = Services.objects.all()
    except Services.DoesNotExist:
        assigned_service = None
    if request.method == 'POST':
        form = ServicesModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Service assigned successfully!")
            return redirect('assign-service')  # Replace 'success-page' with your actual URL name
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ServicesModelForm()
    
    return render(request,'assign_service.html',{'form':form,'assigned_service':assigned_service})
       
@login_required
def assign_service_list(request, id):
    try:
        assign_service_list = Services.objects.filter(account_details_id  = id)
        
        for service in assign_service_list:
            service.subtotal = service.service_price * service.service_quantity
            
    except Services.DoesNotExist:
        assign_service_list = None
    try:
        account_details = Account_Details.objects.get(id=id)
    except Account_Details.DoesNotExist:
        account_details = None
    

    return render(request,'assign_service_review.html',{'assign_service_list':assign_service_list,'account_details':account_details})

@login_required
def delete_assign_service(request, id):
    if request.method == 'GET':
        try:
            assigned_service = get_object_or_404(Services,id = id)
            assigned_service.delete()
            messages.success(request, "Service details deleted successfully!")
        except Exception as e:
           
            messages.error(request, f"An error occurred: {str(e)}")
    return redirect('assign-service') 
@login_required
def update_assign_service(request, id):
    assigned_service = get_object_or_404(Services, id=id)

    if request.method == 'POST':
        form = ServicesModelForm(request.POST, instance=assigned_service)

        if form.is_valid():
            form.save()
            messages.success(request, "assigned service updated successfully!")
            return redirect('assign-service-list', id=id)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = AccountDetailsModelForm(instance=assigned_service)

    return render(request, 'update_assign_service.html', {'form': form})
 
@login_required
def report_print_list(request):
    try:
        account_details = Account_Details.objects.all()
    except Account_Details.DoesNotExist:
        account_details = None

    return render(request, 'report_print_list.html', {'account_details':account_details})

@login_required
def pdf_report(request, id):
    try:
        assign_service_list = Services.objects.filter(account_details_id  = id)
        
        for service in assign_service_list:
            service.subtotal = service.service_price * service.service_quantity
            
    except Services.DoesNotExist:
        assign_service_list = None
    try:
        account_details = Account_Details.objects.get(id=id)
    except Account_Details.DoesNotExist:
        account_details = None,
    return render(request,'pdfreport.html', {'assign_service_list':assign_service_list, 'account_details':account_details})



from .forms import FreeAccountForm

def create_free_account(request):
    if request.method == 'POST':
        form = FreeAccountForm(request.POST)
        if form.is_valid():
            # Set account type as 'free' by default
            account = form.save(commit=False)
            account.account_type = 'free'
            account.save()
            messages.success(request, "Your free account has been created successfully!")
            return redirect('home')  # Redirect to login or dashboard page
        else:
            messages.error(request, "There was an error with your registration. Please try again.")
    else:
        form = FreeAccountForm()

    return render(request, 'create_account.html', {'form': form})



    
@login_required
def custom_logout(request):
    # Perform any custom actions here (e.g., logging out message, clearing data)
    logout(request)
    return redirect('login')  # Redirect to the login page or any URL







