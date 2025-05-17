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

//celery and redis
redis-server
celery -A lms_api worker --loglevel=info


//run redis server with powershell windows
wsl --install
sudo apt update
sudo apt install redis

//to chnage redis port
sudo lsof -i :6380
redis-server --port 6380
sudo systemctl restart redis-server

//to run celery
celery -A your_project_name worker --loglevel=info

//if get permission issue
celery -A lms_api worker --loglevel=info --pool=solo

//run server
python manage.py runserver 0.0.0.0:8000
python manage.py runserver

