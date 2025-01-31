# DjangoVueRolePermissions

This project is a role and permissions-based system built using Django and Vue.js. It allows content to be shown to users based on their assigned roles and permissions.

## Features

- User authentication and authorization
- Role-based access control
- Permission-based content display
- Integration of Django (backend) and Vue.js (frontend)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/hbilal9/DjangoVueRolePermissions.git
    cd DjangoVueRolePermissions
    ```

2. Set up the backend (Django):
    ```bash
    python3 -m venv env
    source env/bin/activate
    pip install -r requirements.txt
    cp .env.example .env
    python manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver
    ```

3. Set up the frontend (Vue.js):
    ```bash
    cd frontend
    npm install
    npm run serve
    ```

## Usage

1. Access the Django admin panel at `http://127.0.0.1:8000/admin` and create roles and permissions.
2. Assign roles and permissions to users.
3. Users can log in and access content based on their assigned roles and permissions.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License.

## Developer
- [HBilal Khan Yousafzai](https://www.linkedin.com/in/hbilal-9/)
