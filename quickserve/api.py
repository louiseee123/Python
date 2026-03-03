import os
import sys

# Add the project directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quickserve.settings')

# Import the WSGI application
from quickserve.wsgi import application

# Vercel requires the application to be called 'app'
app = application
