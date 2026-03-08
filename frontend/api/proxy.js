/**
 * Proxy serverless Vercel → backend Django sur Render.
 * Route: /api/(.*) → /api/proxy?path=$1
 * Variable d'environnement requise : API_BASE_URL (URL du backend Render).
 */
module.exports = async function handler(req, res) {
  const backend = process.env.API_BASE_URL;
  if (!backend) {
    res.status(500).json({
      error: 'Backend non configuré',
      message: 'Définir API_BASE_URL dans les variables d\'environnement Vercel.',
    });
    return;
  }

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

    response.headers.forEach(function (value, name) {
      var n = name.toLowerCase();
      if (n !== 'connection' && n !== 'keep-alive' && n !== 'transfer-encoding') {
        res.setHeader(name, value);
      }
    });

    if (contentType.includes('application/json')) {
      var text = await response.text();
      try {
        res.json(JSON.parse(text));
      } catch (e) {
        res.setHeader('Content-Type', contentType || 'application/json');
        res.send(text);
      }
      return;
    }

    var arrayBuffer = await response.arrayBuffer();
    var buffer = Buffer.from(arrayBuffer);

    res.setHeader('Content-Type', contentType || 'application/octet-stream');
    if (contentLength) {
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
};
