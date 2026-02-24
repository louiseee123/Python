from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon', '0005_pokemon_pokeapi_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainer',
            name='pokeball_count',
            field=models.IntegerField(default=10),
        ),
    ]
