import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quickserve.settings')
django.setup()

from django.db import connection

# Update shiny_luck to 100
cursor = connection.cursor()
cursor.execute('UPDATE pokemon_trainer SET shiny_luck = 100 WHERE id = 1')
print('Updated shiny_luck to 100 for trainer id 1')

# Verify
cursor.execute('SELECT id, shiny_luck FROM pokemon_trainer WHERE id = 1')
print(f'Verified: {cursor.fetchone()}')
