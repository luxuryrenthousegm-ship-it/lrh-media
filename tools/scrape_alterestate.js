const { chromium } = require('playwright');
const fs = require('fs'); fs.mkdirSync('data', { recursive: true });
(async () => {
  const b = await chromium.launch(); const p = await b.newPage();
  const api = [];
  p.on('response', async r => {
    const u = r.url(); const ct = r.headers()['content-type'] || '';
    if (ct.includes('json')) { try { api.push({ u, j: await r.json() }); } catch (e) {} }
  });
  const out = { pages: [] };
  for (let pg = 1; pg <= 6; pg++) {
    const url = `https://luxuryrenthouse.alterestate.com/propiedades?listing_type=1&currency=USD&page=${pg}`;
    await p.goto(url, { waitUntil: 'networkidle', timeout: 90000 });
    await p.waitForTimeout(5000);
    const cards = await p.$$eval('a[href*="/propiedad"]', as => [...new Set(as.map(a => a.href))]);
    const text = await p.innerText('body');
    out.pages.push({ pg, url, cards, text });
    if (!cards.length) break;
  }
  fs.writeFileSync('data/alterestate_catalog.json', JSON.stringify(out, null, 1));
  fs.writeFileSync('data/alterestate_api.json', JSON.stringify(api, null, 1));
  // detail pages
  const links = [...new Set(out.pages.flatMap(x => x.cards))].slice(0, 80);
  const det = [];
  for (const l of links) {
    try { await p.goto(l, { waitUntil: 'networkidle', timeout: 60000 }); await p.waitForTimeout(1500);
      det.push({ url: l, text: (await p.innerText('body')).slice(0, 6000) }); } catch (e) { det.push({ url: l, err: e.message }); }
  }
  fs.writeFileSync('data/alterestate_details.json', JSON.stringify(det, null, 1));
  await b.close();
})().catch(e => { console.error(e); process.exit(1); });
