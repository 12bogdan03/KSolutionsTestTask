import requests
import json

from flask import render_template, jsonify, request

from payment import app, db
from config import PAY_TRIO_SHOP_ID

from .forms import PaymentForm
from .utils import generate_sign
from .models import Payment


@app.route('/', methods=['GET', 'POST'])
def index():
    form = PaymentForm()
    return render_template('index.html', form=form)


@app.route('/ajax-data', methods=['POST'])
def ajax_data():
    data = dict()
    for key, value in request.form.items():
        data[key] = value
    payment = Payment(amount=float(data['amount']),
                      currency=data['currency'],
                      description=data['description'])
    db.session.add(payment)
    db.session.commit()
    data.pop('description', None)
    data['shop_invoice_id'] = payment.id
    return jsonify({'sign': generate_sign(data),
                    'shop_invoice_id': payment.id})


@app.route('/ajax-invoice', methods=['POST'])
def ajax_invoice():
    data = dict()
    data['payway'] = 'payeer_eur'
    data['description'] = request.form['description']
    data['shop_invoice_id'] = request.form['shop_invoice_id']
    data['currency'] = request.form['currency']
    data['amount'] = request.form['amount']
    data['shop_id'] = PAY_TRIO_SHOP_ID
    data['sign'] = request.form['sign']

    r = requests.post("https://central.pay-trio.com/invoice", data=json.dumps(data),
                      headers={'Content-type': 'application/json'})

    if r.json()['result'] == 'ok':
        new_form_html = str()
        for key, value in r.json()['data']['data'].items():
            new_form_html += '<input name="{}" value="{}" hidden />'.format(key, value)
        method = r.json()['data']['method']
        action = r.json()['data']['source']
        return jsonify({
            'status': 'ok',
            'new_form_html': new_form_html,
            'method': method,
            'action': action
        })
    else:
        return jsonify({'status': 'error'})





