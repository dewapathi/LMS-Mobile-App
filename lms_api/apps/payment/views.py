from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
import stripe.error

from lms_api.apps.course import models
from lms_api.apps.payment import models as payment_models

import stripe


stripe.api_key = settings.STRIPE_SECRET_KEY


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_payment_intent(request):
    try:
        course_id = request.data.get("course_id")
        if not course_id:
            return Response(
                {"error": "Course ID is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        course = models.Course.objects.get(id=course_id)
        amount_in_cents = int(course.price * 100)
        print(f"request.user.id: {request.user}")

        customer = stripe.Customer.create(
            name=request.user.first_name, email=request.user.email
        )

        intent = stripe.PaymentIntent.create(
            amount=amount_in_cents,
            currency="usd",
            customer=customer.id,
            automatic_payment_methods={  # disables auto methods
                "enabled": False
            },
            payment_method_types=["card"],
            metadata={"user_id": request.user.id, "course_id": course.id},
        )

        payment_models.Payment.objects.create(
            user=request.user,
            course=course,
            amount=course.price,
            transaction_id=intent["id"],
            status="PENDING",
        )

        return Response(
            {"client_secret": intent["client_secret"]}, status=status.HTTP_200_OK
        )
    except models.Course.DoesNotExist:
        return Response("Course not found!", status=status.HTTP_404_NOT_FOUND)

@csrf_exempt
def stripe_webhook(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed", status=405)

    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=400)
    except stripe.error.SignatureVerificationError:
        return JsonResponse({"error": "Invalid signature"}, status=400)

    if event["type"] == "payment_intent.succeeded":
        intent = event["data"]["object"]
        transaction_id = intent["id"]

        payment = payment_models.Payment.objects.filter(transaction_id=transaction_id).first()
        print(f"payment: {payment}")
        if payment:
            payment.status = "COMPLETED"
            payment.save()

    return HttpResponse(status=200)