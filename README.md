A. Quick setup for subscription payments

1. Pull repo

2. cd stripe && pip install -r requirements.txt

3. python manage.py db upgrade

4. To populate the database with subscription plans id, names and amounts
   
		python manage.py shell

   		p=Plan()
   		p.insert_plan_descriptions()  

6. python manage.py runserver

7. navigate to 127.0.0.1:5000/auth/

