// Lee cada ficha de alquiler (data/alterestate_rentals.json) y guarda texto visible + JSON de la API de detalle + galería original.
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const rentals = JSON.parse(fs.readFileSync('data/alterestate_rentals.json'));
  const b = await chromium.launch(); const p = await b.newPage(); const out = [];
  for (const r of rentals) {
    const api = [];
    const h = async res => { const u = res.url(); if (u.includes('/api/') && (u.includes(r.slug) || u.includes(r.uid))) { try { api.push({ url: u, json: await res.json() }); } catch (e) {} } };
    p.on('response', h);
    const url = `https://luxuryrenthouse.alterestate.com/propiedad/${r.slug}`;
    try {
      await p.goto(url, { waitUntil: 'networkidle', timeout: 90000 }); await p.waitForTimeout(4000);
      const text = await p.evaluate(() => document.body.innerText);
      const imgs = await p.evaluate(() => [...new Set([...document.querySelectorAll('img')].map(i => i.src).filter(s => s.includes('static/properties')))]);
      out.push({ cid: r.cid, slug: r.slug, url, text, imgs, api });
    } catch (e) { out.push({ cid: r.cid, slug: r.slug, url, error: String(e) }); }
    p.off('response', h);
  }
  fs.writeFileSync('data/alterestate_fichas.json', JSON.stringify(out, null, 1));
  console.log('fichas', out.length); await b.close();
})().catch(e => { console.error(e); process.exit(1); });
