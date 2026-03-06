from django.contrib import admin
from .models import ChallengeSession, LeaderboardEntry, FlagAttempt


@admin.register(ChallengeSession)
class ChallengeSessionAdmin(admin.ModelAdmin):
    list_display = ['hacker_nickname', 'session_id', 'started_at', 'is_completed', 
                    'completion_time_seconds', 'current_step', 'failed_attempts']
    list_filter = ['is_completed', 'is_active', 'current_step']
    search_fields = ['hacker_nickname', 'session_id']
    readonly_fields = ['session_id', 'started_at', 'completed_at', 'completion_time_seconds']


@admin.register(LeaderboardEntry)
class LeaderboardEntryAdmin(admin.ModelAdmin):
    list_display = ['rank', 'hacker_nickname', 'completion_time_seconds', 'completed_at']
    list_filter = ['completed_at']
    search_fields = ['hacker_nickname']
    ordering = ['rank']


@admin.register(FlagAttempt)
class FlagAttemptAdmin(admin.ModelAdmin):
    list_display = ['session', 'is_correct', 'attempted_at', 'ip_address']
    list_filter = ['is_correct', 'attempted_at']
    search_fields = ['session__hacker_nickname', 'session__session_id']
    readonly_fields = ['attempted_at']
