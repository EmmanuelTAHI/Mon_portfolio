/**
 * Remplace l'URL de l'API dans environment.prod.ts par la variable d'environnement API_BASE_URL.
 * Utilisé sur Vercel : définir API_BASE_URL = https://ton-backend.onrender.com
 */
const fs = require('fs');
const path = require('path');

const envPath = path.join(__dirname, '../src/environments/environment.prod.ts');
let content = fs.readFileSync(envPath, 'utf8');

const apiBaseUrl = process.env.API_BASE_URL || 'https://YOUR_RENDER_SERVICE.onrender.com';
const urlEscaped = apiBaseUrl.replace(/'/g, "\\'");
content = content.replace(
  /apiBase:\s*'[^']*'/,
  `apiBase: '${urlEscaped}'`
);
fs.writeFileSync(envPath, content);
console.log('API_BASE_URL injecté:', apiBaseUrl);
