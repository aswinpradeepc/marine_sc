import environ
import json
import logging
import razorpay
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from base.utils import sendmail
from payment.utils import payment_completed_test
from .models import Payment

env = environ.Env()

environ.Env.read_env('.env')

# Razorpay client setup
RAZORPAY_KEY_ID = env.str("RAZORPAY_KEY_ID")
RAZORPAY_KEY_SECRET = env.str("RAZORPAY_KEY_SECRET")

# Razorpay client initialization
razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

logger = logging.getLogger("payment")
amount_dict = {
    'id': {
        'amount': 250,
        'currency': 'USD',
        'name': "Faculty/ Scientist (International)"
    }, 'nd': {
        'amount': 500,
        'currency': 'INR',
        'name': "Students"
    }, 'fs': {
        'amount': 3000,
        'currency': 'INR',
        'name': "Faculty/ Scientist"
    }, 'rs': {
        'amount': 1500,
        'currency': 'INR',
        'name': "Research Scholars"
    },
    # 'ts': {
    #     'amount': 1,
    #     'currency': 'INR',
    #     'name': "Test"
    # },
}


def get_amount_for_category(category):
    category_data = amount_dict.get(category)
    if category_data:
        return category_data['amount'] * 100 if category_data['currency'] == 'INR' else category_data['amount']
    return None


class PaymentView(TemplateView):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/login/')
        if payment_completed_test(request.user):
            return redirect('/abstract_closed/')
        return render(request, "payment/checkout.html", {
            'amount_dict': amount_dict
        })  # The page with payment form

    def post(self, request, *args, **kwargs):
        category = request.POST.get('category')
        amount = get_amount_for_category(category)  # Logic to set amount based on category
        if not amount:
            return render(request, 'payment/checkout.html', {'err': 'Invalid category selected.'})

        order_data = {
            'amount': get_amount_for_category(category),
            'currency': amount_dict[category]['currency'],
            'payment_capture': 1,
        }

        order = razorpay_client.order.create(data=order_data)
        razorpay_order_id = order['id']

        # Save the payment data to the database
        payment = Payment.objects.create(
            razorpay_order_id=razorpay_order_id,
            amount=amount,
            currency='INR',
            user=request.user,
            category=amount_dict[category]['name']
        )

        # Pass data to frontend
        context = {
            'payment': payment,
            'razorpay_order_id': razorpay_order_id,
            'razorpay_key_id': RAZORPAY_KEY_ID,
            'amount': amount,
            'currency': 'INR',
            'amount_display': amount_dict[category]['amount'],

        }

        return render(request, 'payment/confirm_payment.html', context)


@csrf_exempt
def payment_verification(request):
    if request.method != "POST":
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)

    try:
        payment_data = json.loads(request.body)
    except json.JSONDecodeError:
        logger.error("Invalid JSON payload received")
        return JsonResponse({'success': False, 'error': 'Invalid JSON payload'}, status=400)

    # Extract required fields
    razorpay_order_id = payment_data.get('razorpay_order_id')
    razorpay_payment_id = payment_data.get('razorpay_payment_id')
    razorpay_signature = payment_data.get('razorpay_signature')

    # Validate required fields
    if not all([razorpay_order_id, razorpay_payment_id, razorpay_signature]):
        logger.error("Missing required fields in webhook payload")
        return JsonResponse({
            'success': False,
            'error': 'Missing required payment data'
        }, status=400)

    try:
        # Verify the payment signature first
        payment_verification = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        }

        razorpay_client.utility.verify_payment_signature(payment_verification)

        # Start a transaction for critical section
        with transaction.atomic():
            # Fetch payment record after signature verification
            try:
                payment = Payment.objects.select_for_update().get(
                    razorpay_order_id=razorpay_order_id
                )
            except Payment.DoesNotExist:
                logger.error(f"Payment record not found for order ID: {razorpay_order_id}")
                return JsonResponse({
                    'success': False,
                    'error': 'Payment record not found'
                }, status=404)

            # Update payment status
            payment.status = 'success'
            payment.razorpay_payment_id = razorpay_payment_id
            payment.save()

        # Send confirmation email (outside the transaction)
        try:
            sendmail(
                f"Dear {payment.user.email},\n\nYou have been successfully registered for ICMBGSD-2025.",
                payment.user.email,
                "ICMBGSD-2025 Registration Fee Payment"
            )
            logger.info(f"Payment confirmed and email sent to {payment.user.email}")
        except Exception as e:
            logger.error(f"Failed to send confirmation email: {str(e)}")
            # Continue execution even if email fails

        return JsonResponse({
            'success': True,
            'redirect_url': '/abstract_closed/'
        })

    except razorpay.errors.SignatureVerificationError as e:
        logger.error(f"Payment signature verification failed: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': 'Invalid payment signature'
        }, status=400)

    except Exception as e:
        logger.error(f"Unexpected error during payment verification: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': 'Internal server error'
        }, status=500)
