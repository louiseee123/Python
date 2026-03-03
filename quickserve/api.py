import os
import sys

# Add the project directory to the path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quickserve.settings')

# Import the WSGI application
from quickserve.wsgi import application

# For Vercel serverless, we need to wrap the WSGI app
from werkzeug.wsgi import DispatcherMiddleware

# Vercel requires the application to be called 'app'
app = DispatcherMiddleware(application, {
    '/': application
})
