from django.db import models
from django.utils import timezone
from django.core.validators import MinLengthValidator
import hashlib
import secrets


class ChallengeSession(models.Model):
    """Session de challenge CTF avec timer côté serveur"""
    session_id = models.CharField(max_length=64, unique=True, db_index=True)
    hacker_nickname = models.CharField(max_length=100, validators=[MinLengthValidator(1)])
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    completion_time_seconds = models.FloatField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    failed_attempts = models.IntegerField(default=0)
    last_attempt_at = models.DateTimeField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    # Étape actuelle du challenge
    current_step = models.IntegerField(default=0)  # 0=start, 1=first_flag, 2=login, 3=final_flag
    
    class Meta:
        ordering = ['-started_at']
        indexes = [
            models.Index(fields=['session_id']),
            models.Index(fields=['is_active', 'is_completed']),
        ]
    
    def __str__(self):
        return f"{self.hacker_nickname} - {self.session_id[:8]}"
    
    def get_elapsed_time(self):
        """Calcule le temps écoulé depuis le début (côté serveur uniquement)"""
        if not self.started_at:
            return 0.0
        if self.completed_at:
            return (self.completed_at - self.started_at).total_seconds()
        return (timezone.now() - self.started_at).total_seconds()
    
    def complete(self):
        """Marque la session comme complétée et calcule le temps"""
        if not self.is_completed:
            self.is_completed = True
            self.completed_at = timezone.now()
            self.completion_time_seconds = self.get_elapsed_time()
            self.save()
    
    @staticmethod
    def generate_session_id():
        """Génère un ID de session unique"""
        return secrets.token_urlsafe(32)


class LeaderboardEntry(models.Model):
    """Entrée du leaderboard pour les challenges complétés"""
    session = models.OneToOneField(ChallengeSession, on_delete=models.CASCADE, related_name='leaderboard_entry')
    hacker_nickname = models.CharField(max_length=100)
    completion_time_seconds = models.FloatField()
    completed_at = models.DateTimeField()
    rank = models.IntegerField(null=True, blank=True)
    
    class Meta:
        ordering = ['completion_time_seconds', 'completed_at']
        indexes = [
            models.Index(fields=['completion_time_seconds']),
            models.Index(fields=['rank']),
        ]
    
    def __str__(self):
        return f"{self.hacker_nickname} - {self.completion_time_seconds:.2f}s"
    
    @staticmethod
    def update_ranks():
        """Met à jour les rangs de tous les participants"""
        entries = LeaderboardEntry.objects.all().order_by('completion_time_seconds', 'completed_at')
        for rank, entry in enumerate(entries, start=1):
            entry.rank = rank
            entry.save()


class FlagAttempt(models.Model):
    """Tentative de soumission de flag pour tracking et rate limiting"""
    session = models.ForeignKey(ChallengeSession, on_delete=models.CASCADE, related_name='flag_attempts')
    submitted_flag = models.CharField(max_length=500)  # Hash du flag soumis
    is_correct = models.BooleanField(default=False)
    attempted_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    class Meta:
        ordering = ['-attempted_at']
        indexes = [
            models.Index(fields=['session', 'attempted_at']),
            models.Index(fields=['ip_address', 'attempted_at']),
        ]
    
    @staticmethod
    def hash_flag(flag: str) -> str:
        """Hash le flag pour stockage sécurisé"""
        return hashlib.sha256(flag.encode()).hexdigest()
