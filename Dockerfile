# Use official Python image
FROM python:3

# Set the working directory
WORKDIR /app

# Copy dependencies first
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Expose the port Django runs on
EXPOSE 8000

WORKDIR ./order_manager_proj/

# Run migrations and start the Django app
CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn order_manager_proj.wsgi:application --bind 0.0.0.0:8000"]

