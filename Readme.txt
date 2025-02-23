mkdir lms_backend
cd lms_backend

python -m venv venv
.\venv\Scripts\activate

touch requirements.txt
pip install -r requirements.txt

django-admin startproject lms_api .

mkdir -p lms_api/apps
cd lms_api/apps

django-admin startapp core
django-admin startapp users
django-admin startapp course
django-admin startapp payment
django-admin startapp enrollment
django-admin startapp notifications


python manage.py makemigrations
python manage.py migrate


//conenct db
netstat -ano | findstr :5432
psql -U postgres
CREATE DATABASE lms_db;
CREATE USER lms_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE lms_db TO lms_user;
psql -U lms_user -d lms_db -h localhost -W

