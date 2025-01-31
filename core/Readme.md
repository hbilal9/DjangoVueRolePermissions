## Developer
- [HBilal Khan Yousafzai](https://www.linkedin.com/in/hbilal-9/)

## Clone the repository
```bash
git clone https://github.com/axlic/tire-backend.git backend
```

## Install dependencies
create a virtual environment and install the dependencies

Windows
```bash
python -m venv venv
```
Mac
```bash
python3 -m venv venv
```

### Activate the virtual environment

Windows
```bash
venv\Scripts\activate
```
Mac
```bash
source venv/bin/activate
```

### Install the dependencies
```bash
pip install -r requirements.txt
```

## Copy a .env file
```bash
cp .env.example .env
```
update the .env file with your own settings

## Migrate the database
```bash
python manage.py migrate
```

## Create a superuser
```bash
python manage.py createsuperuser
```

## Run the server
```bash
python manage.py runserver
```