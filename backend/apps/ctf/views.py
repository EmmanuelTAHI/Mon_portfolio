from django.utils import timezone
from django.core.cache import cache
from django.http import JsonResponse, FileResponse, HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.conf import settings
import os
import hashlib
import re

from .models import ChallengeSession, LeaderboardEntry, FlagAttempt
from .serializers import (
    ChallengeSessionSerializer,
    StartChallengeSerializer,
    SubmitFlagSerializer,
    LoginSerializer,
    LeaderboardEntrySerializer
)

# Flag réel (jamais exposé au frontend)
REAL_FLAG = "FLAG{root@sh00ter_X_V0u5_n3_Tr0uv3r3z_p@5_pr0ch@1n3m3nt}"
REAL_FLAG_HASH = hashlib.sha256(REAL_FLAG.encode()).hexdigest()

# Credentials Ubiquiti
UBIQUITI_USERNAME = "ubnt"
UBIQUITI_PASSWORD = "ubnt"

# Rate limiting
MAX_ATTEMPTS_PER_SESSION = 10
MAX_ATTEMPTS_PER_IP_PER_HOUR = 20
RATE_LIMIT_WINDOW = 3600  # 1 heure


def get_client_ip(request):
    """Récupère l'IP du client"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def check_rate_limit(session_id: str, ip_address: str):
    """Vérifie le rate limiting"""
    # Limite par session
    session_key = f"ctf_session_attempts_{session_id}"
    session_attempts = cache.get(session_key, 0)
    if session_attempts >= MAX_ATTEMPTS_PER_SESSION:
        return False, "Too many attempts for this session. Please try again."
    
    # Limite par IP
    ip_key = f"ctf_ip_attempts_{ip_address}"
    ip_attempts = cache.get(ip_key, 0)
    if ip_attempts >= MAX_ATTEMPTS_PER_IP_PER_HOUR:
        return False, "Too many attempts from this IP address. Try again later."
    
    return True, ""


def increment_rate_limit(session_id: str, ip_address: str):
    """Incrémente les compteurs de rate limiting"""
    session_key = f"ctf_session_attempts_{session_id}"
    session_attempts = cache.get(session_key, 0) + 1
    cache.set(session_key, session_attempts, RATE_LIMIT_WINDOW)
    
    ip_key = f"ctf_ip_attempts_{ip_address}"
    ip_attempts = cache.get(ip_key, 0) + 1
    cache.set(ip_key, ip_attempts, RATE_LIMIT_WINDOW)


def validate_session(session_id: str):
    """Valide une session et retourne l'objet session ou None"""
    if not session_id:
        return None
    try:
        session = ChallengeSession.objects.get(
            session_id=session_id,
            is_active=True
        )
        # Vérifier que la session n'est pas expirée (optionnel: sessions de 24h max)
        # Pour l'instant, on garde les sessions actives indéfiniment
        return session
    except ChallengeSession.DoesNotExist:
        return None


@api_view(['POST'])
@permission_classes([AllowAny])
def abandon_session(request):
    """Marks the session as abandoned (is_active=False) so the user can start again from scratch."""
    session_id = request.data.get('session_id') or request.GET.get('session_id')
    if not session_id:
        return Response({'error': 'Session ID required'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        session = ChallengeSession.objects.get(session_id=session_id)
    except ChallengeSession.DoesNotExist:
        return Response({'error': 'Invalid or expired session'}, status=status.HTTP_404_NOT_FOUND)
    session.is_active = False
    session.save(update_fields=['is_active'])
    return Response({'success': True, 'message': 'Session abandoned. You can start a new challenge.'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def start_challenge(request):
    """Démarre une nouvelle session de challenge ou récupère une session existante"""
    serializer = StartChallengeSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    hacker_nickname = serializer.validated_data['hacker_nickname'].strip()
    ip_address = get_client_ip(request)
    
    # Vérifier s'il existe déjà une session active pour ce nickname
    existing_session = ChallengeSession.objects.filter(
        hacker_nickname=hacker_nickname,
        is_active=True,
        is_completed=False
    ).order_by('-started_at').first()
    
    if existing_session:
        # Retourner la session existante (reprise)
        return Response({
            'session_id': existing_session.session_id,
            'message': 'Existing session restored',
            'instructions': 'Emmanuel connected all the Ubiquiti cameras in his house to his website so he could access them remotely, but something is not working. Help him figure out the problem.',
            'resumed': True
        }, status=status.HTTP_200_OK)
    
    # Un pseudo ne peut être utilisé que pour une seule session active (après Stop, même pseudo peut recommencer)
    if ChallengeSession.objects.filter(hacker_nickname=hacker_nickname, is_active=True).exists():
        return Response({
            'error': 'This nickname has already been used for a challenge. Choose another one.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Créer une nouvelle session (current_step=1 pour permettre directement l'accès au login)
    session = ChallengeSession.objects.create(
        session_id=ChallengeSession.generate_session_id(),
        hacker_nickname=hacker_nickname,
        ip_address=ip_address,
        current_step=1  # Permettre directement l'accès au login
    )
    
    return Response({
        'session_id': session.session_id,
        'message': 'Challenge started',
        'instructions': 'Emmanuel connected all the Ubiquiti cameras in his house to his website so he could access them remotely, but something is not working. Help him figure out the problem.',
        'resumed': False
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def submit_first_flag(request):
    """Soumet le premier flag (métadonnées de l'image de profil)"""
    serializer = SubmitFlagSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    session_id = serializer.validated_data['session_id']
    submitted_flag = serializer.validated_data['flag']
    ip_address = get_client_ip(request)
    
    try:
        session = ChallengeSession.objects.get(session_id=session_id, is_active=True)
    except ChallengeSession.DoesNotExist:
        return Response({'error': 'Invalid session'}, status=status.HTTP_404_NOT_FOUND)
    
    # Vérifier le rate limiting
    can_proceed, error_msg = check_rate_limit(session_id, ip_address)
    if not can_proceed:
        return Response({'error': error_msg}, status=status.HTTP_429_TOO_MANY_REQUESTS)
    
    # Le premier flag attendu est dans les métadonnées: FLAG{root@uname_
    expected_first_flag = "FLAG{root@uname_"
    submitted_hash = FlagAttempt.hash_flag(submitted_flag)
    
    # Enregistrer la tentative
    FlagAttempt.objects.create(
        session=session,
        submitted_flag=submitted_hash,
        is_correct=False,
        ip_address=ip_address
    )
    
    increment_rate_limit(session_id, ip_address)
    session.failed_attempts += 1
    session.last_attempt_at = timezone.now()
    
    # Valider le flag
    if submitted_flag.strip() == expected_first_flag:
        session.current_step = 1
        session.failed_attempts = 0  # Reset pour l'étape suivante
        session.save()
        return Response({
            'success': True,
            'message': 'First flag validated! You can continue.',
            'next_step': 'login'
        }, status=status.HTTP_200_OK)
    else:
        session.save()
        return Response({
            'success': False,
            'message': 'Incorrect flag. Try again.'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def ubiquiti_login(request):
    """Authentification sur l'interface Ubiquiti simulée"""
    serializer = LoginSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    session_id = serializer.validated_data['session_id']
    username = serializer.validated_data['username']
    password = serializer.validated_data['password']
    ip_address = get_client_ip(request)
    
    try:
        session = ChallengeSession.objects.get(session_id=session_id, is_active=True)
    except ChallengeSession.DoesNotExist:
        return Response({'error': 'Invalid session'}, status=status.HTTP_404_NOT_FOUND)
    
    # Permettre l'accès au login même si current_step est 0 (l'utilisateur peut accéder directement)
    # Mais on met à jour l'étape si elle est à 0 pour permettre la progression
    if session.current_step < 1:
        # Si l'utilisateur accède directement au login, on considère qu'il a peut-être sauté l'étape
        # On met current_step à 1 pour permettre la progression
        session.current_step = 1
        session.save()
    
    # Valider les credentials
    if username == UBIQUITI_USERNAME and password == UBIQUITI_PASSWORD:
        session.current_step = 2
        session.save()
        return Response({
            'success': True,
            'message': 'Thanks, you helped me reconnect my cameras. You can download this image.',
            'image_url': '/api/ctf/download-image/'
        }, status=status.HTTP_200_OK)
    else:
        session.failed_attempts += 1
        session.save()
        return Response({
            'success': False,
            'message': 'Invalid credentials'
        }, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@permission_classes([AllowAny])
def download_image(request):
    """Télécharge l'image avec métadonnées (seulement si authentifié)"""
    session_id = request.GET.get('session_id')
    if not session_id:
        return Response({'error': 'Session ID required'}, status=status.HTTP_400_BAD_REQUEST)
    
    session = validate_session(session_id)
    if not session:
        return Response({'error': 'Invalid or expired session'}, status=status.HTTP_404_NOT_FOUND)
    
    if session.current_step < 2:
        return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
    
    # Chemin de l'image avec métadonnées (chercher d'abord Ma_maison.jpg, sinon camera_image.png)
    image_path = os.path.join(settings.MEDIA_ROOT, 'ctf', 'Ma_maison.jpg')
    if not os.path.exists(image_path):
        image_path = os.path.join(settings.MEDIA_ROOT, 'ctf', 'camera_image.png')
    if not os.path.exists(image_path):
        return Response({'error': 'Image not found'}, status=status.HTTP_404_NOT_FOUND)

    try:
        with open(image_path, 'rb') as f:
            data = f.read()
        # Détecter le type réel par magic bytes (PNG: 89 50 4E 47)
        if data[:4] == b'\x89PNG':
            content_type = 'image/png'
            filename = 'Ma_maison.png' if 'Ma_maison' in image_path else 'camera_image.png'
        else:
            content_type = 'image/jpeg'
            filename = 'Ma_maison.jpg'
        return HttpResponse(data, content_type=content_type)
    except Exception as e:
        return Response({'error': 'Error reading image'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
def submit_final_flag(request):
    """Soumet le flag final et complète le challenge"""
    serializer = SubmitFlagSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    session_id = serializer.validated_data['session_id']
    submitted_flag = serializer.validated_data['flag']
    ip_address = get_client_ip(request)
    
    session = validate_session(session_id)
    if not session:
        return Response({'error': 'Invalid or expired session'}, status=status.HTTP_404_NOT_FOUND)
    
    # Vérifier que l'utilisateur est à l'étape finale
    if session.current_step < 1:
        return Response({'error': 'Invalid step'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Vérifier le rate limiting
    can_proceed, error_msg = check_rate_limit(session_id, ip_address)
    if not can_proceed:
        return Response({'error': error_msg}, status=status.HTTP_429_TOO_MANY_REQUESTS)
    
    # Enregistrer la tentative
    submitted_hash = FlagAttempt.hash_flag(submitted_flag)
    is_correct = (submitted_flag.strip() == REAL_FLAG)
    
    FlagAttempt.objects.create(
        session=session,
        submitted_flag=submitted_hash,
        is_correct=is_correct,
        ip_address=ip_address
    )
    
    increment_rate_limit(session_id, ip_address)
    session.failed_attempts += 1
    session.last_attempt_at = timezone.now()
    
    # Valider le flag final
    if is_correct:
        # Compléter le challenge
        session.complete()
        session.current_step = 3
        session.failed_attempts = 0
        session.save()
        
        # Créer ou mettre à jour l'entrée du leaderboard
        leaderboard_entry, created = LeaderboardEntry.objects.get_or_create(
            session=session,
            defaults={
                'hacker_nickname': session.hacker_nickname,
                'completion_time_seconds': session.completion_time_seconds,
                'completed_at': session.completed_at
            }
        )
        if not created:
            leaderboard_entry.completion_time_seconds = session.completion_time_seconds
            leaderboard_entry.completed_at = session.completed_at
            leaderboard_entry.save()
        
        # Mettre à jour les rangs
        LeaderboardEntry.update_ranks()
        
        # Récupérer le rang de l'utilisateur
        user_rank = leaderboard_entry.rank
        
        return Response({
            'success': True,
            'message': 'Flag validated! Challenge completed.',
            'completion_time': session.completion_time_seconds,
            'rank': user_rank,
            'animations': [
                '> validating flag...',
                '> access granted...',
                '> well done hacker'
            ]
        }, status=status.HTTP_200_OK)
    else:
        session.save()
        return Response({
            'success': False,
            'message': 'Incorrect flag. Try again.'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_leaderboard(request):
    """Récupère le top 5 du leaderboard"""
    top_5 = LeaderboardEntry.objects.all().order_by('completion_time_seconds', 'completed_at')[:5]
    serializer = LeaderboardEntrySerializer(top_5, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_session_info(request):
    """Récupère les informations de la session (nom, temps écoulé)"""
    session_id = request.GET.get('session_id')
    if not session_id:
        return Response({'error': 'Session ID required'}, status=status.HTTP_400_BAD_REQUEST)
    
    session = validate_session(session_id)
    if not session:
        return Response({'error': 'Invalid or expired session'}, status=status.HTTP_404_NOT_FOUND)
    
    elapsed_time = session.get_elapsed_time()
    return Response({
        'hacker_nickname': session.hacker_nickname,
        'elapsed_time': int(elapsed_time),
        'is_completed': session.is_completed,
        'current_step': session.current_step
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def check_session(request):
    """Vérifie si une session existe et retourne ses informations"""
    session_id = request.GET.get('session_id')
    if not session_id:
        return Response({
            'exists': False,
            'error': 'Session ID required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    session = validate_session(session_id)
    if not session:
        return Response({
            'exists': False,
            'error': 'Invalid or expired session'
        }, status=status.HTTP_200_OK)
    
    elapsed_time = session.get_elapsed_time()
    return Response({
        'exists': True,
        'session_id': session.session_id,
        'hacker_nickname': session.hacker_nickname,
        'elapsed_time': int(elapsed_time),
        'is_completed': session.is_completed,
        'current_step': session.current_step,
        'started_at': session.started_at.isoformat()
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_user_ranking(request):
    """Récupère le rang et le temps d'un utilisateur spécifique"""
    session_id = request.GET.get('session_id')
    if not session_id:
        return Response({'error': 'Session ID required'}, status=status.HTTP_400_BAD_REQUEST)
    
    session = validate_session(session_id)
    if not session:
        return Response({'error': 'Invalid or expired session'}, status=status.HTTP_404_NOT_FOUND)
    
    if not session.is_completed:
        return Response({'error': 'Challenge not completed'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        leaderboard_entry = session.leaderboard_entry
        serializer = LeaderboardEntrySerializer(leaderboard_entry)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except LeaderboardEntry.DoesNotExist:
        return Response({'error': 'Leaderboard entry not found'}, status=status.HTTP_404_NOT_FOUND)
