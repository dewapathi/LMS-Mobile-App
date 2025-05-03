from django.conf import settings

from rest_framework import status

from .base_payment import PaymentGateway

from lms_api.apps.payment.models import Payment

import stripe


class StripeGateway(PaymentGateway):
    def create_payment_intent(self, user, course):
        customer = stripe.Customer.create(name=user.first_name, email=user.email)
        intent = stripe.PaymentIntent.create(
            amount=int(course.price * 100),
            currency="usd",
            customer=customer.id,
            payment_method_types=["card"],
            metadata={"user_id": user.id, "course_id": course.id},
        )

        Payment.objects.create(
            user=user,
            course=course,
            amount=course.price,
            transaction_id=intent["id"],
            status="PENDING",
        )

        return intent["client_secret"]

    def handle_webhook(self, payload, sig_header):
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        except Exception as e:
            return {"error": str(e), "status": status.HTTP_400_BAD_REQUEST}

        if event["type"] == "payment_intent.succeeded":
            intent = event["data"]["object"]
            payment = Payment.objects.filter(transaction_id=intent["id"]).first()
            if payment:
                payment.status = "COMPLETED"
                payment.save()

        elif event["type"] == "payment_intent.payment_failed":
            intent = event["data"]["object"]
            failure_reason = getattr(
                intent.last_payment_error, "message", "Unknown error"
            )
            payment = Payment.objects.filter(transaction_id=intent["id"]).first()
            if payment:
                payment.status = "FAILED"
                payment.failure_reason = failure_reason
                payment.save()

        return {"status": status.HTTP_200_OK}
