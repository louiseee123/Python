import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quickserve.settings')
django.setup()

from pokemon.models import Pokemon

# Fix Mawile (it has a leading space in the name)
try:
    p = Pokemon.objects.get(name=' Mawile')
    p.name = 'Mawile'
    p.pokeapi_id = 303
    p.save()
    print('Fixed Mawile!')
except Pokemon.DoesNotExist:
    print('Mawile not found with space')
    # Try without space
    p = Pokemon.objects.filter(name__icontains='Mawile').first()
    if p:
        p.pokeapi_id = 303
        p.save()
        print(f'Fixed {p.name} with pokeapi_id 303')
    else:
        print('Mawile not found at all')
