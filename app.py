
import os
import stripe
from flask import Flask, request, session
from flask import render_template

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'secret')

stripe_pub_key = os.environ['STRIPE_PUB_KEY']
stripe.api_key = os.environ['STRIPE_SECRET_KEY']


@app.route('/')
def index():
    amount = request.args.get('amount', 0)
    reason = request.args.get('reason', '')
    try:
        amount = int(amount)
    except:
        amount = 0

    session['reason'] = reason
    return render_template(
        'index.html',
        key=stripe_pub_key,
        amount=amount,
        reason=reason,
    )


@app.route('/charge/<int:amount>', methods=['POST'])
def charge(amount):
    email = request.form['stripeEmail']
    token = request.form['stripeToken']
    reason = session.get('reason') or 'A Charge'
    stripe.Charge.create(
        receipt_email=email,
        source=token,
        amount=amount,
        currency='jpy',
        description=reason,
    )
    return render_template('success.html')