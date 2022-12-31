Clone this git repository in local machine using git clone httplink command

Create a virtual environment using virtualenv environmentname

Start the virtual environment using source environmentname/bin/activate

Move to the project directory

Install the modules required to run this project using pip3 install -r requirements.txt

Make migrations, Create superuser

Create database in pgadmin write the credentials in settings.py

Create models and make migrations

To write data to database use python manage.py write_data_to_database

To run the project use python manage.py runserver