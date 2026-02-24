from django.db import models
from django.contrib.auth.models import User


class Trainer(models.Model):
    """Trainer profile linked to User with level, XP, and team management."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='trainer')
    level = models.IntegerField(default=1)
    experience = models.IntegerField(default=0)
    max_team_size = models.IntegerField(default=6)
    egg_count = models.IntegerField(default=0)
    pokeball_count = models.IntegerField(default=10)
    shiny_luck = models.IntegerField(default=1)
    hunt_coins = models.IntegerField(default=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} (Level {self.level})"

    @property
    def xp_for_next_level(self):
        return self.level * 100

    @property
    def xp_progress(self):
        if self.xp_for_next_level == 0:
            return 100
        return min(100, (self.experience / self.xp_for_next_level) * 100)

    def add_xp(self, amount):
        self.experience += amount
        while self.experience >= self.xp_for_next_level:
            self.experience -= self.xp_for_next_level
            self.level += 1
            if self.level % 5 == 0:
                self.max_team_size += 1
        self.save()


class Pokemon(models.Model):
    """Pokemon database with name, type, level requirement."""
    TYPES = [
        ('Fire', 'Fire'), ('Water', 'Water'), ('Grass', 'Grass'),
        ('Electric', 'Electric'), ('Psychic', 'Psychic'), ('Ghost', 'Ghost'),
        ('Dragon', 'Dragon'), ('Normal', 'Normal'),
    ]
    
    RARITIES = [
        ('Common', 'Common'), ('Uncommon', 'Uncommon'), ('Rare', 'Rare'),
        ('Epic', 'Epic'), ('Legendary', 'Legendary'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    pokeapi_id = models.IntegerField(default=0)
    type = models.CharField(max_length=20, choices=TYPES)
    rarity = models.CharField(max_length=20, choices=RARITIES, default='Common')
    level_requirement = models.IntegerField(default=1)
    image_url = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True)
    is_starter = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.type})"

    @property
    def sprite_url(self):
        api_id = self.pokeapi_id if self.pokeapi_id > 0 else self.id
        return f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{api_id}.png"
    
    @property
    def shiny_sprite_url(self):
        api_id = self.pokeapi_id if self.pokeapi_id > 0 else self.id
        return f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/shiny/{api_id}.png"
    
    @property
    def showdown_url(self):
        api_id = self.pokeapi_id if self.pokeapi_id > 0 else self.id
        return f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/showdown/{api_id}.gif"
    
    @property
    def showdown_shiny_url(self):
        api_id = self.pokeapi_id if self.pokeapi_id > 0 else self.id
        return f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/showdown/shiny/{api_id}.gif"
    
    @property
    def get_type_color(self):
        type_colors = {'Fire': '#ff6b35', 'Water': '#4fc3f7', 'Grass': '#4caf50', 'Electric': '#ffd700', 'Psychic': '#9c27b0', 'Ghost': '#5c6bc0', 'Dragon': '#3f51b5', 'Normal': '#9e9e9e', 'Fighting': '#d32f2f', 'Flying': '#7986cb', 'Poison': '#8e24aa', 'Ground': '#8d6e63', 'Rock': '#795548', 'Bug': '#8bc34a', 'Steel': '#78909c', 'Fairy': '#f48fb1', 'Ice': '#b3e5fc', 'Dark': '#37474f'}
        return type_colors.get(self.type, '#9b59b6')
    
    @property
    def get_type_color_light(self):
        type_colors = {'Fire': '#ff8a5c', 'Water': '#81d4fa', 'Grass': '#81c784', 'Electric': '#ffe57f', 'Psychic': '#ba68c8', 'Ghost': '#7986cb', 'Dragon': '#7986cb', 'Normal': '#bdbdbd', 'Fighting': '#ef5350', 'Flying': '#9fa8da', 'Poison': '#ab47bc', 'Ground': '#a1887f', 'Rock': '#8d6e63', 'Bug': '#aed581', 'Steel': '#90a4ae', 'Fairy': '#f48fb1', 'Ice': '#e1f5fe', 'Dark': '#546e7a'}
        return type_colors.get(self.type, '#ba68c8')
    
    @property
    def get_type_color_dark(self):
        type_colors = {'Fire': '#e55a2b', 'Water': '#29b6f6', 'Grass': '#43a047', 'Electric': '#ffc107', 'Psychic': '#7b1fa2', 'Ghost': '#3f51b5', 'Dragon': '#303f9f', 'Normal': '#757575', 'Fighting': '#c62828', 'Flying': '#5c6bc0', 'Poison': '#6a1b9a', 'Ground': '#6d4c41', 'Rock': '#5d4037', 'Bug': '#689f38', 'Steel': '#607d8b', 'Fairy': '#ec407a', 'Ice': '#81d4fa', 'Dark': '#263238'}
        return type_colors.get(self.type, '#7b449b')
    
    @property
    def get_type_color_glow(self):
        type_colors = {'Fire': 'rgba(255, 107, 53, 0.4)', 'Water': 'rgba(79, 195, 247, 0.4)', 'Grass': 'rgba(76, 175, 80, 0.4)', 'Electric': 'rgba(255, 215, 0, 0.5)', 'Psychic': 'rgba(156, 39, 176, 0.4)', 'Ghost': 'rgba(92, 107, 192, 0.4)', 'Dragon': 'rgba(63, 81, 181, 0.4)', 'Normal': 'rgba(158, 158, 158, 0.3)', 'Fighting': 'rgba(211, 47, 47, 0.4)', 'Flying': 'rgba(121, 134, 203, 0.4)', 'Poison': 'rgba(142, 36, 170, 0.4)', 'Ground': 'rgba(141, 110, 99, 0.4)', 'Rock': 'rgba(121, 85, 72, 0.4)', 'Bug': 'rgba(139, 195, 74, 0.4)', 'Steel': 'rgba(120, 144, 156, 0.3)', 'Fairy': 'rgba(244, 143, 177, 0.4)', 'Ice': 'rgba(179, 229, 252, 0.5)', 'Dark': 'rgba(55, 71, 79, 0.4)'}
        return type_colors.get(self.type, 'rgba(155, 89, 182, 0.4)')
    
    @property
    def get_elemental_particles(self):
        particles = {'Fire': '<div class="particle" style="width:8px;height:8px;background:#ff6b35;top:20%;left:20%;"></div><div class="particle" style="width:6px;height:6px;background:#ff8c42;top:40%;left:70%;animation-delay:0.5s;"></div><div class="particle" style="width:10px;height:10px;background:#ffa726;top:60%;left:30%;animation-delay:1s;"></div>', 'Water': '<div class="particle" style="width:10px;height:10px;background:#4fc3f7;top:15%;left:25%;"></div><div class="particle" style="width:8px;height:8px;background:#29b6f6;top:50%;left:60%;animation-delay:0.7s;"></div><div class="particle" style="width:6px;height:6px;background:#81d4fa;top:70%;left:35%;animation-delay:1.2s;"></div>', 'Grass': '<div class="particle" style="width:8px;height:8px;background:#4caf50;top:20%;left:30%;"></div><div class="particle" style="width:6px;height:6px;background:#81c784;top:45%;left:65%;animation-delay:0.6s;"></div><div class="particle" style="width:10px;height:10px;background:#66bb6a;top:65%;left:25%;animation-delay:1.1s;"></div>', 'Electric': '<div class="particle" style="width:8px;height:8px;background:#ffd700;top:25%;left:20%;box-shadow:0 0 10px #ffd700;"></div><div class="particle" style="width:6px;height:6px;background:#ffe57f;top:50%;left:70%;animation-delay:0.4s;box-shadow:0 0 10px #ffd700;"></div><div class="particle" style="width:10px;height:10px;background:#ffc107;top:70%;left:40%;animation-delay:0.8s;box-shadow:0 0 10px #ffd700;"></div>', 'Psychic': '<div class="particle" style="width:8px;height:8px;background:#9c27b0;top:20%;left:25%;box-shadow:0 0 15px #9c27b0;"></div><div class="particle" style="width:10px;height:10px;background:#ba68c8;top:45%;left:65%;animation-delay:0.6s;box-shadow:0 0 15px #9c27b0;"></div><div class="particle" style="width:6px;height:6px;background:#ce93d8;top:70%;left:30%;animation-delay:1.2s;box-shadow:0 0 15px #9c27b0;"></div>', 'Ice': '<div class="particle" style="width:8px;height:8px;background:#b3e5fc;top:20%;left:30%;box-shadow:0 0 10px #81d4fa;"></div><div class="particle" style="width:10px;height:10px;background:#e1f5fe;top:50%;left:60%;animation-delay:0.5s;box-shadow:0 0 10px #81d4fa;"></div><div class="particle" style="width:6px;height:6px;background:#81d4fa;top:65%;left:25%;animation-delay:1s;box-shadow:0 0 10px #81d4fa;"></div>', 'Dark': '<div class="particle" style="width:10px;height:10px;background:#37474f;top:25%;left:20%;opacity:0.3;"></div><div class="particle" style="width:8px;height:8px;background:#546e7a;top:50%;left:70%;animation-delay:0.6s;opacity:0.3;"></div><div class="particle" style="width:6px;height:6px;background:#263238;top:70%;left:35%;animation-delay:1.1s;opacity:0.3;"></div>'}
        return particles.get(self.type, '<div class="particle" style="width:8px;height:8px;background:#9b59b6;top:25%;left:25%;"></div><div class="particle" style="width:6px;height:6px;background:#ba68c8;top:50%;left:65%;animation-delay:0.5s;"></div><div class="particle" style="width:10px;height:10px;background:#8e44ad;top:65%;left:30%;animation-delay:1s;"></div>')


class Team(models.Model):
    """Team belonging to a trainer."""
    trainer = models.OneToOneField(Trainer, on_delete=models.CASCADE, related_name='team')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.trainer.user.username}'s Team"

    @property
    def current_size(self):
        return self.members.count()

    @property
    def is_full(self):
        return self.current_size >= self.trainer.max_team_size


class TeamMember(models.Model):
    """Pokemon in a team with optional nickname."""
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='members')
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=50, blank=True, null=True)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('team', 'pokemon')

    def __str__(self):
        return self.nickname if self.nickname else self.pokemon.name


class PokemonUnlock(models.Model):
    """Tracks which Pokemon a trainer has unlocked."""
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name='unlocks')
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    shiny = models.BooleanField(default=False)
    unlocked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('trainer', 'pokemon')

    def __str__(self):
        shiny_mark = "⭐" if self.shiny else ""
        return f"{self.trainer.user.username} unlocked {self.pokemon.name} {shiny_mark}"


class DailyTask(models.Model):
    """Daily tasks that trainers can complete."""
    name = models.CharField(max_length=100)
    description = models.TextField()
    xp_reward = models.IntegerField(default=10)
    egg_reward = models.IntegerField(default=0)
    task_type = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        rewards = []
        if self.xp_reward > 0:
            rewards.append(f"+{self.xp_reward} XP")
        if self.egg_reward > 0:
            rewards.append(f"+{self.egg_reward} Egg")
        return f"{self.name} ({', '.join(rewards)})"


class TrainerTaskCompletion(models.Model):
    """Tracks daily task completions for trainers."""
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name='task_completions')
    task = models.ForeignKey(DailyTask, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)
    date = models.DateField()

    class Meta:
        unique_together = ('trainer', 'task', 'date')

    def __str__(self):
        return f"{self.trainer.user.username} completed {self.task.name}"


class ShopItem(models.Model):
    """Items available for purchase in the shop using Hunt Coins."""
    ITEM_TYPES = [
        ('egg', 'Egg'),
        ('pokeball', 'Pokeball'),
        ('boost', 'Boost'),
        ('cosmetic', 'Cosmetic'),
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField(default=0)
    item_type = models.CharField(max_length=20, choices=ITEM_TYPES)
    icon = models.CharField(max_length=50, default='🎁')
    image_url = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} ({self.price} Hunt Coins)"


class InventoryItem(models.Model):
    """Items owned by a trainer."""
    ITEM_CATEGORIES = [
        ('egg', 'Eggs'),
        ('pokeball', 'Pokeballs'),
        ('berry', 'Berries'),
        ('potion', 'Potions'),
        ('status_heal', 'Status Heals'),
        ('evolution', 'Evolution Items'),
        ('vitamin', 'Vitamins'),
        ('exp', 'EXP Candies'),
        ('cosmetic', 'Cosmetics'),
    ]
    
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name='inventory')
    shop_item = models.ForeignKey(ShopItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    category = models.CharField(max_length=20, choices=ITEM_CATEGORIES, default='pokeball')
    
    class Meta:
        unique_together = ('trainer', 'shop_item')
    
    def __str__(self):
        return f"{self.trainer.user.username} - {self.shop_item.name} (x{self.quantity})"
    
    @property
    def image_url(self):
        return self.shop_item.image_url
    
    @property
    def name(self):
        return self.shop_item.name
    
    @property
    def description(self):
        return self.shop_item.description
