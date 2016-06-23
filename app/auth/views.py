from flask import render_template, redirect, request, url_for, flash, g, current_app, json
import stripe
from . import auth
from app.models import User, Plan
from .. import csrf
from .. import db

@auth.route('/', methods=['GET', 'POST'])
def index():
    plans=Plan.query.all()
    if request.method == 'POST':
        plan_id = request.form.get('plan_select') 
        plan=Plan.query.filter_by(plan_id=plan_id).first()
        print plan
        amount = plan.amount
        print amount
        print request.form
        return redirect(url_for('auth.charge', plan_id=plan_id))       
        #return redirect(url_for('auth.charge', amount=amount, plan=plan.name, plan_id=plan_id))       
    return render_template('index.html', plans=plans)


@auth.route('/charge/<plan_id>', methods=['GET', 'POST'])
def charge(plan_id):
    plan = Plan.query.filter_by(plan_id=plan_id).first()
    # Amount in cents for the stripe API
    amount = plan.amount
    plan_name = plan.name
    if request.method == 'POST':

	customer = stripe.Customer.create(
            plan=plan_id,
	    email=request.form['email'],
	    source=request.form['stripeToken']
	)

	charge = stripe.Charge.create(
	    customer=customer.id,
            amount=amount,
	    currency='usd',
	    description=plan_name
	)
	return redirect(url_for('auth.success', plan_id=plan_id))

    return render_template('checkout.html',
        #amount=int(request.args.get('amount')), plan=request.args.get('plan'), plan_id=request.args.get('plan_id'), key=current_app.config['STRIPE_KEYS']['publishable_key'])
        amount=amount, plan_name=plan_name, plan_id=plan_id, key=current_app.config['STRIPE_KEYS']['publishable_key'])

@auth.route('/success/<plan_id>', methods=['GET'])
def success(plan_id):
    plan=Plan.query.filter_by(plan_id=plan_id).first()
    plan_name=plan.name
    amount=plan.amount
    return render_template('success.html', plan_name=plan_name, amount=amount)


# Webhooks are always sent as HTTP POST requests, so we want to ensure
# that only POST requests will reach your webhook view. We can do that by
# decorating `webhook()`.
#
# Then to ensure that the webhook view can receive webhooks, we need
# also need to decorate `webhook()` with `csrf_exempt`.
@csrf.exempt
@auth.route('/webhook', methods=['POST'])
def webhook():
    stripe.api_key=current_app.config['STRIPE_KEYS']['secret_key']
    # Retrieve the request's body and parse it as JSON
    event_json = request.get_json()

    #Do something with event_json
    import pprint
    pprint.pprint(event_json['data'], width=1)
    #customer's id
    print event_json['data']['object']['id']
    #customer's email
    print event_json['data']['object']['email']
    #plan's id
    print event_json['data']['object']['subscriptions']['data'][0]['plan']['id']
    if event_json['type'] == 'charge.succeeded':
        print True
        customer_email= event_json['data']['object']['email']  #customer's email
        #Do something here e.g update the user database or/and email notification
        #u=User.query.filter_by(email=customer_email).first()
        #E.g if users have a column payment we can update it
        #setattr(u, payment, True)
        #p=Plan.query.filter_by(id=plan_id).first()
        #setattr(p, users, u.username)

        #db.session.add(u)
        #db.session.add(p)
        #db.session.commit()
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
