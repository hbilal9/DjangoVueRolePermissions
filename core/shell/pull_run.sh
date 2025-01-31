#!/bin/bash

echo "Changing directory to env.."
cd /var/www/backend
echo "Directory changed to $PWD"

source venv/bin/activate

echo "Changing directory to project.."
cd /var/www/backend/core
echo "Directory changed to $PWD"

# Pulls the latest version of the generator from the repository
echo "Pulling latest version of code from repository.."
sudo git pull origin master
echo "Latest version of code pulled"

# install requirements
echo "Installing requirements.."
pip install -r requirements.txt
echo "Requirements installed"

# migrate
echo "Migrating.."
python manage.py migrate
echo "Migrated"

# collect static
# echo "Collecting static files.."
# python manage.py collectstatic --noinput
# echo "Collected static files"

# restart gunicorn
echo "Restarting gunicorn.."
sudo systemctl restart gunicorn
echo "Gunicorn restarted"

# restart nginx
echo "Restarting nginx.."
sudo systemctl restart nginx
echo "Nginx restarted"