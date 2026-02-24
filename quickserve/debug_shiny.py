import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quickserve.settings')
django.setup()

from pokemon.models import Trainer
from django.contrib.auth.models import User

# Check Lounelle's trainer
try:
    user = User.objects.get(username='Lounelle')
    trainer = user.trainer
    print(f"Trainer: {trainer}")
    print(f"shiny_luck value: {getattr(trainer, 'shiny_luck', 'NOT SET')}")
    
    # Also check via raw SQL
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute("SELECT id, username FROM auth_user WHERE username = 'Lounelle'")
    user_row = cursor.fetchone()
    print(f"User row: {user_row}")
    
    cursor.execute("SELECT id, user_id, shiny_luck FROM pokemon_trainer WHERE user_id = %s", [user_row[0]])
    trainer_row = cursor.fetchone()
    print(f"Trainer row: {trainer_row}")
    
except Exception as e:
    print(f"Error: {e}")
