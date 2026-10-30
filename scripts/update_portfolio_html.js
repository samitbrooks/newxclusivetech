const fs = require('fs');
const excludedUrls = new Set(JSON.parse(fs.readFileSync('assets/data/portfolio-excluded.json', 'utf8')).projects.map(project => project.url));
let html = fs.readFileSync('portfolio.html', 'utf8');

// Featured project count is updated from the rendered cards below.

// 2. Insert PataMaps in Healthcare, Wellness & Medical Education
const hcTarget = `<h2 class="text-4xl md:text-5xl font-bold text-gray-900 mt-3 mb-4 leading-tight">Healthcare, Wellness & Medical Education</h2>
                <p class="text-lg text-gray-600 leading-relaxed">Patient- and student-friendly platforms for clinics, medical schools and therapy practices, built for clarity and easy appointment booking.</p>
            </div>
            <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">`;

const patamapsCard = `
                <div class="bg-white rounded-2xl border border-slate-200 shadow-sm hover:shadow-2xl hover:border-emerald-500 hover:-translate-y-2 transition-all duration-300 flex flex-col group overflow-hidden">
                    <div class="relative overflow-hidden aspect-[16/10] bg-slate-50 border-b border-slate-200">
                        <div class="absolute top-0 inset-x-0 h-7 bg-slate-100/95 backdrop-blur flex items-center gap-1.5 px-3 z-10 border-b border-slate-200">
                            <span class="w-2.5 h-2.5 rounded-full bg-red-400"></span>
                            <span class="w-2.5 h-2.5 rounded-full bg-amber-400"></span>
                            <span class="w-2.5 h-2.5 rounded-full bg-emerald-400"></span>
                            <span class="ml-2 text-[10px] text-slate-600 font-mono font-medium truncate bg-white px-2 py-0.5 rounded border border-slate-200/80">patamaps.com</span>
                        </div>
                        <picture>
                            <source srcset="assets/images/portfolio/patamaps.webp" type="image/webp">
                            <img loading="lazy" decoding="async" src="assets/images/portfolio/patamaps.png" alt="PataMaps — Kenya Special Needs Directory & Disability Support Services" width="800" height="500" class="absolute inset-0 w-full h-full object-cover object-top pt-7 scale-100 group-hover:scale-105 transition-transform duration-500 ease-out">
                        </picture>
                    </div>
                    <div class="p-6 space-y-2 bg-white flex-grow flex flex-col justify-between">
                        <div>
                            <span class="inline-block px-2.5 py-0.5 rounded-full text-[11px] font-semibold tracking-wide uppercase bg-emerald-50 text-emerald-700 border border-emerald-200/80 mb-1.5">Accessibility &amp; Healthcare</span>
                            <h3 class="text-lg font-bold text-gray-900 group-hover:text-emerald-600 transition-colors leading-snug"><a href="https://patamaps.com" target="_blank" rel="noopener noreferrer">PataMaps</a></h3>
                            <p class="text-sm text-gray-600 font-medium">Special Needs, Disability &amp; Therapy Directory</p>
                            <p class="text-xs text-slate-500 leading-relaxed pt-1.5"><strong class="text-slate-700">Problem &amp; Solution:</strong> Kenya's first WCAG 2.2 AA compliant directory connecting caregivers with verified occupational therapy, speech pathology, autism clinics, and NCPWD services with county geo-filtering.</p>
                            <div class="flex flex-wrap gap-1.5 pt-2">
                                <span class="px-2 py-0.5 rounded text-[10px] font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200/60">WCAG 2.2 AA</span>
                                <span class="px-2 py-0.5 rounded text-[10px] font-semibold bg-blue-50 text-blue-700 border border-blue-200/60">Special Needs Directory</span>
                                <span class="px-2 py-0.5 rounded text-[10px] font-semibold bg-purple-50 text-purple-700 border border-purple-200/60">NCPWD Verification</span>
                            </div>
                        </div>
                        <div class="pt-3 border-t border-slate-100 flex items-center justify-between">
                            <a href="/blog/case-study-how-we-built-patamaps-accessible-special-needs-directory-kenya" class="text-xs font-semibold text-emerald-600 hover:text-emerald-800 transition-colors inline-flex items-center gap-1">
                                Read Story <span aria-hidden="true">&rarr;</span>
                            </a>
                            <p class="text-xs font-mono font-semibold text-slate-600 group-hover:text-emerald-600 transition-colors flex items-center gap-1">patamaps.com <span aria-hidden="true" class="group-hover:translate-x-1 transition-transform">&nearr;</span></p>
                        </div>
                    </div>
                </div>`;

if (excludedUrls.has('https://patamaps.com')) {
  console.log("Excluded unavailable project: https://patamaps.com");
} else if (html.includes('href="https://patamaps.com"')) {
  console.log("Project already exists: https://patamaps.com");
} else if (!html.includes(hcTarget)) {
  console.error("Healthcare target not found!");
} else {
  html = html.replace(hcTarget, hcTarget + patamapsCard);
  console.log("Inserted PataMaps into Healthcare section");
}

// 3. Insert SAN Group in Energy, Industrial & Trade
const energyTarget = `<h2 class="text-4xl md:text-5xl font-bold text-gray-900 mt-3 mb-4 leading-tight">Energy, Industrial & Trade</h2>
                <p class="text-lg text-gray-600 leading-relaxed">Operationally serious sites for logistics, manufacturing and energy companies where the site has to prove real capacity, not just style.</p>
            </div>
            <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">`;

const sanCard = `
                <div class="bg-white rounded-2xl border border-slate-200 shadow-sm hover:shadow-2xl hover:border-amber-500 hover:-translate-y-2 transition-all duration-300 flex flex-col group overflow-hidden">
                    <div class="relative overflow-hidden aspect-[16/10] bg-slate-50 border-b border-slate-200">
                        <div class="absolute top-0 inset-x-0 h-7 bg-slate-100/95 backdrop-blur flex items-center gap-1.5 px-3 z-10 border-b border-slate-200">
                            <span class="w-2.5 h-2.5 rounded-full bg-red-400"></span>
                            <span class="w-2.5 h-2.5 rounded-full bg-amber-400"></span>
                            <span class="w-2.5 h-2.5 rounded-full bg-emerald-400"></span>
                            <span class="ml-2 text-[10px] text-slate-600 font-mono font-medium truncate bg-white px-2 py-0.5 rounded border border-slate-200/80">sangrouplimited.com</span>
                        </div>
                        <picture>
                            <source srcset="assets/images/portfolio/sangrouplimited.webp" type="image/webp">
                            <img loading="lazy" decoding="async" src="assets/images/portfolio/sangrouplimited.png" alt="SAN Group Limited website — Civil Engineering, Construction & Infrastructure Kenya" width="800" height="500" class="absolute inset-0 w-full h-full object-cover object-top pt-7 scale-100 group-hover:scale-105 transition-transform duration-500 ease-out">
                        </picture>
                    </div>
                    <div class="p-6 space-y-2 bg-white flex-grow flex flex-col justify-between">
                        <div>
                            <span class="inline-block px-2.5 py-0.5 rounded-full text-[11px] font-semibold tracking-wide uppercase bg-amber-50 text-amber-700 border border-amber-200/80 mb-1.5">Civil Engineering &amp; Infrastructure</span>
                            <h3 class="text-lg font-bold text-gray-900 group-hover:text-amber-600 transition-colors leading-snug"><a href="https://sangrouplimited.com" target="_blank" rel="noopener noreferrer">SAN Group Limited</a></h3>
                            <p class="text-sm text-gray-600 font-medium">Infrastructure, Civil Works &amp; Heavy Equipment</p>
                            <p class="text-xs text-slate-500 leading-relaxed pt-1.5"><strong class="text-slate-700">Problem &amp; Solution:</strong> Multi-tier corporate holding portal for SAN Engineering &amp; Construction (SEC), showcasing cross-border roadworks, WASH systems, and heavy machinery chartering for public and private tenders.</p>
                            <div class="flex flex-wrap gap-1.5 pt-2">
                                <span class="px-2 py-0.5 rounded text-[10px] font-semibold bg-amber-50 text-amber-700 border border-amber-200/60">Tender Qualification</span>
                                <span class="px-2 py-0.5 rounded text-[10px] font-semibold bg-slate-100 text-slate-700 border border-slate-200/60">Heavy Equipment</span>
                                <span class="px-2 py-0.5 rounded text-[10px] font-semibold bg-blue-50 text-blue-700 border border-blue-200/60">WASH Systems</span>
                            </div>
                        </div>
                        <div class="pt-3 border-t border-slate-100 flex items-center justify-between">
                            <a href="/blog/case-study-how-we-built-san-group-limited-civil-engineering-infrastructure-portal" class="text-xs font-semibold text-amber-600 hover:text-amber-800 transition-colors inline-flex items-center gap-1">
                                Read Story <span aria-hidden="true">&rarr;</span>
                            </a>
                            <p class="text-xs font-mono font-semibold text-slate-600 group-hover:text-amber-600 transition-colors flex items-center gap-1">sangrouplimited.com <span aria-hidden="true" class="group-hover:translate-x-1 transition-transform">&nearr;</span></p>
                        </div>
                    </div>
                </div>`;

if (excludedUrls.has('https://sangrouplimited.com')) {
  console.log("Excluded unavailable project: https://sangrouplimited.com");
} else if (html.includes('href="https://sangrouplimited.com"')) {
  console.log("Project already exists: https://sangrouplimited.com");
} else if (!html.includes(energyTarget)) {
  console.error("Energy target not found!");
} else {
  html = html.replace(energyTarget, energyTarget + sanCard);
  console.log("Inserted SAN Group into Energy section");
}

// 4. Insert Irene Muendo Isuzu in Automotive
const autoTarget = `<h2 class="text-4xl md:text-5xl font-bold text-gray-900 mt-3 mb-4 leading-tight">Automotive</h2>
                <p class="text-lg text-gray-600 leading-relaxed">Showroom-grade sites for dealerships and automotive logistics operators that turn browsers into showroom visits.</p>
            </div>
            <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">`;

const isuzuCard = `
                <div class="bg-white rounded-2xl border border-slate-200 shadow-sm hover:shadow-2xl hover:border-red-500 hover:-translate-y-2 transition-all duration-300 flex flex-col group overflow-hidden">
                    <div class="relative overflow-hidden aspect-[16/10] bg-slate-50 border-b border-slate-200">
                        <div class="absolute top-0 inset-x-0 h-7 bg-slate-100/95 backdrop-blur flex items-center gap-1.5 px-3 z-10 border-b border-slate-200">
                            <span class="w-2.5 h-2.5 rounded-full bg-red-400"></span>
                            <span class="w-2.5 h-2.5 rounded-full bg-amber-400"></span>
                            <span class="w-2.5 h-2.5 rounded-full bg-emerald-400"></span>
                            <span class="ml-2 text-[10px] text-slate-600 font-mono font-medium truncate bg-white px-2 py-0.5 rounded border border-slate-200/80">irenemuendoisuzu.co.ke</span>
                        </div>
                        <picture>
                            <source srcset="assets/images/portfolio/irenemuendoisuzu.webp" type="image/webp">
                            <img loading="lazy" decoding="async" src="assets/images/portfolio/irenemuendoisuzu.png" alt="Irene Muendo Isuzu Commercial Dealership website — Nairobi Kenya" width="800" height="500" class="absolute inset-0 w-full h-full object-cover object-top pt-7 scale-100 group-hover:scale-105 transition-transform duration-500 ease-out">
                        </picture>
                    </div>
                    <div class="p-6 space-y-2 bg-white flex-grow flex flex-col justify-between">
                        <div>
                            <span class="inline-block px-2.5 py-0.5 rounded-full text-[11px] font-semibold tracking-wide uppercase bg-red-50 text-red-700 border border-red-200/80 mb-1.5">Automotive Dealership</span>
                            <h3 class="text-lg font-bold text-gray-900 group-hover:text-red-600 transition-colors leading-snug"><a href="https://irenemuendoisuzu.co.ke" target="_blank" rel="noopener noreferrer">Irene Muendo Isuzu</a></h3>
                            <p class="text-sm text-gray-600 font-medium">Commercial Trucks, Pickups &amp; Asset Finance</p>
                            <p class="text-xs text-slate-500 leading-relaxed pt-1.5"><strong class="text-slate-700">Problem &amp; Solution:</strong> Digital showroom for an authorized Isuzu sales consultant, featuring interactive N-Series, F-Series, and D-Max models, 95% bank asset finance calculator, and instant VIP WhatsApp routing.</p>
                            <div class="flex flex-wrap gap-1.5 pt-2">
                                <span class="px-2 py-0.5 rounded text-[10px] font-semibold bg-red-50 text-red-700 border border-red-200/60">Asset Financing</span>
                                <span class="px-2 py-0.5 rounded text-[10px] font-semibold bg-slate-100 text-slate-700 border border-slate-200/60">Commercial Fleet</span>
                                <span class="px-2 py-0.5 rounded text-[10px] font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200/60">WhatsApp Lead Engine</span>
                            </div>
                        </div>
                        <div class="pt-3 border-t border-slate-100 flex items-center justify-between">
                            <a href="/blog/case-study-how-we-built-irene-muendo-isuzu-dealership-website-nairobi" class="text-xs font-semibold text-red-600 hover:text-red-800 transition-colors inline-flex items-center gap-1">
                                Read Story <span aria-hidden="true">&rarr;</span>
                            </a>
                            <p class="text-xs font-mono font-semibold text-slate-600 group-hover:text-red-600 transition-colors flex items-center gap-1">irenemuendoisuzu.co.ke <span aria-hidden="true" class="group-hover:translate-x-1 transition-transform">&nearr;</span></p>
                        </div>
                    </div>
                </div>`;

if (excludedUrls.has('https://irenemuendoisuzu.co.ke')) {
  console.log("Excluded unavailable project: https://irenemuendoisuzu.co.ke");
} else if (html.includes('href="https://irenemuendoisuzu.co.ke"')) {
  console.log("Project already exists: https://irenemuendoisuzu.co.ke");
} else if (!html.includes(autoTarget)) {
  console.error("Automotive target not found!");
} else {
  html = html.replace(autoTarget, autoTarget + isuzuCard);
  console.log("Inserted Irene Muendo Isuzu into Automotive section");
}

// 5. Insert Creative Kigen in Retail, Fashion & Consumer Brands
const retailTarget = `<h2 class="text-4xl md:text-5xl font-bold text-gray-900 mt-3 mb-4 leading-tight">Retail, Fashion & Consumer Brands</h2>
                <p class="text-lg text-gray-600 leading-relaxed">Online boutiques, fashion labels and consumer brands built with mobile-first checkout, M-Pesa integration and high-conversion product layouts.</p>
            </div>
            <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">`;

const kigenCard = `
                <div class="bg-white rounded-2xl border border-slate-200 shadow-sm hover:shadow-2xl hover:border-purple-500 hover:-translate-y-2 transition-all duration-300 flex flex-col group overflow-hidden">
                    <div class="relative overflow-hidden aspect-[16/10] bg-slate-50 border-b border-slate-200">
                        <div class="absolute top-0 inset-x-0 h-7 bg-slate-100/95 backdrop-blur flex items-center gap-1.5 px-3 z-10 border-b border-slate-200">
                            <span class="w-2.5 h-2.5 rounded-full bg-red-400"></span>
                            <span class="w-2.5 h-2.5 rounded-full bg-amber-400"></span>
                            <span class="w-2.5 h-2.5 rounded-full bg-emerald-400"></span>
                            <span class="ml-2 text-[10px] text-slate-600 font-mono font-medium truncate bg-white px-2 py-0.5 rounded border border-slate-200/80">creativekigen.com</span>
                        </div>
                        <picture>
                            <source srcset="assets/images/portfolio/creativekigen.webp" type="image/webp">
                            <img loading="lazy" decoding="async" src="assets/images/portfolio/creativekigen.png" alt="Creative Kigen website — Brand Identity, Motion Design & Creative Direction Kenya" width="800" height="500" class="absolute inset-0 w-full h-full object-cover object-top pt-7 scale-100 group-hover:scale-105 transition-transform duration-500 ease-out">
                        </picture>
                    </div>
                    <div class="p-6 space-y-2 bg-white flex-grow flex flex-col justify-between">
                        <div>
                            <span class="inline-block px-2.5 py-0.5 rounded-full text-[11px] font-semibold tracking-wide uppercase bg-purple-50 text-purple-700 border border-purple-200/80 mb-1.5">Creative &amp; Brand Identity</span>
                            <h3 class="text-lg font-bold text-gray-900 group-hover:text-purple-600 transition-colors leading-snug"><a href="https://creativekigen.com" target="_blank" rel="noopener noreferrer">Creative Kigen</a></h3>
                            <p class="text-sm text-gray-600 font-medium">Brand Identity, Visual Systems &amp; Direction</p>
                            <p class="text-xs text-slate-500 leading-relaxed pt-1.5"><strong class="text-slate-700">Problem &amp; Solution:</strong> High-impact minimalist portfolio for Kenya's leading graphic designer and visual director; dynamic layout with fluid gallery filtering and instant direct creative brief booking.</p>
                            <div class="flex flex-wrap gap-1.5 pt-2">
                                <span class="px-2 py-0.5 rounded text-[10px] font-semibold bg-purple-50 text-purple-700 border border-purple-200/60">Brand Identity</span>
                                <span class="px-2 py-0.5 rounded text-[10px] font-semibold bg-pink-50 text-pink-700 border border-pink-200/60">Visual Direction</span>
                                <span class="px-2 py-0.5 rounded text-[10px] font-semibold bg-slate-100 text-slate-700 border border-slate-200/60">Minimalist UX</span>
                            </div>
                        </div>
                        <div class="pt-3 border-t border-slate-100 flex items-center justify-between">
                            <a href="/blog/case-study-how-we-built-creative-kigen-design-portfolio-website" class="text-xs font-semibold text-purple-600 hover:text-purple-800 transition-colors inline-flex items-center gap-1">
                                Read Story <span aria-hidden="true">&rarr;</span>
                            </a>
                            <p class="text-xs font-mono font-semibold text-slate-600 group-hover:text-purple-600 transition-colors flex items-center gap-1">creativekigen.com <span aria-hidden="true" class="group-hover:translate-x-1 transition-transform">&nearr;</span></p>
                        </div>
                    </div>
                </div>`;

if (excludedUrls.has('https://creativekigen.com')) {
  console.log("Excluded unavailable project: https://creativekigen.com");
} else if (html.includes('href="https://creativekigen.com"')) {
  console.log("Project already exists: https://creativekigen.com");
} else if (!html.includes(retailTarget)) {
  console.error("Retail target not found!");
} else {
  html = html.replace(retailTarget, retailTarget + kigenCard);
  console.log("Inserted Creative Kigen into Retail/Brand section");
}

// 6. Insert Elite Designs in Professional & Business Services
const profTarget = `<h2 class="text-4xl md:text-5xl font-bold text-gray-900 mt-3 mb-4 leading-tight">Professional & Business Services</h2>
                <p class="text-lg text-gray-600 leading-relaxed">Credibility-first sites for law firms, engineering consultancies and procurement specialists that win trust before the first call.</p>
            </div>
            <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">`;

const eliteCard = `
                <div class="bg-white rounded-2xl border border-slate-200 shadow-sm hover:shadow-2xl hover:border-blue-500 hover:-translate-y-2 transition-all duration-300 flex flex-col group overflow-hidden">
                    <div class="relative overflow-hidden aspect-[16/10] bg-slate-50 border-b border-slate-200">
                        <div class="absolute top-0 inset-x-0 h-7 bg-slate-100/95 backdrop-blur flex items-center gap-1.5 px-3 z-10 border-b border-slate-200">
                            <span class="w-2.5 h-2.5 rounded-full bg-red-400"></span>
                            <span class="w-2.5 h-2.5 rounded-full bg-amber-400"></span>
                            <span class="w-2.5 h-2.5 rounded-full bg-emerald-400"></span>
                            <span class="ml-2 text-[10px] text-slate-600 font-mono font-medium truncate bg-white px-2 py-0.5 rounded border border-slate-200/80">elitedesigns.co.ke</span>
                        </div>
                        <picture>
                            <source srcset="assets/images/portfolio/elitedesigns.webp" type="image/webp">
                            <img loading="lazy" decoding="async" src="assets/images/portfolio/elitedesigns.png" alt="Elite Designs Kenya website — Corporate Branding & Digital Solutions Nairobi" width="800" height="500" class="absolute inset-0 w-full h-full object-cover object-top pt-7 scale-100 group-hover:scale-105 transition-transform duration-500 ease-out">
                        </picture>
                    </div>
                    <div class="p-6 space-y-2 bg-white flex-grow flex flex-col justify-between">
                        <div>
                            <span class="inline-block px-2.5 py-0.5 rounded-full text-[11px] font-semibold tracking-wide uppercase bg-blue-50 text-blue-700 border border-blue-200/80 mb-1.5">Branding &amp; Digital Solutions</span>
                            <h3 class="text-lg font-bold text-gray-900 group-hover:text-blue-600 transition-colors leading-snug"><a href="https://elitedesigns.co.ke" target="_blank" rel="noopener noreferrer">Elite Designs Kenya</a></h3>
                            <p class="text-sm text-gray-600 font-medium">Corporate Brand Identity &amp; Digital Collateral</p>
                            <p class="text-xs text-slate-500 leading-relaxed pt-1.5"><strong class="text-slate-700">Problem &amp; Solution:</strong> Agency presentation platform for corporate branding and design packages in Nairobi, featuring interactive service tier selector, vector brand asset downloads, and instant project scoping.</p>
                            <div class="flex flex-wrap gap-1.5 pt-2">
                                <span class="px-2 py-0.5 rounded text-[10px] font-semibold bg-blue-50 text-blue-700 border border-blue-200/60">Corporate Branding</span>
                                <span class="px-2 py-0.5 rounded text-[10px] font-semibold bg-indigo-50 text-indigo-700 border border-indigo-200/60">Design Packages</span>
                                <span class="px-2 py-0.5 rounded text-[10px] font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200/60">Nairobi Agency</span>
                            </div>
                        </div>
                        <div class="pt-3 border-t border-slate-100 flex items-center justify-between">
                            <a href="/blog/case-study-how-we-built-elite-designs-corporate-branding-website" class="text-xs font-semibold text-blue-600 hover:text-blue-800 transition-colors inline-flex items-center gap-1">
                                Read Story <span aria-hidden="true">&rarr;</span>
                            </a>
                            <p class="text-xs font-mono font-semibold text-slate-600 group-hover:text-blue-600 transition-colors flex items-center gap-1">elitedesigns.co.ke <span aria-hidden="true" class="group-hover:translate-x-1 transition-transform">&nearr;</span></p>
                        </div>
                    </div>
                </div>`;

if (excludedUrls.has('https://elitedesigns.co.ke')) {
  console.log("Excluded unavailable project: https://elitedesigns.co.ke");
} else if (html.includes('href="https://elitedesigns.co.ke"')) {
  console.log("Project already exists: https://elitedesigns.co.ke");
} else if (!html.includes(profTarget)) {
  console.error("Professional target not found!");
} else {
  html = html.replace(profTarget, profTarget + eliteCard);
  console.log("Inserted Elite Designs into Professional section");
}

const cardCount = (html.match(/class="[^"]*group overflow-hidden[^"]*"/g) || []).length;
html = html.replace(/data-target="\d+"(?=>0<\/span><\/p>\s*<p[^>]*>Featured Projects)/, `data-target="${cardCount}"`);

fs.writeFileSync('portfolio.html' , html, 'utf8');
console.log('portfolio.html updated successfully!');

