from django.urls import path
from . import views

app_name = 'pokemon'

urlpatterns = [
    # Home & Auth
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Onboarding
    path('create-trainer/', views.create_trainer, name='create_trainer'),
    path('starter/', views.starter_selection, name='starter_selection'),
    
    # Main Views
    path('dashboard/', views.dashboard, name='dashboard'),
    path('pokedex/', views.pokedex, name='pokedex'),
    path('team/', views.my_team, name='my_team'),
    path('profile/', views.profile, name='profile'),
    path('achievements/', views.achievements, name='achievements'),
    
    # Team Actions
    path('team/add/<int:pokemon_id>/', views.add_to_team, name='add_to_team'),
    path('team/remove/<int:member_id>/', views.remove_from_team, name='remove_from_team'),
    path('team/rename/<int:member_id>/', views.rename_member, name='rename_member'),
    
    # Tasks
    path('task/claim/<int:task_id>/', views.claim_task_xp, name='claim_task_xp'),
    
    # Egg Gacha
    path('hatch-egg/', views.hatch_egg, name='hatch_egg'),
    path('hatch-5-eggs/', views.hatch_5_eggs, name='hatch_5_eggs'),

    
    # Pokemon Detail
    path('pokemon/<int:pokemon_id>/', views.pokemon_detail, name='pokemon_detail'),
    
    # Safari Zone
    path('safari/', views.safari_zone, name='safari_zone'),
    path('safari/catch/<int:pokemon_id>/', views.catch_pokemon, name='catch_pokemon'),
    
    # Admin Panel (Lounelle only) - using /admin-panel/ to avoid conflict with Django admin
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('admin-panel/give-eggs/', views.admin_give_eggs, name='admin_give_eggs'),

    path('admin-panel/give-pokeballs/', views.admin_give_pokeballs, name='admin_give_pokeballs'),
    path('admin-panel/toggle-shiny/', views.admin_toggle_shiny, name='admin_toggle_shiny'),

    
    # Shop
    path('shop/', views.shop, name='shop'),
    path('shop/buy-eggs/', views.buy_eggs, name='buy_eggs'),
    
    # Inventory
    path('inventory/', views.inventory, name='inventory'),
]
