/**
 * Proxy serverless Vercel → backend Django sur Render.
 * Toutes les requêtes /api/* sont renvoyées vers API_BASE_URL (ton service Render).
 * Définir sur Vercel : API_BASE_URL = https://ton-backend.onrender.com
 */
export default async function handler(req, res) {
  const backend = process.env.API_BASE_URL;
  if (!backend) {
    res.status(500).json({
      error: 'Backend non configuré',
      message: 'Définir API_BASE_URL dans les variables d’environnement Vercel (URL du backend Render).',
    });
    return;
  }

  const pathAndQuery = (req.url || '/api').startsWith('/api') ? req.url : '/api' + (req.url || '');
  const targetUrl = backend.replace(/\/$/, '') + pathAndQuery;

  const headers = { ...req.headers };
  delete headers.host;
  delete headers.connection;

  const opts = {
    method: req.method,
    headers,
  };
  if (req.method !== 'GET' && req.method !== 'HEAD' && req.body !== undefined) {
    opts.body = typeof req.body === 'string' ? req.body : JSON.stringify(req.body || {});
  }

  try {
    const response = await fetch(targetUrl, opts);
    const contentType = response.headers.get('content-type') || '';
    const text = await response.text();

    res.status(response.status);
    if (contentType.includes('application/json')) {
      try {
        res.json(JSON.parse(text));
      } catch {
        res.setHeader('Content-Type', contentType).send(text);
      }
    } else {
      response.headers.forEach((v, k) => res.setHeader(k, v));
      res.send(text);
    }
  } catch (err) {
    console.error('Proxy error:', err);
    res.status(502).json({
      error: 'Erreur proxy',
      message: err.message || 'Impossible de joindre le backend.',
    });
  }
}
