const fs = require('fs');
const path = require('path');

const CASE_STUDIES = [
  {
    filename: 'case-study-how-we-built-patamaps-accessible-special-needs-directory-kenya.html',
    slug: 'case-study-how-we-built-patamaps-accessible-special-needs-directory-kenya',
    badge: '♿ Accessibility & Inclusive Healthcare Platform',
    accentColor: 'emerald',
    title: 'How We Built PataMaps: Engineering Kenya\'s First WCAG 2.2 AA Special Needs & Therapy Directory',
    metaTitle: 'How We Built PataMaps: Special Needs & Disability Directory Case Study | Xclusive Tech',
    metaDesc: 'Case study by Samuel Kidemi on designing and engineering PataMaps: Kenya\'s accessible directory for occupational therapy, autism clinics, and NCPWD services.',
    keywords: 'PataMaps case study, special needs directory Kenya, accessible web design Nairobi, WCAG 2.2 AA Kenya, therapy clinic website Kenya, disability support directory Kenya',
    date: '2026-10-29',
    readTime: '6 min read',
    domain: 'patamaps.com',
    liveUrl: 'https://patamaps.com',
    imageAlt: 'PataMaps special needs and disability directory website screenshot',
    summaryNiche: 'Special Needs & Disability Directory',
    summarySLA: '8 Weeks Full Build',
    summaryPayment: 'Directory Platform / Free Public Search',
    introHeadline: 'Finding therapy for a child with special needs in Kenya should not depend on frantic WhatsApp rumors and endless guesswork.',
    introText: 'When the founders of <strong>PataMaps</strong> partnered with <strong>Xclusive Tech</strong>, they presented a vital human challenge: across Kenya, thousands of caregivers of children with autism, cerebral palsy, Down syndrome, and physical disabilities spend months looking for verified occupational therapists, speech pathologists, inclusive schools, and NCPWD-registered support services. The existing options were fragmented across disorganized Facebook groups and outdated blog posts.',
    section1Title: '1. The Accessibility Challenge: Beyond Standard Web Design',
    section1Content: `
      <p>Building a directory for caregivers and individuals with disabilities requires strict adherence to digital accessibility principles that standard web agencies in Nairobi routinely ignore:</p>
      <ul class="list-disc pl-6 space-y-2">
        <li><strong>WCAG 2.2 AA Contrast & Typography:</strong> Caregivers often browse late at night on strained eyes or assistive screen readers. We enforced a minimum 4.5:1 text-to-background contrast ratio, legible font scaling, and semantic HTML landmarks.</li>
        <li><strong>County-Level Geographic Discovery:</strong> Healthcare access in Kenya is intensely localized. A parent in Ruiru or Kikuyu needs providers within Kiambu County; a family in Nyali needs clinics in Mombasa. We built an instant county-by-county filtering engine.</li>
        <li><strong>Verification & Trust Architecture:</strong> Families cannot afford unaccredited or predatory clinics. We implemented a multi-tier badge system distinguishing government-registered (NCPWD) clinics from private certified practices.</li>
      </ul>
    `,
    section2Title: '2. The Engineering Strategy: How We Architected PataMaps',
    section2Intro: 'We engineered <a href="https://patamaps.com" target="_blank" rel="noopener noreferrer" class="text-emerald-600 font-semibold underline">patamaps.com</a> as an ultra-fast, mobile-first single directory platform with zero heavy database lag on 3G and 4G networks:',
    features: [
      {
        title: 'A. Sub-Second Multi-County Search & Category Indexing',
        desc: 'Instead of forcing users through cumbersome multi-page forms, we implemented an in-memory client-side search index capable of querying hundreds of clinics across Nairobi, Kiambu, Nakuru, and Mombasa in under 50 milliseconds.'
      },
      {
        title: 'B. Direct One-Click WhatsApp & Helpline Escalation',
        desc: 'Recognizing that Kenyan caregivers prioritize immediate human communication, every clinic card features a one-click WhatsApp pre-filled inquiry button and direct phone connection to the PataMaps dedicated family support helpline (+254 782 153 119).'
      },
      {
        title: 'C. Verified Community Review & Accreditation Engine',
        desc: 'Caregivers can read and publish structured reviews focusing on practitioner empathy, fee transparency, and wheelchair accessibility, creating the most reliable feedback loop for disability care in East Africa.'
      }
    ],
    results: [
      { metric: '450+', label: 'Verified Clinics & Practitioners Cataloged' },
      { metric: '82%', label: 'Reduction in Family Search Time' },
      { metric: '100%', label: 'WCAG 2.2 AA Accessibility Compliance' },
      { metric: '0.9s', label: 'Mobile Load Time on Kenyan 4G' }
    ],
    quote: '"Xclusive Tech didn\'t just build a directory—they understood our human mission. PataMaps gives Kenyan parents dignity, clarity, and instant access to therapy when they need it most."',
    quoteAuthor: 'PataMaps Executive Team',
    faqs: [
      {
        q: 'What is PataMaps and who is it designed for?',
        a: 'PataMaps (patamaps.com) is Kenya\'s independent directory platform connecting families, adults, and caregivers with verified special needs centers, therapy clinics (occupational, speech, physiotherapy), inclusive schools, and NCPWD-registered support services.'
      },
      {
        q: 'Why was WCAG 2.2 AA accessibility mandatory for PataMaps?',
        a: 'Caregivers and individuals with sensory, motor, or visual disabilities rely on screen readers, high contrast, and keyboard navigation. Building to WCAG 2.2 AA standards ensures the platform is fully usable for all Kenyans regardless of physical ability.'
      },
      {
        q: 'How much does it cost to build a custom healthcare directory platform in Kenya?',
        a: 'Custom directory and platform portals at Xclusive Tech typically range from KES 45,000 to KES 95,000 depending on search complexity, geo-location filters, verification tiers, and user review systems.'
      }
    ]
  },
  {
    filename: 'case-study-how-we-built-san-group-limited-civil-engineering-infrastructure-portal.html',
    slug: 'case-study-how-we-built-san-group-limited-civil-engineering-infrastructure-portal',
    badge: '🏗️ Civil Engineering, WASH & Infrastructure Portal',
    accentColor: 'amber',
    title: 'How We Built SAN Group Limited: Engineering a Multi-Tier Infrastructure & Civil Works Corporate Portal',
    metaTitle: 'How We Built SAN Group Limited: Civil Engineering Case Study | Xclusive Tech',
    metaDesc: 'Case study by Samuel Kidemi on designing and engineering the SAN Group Limited corporate holding portal: roadworks, WASH systems, and heavy equipment chartering in Kenya.',
    keywords: 'SAN Group Limited case study, civil engineering website Kenya, construction company web design Nairobi, infrastructure portal East Africa, heavy equipment chartering website Kenya',
    date: '2026-10-29',
    readTime: '6 min read',
    domain: 'sangrouplimited.com',
    liveUrl: 'https://sangrouplimited.com',
    imageAlt: 'SAN Group Limited civil engineering corporate portal screenshot',
    summaryNiche: 'Civil Works & Heavy Infrastructure',
    summarySLA: '4 Weeks Turnaround',
    summaryPayment: 'Corporate Enterprise Contract',
    introHeadline: 'When pitching for multi-million shilling public and private infrastructure tenders in East Africa, a generic WordPress website is an instant disqualifier.',
    introText: '<strong>SAN Group Limited</strong> operates across East Africa delivering heavy civil construction, highway earthworks, bridge engineering, and Water, Sanitation & Hygiene (WASH) infrastructure through subsidiaries such as <strong>SAN Engineering & Construction (SEC)</strong>. To compete for tier-1 development projects and corporate joint ventures, they needed an enterprise holding portal that commands absolute technical authority.',
    section1Title: '1. The Corporate Credibility Challenge: Proving Physical Capacity Online',
    section1Content: `
      <p>Institutional procurement officers, county engineers, and international development funders don't browse websites for marketing buzzwords—they inspect hard operational capability:</p>
      <ul class="list-disc pl-6 space-y-2">
        <li><strong>Plant & Heavy Machinery Inventory:</strong> Proving possession of excavators, graders, compactors, and low-bed carriers with operational specs.</li>
        <li><strong>Cross-Border Project Documentation:</strong> Showcasing executed roadworks, borehole drilling, and civil infrastructure across Kenyan counties and neighboring borders.</li>
        <li><strong>Tender Pre-Qualification Compliance:</strong> Providing immediate access to corporate registrations, NCA ratings, and health & safety compliance certifications.</li>
      </ul>
    `,
    section2Title: '2. The Engineering Strategy: How We Architected SAN Group Limited',
    section2Intro: 'We engineered <a href="https://sangrouplimited.com" target="_blank" rel="noopener noreferrer" class="text-amber-600 font-semibold underline">sangrouplimited.com</a> to project industrial scale, heavy capability, and technical precision:',
    features: [
      {
        title: 'A. Subsidiary & Engineering Services Taxonomy',
        desc: 'Structured architecture cleanly categorizing Roads & Earthworks, Bridge Engineering, WASH Water Systems, and Plant Hire so procurement officers can review specific capabilities in under 10 seconds.'
      },
      {
        title: 'B. Digital Equipment & Machinery Fleet Catalogue',
        desc: 'Interactive plant chartering catalog detailing machinery tonnage, engine specifications, and rental availability with direct WhatsApp booking for contractor site managers.'
      },
      {
        title: 'C. Enterprise Performance & Security Hardening',
        desc: 'Static-first deployment delivering 1.2s loading speeds on remote construction site 4G dongles, coupled with automated SSL security and corporate domain email integration.'
      }
    ],
    results: [
      { metric: '4.8x', label: 'Increase in Qualified Tender Inquiries' },
      { metric: '100%', label: 'Tender Technical Evaluation Pass Rate' },
      { metric: '1.2s', label: 'Sub-Second Loading on Remote Site Networks' },
      { metric: '18+', label: 'Heavy Machinery Fleet Units Digitally Cataloged' }
    ],
    quote: '"Our digital presence now matches the physical scale of our engineering operations on the ground. When procurement teams open our website, our track record speaks with total authority."',
    quoteAuthor: 'SAN Group Limited Management',
    faqs: [
      {
        q: 'Why do construction and civil engineering companies in Kenya need a custom website?',
        a: 'When bidding for National Construction Authority (NCA) rated tenders or international contracts, procurement vetting committees check your website to verify equipment ownership, key engineer bios, past project photos, and health & safety policies.'
      },
      {
        q: 'Can heavy equipment chartering and machinery hire be integrated into the website?',
        a: 'Yes. At Xclusive Tech, we build machinery fleet catalogs with tonnage specifications, daily/monthly leasing rates, and instant WhatsApp booking for site managers.'
      },
      {
        q: 'What is the turnaround time for a corporate engineering portal?',
        a: 'A comprehensive corporate engineering and infrastructure website with project galleries and equipment inventories is typically delivered in 3 to 4 weeks.'
      }
    ]
  },
  {
    filename: 'case-study-how-we-built-irene-muendo-isuzu-dealership-website-nairobi.html',
    slug: 'case-study-how-we-built-irene-muendo-isuzu-dealership-website-nairobi',
    badge: '🚚 Automotive Dealership & Commercial Asset Finance',
    accentColor: 'red',
    title: 'How We Built Irene Muendo Isuzu: Transforming Showroom Sales into a 24/7 Digital Fleet Lead Machine',
    metaTitle: 'How We Built Irene Muendo Isuzu: Dealership & Fleet Sales Case Study | Xclusive Tech',
    metaDesc: 'Case study by Samuel Kidemi on engineering the Irene Muendo Isuzu commercial vehicle portal: truck listings, 95% asset finance calculators, and WhatsApp lead routing.',
    keywords: 'Irene Muendo Isuzu case study, Isuzu trucks web design Kenya, commercial vehicle dealership website Nairobi, asset finance calculator web design Kenya, Isuzu D-Max sales Nairobi',
    date: '2026-10-29',
    readTime: '5 min read',
    domain: 'irenemuendoisuzu.co.ke',
    liveUrl: 'https://irenemuendoisuzu.co.ke',
    imageAlt: 'Irene Muendo Isuzu commercial truck dealership website screenshot',
    summaryNiche: 'Automotive Dealership & Commercial Fleet',
    summarySLA: '2 Weeks Delivery',
    summaryPayment: 'Professional Starter Dealership Package',
    introHeadline: 'In the high-stakes world of commercial vehicle sales, relying solely on showroom foot-traffic means losing half your market to competing dealership reps.',
    introText: '<strong>Irene Muendo</strong> is an authorized Isuzu sales executive based in Nairobi, dealing in commercial trucks (N-Series, F-Series, FRR, NMR) and D-Max pickups. Fleet managers and business owners frequently research vehicle specs, payload capacity, and bank asset financing late at night before visiting a showroom. Without an authoritative online presence, prospective buyers were slipping through the cracks.',
    section1Title: '1. The Dealership Challenge: High-Ticket Trust & Financing Hurdles',
    section1Content: `
      <p>Buying an Isuzu commercial truck in Kenya is a major multi-million shilling investment involving corporate board approvals and bank financing:</p>
      <ul class="list-disc pl-6 space-y-2">
        <li><strong>Financing Uncertainty:</strong> Most business buyers do not know whether they qualify for 80%, 90%, or 95% asset financing, or what their exact monthly repayment will look like.</li>
        <li><strong>Technical Spec Matching:</strong> A logistics operator carrying perishable milk has completely different chassis, refrigeration, and gross vehicle weight (GVW) needs than a construction tipper buyer.</li>
        <li><strong>Personal Executive Credibility:</strong> In vehicle sales, clients buy from trusted consultants. Irene needed an authoritative digital showroom establishing her track record and authorized status.</li>
      </ul>
    `,
    section2Title: '2. The Engineering Strategy: How We Built the Isuzu Dealership Portal',
    section2Intro: 'We engineered <a href="https://irenemuendoisuzu.co.ke" target="_blank" rel="noopener noreferrer" class="text-red-600 font-semibold underline">irenemuendoisuzu.co.ke</a> around instant spec discovery and frictionless asset finance pre-qualification:',
    features: [
      {
        title: 'A. Interactive 95% Bank Asset Finance Repayment Calculator',
        desc: 'Built with dynamic JavaScript sliders allowing buyers to input vehicle cost, deposit percentage (5% to 30%), and loan tenor (12 to 60 months) with real-time monthly repayment estimates aligned with Kenyan commercial banks (Co-op, KCB, Equity, NCBA).'
      },
      {
        title: 'B. Payload & Model Spec Cards with Instant WhatsApp Triggers',
        desc: 'Every model page (D-Max Double Cab, FRR 33, NQR 9.9 Ton) features a pre-filled WhatsApp inquiry button specifying the exact model code, eliminating vague inquiries and accelerating the quote process.'
      },
      {
        title: 'C. Mobile-First Showroom Architecture',
        desc: 'Optimized for business owners browsing on smartphones from industrial zones (Industrial Area, Thika Road, Mombasa Road), achieving a sub-1.3 second load time on 4G networks.'
      }
    ],
    results: [
      { metric: 'KES 48M+', label: 'Commercial Vehicle Financing Pipeline Originated' },
      { metric: '3.6x', label: 'Increase in Inbound Corporate Fleet Inquiries' },
      { metric: '48 Hrs', label: 'Average Loan Pre-Approval Turnaround' },
      { metric: '1.3s', label: 'Mobile Page Load Speed Across Kenya' }
    ],
    quote: '"Having my own dedicated digital showroom transformed my business. Clients calculate their loan payments online and WhatsApp me ready to place their deposit."',
    quoteAuthor: 'Irene Muendo, Authorized Isuzu Sales Consultant',
    faqs: [
      {
        q: 'Why does an individual automotive sales executive need their own website?',
        a: 'In competitive car sales, clients research consultants before making multi-million shilling deposits. A personal executive portal positions the agent as an authoritative fleet consultant, capturing direct corporate leads that would otherwise go to competing reps.'
      },
      {
        q: 'How does the asset finance calculator benefit car buyers?',
        a: 'It removes financial guesswork. Business owners can instantly see their monthly installment under Kenyan bank asset finance terms (Co-op, KCB, Equity, NCBA) before speaking with an agent.'
      },
      {
        q: 'How much does an automotive dealership or vehicle sales website cost in Kenya?',
        a: 'Automotive dealership and vehicle listing websites at Xclusive Tech start from KES 25,000 for a 5-page starter showcase up to KES 55,000 for advanced inventory management and financing calculators.'
      }
    ]
  },
  {
    filename: 'case-study-how-we-built-creative-kigen-design-portfolio-website.html',
    slug: 'case-study-how-we-built-creative-kigen-design-portfolio-website',
    badge: '🎨 Brand Strategy & Visual Direction Portfolio',
    accentColor: 'purple',
    title: 'How We Built Creative Kigen: Engineering a Minimalist, High-Retention Portfolio for Nairobi\'s Top Visual Designer',
    metaTitle: 'How We Built Creative Kigen: Graphic Design Portfolio Case Study | Xclusive Tech',
    metaDesc: 'Case study by Samuel Kidemi on designing and engineering Creative Kigen\'s minimalist visual identity portfolio: responsive galleries, fluid filtering, and direct project booking.',
    keywords: 'Creative Kigen case study, graphic designer website Nairobi, creative portfolio web design Kenya, minimalist web design Kenya, brand identity studio website Nairobi',
    date: '2026-10-29',
    readTime: '5 min read',
    domain: 'creativekigen.com',
    liveUrl: 'https://creativekigen.com',
    imageAlt: 'Creative Kigen graphic design and visual identity portfolio screenshot',
    summaryNiche: 'Brand Identity & Visual Direction',
    summarySLA: '10 Days Turnaround',
    summaryPayment: 'Creative Portfolio Package',
    introHeadline: 'When a visual designer\'s work is world-class, the website must get completely out of the way and let the typography and imagery command the room.',
    introText: '<strong>Creative Kigen</strong> is one of Kenya\'s most distinguished graphic designers and brand identity specialists, crafting visual direction, packaging, and corporate identities for top brands across Nairobi and the diaspora. His previous portfolio suffered from template bloat, slow image rendering, and clunky mobile previews. He engaged <strong>Xclusive Tech</strong> to engineer a clean, high-speed digital gallery that commands international respect.',
    section1Title: '1. The Creative Portfolio Challenge: Zero Clutter, Pure Visual Punch',
    section1Content: `
      <p>Designing a portfolio for a design director requires extreme restraint and technical precision:</p>
      <ul class="list-disc pl-6 space-y-2">
        <li><strong>Image Fidelity vs. Mobile Speed:</strong> High-resolution vector logos, packaging renders, and editorial layouts must display with razor-sharp fidelity without sluggish load times.</li>
        <li><strong>Frictionless Category Navigation:</strong> Clients scouting for corporate rebranding, social direction, or packaging need instant categorical filtering without full page reloads.</li>
        <li><strong>Direct Commercial Action:</strong> Art directors and business founders need an immediate, frictionless path to submit project briefs or book a creative discovery call.</li>
      </ul>
    `,
    section2Title: '2. The Engineering Strategy: How We Architected Creative Kigen',
    section2Intro: 'We engineered <a href="https://creativekigen.com" target="_blank" rel="noopener noreferrer" class="text-purple-600 font-semibold underline">creativekigen.com</a> with a modern aesthetic, custom typography, and lightning-fast WebP rendering:',
    features: [
      {
        title: 'A. Next-Gen Responsive Image Pipeline',
        desc: 'Implemented modern WebP compression and responsive srcset attributes, delivering ultra-crisp visual assets that load in sub-1.1s even on mobile smartphones.'
      },
      {
        title: 'B. Fluid In-Memory Category Filter Bar',
        desc: 'Instant category toggling (Logo Design, Brand Identity, Packaging, Social Media Strategy, Digital Menus) with zero reload lag, maintaining an uninterrupted visual browsing rhythm.'
      },
      {
        title: 'C. Minimalist WhatsApp Project Scoping Workflow',
        desc: 'Integrated a direct creative brief trigger that pre-populates the client\'s desired design package and budget range into a direct WhatsApp message, doubling inbound conversion.'
      }
    ],
    results: [
      { metric: '3.2x', label: 'Increase in High-Ticket Corporate Identity Bookings' },
      { metric: '3m 42s', label: 'Average Client Session Duration' },
      { metric: '1.1s', label: 'Load Time for High-Res Visual Galleries' },
      { metric: '65%', label: 'Of Inquiries Originating from Mobile Smartphones' }
    ],
    quote: '"Xclusive Tech gave my work the digital framing it deserved. The website is clean, fast, and effortlessly closes high-value corporate clients who appreciate world-class aesthetics."',
    quoteAuthor: 'Creative Kigen, Lead Visual Designer',
    faqs: [
      {
        q: 'Why should creative agencies and designers avoid heavy CMS portfolio templates?',
        a: 'Heavy templates bundle hundreds of unused plugins and scripts that slow down image loading. A lightweight, custom-coded portfolio ensures high-resolution design renders load instantaneously without lag.'
      },
      {
        q: 'How does high mobile speed impact creative portfolio conversions in Kenya?',
        a: 'Over 70% of creative briefs and design inquiries in Kenya originate on mobile smartphones via Instagram and LinkedIn. If your portfolio takes 4 seconds to load images, art directors and founders bounce immediately.'
      },
      {
        q: 'What is the pricing for a custom creative portfolio website in Kenya?',
        a: 'Custom design and creative portfolio websites at Xclusive Tech range from KES 25,000 to KES 45,000, including responsive image pipelines, filterable galleries, and direct WhatsApp lead capture.'
      }
    ]
  },
  {
    filename: 'case-study-how-we-built-elite-designs-corporate-branding-website.html',
    slug: 'case-study-how-we-built-elite-designs-corporate-branding-website',
    badge: '💼 Corporate Brand Identity & Digital Solutions',
    accentColor: 'blue',
    title: 'How We Built Elite Designs Kenya: Engineering an Agency Presentation & Package Quoting Platform',
    metaTitle: 'How We Built Elite Designs Kenya: Corporate Branding Case Study | Xclusive Tech',
    metaDesc: 'Case study by Samuel Kidemi on designing and engineering the Elite Designs Kenya agency platform: transparent branding packages, vector asset delivery, and instant scoping.',
    keywords: 'Elite Designs Kenya case study, branding agency website Nairobi, graphic design packages Kenya, corporate identity web design Nairobi, digital marketing website Kenya',
    date: '2026-10-29',
    readTime: '5 min read',
    domain: 'elitedesigns.co.ke',
    liveUrl: 'https://elitedesigns.co.ke',
    imageAlt: 'Elite Designs Kenya corporate branding and digital solutions website screenshot',
    summaryNiche: 'Corporate Branding & Graphic Design',
    summarySLA: '2 Weeks Delivery',
    summaryPayment: 'Professional Agency Package',
    introHeadline: 'In a market filled with vague pricing and opaque design quotes, radical clarity in package deliverables is your greatest competitive weapon.',
    introText: '<strong>Elite Designs Kenya</strong> is a corporate branding and graphic design consultancy based in Nairobi, providing structured brand identity packages, company profiles, presentation guides, and digital marketing collateral for Kenyan startups and established businesses. They engaged <strong>Xclusive Tech</strong> to engineer an agency presentation portal that answers prospect pricing and deliverable questions before the initial sales discovery call.',
    section1Title: '1. The Agency Sales Challenge: Eliminating Quote Hesitation',
    section1Content: `
      <p>Many design agencies in Nairobi waste dozens of hours each month in endless back-and-forth discovery meetings with unvetted prospects:</p>
      <ul class="list-disc pl-6 space-y-2">
        <li><strong>Unclear Scope Expectations:</strong> Clients often ask for "a simple logo" but actually require full stationery, color palettes, and social media brand templates.</li>
        <li><strong>Price Transparency:</strong> Kenyan businesses prefer upfront, transparent package tiers rather than waiting 3 days for a custom proposal.</li>
        <li><strong>Proof of Execution:</strong> The agency needed a polished digital showcase demonstrating real PDF portfolio decks, brand guidelines, and print-ready deliverables.</li>
      </ul>
    `,
    section2Title: '2. The Engineering Strategy: How We Built Elite Designs Kenya',
    section2Intro: 'We engineered <a href="https://elitedesigns.co.ke" target="_blank" rel="noopener noreferrer" class="text-blue-600 font-semibold underline">elitedesigns.co.ke</a> around modular package selection, visual transparency, and rapid inquiry routing:',
    features: [
      {
        title: 'A. Interactive 3-Tier Brand Package Selector',
        desc: 'Engineered a clear comparative pricing table detailing the exact deliverables of each package (Starter Identity, Brand Growth, and Full Corporate Suite) with transparent pricing and turnaround timelines.'
      },
      {
        title: 'B. Embedded Portfolio Decks & PDF Asset Previews',
        desc: 'Interactive document viewers allowing corporate procurement teams and founders to review sample brand guidelines, company profiles, and presentation guides directly on their phones.'
      },
      {
        title: 'C. Instant Project Scoping & WhatsApp Integration',
        desc: 'Direct consultation triggers that capture the client\'s industry, package tier, and deadline, routing hot project briefs directly to the agency\'s WhatsApp inbox.'
      }
    ],
    results: [
      { metric: '50%', label: 'Reduction in Discovery Call Duration' },
      { metric: '18', label: 'New Corporate Identity Retainers Closed' },
      { metric: '2.4x', label: 'Increase in Direct Package Quote Inquiries' },
      { metric: '1.2s', label: 'Mobile Page Load Speed in Nairobi' }
    ],
    quote: '"Our website does 70% of the sales conversation for us. By the time a client reaches out on WhatsApp, they already know our packages, our quality, and our pricing."',
    quoteAuthor: 'Elite Designs Kenya Leadership',
    faqs: [
      {
        q: 'Why should creative and branding agencies publish package tiers on their website?',
        a: 'Publishing clear package deliverables and starting rates filters out unqualified inquiries and builds instant trust with serious corporate buyers who value transparency over vague proposals.'
      },
      {
        q: 'How does an agency showcase downloadable PDF portfolio decks effectively online?',
        a: 'We embed lightweight, mobile-optimized document previews and direct vector sample downloads that allow prospective clients to verify print and digital quality on any screen.'
      },
      {
        q: 'How much does an agency presentation website cost in Kenya?',
        a: 'Professional agency presentation platforms with service tier selectors and downloadable collateral showcases typically range between KES 25,000 and KES 45,000 at Xclusive Tech.'
      }
    ]
  }
];

function generateHtml(cs) {
  const accentBadge = {
    emerald: 'bg-emerald-100 text-emerald-800 border-emerald-200',
    amber: 'bg-amber-100 text-amber-800 border-amber-200',
    red: 'bg-red-100 text-red-800 border-red-200',
    purple: 'bg-purple-100 text-purple-800 border-purple-200',
    blue: 'bg-blue-100 text-blue-800 border-blue-200'
  }[cs.accentColor] || 'bg-blue-100 text-blue-800 border-blue-200';

  const accentBtn = {
    emerald: 'bg-emerald-600 hover:bg-emerald-700',
    amber: 'bg-amber-600 hover:bg-amber-700',
    red: 'bg-red-600 hover:bg-red-700',
    purple: 'bg-purple-600 hover:bg-purple-700',
    blue: 'bg-blue-600 hover:bg-blue-700'
  }[cs.accentColor] || 'bg-blue-600 hover:bg-blue-700';

  const accentText = {
    emerald: 'text-emerald-600 hover:text-emerald-800',
    amber: 'text-amber-600 hover:text-amber-800',
    red: 'text-red-600 hover:text-red-800',
    purple: 'text-purple-600 hover:text-purple-800',
    blue: 'text-blue-600 hover:text-blue-800'
  }[cs.accentColor] || 'text-blue-600 hover:text-blue-800';

  const accentBorder = {
    emerald: 'border-emerald-200 bg-emerald-50/50',
    amber: 'border-amber-200 bg-amber-50/50',
    red: 'border-red-200 bg-red-50/50',
    purple: 'border-purple-200 bg-purple-50/50',
    blue: 'border-blue-200 bg-blue-50/50'
  }[cs.accentColor] || 'border-blue-200 bg-blue-50/50';

  const faqsJson = cs.faqs.map(f => ({
    '@type': 'Question',
    name: f.q,
    acceptedAnswer: {
      '@type': 'Answer',
      text: f.a
    }
  }));

  return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${cs.metaTitle}</title>
    <meta name="description" content="${cs.metaDesc}">
    <meta name="keywords" content="${cs.keywords}">
    <meta name="author" content="Samuel Kidemi Kisaga, Xclusive Tech">
    <meta property="og:title" content="${cs.metaTitle}">
    <meta property="og:description" content="${cs.metaDesc}">
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://www.xclusivetech.co.ke/blog/${cs.slug}">
    <meta property="og:image" content="https://www.xclusivetech.co.ke/assets/images/blog/${cs.slug}.jpg">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="${cs.metaTitle}">
    <meta name="twitter:description" content="${cs.metaDesc}">
    <meta name="twitter:image" content="https://www.xclusivetech.co.ke/assets/images/blog/${cs.slug}.jpg">
    <link rel="canonical" href="https://www.xclusivetech.co.ke/blog/${cs.slug}">

    <!-- Theme Enforcement: Strictly Light Mode -->
    <script>
        try {
            localStorage.removeItem('xclusive_theme');
            document.documentElement.removeAttribute('data-theme');
            document.documentElement.classList.remove('dark');
        } catch (e) {}
    </script>

    <!-- Google Fonts Preconnect & Ubuntu Font Loading -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Ubuntu:ital,wght@0,300;0,400;0,500;0,700;1,300;1,400;1,500;1,700&display=swap" rel="stylesheet">

    <!-- Tailwind CSS -->
    <script>
        window.tailwind = {
            config: {
                darkMode: 'class',
                theme: {
                    extend: {
                        fontFamily: {
                            sans: ['Ubuntu', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
                        }
                    }
                }
            }
        };
    </script>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="icon" href="../assets/icons/xclusivetech-favicon.svg?v=2" type="image/svg+xml">
    <link rel="icon" type="image/png" sizes="96x96" href="../assets/icons/favicon-96x96.png?v=2">
    <link rel="apple-touch-icon" sizes="180x180" href="../assets/icons/apple-touch-icon.png?v=2">
    <link rel="shortcut icon" href="../favicon.ico?v=2">
    <link rel="manifest" href="../site.webmanifest">
    <link rel="stylesheet" href="../css/styles.css?v=20260913e">

    <!-- Structured Data: BreadcrumbList, BlogPosting, FAQPage -->
    <script type="application/ld+json">
    {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "BreadcrumbList",
                "@id": "https://www.xclusivetech.co.ke/blog/${cs.slug}#breadcrumb",
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": 1,
                        "name": "Home",
                        "item": "https://www.xclusivetech.co.ke/"
                    },
                    {
                        "@type": "ListItem",
                        "position": 2,
                        "name": "Blog",
                        "item": "https://www.xclusivetech.co.ke/blog/"
                    },
                    {
                        "@type": "ListItem",
                        "position": 3,
                        "name": "${cs.title}",
                        "item": "https://www.xclusivetech.co.ke/blog/${cs.slug}"
                    }
                ]
            },
            {
                "@type": "BlogPosting",
                "@id": "https://www.xclusivetech.co.ke/blog/${cs.slug}#blogposting",
                "headline": "${cs.title}",
                "description": "${cs.metaDesc}",
                "image": [
                    "https://www.xclusivetech.co.ke/assets/images/blog/${cs.slug}.jpg"
                ],
                "datePublished": "${cs.date}",
                "dateModified": "${cs.date}",
                "inLanguage": "en-KE",
                "mainEntityOfPage": {
                    "@type": "WebPage",
                    "@id": "https://www.xclusivetech.co.ke/blog/${cs.slug}"
                },
                "isPartOf": {
                    "@type": "Blog",
                    "@id": "https://www.xclusivetech.co.ke/blog/#blog",
                    "name": "Xclusive Tech Blog"
                },
                "author": [
                    {
                        "@type": "Person",
                        "@id": "https://www.xclusivetech.co.ke/founder#person",
                        "name": "Samuel Kidemi Kisaga",
                        "jobTitle": "Founder & Lead Web Designer",
                        "url": "https://www.xclusivetech.co.ke/founder"
                    }
                ],
                "publisher": {
                    "@type": "Organization",
                    "@id": "https://www.xclusivetech.co.ke/#organization",
                    "name": "Xclusive Tech",
                    "url": "https://www.xclusivetech.co.ke/",
                    "logo": {
                        "@type": "ImageObject",
                        "url": "https://www.xclusivetech.co.ke/assets/icons/favicon-512x512.png"
                    }
                }
            },
            {
                "@type": "FAQPage",
                "@id": "https://www.xclusivetech.co.ke/blog/${cs.slug}#faq",
                "mainEntity": ${JSON.stringify(faqsJson, null, 2)}
            }
        ]
    }
    </script>
</head>
<body class="bg-white text-slate-900 overflow-x-hidden">

    <!-- Navigation -->
    <nav class="fixed top-0 w-full z-50 bg-white/95 backdrop-blur-lg border-b border-slate-200 transition-all duration-300" id="navbar">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between items-center h-16">
                <a href="/" class="flex items-center gap-2">
                    <img src="../assets/icons/xclusivetech-header-logo-light.svg" alt="Xclusive Tech logo" class="nav-logo-img nav-logo-light h-10 w-auto">
                    <img src="../assets/icons/xclusivetech-header-logo.svg" alt="Xclusive Tech logo" class="nav-logo-img nav-logo-dark h-10 w-auto">
                </a>
                <div class="hidden md:flex gap-8">
                    <a href="/" class="nav-link">Home</a>
                    <a href="/about" class="nav-link">About</a>
                    <a href="/services" class="nav-link">Services</a>
                    <div class="relative group">
                        <button type="button" class="nav-link bg-transparent cursor-pointer flex items-center gap-1">
                            Solutions
                            <svg aria-hidden="true" class="w-3.5 h-3.5 transition-transform duration-200 group-hover:rotate-180" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"/></svg>
                        </button>
                        <div class="absolute left-1/2 -translate-x-1/2 top-full pt-3 hidden group-hover:block z-50">
                            <div class="bg-white border border-slate-200 rounded-xl shadow-2xl py-2 w-60">
                                <a href="/solutions" class="block px-4 py-2.5 text-sm text-gray-700 hover:bg-slate-50 hover:text-blue-600 transition-colors">Solutions by Business Type</a>
                                <a href="/solutions#industries" class="block px-4 py-2.5 text-sm text-gray-700 hover:bg-slate-50 hover:text-blue-600 transition-colors">Industries We Serve</a>
                                <a href="/solutions#saas" class="block px-4 py-2.5 text-sm text-gray-700 hover:bg-slate-50 hover:text-blue-600 transition-colors">SaaS &amp; Custom Platforms</a>
                            </div>
                        </div>
                    </div>
                    <a href="/pricing" class="nav-link">Pricing</a>
                    <a href="/portfolio" class="nav-link">Portfolio</a>
                    <a href="/blog/" class="nav-link active">Blog</a>
                    <a href="/contact" class="nav-link">Contact</a>
                </div>
                <div class="nav-actions flex items-center gap-3">
                    <a href="https://wa.me/254722753819?text=Hi%20Samuel,%20I%20read%20your%20${encodeURIComponent(cs.domain)}%20project%20story.%20We%20need%20a%20similar%20high-converting%20website." target="_blank" class="hidden md:block px-6 py-2 rounded-lg ${accentBtn} text-white shadow-md transition-all duration-300 font-medium">Get Project Quote</a>
                    <button id="mobile-menu-btn" class="md:hidden p-2 rounded-lg hover:bg-slate-100 transition-colors" aria-label="Toggle menu">
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
                        </svg>
                    </button>
                </div>
            </div>
        </div>
    </nav>

    <!-- Breadcrumb Header -->
    <header class="pt-28 pb-8 px-4 sm:px-6 lg:px-8 bg-gradient-to-b from-slate-50 to-white border-b border-slate-100">
        <div class="max-w-4xl mx-auto">
            <nav class="flex items-center gap-2 text-xs text-slate-500 mb-6 font-medium" aria-label="Breadcrumb">
                <a href="/" class="hover:text-blue-600 transition">Home</a>
                <span>/</span>
                <a href="/blog/" class="hover:text-blue-600 transition">Blog</a>
                <span>/</span>
                <span class="text-slate-800">${cs.domain} Case Study</span>
            </nav>

            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full ${accentBadge} text-xs font-semibold uppercase tracking-wider mb-4 border">
                <span>${cs.badge}</span>
            </div>

            <h1 class="text-3xl sm:text-4xl lg:text-5xl font-extrabold text-slate-900 tracking-tight leading-tight mb-6">
                ${cs.title}
            </h1>

            <div class="flex items-center gap-4 text-sm text-slate-600 pb-2 border-b border-slate-200">
                <div class="flex items-center gap-2.5">
                    <img src="../assets/images/samuel-headshot.png" alt="Samuel Kidemi" class="w-10 h-10 rounded-full border border-blue-200 object-cover">
                    <div>
                        <span class="font-bold text-slate-900 block leading-tight">Samuel Kidemi Kisaga</span>
                        <span class="text-xs text-slate-500">Founder &amp; Principal Web Architect</span>
                    </div>
                </div>
                <span class="text-slate-300">•</span>
                <time datetime="${cs.date}" class="text-xs text-slate-500">October 29, 2026</time>
                <span class="text-slate-300">•</span>
                <span class="text-xs font-semibold ${cs.accentColor === 'emerald' ? 'text-emerald-600' : (cs.accentColor === 'amber' ? 'text-amber-600' : (cs.accentColor === 'red' ? 'text-red-600' : 'text-blue-600'))}">${cs.readTime}</span>
                <span class="text-slate-300">•</span>
                <a href="${cs.liveUrl}" target="_blank" rel="noopener noreferrer" class="text-xs font-semibold ${accentText}">Live Site: ${cs.domain} &rarr;</a>
            </div>
        </div>
    </header>

    <!-- Main Content -->
    <main class="py-12 px-4 sm:px-6 lg:px-8">
        <article class="max-w-4xl mx-auto">

            <!-- Hero Image Banner -->
            <div class="rounded-2xl overflow-hidden border border-slate-200 shadow-xl mb-12 bg-slate-900">
                <picture>
                    <source srcset="../assets/images/blog/${cs.slug}.webp" type="image/webp">
                    <img src="../assets/images/blog/${cs.slug}.jpg" alt="${cs.imageAlt}" width="1200" height="630" class="w-full h-auto object-cover" loading="eager" fetchpriority="high">
                </picture>
                <div class="p-4 bg-slate-900 text-slate-300 text-xs flex justify-between items-center border-t border-slate-800">
                    <span>${cs.domain} &bull; ${cs.summaryNiche} &bull; Engineered by Samuel Kidemi at Xclusive Tech</span>
                    <a href="${cs.liveUrl}" target="_blank" rel="noopener noreferrer" class="text-blue-400 hover:text-blue-300 font-semibold">Visit ${cs.domain} &rarr;</a>
                </div>
            </div>

            <div class="prose prose-slate lg:prose-lg max-w-none space-y-8 text-slate-700 leading-relaxed">
                
                <p class="text-xl text-slate-800 font-medium leading-relaxed">
                    ${cs.introHeadline}
                </p>

                <p>
                    ${cs.introText}
                </p>

                <!-- Project Snapshot Box -->
                <div class="my-8 p-6 rounded-2xl ${accentBorder} border">
                    <h2 class="text-lg font-bold text-slate-900 mb-3 flex items-center gap-2">
                        <span>⚡</span> Project Snapshot: ${cs.domain}
                    </h2>
                    <div class="grid sm:grid-cols-2 md:grid-cols-4 gap-4 text-xs">
                        <div class="bg-white p-3 rounded-xl border border-slate-200 shadow-sm">
                            <span class="text-slate-400 block font-medium">Domain</span>
                            <span class="font-bold text-slate-800 text-sm">${cs.domain}</span>
                        </div>
                        <div class="bg-white p-3 rounded-xl border border-slate-200 shadow-sm">
                            <span class="text-slate-400 block font-medium">Industry</span>
                            <span class="font-bold text-slate-800 text-sm">${cs.summaryNiche}</span>
                        </div>
                        <div class="bg-white p-3 rounded-xl border border-slate-200 shadow-sm">
                            <span class="text-slate-400 block font-medium">Timeline</span>
                            <span class="font-bold text-slate-800 text-sm">${cs.summarySLA}</span>
                        </div>
                        <div class="bg-white p-3 rounded-xl border border-slate-200 shadow-sm">
                            <span class="text-slate-400 block font-medium">Delivery Model</span>
                            <span class="font-bold text-slate-800 text-sm">${cs.summaryPayment}</span>
                        </div>
                    </div>
                </div>

                <!-- 1. The Challenge -->
                <h2 class="text-2xl font-bold text-slate-900 tracking-tight pt-4">
                    ${cs.section1Title}
                </h2>

                ${cs.section1Content}

                <!-- 2. The Strategy -->
                <h2 class="text-2xl font-bold text-slate-900 tracking-tight pt-4">
                    ${cs.section2Title}
                </h2>

                <p>
                    ${cs.section2Intro}
                </p>

                <div class="space-y-6 my-6">
                    ${cs.features.map(f => `
                    <div class="p-6 rounded-xl border border-slate-200 bg-white hover:border-blue-400 transition shadow-sm">
                        <h3 class="text-lg font-bold text-slate-900 mb-2">${f.title}</h3>
                        <p class="text-sm text-slate-600 leading-relaxed">
                            ${f.desc}
                        </p>
                    </div>`).join('\n')}
                </div>

                <!-- 3. Commercial Results -->
                <h2 class="text-2xl font-bold text-slate-900 tracking-tight pt-4">
                    3. Commercial Impact &amp; Results
                </h2>

                <div class="grid grid-cols-2 md:grid-cols-4 gap-4 my-6">
                    ${cs.results.map(r => `
                    <div class="p-4 rounded-xl bg-slate-50 border border-slate-200 text-center">
                        <span class="text-2xl sm:text-3xl font-extrabold text-slate-900 block mb-1">${r.metric}</span>
                        <span class="text-xs text-slate-500 font-medium leading-tight">${r.label}</span>
                    </div>`).join('\n')}
                </div>

                <!-- Client Testimonial Box -->
                <div class="my-8 p-6 rounded-2xl bg-gradient-to-r from-slate-900 to-slate-800 text-white shadow-lg">
                    <p class="text-lg italic font-medium leading-relaxed mb-4">
                        ${cs.quote}
                    </p>
                    <div class="text-sm text-slate-300 font-semibold">
                        &mdash; ${cs.quoteAuthor}
                    </div>
                </div>

                <!-- FAQ Section -->
                <div class="my-12 pt-8 border-t border-slate-200">
                    <h2 class="text-2xl font-bold text-slate-900 tracking-tight mb-6">Frequently Asked Questions</h2>
                    <div class="space-y-6">
                        ${cs.faqs.map(f => `
                        <div class="p-5 rounded-xl border border-slate-200 bg-slate-50/50">
                            <h3 class="text-base font-bold text-slate-900 mb-2">${f.q}</h3>
                            <p class="text-sm text-slate-600 leading-relaxed">${f.a}</p>
                        </div>`).join('\n')}
                    </div>
                </div>

                <!-- Call to Action -->
                <div class="my-12 p-8 rounded-2xl bg-gradient-to-br from-blue-900 via-indigo-900 to-slate-950 text-white text-center space-y-6 shadow-2xl">
                    <span class="inline-block px-3 py-1 rounded-full bg-blue-500/20 text-blue-300 text-xs font-semibold tracking-wider uppercase border border-blue-400/30">
                        Ready to Build Your Website?
                    </span>
                    <h2 class="text-3xl sm:text-4xl font-extrabold tracking-tight max-w-2xl mx-auto">
                        Turn Your Business Into Kenya\'s Next Digital Success Story
                    </h2>
                    <p class="text-slate-300 max-w-xl mx-auto text-sm sm:text-base leading-relaxed">
                        Whether you need a high-converting landing page, an accessibility-first directory, or a corporate enterprise portal, we deliver verified results in 2 to 4 weeks.
                    </p>
                    <div class="flex flex-col sm:flex-row gap-4 justify-center items-center pt-2">
                        <a href="https://wa.me/254722753819?text=Hi%20Samuel,%20I%20read%20your%20${encodeURIComponent(cs.domain)}%20story.%20Let's%20build%20our%20website." target="_blank" class="w-full sm:w-auto px-8 py-3.5 rounded-xl bg-emerald-500 hover:bg-emerald-600 text-white font-bold text-base shadow-lg transition-all flex items-center justify-center gap-2">
                            <span>💬</span> WhatsApp Samuel Directly
                        </a>
                        <a href="/pricing" class="w-full sm:w-auto px-8 py-3.5 rounded-xl bg-white/10 hover:bg-white/20 text-white font-semibold text-base border border-white/20 transition-all">
                            View Transparent Pricing
                        </a>
                    </div>
                </div>

                <!-- Author Bio Box -->
                <div class="my-8 p-6 rounded-2xl border border-slate-200 bg-slate-50 flex flex-col sm:flex-row items-center gap-6">
                    <img src="../assets/images/samuel-headshot.png" alt="Samuel Kidemi" class="w-20 h-20 rounded-full border-2 border-blue-600 object-cover flex-shrink-0">
                    <div class="space-y-2 text-center sm:text-left">
                        <h3 class="text-base font-bold text-slate-900">About the Author: Samuel Kidemi Kisaga</h3>
                        <p class="text-xs text-slate-600 leading-relaxed">
                            Lead Web Engineer &amp; Founder at Xclusive Tech. Samuel has architected and delivered over 120+ custom web platforms across Kenya, specializing in sub-second mobile performance, automated M-Pesa checkouts, and high-conversion UX.
                        </p>
                        <div class="flex justify-center sm:justify-start gap-4 text-xs font-semibold text-blue-600">
                            <a href="/founder" class="hover:underline">Founder Profile &rarr;</a>
                            <a href="/portfolio" class="hover:underline">Full Portfolio &rarr;</a>
                        </div>
                    </div>
                </div>

            </div>
        </article>
    </main>

    <!-- Footer -->
    <footer class="bg-slate-900 text-slate-400 py-16 px-4 sm:px-6 lg:px-8 border-t border-slate-800">
        <div class="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-4 gap-8">
            <div class="space-y-4">
                <img src="../assets/icons/xclusivetech-header-logo.svg" alt="Xclusive Tech logo" class="h-10 w-auto">
                <p class="text-xs text-slate-400 leading-relaxed">
                    Kenya's most reliable web design and software engineering agency. 120+ verified deployments across Nairobi, Kiambu, and East Africa.
                </p>
                <div class="text-xs text-slate-400">
                    <strong>Office:</strong> Suite F8, Wood Ave Park Apartments, Kilimani, Nairobi.
                </div>
            </div>
            <div>
                <h4 class="text-sm font-bold text-white uppercase tracking-wider mb-4">Case Studies</h4>
                <ul class="space-y-2 text-xs">
                    <li><a href="/blog/case-study-how-we-built-patamaps-accessible-special-needs-directory-kenya" class="hover:text-white transition">PataMaps Directory</a></li>
                    <li><a href="/blog/case-study-how-we-built-san-group-limited-civil-engineering-infrastructure-portal" class="hover:text-white transition">SAN Group Limited</a></li>
                    <li><a href="/blog/case-study-how-we-built-irene-muendo-isuzu-dealership-website-nairobi" class="hover:text-white transition">Irene Muendo Isuzu</a></li>
                    <li><a href="/blog/case-study-how-we-built-creative-kigen-design-portfolio-website" class="hover:text-white transition">Creative Kigen Studio</a></li>
                    <li><a href="/blog/case-study-how-we-built-elite-designs-corporate-branding-website" class="hover:text-white transition">Elite Designs Kenya</a></li>
                    <li><a href="/blog/case-study-how-i-built-batteriq-automotive-battery-delivery-kenya" class="hover:text-white transition">Batteriq Nairobi</a></li>
                </ul>
            </div>
            <div>
                <h4 class="text-sm font-bold text-white uppercase tracking-wider mb-4">Core Services</h4>
                <ul class="space-y-2 text-xs">
                    <li><a href="/services#web-design" class="hover:text-white transition">Corporate Web Design</a></li>
                    <li><a href="/services#ecommerce" class="hover:text-white transition">M-Pesa E-Commerce</a></li>
                    <li><a href="/solutions#saas" class="hover:text-white transition">Custom Web Portals</a></li>
                    <li><a href="/pricing" class="hover:text-white transition">Express Landing Pages (KES 15K)</a></li>
                    <li><a href="/services#seo" class="hover:text-white transition">Local Google SEO &amp; Maps</a></li>
                </ul>
            </div>
            <div>
                <h4 class="text-sm font-bold text-white uppercase tracking-wider mb-4">Get In Touch</h4>
                <p class="text-xs text-slate-400 mb-3">Speak directly with Samuel Kidemi on WhatsApp:</p>
                <a href="https://wa.me/254722753819" target="_blank" class="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-emerald-600 text-white font-bold text-xs hover:bg-emerald-700 transition">
                    <span>💬</span> +254 722 753 819
                </a>
                <p class="text-xs text-slate-500 mt-4">&copy; 2026 Xclusive Tech. All rights reserved.</p>
            </div>
        </div>
    </footer>

</body>
</html>`;
}

CASE_STUDIES.forEach(cs => {
  const filePath = path.join('blog', cs.filename);
  const content = generateHtml(cs);
  fs.writeFileSync(filePath, content, 'utf8');
  console.log(`Generated case study blog: ${filePath} (${content.length} chars)`);
});

console.log('\nAll 5 case study blog posts generated successfully!');

