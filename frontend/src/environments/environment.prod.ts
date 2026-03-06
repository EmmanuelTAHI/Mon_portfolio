// Production : sur Vercel on utilise /api (proxy vers le backend). Sur Render, utiliser "npm run build:render" pour injecter l'URL du backend.
export const environment = {
  production: true,
  apiBase: '/api',
};
