# Add sprite_url property to Pokemon model

# Read the models.py file
with open('quickserve/pokemon/models.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the Pokemon class and add a property after the __str__ method
old_str = '''    def __str__(self):
        return f"{self.name} ({self.type})"


class Team(models.Model):'''

new_str = '''    def __str__(self):
        return f"{self.name} ({self.type})"

    @property
    def sprite_url(self):
        """Get the official artwork sprite URL from PokeAPI"""
        # Convert name to lowercase and replace spaces with hyphens
        name_slug = self.name.lower().replace(' ', '-')
        # Use the official artwork
        return f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{self.id}.png"


class Team(models.Model):'''

content = content.replace(old_str, new_str)

with open('quickserve/pokemon/models.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Added sprite_url property to Pokemon model!')
print('Now updating templates to use sprites...')
