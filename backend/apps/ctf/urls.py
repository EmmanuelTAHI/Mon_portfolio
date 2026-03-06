from django.urls import path
from . import views

urlpatterns = [
    path('start/', views.start_challenge, name='ctf_start'),
    path('abandon-session/', views.abandon_session, name='ctf_abandon_session'),
    path('check-session/', views.check_session, name='ctf_check_session'),
    path('session-info/', views.get_session_info, name='ctf_session_info'),
    path('submit-first-flag/', views.submit_first_flag, name='ctf_submit_first_flag'),
    path('ubiquiti-login/', views.ubiquiti_login, name='ctf_ubiquiti_login'),
    path('download-image/', views.download_image, name='ctf_download_image'),
    path('submit-final-flag/', views.submit_final_flag, name='ctf_submit_final_flag'),
    path('leaderboard/', views.get_leaderboard, name='ctf_leaderboard'),
    path('user-ranking/', views.get_user_ranking, name='ctf_user_ranking'),
]
