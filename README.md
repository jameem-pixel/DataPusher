# DataPusher
Face Infinics Interview Task

# Step for running the project
> 1. Download the project or pull it from the respository
> 2. Create a virtual environment with python 3.10 or above.
> 3. Go inside the folder where requirements.txt is located.
> 4. Run Command pip install -r requirements.txt
> 5. Go inside the folder where manage.py is located
> 6. Run Command python manage.py makemigrations
> 7. Run Command python manage.py migrate
> 8. Create superuser by running python manage.py createsuperuser


# List of URLs
> 1. 'server/account-list/' - Returns list of accounts in active mode (GET method).
> 2. 'server/account-create/' - Creates a new Account (POST method)
> 3. 'server/account-update/<account_id>/<mode>' - Account can be updated or deleted (POST method, parameter =[account_id, mode which is edit or delete]). 
> 4. 'server/'account-based-destination-list/<account_id>/' - Return Account type based Destination list (GET method)
> 5. 'server/destination-list/' - Returns list of destinations in active mode (GET method).
> 6. 'server/destination-create/' - Creates a new destinations (POST method)
> 7. 'server/destination-update/<account_id>/<mode>' - destinations can be updated or deleted (POST method, parameter =[account_id, mode which is edit or delete]).
> 8.  'server/incoming-data/' - Sends the data given to the respective destinations based on app secert token which is sent through the 'HTTP_X_AUTHORIZATION' in request.headers