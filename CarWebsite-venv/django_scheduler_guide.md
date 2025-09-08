# Django APScheduler Implementation Guide

## Problem Solved
Fixed the Django error: "Accessing the database during app initialization is discouraged"

## Solution Overview
Use AppConfig.ready() with RUN_MAIN environment variable check to start scheduler after Django initialization, preventing database access during app startup.

## Prerequisites
```bash
pip install apscheduler
pip install django-apscheduler
pip install djangorestframework  # For JSONParser if needed
```

## Project Structure

Your Django app should be organized like this:

```
your_project/
├── your_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── website/  # Your app directory
│   ├── __init__.py
│   ├── apps.py              # Contains WebsiteConfig
│   ├── models.py            # Contains your models
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── my_apps/             # Custom subdirectory for scheduler
│       ├── __init__.py
│       └── schedular.py     # Your scheduler implementation
├── manage.py
└── requirements.txt
```

**Important**: The scheduler file must be in a subdirectory (like `my_apps/`) to avoid circular import issues.

## Step-by-Step Implementation

### 1. Add to INSTALLED_APPS
```python
# settings.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',       # If using JSONParser
    'django_apscheduler',   # Required for scheduler
    'website',              # Your app
]
```

### 2. Configure Logging (Recommended)
```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'website': {  # Replace with your app name
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
```

### 3. Create Your Models
```python
# models.py
from django.db import models

class GeneralInformation(models.Model):
    info = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"General Info - {self.updated_at}"
```

### 4. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Configure AppConfig
```python
# apps.py
from django.apps import AppConfig

class WebsiteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'website'  # Must match your app directory name

    def ready(self):
        import os
        # Only start scheduler in main process, not reloader process
        if os.environ.get("RUN_MAIN") == "true":
            from .my_apps import schedular
            schedular.start()
```

### 6. Create Scheduler Implementation
```python
# my_apps/schedular.py
from django_apscheduler.jobstores import DjangoJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.models import DjangoJobExecution
import logging
import requests
from website.models import GeneralInformation
from io import BytesIO
from rest_framework.parsers import JSONParser

logger = logging.getLogger(__name__)

def your_scheduled_job_function():
    """
    Your main scheduled job function.
    Replace this with your actual business logic.
    """
    try:
        logger.info("Starting scheduled job...")
        
        # Your job logic here
        attrs = ["bodies.type", "engines.cylinders", "engines.drive_type", 
                "engines.engine_type", "engines.fuel_type", "engines.transmission", "engines.valves"]
        data_dict = {}
        
        for attr in attrs:
            url = f"https://carapi.app/api/vehicle-attributes?attribute={attr}"
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            r = BytesIO(response.content)
            parser = JSONParser()
            data = parser.parse(stream=r)
            data_dict[attr] = data

        # Update or create record
        GeneralInformation.objects.update_or_create(
            defaults={
                "info": {
                    "body_types": data_dict["bodies.type"],
                    "cylinders": data_dict["engines.cylinders"],
                    "drive_types": data_dict["engines.drive_type"],  # Fixed typo
                    "engine_types": data_dict["engines.engine_type"],
                    "fuel_types": data_dict["engines.fuel_type"],
                    "transmission": data_dict["engines.transmission"],
                    "valves": data_dict["engines.valves"]
                }
            }
        )
        
        logger.info("Scheduled job completed successfully")
        
    except Exception as e:
        logger.error(f"Scheduled job failed: {str(e)}")

def delete_old_job_executions(max_age=604_800):
    """Delete old job executions (default: 7 days)"""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)

def start():
    """Initialize and start the scheduler"""
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")

    # Add your main scheduled job
    scheduler.add_job(
        your_scheduled_job_function,
        trigger=CronTrigger(hour="*/6"),  # Every 6 hours
        id="your_main_job_id",
        max_instances=1,  # Prevent overlapping executions
        replace_existing=True,
    )

    # Add cleanup job for old executions
    scheduler.add_job(
        delete_old_job_executions,
        trigger=CronTrigger(day_of_week="sun", hour="23", minute="59"),
        id="delete_old_job_executions",
        max_instances=1,
        replace_existing=True,
    )

    try:
        logger.info("Starting scheduler...")
        scheduler.start()
        logger.info("Scheduler started successfully!")
    except KeyboardInterrupt:
        logger.info("Stopping scheduler...")
        scheduler.shutdown()
        logger.info("Scheduler shut down successfully!")
```

## Key Concepts Explained

### Why RUN_MAIN Check is Required
- Django's development server (`runserver`) creates **two processes**:
  1. **Main process**: Handles actual HTTP requests
  2. **Reloader process**: Monitors file changes for auto-reload
- Without the `RUN_MAIN` check, your scheduler would start in **both processes**
- `RUN_MAIN='true'` environment variable only exists in the main process
- This prevents duplicate job executions and database conflicts

### Common Cron Trigger Patterns
```python
# Every 6 hours
CronTrigger(hour="*/6")

# Daily at 2:00 AM
CronTrigger(hour=2, minute=0)

# Every weekday at 9:00 AM  
CronTrigger(day_of_week='mon-fri', hour=9, minute=0)

# Every 30 seconds (for testing)
CronTrigger(second="*/30")

# Every 45 seconds (for testing)
CronTrigger(second="*/45")

# Weekly on Sunday at 11:59 PM
CronTrigger(day_of_week="sun", hour="23", minute="59")
```

### Important Parameters
- `max_instances=1`: Prevents overlapping job executions
- `replace_existing=True`: Replaces job with same ID if it exists
- `id`: Unique identifier for the job (used for replacing/removing)

## Testing Your Implementation

### 1. Start the Development Server
```bash
python manage.py runserver
```

### 2. Expected Console Output
You should see messages like:
```
Watching for file changes with StatReloader
Performing system checks...
System check identified no issues (0 silenced).
Starting scheduler...
Scheduler started successfully!
Starting development server at http://127.0.0.1:8000/
```

### 3. Job Execution Logs
When jobs run, you'll see:
```
INFO Starting scheduled job...
INFO Scheduled job completed successfully
```

## Troubleshooting

### Scheduler Not Starting
1. Verify `RUN_MAIN` environment variable: Add `print(os.environ.get("RUN_MAIN"))` to debug
2. Check import paths: Ensure `from .my_apps import schedular` is correct
3. Verify app is in `INSTALLED_APPS`

### Jobs Not Executing
1. Check for job errors in console logs
2. Verify cron trigger syntax
3. Ensure database migrations are applied
4. Check if previous job instance is still running

### Database Access Errors
- Confirm scheduler start is only in `AppConfig.ready()`
- Don't put database queries in module-level imports
- Use the `RUN_MAIN` environment check

## Production Considerations

### For Production Deployment
- Consider using **Celery** instead of APScheduler for production
- The `RUN_MAIN` check is development-specific
- Set up proper logging and monitoring
- Use environment variables for configuration

### Job Monitoring
```python
# Add this to view job status in Django admin
# admin.py
from django.contrib import admin
from django_apscheduler.models import DjangoJobExecution

@admin.register(DjangoJobExecution)
class DjangoJobExecutionAdmin(admin.ModelAdmin):
    list_display = ['id', 'job_id', 'status', 'run_time', 'duration']
    list_filter = ['status', 'run_time']
```

## Working Example Files

Based on the actual implementation, here are the complete working files:

### apps.py
```python
from django.apps import AppConfig

class WebsiteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'website'

    def ready(self):
        import os
        if os.environ.get("RUN_MAIN") == "true":
            from .my_apps import schedular
            print(schedular.start())
```

### schedular.py
```python
from django_apscheduler.jobstores import DjangoJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import logging
import requests
from website.models import GeneralInformation
from io import BytesIO
from rest_framework.parsers import JSONParser
logger = logging.getLogger(__name__)

def GeneralInformation_Model_Updater():
    attrs = ["bodies.type", "engines.cylinders", "engines.drive_type", "engines.engine_type", 
                "engines.fuel_type", "engines.transmission", "engines.valves"]
    data_dict = {}
    for i in attrs:
        url = "https://carapi.app/api/vehicle-attributes?attribute="
        url += i
        recieved = requests.get(url)
        r = BytesIO(recieved.content)
        parser  = JSONParser()
        data = parser.parse(stream=r)
        data_dict[i] = data

    GeneralInformation.objects.update_or_create(info={"body_types":data_dict["bodies.type"],
                                                    "cylinders":data_dict["engines.cylinders"],
                                                    "derive_types":data_dict["engines.drive_type"],
                                                    "engine_types":data_dict["engines.engine_type"],
                                                    "fuel_types":data_dict["engines.fuel_type"],
                                                    "transmission":data_dict["engines.transmission"],
                                                    "valves":data_dict["engines.valves"]})
    logger.info("update was successful")



def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")

    scheduler.add_job(
        GeneralInformation_Model_Updater,
        trigger=CronTrigger(second="*/45"),
        id="updates the GeneralInformation model every 6 hours",
        replace_existing=True
    )

    logger.info("added the job 'updates the GeneralInformation model evety 6 hours'")

    scheduler.start()
    logger.info("job is started")
```

## Retrieving JSON Data from Database

Once your scheduler is running and populating data, you'll want to retrieve and display this JSON data in your Django views and templates.

### Step 1: Create View Functions

Create view functions to retrieve the JSON data from your `GeneralInformation` model:

```python
# views.py
from django.shortcuts import render
from django.http import JsonResponse
from .models import GeneralInformation
import json

def general_info_view(request):
    """
    Retrieve general information data and send to template
    """
    try:
        # Get the latest GeneralInformation record
        general_info = GeneralInformation.objects.latest('updated_at')
        
        # Extract the JSON data
        info_data = general_info.info
        
        # You can also format the data if needed
        context = {
            'general_info': info_data,
            'last_updated': general_info.updated_at,
            'body_types': info_data.get('body_types', []),
            'cylinders': info_data.get('cylinders', []),
            'drive_types': info_data.get('derive_types', []),  # Note: keeping your field name
            'engine_types': info_data.get('engine_types', []),
            'fuel_types': info_data.get('fuel_types', []),
            'transmissions': info_data.get('transmission', []),
            'valves': info_data.get('valves', []),
        }
        
        return render(request, 'website/general_info.html', context)
        
    except GeneralInformation.DoesNotExist:
        # Handle case where no data exists yet
        context = {
            'error_message': 'No general information data available yet. Please wait for the scheduler to run.',
            'general_info': None,
        }
        return render(request, 'website/general_info.html', context)

def general_info_api(request):
    """
    API endpoint to return JSON data directly
    """
    try:
        general_info = GeneralInformation.objects.latest('updated_at')
        return JsonResponse({
            'success': True,
            'data': general_info.info,
            'last_updated': general_info.updated_at,
        })
    except GeneralInformation.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'No data available',
        }, status=404)
```

### Step 2: Configure URLs

```python
# website/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.general_info_view, name='general_info'),
    path('api/general-info/', views.general_info_api, name='general_info_api'),
]
```

```python
# your_project/urls.py (main urls.py)
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('website.urls')),
]
```

### Step 3: Create Templates

Create your template directory structure and HTML templates to display the data:

```
website/
├── templates/
│   └── website/
│       ├── base.html
│       └── general_info.html
└── ...
```

**Base Template:**
```html
<!-- templates/website/base.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Vehicle Information{% endblock %}</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 40px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .section {
            margin: 20px 0;
            padding: 20px;
            background: #f9f9f9;
            border-radius: 5px;
        }
        .section h3 {
            color: #333;
            border-bottom: 2px solid #007bff;
            padding-bottom: 10px;
        }
        .items {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 15px;
        }
        .item {
            background: #007bff;
            color: white;
            padding: 8px 15px;
            border-radius: 20px;
            font-size: 14px;
        }
        .error {
            color: #dc3545;
            text-align: center;
            padding: 20px;
        }
        .last-updated {
            text-align: center;
            color: #666;
            font-size: 14px;
            margin-bottom: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        {% block content %}
        {% endblock %}
    </div>
</body>
</html>
```

**Main Template:**
```html
<!-- templates/website/general_info.html -->
{% extends 'website/base.html' %}

{% block title %}Vehicle General Information{% endblock %}

{% block content %}
<h1>Vehicle General Information</h1>

{% if error_message %}
    <div class="error">
        <h2>{{ error_message }}</h2>
        <p>The scheduler will automatically populate this data. Please check back later.</p>
    </div>
{% elif general_info %}
    
    {% if last_updated %}
    <div class="last-updated">
        <strong>Last Updated:</strong> {{ last_updated|date:"F d, Y H:i" }}
    </div>
    {% endif %}

    {% if body_types %}
    <div class="section">
        <h3>Body Types</h3>
        <div class="items">
            {% for item in body_types %}
                <span class="item">{{ item }}</span>
            {% endfor %}
        </div>
    </div>
    {% endif %}

    {% if cylinders %}
    <div class="section">
        <h3>Engine Cylinders</h3>
        <div class="items">
            {% for item in cylinders %}
                <span class="item">{{ item }}</span>
            {% endfor %}
        </div>
    </div>
    {% endif %}

    {% if drive_types %}
    <div class="section">
        <h3>Drive Types</h3>
        <div class="items">
            {% for item in drive_types %}
                <span class="item">{{ item }}</span>
            {% endfor %}
        </div>
    </div>
    {% endif %}

    {% if engine_types %}
    <div class="section">
        <h3>Engine Types</h3>
        <div class="items">
            {% for item in engine_types %}
                <span class="item">{{ item }}</span>
            {% endfor %}
        </div>
    </div>
    {% endif %}

    {% if fuel_types %}
    <div class="section">
        <h3>Fuel Types</h3>
        <div class="items">
            {% for item in fuel_types %}
                <span class="item">{{ item }}</span>
            {% endfor %}
        </div>
    </div>
    {% endif %}

    {% if transmissions %}
    <div class="section">
        <h3>Transmission Types</h3>
        <div class="items">
            {% for item in transmissions %}
                <span class="item">{{ item }}</span>
            {% endfor %}
        </div>
    </div>
    {% endif %}

    {% if valves %}
    <div class="section">
        <h3>Valve Configurations</h3>
        <div class="items">
            {% for item in valves %}
                <span class="item">{{ item }}</span>
            {% endfor %}
        </div>
    </div>
    {% endif %}

    <!-- Raw JSON data (for debugging) -->
    <details style="margin-top: 30px;">
        <summary>Raw JSON Data (Click to expand)</summary>
        <pre style="background: #f8f9fa; padding: 20px; border-radius: 5px; overflow-x: auto;">{{ general_info|pprint }}</pre>
    </details>

{% else %}
    <div class="error">
        <h2>No data available</h2>
        <p>Please wait for the scheduler to fetch data.</p>
    </div>
{% endif %}

<!-- Add refresh button -->
<div style="text-align: center; margin-top: 30px;">
    <button onclick="location.reload()" style="background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer;">
        Refresh Data
    </button>
</div>

{% endblock %}
```

### Step 4: Test Your Implementation

1. **Run your server:**
   ```bash
   python manage.py runserver
   ```

2. **Visit your URLs:**
   - Main page: `http://127.0.0.1:8000/`
   - API endpoint: `http://127.0.0.1:8000/api/general-info/`

3. **Expected behavior:**
   - If no data exists: Shows "No data available" message
   - If data exists: Shows organized vehicle information in a clean interface
   - Data updates automatically when your scheduler runs

### Enhanced View (Optional)

For more control over data processing:

```python
def general_info_enhanced_view(request):
    """
    Enhanced view with better data handling
    """
    try:
        general_info = GeneralInformation.objects.latest('updated_at')
        info_data = general_info.info
        
        # Process and clean the data
        processed_data = {}
        field_mapping = {
            'body_types': 'Body Types',
            'cylinders': 'Engine Cylinders', 
            'derive_types': 'Drive Types',
            'engine_types': 'Engine Types',
            'fuel_types': 'Fuel Types',
            'transmission': 'Transmission Types',
            'valves': 'Valve Configurations'
        }
        
        for key, display_name in field_mapping.items():
            data_list = info_data.get(key, [])
            if isinstance(data_list, list) and data_list:
                processed_data[key] = {
                    'display_name': display_name,
                    'items': sorted(set(data_list)),  # Remove duplicates and sort
                    'count': len(set(data_list))
                }
        
        context = {
            'processed_data': processed_data,
            'last_updated': general_info.updated_at,
            'total_categories': len(processed_data),
        }
        
        return render(request, 'website/general_info_enhanced.html', context)
        
    except GeneralInformation.DoesNotExist:
        context = {
            'error_message': 'No data available yet. The scheduler will populate this automatically.',
        }
        return render(request, 'website/general_info_enhanced.html', context)
```

## Troubleshooting: Scheduler Trigger Changes Not Taking Effect

A common issue occurs when you modify the scheduler trigger timing (e.g., changing from every 6 hours to every 5 minutes) but the changes don't take effect. This happens because the old job is already registered in the database and persists even when you modify your code.

### Solution: Clear the Job Store

The most reliable way to fix this is to clear the existing job records from the database and restart the server:

```python
# Method 1: Using Django Shell
# Run: python manage.py shell

from django_apscheduler.models import DjangoJob, DjangoJobExecution

# Delete existing jobs and executions
DjangoJob.objects.all().delete()
DjangoJobExecution.objects.all().delete()

# Exit shell and restart your server
# python manage.py runserver
```

```python
# Method 2: Create a Management Command (Recommended)
# Create: management/commands/clear_scheduler_jobs.py

from django.core.management.base import BaseCommand
from django_apscheduler.models import DjangoJob, DjangoJobExecution

class Command(BaseCommand):
    help = 'Clear all scheduler jobs and executions'

    def handle(self, *args, **options):
        job_count = DjangoJob.objects.count()
        execution_count = DjangoJobExecution.objects.count()
        
        DjangoJob.objects.all().delete()
        DjangoJobExecution.objects.all().delete()
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully cleared {job_count} jobs and {execution_count} executions'
            )
        )
```

Then run:
```bash
python manage.py clear_scheduler_jobs
python manage.py runserver
```

### Why This Happens
- APScheduler stores job information in the database via `DjangoJobStore`
- When you change trigger timing in your code, the old job record remains in the database
- The scheduler loads the existing job record instead of creating a new one with your updated trigger
- `replace_existing=True` doesn't always work as expected with trigger changes

### Verification
After clearing and restarting, you should see logs confirming the new trigger:
```
Starting scheduler...
Added job with new trigger: cron[minute='*/5']
Scheduler started successfully!
```

## Summary

This guide provides a complete implementation for Django APScheduler that:
- ✅ Prevents database access during app initialization
- ✅ Uses proper process isolation with `RUN_MAIN` check
- ✅ Includes comprehensive error handling and logging
- ✅ Provides a scalable structure for multiple scheduled jobs
- ✅ Works reliably in Django development environment
- ✅ Includes complete view and template setup for displaying JSON data
- ✅ Includes troubleshooting for common scheduling issues

Save this guide for future Django projects that need background job scheduling with data visualization!