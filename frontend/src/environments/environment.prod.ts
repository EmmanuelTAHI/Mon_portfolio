// Production : sur Vercel on utilise /api (proxy vers le backend). L'API doit renvoyer des URLs absolues pour les images.
export const environment = {
  production: true,
  apiBase: '/api',
  /** En prod l'API renvoie des URLs absolues (BACKEND_PUBLIC_URL sur Render). Pas de préfixe. */
  backendMediaBase: '',
  /** EmailJS : formulaire de contact (envoi depuis le navigateur). */
  emailJsPublicKey: 'vREBuWY3ZCsTyIFKc',
  emailJsServiceId: 'service_dvdfxfg',
  emailJsTemplateId: 'template_8gnwokd',
};
