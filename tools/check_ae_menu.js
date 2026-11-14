const { chromium } = require('playwright');
const fs = require('fs'); fs.mkdirSync('data', { recursive: true });
(async () => {
  const b = await chromium.launch(); const p = await b.newPage();
  await p.goto('https://luxuryrenthouse.alterestate.com/?nocache=' + Date.now(), { waitUntil: 'networkidle', timeout: 90000 });
  await p.waitForTimeout(4000);
  const links = await p.$$eval('a', as => as.filter(a => /propiedad/i.test(a.href) || /Exclusiv/i.test(a.textContent)).map(a => ({ t: a.textContent.trim(), h: a.href })));
  const home = await p.innerText('body');
  const link = await p.$('a:has-text("Propiedades Exclusivas")');
  let after = '', url = '';
  if (link) { await link.click(); await p.waitForLoadState('networkidle'); await p.waitForTimeout(5000); url = p.url(); after = await p.innerText('body'); }
  const m = after.match(/(\d+)\s+Propiedades encontradas/i);
  fs.writeFileSync('data/ae_menu_check.json', JSON.stringify({ when: new Date().toISOString(), links, clickedUrl: url, found: m ? m[1] : null, homeHasCards: /US\$|USD\s?\d/.test(home), homeSnippet: home.slice(0, 2500), afterSnippet: after.slice(0, 2500) }, null, 1));
  await b.close();
})().catch(e => { console.error(e); process.exit(1); });
