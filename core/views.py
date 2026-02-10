from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.contrib import messages
from django.conf import settings
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import logging
import sys

logger = logging.getLogger(__name__)


# Create your views here.
def home(request):
    return render(request, 'core/index.html')


@csrf_exempt
@require_http_methods(["POST"])
def contact(request):
    """Handle contact form submissions and send email"""
    # Debug: Print to console immediately
    print("=" * 50, file=sys.stderr)
    print("CONTACT FORM RECEIVED", file=sys.stderr)
    print("=" * 50, file=sys.stderr)
    
    name = request.POST.get('name', '').strip()
    email = request.POST.get('email', '').strip()
    phone = request.POST.get('phone', '').strip()
    message_text = request.POST.get('message', '').strip()
    
    print(f"Name: {name}", file=sys.stderr)
    print(f"Email: {email}", file=sys.stderr)
    print(f"Phone: {phone}", file=sys.stderr)
    print(f"Message: {message_text}", file=sys.stderr)
    
    if not all([name, email, message_text]):
        print("ERROR: Missing required fields", file=sys.stderr)
        messages.error(request, 'Please fill in all required fields.')
        return redirect('home')
    
    try:
        # Construct the email message
        full_message = f"""New contact form submission:

Name: {name}
Email: {email}
Phone: {phone}

Message:
{message_text}
"""
        
        print(f"\nSending email...", file=sys.stderr)
        print(f"From: {settings.DEFAULT_FROM_EMAIL}", file=sys.stderr)
        print(f"Reply-To: {email}", file=sys.stderr)
        print(f"To: oluwayemisiessien@gmail.com", file=sys.stderr)
        print(f"Backend: {settings.EMAIL_BACKEND}", file=sys.stderr)
        
        # Use EmailMessage for more control (supports reply_to)
        email_message = EmailMessage(
            subject=f'New Contact Form Submission from {name}',
            body=full_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=['oluwayemisiessien@gmail.com'],
            reply_to=[email],
        )
        
        result = email_message.send(fail_silently=False)
        
        print(f"Email sent successfully! Result: {result}", file=sys.stderr)
        print("\n--- EMAIL CONTENT ---", file=sys.stderr)
        print(full_message, file=sys.stderr)
        print("--- END EMAIL ---\n", file=sys.stderr)
        
        logger.info(f'Contact form submitted by {name} ({email})')
        messages.success(request, 'Thank you! Your message has been sent successfully.')
        return redirect('home')
    
    except Exception as e:
        print(f"ERROR SENDING EMAIL: {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        logger.error(f'Error sending contact form email: {str(e)}')
        messages.error(request, f'Error sending message: {str(e)}')
        return redirect('home')
