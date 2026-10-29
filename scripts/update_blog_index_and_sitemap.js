const fs = require('fs');
const path = require('path');

const blogIndexPath = path.join(__dirname, '../blog/index.html');
const sitemapPath = path.join(__dirname, '../sitemap.xml');

// 1. Update blog/index.html
let blogIndexHtml = fs.readFileSync(blogIndexPath, 'utf8');

const newCaseStudyCards = `
                <!-- Case Study: PataMaps -->
                <a href="/blog/case-study-how-we-built-patamaps-accessible-special-needs-directory-kenya" class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm hover:shadow-xl hover:border-emerald-600 transition-all duration-300 flex flex-col group relative">
                    <span class="absolute top-4 right-4 bg-emerald-600 text-white text-[10px] font-bold uppercase tracking-wider px-2.5 py-1 rounded-full shadow-sm">Client Case Study</span>
                    <div class="w-full h-48 rounded-xl overflow-hidden mb-4 bg-slate-900 border border-slate-200">
                        <picture>
                            <source srcset="../assets/images/blog/case-study-how-we-built-patamaps-accessible-special-needs-directory-kenya.webp" type="image/webp">
                            <img src="../assets/images/blog/case-study-how-we-built-patamaps-accessible-special-needs-directory-kenya.jpg" alt="PataMaps special needs directory Kenya website screenshot" width="600" height="315" loading="lazy" decoding="async" onerror="this.onerror=null; this.src='/assets/images/blog/case-study-how-we-built-patamaps-accessible-special-needs-directory-kenya.jpg';" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300">
                        </picture>
                    </div>
                    <span class="text-xs uppercase tracking-widest text-emerald-600 font-semibold mb-2">Healthcare &amp; Accessibility</span>
                    <h2 class="text-xl font-bold text-gray-900 group-hover:text-emerald-600 transition-colors mb-2">How We Built PataMaps: Engineering Kenya’s Accessible Special Needs &amp; Therapy Directory</h2>
                    <p class="text-gray-600 text-sm flex-grow">Building a WCAG 2.2 AA compliant disability therapy portal with screen-reader optimization, high-contrast UI, verified clinic credentials, and direct WhatsApp consultations.</p>
                    <span class="text-sm font-semibold text-emerald-600 mt-4 flex items-center gap-1 group-hover:translate-x-1 transition-transform">Read case study &rarr;</span>
                </a>

                <!-- Case Study: SAN Group Limited -->
                <a href="/blog/case-study-how-we-built-san-group-limited-civil-engineering-infrastructure-portal" class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm hover:shadow-xl hover:border-amber-600 transition-all duration-300 flex flex-col group relative">
                    <span class="absolute top-4 right-4 bg-amber-600 text-white text-[10px] font-bold uppercase tracking-wider px-2.5 py-1 rounded-full shadow-sm">Client Case Study</span>
                    <div class="w-full h-48 rounded-xl overflow-hidden mb-4 bg-slate-900 border border-slate-200">
                        <picture>
                            <source srcset="../assets/images/blog/case-study-how-we-built-san-group-limited-civil-engineering-infrastructure-portal.webp" type="image/webp">
                            <img src="../assets/images/blog/case-study-how-we-built-san-group-limited-civil-engineering-infrastructure-portal.jpg" alt="SAN Group Limited civil engineering infrastructure portal screenshot" width="600" height="315" loading="lazy" decoding="async" onerror="this.onerror=null; this.src='/assets/images/blog/case-study-how-we-built-san-group-limited-civil-engineering-infrastructure-portal.jpg';" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300">
                        </picture>
                    </div>
                    <span class="text-xs uppercase tracking-widest text-amber-600 font-semibold mb-2">Civil Engineering &amp; Infrastructure</span>
                    <h2 class="text-xl font-bold text-gray-900 group-hover:text-amber-600 transition-colors mb-2">How We Built SAN Group Limited: Engineering a High-Authority Civil Engineering &amp; Infrastructure Portal</h2>
                    <p class="text-gray-600 text-sm flex-grow">Inside the engineering of a heavyweight contractor portal: KeNHA/KURA tender showcase, heavy equipment fleet catalogs, and institutional credibility for multi-million shilling civil tenders.</p>
                    <span class="text-sm font-semibold text-amber-600 mt-4 flex items-center gap-1 group-hover:translate-x-1 transition-transform">Read case study &rarr;</span>
                </a>

                <!-- Case Study: Irene Muendo Isuzu -->
                <a href="/blog/case-study-how-we-built-irene-muendo-isuzu-dealership-website-nairobi" class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm hover:shadow-xl hover:border-red-600 transition-all duration-300 flex flex-col group relative">
                    <span class="absolute top-4 right-4 bg-red-600 text-white text-[10px] font-bold uppercase tracking-wider px-2.5 py-1 rounded-full shadow-sm">Client Case Study</span>
                    <div class="w-full h-48 rounded-xl overflow-hidden mb-4 bg-slate-900 border border-slate-200">
                        <picture>
                            <source srcset="../assets/images/blog/case-study-how-we-built-irene-muendo-isuzu-dealership-website-nairobi.webp" type="image/webp">
                            <img src="../assets/images/blog/case-study-how-we-built-irene-muendo-isuzu-dealership-website-nairobi.jpg" alt="Irene Muendo Isuzu commercial truck dealership website screenshot" width="600" height="315" loading="lazy" decoding="async" onerror="this.onerror=null; this.src='/assets/images/blog/case-study-how-we-built-irene-muendo-isuzu-dealership-website-nairobi.jpg';" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300">
                        </picture>
                    </div>
                    <span class="text-xs uppercase tracking-widest text-red-600 font-semibold mb-2">Automotive &amp; Commercial Dealership</span>
                    <h2 class="text-xl font-bold text-gray-900 group-hover:text-red-600 transition-colors mb-2">How We Built Irene Muendo Isuzu: Engineering a High-Converting Commercial Vehicle Dealership Portal in Nairobi</h2>
                    <p class="text-gray-600 text-sm flex-grow">Architecting a digital commercial showroom: 95% bank asset finance calculators, commercial truck specification sheets (N-Series, F-Series, Pickups), and instant WhatsApp trade-in funnels.</p>
                    <span class="text-sm font-semibold text-red-600 mt-4 flex items-center gap-1 group-hover:translate-x-1 transition-transform">Read case study &rarr;</span>
                </a>

                <!-- Case Study: Creative Kigen -->
                <a href="/blog/case-study-how-we-built-creative-kigen-design-portfolio-website" class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm hover:shadow-xl hover:border-purple-600 transition-all duration-300 flex flex-col group relative">
                    <span class="absolute top-4 right-4 bg-purple-600 text-white text-[10px] font-bold uppercase tracking-wider px-2.5 py-1 rounded-full shadow-sm">Client Case Study</span>
                    <div class="w-full h-48 rounded-xl overflow-hidden mb-4 bg-slate-900 border border-slate-200">
                        <picture>
                            <source srcset="../assets/images/blog/case-study-how-we-built-creative-kigen-design-portfolio-website.webp" type="image/webp">
                            <img src="../assets/images/blog/case-study-how-we-built-creative-kigen-design-portfolio-website.jpg" alt="Creative Kigen brand identity design portfolio screenshot" width="600" height="315" loading="lazy" decoding="async" onerror="this.onerror=null; this.src='/assets/images/blog/case-study-how-we-built-creative-kigen-design-portfolio-website.jpg';" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300">
                        </picture>
                    </div>
                    <span class="text-xs uppercase tracking-widest text-purple-600 font-semibold mb-2">Design Studio &amp; Visual Identity</span>
                    <h2 class="text-xl font-bold text-gray-900 group-hover:text-purple-600 transition-colors mb-2">How We Built Creative Kigen: Crafting an Ultra-Fast Brand Identity &amp; Motion Design Portfolio Website</h2>
                    <p class="text-gray-600 text-sm flex-grow">Engineering an immersive visual design portfolio: lazy-loaded WebP brand case studies, motion showcase frames, sub-second load times, and frictionless client booking channels.</p>
                    <span class="text-sm font-semibold text-purple-600 mt-4 flex items-center gap-1 group-hover:translate-x-1 transition-transform">Read case study &rarr;</span>
                </a>

                <!-- Case Study: Elite Designs Kenya -->
                <a href="/blog/case-study-how-we-built-elite-designs-corporate-branding-website" class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm hover:shadow-xl hover:border-blue-600 transition-all duration-300 flex flex-col group relative">
                    <span class="absolute top-4 right-4 bg-blue-600 text-white text-[10px] font-bold uppercase tracking-wider px-2.5 py-1 rounded-full shadow-sm">Client Case Study</span>
                    <div class="w-full h-48 rounded-xl overflow-hidden mb-4 bg-slate-900 border border-slate-200">
                        <picture>
                            <source srcset="../assets/images/blog/case-study-how-we-built-elite-designs-corporate-branding-website.webp" type="image/webp">
                            <img src="../assets/images/blog/case-study-how-we-built-elite-designs-corporate-branding-website.jpg" alt="Elite Designs corporate branding website screenshot" width="600" height="315" loading="lazy" decoding="async" onerror="this.onerror=null; this.src='/assets/images/blog/case-study-how-we-built-elite-designs-corporate-branding-website.jpg';" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300">
                        </picture>
                    </div>
                    <span class="text-xs uppercase tracking-widest text-blue-600 font-semibold mb-2">Creative Agency &amp; Branding</span>
                    <h2 class="text-xl font-bold text-gray-900 group-hover:text-blue-600 transition-colors mb-2">How We Built Elite Designs: Engineering a High-Converting Corporate Branding Agency Website</h2>
                    <p class="text-gray-600 text-sm flex-grow">Transforming graphic design services into tangible client value: tiered corporate startup packages, downloadable brand decks, interactive quote requests, and instant M-Pesa retainer workflows.</p>
                    <span class="text-sm font-semibold text-blue-600 mt-4 flex items-center gap-1 group-hover:translate-x-1 transition-transform">Read case study &rarr;</span>
                </a>
`;

if (!blogIndexHtml.includes('case-study-how-we-built-patamaps')) {
    blogIndexHtml = blogIndexHtml.replace(
        '<div id="post-grid" class="grid sm:grid-cols-2 lg:grid-cols-3 gap-8">\n                <!-- Case Study 1: OPSOK -->',
        `<div id="post-grid" class="grid sm:grid-cols-2 lg:grid-cols-3 gap-8">${newCaseStudyCards}\n                <!-- Case Study 1: OPSOK -->`
    );
    fs.writeFileSync(blogIndexPath, blogIndexHtml, 'utf8');
    console.log('Updated blog/index.html with 5 new case study cards!');
} else {
    console.log('blog/index.html already contains new case studies.');
}

// 2. Update sitemap.xml
let sitemapXml = fs.readFileSync(sitemapPath, 'utf8');
const newSitemapEntries = `
    <url>
        <loc>https://www.xclusivetech.co.ke/blog/case-study-how-we-built-patamaps-accessible-special-needs-directory-kenya</loc>
        <lastmod>2026-10-29</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.85</priority>
    </url>

    <url>
        <loc>https://www.xclusivetech.co.ke/blog/case-study-how-we-built-san-group-limited-civil-engineering-infrastructure-portal</loc>
        <lastmod>2026-10-29</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.85</priority>
    </url>

    <url>
        <loc>https://www.xclusivetech.co.ke/blog/case-study-how-we-built-irene-muendo-isuzu-dealership-website-nairobi</loc>
        <lastmod>2026-10-29</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.85</priority>
    </url>

    <url>
        <loc>https://www.xclusivetech.co.ke/blog/case-study-how-we-built-creative-kigen-design-portfolio-website</loc>
        <lastmod>2026-10-29</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.85</priority>
    </url>

    <url>
        <loc>https://www.xclusivetech.co.ke/blog/case-study-how-we-built-elite-designs-corporate-branding-website</loc>
        <lastmod>2026-10-29</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.85</priority>
    </url>
`;

if (!sitemapXml.includes('case-study-how-we-built-patamaps')) {
    sitemapXml = sitemapXml.replace(
        '<loc>https://www.xclusivetech.co.ke/blog/case-study-how-i-built-opsok-medical-website-kenya</loc>',
        `${newSitemapEntries.trim()}\n\n    <url>\n        <loc>https://www.xclusivetech.co.ke/blog/case-study-how-i-built-opsok-medical-website-kenya</loc>`
    );
    // Remove the extra <url> tag duplication if any, or cleanly write
    // Let's replace precisely before the opsok entry
    fs.writeFileSync(sitemapPath, sitemapXml, 'utf8');
    console.log('Updated sitemap.xml with 5 new case study URLs!');
} else {
    console.log('sitemap.xml already contains new case studies.');
}

