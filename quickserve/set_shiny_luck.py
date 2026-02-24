import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quickserve.settings')
django.setup()

from pokemon.models import Trainer
from django.contrib.auth.models import User

# Find user Lounelle and set shiny_luck to 100
try:
    user = User.objects.get(username='Lounelle')
    trainer = user.trainer
    trainer.shiny_luck = 100
    trainer.save()
    print(f'Set shiny_luck to 100 for {user.username}')
except User.DoesNotExist:
    print('User Lounelle not found')
except Exception as e:
    print(f'Error: {e}')
