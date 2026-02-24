# Add shiny field to PokemonUnlock model

with open('pokemon/models.py', 'r', encoding='utf-8') as f:
    content = f.read()

old = '''class PokemonUnlock(models.Model):
    """Tracks which Pokemon a trainer has unlocked."""
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name='unlocks')
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    unlocked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('trainer', 'pokemon')

    def __str__(self):
        return f"{self.trainer.user.username} unlocked {self.pokemon.name}"'''

new = '''class PokemonUnlock(models.Model):
    """Tracks which Pokemon a trainer has unlocked."""
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name='unlocks')
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    shiny = models.BooleanField(default=False)
    unlocked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('trainer', 'pokemon')

    def __str__(self):
        shiny_mark = "⭐" if self.shiny else ""
        return f"{self.trainer.user.username} unlocked {self.pokemon.name} {shiny_mark}"'''

content = content.replace(old, new)

with open('pokemon/models.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Model updated')
