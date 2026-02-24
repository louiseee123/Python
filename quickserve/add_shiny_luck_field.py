import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quickserve.settings')
django.setup()

from pokemon.models import Trainer
from django.contrib.auth.models import User
from django.db import connection

# Add the field manually via raw SQL since migration didn't work
cursor = connection.cursor()
try:
    cursor.execute('ALTER TABLE pokemon_trainer ADD COLUMN shiny_luck INTEGER DEFAULT 1')
    print('Column added!')
except Exception as e:
    print(f'Column might already exist: {e}')

# Now set it for Lounelle
user = User.objects.get(username='Lounelle')
trainer = user.trainer
trainer.shiny_luck = 100
trainer.save()
print(f'Set shiny_luck = 100 for {trainer}')
