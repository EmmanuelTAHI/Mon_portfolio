// En prod sur Vercel, le front appelle /api (même origine) ; le proxy serverless renvoie vers Render.
export const environment = {
  production: true,
  apiBase: '/api',
};
