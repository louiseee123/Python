# Add pokeapi_id field to Pokemon model and create mapping

# Read the models.py file
with open('quickserve/pokemon/models.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add pokeapi_id field to Pokemon model
old_model = '''    name = models.CharField(max_length=100, unique=True)
    type = models.CharField(max_length=20, choices=TYPES)
    rarity = models.CharField(max_length=20, choices=RARITIES, default='Common')
    level_requirement = models.IntegerField(default=1)
    image_url = models.URLField(blank=True, null=True)'''

new_model = '''    name = models.CharField(max_length=100, unique=True)
    pokeapi_id = models.IntegerField(default=0)  # Actual PokeAPI ID for sprites
    type = models.CharField(max_length=20, choices=TYPES)
    rarity = models.CharField(max_length=20, choices=RARITIES, default='Common')
    level_requirement = models.IntegerField(default=1)
    image_url = models.URLField(blank=True, null=True)'''

content = content.replace(old_model, new_model)

# Update sprite_url to use pokeapi_id
old_sprite = '''    @property
    def sprite_url(self):
        """Get the official artwork sprite URL from PokeAPI"""
        # Convert name to lowercase and replace spaces with hyphens
        name_slug = self.name.lower().replace(' ', '-')
        # Use the official artwork
        return f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{self.id}.png"'''

new_sprite = '''    @property
    def sprite_url(self):
        """Get the official artwork sprite URL from PokeAPI"""
        # Use pokeapi_id if available, otherwise fallback to database id
        api_id = self.pokeapi_id if self.pokeapi_id > 0 else self.id
        return f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{api_id}.png"'''

content = content.replace(old_sprite, new_sprite)

with open('quickserve/pokemon/models.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Added pokeapi_id field to Pokemon model!')
