# Setup project
## Tạo môi trường ảo
### Linux:
```sh
virtualenv env
```
```sh
source env/bin/activate
```
### Other Operation system: tự tìm hiểu

## Install requirements
### Install requirements
```sh
pip install -r requirements.txt
```

## Copy env
```sh
cp env-sample .env
```
## Makemigrattions database khi có thay đổi ở model 

```sh
python manage.py makemigrations
```
## Migrate database

```sh
python manage.py migrate
```

## Run server
```sh
python manage.py runserver
```

# Tạo 1 app mới
```sh
django-admin startapp <app_name>
```