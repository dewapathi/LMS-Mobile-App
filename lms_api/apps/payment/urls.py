from django.urls import path

from .views import create_payment_intent, stripe_webhook


urlpatterns = [
    path("create-payment-intent/", create_payment_intent, name="create-payment-intent"),
    # path("payment/webhook/", stripe_webhook),
    path("webhook/", stripe_webhook, name="stripe-webhook")
]
