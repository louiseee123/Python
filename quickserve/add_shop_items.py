"""
Script to add Pokeball items with sprites from PokeAPI to the shop.
Run this script to populate the shop with various Pokeballs and other items.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quickserve.settings')
django.setup()

from pokemon.models import ShopItem

# Base URL for item sprites from PokeAPI
ITEM_SPRITE_BASE = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/items"

# Define the items to add
items = [
    # Pokeballs
    {
        'name': 'Pokeball',
        'description': 'A device used to capture wild Pokemon. It is designed as a sphere with a red top half and white bottom half.',
        'price': 100,
        'item_type': 'pokeball',
        'icon': '🔴',
        'image_url': f'{ITEM_SPRITE_BASE}/poke-ball.png',
    },
    {
        'name': 'Great Ball',
        'description': 'A device used to capture wild Pokemon. It has a higher success rate than a standard Pokeball.',
        'price': 300,
        'item_type': 'pokeball',
        'icon': '🔵',
        'image_url': f'{ITEM_SPRITE_BASE}/great-ball.png',
    },
    {
        'name': 'Ultra Ball',
        'description': 'A device used to capture wild Pokemon. It has an even higher success rate than a Great Ball.',
        'price': 800,
        'item_type': 'pokeball',
        'icon': '🟡',
        'image_url': f'{ITEM_SPRITE_BASE}/ultra-ball.png',
    },
    {
        'name': 'Master Ball',
        'description': 'The ultimate Pokeball. It will never fail to capture any Pokemon.',
        'price': 5000,
        'item_type': 'pokeball',
        'icon': '🟣',
        'image_url': f'{ITEM_SPRITE_BASE}/master-ball.png',
    },
    {
        'name': 'Premier Ball',
        'description': 'A special Pokeball awarded for completing certain tasks.',
        'price': 200,
        'item_type': 'pokeball',
        'icon': '⚪',
        'image_url': f'{ITEM_SPRITE_BASE}/premier-ball.png',
    },
    {
        'name': 'Dive Ball',
        'description': 'A specialized Pokeball optimized for catching water-dwelling Pokemon.',
        'price': 500,
        'item_type': 'pokeball',
        'icon': '🌊',
        'image_url': f'{ITEM_SPRITE_BASE}/dive-ball.png',
    },
    {
        'name': 'Nest Ball',
        'description': 'A Pokeball designed for catching lower-level Pokemon.',
        'price': 250,
        'item_type': 'pokeball',
        'icon': '🪺',
        'image_url': f'{ITEM_SPRITE_BASE}/nest-ball.png',
    },
    {
        'name': 'Net Ball',
        'description': 'A Pokeball that is more effective at catching Water and Bug-type Pokemon.',
        'price': 400,
        'item_type': 'pokeball',
        'icon': '🕸️',
        'image_url': f'{ITEM_SPRITE_BASE}/net-ball.png',
    },
    {
        'name': 'Repeat Ball',
        'description': 'A Pokeball that is more effective at catching Pokemon you have already captured.',
        'price': 600,
        'item_type': 'pokeball',
        'icon': '🔄',
        'image_url': f'{ITEM_SPRITE_BASE}/repeat-ball.png',
    },
    {
        'name': 'Timer Ball',
        'description': 'A Pokeball that becomes more effective the more turns have passed in battle.',
        'price': 700,
        'item_type': 'pokeball',
        'icon': '⏱️',
        'image_url': f'{ITEM_SPRITE_BASE}/timer-ball.png',
    },
    {
        'name': 'Quick Ball',
        'description': 'A Pokeball that is more effective at the start of a battle.',
        'price': 400,
        'item_type': 'pokeball',
        'icon': '⚡',
        'image_url': f'{ITEM_SPRITE_BASE}/quick-ball.png',
    },
    {
        'name': 'Dusk Ball',
        'description': 'A Pokeball that is more effective at night or in caves.',
        'price': 500,
        'item_type': 'pokeball',
        'icon': '🌙',
        'image_url': f'{ITEM_SPRITE_BASE}/dusk-ball.png',
    },
    {
        'name': 'Luxury Ball',
        'description': 'A comfortable Pokeball that makes captured Pokemon grow faster.',
        'price': 1000,
        'item_type': 'pokeball',
        'icon': '💎',
        'image_url': f'{ITEM_SPRITE_BASE}/luxury-ball.png',
    },
    {
        'name': 'Heal Ball',
        'description': 'A remedial Pokeball that restores captured Pokemon to full health.',
        'price': 300,
        'item_type': 'pokeball',
        'icon': '💚',
        'image_url': f'{ITEM_SPRITE_BASE}/heal-ball.png',
    },
    {
        'name': 'Cherish Ball',
        'description': 'A rare Pokeball used to commemorate special events.',
        'price': 2000,
        'item_type': 'pokeball',
        'icon': '💖',
        'image_url': f'{ITEM_SPRITE_BASE}/cherish-ball.png',
    },
    # Potions
    {
        'name': 'Potion',
        'description': 'A spray-type medicine that restores 20 HP.',
        'price': 50,
        'item_type': 'boost',
        'icon': '🧪',
        'image_url': f'{ITEM_SPRITE_BASE}/potion.png',
    },
    {
        'name': 'Super Potion',
        'description': 'A spray-type medicine that restores 50 HP.',
        'price': 150,
        'item_type': 'boost',
        'icon': '⚗️',
        'image_url': f'{ITEM_SPRITE_BASE}/super-potion.png',
    },
    {
        'name': 'Hyper Potion',
        'description': 'A spray-type medicine that restores 120 HP.',
        'price': 400,
        'item_type': 'boost',
        'icon': '🔮',
        'image_url': f'{ITEM_SPRITE_BASE}/hyper-potion.png',
    },
    {
        'name': 'Max Potion',
        'description': 'A spray-type medicine that fully restores HP.',
        'price': 800,
        'item_type': 'boost',
        'icon': '💠',
        'image_url': f'{ITEM_SPRITE_BASE}/max-potion.png',
    },
    # Status Heals
    {
        'name': 'Antidote',
        'description': 'A medicine that cures poison.',
        'price': 50,
        'item_type': 'boost',
        'icon': '💊',
        'image_url': f'{ITEM_SPRITE_BASE}/antidote.png',
    },
    {
        'name': 'Paralyze Heal',
        'description': 'A medicine that cures paralysis.',
        'price': 50,
        'item_type': 'boost',
        'icon': '⚡',
        'image_url': f'{ITEM_SPRITE_BASE}/paralyze-heal.png',
    },
    {
        'name': 'Burn Heal',
        'description': 'A medicine that cures burns.',
        'price': 50,
        'item_type': 'boost',
        'icon': '🔥',
        'image_url': f'{ITEM_SPRITE_BASE}/burn-heal.png',
    },
    {
        'name': 'Ice Heal',
        'description': 'A medicine that cures freezing.',
        'price': 50,
        'item_type': 'boost',
        'icon': '❄️',
        'image_url': f'{ITEM_SPRITE_BASE}/ice-heal.png',
    },
    {
        'name': 'Awakening',
        'description': 'A medicine that cures sleep.',
        'price': 50,
        'item_type': 'boost',
        'icon': '😴',
        'image_url': f'{ITEM_SPRITE_BASE}/awakening.png',
    },
    {
        'name': 'Full Heal',
        'description': 'A medicine that cures all status conditions.',
        'price': 200,
        'item_type': 'boost',
        'icon': '✨',
        'image_url': f'{ITEM_SPRITE_BASE}/full-heal.png',
    },
    # Evolution Items
    {
        'name': 'Moon Stone',
        'description': 'A peculiar stone that makes certain species of Pokemon evolve.',
        'price': 500,
        'item_type': 'boost',
        'icon': '🌕',
        'image_url': f'{ITEM_SPRITE_BASE}/moon-stone.png',
    },
    {
        'name': 'Fire Stone',
        'description': 'A peculiar stone that makes certain species of Pokemon evolve.',
        'price': 500,
        'item_type': 'boost',
        'icon': '🔶',
        'image_url': f'{ITEM_SPRITE_BASE}/fire-stone.png',
    },
    {
        'name': 'Water Stone',
        'description': 'A peculiar stone that makes certain species of Pokemon evolve.',
        'price': 500,
        'item_type': 'boost',
        'icon': '💧',
        'image_url': f'{ITEM_SPRITE_BASE}/water-stone.png',
    },
    {
        'name': 'Thunder Stone',
        'description': 'A peculiar stone that makes certain species of Pokemon evolve.',
        'price': 500,
        'item_type': 'boost',
        'icon': '⚡',
        'image_url': f'{ITEM_SPRITE_BASE}/thunder-stone.png',
    },
    {
        'name': 'Leaf Stone',
        'description': 'A peculiar stone that makes certain species of Pokemon evolve.',
        'price': 500,
        'item_type': 'boost',
        'icon': '🍃',
        'image_url': f'{ITEM_SPRITE_BASE}/leaf-stone.png',
    },
    # Vitamins
    {
        'name': 'HP Up',
        'description': 'Increases the base HP stat of a Pokemon.',
        'price': 1000,
        'item_type': 'boost',
        'icon': '❤️',
        'image_url': f'{ITEM_SPRITE_BASE}/hp-up.png',
    },
    {
        'name': 'Protein',
        'description': 'Increases the base Attack stat of a Pokemon.',
        'price': 1000,
        'item_type': 'boost',
        'icon': '💪',
        'image_url': f'{ITEM_SPRITE_BASE}/protein.png',
    },
    {
        'name': 'Iron',
        'description': 'Increases the base Defense stat of a Pokemon.',
        'price': 1000,
        'item_type': 'boost',
        'icon': '🛡️',
        'image_url': f'{ITEM_SPRITE_BASE}/iron.png',
    },
    {
        'name': 'Calcium',
        'description': 'Increases the base Special Attack stat of a Pokemon.',
        'price': 1000,
        'item_type': 'boost',
        'icon': '🧠',
        'image_url': f'{ITEM_SPRITE_BASE}/calcium.png',
    },
    {
        'name': 'Zinc',
        'description': 'Increases the base Special Defense stat of a Pokemon.',
        'price': 1000,
        'item_type': 'boost',
        'icon': '🧩',
        'image_url': f'{ITEM_SPRITE_BASE}/zinc.png',
    },
    {
        'name': 'Carbos',
        'description': 'Increases the base Speed stat of a Pokemon.',
        'price': 1000,
        'item_type': 'boost',
        'icon': '👟',
        'image_url': f'{ITEM_SPRITE_BASE}/carbos.png',
    },
    # Eggs
    {
        'name': 'Egg',
        'description': 'An Egg that hatches into a random Pokemon when incubated.',
        'price': 500,
        'item_type': 'egg',
        'icon': '🥚',
        'image_url': f'{ITEM_SPRITE_BASE}/odd-egg.png',
    },
]


def add_items():
    """Add all items to the database."""
    added_count = 0
    updated_count = 0
    
    for item_data in items:
        # Check if item already exists
        existing_item = ShopItem.objects.filter(name=item_data['name']).first()
        
        if existing_item:
            # Update existing item
            for key, value in item_data.items():
                setattr(existing_item, key, value)
            existing_item.save()
            updated_count += 1
            print(f'Updated: {item_data["name"]}')
        else:
            # Create new item
            ShopItem.objects.create(**item_data)
            added_count += 1
            print(f'Added: {item_data["name"]}')
    
    # Remove items that are no longer in the list
    item_names = [item['name'] for item in items]
    removed_count = 0
    for item in ShopItem.objects.all():
        if item.name not in item_names:
            print(f'Removed: {item.name}')
            item.delete()
            removed_count += 1
    
    print(f'\n=== Summary ===')
    print(f'Items added: {added_count}')
    print(f'Items updated: {updated_count}')
    print(f'Items removed: {removed_count}')
    print(f'Total items: {ShopItem.objects.count()}')


if __name__ == '__main__':
    print('Adding shop items with PokeAPI sprites...')
    add_items()
    print('Done!')
