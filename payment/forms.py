from flask_wtf import FlaskForm
from wtforms import FloatField, SelectField, StringField
from wtforms.widgets import TextArea, HiddenInput

from config import PAY_TRIO_SHOP_ID


class PaymentForm(FlaskForm):
    CURRENCY_CHOICES = (
        ('840', 'USD'),
        ('978', 'EUR')
    )

    amount = FloatField('Amount')
    currency = SelectField('Currency',
                           choices=CURRENCY_CHOICES,
                           default='USD')
    description = StringField('Description',
                              widget=TextArea())
    sign = StringField(widget=HiddenInput())
    shop_id = StringField(widget=HiddenInput(), default=PAY_TRIO_SHOP_ID)
    shop_invoice_id = StringField(widget=HiddenInput())
