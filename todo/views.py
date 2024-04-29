# views.py
from django.shortcuts import render, redirect
from .models import ServiceRequest, SupportTicket

def submit_service_request(request):
    if request.method == 'POST':
        # Logic to handle form submission
        request_type = request.POST.get('request_type')
        details = request.POST.get('details')
        attachment = request.FILES.get('attachment')
        service_request = ServiceRequest.objects.create(
            customer=request.user,
            request_type=request_type,
            details=details,
            attachment=attachment
        )
        return redirect('track_service_request', request_id=service_request.id)
    else:
        # Render form for submitting service request
        return render(request, 'submit_service_request.html')

def track_service_request(request, request_id):
    service_request = ServiceRequest.objects.get(id=request_id)
    return render(request, 'track_service_request.html', {'request': service_request})

def manage_support_tickets(request):
    support_tickets = SupportTicket.objects.all()
    return render(request, 'manage_support_tickets.html', {'tickets': support_tickets})
