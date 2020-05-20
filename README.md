# Sayur Django

The backend for an Angular 9 grocery ordering app and an order management system. 

To get Django running, get a Python 3 virtual environment running, instructions here: 
https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/

Then, install necessary packages using pip install -r req.txt
Then, you can run the server on whatever port and address using manage.py runserver. 
The angular frontend is configured by default to talk to localhost and port 8047, so you can run Django on that port,
or you can change the api url of the frontend app by changing src/environments/environment.ts in the angular code.

