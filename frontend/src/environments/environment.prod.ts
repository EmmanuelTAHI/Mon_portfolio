// En production : sur Render, définir API_BASE_URL (URL du backend) avant le build.
// Ce fichier est remplacé par scripts/replace-api-url.js lors de "npm run build:render".
export const environment = {
  production: true,
  apiBase: 'https://YOUR_BACKEND.onrender.com',
};
