import stripe
from config.settings import STRIPE_API_KEY
from forex_python.converter import CurrencyRates

stripe.api_key = STRIPE_API_KEY


def convert_rub_to_dollars(amount):
    """Конвертирует рубли в доллары"""
    c = CurrencyRates()
    rate = c.get_rate('RUB', 'USD')
    return int(amount * rate)


def create_stripe_product(name, description):
    """Создание продукта в Stripe"""
    product = stripe.Product.create(name=name, description=description)
    return product.id


def create_stripe_price(product_id, amount):
    """Создание цены в Stripe"""
   # amount_usd = convert_rub_to_dollars(amount_rub)
    price = stripe.Price.create(
        product=product_id,
        unit_amount=int(amount * 100),  # сумма в центах
        currency='usd',
    )
    return price.id


def create_stripe_session(price_id):
    """Создание сессии оплаты в Stripe"""
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': price_id,
            'quantity': 1,
        }],
        mode='payment',
        success_url="https://127.0.0.1:8000/",
    )
    return session.get("id"), session.get("url")
