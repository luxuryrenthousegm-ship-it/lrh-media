const { chromium } = require('playwright');
const fs = require('fs'); fs.mkdirSync('data', { recursive: true });
(async () => {
  const b = await chromium.launch(); const p = await b.newPage();
  const results = []; let last = null;
  p.on('response', async r => {
    const u = r.url();
    if (u.includes('/api/v1/properties/filter/')) { try { const j = await r.json(); last = j; if (j.results) results.push(...j.results); } catch (e) {} }
  });
  for (let pg = 1; pg <= 15; pg++) {
    last = null;
    await p.goto(`https://luxuryrenthouse.alterestate.com/propiedades?listing_type=2&currency=USD&page=${pg}`, { waitUntil: 'networkidle', timeout: 90000 });
    await p.waitForTimeout(4000);
    if (!last || !last.next) break;
  }
  const seen = new Set(); const uniq = results.filter(x => { const k = x.uid || x.id || x.cid || JSON.stringify(x).slice(0,80); if (seen.has(k)) return false; seen.add(k); return true; });
  fs.writeFileSync('data/alterestate_rentals.json', JSON.stringify(uniq, null, 1));
  console.log('rentals', uniq.length);
  await b.close();
})().catch(e => { console.error(e); process.exit(1); });
