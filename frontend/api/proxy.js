/**
 * Proxy serverless Vercel → backend Django sur Render.
 * Toutes les requêtes /api/* sont renvoyées vers API_BASE_URL (ton service Render).
 * Définir sur Vercel : API_BASE_URL = https://ton-backend.onrender.com
 *
 * Gère correctement les réponses binaires (images, etc.) : utilisation de arrayBuffer()
 * et en-têtes Content-Type / Content-Length explicites pour éviter corruption et perte d'en-têtes.
 *
 * Avec rewrite source "/api/:path*" → destination "/api/proxy", Vercel envoie le path en query (?path=...).
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

  // Path original : soit depuis la query (rewrite Vercel /api/:path* → /api/proxy?path=...), soit depuis req.url
  const pathFromQuery = req.query && typeof req.query.path === 'string' ? req.query.path : null;
  const pathOnly = pathFromQuery ? '/api/' + pathFromQuery : (req.url || '/api').split('?')[0] || '/api';
  const queryString = (req.url || '').includes('?') ? req.url.slice(req.url.indexOf('?')) : '';
  const queryParams = new URLSearchParams(queryString);
  if (pathFromQuery) queryParams.delete('path');
  const qs = queryParams.toString();
  const pathAndQuery = pathOnly + (qs ? '?' + qs : '');

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
    const contentType = (response.headers.get('content-type') || '').toLowerCase();
    const contentLength = response.headers.get('content-length');

    res.status(response.status);

    if (contentType.includes('application/json')) {
      const text = await response.text();
      try {
        res.json(JSON.parse(text));
      } catch {
        res.setHeader('Content-Type', contentType).send(text);
      }
      return;
    }

    // Réponse binaire (images, fichiers) : ne jamais utiliser .text() pour éviter corruption
    const arrayBuffer = await response.arrayBuffer();
    const buffer = Buffer.from(arrayBuffer);

    res.setHeader('Content-Type', contentType || 'application/octet-stream');
    if (contentLength !== undefined && contentLength !== null) {
      res.setHeader('Content-Length', contentLength);
    }
    res.send(buffer);
  } catch (err) {
    console.error('Proxy error:', err);
    res.status(502).json({
      error: 'Erreur proxy',
      message: err.message || 'Impossible de joindre le backend.',
    });
  }
}
