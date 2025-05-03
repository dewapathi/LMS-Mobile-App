from .stripe_gateway import StripeGateway


def get_gateway(provider: str):
    if provider == "stripe":
        return StripeGateway()

    raise ValueError("Unsupported payment provider")
