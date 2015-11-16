Transport Portal


This software inteded for 3 types of users guests , staff and administrator.

1. Guests can only view the vehicle schedule.

2. Staff can view the schedule, book vehicles.

3. Administrator can modify vehicle schedule, manage users and add/remove vehicles.





For the installation process, please go through following bash commands and instructions


cd "Installation directory"

sudo apt-get update

#For installing python pip 
sudo apt-get install python-pip python-dev build-essential

#For installing virtual environment 
sudo apt-get install virtualenv
virtualenv env
source env/bin/activate

#For installing all the requirements
pip install -r /"Setup Directory"/requirements.txt
django-admin startproject transport
mv transport src
cd src
python manage.py migrate

#Command to create superuser Enter the admin details here
python manage.py createsuperuser 

python manage.py startapp main
mkdir -p static_pro/
#Copying the project files
cp /"Setup Directory"/main/models.py main/models.py
cp /"Setup Directory"/main/admin.py main/admin.py
cp /"Setup Directory"/main/forms.py main/forms.py
cp /"Setup Directory"/main/views.py main/views.py
cp /"Setup Directory"/main/tables.py main/tables.py
cp /"Setup Directory"/transport/urls.py transport/urls.py

gedit transport/settings.py
#Replace everything after SECRET_KEY = 'YOUR SECRET KEY????????' 
#with the contents of /"Setup Directory"/settingscopy.txt

cp -r /"Setup Directory"/templates templates
cp -r /"Setup Directory"/static_pro/our_static/ static_pro/our_static/

python manage.py collectstatic
python manage.py makemigrations
python manage.py migrate
#You can check your ip from ifconfig
ifconfig
python manage.py runserver <Replace ip from ifconfig>:<available port of your choice>

#Your server will be running now


# travelportal2
# travelportal2
# travelportal2
