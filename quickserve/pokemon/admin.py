from django.contrib import admin
from .models import Trainer, Pokemon, Team, TeamMember, PokemonUnlock, DailyTask, TrainerTaskCompletion


@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    list_display = ('user', 'level', 'experience', 'max_team_size', 'created_at')
    list_filter = ('level',)
    search_fields = ('user__username',)


@admin.register(Pokemon)
class PokemonAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'level_requirement', 'is_starter')
    list_filter = ('type', 'is_starter')
    search_fields = ('name',)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('trainer', 'current_size', 'created_at')
    list_filter = ('created_at',)


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('team', 'pokemon', 'nickname', 'added_at')
    search_fields = ('team__trainer__user__username', 'pokemon__name', 'nickname')


@admin.register(PokemonUnlock)
class PokemonUnlockAdmin(admin.ModelAdmin):
    list_display = ('trainer', 'pokemon', 'unlocked_at')
    list_filter = ('unlocked_at',)
    search_fields = ('trainer__user__username', 'pokemon__name')


@admin.register(DailyTask)
class DailyTaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'xp_reward', 'task_type', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)


@admin.register(TrainerTaskCompletion)
class TrainerTaskCompletionAdmin(admin.ModelAdmin):
    list_display = ('trainer', 'task', 'date', 'completed_at')
    list_filter = ('date',)
    search_fields = ('trainer__user__username', 'task__name')
