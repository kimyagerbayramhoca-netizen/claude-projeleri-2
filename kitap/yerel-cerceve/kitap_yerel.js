// Kimya Rotası · yeni tasarım (yerel) BİRLEŞİK KİTAP: node kitap/yerel-cerceve/kitap_yerel.js <9|10> [--varyantlar] [--onizleme]
//
//   → kitap/kimya-rotasi-<9|10>-yerel.pdf  (+ -fotokopi / -ogretmen nüshaları, bütün üniteler o nüshayı sağlıyorsa)
//
// Sıra: ön kapak → rehber (2) → Türkiye haritası + içindekiler → üniteler (Yol sırası; her biri tek numaralı sayfada,
// gerekirse önüne "Notlar" sayfası) → Medeniyetimizden zaman şeridi (karşılıklı 2 sayfa) → periyodik tablo → kavram sözlüğü
// → nişan albümü → hazine kartları eki (ünite <klasör>-hazine-kartlari.pdf veriyorsa) → arka kapak.
//
// Sayfa numaraları baştan sona süreklidir. Üniteler ortak kurucunun ortam değişkenleriyle yeniden kurulur:
//   YEREL_SAYFA_BASLANGIC=<kitaptaki ilk sayfa>  YEREL_CIKTI=<geçici>/uNN.html  python3 <ünite>/uretec/kur.py [--fotokopi]
//   node yerel-ortak/render.js <geçici>/uNN.html --pngsiz [--ogretmen|--fotokopi]
// Ünite kurucusu bu değişkenleri tanımıyorsa (eski ünite) unite.html açılıp altbilgi numaraları ve "s.N" göndermeleri
// tarayıcıda kaydırılır (Türkçe ek uyumu düzeltilerek).
// Çerçeve sayfaları uretec/kur.py ile kurulur (içindekiler sayfa numaraları bu plandan gelir), bloklar hâlinde PDF'e basılır,
// hepsi pdfunite ile birleştirilir. Sonunda Type 3 font denetimi (pdffonts) yapılır.
const path = require('path');
const fs = require('fs');
const os = require('os');
const { execFileSync } = require('child_process');
const { chromium } = require('playwright');

const CERCEVE = __dirname;
const KITAP = path.dirname(CERCEVE);
const ORTAK = path.join(KITAP, 'yerel-ortak');
const sinif = process.argv[2];
if (!['9', '10'].includes(sinif)) { console.error('kullanım: node kitap/yerel-cerceve/kitap_yerel.js <9|10> [--varyantlar] [--onizleme]'); process.exit(1); }
const ZORLA_VARYANT = process.argv.includes('--varyantlar');
const GECICI = fs.mkdtempSync(path.join(os.tmpdir(), `kitap-yerel-${sinif}-`));

const calistir = (komut, arg, env = {}) => execFileSync(komut, arg, { env: { ...process.env, ...env }, stdio: ['ignore', 'pipe', 'pipe'] }).toString();
const sayfaSayisi = pdf => parseInt(/Pages:\s+(\d+)/.exec(calistir('pdfinfo', [pdf]))[1], 10);

// ------------------------------------------------------------------ Türkçe sayı eki (yedek yol: "s.13'te" → "s.17'de")
const BIR = ['sıfır', 'bir', 'iki', 'üç', 'dört', 'beş', 'altı', 'yedi', 'sekiz', 'dokuz'];
const ON = ['', 'on', 'yirmi', 'otuz', 'kırk', 'elli', 'altmış', 'yetmiş', 'seksen', 'doksan'];

function planKur(sayilar) {
  const arg = [path.join(CERCEVE, 'uretec', 'kur.py'), sinif, '--plan', path.join(GECICI, 'plan.json'), '--fotokopi'];
  if (sayilar) arg.push('--sayfa-sayilari', JSON.stringify(sayilar));
  process.stdout.write(calistir('python3', arg));
  return JSON.parse(fs.readFileSync(path.join(GECICI, 'plan.json'), 'utf8'));
}

function envDestegi(dizin) {
  const kur = path.join(dizin, 'uretec', 'kur.py');
  if (!fs.existsSync(kur)) return false;
  const metin = fs.readFileSync(kur, 'utf8');
  if (metin.includes('YEREL_SAYFA_BASLANGIC')) return true;
  return metin.includes('kur_ortak') && fs.readFileSync(path.join(ORTAK, 'kur_ortak.py'), 'utf8').includes('YEREL_SAYFA_BASLANGIC');
}

// Bir üniteyi kitap numarasıyla kurar ve istenen nüshaları basar → { ogrenci, fotokopi?, ogretmen? } PDF yolları
function uniteKur(u, bas, nushalar) {
  const ad = `u${String(u.yol).padStart(2, '0')}`;
  const html = path.join(GECICI, `${ad}.html`);
  const env = { YEREL_SAYFA_BASLANGIC: String(bas), YEREL_CIKTI: html };
  const kur = path.join(u.dizin, 'uretec', 'kur.py');
  calistir('python3', [kur], env);
  const render = path.join(ORTAK, 'render.js');
  const sonuc = {};
  calistir('node', [render, html, '--pngsiz'], env);
  sonuc.ogrenci = path.join(GECICI, `${ad}.pdf`);
  if (nushalar.includes('ogretmen')) { calistir('node', [render, html, '--ogretmen', '--pngsiz'], env); sonuc.ogretmen = path.join(GECICI, `${ad}-ogretmen.pdf`); }
  if (nushalar.includes('fotokopi')) {
    calistir('python3', [kur, '--fotokopi'], env);
    calistir('node', [render, html, '--fotokopi', '--pngsiz'], env);
    sonuc.fotokopi = path.join(GECICI, `${ad}-fotokopi.pdf`);
  }
  for (const [k, v] of Object.entries(sonuc)) if (!fs.existsSync(v)) throw new Error(`${u.klasor}: ${k} PDF'i üretilmedi (${v})`);
  return sonuc;
}

// Yedek yol: ortam değişkeni tanımayan ünite → unite.html'i aç, numaraları kaydır, bas
async function uniteKaydirarak(tarayici, u, bas, nusha) {
  const html = path.join(u.dizin, nusha === 'fotokopi' ? 'unite-fotokopi.html' : 'unite.html');
  const sayfa = await tarayici.newPage();
  await sayfa.goto('file://' + html, { waitUntil: 'load' });
  await sayfa.evaluate(() => document.fonts.ready);
  await sayfa.evaluate(({ k, ogretmen, BIR, ON }) => {
    const son = n => (n % 10 || n === 0) ? BIR[n % 10] : (n % 100 ? ON[Math.floor(n / 10) % 10] : (n % 1000 ? 'yüz' : 'bin'));
    const ek = (n, kalip) => {
      const w = son(n); const unlu = [...w].filter(c => 'aeıioöuü'.includes(c)).pop(); const ince = 'eiöü'.includes(unlu);
      const sert = 'fstkçşhp'.includes(w.slice(-1)); const unluSon = 'aeıioöuü'.includes(w.slice(-1));
      if (/^[dt][ea]$/.test(kalip)) return (sert ? 't' : 'd') + (ince ? 'e' : 'a');
      if (/^[dt][ea]n$/.test(kalip)) return (sert ? 't' : 'd') + (ince ? 'en' : 'an');
      if (/^y?[ea]$/.test(kalip)) return (unluSon ? 'y' : '') + (ince ? 'e' : 'a');
      return kalip;
    };
    if (ogretmen) document.documentElement.classList.add('ogretmen');
    document.querySelectorAll('.alt .no b').forEach(b => { const v = parseInt(b.textContent, 10); if (!isNaN(v)) b.textContent = v + k; });
    const yuru = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    const dugum = []; while (yuru.nextNode()) dugum.push(yuru.currentNode);
    dugum.forEach(t => {
      if (t.parentElement.closest('svg,script,style')) return;
      t.textContent = t.textContent.replace(/\bs\.(\d+)(?:([–-])(\d+))?(?:([’'])([a-zçğıöşü]+))?/g, (m, a, tire, b, kesme, e2) => {
        const n1 = +a + k, n2 = b ? +b + k : null; const son_ = n2 ?? n1;
        return `s.${n1}${tire ? tire + n2 : ''}${kesme ? kesme + ek(son_, e2) : ''}`;
      });
    });
  }, { k: bas - 1, ogretmen: nusha === 'ogretmen', BIR, ON });
  const hedef = path.join(GECICI, `u${String(u.yol).padStart(2, '0')}-kaydirma-${nusha}.pdf`);
  await sayfa.pdf({ path: hedef, preferCSSPageSize: true, printBackground: true });
  await sayfa.close();
  return hedef;
}

// Çerçeve sayfalarını ardışık bloklar hâlinde basar → { planNo: pdf (bloğun ilk sayfası), ... } ve blok listesi
async function cerceveBas(tarayici, htmlYolu, plan, nusha) {
  const bloklar = [];
  let simdiki = null;
  for (const p of plan.sayfalar) {
    if (p.tur === 'unite' || p.tur === 'hazine') { simdiki = null; continue; }
    if (!simdiki) { simdiki = []; bloklar.push(simdiki); }
    simdiki.push(p.no);
  }
  const sayfa = await tarayici.newPage();
  await sayfa.goto('file://' + htmlYolu, { waitUntil: 'load' });
  await sayfa.evaluate(() => document.fonts.ready);
  if (nusha === 'ogretmen') await sayfa.evaluate(() => document.documentElement.classList.add('ogretmen'));
  const sonuc = {};
  for (const [i, blok] of bloklar.entries()) {
    await sayfa.evaluate(nolar => {
      document.querySelectorAll('section.sayfa').forEach(s => { s.style.display = nolar.includes(+s.dataset.no) ? '' : 'none'; });
    }, blok);
    const hedef = path.join(GECICI, `cerceve-${nusha}-${i}.pdf`);
    await sayfa.pdf({ path: hedef, preferCSSPageSize: true, printBackground: true });
    const n = sayfaSayisi(hedef);
    if (n !== blok.length) throw new Error(`çerçeve bloğu ${blok[0]}–${blok[blok.length - 1]}: ${n} sayfa basıldı, ${blok.length} bekleniyordu`);
    sonuc[blok[0]] = hedef;
  }
  await sayfa.close();
  return sonuc;
}

(async () => {
  const t0 = Date.now();
  // 1) plan (içindekiler numaraları bu plandan); ünitelerin gerçek sayfa sayısıyla en çok 3 tur uzlaştırılır
  let plan = planKur(null);
  const nushaAdaylari = ['fotokopi', 'ogretmen'].filter(v => plan.uniteler.length &&
    (ZORLA_VARYANT || plan.uniteler.every(u => u.varyantlar && u.varyantlar[v])));
  let uniteler = {};
  for (let tur = 0; tur < 3; tur++) {
    uniteler = {};
    const sayilar = {};
    for (const u of plan.uniteler) {
      const bas = plan.baslar[String(u.yol)];
      if (!bas) continue;
      process.stdout.write(`ünite Yol ${u.yol} (${u.klasor}) → s.${bas} … `);
      if (envDestegi(u.dizin)) uniteler[u.yol] = uniteKur(u, bas, nushaAdaylari);
      else uniteler[u.yol] = { yedek: true, bas };
      if (!uniteler[u.yol].yedek) sayilar[u.yol] = sayfaSayisi(uniteler[u.yol].ogrenci);
      console.log(uniteler[u.yol].yedek ? 'yedek yol (numara kaydırma)' : `${sayilar[u.yol]} sayfa`);
    }
    const uyusmaz = plan.uniteler.filter(u => sayilar[u.yol] && sayilar[u.yol] !== u.sayfa_sayisi);
    if (!uyusmaz.length) break;
    console.log('sayfa sayısı değişti, plan yeniden kuruluyor: ' + uyusmaz.map(u => `Yol ${u.yol} ${u.sayfa_sayisi}→${sayilar[u.yol]}`).join(', '));
    plan = planKur(Object.fromEntries(plan.uniteler.map(u => [u.yol, sayilar[u.yol] || u.sayfa_sayisi])));
  }

  const tarayici = await chromium.launch();
  const nushalar = ['ogrenci', ...nushaAdaylari];
  const ciktilar = [];
  for (const nusha of nushalar) {
    const htmlYolu = nusha === 'fotokopi' ? plan.html.replace(/\.html$/, '-fotokopi.html') : plan.html;
    const cerceve = await cerceveBas(tarayici, htmlYolu, plan, nusha);
    const bos = [];
    const parcalar = [];
    for (const p of plan.sayfalar) {
      if (cerceve[p.no]) parcalar.push(cerceve[p.no]);
      if (p.tur === 'unite' && p.ilk) {
        const u = uniteler[p.yol];
        const uPlan = plan.uniteler.find(x => x.yol === p.yol);
        parcalar.push(u.yedek ? await uniteKaydirarak(tarayici, uPlan, u.bas, nusha) : u[nusha] || u.ogrenci);
      }
      if (p.tur === 'hazine' && p.ilk) parcalar.push(p.pdf);
    }
    const ek = nusha === 'ogrenci' ? '' : `-${nusha}`;
    const hedef = path.join(KITAP, `kimya-rotasi-${sinif}-yerel${ek}.pdf`);
    execFileSync('pdfunite', [...parcalar, hedef]);
    const n = sayfaSayisi(hedef);
    const t3 = calistir('pdffonts', [hedef]).split('\n').filter(l => /Type 3/.test(l)).length;
    console.log(`${path.relative(process.cwd(), hedef)}: ${n} sayfa (plan ${plan.sayfalar.length}) · ${(fs.statSync(hedef).size / 1048576).toFixed(1)} MB · Type 3 font: ${t3}`);
    if (n !== plan.sayfalar.length) console.error('UYARI: sayfa sayısı plandan farklı!');
    if (t3) console.error('UYARI: Type 3 font var (matbaa için düzeltilmeli)');
    ciktilar.push(hedef);
    bos.length = 0;
  }
  await tarayici.close();
  fs.rmSync(GECICI, { recursive: true, force: true });
  console.log('Plan: ' + plan.sayfalar.filter(p => p.tur !== 'unite' || p.ilk).map(p => `${p.no}:${p.tur}${p.yol ? ' Yol ' + p.yol : ''}`).join(' · '));
  console.log(`Bitti (${((Date.now() - t0) / 1000).toFixed(0)} sn).`);
})().catch(e => { console.error('HATA:', e.message); fs.rmSync(GECICI, { recursive: true, force: true }); process.exit(1); });
