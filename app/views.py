from flask import render_template, redirect, request, url_for, flash, g, current_app, json
from flask_api import status
import stripe
from app.models import User, Plan
from .. import csrf
from .. import db

# Set your secret key: remember to change this to your live secret key in production
# See your keys here https://dashboard.stripe.com/account/apikeys
stripe.api_key = "sk_test_vv1QGRslGX4eXCSfZLc0KcoZ"

# Webhooks are always sent as HTTP POST requests, so we want to ensure
# that only POST requests will reach your webhook view. We can do that by
# decorating `webhook()` with `require_POST`.
#
# Then to ensure that the webhook view can receive webhooks, we need
# also need to decorate `webhook()` with `csrf_exempt`.
@require_POST
#@csrf_exempt
@app.route('/')
def webhook(request):
  # Retrieve the request's body and parse it as JSON
    event_json = json.load(request.body)

  # Do something with event_json
    print event_json
    u=User.query.filter_by(id=g.user.id).first()
    # Do something here e.g update the user database or/and email notification
    return status_HTTP_200_OK
