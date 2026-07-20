#!/usr/bin/env node
/* ============================================
   XCLUSIVE TECH — WEEKLY BLOG POST GENERATOR
   ============================================
   Fact-grounded, autonomous, zero-review by design.
   Safety comes from constraining the model to
   content/site-facts.json — not from a human
   reading every post before it publishes.

   Run: node scripts/generate-post.mjs
   Requires: ANTHROPIC_API_KEY env var
   ============================================ */

import Anthropic from '@anthropic-ai/sdk';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');

const FACTS_PATH = path.join(ROOT, 'content', 'site-facts.json');
const LOG_PATH = path.join(ROOT, 'content', 'posts-log.json');
const BLOG_DIR = path.join(ROOT, 'blog');
const BLOG_INDEX_PATH = path.join(BLOG_DIR, 'index.html');
const SITEMAP_PATH = path.join(ROOT, 'sitemap.xml');

const MODEL = 'claude-sonnet-5';
const MIN_WORDS = 650;
const PLACEHOLDER_PATTERNS = [/\[insert/i, /\btodo\b/i, /lorem ipsum/i, /\[placeholder/i];

// A small, fixed list of reputable, legitimate public RSS feeds for roundup posts.
// Only titles/links/summaries are ever used — never full article text.
const ROUNDUP_FEEDS = [
  { name: 'Google Search Central Blog', url: 'https://developers.google.com/search/blog/feed.xml' },
  { name: 'Smashing Magazine', url: 'https://www.smashingmagazine.com/feed/' },
  { name: 'Search Engine Journal', url: 'https://www.searchenginejournal.com/feed/' }
];

const GENERAL_TOPICS = [
  'M-Pesa and Daraja API integration for small business websites',
  'Mobile-first design and why it matters more in Kenya than almost anywhere',
  'What to actually check before hiring a web designer in Kenya',
  'Website maintenance: what it covers and why it is not optional',
  'E-commerce basics for Kenyan SMEs moving online for the first time',
  'Local business marketing tips for Thika, Kiambu, Ruiru and Juja',
  'Domain names explained: .co.ke vs .com and what to actually pick',
  'Google Business Profile: the free tool most small businesses ignore'
];

function loadJson(p) {
  return JSON.parse(fs.readFileSync(p, 'utf8'));
}

function saveJson(p, data) {
  fs.writeFileSync(p, JSON.stringify(data, null, 2) + '\n');
}

function slugify(title) {
  return title
    .toLowerCase()
    .replace(/[^a-z0-9\s-]/g, '')
    .trim()
    .replace(/\s+/g, '-')
    .replace(/-+/g, '-');
}

function uniqueSlug(baseSlug) {
  let slug = baseSlug;
  let n = 2;
  while (fs.existsSync(path.join(BLOG_DIR, `${slug}.html`))) {
    slug = `${baseSlug}-${n}`;
    n += 1;
  }
  return slug;
}

function wordCount(text) {
  return text.trim().split(/\s+/).filter(Boolean).length;
}

function hasPlaceholderText(text) {
  return PLACEHOLDER_PATTERNS.some((re) => re.test(text));
}

/** Decide what this week's post should be about. */
function decideTopic(facts, log) {
  const totalPosts = log.posts.length;
  const isRoundupWeek = (totalPosts + 1) % 4 === 0;

  if (isRoundupWeek) {
    return { type: 'roundup' };
  }

  const coveredIndustries = new Set(
    log.posts.filter((p) => p.type === 'industry').map((p) => p.topic)
  );
  const nextIndustry = facts.industriesServed.find((i) => !coveredIndustries.has(i));
  if (nextIndustry) {
    const matchingProject = facts.portfolio.find((p) =>
      nextIndustry.toLowerCase().includes(p.industry.toLowerCase().split(' ')[0].toLowerCase())
    );
    return { type: 'industry', industry: nextIndustry, portfolioProject: matchingProject || null };
  }

  const usedGeneralTopics = new Set(
    log.posts.filter((p) => p.type === 'original').map((p) => p.topic)
  );
  const nextGeneral =
    GENERAL_TOPICS.find((t) => !usedGeneralTopics.has(t)) ||
    GENERAL_TOPICS[totalPosts % GENERAL_TOPICS.length];
  return { type: 'original', topic: nextGeneral };
}

async function fetchRoundupItems() {
  const items = [];
  for (const feed of ROUNDUP_FEEDS) {
    try {
      const res = await fetch(feed.url, { headers: { 'User-Agent': 'XclusiveTechBot/1.0' } });
      if (!res.ok) continue;
      const xml = await res.text();
      const entries = [...xml.matchAll(/<item>([\s\S]*?)<\/item>/g)].slice(0, 3);
      for (const [, block] of entries) {
        const title = (block.match(/<title>([\s\S]*?)<\/title>/) || [])[1]?.replace(/<!\[CDATA\[|\]\]>/g, '').trim();
        const link = (block.match(/<link>([\s\S]*?)<\/link>/) || [])[1]?.trim();
        const desc = (block.match(/<description>([\s\S]*?)<\/description>/) || [])[1]
          ?.replace(/<!\[CDATA\[|\]\]>/g, '')
          .replace(/<[^>]+>/g, '')
          .trim();
        if (title && link) {
          items.push({ source: feed.name, title, link, summary: (desc || '').slice(0, 300) });
        }
      }
    } catch (err) {
      console.warn(`Could not fetch ${feed.name}:`, err.message);
    }
  }
  return items.slice(0, 6);
}

function buildPrompt(facts, decision, roundupItems) {
  const factsJson = JSON.stringify(facts, null, 2);
  const baseRules = `You are writing a blog post for Xclusive Tech, a web design and development company in Kenya. The post will be published to their live business website with NO human review before it goes live, so accuracy is critical.

STRICT RULES:
1. Only use facts, prices, service descriptions, and portfolio details from the JSON context below. Never invent statistics, client results, testimonials, dates, or specific numbers that are not explicitly present in the context.
2. If you reference a portfolio project, use ONLY the challenge/whatWeBuilt/result fields provided — do not add invented narrative details about how or why decisions were made.
3. Do not claim things about competitors, do not make legal/medical/financial guarantees, and do not use superlatives ("the best", "#1") that aren't already used verbatim in the context.
4. Mention the service area (Thika, Kiambu, Ruiru, Juja, Nairobi) only where genuinely relevant to the sentence — never forced into every paragraph.
5. Write 700-1200 words of original body content.
6. Include at least one natural internal link using relative paths like "../pricing.html", "../services.html", "../solutions.html", or "../portfolio.html".

SITE FACTS (the only source of truth — do not go beyond this):
${factsJson}

Respond with ONLY a single valid JSON object (no markdown fences, no commentary) with exactly these keys:
{
  "title": "SEO title tag, under 65 characters, include 'Xclusive Tech'",
  "headline": "H1 headline, can be longer/punchier than the title tag, may include & as &amp;",
  "description": "meta description, under 160 characters",
  "keywords": "comma-separated SEO keywords",
  "category": "short category label like 'Industry' or 'Pricing' or 'SEO & AEO'",
  "intro": "1-2 sentence hook paragraph shown large under the headline",
  "bodyHtml": "the full article body as HTML using only <h2>, <p>, <ul>, <li>, <strong>, <a> tags with Tailwind classes matching this pattern: h2 gets class='text-2xl font-bold text-white mt-10 mb-4', ul gets class='list-disc pl-6 space-y-2', a gets class='text-white underline hover:no-underline'. Do not include <html>, <head>, <body>, or the CTA block.",
  "ctaHeading": "short CTA heading",
  "ctaSub": "one line CTA subtext",
  "ctaLink": "relative path to the most relevant existing page, e.g. ../solutions.html or ../pricing.html",
  "ctaLinkText": "CTA button text"
}`;

  if (decision.type === 'industry') {
    const projectNote = decision.portfolioProject
      ? `A real portfolio project exists for a related industry and MAY be referenced using only these exact facts: ${JSON.stringify(decision.portfolioProject)}`
      : 'No matching portfolio project exists for this industry — do not reference a specific past project by name; speak generally about what this kind of business needs from a website.';
    return `${baseRules}\n\nWrite this post specifically about why businesses in the "${decision.industry}" industry in Kenya need a professional website, what such a site should include, and which Xclusive Tech package (from the pricing in the facts) tends to fit best. ${projectNote}`;
  }

  if (decision.type === 'roundup') {
    const itemsBlock = roundupItems
      .map((it) => `- [${it.source}] "${it.title}" (${it.link}): ${it.summary}`)
      .join('\n');
    return `${baseRules}\n\nWrite a curated "industry roundup" post. Below are recent items from reputable web design/SEO publications (title, link, and a short snippet only — never reproduce full article text). Write original commentary and analysis around 3-5 of these items, framed for a Kenyan small-business audience, with clear attribution and an outbound link to each source you discuss (e.g. "According to Smashing Magazine, ..." with an <a> tag to the link). This must read as original commentary, not a summary or copy.\n\nRECENT ITEMS:\n${itemsBlock}`;
  }

  return `${baseRules}\n\nWrite this post about: "${decision.topic}". Keep it practical and specific to a Kenyan small-business audience.`;
}

async function generateWithRetries(client, facts, decision, roundupItems, maxAttempts = 3) {
  const prompt = buildPrompt(facts, decision, roundupItems);
  let lastError = 'unknown';

  for (let attempt = 1; attempt <= maxAttempts; attempt += 1) {
    const message = await client.messages.create({
      model: MODEL,
      max_tokens: 4096,
      messages: [{ role: 'user', content: prompt }]
    });
    const raw = message.content
      .filter((block) => block.type === 'text')
      .map((block) => block.text)
      .join('\n')
      .trim();

    let parsed;
    try {
      const jsonMatch = raw.match(/\{[\s\S]*\}/);
      parsed = JSON.parse(jsonMatch ? jsonMatch[0] : raw);
    } catch (err) {
      lastError = `Attempt ${attempt}: could not parse JSON from model output`;
      continue;
    }

    const requiredFields = ['title', 'headline', 'description', 'keywords', 'category', 'intro', 'bodyHtml', 'ctaHeading', 'ctaSub', 'ctaLink', 'ctaLinkText'];
    const missing = requiredFields.filter((f) => !parsed[f] || String(parsed[f]).trim() === '');
    if (missing.length > 0) {
      lastError = `Attempt ${attempt}: missing fields: ${missing.join(', ')}`;
      continue;
    }

    const plainText = parsed.bodyHtml.replace(/<[^>]+>/g, ' ');
    if (wordCount(plainText) < MIN_WORDS) {
      lastError = `Attempt ${attempt}: body too short (${wordCount(plainText)} words, need ${MIN_WORDS}+)`;
      continue;
    }
    if (hasPlaceholderText(raw)) {
      lastError = `Attempt ${attempt}: placeholder text detected`;
      continue;
    }
    if (!/href="\.\.\//.test(parsed.bodyHtml)) {
      lastError = `Attempt ${attempt}: no internal link found in body`;
      continue;
    }

    return parsed;
  }

  throw new Error(`Generation failed after ${maxAttempts} attempts. Last error: ${lastError}`);
}

function renderPostHtml(post, slug, dateIso, dateDisplay) {
  const waLink = `https://wa.me/254722753819?text=Hi%20Xclusive%20Tech,%20I%27d%20like%20to%20know%20more%20about%20${encodeURIComponent(post.headline).slice(0, 80)}.`;
  return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${post.title}</title>
    <meta name="description" content="${post.description}">
    <meta name="keywords" content="${post.keywords}">
    <meta name="author" content="Xclusive Tech">
    <meta property="og:title" content="${post.title}">
    <meta property="og:description" content="${post.description}">
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://xclusivetech.co.ke/blog/${slug}.html">
    <meta property="og:image" content="../assets/images/og-preview.png">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="${post.title}">
    <meta name="twitter:description" content="${post.description}">
    <meta name="twitter:image" content="../assets/images/og-preview.png">
    <link rel="canonical" href="https://xclusivetech.co.ke/blog/${slug}.html">

    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="icon" href="../assets/icons/xclusivetech-favicon.svg" type="image/svg+xml">
    <link rel="apple-touch-icon" href="../assets/icons/xclusivetech-favicon.svg">
    <link rel="stylesheet" href="../css/styles.css">

    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "BlogPosting",
      "headline": ${JSON.stringify(post.headline.replace(/&amp;/g, '&'))},
      "description": ${JSON.stringify(post.description)},
      "author": { "@type": "Organization", "name": "Xclusive Tech", "url": "https://xclusivetech.co.ke/" },
      "publisher": { "@id": "https://xclusivetech.co.ke/" },
      "datePublished": "${dateIso}",
      "dateModified": "${dateIso}",
      "mainEntityOfPage": "https://xclusivetech.co.ke/blog/${slug}.html",
      "image": "https://xclusivetech.co.ke/assets/images/og-preview.png"
    }
    </script>
</head>
<body class="bg-gray-900 text-white overflow-x-hidden">

    <!-- Navigation -->
    <nav class="fixed top-0 w-full z-50 bg-gray-900/95 backdrop-blur-lg border-b border-gray-800 transition-all duration-300" id="navbar">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between items-center h-16">
                <a href="../index.html" class="flex items-center gap-2">
                    <img src="../assets/icons/xclusivetech-header-logo.svg" alt="Xclusive Tech logo" class="h-10 w-auto">
                </a>
                <div class="hidden md:flex gap-8">
                    <a href="../index.html" class="nav-link">Home</a>
                    <a href="../about.html" class="nav-link">About</a>
                    <a href="../services.html" class="nav-link">Services</a>
                    <a href="../solutions.html" class="nav-link">Solutions</a>
                    <a href="../pricing.html" class="nav-link">Pricing</a>
                    <a href="../portfolio.html" class="nav-link">Portfolio</a>
                    <a href="index.html" class="nav-link active">Blog</a>
                    <a href="../contact.html" class="nav-link">Contact</a>
                </div>
                <a href="https://wa.me/254722753819?text=Hi%20Xclusive%20Tech,%20I%27d%20like%20a%20free%20quote." target="_blank" class="hidden md:block px-6 py-2 rounded-lg bg-white text-gray-900 hover:bg-gray-100 hover:shadow-lg hover:shadow-white/50 transition-all duration-300 font-medium">Get a Free Quote</a>
                <button id="mobile-menu-btn" class="md:hidden p-2 rounded-lg hover:bg-gray-800 transition-colors" aria-label="Toggle menu">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
                    </svg>
                </button>
            </div>
            <div id="mobile-menu" class="hidden md:hidden pb-4 border-t border-gray-800 mt-4">
                <a href="../index.html" class="block py-2 px-4 rounded-lg hover:bg-gray-800">Home</a>
                <a href="../about.html" class="block py-2 px-4 rounded-lg hover:bg-gray-800">About</a>
                <a href="../services.html" class="block py-2 px-4 rounded-lg hover:bg-gray-800">Services</a>
                <a href="../solutions.html" class="block py-2 px-4 rounded-lg hover:bg-gray-800">Solutions</a>
                <a href="../pricing.html" class="block py-2 px-4 rounded-lg hover:bg-gray-800">Pricing</a>
                <a href="../portfolio.html" class="block py-2 px-4 rounded-lg hover:bg-gray-800">Portfolio</a>
                <a href="index.html" class="block py-2 px-4 rounded-lg hover:bg-gray-800">Blog</a>
                <a href="../contact.html" class="block py-2 px-4 rounded-lg hover:bg-gray-800">Contact</a>
                <a href="https://wa.me/254722753819?text=Hi%20Xclusive%20Tech,%20I%27d%20like%20a%20free%20quote." target="_blank" class="block mt-2 px-6 py-2 rounded-lg bg-white text-gray-900 text-center font-medium">Get a Free Quote</a>
            </div>
        </div>
    </nav>

    <!-- Article -->
    <article class="pt-32 pb-20 px-4 sm:px-6 lg:px-8">
        <div class="max-w-3xl mx-auto">
            <p class="text-sm text-gray-500 uppercase tracking-widest mb-3">${post.category} &bull; ${dateDisplay}</p>
            <h1 class="text-4xl md:text-5xl font-bold leading-tight mb-6">${post.headline}</h1>
            <p class="text-xl text-gray-400 mb-10">${post.intro}</p>

            <div class="prose prose-invert max-w-none space-y-6 text-gray-300 leading-relaxed">
${post.bodyHtml}
                <div class="mt-12 p-8 rounded-2xl bg-white/5 border border-white/10 text-center">
                    <h3 class="text-2xl font-bold mb-3">${post.ctaHeading}</h3>
                    <p class="text-gray-400 mb-6">${post.ctaSub}</p>
                    <div class="flex flex-col sm:flex-row gap-4 justify-center">
                        <a href="${post.ctaLink}" class="inline-block px-6 py-3 rounded-lg bg-white text-gray-900 hover:bg-gray-100 font-medium transition-all duration-300">${post.ctaLinkText}</a>
                        <a href="${waLink}" target="_blank" class="inline-block px-6 py-3 rounded-lg border border-white/20 hover:bg-white/10 font-medium transition-all duration-300">Ask us on WhatsApp</a>
                    </div>
                </div>
            </div>
        </div>
    </article>

    <!-- Footer -->
    <footer class="bg-gray-900 border-t border-gray-800">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
            <div class="grid md:grid-cols-4 gap-8 mb-10">
                <div class="space-y-4">
                    <a href="../index.html" class="flex items-center gap-2">
                        <img src="../assets/icons/xclusivetech-footer-logo.svg" alt="Xclusive Tech logo" class="h-10 w-auto">
                    </a>
                    <p class="text-gray-400">The most affordable, reliable web design &amp; development company serving Thika, Kiambu and Kenya-wide — fast delivery, M-Pesa accepted.</p>
                </div>
                <div class="space-y-4">
                    <h4 class="font-bold">Quick links</h4>
                    <ul class="space-y-2 text-gray-400">
                        <li><a href="../index.html" class="hover:text-white transition-colors">Home</a></li>
                        <li><a href="../about.html" class="hover:text-white transition-colors">About</a></li>
                        <li><a href="../services.html" class="hover:text-white transition-colors">Services</a></li>
                        <li><a href="../solutions.html" class="hover:text-white transition-colors">Solutions</a></li>
                        <li><a href="../portfolio.html" class="hover:text-white transition-colors">Portfolio</a></li>
                        <li><a href="../pricing.html" class="hover:text-white transition-colors">Pricing</a></li>
                        <li><a href="index.html" class="hover:text-white transition-colors">Blog</a></li>
                    </ul>
                </div>
                <div class="space-y-4">
                    <h4 class="font-bold">Services</h4>
                    <ul class="space-y-2 text-gray-400">
                        <li><a href="../services.html" class="hover:text-white transition-colors">Web Design</a></li>
                        <li><a href="../services.html" class="hover:text-white transition-colors">Web Development</a></li>
                        <li><a href="../services.html" class="hover:text-white transition-colors">E-commerce &amp; M-Pesa</a></li>
                        <li><a href="../services.html" class="hover:text-white transition-colors">SEO, GEO &amp; AEO</a></li>
                        <li><a href="../services.html#domain-registration" class="hover:text-white transition-colors">Domain Registration</a></li>
                    </ul>
                </div>
                <div class="space-y-4">
                    <h4 class="font-bold">Contact</h4>
                    <ul class="space-y-3 text-gray-400">
                        <li><a href="mailto:hello@xclusivetech.co.ke" class="hover:text-white transition-colors">hello@xclusivetech.co.ke</a></li>
                        <li><a href="tel:+254722753819" class="hover:text-white transition-colors">+254 722 753 819</a></li>
                        <li><a href="https://share.google/nOqYIkKFu0ynASqVK" target="_blank" class="hover:text-white transition-colors">Find us on Google</a></li>
                        <li><a href="https://www.facebook.com/share/1CcjjbidRp/" target="_blank" class="hover:text-white transition-colors">Facebook</a></li>
                        <li><a href="https://www.instagram.com/xclusivetech.co.ke" target="_blank" class="hover:text-white transition-colors">Instagram</a></li>
                    </ul>
                </div>
            </div>
            <div class="border-t border-gray-800 pt-8 flex flex-col md:flex-row justify-between items-center gap-4 text-gray-400 text-sm">
                <p>&copy; 2026 Xclusive Tech. All Rights Reserved.</p>
                <div class="flex gap-4">
                    <a href="../privacy.html" class="hover:text-white transition-colors">Privacy Policy</a>
                    <a href="../terms.html" class="hover:text-white transition-colors">Terms of Service</a>
                </div>
            </div>
        </div>
    </footer>

    <a href="https://wa.me/254722753819?text=Hi%20Xclusive%20Tech,%20I%27d%20like%20to%20discuss%20my%20project%20needs." target="_blank" class="fixed bottom-6 right-6 w-14 h-14 bg-gradient-to-r from-green-400 to-green-500 hover:from-green-500 hover:to-green-600 text-white rounded-full flex items-center justify-center shadow-lg hover:shadow-green-500/50 transition-all duration-300 hover:scale-110 z-40" title="Chat on WhatsApp">
        <svg class="w-7 h-7" fill="currentColor" viewBox="0 0 24 24" aria-label="Chat on WhatsApp"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.67-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.076 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421-7.403h-.004c-1.025 0-2.031.313-2.891.893L9.9 4.504C10.742 3.74 11.853 3.3 13.05 3.3c2.969 0 5.387 2.418 5.387 5.387 0 1.197-.46 2.307-1.224 3.15l.531 1.465c.592-.689.956-1.586.956-2.615 0-2.206-1.794-4-4-4zm0 0"/></svg>
    </a>

    <script src="../js/main.js"></script>
    <script src="../js/animations.js"></script>
    <script src="../js/navigation.js"></script>
    <script src="../js/offer-popup.js"></script>
</body>
</html>
`;
}

function updateBlogIndex(post, slug, dateDisplay) {
  const indexHtml = fs.readFileSync(BLOG_INDEX_PATH, 'utf8');
  const card = `                <a href="${slug}.html" class="glassmorphism-card p-6 rounded-2xl border border-white/10 hover:border-white/30 transition-all duration-300 flex flex-col">
                    <span class="text-xs uppercase tracking-widest text-gray-500 mb-2">${dateDisplay} &bull; ${post.category}</span>
                    <h2 class="text-xl font-bold mb-2">${post.headline}</h2>
                    <p class="text-gray-400 text-sm flex-grow">${post.description}</p>
                    <span class="text-sm font-medium text-white/80 mt-4">Read more &rarr;</span>
                </a>
`;
  const updated = indexHtml.replace(
    '<!-- POST_CARDS_START -->',
    `<!-- POST_CARDS_START -->\n${card}`
  );
  fs.writeFileSync(BLOG_INDEX_PATH, updated);
}

function updateSitemap(slug, dateIso) {
  let sitemap = fs.readFileSync(SITEMAP_PATH, 'utf8');
  const entry = `
    <!-- Blog: ${slug} -->
    <url>
        <loc>https://www.xclusivetech.co.ke/blog/${slug}.html</loc>
        <lastmod>${dateIso}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.7</priority>
    </url>
`;
  sitemap = sitemap.replace('</urlset>', `${entry}</urlset>`);
  sitemap = sitemap.replace(
    /(<loc>https:\/\/www\.xclusivetech\.co\.ke\/blog\/<\/loc>\s*<lastmod>)[^<]*(<\/lastmod>)/,
    `$1${dateIso}$2`
  );
  fs.writeFileSync(SITEMAP_PATH, sitemap);
}

async function main() {
  const apiKey = process.env.ANTHROPIC_API_KEY;
  if (!apiKey) {
    console.error('ANTHROPIC_API_KEY is not set. Aborting — no post generated, nothing committed.');
    process.exit(1);
  }

  const facts = loadJson(FACTS_PATH);
  const log = loadJson(LOG_PATH);
  const client = new Anthropic({ apiKey });

  const decision = decideTopic(facts, log);
  console.log('Decision:', decision);

  let roundupItems = [];
  if (decision.type === 'roundup') {
    roundupItems = await fetchRoundupItems();
    if (roundupItems.length === 0) {
      console.error('No roundup items could be fetched. Aborting this run rather than publishing an empty roundup.');
      process.exit(1);
    }
  }

  const post = await generateWithRetries(client, facts, decision, roundupItems);

  const now = new Date();
  const dateIso = now.toISOString().slice(0, 10);
  const dateDisplay = now.toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric' });
  const slug = uniqueSlug(slugify(post.title.replace(/\s*\|\s*Xclusive Tech.*/i, '')));

  const html = renderPostHtml(post, slug, dateIso, dateDisplay);
  fs.mkdirSync(BLOG_DIR, { recursive: true });
  fs.writeFileSync(path.join(BLOG_DIR, `${slug}.html`), html);

  updateBlogIndex(post, slug, dateDisplay);
  updateSitemap(slug, dateIso);

  log.posts.unshift({
    slug,
    title: post.headline,
    date: dateIso,
    type: decision.type,
    topic: decision.industry || decision.topic || 'roundup',
    ...(decision.type === 'roundup' ? { sources: roundupItems.map((i) => i.source) } : {})
  });
  saveJson(LOG_PATH, log);

  console.log(`Published: blog/${slug}.html`);
}

main().catch((err) => {
  console.error('Post generation failed:', err.message);
  process.exit(1);
});
