const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
const { execSync } = require('child_process');

const DOWNLOADS_DIR = path.join(process.env.HOME, 'Downloads');
const VIDEOS_DIR = path.resolve('assets/videos');

const REELS = [
  {
    num: 1,
    template: 'scripts/animated_templates/reel1_animated.html',
    assetName: 'reel1_dm_for_price_trap.mp4',
    downloadName: '01_Reel_DM_For_Price_Trap.mp4',
    title: "Why 'DM For Price' is Killing 70% of Sales"
  },
  {
    num: 2,
    template: 'scripts/animated_templates/reel2_animated.html',
    assetName: 'reel2_huna_website_corporate.mp4',
    downloadName: '02_Reel_Huna_Website_Corporate.mp4',
    title: 'How to Lose a KES 200,000 Corporate Client'
  },
  {
    num: 3,
    template: 'scripts/animated_templates/reel3_animated.html',
    assetName: 'reel3_ghosted_web_guy.mp4',
    downloadName: '03_Reel_Ghosted_By_Cheap_Web_Guy.mp4',
    title: '3 Signs Your Cheap Web Guy is About to Ghost You'
  },
  {
    num: 4,
    template: 'scripts/animated_templates/reel4_animated.html',
    assetName: 'reel4_express_landing_page.mp4',
    downloadName: '04_Reel_KES_15K_Express_Landing_Page.mp4',
    title: 'KES 15K Express Landing Page Secret'
  },
  {
    num: 5,
    template: 'scripts/animated_templates/reel5_animated.html',
    assetName: 'reel5_chama_sacco_automation.mp4',
    downloadName: '05_Reel_Chama_SACCO_Automation.mp4',
    title: 'Bado Mnasimamia Chama kwa Excel na WhatsApp?'
  }
];

async function renderReel(reel, soundtrackPath) {
  console.log(`\n======================================================`);
  console.log(`🎬 Rendering Reel #${reel.num}: ${reel.title}`);
  console.log(`======================================================`);

  const tmpDir = `/tmp/pw_render_reel_${reel.num}`;
  if (fs.existsSync(tmpDir)) {
    fs.rmSync(tmpDir, { recursive: true, force: true });
  }
  fs.mkdirSync(tmpDir, { recursive: true });

  const browser = await chromium.launch({
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    headless: true,
    args: ['--no-sandbox', '--disable-gpu', '--autoplay-policy=no-user-gesture-required']
  });

  const context = await browser.newContext({
    viewport: { width: 1080, height: 1920 },
    recordVideo: { dir: tmpDir, size: { width: 1080, height: 1920 } }
  });

  const page = await context.newPage();
  const fileUrl = 'file://' + path.resolve(reel.template);
  console.log(`Loading template: ${fileUrl}`);
  await page.goto(fileUrl);

  console.log(`Recording 23.0s of Canva-style animations (Typewriter + Boom + Slams)...`);
  await page.waitForTimeout(23000);

  await context.close();
  await browser.close();

  // Find recorded webm
  const files = fs.readdirSync(tmpDir).filter(f => f.endsWith('.webm'));
  if (files.length === 0) {
    throw new Error(`No webm file found in ${tmpDir}`);
  }
  const webmPath = path.join(tmpDir, files[0]);
  console.log(`Recorded raw video: ${webmPath} (${fs.statSync(webmPath).size} bytes)`);

  const targetAssetPath = path.join(VIDEOS_DIR, reel.assetName);
  const targetDownloadPath = path.join(DOWNLOADS_DIR, reel.downloadName);

  // Mux with audio using FFmpeg
  console.log(`Muxing with audio soundtrack and encoding H.264 / AAC 1080x1920...`);
  const ffmpegCmd = `ffmpeg -y -i "${webmPath}" -i "${soundtrackPath}" -c:v libx264 -preset veryfast -crf 19 -pix_fmt yuv420p -c:a aac -b:a 192k -shortest "${targetAssetPath}"`;
  execSync(ffmpegCmd, { stdio: 'inherit' });

  // Copy to downloads
  fs.copyFileSync(targetAssetPath, targetDownloadPath);
  console.log(`✅ Asset Saved: ${targetAssetPath}`);
  console.log(`📁 Download Ready: ${targetDownloadPath} (${fs.statSync(targetDownloadPath).size} bytes)`);
}

async function main() {
  fs.mkdirSync(VIDEOS_DIR, { recursive: true });
  fs.mkdirSync(DOWNLOADS_DIR, { recursive: true });

  const soundtrackPath = '/tmp/reel_soundtrack.wav';
  if (!fs.existsSync(soundtrackPath)) {
    console.log(`Generating soundtrack via Python helper...`);
    execSync(`python3 -c "import sys; sys.path.append('scripts'); import render_all_premium_reels as r; r.generate_soundtrack('${soundtrackPath}', 24.5)"`, { stdio: 'inherit' });
  }

  const startTime = Date.now();
  for (const reel of REELS) {
    await renderReel(reel, soundtrackPath);
  }

  const durationSec = Math.round((Date.now() - startTime) / 1000);
  console.log(`\n🎉 ALL 5 CANVA-ANIMATED REELS SUCCESSFULLY RENDERED IN ${durationSec}s!`);
}

main().catch(err => {
  console.error('Fatal error in rendering:', err);
  process.exit(1);
});

