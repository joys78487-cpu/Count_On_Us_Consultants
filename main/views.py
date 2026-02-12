from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .models import ContactMessage, NewsletterSubscriber

def index(request):
    if request.method == "POST" and 'message' in request.POST:
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        name = f"{first_name} {last_name}"
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        service = request.POST.get('service')
        message_text = request.POST.get('message')

        # Save message
        ContactMessage.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            service=service,
            message=message_text
        )

        # Email to owner
        try:
            send_mail(
                subject="New Enquiry Received",
                message=f"Name: {name}\nEmail: {email}\nPhone: {phone}\nService: {service}\nMessage:\n{message_text}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=["cou.consulting@gmail.com"],
                fail_silently=False,
            )
            messages.success(request, "Your message has been sent successfully!")
        except Exception as e:
            messages.error(request, f"Message saved but email failed: {str(e)}")
        return redirect('home')

    return render(request, 'main/index.html')


def subscribe(request):
    if request.method == "POST" and 'subscribe_email' in request.POST:
        email = request.POST.get('subscribe_email')
        NewsletterSubscriber.objects.get_or_create(email=email)

        # Email to owner
        try:
            send_mail(
                subject="New Newsletter Subscriber",
                message=f"{email} subscribed to your newsletter.",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=["cou.consulting@gmail.com"],
                fail_silently=False,
            )
            messages.success(request, "Subscribed successfully!")
        except Exception as e:
            messages.error(request, f"Subscription saved but email failed: {str(e)}")
        return redirect('home')
