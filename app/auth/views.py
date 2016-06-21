from flask import render_template, redirect, request, url_for, flash, g, current_app
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


#@csrf_exempt
@auth.route('/charge/<plan_id>', methods=['GET', 'POST'])
def charge(plan_id):
    plan = Plan.query.filter_by(plan_id=plan_id).first()
    amount = plan.amount
    plan_name = plan.name
    if request.method == 'POST':
        #amount=request.form['amount']
        #plan=request.form['plan']
        #plan_name=request.form['plan_name']
	# Amount in cents

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


@auth.route('/success/<plan_id>', methods=['GET', 'POST'])
def success(plan_id):
    plan=Plan.query.filter_by(plan_id=plan_id).first() 
    plan_name=plan.name
    amount=plan.amount
    return render_template('success.html', plan_name=plan_name, amount=amount)
