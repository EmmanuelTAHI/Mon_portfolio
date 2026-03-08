# Audit : affichage de Ma_maison.jpg

## Contexte

L’image **Ma_maison.jpg** est l’image du challenge CTF affichée après la connexion “Ubiquiti”. Elle n’est **pas** servie comme fichier statique : elle est envoyée par l’API backend (Django sur Render), puis passée par le proxy Vercel jusqu’au frontend Angular. L’affichage se fait via une balise `<img>` dont le `src` est l’URL de l’API.

---

## 1. Chemin du fichier et orthographe

| Élément | Emplacement | Valeur / orthographe |
|--------|-------------|----------------------|
| Fichier sur disque | `backend/media/ctf/Ma_maison.jpg` | **Ma_maison.jpg** (M et m minuscule après l’underscore) |
| Backend (views.py) | `image_path = os.path.join(media_root, 'ctf', 'Ma_maison.jpg')` | **Ma_maison.jpg** ✅ |
| Backend (setup_ctf_images.py) | `camera_image_path = ... 'Ma_maison.jpg'` | **Ma_maison.jpg** ✅ |
| Frontend (download lien) | `download="Ma_maison.jpg"` | **Ma_maison.jpg** ✅ |
| Fallback backend | `camera_image.png` si Ma_maison.jpg absent | Cohérent |

**Vérification locale :** le fichier existe bien dans `backend/media/ctf/Ma_maison.jpg` (≈ 285 Ko).

- **Conclusion :** pas d’erreur d’orthographe ni de chemin dans le code par rapport au nom du fichier.

---

## 2. Permissions et accès au fichier

| Couche | Rôle | Problème potentiel |
|--------|------|---------------------|
| Système de fichiers (local) | Lecture par Django | Fichier présent, pas de restriction détectée dans le code. |
| Render (production) | `MEDIA_ROOT` = `STATIC_ROOT / "media"` | Les médias sont copiés au build : `cp -r media/* static/media/` dans `render.yaml`. |
| Build Render | `buildCommand` inclut `mkdir -p static/media && cp -r media/* static/media/` | Si `backend/media/ctf/` est vide ou absent du déploiement, l’image ne sera pas sur le serveur. |

**À vérifier en production :**

- Que le repo contient bien `backend/media/ctf/Ma_maison.jpg` (ou qu’il est généré par une commande exécutée au build).
- Que `media/` n’est pas dans `.gitignore` (actuellement il ne l’est pas ✅).

**Solution si l’image manque sur Render :** s’assurer que `Ma_maison.jpg` est commité dans `backend/media/ctf/` ou que le build exécute une commande qui crée/copie ce fichier dans `static/media/ctf/`.

---

## 3. Format de l’image, casse, compatibilité navigateur

| Point | Détail |
|-------|--------|
| Extension | `.jpg` → contenu attendu JPEG. |
| Contenu réel | Le backend détecte le type par **magic bytes** (PNG : `\x89PNG`, sinon JPEG). Donc même si le fichier était en PNG avec l’extension .jpg, le `Content-Type` envoyé serait correct. ✅ |
| Casse du nom | Sous Windows, la casse peut être ignorée ; sous Linux (Render), **Ma_maison.jpg** doit correspondre exactement au nom du fichier. Le code utilise partout `Ma_maison.jpg` (majuscule M). ✅ |
| Compatibilité navigateur | JPEG et PNG sont supportés par tous les navigateurs modernes. Pas de souci. |

**Note :** La commande `setup_ctf_images` crée une image PNG mais l’enregistre sous le chemin `Ma_maison.jpg`. Si tu utilises ce script, le fichier est en fait du PNG avec une extension .jpg ; la détection par magic bytes dans la vue évite tout conflit de `Content-Type`.

---

## 4. Balises HTML / CSS et conflits de style

| Élément | Rôle |
|--------|------|
| Balise | `<img [src]="imageUrl" ...>` dans `image-viewer.component.html`. Pas de `background-image` pour cette image. |
| Classes sur l’image | `max-h-[500px] w-auto object-contain rounded-md` — pas de `display: none` ni `visibility: hidden`. |
| Conteneur | `min-h-[200px]`, `flex justify-center items-center` — l’image peut s’afficher au centre. |
| CSS du composant | Aucune règle qui masque ou réinitialise le `src` de l’image. |

**Conclusion :** pas de conflit HTML/CSS identifié qui empêcherait l’image d’apparaître. Si l’URL est correcte et renvoie une image valide, elle doit s’afficher.

---

## 5. Erreurs réseau / console (404, CORS, etc.)

Flux réel :

1. **Frontend (Vercel)** : `imageUrl` = `/api/ctf/download-image/?session_id=...&_t=...`
2. **Requête** : GET vers la même origine (Vercel) → pas de CORS côté front.
3. **Vercel** : rewrite `/api/:path*` → `/api/proxy?path=:path*` → la requête est traitée par la serverless `api/proxy.js`.
4. **Proxy** : appelle le backend Render (`API_BASE_URL`) avec le même chemin et query string.
5. **Backend** : vérifie `session_id`, étape du challenge, puis lit `MEDIA_ROOT/ctf/Ma_maison.jpg` et renvoie le binaire avec le bon `Content-Type`.

**Erreurs possibles et signification :**

| Code / erreur | Signification | Piste de résolution |
|---------------|---------------|----------------------|
| **404** | Session invalide/expirée, ou image non trouvée (fichier absent sur Render). | Vérifier les logs Render pour `[CTF download_image]` (path, exists). Vérifier que le fichier est bien présent dans `static/media/ctf/` après le build. |
| **403** | `current_step < 2` : l’utilisateur n’a pas encore “validé” l’étape qui débloque l’image. | Atteindre la bonne étape du challenge (connexion Ubiquiti) avant d’ouvrir la page image. |
| **400** | `session_id` manquant dans l’URL. | S’assurer que la redirection vers `/_my_challenge/image` inclut bien `?session_id=...`. |
| **502** | Le proxy ne peut pas joindre le backend (timeout, URL incorrecte). | Vérifier `API_BASE_URL` sur Vercel (doit être l’URL du service Render). Vérifier que le backend Render est actif. |
| **304 Not Modified** | Réponse mise en cache ; le navigateur ou un CDN renvoie une ancienne réponse. | Déjà atténué par `_t=` dans l’URL et par les en-têtes no-cache dans le proxy pour `download-image`. Tester en navigation privée ou avec cache désactivé. |
| **CORS** | Peu probable ici car la requête est same-origin (vers /api sur Vercel). | Si tu vois une erreur CORS, elle viendrait du backend appelé par le proxy ; vérifier CORS sur Render si tu appelles le backend directement depuis le navigateur. |

**À faire côté debug :** ouvrir les DevTools → onglet Network, recharger la page image, cliquer sur la requête `download-image` et noter le **status code**, les **headers** de la réponse et l’onglet **Response** (ou Preview) pour voir si le corps est une image ou du JSON d’erreur.

---

## 6. Cache et CDN

| Mécanisme | Rôle | État dans le projet |
|-----------|------|----------------------|
| **Cache navigateur** | Peut renvoyer une ancienne réponse (ex. 304) pour la même URL. | Contourné en ajoutant `_t=Date.now()` dans l’URL à chaque chargement (et au retry). ✅ |
| **Proxy Vercel** | Pour les requêtes contenant `download-image`, le code supprime `If-None-Match` et `If-Modified-Since` et envoie `Cache-Control: no-cache, no-store, must-revalidate`, `Pragma: no-cache`, `Expires: 0`. ✅ |
| **Backend Django** | La vue `download_image` renvoie un `HttpResponse` sans en-têtes de cache explicites. | Recommandation : ajouter les mêmes en-têtes anti-cache côté backend pour cohérence. |

**Solutions si le cache pose encore problème :**

- Tester en **navigation privée** ou avec l’option “Désactiver le cache” dans l’onglet Network.
- S’assurer que le **bouton “Réessayer”** sur la page image est bien utilisé (il régénère une URL avec un nouveau `_t`).

---

## 7. Synthèse des causes possibles et solutions

### A. Image absente sur Render

- **Symptôme :** 404 ou message “Image not found” dans les logs / réponse JSON.
- **Vérification :** logs Render contenant `[CTF download_image] Ma_maison.jpg path=... exists=False`.
- **Solution :** s’assurer que `backend/media/ctf/Ma_maison.jpg` est bien présent dans le dépôt (ou généré au build) et que le build fait bien `cp -r media/* static/media/`.

### B. Session invalide ou mauvaise étape

- **Symptôme :** 404 (session) ou 403 (étape).
- **Solution :** refaire le parcours du challenge jusqu’à la page “image” (après connexion Ubiquiti) avec un `session_id` valide ; vérifier que le lien vers `/_my_challenge/image` contient bien `?session_id=...`.

### C. Proxy ou backend injoignable

- **Symptôme :** 502 ou erreur réseau.
- **Solution :** vérifier `API_BASE_URL` sur Vercel (URL du backend Render), et que le backend est bien “up” sur Render.

### D. Réponse 200 mais image ne s’affiche pas

- **Symptôme :** status 200 sur `download-image` mais image cassée ou vide dans l’UI.
- **Vérifications :** dans Network, regarder le **Content-Type** (doit être `image/jpeg` ou `image/png`) et la **taille** du corps (non nulle). Si le corps est du JSON, le backend a renvoyé une erreur au lieu du binaire.
- **Solution :** vérifier les logs Render au moment de la requête ; s’assurer que la vue lit bien le fichier et renvoie `HttpResponse(data, content_type=...)` sans être interceptée par une erreur avant.

### E. Cache (304 ou ancienne version)

- **Symptôme :** 304 ou ancienne image affichée.
- **Solution :** déjà prévu avec `_t` et en-têtes no-cache dans le proxy. Tester en navigation privée ; si le problème persiste, vérifier que la requête contient bien `_t` et que les en-têtes de réponse du proxy sont bien envoyés (inspecter dans Network).

---

## 8. Checklist de diagnostic rapide

1. [ ] **Ouvrir** la page `/_my_challenge/image?session_id=XXX` (avec un session_id valide après connexion Ubiquiti).
2. [ ] **Ouvrir** DevTools → Network, recharger, trouver la requête `download-image`.
3. [ ] Noter le **status** (200 / 304 / 403 / 404 / 502).
4. [ ] Regarder le **Content-Type** et la **taille** du corps.
5. [ ] Si 200 + image/jpeg ou image/png + corps non vide → le problème est côté affichage (rare). Si JSON ou erreur → corriger backend/proxy/session/fichier selon le code et les logs.
6. [ ] Sur Render : consulter les logs au moment de la requête pour les messages `[CTF download_image]` (path, exists, content_type, size).

---

## 9. Recommandation de correction côté backend (optionnel)

Pour renforcer la cohérence avec le proxy et éviter tout cache intermédiaire, tu peux ajouter les en-têtes anti-cache dans la vue Django qui sert l’image :

```python
# Dans download_image(), avant return HttpResponse(...)
response = HttpResponse(data, content_type=content_type)
response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
response['Pragma'] = 'no-cache'
response['Expires'] = '0'
return response
```

Cela garantit que, même si le proxy change, la réponse du backend indique clairement qu’elle ne doit pas être mise en cache.

---

*Audit basé sur l’état du dépôt (frontend Angular, proxy Vercel, backend Django sur Render) et le flux d’affichage de Ma_maison.jpg.*
