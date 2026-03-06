from rest_framework import serializers
from .models import ChallengeSession, LeaderboardEntry


class ChallengeSessionSerializer(serializers.ModelSerializer):
    elapsed_time = serializers.SerializerMethodField()
    
    class Meta:
        model = ChallengeSession
        fields = ['session_id', 'hacker_nickname', 'started_at', 'elapsed_time', 
                  'is_completed', 'current_step', 'failed_attempts']
        read_only_fields = ['session_id', 'started_at', 'elapsed_time', 
                           'is_completed', 'current_step', 'failed_attempts']
    
    def get_elapsed_time(self, obj):
        return obj.get_elapsed_time()


class StartChallengeSerializer(serializers.Serializer):
    hacker_nickname = serializers.CharField(
        max_length=100,
        min_length=1,
        help_text="Nom d'utilisateur hacker"
    )
    
    def validate_hacker_nickname(self, value):
        """Sanitize et valide le nickname"""
        # Retirer les caractères dangereux
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Nickname cannot be empty")
        if len(value) > 100:
            raise serializers.ValidationError("Nickname is too long")
        return value


class SubmitFlagSerializer(serializers.Serializer):
    flag = serializers.CharField(max_length=500, help_text="Flag à valider")
    session_id = serializers.CharField(max_length=64, help_text="ID de session")
    
    def validate_flag(self, value):
        """Sanitize le flag"""
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Flag cannot be empty")
        if len(value) > 500:
            raise serializers.ValidationError("Flag is too long")
        return value


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)
    session_id = serializers.CharField(max_length=64)


class LeaderboardEntrySerializer(serializers.ModelSerializer):
    completion_time_formatted = serializers.SerializerMethodField()
    
    class Meta:
        model = LeaderboardEntry
        fields = ['hacker_nickname', 'completion_time_seconds', 
                  'completion_time_formatted', 'rank', 'completed_at']
    
    def get_completion_time_formatted(self, obj):
        """Formate le temps en format lisible"""
        seconds = obj.completion_time_seconds
        if seconds < 60:
            return f"{seconds:.2f}s"
        minutes = int(seconds // 60)
        secs = seconds % 60
        return f"{minutes}m {secs:.2f}s"
