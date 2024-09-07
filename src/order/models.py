from decimal import Decimal
from core.models import TimeStampMixin
from restaurant.models import Item
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
class Order(TimeStampMixin):
    class PaymentStatus(models.TextChoices):
        UNPAID = 'unpaid', _('Unpaid')
        PAID = 'paid', _('Paid')

    class PaymentMethod(models.TextChoices):
        CASH = 'cash', _('Cash')
        CARD = 'card', _('Card')

    placed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders'
    )
    payment_status = models.CharField(
        max_length=10, choices=PaymentStatus.choices, default=PaymentStatus.UNPAID
    )
    payment_method = models.CharField(
        max_length=10, choices=PaymentMethod.choices, default=PaymentMethod.CASH
    )
    payment_id = models.CharField(max_length=200, null=True, unique=True, blank=True)

    @property
    def subtotal(self):
        """Calculate the subtotal (sum of item prices multiplied by quantity) for the order."""
        return sum([Decimal(item.subtotal) for item in self.order_items.all()])

    @property
    def total(self):
        """Calculate the total, including tax."""
        tax_rate = Decimal(getattr(settings, 'TAX_PERCENT', 0)) / Decimal(100)
        tax = Decimal(self.subtotal) * tax_rate
        return round(Decimal(self.subtotal) + tax, 2)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    item = models.ForeignKey('restaurant.Item', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def subtotal(self):
        """Calculate the subtotal for this specific OrderItem."""
        return self.item.price * self.quantity

class Payment(TimeStampMixin):
    class PaymentStatus(models.TextChoices):
        UNPAID = 'unpaid', _('Unpaid')
        PAID = 'paid', _('Paid')
    order = models.ForeignKey(
        Order, on_delete=models.SET_NULL, null=True, related_name='payments')
    checkout_session_id = models.CharField(max_length=200, null=True)
    stripe_payment_intent_id = models.CharField(max_length=200, null=True)
    payer_email = models.EmailField(null=True)
    payer_name = models.CharField(max_length=100, null=True, blank=True)
    payer_phone = models.CharField(max_length=14, null=True, blank=True)
    payment_status = models.CharField(
        max_length=10, choices=PaymentStatus.choices, default=PaymentStatus.UNPAID)
    amount = models.FloatField(null=True)