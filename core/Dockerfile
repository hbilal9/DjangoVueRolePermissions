FROM python:3.12-alpine AS builder

# Set environment variables (adjust as needed)
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE core.settings

# Create and set the working directory in the container
WORKDIR /core

# Update the package list and install dependencies
RUN apk update && apk add --no-cache gcc musl-dev libffi-dev

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies using pip
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Final Stage (runtime)
FROM python:3.12-alpine

# Set environment variables (adjust as needed)
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE core.settings

# Create and set the working directory in the container
WORKDIR /core

# Copy the installed dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

# Ensure the `uvicorn` executable is available in the PATH
COPY --from=builder /usr/local/bin/uvicorn /usr/local/bin/uvicorn

# Copy the rest of the application code into the container
COPY . .

# Expose the port your Django application will run on (adjust as needed)
EXPOSE 8000

# RUN python manage.py migrate

# RUN python manage.py createsuperuser admin admin@gmail.com password

# Command to start the Django development server
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# Command to start Uvicorn ASGI server
# CMD ["uvicorn", "core.asgi:application", "--host", "0.0.0.0", "--port", "8000"]