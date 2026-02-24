import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quickserve.settings')
django.setup()

from pokemon.models import Trainer
from django.contrib.auth.models import User

# Update Lounelle to have 999 pokeballs
try:
    user = User.objects.get(username='Lounelle')
    trainer = Trainer.objects.get(user=user)
    trainer.pokeball_count = 999
    trainer.save()
    print(f'Success! Lounelle now has {trainer.pokeball_count} pokeballs')
except User.DoesNotExist:
    print('User Lounelle not found')
except Trainer.DoesNotExist:
    print('Trainer profile not found for Lounelle')
