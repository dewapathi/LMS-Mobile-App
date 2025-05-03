from abc import ABC, abstractmethod


class PaymentGateway(ABC):
    @abstractmethod
    def create_payment_intent(self, user, course):
        pass

    @abstractmethod
    def handle_webhook(self, payload, sig_header):
        pass
