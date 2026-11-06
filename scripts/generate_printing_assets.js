const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const HTML_SERVICE = `<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    width: 1200px;
    height: 800px;
    background: radial-gradient(circle at 75% 20%, #1e293b 0%, #0f172a 50%, #020617 100%);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    color: #fff;
    display: flex;
    position: relative;
    overflow: hidden;
  }
  
  .grid-pattern {
    position: absolute;
    inset: 0;
    background-image: 
      linear-gradient(to right, rgba(255,255,255,0.03) 1px, transparent 1px),
      linear-gradient(to bottom, rgba(255,255,255,0.03) 1px, transparent 1px);
    background-size: 40px 40px;
  }
  
  .glow-cyan {
    position: absolute;
    top: -100px;
    right: 150px;
    width: 500px;
    height: 500px;
    background: radial-gradient(circle, rgba(14, 165, 233, 0.25) 0%, transparent 70%);
    filter: blur(40px);
  }
  
  .glow-amber {
    position: absolute;
    bottom: -150px;
    left: 200px;
    width: 600px;
    height: 600px;
    background: radial-gradient(circle, rgba(245, 158, 11, 0.15) 0%, transparent 70%);
    filter: blur(60px);
  }

  .content-wrap {
    position: relative;
    z-index: 10;
    width: 100%;
    height: 100%;
    display: flex;
    padding: 60px;
    gap: 50px;
  }

  .left-col {
    flex: 1.1;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }

  .brand-tag {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 6px 16px;
    background: rgba(14, 165, 233, 0.15);
    border: 1px solid rgba(14, 165, 233, 0.4);
    border-radius: 999px;
    color: #38bdf8;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    width: fit-content;
    margin-bottom: 24px;
  }

  h1 {
    font-size: 46px;
    font-weight: 800;
    line-height: 1.15;
    margin-bottom: 20px;
    letter-spacing: -0.02em;
  }
  
  .gradient-text {
    background: linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #f472b6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }

  p.lead {
    font-size: 18px;
    color: #94a3b8;
    line-height: 1.6;
    margin-bottom: 32px;
  }

  .features-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 16px;
    margin-bottom: 32px;
  }

  .feature-pill {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 12px 16px;
    background: rgba(30, 41, 59, 0.7);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    font-size: 14px;
    font-weight: 600;
    color: #e2e8f0;
  }

  .right-col {
    flex: 1.2;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .mockup-stage {
    position: relative;
    width: 100%;
    height: 600px;
  }

  .book-a4 {
    position: absolute;
    width: 320px;
    height: 440px;
    background: linear-gradient(145deg, #0f172a, #1e293b);
    border-radius: 6px 16px 16px 6px;
    box-shadow: 
      -12px 18px 45px rgba(0,0,0,0.8),
      inset 4px 0 10px rgba(255,255,255,0.1),
      inset -4px 0 12px rgba(0,0,0,0.6);
    top: 50px;
    left: 40px;
    transform: rotate(-6deg);
    border-left: 8px solid #0284c7;
    padding: 30px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    z-index: 3;
  }

  .book-sub {
    font-size: 11px;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #38bdf8;
    font-weight: 700;
  }

  .book-title {
    font-size: 24px;
    font-weight: 800;
    line-height: 1.2;
    color: #ffffff;
  }

  .book-spine-line {
    width: 60px;
    height: 3px;
    background: #f59e0b;
    border-radius: 2px;
    margin-top: 8px;
  }

  .book-chart-art {
    width: 100%;
    height: 140px;
    background: rgba(14, 165, 233, 0.08);
    border: 1px dashed rgba(14, 165, 233, 0.3);
    border-radius: 8px;
    display: flex;
    align-items: flex-end;
    padding: 15px;
    gap: 12px;
  }

  .chart-bar {
    flex: 1;
    border-radius: 4px;
    background: linear-gradient(to top, #0284c7, #38bdf8);
  }

  .book-foot {
    font-size: 11px;
    color: #64748b;
    display: flex;
    justify-content: space-between;
    border-top: 1px solid rgba(255,255,255,0.1);
    padding-top: 15px;
  }

  .wireo-manual {
    position: absolute;
    width: 290px;
    height: 390px;
    background: linear-gradient(135deg, #1e1b4b, #312e81);
    border-radius: 8px;
    box-shadow: 15px 25px 50px rgba(0,0,0,0.7);
    top: 140px;
    right: 20px;
    transform: rotate(8deg);
    padding: 25px;
    z-index: 2;
    border-top: 2px solid rgba(255,255,255,0.15);
  }

  .wire-rings {
    position: absolute;
    left: -12px;
    top: 20px;
    bottom: 20px;
    width: 24px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }

  .ring {
    width: 20px;
    height: 10px;
    border: 3px solid #cbd5e1;
    border-radius: 10px;
    background: #475569;
  }

  .calc-badge {
    position: absolute;
    bottom: 40px;
    left: 90px;
    background: rgba(15, 23, 42, 0.95);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(56, 189, 248, 0.4);
    border-radius: 16px;
    padding: 20px 24px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.8), 0 0 25px rgba(14, 165, 233, 0.25);
    z-index: 5;
    display: flex;
    align-items: center;
    gap: 18px;
  }

  .calc-icon {
    width: 48px;
    height: 48px;
    background: linear-gradient(135deg, #0284c7, #38bdf8);
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
  }

  .calc-details h4 {
    font-size: 13px;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #94a3b8;
    margin-bottom: 4px;
  }

  .calc-details .price {
    font-size: 22px;
    font-weight: 800;
    color: #38bdf8;
  }

  .calc-details .meta {
    font-size: 11px;
    color: #10b981;
    font-weight: 600;
  }

  .swatch-fan {
    position: absolute;
    top: 30px;
    right: 80px;
    background: #020617;
    border: 1px solid rgba(255,255,255,0.15);
    padding: 8px 14px;
    border-radius: 999px;
    font-size: 12px;
    color: #f59e0b;
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 6px;
    box-shadow: 0 10px 20px rgba(0,0,0,0.5);
    z-index: 4;
  }
</style>
</head>
<body>
  <div class="grid-pattern"></div>
  <div class="glow-cyan"></div>
  <div class="glow-amber"></div>

  <div class="content-wrap">
    <div class="left-col">
      <div class="brand-tag">
        <span>⚙️</span> Industrial Digital & Offset Press
      </div>
      <h1>
        Commercial Printing &amp; <br>
        <span class="gradient-text">Publication Production</span>
      </h1>
      <p class="lead">
        Executive annual reports, corporate training manuals, brand booklets, and marketing collateral. Engineered with industrial machine bindery and transparent real-time pricing.
      </p>

      <div class="features-grid">
        <div class="feature-pill">
          <span>✨</span> 300 DPI CMYK High-Fidelity
        </div>
        <div class="feature-pill">
          <span>📐</span> Perfect, Wire-O &amp; Hardcover
        </div>
        <div class="feature-pill">
          <span>⚡</span> Live Transparent Calculator
        </div>
        <div class="feature-pill">
          <span>🚚</span> All 47 Counties Dispatch
        </div>
      </div>
    </div>

    <div class="right-col">
      <div class="mockup-stage">
        
        <div class="swatch-fan">
          <span>🎨</span> 80gsm – 350gsm Certified Stocks
        </div>

        <!-- Wire-O Manual -->
        <div class="wireo-manual">
          <div class="wire-rings">
            <div class="ring"></div><div class="ring"></div><div class="ring"></div>
            <div class="ring"></div><div class="ring"></div><div class="ring"></div>
            <div class="ring"></div><div class="ring"></div><div class="ring"></div>
          </div>
          <div style="font-size: 10px; color: #a5b4fc; text-transform: uppercase; font-weight: 700; letter-spacing: 1px;">SOP &amp; Training Module</div>
          <div style="font-size: 18px; font-weight: 800; color: #fff; margin-top: 8px;">Corporate Induction &amp; Policy Manual</div>
          <div style="font-size: 11px; color: #94a3b8; margin-top: 15px;">Wire-O 360° Lay-Flat Bindery<br>Matt Laminated Heavy Cover</div>
        </div>

        <!-- A4 Book -->
        <div class="book-a4">
          <div>
            <div class="book-sub">Executive Edition</div>
            <div class="book-title">Annual Report &amp; Audited Financials</div>
            <div class="book-spine-line"></div>
          </div>
          <div class="book-chart-art">
            <div class="chart-bar" style="height: 40%;"></div>
            <div class="chart-bar" style="height: 65%;"></div>
            <div class="chart-bar" style="height: 85%;"></div>
            <div class="chart-bar" style="height: 100%;"></div>
            <div class="chart-bar" style="height: 75%;"></div>
          </div>
          <div class="book-foot">
            <span>A4 Corporate • 130gsm Silk</span>
            <span>Perfect Binding</span>
          </div>
        </div>

        <!-- Floating Calc Badge -->
        <div class="calc-badge">
          <div class="calc-icon">🧮</div>
          <div class="calc-details">
            <h4>Live Pricing Engine</h4>
            <div class="price">KES 245.00 <span style="font-size: 13px; color: #94a3b8; font-weight: 400;">/ copy</span></div>
            <div class="meta">✓ Instant WhatsApp Formal Proforma</div>
          </div>
        </div>

      </div>
    </div>
  </div>
</body>
</html>`;

const HTML_BLOG = `<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    width: 1200px;
    height: 630px;
    background: #020617;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    color: #fff;
    display: flex;
    position: relative;
    overflow: hidden;
  }
  
  .glow-top {
    position: absolute;
    top: -120px;
    left: 300px;
    width: 600px;
    height: 400px;
    background: radial-gradient(circle, rgba(14, 165, 233, 0.3) 0%, transparent 70%);
    filter: blur(50px);
  }

  .glow-bot {
    position: absolute;
    bottom: -100px;
    right: 150px;
    width: 500px;
    height: 400px;
    background: radial-gradient(circle, rgba(99, 102, 241, 0.25) 0%, transparent 70%);
    filter: blur(60px);
  }

  .grid-pattern {
    position: absolute;
    inset: 0;
    background-image: 
      linear-gradient(to right, rgba(255,255,255,0.04) 1px, transparent 1px),
      linear-gradient(to bottom, rgba(255,255,255,0.04) 1px, transparent 1px);
    background-size: 48px 48px;
  }

  .content-wrap {
    position: relative;
    z-index: 10;
    width: 100%;
    height: 100%;
    display: flex;
    padding: 60px 70px;
    gap: 40px;
  }

  .left-col {
    flex: 1.25;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }

  .badge-row {
    display: flex;
    gap: 12px;
    margin-bottom: 22px;
  }

  .tag-pill {
    padding: 6px 14px;
    background: rgba(14, 165, 233, 0.15);
    border: 1px solid rgba(14, 165, 233, 0.4);
    border-radius: 999px;
    color: #38bdf8;
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  .tag-pill.gold {
    background: rgba(245, 158, 11, 0.15);
    border-color: rgba(245, 158, 11, 0.4);
    color: #fbbf24;
  }

  h1 {
    font-size: 38px;
    font-weight: 800;
    line-height: 1.2;
    margin-bottom: 18px;
    letter-spacing: -0.02em;
  }

  .highlight {
    background: linear-gradient(135deg, #38bdf8, #818cf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }

  p.desc {
    font-size: 17px;
    color: #94a3b8;
    line-height: 1.55;
    margin-bottom: 26px;
  }

  .author-row {
    display: flex;
    align-items: center;
    gap: 14px;
    border-top: 1px solid rgba(255,255,255,0.1);
    padding-top: 20px;
  }

  .author-avatar {
    width: 44px;
    height: 44px;
    border-radius: 50%;
    background: linear-gradient(135deg, #0284c7, #38bdf8);
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
    font-size: 16px;
    color: #fff;
    border: 2px solid #38bdf8;
  }

  .author-meta h4 {
    font-size: 14px;
    font-weight: 700;
    color: #fff;
  }

  .author-meta p {
    font-size: 12px;
    color: #64748b;
  }

  .right-col {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
  }

  .frame-card {
    width: 380px;
    background: #0f172a;
    border: 1px solid #334155;
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 25px 60px rgba(0,0,0,0.8), 0 0 35px rgba(56, 189, 248, 0.2);
    transform: rotate(2deg);
  }

  .frame-head {
    background: #1e293b;
    padding: 12px 16px;
    display: flex;
    align-items: center;
    gap: 8px;
    border-bottom: 1px solid #334155;
  }

  .dot { width: 10px; height: 10px; border-radius: 50%; }
  .dot.r { background: #ef4444; }
  .dot.y { background: #f59e0b; }
  .dot.g { background: #10b981; }

  .frame-body {
    padding: 24px;
  }

  .calc-title {
    font-size: 13px;
    font-weight: 700;
    color: #38bdf8;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 16px;
    display: flex;
    justify-content: space-between;
  }

  .spec-item {
    display: flex;
    justify-content: space-between;
    padding: 10px 0;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    font-size: 13px;
  }

  .spec-label { color: #94a3b8; }
  .spec-val { color: #f1f5f9; font-weight: 600; }

  .total-row {
    margin-top: 18px;
    padding-top: 14px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 1px dashed #38bdf8;
  }

  .total-label { font-size: 13px; font-weight: 700; color: #fff; }
  .total-price { font-size: 24px; font-weight: 900; color: #38bdf8; }

  .wa-button {
    margin-top: 16px;
    width: 100%;
    padding: 10px;
    background: #10b981;
    border-radius: 8px;
    color: #fff;
    font-weight: 700;
    font-size: 13px;
    text-align: center;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
  }
</style>
</head>
<body>
  <div class="grid-pattern"></div>
  <div class="glow-top"></div>
  <div class="glow-bot"></div>

  <div class="content-wrap">
    <div class="left-col">
      <div class="badge-row">
        <span class="tag-pill">Commercial Printing Guide</span>
        <span class="tag-pill gold">2026 Price Benchmark</span>
      </div>
      <h1>
        Commercial Printing in Kenya: <br>
        <span class="highlight">Paper GSM, Binding &amp; Live Costs</span>
      </h1>
      <p class="desc">
        Everything you need to know about corporate publication printing in Nairobi. Avoid pre-press errors, choose the right paper weights, and calculate exact press runs in seconds.
      </p>

      <div class="author-row">
        <div class="author-avatar">XT</div>
        <div class="author-meta">
          <h4>Samuel Kidemi • Xclusive Tech</h4>
          <p>Lead Engineer &amp; Co-Founder Top Digitally Fit Firm</p>
        </div>
      </div>
    </div>

    <div class="right-col">
      <div class="frame-card">
        <div class="frame-head">
          <div class="dot r"></div>
          <div class="dot y"></div>
          <div class="dot g"></div>
          <span style="font-size: 11px; font-family: monospace; color: #94a3b8; margin-left: 10px;">xclusivetech.co.ke/printing</span>
        </div>
        <div class="frame-body">
          <div class="calc-title">
            <span>Live Print Estimator</span>
            <span style="color: #10b981;">Online</span>
          </div>
          <div class="spec-item">
            <span class="spec-label">Format:</span>
            <span class="spec-val">A4 Corporate Document</span>
          </div>
          <div class="spec-item">
            <span class="spec-label">Volume &amp; Pages:</span>
            <span class="spec-val">100 copies × 48pp</span>
          </div>
          <div class="spec-item">
            <span class="spec-label">Inner Paper:</span>
            <span class="spec-val">130gsm Art Paper (Colour)</span>
          </div>
          <div class="spec-item">
            <span class="spec-label">Cover &amp; Finish:</span>
            <span class="spec-val">300gsm Matt Lamination</span>
          </div>
          <div class="spec-item">
            <span class="spec-label">Bindery:</span>
            <span class="spec-val">Perfect Bound Square Spine</span>
          </div>
          
          <div class="total-row">
            <span class="total-label">Live Estimate:</span>
            <span class="total-price">KES 24,500</span>
          </div>
          
          <div class="wa-button">
            <span>💬</span> Instant WhatsApp Proforma
          </div>
        </div>
      </div>
    </div>
  </div>
</body>
</html>`;

(async () => {
  fs.mkdirSync('assets/images/services', { recursive: true });
  fs.mkdirSync('assets/images/blog', { recursive: true });
  fs.mkdirSync('/tmp/printing_render', { recursive: true });

  fs.writeFileSync('/tmp/printing_render/service.html', HTML_SERVICE);
  fs.writeFileSync('/tmp/printing_render/blog.html', HTML_BLOG);

  const browser = await chromium.launch();

  // 1. Service mockup (1200x800)
  const page1 = await browser.newPage({ viewport: { width: 1200, height: 800 }, deviceScaleFactor: 2 });
  await page1.goto('file:///tmp/printing_render/service.html');
  await page1.screenshot({ path: '/tmp/printing_render/service_raw.png' });
  console.log('Captured service_raw.png');

  // 2. Blog cover (1200x630)
  const page2 = await browser.newPage({ viewport: { width: 1200, height: 630 }, deviceScaleFactor: 2 });
  await page2.goto('file:///tmp/printing_render/blog.html');
  await page2.screenshot({ path: '/tmp/printing_render/blog_raw.png' });
  console.log('Captured blog_raw.png');

  await browser.close();

  // Convert via python pillow
  execSync(`python3 -c '
from PIL import Image
# Service
im1 = Image.open("/tmp/printing_render/service_raw.png").resize((1200, 800), Image.Resampling.LANCZOS)
im1.convert("RGB").save("assets/images/services/commercial-printing.jpg", "JPEG", quality=92, optimize=True)
im1.save("assets/images/services/commercial-printing.webp", "WEBP", quality=90)

# Blog
im2 = Image.open("/tmp/printing_render/blog_raw.png").resize((1200, 630), Image.Resampling.LANCZOS)
im2.convert("RGB").save("assets/images/blog/guide-to-commercial-printing-services-kenya-costs-paper-calculator.jpg", "JPEG", quality=92, optimize=True)
im2.save("assets/images/blog/guide-to-commercial-printing-services-kenya-costs-paper-calculator.webp", "WEBP", quality=90)
print("Finished image conversion!")
'`);

  console.log('Assets created successfully!');
})();

