/**
 * Route /api (santé de l’API).
 * Le proxy principal pour /api/* est dans proxy.js (configuré via vercel.json).
 */
export default function handler(req, res) {
  res.status(200).json({
    message: 'Backend fonctionne !',
    proxy: true,
    hint: 'Les routes réelles (projects, contact, etc.) passent par /api/projects/, /api/contact/, etc.',
  });
}
