# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ServiceRequest, SupportTicket
from .forms import ServiceRequestForm
from django.contrib.auth import authenticate, login

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('submit_service_request')
    return render(request, 'login.html')

@login_required
def submit_service_request(request):
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST, request.FILES)
        if form.is_valid():
            service_request = form.save(commit=False)
            service_request.customer = request.user
            service_request.save()
            messages.success(request, 'Your service request has been submitted successfully.')
            return redirect('track_service_request', request_id=service_request.id)
    else:
        form = ServiceRequestForm()
    return render(request, 'submit_service_request.html', {'form': form})

@login_required
def track_service_request(request, request_id):
    service_request = get_object_or_404(ServiceRequest, id=request_id, customer=request.user)
    return render(request, 'track_service_request.html', {'request': service_request})

@login_required
def manage_support_tickets(request):
    if not request.user.is_staff:
        return redirect('submit_service_request')
    support_tickets = SupportTicket.objects.all()
    return render(request, 'manage_support_tickets.html', {'tickets': support_tickets})

@login_required
def update_service_request_status(request, request_id):
    if not request.user.is_staff:
        return redirect('submit_service_request')
    service_request = get_object_or_404(ServiceRequest, id=request_id)
    if request.method == 'POST':
        status = request.POST.get('status')
        service_request.status = status
        if status == 'Resolved':
            service_request.resolved_at = timezone.now()
        service_request.save()
        messages.success(request, 'Service request status updated successfully.')
        return redirect('track_service_request', request_id=service_request.id)
    return render(request, 'update_service_request_status.html', {'request': service_request})
