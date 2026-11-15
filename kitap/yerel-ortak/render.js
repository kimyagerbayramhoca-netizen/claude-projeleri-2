// Ünite render betiği: unite.html → PDF + onizleme/sNN.png (deviceScaleFactor 2) + taşma denetimi (+ varyantlar)
// Çalıştır (ünite klasöründen ya da herhangi bir yerden):
//   node yerel-ortak/render.js <ünite-klasörü>            → öğrenci PDF'i + bütün PNG'ler + taşma denetimi
//   node yerel-ortak/render.js <ünite-klasörü> 3 4        → yalnızca 3. ve 4. sayfanın PNG'si (PDF yine üretilir)
//   node yerel-ortak/render.js <ünite-klasörü> --pdfsiz 3 → yalnızca PNG (hızlı deneme)
//   node yerel-ortak/render.js <dosya.html> --pngsiz      → başka yere kurulmuş HTML'den yalnız PDF (dosya.pdf, aynı klasör)
//   Ünite klasörü verilmezse içinde bulunulan klasör kullanılır.
// Varyantlar (TASARIM-SISTEMI.md §12):
//   --hepsi      önce `python3 uretec/kur.py --hepsi`, sonra öğrenci + aşağıdaki dördü
//   --ogretmen   <klasör>-ogretmen.pdf          aynı unite.html, <html class="ogretmen">: data-dogru şıklar ve .ogr cevaplar kırmızı
//   --fotokopi   <klasör>-fotokopi.pdf          unite-fotokopi.html (kur.py --fotokopi), sayfa başına mürekkep raporu
//   --baski      <klasör>-baski.pdf             3,2 mm taşma payı, kesim izleri, TrimBox/BleedBox (pypdf; pdf_kutular.py)
//   --hazine     <klasör>-hazine-kartlari.pdf   hazine-kartlari.html (kur.py --hazine): meta.json H kartları, tek A4 kesme yaprağı
//   --onizleme   varyantların PNG'leri de: onizleme/varyant/<ad>/sNN.png
// Denetim iki tür sorunu listeler (yatayda bilerek taşan dekorlu kapsayıcılar data-tasma-yatay ile işaretlenir):
//   • alan dışı   : HUD+çini şeridi altı (12 mm) ile altbilgi üstü (283 mm) arasındaki alandan taşan öğe
//                   (sahne bantları, panorama gibi [data-serbest] öğeler hariç)
//   • kutu taşması: kart, balon, şık gibi kutulara sığmayan metin
// Öğretmen baskısında ayrıca kırmızı (.ogr) metnin kutusundan taşması denetlenir. Bütün PDF'lerde Type 3 font sayılır (pdffonts).
const path = require('path');
const fs = require('fs');
const { execFileSync } = require('child_process');
const { chromium } = require('playwright');

const ORTAK = __dirname;
const _arg = process.argv.slice(2);
// hedef: ünite klasörü ya da doğrudan bir .html dosyası (ör. YEREL_CIKTI ile başka yere kurulmuş ünite)
const _hedef = _arg.find(a => !a.startsWith('--') && fs.existsSync(a) && (fs.statSync(a).isDirectory() || a.endsWith('.html')));
const _dosya = _hedef && fs.statSync(_hedef).isFile();
const UNITE = _dosya ? path.dirname(path.resolve(_hedef)) : path.resolve(_hedef || process.cwd());
const HTML = _dosya ? path.resolve(_hedef) : path.join(UNITE, 'unite.html');
const _ad = path.basename(HTML, '.html');
const KOK = _ad === 'unite' ? path.basename(UNITE) : _ad;
const PDF = path.join(UNITE, KOK + '.pdf');
const ONIZ = path.join(UNITE, _ad === 'unite' ? 'onizleme' : 'onizleme-' + _ad);

const argv = _arg.filter(a => a !== _hedef);
const bayrak = b => argv.includes(b);
const HEPSI = bayrak('--hepsi');
const VAR = { ogretmen: HEPSI || bayrak('--ogretmen'), fotokopi: HEPSI || bayrak('--fotokopi'), baski: HEPSI || bayrak('--baski'), hazine: HEPSI || bayrak('--hazine') };
const yalnizVaryant = !HEPSI && Object.values(VAR).some(Boolean);
const pdfsiz = bayrak('--pdfsiz');
const pngsiz = bayrak('--pngsiz');
const varyantPng = bayrak('--onizleme');
const sec = argv.filter(a => !a.startsWith('--')).map(Number);
const MM = 96 / 25.4;

// ------------------------------------------------------------------ taşma denetimi (öğrenci sayfaları)
function tasmaDenetimi() {
  const mm = v => v * 96 / 25.4;
  const out = [];
  document.querySelectorAll('.sayfa').forEach((s, i) => {
    const sr = s.getBoundingClientRect();
    const ust = sr.top + mm(12), alt = sr.top + mm(283), sol = sr.left + mm(10), sag = sr.right - mm(10);
    s.querySelectorAll('*').forEach(el => {
      if (el.closest('.hud') || el.closest('.alt') || el.closest('svg') || el.closest('[data-serbest]') || el.closest('.ebru-alt')) return;
      const r = el.getBoundingClientRect();
      if (!r.width || !r.height) return;
      const ad = (el.className && el.className.baseVal === undefined ? el.className : el.tagName) || el.tagName;
      const metin = (el.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 42);
      if (r.bottom > alt + 1 || r.top < ust - 1 || r.left < sol - 1 || r.right > sag + 1)
        out.push(`s${i + 1}: alan dışı [${ad}] "${metin}" alt=${((r.bottom - sr.top) * 25.4 / 96).toFixed(1)}mm`);
      const cs = getComputedStyle(el);
      if (cs.overflow !== 'visible' || el.matches('.kart,.tuzak,.ozet-kart,.balon,.sik,.oy > div,.hazine,.levha,.durak-et,.basamak,.meclis,.kissa,.mesveret,.medeniyet,.esnek,.bento,.mesveret-izgara,.ozetler,.unvanlar,.sandik-izgara,.cozumler,.ustad-soru,.ustad-izgara,.ustad-muhur'))
        if (el.scrollHeight > el.clientHeight + 2 || (el.scrollWidth > el.clientWidth + 2 && !el.hasAttribute('data-tasma-yatay')))
          out.push(`s${i + 1}: kutu taşması [${ad}] "${metin}" (${el.scrollWidth}x${el.scrollHeight} > ${el.clientWidth}x${el.clientHeight})`);
    });
    // levha ve etiketler sayfa dışına taşmasın
    s.querySelectorAll('.levha,.durak-et').forEach(el => {
      const r = el.getBoundingClientRect();
      if (r.left < sr.left + mm(3) || r.right > sr.right - mm(3)) out.push(`s${i + 1}: kenara taşan etiket "${el.textContent.trim().slice(0, 30)}"`);
    });
  });
  return out;
}

// ------------------------------------------------------------------ öğretmen: kırmızı metin kutusundan taşmasın
function ogretmenDenetimi() {
  const out = [];
  document.querySelectorAll('.sayfa').forEach((s, i) => {
    s.querySelectorAll('.ogr').forEach(el => {
      const r = el.getBoundingClientRect();
      if (!r.width) return;
      const kap = el.closest('.karalama,.cevap-kutu,.cizgili,.cozum-alani,.bos-satir,.satirlar') || el.closest('.kart,.mesveret,.kissa,.ustad-soru,.meclis,.tuzak,.medeniyet') || s;
      const k = (kap.matches('.cizgili') ? kap.closest('.hukum') : kap.matches('.cozum-alani,.bos-satir,.satirlar,.cevap-kutu') ? (kap.closest('.kart') || kap) : kap).getBoundingClientRect();
      if (r.left < k.left - 1 || r.right > k.right + 1 || r.top < k.top - 1 || r.bottom > k.bottom + 1)
        out.push(`s${i + 1}: öğretmen metni taşıyor "${el.textContent.trim().slice(0, 40)}" (${Math.round(r.width)}x${Math.round(r.height)} kutu ${Math.round(k.width)}x${Math.round(k.height)})`);
    });
  });
  return out;
}

// ------------------------------------------------------------------ baskı: taşma payı, kesim izleri
// Kâğıt 9,21 × 12,64 inç (Chromium PDF sayfasını 1/100 inçe yuvarlar; tam bu değerler ölçeksiz basılır).
// Kesim (trim) kutusu 210×297 mm, sol üstten 45 px (11,906 mm) içeride → sayfa tam piksele oturur, kesim içi öğrenci
// baskısıyla aynı dizilir. Taşma (bleed) 12 px = 3,175 mm (≥ 3 mm). Kesim izleri taşmanın dışında. Ölçüler CSS px (96/inç).
const KAGIT = { w: 884.16, h: 1213.44, kenar: 45, tasma: 12, trimW: 210 * 96 / 25.4, trimH: 297 * 96 / 25.4 };
function baskiHazirla(K) {
  const ns = 'http://www.w3.org/2000/svg';
  document.documentElement.classList.add('baski');
  // 1) sahneler: viewBox kenarlarının dışına ayna kopya (kenara değen bantlar taşma payını gerçekten doldursun)
  let n = 0;
  document.querySelectorAll('.sayfa svg.sahne').forEach(svg => {
    const vb = svg.viewBox.baseVal;
    if (!vb || !vb.width) return;
    const r = svg.getBoundingClientRect();
    const olcek = Math.max(r.width / vb.width, r.height / vb.height);   // px / birim (slice)
    const pay = (K.tasma + 6) / olcek;
    const id = 'bsk' + (n++);
    const g = document.createElementNS(ns, 'g');
    g.setAttribute('id', id);
    [...svg.childNodes].forEach(c => { if (c.nodeName !== 'defs') g.appendChild(c); });
    svg.appendChild(g);
    let defs = svg.querySelector(':scope > defs');
    if (!defs) { defs = document.createElementNS(ns, 'defs'); svg.insertBefore(defs, svg.firstChild); }
    for (const [kenar, a] of [['s', vb.x], ['g', vb.x + vb.width]]) {
      const cp = document.createElementNS(ns, 'clipPath');
      cp.setAttribute('id', id + kenar);
      const rc = document.createElementNS(ns, 'rect');
      rc.setAttribute('x', kenar === 's' ? a - pay : a); rc.setAttribute('y', vb.y - vb.height);
      rc.setAttribute('width', pay); rc.setAttribute('height', vb.height * 3);
      cp.appendChild(rc); defs.appendChild(cp);
      const kap = document.createElementNS(ns, 'g');
      kap.setAttribute('clip-path', `url(#${id + kenar})`);
      const u = document.createElementNS(ns, 'use');
      u.setAttribute('href', '#' + id);
      u.setAttribute('transform', `matrix(-1 0 0 1 ${2 * a} 0)`);
      kap.appendChild(u); svg.appendChild(kap);
    }
  });
  // 2) çini şeridi: sola bir karo (sağda zaten 720/700 birim taşar)
  document.querySelectorAll('.sayfa > svg.cini-serit').forEach(svg => {
    const ilk = svg.querySelector(':scope > g');
    if (!ilk) return;
    const k = ilk.cloneNode(true);
    k.setAttribute('transform', 'translate(-24 0)');
    svg.insertBefore(k, ilk);
  });
  // 3) her sayfayı kâğıda koy: taşma kutusu + kesim izleri + künye satırı
  const sayfalar = [...document.querySelectorAll('.sayfa')];
  const baslik = document.title || '';
  sayfalar.forEach((s, i) => {
    const kagit = document.createElement('div');
    kagit.className = 'baski-kagit';
    const tasma = document.createElement('div');
    tasma.className = 'baski-tasma';
    s.parentNode.insertBefore(kagit, s);
    tasma.appendChild(s);
    kagit.appendChild(tasma);
    const x0 = K.kenar, y0 = K.kenar, x1 = K.kenar + K.trimW, y1 = K.kenar + K.trimH;
    const a = K.tasma + 4, b = K.kenar - 6;     // izler kesimden 16 px (4,2 mm) uzakta başlar, 39 px'te (10,3 mm) biter
    const izler = [
      [x0 - a, y0, x0 - b, y0], [x0, y0 - a, x0, y0 - b], [x1 + a, y0, x1 + b, y0], [x1, y0 - a, x1, y0 - b],
      [x0 - a, y1, x0 - b, y1], [x0, y1 + a, x0, y1 + b], [x1 + a, y1, x1 + b, y1], [x1, y1 + a, x1, y1 + b]];
    const svg = document.createElementNS(ns, 'svg');
    svg.setAttribute('class', 'kesim-izleri');
    svg.setAttribute('viewBox', `0 0 ${K.w} ${K.h}`);
    svg.innerHTML = izler.map(([p, q, r_, t]) => `<path d="M${p} ${q} L${r_} ${t}" stroke="#000" stroke-width=".5"/>`).join('');
    kagit.appendChild(svg);
    const kunye = document.createElement('div');
    kunye.className = 'baski-kunye';
    kunye.textContent = `${baslik} · sayfa ${i + 1}/${sayfalar.length} · kesim 210×297 mm · taşma 3,2 mm`;
    kagit.appendChild(kunye);
  });
}

// ------------------------------------------------------------------ mürekkep (fotokopi): sayfa PNG'sinin ortalama koyuluğu
async function murekkepOlc(tarayici, pngler) {
  const p = await tarayici.newPage();
  await p.setContent('<canvas id="c"></canvas>');
  const out = [];
  for (const b of pngler) {
    out.push(await p.evaluate(async b64 => {
      const img = new Image();
      img.src = 'data:image/png;base64,' + b64;
      await img.decode();
      const c = document.getElementById('c');
      c.width = img.width; c.height = img.height;
      const x = c.getContext('2d');
      x.drawImage(img, 0, 0);
      const d = x.getImageData(0, 0, c.width, c.height).data;
      let t = 0;
      for (let i = 0; i < d.length; i += 4) t += 255 - (0.299 * d[i] + 0.587 * d[i + 1] + 0.114 * d[i + 2]);
      return t / (d.length / 4) / 255;
    }, b.toString('base64')));
  }
  await p.close();
  return out;
}

function type3(pdf) {
  try {
    const cikti = execFileSync('pdffonts', [pdf], { encoding: 'utf8' });
    return cikti.split('\n').filter(l => l.includes('Type 3')).length;
  } catch (e) { return null; }
}

function boyut(pdf) { return (fs.statSync(pdf).size / 1048576).toFixed(2) + ' MB'; }

async function sayfaAc(tarayici, html, olcek = 2) {
  const page = await tarayici.newPage({ viewport: { width: 900, height: 1200 }, deviceScaleFactor: olcek });
  await page.goto('file://' + html, { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  return page;
}

async function pngYaz(page, klasor, secim = []) {
  fs.mkdirSync(klasor, { recursive: true });
  const sayfalar = await page.$$('.sayfa');
  for (let i = 0; i < sayfalar.length; i++) {
    if (secim.length && !secim.includes(i + 1)) continue;
    await sayfalar[i].screenshot({ path: path.join(klasor, `s${String(i + 1).padStart(2, '0')}.png`) });
  }
}

(async () => {
  const ozet = [];
  if (HEPSI && !_dosya) {
    const kur = path.join(UNITE, 'uretec', 'kur.py');
    if (fs.existsSync(kur)) {
      console.log('kurulum: python3 uretec/kur.py --hepsi');
      execFileSync('python3', [kur, '--hepsi'], { stdio: 'inherit' });
    }
  }
  const tarayici = await chromium.launch();

  // ---------------------------------------------------------------- öğrenci
  if (!yalnizVaryant) {
    if (!fs.existsSync(HTML)) { console.error(`HATA: ${HTML} yok; önce python3 uretec/kur.py`); process.exit(1); }
    const page = await sayfaAc(tarayici, HTML);
    const sorunlar = await page.evaluate(tasmaDenetimi);
    console.log(sorunlar.length ? sorunlar.join('\n') : 'Taşma yok.');
    if (!pngsiz) await pngYaz(page, ONIZ, sec);
    if (!pdfsiz) {
      await page.pdf({ path: PDF, preferCSSPageSize: true, printBackground: true });
      const n = (await page.$$('.sayfa')).length;
      console.log(`${n} sayfa → ${path.relative(process.cwd(), PDF)} (${boyut(PDF)})`);
      ozet.push(['öğrenci', PDF]);
    }
    await page.close();
  }

  // ---------------------------------------------------------------- öğretmen
  if (VAR.ogretmen) {
    const page = await sayfaAc(tarayici, HTML);
    await page.evaluate(() => document.documentElement.classList.add('ogretmen'));
    const sorunlar = await page.evaluate(ogretmenDenetimi);
    const dogru = await page.evaluate(() => document.querySelectorAll('[data-dogru]').length);
    const ogr = await page.evaluate(() => document.querySelectorAll('.ogr').length);
    console.log(`öğretmen: ${dogru} doğru işareti, ${ogr} kırmızı cevap` + (sorunlar.length ? '\n' + sorunlar.join('\n') : ' · taşma yok'));
    if (varyantPng) await pngYaz(page, path.join(ONIZ, 'varyant', 'ogretmen'), sec);
    const hedef = path.join(UNITE, KOK + '-ogretmen.pdf');
    await page.pdf({ path: hedef, preferCSSPageSize: true, printBackground: true });
    ozet.push(['öğretmen', hedef]);
    await page.close();
  }

  // ---------------------------------------------------------------- fotokopi
  if (VAR.fotokopi) {
    const html = path.join(UNITE, _ad + '-fotokopi.html');
    if (!fs.existsSync(html)) { console.error(`HATA: ${path.basename(html)} yok; önce python3 uretec/kur.py --fotokopi`); process.exit(1); }
    const page = await sayfaAc(tarayici, html, 1);
    const sayfalar = await page.$$('.sayfa');
    const pngler = [];
    for (const s of sayfalar) pngler.push(await s.screenshot());
    const m = await murekkepOlc(tarayici, pngler);
    const ort = m.reduce((a, b) => a + b, 0) / m.length;
    console.log('fotokopi mürekkebi (sayfa ortalaması, %): ' + m.map((v, i) => `s${i + 1} ${(v * 100).toFixed(1)}`).join(' · ') +
      ` · ORTALAMA ${(ort * 100).toFixed(1)} · EN ÇOK ${(Math.max(...m) * 100).toFixed(1)}`);
    fs.mkdirSync(ONIZ, { recursive: true });
    fs.writeFileSync(path.join(ONIZ, 'fotokopi-murekkep.json'),
      JSON.stringify({ sayfa: m.map(v => +(v * 100).toFixed(2)), ortalama: +(ort * 100).toFixed(2) }, null, 1) + '\n');
    if (varyantPng) { await page.close(); const p2 = await sayfaAc(tarayici, html, 2); await pngYaz(p2, path.join(ONIZ, 'varyant', 'fotokopi'), sec); await p2.close(); }
    else await page.close();
    const p3 = await sayfaAc(tarayici, html, 1);
    const hedef = path.join(UNITE, KOK + '-fotokopi.pdf');
    await p3.pdf({ path: hedef, preferCSSPageSize: true, printBackground: true });
    ozet.push(['fotokopi', hedef]);
    await p3.close();
  }

  // ---------------------------------------------------------------- baskı (matbaa)
  if (VAR.baski) {
    const page = await sayfaAc(tarayici, HTML);
    await page.evaluate(baskiHazirla, KAGIT);
    if (varyantPng) {
      const kl = path.join(ONIZ, 'varyant', 'baski');
      fs.mkdirSync(kl, { recursive: true });
      const kagitlar = await page.$$('.baski-kagit');
      for (let i = 0; i < kagitlar.length; i++) {
        if (sec.length && !sec.includes(i + 1)) continue;
        await kagitlar[i].screenshot({ path: path.join(kl, `s${String(i + 1).padStart(2, '0')}.png`) });
      }
    }
    const hedef = path.join(UNITE, KOK + '-baski.pdf');
    // @page boyutu da kâğıt olmalı: yoksa Chromium A4'e göre dizip içeriği 210/234 oranında küçültür
    await page.addStyleTag({ content: `@page { size: ${KAGIT.w}px ${KAGIT.h}px; margin: 0; }` });
    await page.pdf({ path: hedef, preferCSSPageSize: true, printBackground: true });
    await page.close();
    try {
      execFileSync('python3', [path.join(ORTAK, 'pdf_kutular.py'), hedef, String(KAGIT.kenar * 25.4 / 96), String(KAGIT.tasma * 25.4 / 96)], { stdio: 'inherit' });
    } catch (e) { console.error('UYARI: TrimBox/BleedBox yazılamadı (python3 + pypdf gerekli)'); }
    ozet.push(['baskı', hedef]);
  }

  // ---------------------------------------------------------------- hazine kartları kesme yaprağı
  if (VAR.hazine) {
    const html = path.join(UNITE, 'hazine-kartlari.html');
    if (!fs.existsSync(html)) { console.error('HATA: hazine-kartlari.html yok; önce python3 uretec/kur.py --hazine'); process.exit(1); }
    const page = await sayfaAc(tarayici, html);
    const sorun = await page.evaluate(() => [...document.querySelectorAll('.hy-hucre')].filter(h => h.scrollHeight > h.clientHeight + 2 || h.scrollWidth > h.clientWidth + 2).map(h => h.textContent.trim().slice(0, 30)));
    console.log(sorun.length ? 'hazine yaprağı taşma: ' + sorun.join(' | ') : 'hazine yaprağı: taşma yok');
    if (!pngsiz) { fs.mkdirSync(ONIZ, { recursive: true }); await (await page.$('.sayfa')).screenshot({ path: path.join(ONIZ, 'hazine-kartlari.png') }); }
    const hedef = path.join(UNITE, KOK + '-hazine-kartlari.pdf');
    await page.pdf({ path: hedef, preferCSSPageSize: true, printBackground: true });
    ozet.push(['hazine kartları', hedef]);
    await page.close();
  }
  await tarayici.close();

  if (ozet.length > 1 || yalnizVaryant) {
    console.log('\nPDF                         boyut      Type 3');
    for (const [ad, p] of ozet) {
      const t = type3(p);
      console.log(`${path.basename(p).padEnd(28)}${boyut(p).padEnd(11)}${t === null ? '?' : t}${t ? '  ← HATA: Type 3 font' : ''}`);
    }
  }
})();
