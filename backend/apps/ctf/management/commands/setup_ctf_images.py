"""
Script pour créer les images avec métadonnées pour le challenge CTF.
Utilisez: python manage.py setup_ctf_images
"""
from django.core.management.base import BaseCommand
from django.conf import settings
from PIL import Image, PngImagePlugin
import os
import shutil


class Command(BaseCommand):
    help = 'Crée les images avec métadonnées pour le challenge CTF'

    def handle(self, *args, **options):
        # Créer le dossier media/ctf si nécessaire
        media_ctf_dir = os.path.join(settings.MEDIA_ROOT, 'ctf')
        os.makedirs(media_ctf_dir, exist_ok=True)
        
        # Chemin de l'image de profil source
        profile_image_source = os.path.join(
            settings.BASE_DIR.parent, 
            'frontend', 
            'src', 
            'assets', 
            'images', 
            'Mon_image.png'
        )
        
        profile_image_dest = os.path.join(
            settings.BASE_DIR.parent,
            'frontend',
            'src',
            'assets',
            'images',
            'Mon_image.png'
        )
        
        # Ajouter métadonnées à l'image de profil
        if os.path.exists(profile_image_source):
            self.stdout.write('Ajout des métadonnées à l\'image de profil...')
            try:
                img = Image.open(profile_image_source)
                
                # Créer les métadonnées avec le premier fragment de flag
                metadata = PngImagePlugin.PngInfo()
                metadata.add_text("Comment", "FLAG{root@uname_")
                metadata.add_text("Description", "Profile image with hidden metadata")
                metadata.add_text("Author", "Emmanuel TAHI")
                
                # Sauvegarder avec métadonnées
                img.save(profile_image_dest, "PNG", pnginfo=metadata)
                self.stdout.write(self.style.SUCCESS(f'[OK] Image de profil mise a jour: {profile_image_dest}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Erreur lors de la mise à jour de l\'image de profil: {e}'))
        else:
            self.stdout.write(self.style.WARNING(f'Image de profil non trouvée: {profile_image_source}'))
            # Créer une image de test
            self.create_test_profile_image(profile_image_dest)
        
        # Créer l'image de caméra avec le second fragment
        camera_image_path = os.path.join(media_ctf_dir, 'Ma_maison.png')
        self.stdout.write('Creation de l\'image de camera...')
        self.create_camera_image(camera_image_path)
        self.stdout.write(self.style.SUCCESS(f'[OK] Image de camera creee: {camera_image_path}'))
        
        self.stdout.write(self.style.SUCCESS('\n[OK] Toutes les images ont ete creees avec succes!'))
    
    def create_test_profile_image(self, path):
        """Crée une image de test si l'image de profil n'existe pas"""
        img = Image.new('RGB', (400, 400), color='#1a1a1a')
        metadata = PngImagePlugin.PngInfo()
        metadata.add_text("Comment", "FLAG{root@uname_")
        metadata.add_text("Description", "Profile image with hidden metadata")
        img.save(path, "PNG", pnginfo=metadata)
    
    def create_camera_image(self, path):
        """Crée l'image de caméra avec le second fragment de flag"""
        # Créer une image simulant une caméra Ubiquiti
        img = Image.new('RGB', (800, 600), color='#0a0a0a')
        
        # Ajouter du texte simple pour simuler une interface de caméra
        from PIL import ImageDraw, ImageFont
        draw = ImageDraw.Draw(img)
        
        # Dessiner un rectangle pour simuler l'interface
        draw.rectangle([50, 50, 750, 550], outline='#00ff9f', width=2)
        draw.text((100, 100), "Ubiquiti Camera Interface", fill='#00ff9f')
        draw.text((100, 150), "Status: Connected", fill='#00ff9f')
        
        # Ajouter les métadonnées avec le second fragment
        metadata = PngImagePlugin.PngInfo()
        metadata.add_text("Comment", "V0u5_n3_Tr0uv3r3z_p@5_pr0ch@1n3m3nt}")
        metadata.add_text("Description", "Ubiquiti camera image with metadata")
        metadata.add_text("Camera", "Ubiquiti UVC-G3")
        metadata.add_text("Location", "Home Security System")
        
        img.save(path, "PNG", pnginfo=metadata)
