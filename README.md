A. Pull from github and run the stripe flask app
1. git clone git@github.com:Pathio/pathio-stripe.git && pull origin master
2. cd stripe && pip install -r requirements.txt
3. python manage.py db init
4. python manage.py db upgrade
5. To populate the plans db with the stripe plans id, names and amounts
   python manage.py shell
   >>> p=Plan()
   >>> p.insert_plan_descriptions()  
6. python manage.py runserver
7. navigate to 127.0.0.1:5000/auth/

B. Steps for the stripe flask app with blueprint 'auth' - it can help with how to integrate the app to an existing project.

1. In virtualenv or machine install stripe with

	pip install --upgrade stripe

2. Edit config.py with the stripe secret and public keys, first the test versions, then with the live versions for the production environment. Get the keys from your stripe account here
	https://dashboard.stripe.com/account/apikeys

3. Install Flask-SQLalchemy so flask talks to sqlite or any other database we have configured in config.py

4. Create the views for the payment - in this strip app, they are located at app/auth/views.py - replace app dir with your desirable dir depending which route you want to use e.g it can be under the auth dir so that's accessible for authenticated users.

5. Create the webhook views for receiveng stripe responses when subscription events are completed. here this is located at app/views.py. In this file we can also set the actions we want to happen when subscriptions succeed, e.g send an email or/and update the users, plans databases.

6. Create the templates - see app/template dir

6. Other dependecies:
  pip install coverage -- (for testing)
  pip install Flask-Script
  pip install Flask-Migrate -- (for manager migration command)
