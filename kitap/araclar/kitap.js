// Bir sınıfın bütün ünitelerini tek kitapta birleştirir:
//   genel kapak + kullanım rehberi + içindekiler + üniteler (sürekli sayfa numarası).
// Her ünite tek numaralı (sağ) sayfada başlar; gerekirse araya boş sayfa eklenir.
// Kullanım: node araclar/kitap.js 9-sinif   ->  kimya-rotasi-9-sinif.pdf
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');

const KOK = path.resolve(__dirname, '..');
const sinifKlasor = process.argv[2];
const sinifNo = sinifKlasor.split('-')[0];
const GECICI = fs.mkdtempSync(path.join(require('os').tmpdir(), 'kitap-'));
const CSS = fs.readFileSync(path.join(KOK, 'stil', 'kitap.css'), 'utf8');
const ON_SAYFA = 4; // kapak, rehber, içindekiler (2 sayfa)

const esc = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;');

(async () => {
  const tarayici = await chromium.launch();
  const sayfa = await tarayici.newPage({ viewport: { width: 794, height: 1123 } });
  const uniteler = fs.readdirSync(path.join(KOK, sinifKlasor))
    .filter(d => /^\d\d-/.test(d)).sort()
    .map(d => path.join(KOK, sinifKlasor, d, 'unite.html'));

  // 1) Ünite bilgilerini topla ve başlangıç sayfalarını hesapla
  let siradaki = ON_SAYFA + 1;
  const bilgi = [];
  for (const dosya of uniteler) {
    await sayfa.goto('file://' + dosya, { waitUntil: 'load' });
    const b = await sayfa.evaluate(() => {
      const kok = getComputedStyle(document.documentElement);
      const ust = [...document.querySelectorAll('.kapak .ust span')].map(s => s.textContent.trim());
      const baslik = document.querySelector('.kapak h1').innerText.replace(/\s+/g, ' ').trim();
      const ogeler = [...document.querySelectorAll('.icindekiler li')].map(li => {
        const sp = li.querySelectorAll('span');
        return { ad: sp[0].textContent.trim(), no: parseInt(sp[sp.length - 1].textContent, 10) };
      });
      return { renk: kok.getPropertyValue('--unite').trim(), ust, baslik, ogeler,
               sayfaSayisi: document.querySelectorAll('.sayfa').length };
    });
    if (siradaki % 2 === 0) { b.oncesiBos = true; siradaki++; }
    b.baslangic = siradaki;
    b.dosya = dosya;
    siradaki += b.sayfaSayisi;
    bilgi.push(b);
  }
  const toplam = siradaki - 1;

  // 2) Her üniteyi kaydırılmış sayfa numaralarıyla PDF'e bas
  const parcalar = [];
  const bosPdf = path.join(GECICI, 'bos.pdf');
  await sayfa.setContent(`<style>${CSS}</style><section class="sayfa"></section>`);
  await sayfa.pdf({ path: bosPdf, preferCSSPageSize: true, printBackground: true });

  for (const [i, b] of bilgi.entries()) {
    await sayfa.goto('file://' + b.dosya, { waitUntil: 'load' });
    await sayfa.evaluate(() => document.fonts.ready);
    const kaydir = b.baslangic - 1;
    await sayfa.evaluate(k => {
      document.querySelectorAll('.alt-bilgi .no').forEach(n => {
        const v = parseInt(n.textContent, 10); if (!isNaN(v)) n.textContent = v + k;
      });
      document.querySelectorAll('.icindekiler li').forEach(li => {
        const sp = li.querySelectorAll('span'); const son = sp[sp.length - 1];
        son.textContent = son.textContent.replace(/\d+/g, m => +m + k);
      });
    }, kaydir);
    await sayfa.emulateMedia({ media: 'print' });
    const cikti = path.join(GECICI, `u${String(i).padStart(2, '0')}.pdf`);
    await sayfa.pdf({ path: cikti, preferCSSPageSize: true, printBackground: true });
    if (b.oncesiBos) parcalar.push(bosPdf);
    parcalar.push(cikti);
  }

  // 3) Ön sayfalar: kapak, rehber, içindekiler
  const temalar = {};
  bilgi.forEach(b => {
    const t = (b.ust[1] || '').split('·')[0].trim() || 'Tema';
    (temalar[t] = temalar[t] || []).push(b);
  });

  const uniteSatiri = b => {
    const konular = b.ogeler.filter(o => /^\d+\s*·/.test(o.ad));
    const ek = b.ogeler.filter(o => !/^\d+\s*·/.test(o.ad));
    const bolum = (b.ust[1] || '').split('·')[1] || '';
    return `<div class="ic-unite" style="--r:${b.renk}">
      <div class="ic-bas"><span class="ic-etiket">${esc(bolum.trim())}</span><b>${esc(b.baslik)}</b><span class="ic-no">${b.baslangic}</span></div>
      <div class="ic-konular">${konular.map(o => `<div class="ic-alt"><span>${esc(o.ad)}</span><span>${o.no + b.baslangic - 1}</span></div>`).join('')}</div>
      <div class="ic-ek">${ek.map(o => esc(o.ad.replace(/\s*\(özet\)/, '').replace(/^Tek sayfada.*/, 'Özet'))).join(' · ')} <span>${ek.length ? ek[0].no + b.baslangic - 1 : ''}–${b.baslangic + b.sayfaSayisi - 1}</span></div>
    </div>`;
  };

  const temaBloklari = Object.entries(temalar).map(([t, list]) =>
    `<div class="ic-tema"><h3>${esc(t)}</h3>${list.map(uniteSatiri).join('')}</div>`);
  // İçindekiler iki sayfaya bölünür: temaları ünite sayısına göre dengele
  const tumUniteler = Object.entries(temalar).flatMap(([t, l]) => l.map(b => [t, b]));
  const yari = Math.ceil(tumUniteler.length / 2);
  const sayfaIcerik = [tumUniteler.slice(0, yari), tumUniteler.slice(yari)].map(grup => {
    const gruplar = {};
    grup.forEach(([t, b]) => (gruplar[t] = gruplar[t] || []).push(b));
    return Object.entries(gruplar).map(([t, l]) =>
      `<div class="ic-tema"><h3>${esc(t)}</h3>${l.map(uniteSatiri).join('')}</div>`).join('');
  });

  const seritler = bilgi.map(b => `<i style="background:${b.renk}"></i>`).join('');
  const onHtml = `<!doctype html><html lang="tr"><head><meta charset="utf-8"><style>${CSS}
  .gk { padding:0; background:#14112e; color:#fff; }
  .gk .ic { position:absolute; inset:0; padding:24mm 20mm 18mm; display:flex; flex-direction:column; }
  .gk .ust { font-size:9pt; letter-spacing:.16em; text-transform:uppercase; opacity:.8; font-weight:600; }
  .gk h1 { font-size:66pt; font-weight:900; line-height:.92; margin-top:38mm; letter-spacing:-.02em; }
  .gk h1 span { color:#fbbf24; }
  .gk .sinif { font-size:24pt; font-weight:300; margin-top:5mm; }
  .gk .alt { margin-top:auto; display:flex; justify-content:space-between; align-items:flex-end; font-size:9pt; opacity:.85; }
  .gk .seritler { position:absolute; right:0; top:0; bottom:0; width:58mm; display:flex; flex-direction:column; }
  .gk .seritler i { flex:1; display:block; opacity:.92; }
  .gk .bilgi { margin-top:10mm; font-size:10pt; opacity:.85; line-height:1.6; max-width:110mm; }
  .rehber .kart { display:grid; grid-template-columns:24mm 1fr; gap:4mm; align-items:start; margin-bottom:4.4mm; }
  .rehber .kart .ikon { height:16mm; border-radius:3mm; background:var(--renk); color:#fff; display:grid; place-items:center; }
  .rehber .kart .ikon svg { width:8mm; height:8mm; }
  .rehber .kart b { font-size:11pt; color:var(--renk); }
  .rehber .kart p { margin:.6mm 0 0; font-size:9.6pt; }
  .rota { display:grid; grid-template-columns:repeat(4,1fr); gap:2.6mm; }
  .rota div { background:var(--unite-acik); border-radius:2.4mm; padding:2.4mm 3mm; display:flex; gap:2mm; align-items:center; font-size:9pt; font-weight:600; color:var(--unite-koyu); }
  .rota b { width:6mm; height:6mm; flex:none; border-radius:50%; background:var(--unite); color:#fff; display:grid; place-items:center; font-size:8pt; }
  .ic-tema h3 { margin:2mm 0 2.4mm; }
  .ic-unite { border-left:1.6mm solid var(--r); padding:1.4mm 0 1.6mm 3.4mm; margin-bottom:3mm; background:linear-gradient(90deg, color-mix(in srgb, var(--r) 7%, #fff), #fff 60%); border-radius:0 2mm 2mm 0; }
  .ic-bas { display:flex; align-items:baseline; gap:2.4mm; font-size:11.4pt; color:var(--r); }
  .ic-bas b { flex:1; }
  .ic-etiket { font-size:7.4pt; font-weight:800; color:#fff; background:var(--r); border-radius:1.2mm; padding:.3mm 1.8mm; letter-spacing:.06em; text-transform:uppercase; white-space:nowrap; }
  .ic-no { font-weight:800; font-size:12pt; }
  .ic-konular { display:grid; grid-template-columns:1fr 1fr; column-gap:6mm; }
  .ic-alt { display:flex; justify-content:space-between; font-size:9pt; padding:.35mm 0 .35mm 2mm; border-bottom:.25mm dotted #d5d9e6; margin-right:1mm; }
  .ic-alt span:last-child { color:var(--r); font-weight:700; }
  .ic-ek { font-size:8pt; color:var(--soluk); padding:.8mm 0 0 2mm; display:flex; justify-content:space-between; gap:3mm; margin-right:1mm; }
  .ic-ek span { color:var(--r); font-weight:700; white-space:nowrap; }
  </style></head><body style="--unite:#2a2380;--unite-acik:#eef0ff;--unite-koyu:#1e1a5c">

  <section class="sayfa gk">
    <div class="seritler">${seritler}</div>
    <div class="ic">
      <div class="ust">Kimya · Konu anlatımı ve soru kitabı</div>
      <h1>Kimya<br><span>Rotası</span></h1>
      <div class="sinif">${sinifNo}. Sınıf</div>
      <div class="bilgi">${bilgi.length} ünite · ${toplam} sayfa<br>Konu anlatımı · Hata Avcısı · Bağlam temelli sorular · İpucu Merdiveni · Bölüm testleri ve açıklamalı çözümler</div>
      <div class="alt"><span>Yazar: ______________________<br><br>${new Date().getFullYear()}</span></div>
    </div>
  </section>

  <section class="sayfa cift rehber">
    <div class="ust-serit"><span class="baslik-k"><span class="nokta"></span>Kimya Rotası ${sinifNo}</span><span>Bu kitabı nasıl kullanırım?</span></div>
    <h2 class="konu">Bu kitabı nasıl kullanırım?</h2>
    <div class="alt-baslik">Her ünite aynı rotayı izler. Kutuların rengi, ne okuduğunu bir bakışta söyler.</div>
    <div class="kart" style="--renk:var(--kavram)"><div class="ikon">@ikon:kavram</div><div><b>Kavram</b><p>Tanımlar ve temel fikirler. Önce bunları anla; geri kalan her şey bunların üzerine kurulur.</p></div></div>
    <div class="kart" style="--renk:var(--hayat)"><div class="ikon">@ikon:hayat</div><div><b>Hayatın İçinden</b><p>Konunun mutfakta, hastanede, fabrikada ya da doğada nasıl karşına çıktığı.</p></div></div>
    <div class="kart" style="--renk:var(--dikkat)"><div class="ikon">@ikon:dikkat</div><div><b>Kavram Yanılgısı</b><p>Çok sık yapılan bir yanlış ve doğrusu yan yana. Sınavdaki çeldiricilerin çoğu buradan gelir.</p></div></div>
    <div class="kart" style="--renk:var(--ornek)"><div class="ikon">@ikon:ornek</div><div><b>Çözümlü Örnek</b><p>Adım adım çözüm. Önce kendin dene, sonra adımlarla karşılaştır.</p></div></div>
    <div class="kart" style="--renk:var(--hata)"><div class="ikon">@ikon:hata</div><div><b>Hata Avcısı</b><p>Başka öğrencilerin hatalı çözümleri. Hatalı satırı bul, nedenini yaz, doğrusunu çöz.</p></div></div>
    <div class="kart" style="--renk:var(--ipucu)"><div class="ikon">@ikon:ipucu</div><div><b>İpucu Merdiveni</b><p>Takıldığında bir basamak in, yalnızca o ipucunu oku. Ne kadar az basamak kullanırsan o kadar ustasın.</p></div></div>
    <div class="kart" style="--renk:var(--unite)"><div class="ikon">@ikon:test</div><div><b>Tek sayfada özet ve bölüm testi</b><p>Her ünite bir özet sayfası, öz değerlendirme listesi ve 12 soruluk testle biter. Cevap anahtarında her sorunun kısa çözümü var.</p></div></div>
    <h3 style="margin-top:6mm">Bir ünitenin rotası</h3>
    <div class="rota">${['Kapak ve hedefler','Konu anlatımı','Tek sayfada özet','Hata Avcısı','Bağlam temelli sorular','İpucu Merdiveni','Bölüm testi','Cevaplar ve çözümler'].map((a,i)=>`<div><b>${i+1}</b><span>${a}</span></div>`).join('')}</div>
    <p class="kucuk" style="margin-top:4mm">Önerilen çalışma: konu sayfalarını okurken Çözümlü Örnekleri kapatıp önce kendin dene. Özet sayfasındaki "Kendimi değerlendiriyorum" listesinde "Tekrar" işaretlediğin konuya dön, sonra soru sayfalarına geç. Testi süre tutarak çöz; yanlışlarını cevap anahtarındaki çözümle karşılaştır.</p>
    <div class="alt-bilgi"><span>Kimya Rotası ${sinifNo}</span><span class="no">2</span></div>
  </section>

  <section class="sayfa">
    <div class="ust-serit"><span class="baslik-k"><span class="nokta"></span>Kimya Rotası ${sinifNo}</span><span>İçindekiler</span></div>
    <h2 class="konu">İçindekiler</h2>
    ${sayfaIcerik[0]}
    <div class="alt-bilgi"><span>Kimya Rotası ${sinifNo}</span><span class="no">3</span></div>
  </section>

  <section class="sayfa cift">
    <div class="ust-serit"><span class="baslik-k"><span class="nokta"></span>Kimya Rotası ${sinifNo}</span><span>İçindekiler</span></div>
    ${sayfaIcerik[1]}
    <div class="alt-bilgi"><span>Kimya Rotası ${sinifNo}</span><span class="no">4</span></div>
  </section>
  </body></html>`;

  // ikonları derle.py ile aynı kaynaktan al
  const ikonlar = JSON.parse(execFileSync('python3', ['-c',
    'import json,sys; sys.path.insert(0,"' + path.join(KOK, 'araclar') + '"); from ikonlar import IKONLAR; print(json.dumps(IKONLAR))']).toString());
  const onDosya = path.join(GECICI, 'on.html');
  fs.writeFileSync(onDosya, onHtml.replace(/@ikon:(\w+)/g, (_, a) => ikonlar[a]));
  await sayfa.goto('file://' + onDosya, { waitUntil: 'load' });
  await sayfa.evaluate(() => document.fonts.ready);
  const tasma = await sayfa.evaluate(() => [...document.querySelectorAll('.sayfa')].map((s, i) => {
    if (i === 0) return null;
    const alt = s.getBoundingClientRect().bottom - 50;
    const b = Math.max(...[...s.children].filter(e => !e.classList.contains('alt-bilgi')).map(e => e.getBoundingClientRect().bottom));
    return b > alt ? `Ön sayfa ${i + 1}: ${Math.round(b - alt)}px taşma` : null;
  }).filter(Boolean));
  tasma.forEach(t => console.warn('UYARI', t));
  if (process.env.ONIZLEME) {
    for (let i = 0; i < 4; i++) await sayfa.locator('.sayfa').nth(i).screenshot({ path: path.join(process.env.ONIZLEME, `on${i + 1}.png`) });
  }
  await sayfa.emulateMedia({ media: 'print' });
  const onPdf = path.join(GECICI, 'on.pdf');
  await sayfa.pdf({ path: onPdf, preferCSSPageSize: true, printBackground: true });
  await tarayici.close();

  const hedef = path.join(KOK, `kimya-rotasi-${sinifKlasor}.pdf`);
  execFileSync('pdfunite', [onPdf, ...parcalar, hedef]);
  fs.rmSync(GECICI, { recursive: true, force: true });
  console.log(`Hazır: ${hedef} (${toplam} sayfa)`);
  bilgi.forEach(b => console.log(`  s.${b.baslangic}${b.oncesiBos ? ' (öncesi boş)' : ''}  ${b.baslik}`));
})();
