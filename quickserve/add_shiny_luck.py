import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quickserve.settings')
django.setup()

from pokemon.models import Trainer
from django.contrib.auth.models import User

# First, let's check if the trainer has shiny_luck attribute
user = User.objects.get(username='Lounelle')
trainer = user.trainer

print(f"Trainer: {trainer}")
print(f"Has shiny_luck attr: {hasattr(trainer, 'shiny_luck')}")

# Check what fields the trainer has
print("\nTrainer fields:")
for field in Trainer._meta.get_fields():
    print(f"  - {field.name}")

# Try to get or set shiny_luck
try:
    print(f"\nCurrent shiny_luck: {trainer.shiny_luck}")
except Exception as e:
    print(f"Error getting shiny_luck: {e}")

# Set it anyway
trainer.shiny_luck = 100
trainer.save()
print(f"Set shiny_luck to 100 and saved!")

# Verify
trainer.refresh_from_db()
print(f"After refresh - shiny_luck: {getattr(trainer, 'shiny_luck', 'NOT FOUND')}")
