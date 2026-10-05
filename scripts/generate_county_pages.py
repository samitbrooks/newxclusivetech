#!/usr/bin/env python3
"""
generate_county_pages.py
Generates 47 high-converting commercial landing pages for all 47 counties of Kenya,
plus the central County Directory Hub index page at /locations/index.html.
Includes rich LocalBusiness, Service, BreadcrumbList and FAQPage structured JSON-LD schema,
tailored local economic contexts, key commercial town hubs, and direct WhatsApp / lead intake CTAs.
"""

import os
import re
import json

WORKSPACE_DIR = "/Users/app/newxclusivetech"
LOCATIONS_DIR = os.path.join(WORKSPACE_DIR, "locations")
os.makedirs(LOCATIONS_DIR, exist_ok=True)

COUNTIES = [
    {
        "code": "001",
        "name": "Mombasa",
        "slug": "web-design-mombasa",
        "region": "Coast",
        "seat": "Mombasa City",
        "towns": ["Mombasa CBD", "Nyali", "Bamburi", "Changamwe", "Likoni", "Mtwapa border"],
        "tagline": "Maritime Commerce, Beach Hospitality & Port Logistics Web Solutions",
        "desc": "Mombasa is Kenya's principal coastal trade gateway and second-largest economic powerhouse. From beach resorts and holiday villas in Nyali and Bamburi to freight forwarders, container logistics firms, and clearing agents near Kilindini Harbour, businesses in Mombasa need fast, mobile-first websites that convert both local East African clients and international maritime partners.",
        "economic_focus": "Port logistics, international clearing & forwarding, beachfront resorts, holiday home rentals, deep-sea fishing, and coastal retail.",
        "top_searches": ["web design in Mombasa", "Mombasa website developers", "affordable web design Nyali", "website design company Mombasa", "e-commerce web design Mombasa"]
    },
    {
        "code": "002",
        "name": "Kwale",
        "slug": "web-design-kwale",
        "region": "Coast",
        "seat": "Kwale Town",
        "towns": ["Diani Beach", "Ukunda", "Kwale Town", "Msambweni", "Kinango", "Lungalunga"],
        "tagline": "Luxury Safari & Beach Tourism, Eco-Lodges & Agribusiness Web Design",
        "desc": "Home to the world-renowned Diani Beach, Kwale County is a premier destination for luxury boutique hotels, kitesurfing academies, private villas, and marine eco-tourism. A modern website with real-time room reservations, direct M-Pesa deposit processing, and international card gateways enables Kwale businesses to bypass high third-party OTA commissions.",
        "economic_focus": "Luxury beach tourism, marine water sports, mineral mining, fruit processing, and eco-lodge hospitality.",
        "top_searches": ["web design Diani", "website developers in Kwale", "hotel website design Diani Beach", "tour website design Kwale"]
    },
    {
        "code": "003",
        "name": "Kilifi",
        "slug": "web-design-kilifi",
        "region": "Coast",
        "seat": "Kilifi Town",
        "towns": ["Malindi", "Kilifi Town", "Watamu", "Mtwapa", "Mariakani", "Kaloleni"],
        "tagline": "Marine Tourism, Real Estate Developments & Coastal Agribusiness Websites",
        "desc": "Spanning vibrant commercial and tourist centers from Mtwapa and Kilifi Bofa to Watamu and Malindi, Kilifi County is an active hub for oceanfront real estate, marine conservation, hospitality, and cashew processing. We engineer high-speed websites with integrated WhatsApp chat and Google Maps location indexing to capture tourist and investor foot traffic.",
        "economic_focus": "Oceanfront holiday real estate, Watamu marine tourism, deep-sea sport fishing, cashew/coconut value addition, and cement manufacturing.",
        "top_searches": ["web design Malindi", "website developers Kilifi", "web design Watamu", "real estate website design Kilifi"]
    },
    {
        "code": "004",
        "name": "Tana River",
        "slug": "web-design-tana-river",
        "region": "Coast",
        "seat": "Hola",
        "towns": ["Hola Town", "Madogo", "Garsen", "Bura", "Kipini"],
        "tagline": "Irrigation Agriculture, Livestock Trade & Community Enterprise Web Design",
        "desc": "Tana River County's economy is powered by expansive irrigation schemes at Bura and Hola, commercial livestock trade, and riverine eco-enterprises. Modern websites empower local agricultural cooperatives, mango processors, and contractor suppliers to bid for government tenders and access direct buyers nationwide.",
        "economic_focus": "Commercial irrigation farming, livestock markets, mango and watermelon supply, riverine fisheries, and civil engineering tenders.",
        "top_searches": ["website design Tana River", "web developers Hola", "agribusiness website Kenya", "cooperative web design Kenya"]
    },
    {
        "code": "005",
        "name": "Lamu",
        "slug": "web-design-lamu",
        "region": "Coast",
        "seat": "Lamu Old Town",
        "towns": ["Lamu Old Town", "Shela", "Mpeketoni", "Mokowe", "Faza", "Kiunga"],
        "tagline": "UNESCO Heritage Tourism, LAPSSET Corridor Logistics & Island Hospitality",
        "desc": "From the historic architecture of Lamu Old Town and luxury bohemian retreats of Shela to the burgeoning LAPSSET deep-sea port logistics at Mokowe, Lamu requires websites that balance exquisite visual storytelling with high-converting booking systems and maritime logistics profiles.",
        "economic_focus": "Heritage eco-tourism, dhow sailing charters, boutique island guest houses, LAPSSET maritime infrastructure, and Mpeketoni cotton/produce.",
        "top_searches": ["web design Lamu", "hotel website Shela Lamu", "LAPSSET logistics website", "dhow charter booking website"]
    },
    {
        "code": "006",
        "name": "Taita-Taveta",
        "slug": "web-design-taita-taveta",
        "region": "Coast",
        "seat": "Mwatate",
        "towns": ["Voi", "Taveta", "Wundanyi", "Mwatate", "Mackinnon Road"],
        "tagline": "Tsavo Safari Lodges, Cross-Border Trade & Mining Enterprise Web Portals",
        "desc": "Strategically situated along the Nairobi-Mombasa highway and the Tanzania border at Taveta, Taita-Taveta is a vital trade node and the gateway to Tsavo East and West National Parks. Our bespoke websites equip safari camps, gemstone dealers, and cross-border logistics operators with conversion-optimized digital presence.",
        "economic_focus": "Tsavo wildlife safari lodges, Tsavo gemstone and tanzanite mining, cross-border agro-trade with Tanzania, and sisal plantations.",
        "top_searches": ["web design Voi", "website developers Taita Taveta", "safari camp website design Tsavo", "tour company website Voi"]
    },
    {
        "code": "007",
        "name": "Garissa",
        "slug": "web-design-garissa",
        "region": "North Eastern",
        "seat": "Garissa Town",
        "towns": ["Garissa Town", "Dadaab", "Masalani", "Modogashe", "Bura East"],
        "tagline": "Regional Commercial Hub, Livestock Logistics & Energy Enterprise Websites",
        "desc": "Garissa Town serves as the principal economic capital of North Eastern Kenya, boasting one of the largest livestock markets in East Africa and expanding solar energy projects. We build robust, mobile-optimized business websites and supply chain portals that connect Garissa enterprises to national markets.",
        "economic_focus": "Regional livestock auction markets, cross-border wholesale, solar energy infrastructure, NGO contractor supplies, and commercial real estate.",
        "top_searches": ["web design Garissa", "website developers Garissa", "livestock trade website Kenya", "contractor website Garissa"]
    },
    {
        "code": "008",
        "name": "Wajir",
        "slug": "web-design-wajir",
        "region": "North Eastern",
        "seat": "Wajir Town",
        "towns": ["Wajir Town", "Habaswein", "Tarbaj", "Eldas", "Bute", "Griftu"],
        "tagline": "Pastoral Agribusiness, Livestock Export & Renewable Power Web Systems",
        "desc": "Wajir County is a vital livestock production center with rapid infrastructure modernization. We equip Wajir entrepreneurs, healthcare centers, transport fleets, and suppliers with mobile-responsive websites featuring WhatsApp lead intake and clear service catalogs.",
        "economic_focus": "Camel and cattle livestock export, commercial retail distribution, borehole and water infrastructure contracting, and community health.",
        "top_searches": ["web design Wajir", "website developers in Wajir", "business website Wajir", "livestock exporter website"]
    },
    {
        "code": "009",
        "name": "Mandera",
        "slug": "web-design-mandera",
        "region": "North Eastern",
        "seat": "Mandera Town",
        "towns": ["Mandera Town", "Elwak", "Rhamu", "Takaba", "Banissa", "Lafey"],
        "tagline": "Tri-Border Trade, Commercial Contracting & Mineral Quarrying Web Platforms",
        "desc": "Bordering Ethiopia and Somalia, Mandera County occupies an indispensable geopolitical and commercial cross-border corridor. We build professional company websites that establish trust with international partners, aid organizations, and government agencies.",
        "economic_focus": "Tri-border international commerce, building stone and gypsum quarrying, irrigation farming along the Daua River, and logistics.",
        "top_searches": ["web design Mandera", "website developers Mandera", "construction website Mandera", "import export website Kenya"]
    },
    {
        "code": "010",
        "name": "Marsabit",
        "slug": "web-design-marsabit",
        "region": "Eastern",
        "seat": "Marsabit Town",
        "towns": ["Marsabit Town", "Moyale", "Loiyangalani", "North Horr", "Laisamis"],
        "tagline": "Moyale One-Stop Border Trade, Lake Turkana Wind Power & Cultural Tourism",
        "desc": "From the bustling Moyale border post trading directly with Ethiopia to wind energy pioneers at Lake Turkana, Marsabit County is undergoing unprecedented commercial expansion. Our web development solutions help local businesses showcase cross-border services and cultural safari expeditions.",
        "economic_focus": "Ethiopia cross-border clearing, Lake Turkana wind energy support, cultural heritage tourism, livestock value chains, and fisheries.",
        "top_searches": ["web design Moyale", "website developers Marsabit", "cross border logistics website", "cultural tourism website Kenya"]
    },
    {
        "code": "011",
        "name": "Isiolo",
        "slug": "web-design-isiolo",
        "region": "Eastern",
        "seat": "Isiolo Town",
        "towns": ["Isiolo Town", "Garbatulla", "Merti", "Oldonyiro", "Kinna"],
        "tagline": "LAPSSET Resort City, Northern Safari Circuit & Logistics Hub Websites",
        "desc": "Designated as a flagship LAPSSET resort hub and the central transport nexus linking Nairobi to Northern Kenya and Ethiopia, Isiolo is prime ground for logistics, hospitality, and modern commerce. We build high-converting websites designed to capture institutional and commercial contracts.",
        "economic_focus": "LAPSSET transport corridor logistics, Samburu/Buffalo Springs safari connections, international airport trade, and modern abattoirs.",
        "top_searches": ["web design Isiolo", "website developers Isiolo", "hotel website Isiolo", "transport company website Isiolo"]
    },
    {
        "code": "012",
        "name": "Meru",
        "slug": "web-design-meru",
        "region": "Eastern",
        "seat": "Meru Town",
        "towns": ["Meru Town", "Nkubu", "Maua", "Timau", "Makutano", "Mikinduri"],
        "tagline": "Horticulture, Floriculture, Miraa Commerce & Mount Kenya Tourism Web Portals",
        "desc": "Meru County is an agricultural powerhouse, boasting rich volcanic soils that produce high-value exports in Timau floriculture, miraa trading hubs in Maua, and coffee/dairy cooperatives around Nkubu. Our e-commerce and corporate websites help Meru businesses expand into Nairobi and global markets.",
        "economic_focus": "Floriculture and fresh produce exports, miraa commercial logistics, high-grade specialty coffee and tea, dairy farming, and Mt. Kenya tourism.",
        "top_searches": ["web design Meru", "website developers in Meru", "web design Maua", "agribusiness website Meru", "floriculture website Kenya"]
    },
    {
        "code": "013",
        "name": "Tharaka-Nithi",
        "slug": "web-design-tharaka-nithi",
        "region": "Eastern",
        "seat": "Kathwana",
        "towns": ["Chuka", "Kathwana", "Marimanti", "Chogoria", "Magutuni"],
        "tagline": "Chuka University Tech Hub, Mount Kenya Climbing & Agro-Processing Websites",
        "desc": "Anchored by Chuka's thriving student and academic economy, Chogoria's medical and mountaineering routes, and Kathwana's administrative center, Tharaka-Nithi enterprises need agile, modern digital platforms with online payments and mobile lead forms.",
        "economic_focus": "Higher education and student housing, Mt. Kenya climbing expeditions, specialty tea/coffee farming, and honey processing.",
        "top_searches": ["web design Chuka", "website developers Tharaka Nithi", "web design Chogoria", "student hostel website Kenya"]
    },
    {
        "code": "014",
        "name": "Embu",
        "slug": "web-design-embu",
        "region": "Eastern",
        "seat": "Embu Town",
        "towns": ["Embu Town", "Runyenjes", "Siakago", "Manyatta", "Kiritiri"],
        "tagline": "Macadamia Nut Processing, Coffee Cooperatives & Hospitality Web Platforms",
        "desc": "Embu is a historic regional administrative hub with thriving macadamia processing factories, high-altitude coffee mills, and eco-tourism resorts along Mount Kenya's eastern slopes. We craft websites that highlight processing credentials and capture direct corporate inquiries.",
        "economic_focus": "Macadamia and avocado processing, specialty coffee processing, dairy cooperatives, and conference hospitality.",
        "top_searches": ["web design Embu", "website developers in Embu", "coffee exporter website Kenya", "hotel website Embu"]
    },
    {
        "code": "015",
        "name": "Kitui",
        "slug": "web-design-kitui",
        "region": "Eastern",
        "seat": "Kitui Town",
        "towns": ["Kitui Town", "Mwingi", "Mutomo", "Kwa Vonza", "Kibwezi border"],
        "tagline": "Textile Manufacturing, Mining Minerals, Honey & Agribusiness Web Design",
        "desc": "Kitui County has made notable strides in textile apparel production (KICOTEC), mineral mining at Mutomo, and pure organic honey packaging. We engineer commercial e-commerce websites and corporate portals to help Kitui producers scale national distribution.",
        "economic_focus": "Textile and uniform manufacturing, limestone and coal mining support, beekeeping and organic honey processing, and dryland agribusiness.",
        "top_searches": ["web design Kitui", "website developers in Kitui", "web design Mwingi", "apparel manufacturing website Kenya"]
    },
    {
        "code": "016",
        "name": "Machakos",
        "slug": "web-design-machakos",
        "region": "Eastern",
        "seat": "Machakos Town",
        "towns": ["Machakos Town", "Athi River", "Syokimau", "Mavoko", "Mlolongo", "Tala", "Kangundo"],
        "tagline": "Industrial Manufacturing Parks, Real Estate & EPZ Commercial Web Engineering",
        "desc": "Bordering Nairobi and hosting the heavy manufacturing epicenter of Athi River, Syokimau, and Mavoko EPZ, Machakos County is an industrial powerhouse. From logistics parks along Mombasa Road to master-planned residential communities, Machakos businesses demand robust, enterprise-grade web engineering.",
        "economic_focus": "Heavy manufacturing (cement, steel, consumer goods), EPZ export manufacturing, commuter residential real estate, warehousing, and entertainment.",
        "top_searches": ["web design Machakos", "web design Athi River", "website developers Syokimau", "industrial website design Kenya", "real estate web design Machakos"]
    },
    {
        "code": "017",
        "name": "Makueni",
        "slug": "web-design-makueni",
        "region": "Eastern",
        "seat": "Wote",
        "towns": ["Wote", "Mtito Andei", "Kibwezi", "Emali", "Makindu", "Sultan Hamud"],
        "tagline": "Fruit Processing Value Chains, SGR Corridor Logistics & Hospitality Websites",
        "desc": "Recognized nationwide for value-addition in fruit processing (Kalamba fruit processing plant) and strategically straddling the SGR and Mombasa-Nairobi highway, Makueni enterprises require modern digital storefronts and transit hotel booking engines.",
        "economic_focus": "Mango, citrus and fruit juice processing, dairy processing, transit hotel and truck-stop hospitality along Mombasa Road, and sand harvesting regulation.",
        "top_searches": ["web design Makueni", "website developers Wote", "web design Mtito Andei", "fruit processing website Kenya"]
    },
    {
        "code": "018",
        "name": "Nyandarua",
        "slug": "web-design-nyandarua",
        "region": "Central",
        "seat": "Ol Kalou",
        "towns": ["Ol Kalou", "Engineer", "Mairo Inya", "Ndunyu Njeru", "Ndaragwa"],
        "tagline": "Commercial Potato Farming, Cold Storage Logistics & Dairy Enterprise Websites",
        "desc": "As the food basket of Kenya producing a massive share of the nation's potatoes and dairy along the Aberdare mountain ranges, Nyandarua County's agricultural processors and cold-storage operators require digital platforms to connect directly with supermarket chains and urban food markets.",
        "economic_focus": "Large-scale commercial potato cultivation, milk cooling and dairy processing, cold-chain logistics, and Aberdare eco-tourism.",
        "top_searches": ["web design Nyandarua", "website developers Ol Kalou", "dairy farming website Kenya", "cold storage logistics website"]
    },
    {
        "code": "019",
        "name": "Nyeri",
        "slug": "web-design-nyeri",
        "region": "Central",
        "seat": "Nyeri Town",
        "towns": ["Nyeri Town", "Karatina", "Othaya", "Mukurweini", "Tetu", "Mweiga"],
        "tagline": "Karatina Commercial Trading, Specialty Coffee, Tea & Eco-Lodge Web Portals",
        "desc": "Nyeri County blends deep agricultural wealth in high-grade Arabica coffee and tea with the famous Karatina Open Air Market—one of the largest in sub-Saharan Africa. Our websites help Nyeri exporters, colleges, private hospitals, and safari lodges establish authoritative web dominance.",
        "economic_focus": "Specialty export coffee and tea factories, Karatina wholesale agricultural trade, Aberdare luxury safari lodges, and private medical centers.",
        "top_searches": ["web design Nyeri", "website developers in Nyeri", "web design Karatina", "hotel website Nyeri", "specialty coffee website Kenya"]
    },
    {
        "code": "020",
        "name": "Kirinyaga",
        "slug": "web-design-kirinyaga",
        "region": "Central",
        "seat": "Kerugoya / Kutus",
        "towns": ["Kerugoya", "Kutus", "Sagana", "Wang'uru (Mwea)", "Kagio"],
        "tagline": "Mwea Rice Agribusiness, Sagana River Adventure Tourism & Coffee Web Design",
        "desc": "Kirinyaga is the epicenter of Kenya's pishori rice industry at Mwea and the adventure sports capital of East Africa at Sagana (white-water rafting, bungee jumping, and luxury river camps). We engineer booking platforms and direct farm-to-consumer e-commerce websites with automated M-Pesa.",
        "economic_focus": "Mwea pishori rice milling and national distribution, Sagana extreme adventure tourism and water sports, tea factories, and horticulture.",
        "top_searches": ["web design Kirinyaga", "web design Sagana", "web design Kerugoya", "adventure tour website Kenya", "rice e-commerce website Mwea"]
    },
    {
        "code": "021",
        "name": "Murang'a",
        "slug": "web-design-muranga",
        "region": "Central",
        "seat": "Murang'a Town",
        "towns": ["Murang'a Town", "Kenol", "Thika Greens", "Kangema", "Kiriaini", "Maragua"],
        "tagline": "Hass Avocado Exports, Real Estate Boom at Kenol & Agribusiness Portals",
        "desc": "Led by booming real estate expansion along the dual-carriageway at Kenol and world-class Hass avocado export packhouses, Murang'a is an economic dynamo. We build high-converting real estate websites and agribusiness portals with full GlobalGAP certification showcases.",
        "economic_focus": "Hass avocado international exports, real estate and gated communities at Kenol, dairy production, macadamia processing, and coffee cooperatives.",
        "top_searches": ["web design Muranga", "web design Kenol", "website developers Muranga", "avocado exporter website", "real estate web design Kenol"]
    },
    {
        "code": "022",
        "name": "Kiambu",
        "slug": "web-design-kiambu",
        "region": "Central",
        "seat": "Kiambu Town",
        "towns": ["Thika", "Ruiru", "Juja", "Kikuyu", "Limuru", "Kiambu Town", "Gatundu", "Karuri"],
        "tagline": "Industrial Parks, Tech Hubs, Coffee Estates & Real Estate Commercial Websites",
        "desc": "Kiambu County is Nairobi's premier industrial and residential twin, hosting massive manufacturing and warehouse zones in Ruiru and Thika, tech hubs around Juja, and high-end residential estates in Kikuyu and Limuru. Our local engineering provides lightning-fast websites that dominate Google search across Kiambu.",
        "economic_focus": "Heavy manufacturing and warehousing (Tatu City, Thika), real estate developments, university tech ecosystems (JKUAT Juja), tea/coffee estates, and retail malls.",
        "top_searches": ["web design Kiambu", "web design Thika", "website design Ruiru", "web design Juja", "website developers Kikuyu", "web design firms in Kiambu"]
    },
    {
        "code": "023",
        "name": "Turkana",
        "slug": "web-design-turkana",
        "region": "Rift Valley",
        "seat": "Lodwar",
        "towns": ["Lodwar", "Kakuma", "Lokichogio", "Kalokol", "Lokichar"],
        "tagline": "Energy & Oil Exploration, Lake Turkana Fisheries & NGO Operations Web Portals",
        "desc": "Turkana is a dynamic frontier economy centered on oil exploration in the South Lokichar basin, solar/geothermal installations, humanitarian logistics at Kakuma, and Lake Turkana fisheries at Kalokol. We build professional corporate and contractor websites that meet rigorous international procurement standards.",
        "economic_focus": "Oil and gas exploration logistics, humanitarian NGO supply contracts, solar mini-grids, Lake Turkana fish processing, and mineral mining.",
        "top_searches": ["web design Lodwar", "website developers Turkana", "NGO contractor website Kenya", "logistics website Lodwar"]
    },
    {
        "code": "024",
        "name": "West Pokot",
        "slug": "web-design-west-pokot",
        "region": "Rift Valley",
        "seat": "Kapenguria",
        "towns": ["Kapenguria", "Makutano", "Chepareria", "Ortum", "Alale"],
        "tagline": "Cement Manufacturing, Gold Mining Support & Pastoral Agribusiness Websites",
        "desc": "Driven by Ortum cement manufacturing, commercial gold mining exploration, and extensive livestock trading at Makutano, West Pokot enterprises benefit immensely from a professional online presence that reaches buyers across the East African Community.",
        "economic_focus": "Cement manufacturing, artisanal gold mining support, commercial livestock auctions, onion farming, and honey production.",
        "top_searches": ["web design Kapenguria", "website developers West Pokot", "mining supplier website Kenya", "livestock marketing website"]
    },
    {
        "code": "025",
        "name": "Samburu",
        "slug": "web-design-samburu",
        "region": "Rift Valley",
        "seat": "Maralal",
        "towns": ["Maralal", "Archer's Post", "Baragoi", "Wamba", "South Horr"],
        "tagline": "Luxury Safari Conservancies, Maralal Camel Derby & Eco-Tourism Web Portals",
        "desc": "Home to the world-renowned Samburu National Reserve, community wildlife conservancies, and the annual Maralal Camel Derby, Samburu County is a global destination for discerning travelers. We build high-end lodge and safari booking websites with multi-currency payment integrations.",
        "economic_focus": "Luxury wildlife safari lodges, community conservation tourism, cultural artifacts, and livestock trade.",
        "top_searches": ["web design Samburu", "safari lodge website Samburu", "hotel website Maralal", "tour operator website Samburu"]
    },
    {
        "code": "026",
        "name": "Trans Nzoia",
        "slug": "web-design-trans-nzoia",
        "region": "Rift Valley",
        "seat": "Kitale",
        "towns": ["Kitale", "Kiminini", "Endebess", "Cherangany", "Saboti"],
        "tagline": "Kenya's Maize & Seed Production Capital, Agro-Machinery & Dairy Web Design",
        "desc": "Kitale and Trans Nzoia County represent the undisputed breadbasket for seed production and commercial grain farming in Kenya. We equip agro-machinery suppliers, seed stockists, farm input distributors, and private schools with conversion-driven websites.",
        "economic_focus": "Commercial seed maize production, agricultural machinery dealership, large-scale dairy farming, horticulture, and private education.",
        "top_searches": ["web design Kitale", "website developers in Kitale", "agro machinery website Kenya", "seed company website Kitale"]
    },
    {
        "code": "027",
        "name": "Uasin Gishu",
        "slug": "web-design-uasin-gishu",
        "region": "Rift Valley",
        "seat": "Eldoret City",
        "towns": ["Eldoret City", "Annex", "Turbo", "Moiben", "Burnt Forest", "Soy"],
        "tagline": "Eldoret City Medical Hub, Sports Tourism, Grain Trade & Aviation Web Solutions",
        "desc": "Now officially Kenya's newest City, Eldoret is the commercial heartbeat of the North Rift, hosting premier national referral hospitals, international sports training camps, an international cargo airport, and thriving agricultural trade. We build enterprise-grade web applications and commercial websites for Eldoret's rapid corporate expansion.",
        "economic_focus": "Regional healthcare referral hubs and private clinics, international athletics sports tourism, large-scale cereal trade, Eldoret cargo aviation, and real estate.",
        "top_searches": ["web design Eldoret", "website developers in Eldoret", "clinic website design Eldoret", "hospital website Eldoret", "real estate web design Eldoret"]
    },
    {
        "code": "028",
        "name": "Elgeyo-Marakwet",
        "slug": "web-design-elgeyo-marakwet",
        "region": "Rift Valley",
        "seat": "Iten",
        "towns": ["Iten", "Kapsowar", "Tambach", "Tot", "Chepkorio"],
        "tagline": "Home of Champions Athletics Training, Fluorspar & Kerio Valley Eco-Tourism",
        "desc": "Known globally as the 'Home of Champions', Iten attracts Olympic champions and international sports tourists year-round. Our bespoke websites equip high-altitude training camps, paragliding adventure operators, and Kerio Valley fruit processors with direct booking and international payment systems.",
        "economic_focus": "High-altitude athletics training camps, Kerio Valley adventure tourism, mango and fruit processing, and fluorspar mining support.",
        "top_searches": ["web design Iten", "athletics training camp website", "website developers Iten", "tour website Kerio Valley"]
    },
    {
        "code": "029",
        "name": "Nandi",
        "slug": "web-design-nandi",
        "region": "Rift Valley",
        "seat": "Kapsabet",
        "towns": ["Kapsabet", "Nandi Hills", "Mosoriot", "Chepterit", "Kobujoi"],
        "tagline": "Multinational Tea Plantations, Dairy Farming & Sports Excellence Web Design",
        "desc": "Blanketed in lush tea estates across Nandi Hills and anchored by Kapsabet's booming commerce and athletics training centers, Nandi County combines agricultural strength with elite sports talent. We build corporate websites for tea factories, dairy processors, and hospitality venues.",
        "economic_focus": "Commercial tea estate processing and export, dairy farming cooperatives, athletics training camps, and eco-tourism.",
        "top_searches": ["web design Kapsabet", "web design Nandi Hills", "tea estate website Kenya", "dairy cooperative website Nandi"]
    },
    {
        "code": "030",
        "name": "Baringo",
        "slug": "web-design-baringo",
        "region": "Rift Valley",
        "seat": "Kabarnet",
        "towns": ["Kabarnet", "Eldama Ravine", "Marigat", "Mogotio", "Chemolingot"],
        "tagline": "Lake Baringo & Bogoria Eco-Tourism, Geothermal Energy & Organic Honey Websites",
        "desc": "Famous for flamingos at Lake Bogoria, hot springs, geothermal power exploration, and pure Acacia honey, Baringo County is prime for eco-tourism marketing and specialized agribusiness. We build responsive hotel and tour booking websites that attract international safari travelers.",
        "economic_focus": "Lake Bogoria and Lake Baringo safari tourism, geothermal exploration support, Acacia honey packaging, and commercial livestock auctions.",
        "top_searches": ["web design Kabarnet", "web design Eldama Ravine", "hotel website Lake Baringo", "tour company website Baringo"]
    },
    {
        "code": "031",
        "name": "Laikipia",
        "slug": "web-design-laikipia",
        "region": "Rift Valley",
        "seat": "Rumuruti / Nanyuki",
        "towns": ["Nanyuki", "Nyahururu", "Rumuruti", "Doldol", "Kinamba"],
        "tagline": "Exclusive Wildlife Conservancies, High-End Safari Tourism & Ranching Websites",
        "desc": "Nanyuki is the premier safari tourism and ranching hub at the foot of Mount Kenya, housing luxury conservancies (Ol Pejeta, Lewa border), British Army training support services, and upscale lifestyle real estate. Our websites deliver world-class visual luxury, online booking, and conversion architecture.",
        "economic_focus": "Luxury private wildlife conservancies, boutique safari lodges, high-grade beef cattle ranching, floriculture, and Mount Kenya holiday homes.",
        "top_searches": ["web design Nanyuki", "website developers Nanyuki", "safari lodge website Nanyuki", "real estate web design Nanyuki", "web design Nyahururu"]
    },
    {
        "code": "032",
        "name": "Nakuru",
        "slug": "web-design-nakuru",
        "region": "Rift Valley",
        "seat": "Nakuru City",
        "towns": ["Nakuru City", "Naivasha", "Gilgil", "Njoro", "Molo", "Subukia", "Rongai"],
        "tagline": "City of Nakuru Retail, Naivasha Floriculture & Lake Tourism Web Engineering",
        "desc": "Nakuru is Kenya's fourth city and a commercial juggernaut, uniting the massive export flower farms and geothermal energy plants of Naivasha with Nakuru City's industrial processing, hospitality, and grain trade. We engineer high-speed, conversion-focused websites for Nakuru enterprises looking to dominate their market.",
        "economic_focus": "Naivasha international floriculture and rose exports, conference tourism and lake resort hospitality, geothermal energy contracting, and agricultural processing.",
        "top_searches": ["web design Nakuru", "web design Naivasha", "website developers in Nakuru", "hotel website design Naivasha", "flower exporter website Kenya"]
    },
    {
        "code": "033",
        "name": "Narok",
        "slug": "web-design-narok",
        "region": "Rift Valley",
        "seat": "Narok Town",
        "towns": ["Narok Town", "Maasai Mara", "Kilgoris", "Nairagie Enkare", "Ololulung'a"],
        "tagline": "World-Famous Maasai Mara Safari Camps, Wheat Farming & Tourism Portals",
        "desc": "Home of the Eighth Wonder of the World—the Great Wildebeest Migration in the Maasai Mara—Narok is an undisputed titan of global eco-tourism, complemented by expansive commercial wheat and barley production. We build premier safari lodge and tour operator websites that convert international holiday bookings.",
        "economic_focus": "Maasai Mara luxury safari camps and game lodges, balloon safari charters, commercial wheat and barley farming, and cultural tourism.",
        "top_searches": ["web design Narok", "Maasai Mara safari website design", "hotel website Maasai Mara", "tour operator web design Narok"]
    },
    {
        "code": "034",
        "name": "Kajiado",
        "slug": "web-design-kajiado",
        "region": "Rift Valley",
        "seat": "Kajiado Town",
        "towns": ["Kitengela", "Ongata Rongai", "Ngong", "Kiserian", "Kajiado Town", "Namanga"],
        "tagline": "Metropolitan Commuter Real Estate, Industrial Manufacturing & Meat Commerce",
        "desc": "Fast-growing metropolitan hubs like Kitengela, Ongata Rongai, and Ngong make Kajiado County one of Kenya's most vibrant commercial and real estate markets. Bordering Tanzania at Namanga, Kajiado businesses require high-converting lead generation websites for property sales, clinics, and private schools.",
        "economic_focus": "Nairobi commuter residential real estate and land sales, export processing and glass manufacturing, cross-border Namanga trade, and beef value chains.",
        "top_searches": ["web design Kitengela", "web design Ongata Rongai", "web design Ngong", "real estate website design Kitengela", "website developers Kajiado"]
    },
    {
        "code": "035",
        "name": "Kericho",
        "slug": "web-design-kericho",
        "region": "Rift Valley",
        "seat": "Kericho Town",
        "towns": ["Kericho Town", "Litein", "Kipkelion", "Londiani", "Chepseon"],
        "tagline": "World Tea Capital, Specialty Agro-Processing & Commercial Enterprise Websites",
        "desc": "Kericho is the tea capital of the world, housing multinational tea plantations, automated factories, and rich agricultural commerce. We build sophisticated corporate profiles, cooperative portals, and e-commerce websites with automated M-Pesa payments for Kericho businesses.",
        "economic_focus": "Multinational commercial tea estates and black tea exports, specialty agro-processing, dairy cooperatives, forestry, and wholesale commerce.",
        "top_searches": ["web design Kericho", "website developers in Kericho", "tea factory website Kenya", "web design Litein", "agribusiness web design Kericho"]
    },
    {
        "code": "036",
        "name": "Bomet",
        "slug": "web-design-bomet",
        "region": "Rift Valley",
        "seat": "Bomet Town",
        "towns": ["Bomet Town", "Sotik", "Longisa", "Silibwet", "Mogogosiek"],
        "tagline": "Sotik Dairy Processing, High-Altitude Tea Estates & Healthcare Web Systems",
        "desc": "Bomet County is renowned for extensive tea plantations and the famous Sotik dairy and tea processing belt. With expanding regional medical referral facilities at Tenwek, Bomet businesses demand professional, accessible websites that build patient and buyer trust.",
        "economic_focus": "Sotik dairy value chains, smallholder tea factories, Tenwek medical referral support, and commercial maize farming.",
        "top_searches": ["web design Bomet", "web design Sotik", "website developers Bomet", "hospital website Bomet", "dairy processor website"]
    },
    {
        "code": "037",
        "name": "Kakamega",
        "slug": "web-design-kakamega",
        "region": "Western",
        "seat": "Kakamega Town",
        "towns": ["Kakamega Town", "Mumias", "Malava", "Butere", "Lugari", "Shinyalu"],
        "tagline": "Kakamega Tropical Rainforest Eco-Tourism, Sugar Industry & University Hub",
        "desc": "Kakamega is the commercial, administrative, and educational nucleus of Western Kenya. Hosting Masinde Muliro University and the last remaining equatorial rainforest in Kenya, Kakamega businesses need modern websites for hospitality, education, healthcare, and retail distribution.",
        "economic_focus": "Kakamega tropical rainforest eco-tourism, higher education and student housing, sugar value chain diversification, and commercial retail banking.",
        "top_searches": ["web design Kakamega", "website developers in Kakamega", "hotel website Kakamega", "school website Kakamega", "web design Mumias"]
    },
    {
        "code": "038",
        "name": "Vihiga",
        "slug": "web-design-vihiga",
        "region": "Western",
        "seat": "Mbale",
        "towns": ["Mbale", "Chavakali", "Luanda", "Hamisi", "Majengo", "Serem"],
        "tagline": "Luanda Commercial Interstate Market, High-Density Retail & Cottage Industry",
        "desc": "Centering on the thriving interstate trade at Luanda Market and strategic road connections between Kisumu and Kakamega, Vihiga County is a dense entrepreneurial ecosystem. We build fast, mobile-first websites with instant WhatsApp chat widgets to turn online traffic into direct sales.",
        "economic_focus": "Luanda market interstate trade, high-density retail, tea cultivation, cottage manufacturing, and technical education institutions.",
        "top_searches": ["web design Vihiga", "web design Luanda", "website developers Mbale", "retail website Kenya"]
    },
    {
        "code": "039",
        "name": "Bungoma",
        "slug": "web-design-bungoma",
        "region": "Western",
        "seat": "Bungoma Town",
        "towns": ["Bungoma Town", "Webuye", "Kimilili", "Chwele", "Sirisia", "Malakisi"],
        "tagline": "Chwele Agricultural Market, Webuye Industrial Parks & Cross-Border Logistics",
        "desc": "Home to Chwele—the second-largest agricultural market in Kenya—and industrial manufacturing in Webuye along the Northern Corridor highway, Bungoma County is a commercial giant. We engineer high-performing corporate websites that facilitate national produce distribution and cross-border trade.",
        "economic_focus": "Chwele fresh produce distribution, Pan-African industrial manufacturing at Webuye, sugar cane farming, and Uganda border trade connections.",
        "top_searches": ["web design Bungoma", "web design Webuye", "website developers in Bungoma", "web design Kimilili", "agribusiness website Bungoma"]
    },
    {
        "code": "040",
        "name": "Busia",
        "slug": "web-design-busia",
        "region": "Western",
        "seat": "Busia Town",
        "towns": ["Busia Town", "Malaba", "Nambale", "Funyula", "Port Victoria", "Alupe"],
        "tagline": "One-Stop Border Post Logistics, Clearing & Forwarding & Lake Victoria Fisheries",
        "desc": "Operating Kenya's two busiest international border crossings with Uganda at Busia and Malaba, this county handles the bulk of freight moving across the Great Lakes region. We build robust logistics platforms, tracking websites, and clearing firm portals that establish corporate credibility.",
        "economic_focus": "International One-Stop Border Post (OSBP) clearing & forwarding, transit logistics, Lake Victoria commercial fisheries at Port Victoria, and cross-border hospitality.",
        "top_searches": ["web design Busia", "web design Malaba", "clearing and forwarding website Kenya", "logistics website Busia"]
    },
    {
        "code": "041",
        "name": "Siaya",
        "slug": "web-design-siaya",
        "region": "Nyanza",
        "seat": "Siaya Town",
        "towns": ["Siaya Town", "Bondo", "Ugunja", "Usenge", "Yala", "Kogelo"],
        "tagline": "Lake Victoria Tilapia Fisheries, Bondo University Hub & Heritage Eco-Tourism",
        "desc": "From deep-water tilapia fishing at Usenge and Luanda Kotieno to university campus commerce at Bondo and cultural heritage tourism in Kogelo, Siaya County is expanding rapidly. We build custom websites with M-Pesa checkout, gallery showcases, and automated quotation forms.",
        "economic_focus": "Lake Victoria commercial cage aquaculture, artisanal gold mining support, tertiary education and private student hostels, and eco-heritage tourism.",
        "top_searches": ["web design Siaya", "web design Bondo", "website developers Siaya", "fisheries website Kenya", "hotel website Bondo"]
    },
    {
        "code": "042",
        "name": "Kisumu",
        "slug": "web-design-kisumu",
        "region": "Nyanza",
        "seat": "Kisumu City",
        "towns": ["Kisumu City", "Milimani", "Maseno", "Ahero", "Kondele", "Mamboleo", "Kibos"],
        "tagline": "Kisumu Port Lake Logistics, Regional Medical Hub, Hospitality & Retail Commerce",
        "desc": "As Kenya's third city and the commercial capital of the Lake Victoria Basin, Kisumu unites deep-water port logistics with premier conference hospitality, regional medical centers, and rice farming in Ahero. We develop cutting-edge web applications, hospital portals, and retail e-commerce stores for Kisumu's leading businesses.",
        "economic_focus": "Lake Victoria maritime port trade, conference tourism and upscale hotel resorts, regional healthcare referral clinics, Ahero rice irrigation, and commercial real estate.",
        "top_searches": ["web design Kisumu", "website developers in Kisumu", "hotel website design Kisumu", "e-commerce web design Kisumu", "web design company Kisumu"]
    },
    {
        "code": "043",
        "name": "Homa Bay",
        "slug": "web-design-homa-bay",
        "region": "Nyanza",
        "seat": "Homa Bay Town",
        "towns": ["Homa Bay Town", "Mbita", "Kendu Bay", "Oyugis", "Ndhiwa", "Rusinga Island"],
        "tagline": "Rusinga Island Luxury Resorts, Lake Fisheries Cold-Chain & Agribusiness",
        "desc": "Blessed with the longest shoreline on Lake Victoria and luxury island escapes on Rusinga and Mfangano Islands, Homa Bay County is a burgeoning eco-tourism and fisheries powerhouse. We build booking websites and supplier portals that connect local enterprises with national and global markets.",
        "economic_focus": "Rusinga Island boutique luxury resorts, Lake Victoria cold-chain fish processing, sugarcane value addition at Ndhiwa, and cotton agribusiness.",
        "top_searches": ["web design Homa Bay", "hotel website Rusinga Island", "website developers Homa Bay", "tour website Lake Victoria"]
    },
    {
        "code": "044",
        "name": "Migori",
        "slug": "web-design-migori",
        "region": "Nyanza",
        "seat": "Migori Town",
        "towns": ["Migori Town", "Isebania", "Rongo", "Kehancha", "Awendo", "Muhuru Bay"],
        "tagline": "Isebania Tanzania Border Trade, Commercial Gold Mining & Sugar Value Chains",
        "desc": "Positioned on the primary transit corridor between Kenya and Tanzania at Isebania, and hosting active gold mining and sugarcane processing at Awendo, Migori County is an economic dynamo. We design professional corporate and logistics websites that capture cross-border opportunities.",
        "economic_focus": "Tanzania border clearing & forwarding at Isebania, commercial gold mining support, sugar processing at Sony Sugar Awendo, and tobacco/cereal farming.",
        "top_searches": ["web design Migori", "web design Isebania", "website developers Migori", "cross border trading website Kenya"]
    },
    {
        "code": "045",
        "name": "Kisii",
        "slug": "web-design-kisii",
        "region": "Nyanza",
        "seat": "Kisii Town",
        "towns": ["Kisii Town", "Ogembo", "Suneka", "Tabaka", "Nyamache", "Keroka border"],
        "tagline": "High-Density Commercial Wholesale, Soapstone Exports & Banana Agribusiness",
        "desc": "Kisii Town is one of the highest-density commercial banking and wholesale centers in Kenya, famous worldwide for Tabaka soapstone carvings and commercial banana and tea value chains. Our e-commerce and business websites help Kisii entrepreneurs sell directly to customers in Nairobi and abroad.",
        "economic_focus": "High-density retail and wholesale commerce, Tabaka soapstone global exports, commercial banana value addition, tea factories, and private hospitals.",
        "top_searches": ["web design Kisii", "website developers in Kisii", "e-commerce website Kisii", "soapstone export website Kenya", "hospital web design Kisii"]
    },
    {
        "code": "046",
        "name": "Nyamira",
        "slug": "web-design-nyamira",
        "region": "Nyanza",
        "seat": "Nyamira Town",
        "towns": ["Nyamira Town", "Nyansiongo", "Keroka", "Manga", "Borabu"],
        "tagline": "Highland Tea Factories, Borabu Dairy Ranching & Horticulture Web Platforms",
        "desc": "With highland tea factories dotting its green hills and commercial dairy ranching in Borabu settlement schemes, Nyamira County is an agricultural powerhouse. We build modern cooperative websites and agribusiness portals with automated M-Pesa payments.",
        "economic_focus": "Smallholder and estate tea processing, Borabu commercial dairy ranching, banana horticulture, and regional cross-county wholesale at Keroka.",
        "top_searches": ["web design Nyamira", "website developers Nyamira", "tea factory website Nyamira", "dairy farming website Kenya"]
    },
    {
        "code": "047",
        "name": "Nairobi",
        "slug": "web-design-nairobi",
        "region": "Nairobi",
        "seat": "Nairobi City (Capital)",
        "towns": ["Nairobi CBD", "Westlands", "Kilimani", "Upper Hill", "Karen", "Lavington", "Gigiri", "Eastleigh", "Industrial Area"],
        "tagline": "Kenya's Capital, Regional Financial Gateway & Tech Innovation Epicenter",
        "desc": "As the economic engine of East and Central Africa and the Silicon Savannah of the continent, Nairobi hosts multinational corporate headquarters, international diplomatic missions in Gigiri, financial giants in Upper Hill, and dynamic tech startups in Kilimani and Westlands. We build premier high-performance web systems, custom SaaS applications, and e-commerce platforms engineered for competitive dominance.",
        "economic_focus": "Multinational corporate headquarters, financial services and banking, tech startups and software engineering, diplomatic and NGO agencies, and luxury real estate.",
        "top_searches": ["website developers in Nairobi", "web design companies in Kenya", "website designers in Nairobi", "web developers in Nairobi", "best web design company Nairobi", "e-commerce website design Nairobi"]
    }
]

def render_county_page(c):
    towns_list_html = "".join([f'<span class="county-town-pill inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold">📍 {t}</span>' for t in c["towns"]])
    
    # Regional neighbor counties
    same_region = [other for other in COUNTIES if other["region"] == c["region"] and other["code"] != c["code"]]
    if not same_region:
        same_region = [other for other in COUNTIES if other["code"] != c["code"]][:4]
    else:
        same_region = same_region[:4]
    
    neighbor_cards_html = "".join([
        f'''<a href="/locations/{other["slug"]}" class="p-4 rounded-2xl bg-white border border-slate-200 hover:border-blue-500 hover:shadow-md transition-all flex flex-col justify-between">
            <div>
                <span class="text-[10px] font-bold uppercase tracking-wider text-blue-600">County {other["code"]} &bull; {other["region"]}</span>
                <h4 class="font-bold text-slate-900 text-base mt-1">{other["name"]} County</h4>
                <p class="text-xs text-slate-600 mt-1 line-clamp-2">{other["tagline"]}</p>
            </div>
            <span class="text-xs font-semibold text-blue-600 mt-3 inline-flex items-center gap-1">Explore {other["name"]} &rarr;</span>
        </a>''' for other in same_region
    ])
    
    whatsapp_hero_msg = f"Hi Xclusive Tech, I'm looking for a professional website for my business in {c['name']} County ({c['seat']})."
    encoded_whatsapp_hero = urllib_quote(whatsapp_hero_msg)
    
    whatsapp_express_msg = f"Hi Xclusive Tech, I want to claim the KES 15,000 Express Landing Page package for my business in {c['name']} County."
    encoded_whatsapp_express = urllib_quote(whatsapp_express_msg)

    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Web Design in {c["name"]} County | Top Website Developers {c["seat"]} — Xclusive Tech</title>
    <meta name="description" content="Looking for trusted website developers in {c["name"]} County? Xclusive Tech builds mobile-first websites from KES 15,000 with Daraja M-Pesa checkout, local SEO, and custom UI/UX for businesses in {", ".join(c["towns"][:4])}.">
    <meta name="keywords" content="{", ".join(c["top_searches"])}, web design kenya, website developers in {c["name"].lower()}">
    <meta name="author" content="Xclusive Tech">
    <link rel="canonical" href="https://www.xclusivetech.co.ke/locations/{c["slug"]}">
    <link rel="describedby" href="/llms.txt">
    <link rel="alternate" type="text/markdown" href="/llms.txt" title="LLMs.txt">

    <!-- Open Graph & Social Cards -->
    <meta property="og:title" content="Web Design in {c["name"]} County | Top Website Developers — Xclusive Tech">
    <meta property="og:description" content="Award-winning website design in {c["name"]} County ({", ".join(c["towns"][:3])}). High-speed mobile sites, M-Pesa checkout, and local SEO from KES 15,000.">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://www.xclusivetech.co.ke/locations/{c["slug"]}">
    <meta property="og:image" content="../assets/images/og-preview.png">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Web Design in {c["name"]} County | Xclusive Tech">
    <meta name="twitter:description" content="Professional websites for commercial enterprises and growing businesses in {c["name"]} County from KES 15,000.">
    <meta name="twitter:image" content="../assets/images/og-preview.png">

    <!-- Theme Enforcement: Strictly Light Mode -->
    <script>
        try {{
            localStorage.removeItem('xclusive_theme');
            document.documentElement.removeAttribute('data-theme');
            document.documentElement.classList.remove('dark');
            document.documentElement.classList.add('light');
        }} catch (e) {{}}
    </script>

    <!-- Tailwind CSS & Styles (Configured to ignore OS dark mode) -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            darkMode: 'class'
        }};
        document.documentElement.classList.remove('dark');
        document.documentElement.classList.add('light');
    </script>
    <link rel="icon" href="../assets/icons/xclusivetech-favicon.svg?v=2" type="image/svg+xml">
    <link rel="icon" type="image/png" sizes="96x96" href="../assets/icons/favicon-96x96.png?v=2">
    <link rel="apple-touch-icon" sizes="180x180" href="../assets/icons/apple-touch-icon.png?v=2">
    <link rel="manifest" href="../site.webmanifest">
    <link rel="stylesheet" href="../css/styles.css?v=20260926d">

    <!-- Structured Data: LocalBusiness, Service, BreadcrumbList, FAQPage -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@graph": [
            {{
                "@type": "BreadcrumbList",
                "@id": "https://www.xclusivetech.co.ke/locations/{c["slug"]}#breadcrumb",
                "itemListElement": [
                    {{
                        "@type": "ListItem",
                        "position": 1,
                        "name": "Home",
                        "item": "https://www.xclusivetech.co.ke/"
                    }},
                    {{
                        "@type": "ListItem",
                        "position": 2,
                        "name": "Locations",
                        "item": "https://www.xclusivetech.co.ke/locations/"
                    }},
                    {{
                        "@type": "ListItem",
                        "position": 3,
                        "name": "{c["name"]} County Web Design",
                        "item": "https://www.xclusivetech.co.ke/locations/{c["slug"]}"
                    }}
                ]
            }},
            {{
                "@type": "Service",
                "@id": "https://www.xclusivetech.co.ke/locations/{c["slug"]}#service",
                "name": "Web Design & Development in {c["name"]} County",
                "serviceType": "Web Development, E-Commerce, Local SEO & UI/UX Design",
                "provider": {{
                    "@type": "LocalBusiness",
                    "name": "Xclusive Tech",
                    "telephone": "+254722753819",
                    "email": "hello@xclusivetech.co.ke",
                    "url": "https://www.xclusivetech.co.ke/",
                    "priceRange": "KES 15000 - KES 85000",
                    "address": {{
                        "@type": "PostalAddress",
                        "streetAddress": "1st Floor, Suite F8, Wood Ave, Park Apartments, Kilimani",
                        "addressLocality": "Nairobi",
                        "addressCountry": "KE"
                    }}
                }},
                "areaServed": [
                    "{c["name"]} County",
                    "{c["seat"]}",
                    {json.dumps(c["towns"])[1:-1]}
                ],
                "description": "{c["desc"]}",
                "offers": {{
                    "@type": "AggregateOffer",
                    "priceCurrency": "KES",
                    "lowPrice": "15000",
                    "highPrice": "85000",
                    "url": "https://www.xclusivetech.co.ke/pricing"
                }}
            }},
            {{
                "@type": "FAQPage",
                "@id": "https://www.xclusivetech.co.ke/locations/{c["slug"]}#faq",
                "mainEntity": [
                    {{
                        "@type": "Question",
                        "name": "How much does a website cost in {c["name"]} County?",
                        "acceptedAnswer": {{
                            "@type": "Answer",
                            "text": "Website prices for businesses in {c["name"]} County start at KES 15,000 for our high-converting Express Sales Landing Page. Full multi-page corporate sites range from KES 25,000 to KES 45,500, and comprehensive e-commerce stores with automated M-Pesa integration range from KES 72,000 to KES 85,000. All prices are transparent with zero hidden fees."
                        }}
                    }},
                    {{
                        "@type": "Question",
                        "name": "How long will it take to build a website for my {c["name"]} business?",
                        "acceptedAnswer": {{
                            "@type": "Answer",
                            "text": "Express landing pages are delivered in 3 to 5 business days. A standard 5-page business website takes 2 to 3 weeks, and an e-commerce platform with M-Pesa integration takes 4 to 6 weeks."
                        }}
                    }},
                    {{
                        "@type": "Question",
                        "name": "Can my website accept M-Pesa payments directly in {c["name"]}?",
                        "acceptedAnswer": {{
                            "@type": "Answer",
                            "text": "Yes! We integrate the official Safaricom Daraja M-Pesa API directly into your website. Your customers in {c["name"]} County and across Kenya will receive instant STK push prompts on their phones, and funds go straight to your own Till or Paybill."
                        }}
                    }},
                    {{
                        "@type": "Question",
                        "name": "Do I need to travel to Nairobi to work with Xclusive Tech?",
                        "acceptedAnswer": {{
                            "@type": "Answer",
                            "text": "No travel is required. Over 85% of our 120+ client projects across Kenya are managed seamlessly via WhatsApp, Google Meet, phone calls, and email. You will receive interactive Figma prototypes and live staging previews before launch."
                        }}
                    }}
                ]
            }}
        ]
    }}
    </script>
</head>
<body class="bg-white text-slate-900 overflow-x-hidden">

    <!-- Header & Navigation -->
    <header class="site-header">
        <nav id="navbar" class="nav-container" aria-label="Main navigation">
            <div class="nav-row">
                <!-- Logo -->
                <a href="/" class="nav-logo" aria-label="Xclusive Tech home">
                    <img src="../assets/icons/xclusivetech-header-logo-light.svg" alt="Xclusive Tech logo" class="nav-logo-img nav-logo-light" width="160" height="40">
                    <img src="../assets/icons/xclusivetech-header-logo.svg" alt="Xclusive Tech logo" class="nav-logo-img nav-logo-dark" width="160" height="40">
                </a>

                <!-- Desktop nav links -->
                <div class="nav-menu-desktop">
                    <a href="/" class="nav-link">Home</a>
                    <a href="/about" class="nav-link">About</a>
                    <a href="/services" class="nav-link">Services</a>
                    <div class="nav-dropdown">
                        <button type="button" class="nav-link" aria-expanded="false" aria-haspopup="true">
                            Solutions
                            <svg aria-hidden="true" class="w-3.5 h-3.5 transition-transform duration-200" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"/></svg>
                        </button>
                        <div class="nav-dropdown-menu">
                            <div class="nav-dropdown-inner">
                                <a href="/frostwoodcrm" class="nav-dropdown-item bg-blue-50/70 text-blue-700 font-semibold flex items-center justify-between">
                                    Frostwood CRM
                                    <span class="text-[9px] uppercase font-bold tracking-wider px-1.5 py-0.5 rounded bg-blue-600 text-white">Flagship SaaS</span>
                                </a>
                                <a href="/solutions" class="nav-dropdown-item">Solutions by Business Type</a>
                                <a href="/solutions#industries" class="nav-dropdown-item">Industries We Serve</a>
                                <a href="/locations/" class="nav-dropdown-item font-semibold text-emerald-600 flex items-center justify-between">
                                    All 47 Counties Coverage
                                    <span class="text-[9px] uppercase font-bold tracking-wider px-1.5 py-0.5 rounded bg-emerald-600 text-white">Kenya</span>
                                </a>
                            </div>
                        </div>
                    </div>
                    <a href="/pricing" class="nav-link">Pricing</a>
                    <a href="/portfolio" class="nav-link">Portfolio</a>
                    <a href="/locations/" class="nav-link active font-semibold text-blue-600" aria-current="page">Locations</a>
                    <a href="/blog/" class="nav-link">Blog</a>
                    <a href="/contact" class="nav-link">Contact</a>
                </div>

                <!-- Navigation Actions -->
                <div class="nav-actions">
                    <a href="https://wa.me/254722753819?text={encoded_whatsapp_hero}" target="_blank" rel="noopener noreferrer" class="nav-quote-btn">
                        <span>WhatsApp Us</span>
                        <svg aria-hidden="true" class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
                    </a>
                    <button type="button" id="mobile-menu-toggle" class="mobile-menu-btn" aria-label="Toggle navigation menu" aria-expanded="false" aria-controls="mobile-menu">
                        <span class="hamburger-line"></span>
                        <span class="hamburger-line"></span>
                        <span class="hamburger-line"></span>
                    </button>
                </div>
            </div>
        </nav>
    </header>

    <main class="min-h-screen">
        <!-- Hero Section -->
        <section class="py-16 md:py-24 px-4 sm:px-6 lg:px-8 bg-gradient-to-b from-blue-50/60 via-white to-white border-b border-slate-200">
            <div class="max-w-6xl mx-auto">
                <!-- Breadcrumbs -->
                <nav class="flex items-center gap-2 text-xs text-slate-500 mb-6" aria-label="Breadcrumb">
                    <a href="/" class="hover:text-blue-600 transition-colors">Home</a>
                    <span>/</span>
                    <a href="/locations/" class="hover:text-blue-600 transition-colors">Locations</a>
                    <span>/</span>
                    <span class="text-slate-800 font-medium">{c["name"]} County</span>
                </nav>

                <div class="grid lg:grid-cols-12 gap-12 items-center">
                    <div class="lg:col-span-8 space-y-6">
                        <div class="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-blue-50 border border-blue-200 text-blue-800 text-xs font-bold uppercase tracking-wider">
                            <span>📍 Serving {c["name"]} County</span>
                            <span class="w-1.5 h-1.5 rounded-full bg-blue-500"></span>
                            <span>County Code {c["code"]} &bull; {c["region"]} Region</span>
                        </div>
                        
                        <h1 class="text-3xl sm:text-4xl lg:text-5xl font-extrabold text-slate-900 tracking-tight leading-tight">
                            Website Design &amp; Digital Engineering in <span class="text-blue-600">{c["name"]} County</span>
                        </h1>
                        
                        <p class="text-lg text-slate-700 leading-relaxed">
                            {c["desc"]}
                        </p>

                        <!-- Key Towns List -->
                        <div class="space-y-2 pt-2">
                            <p class="text-xs font-bold uppercase tracking-wider text-slate-600">Coverage Across Commercial Centers &amp; Towns:</p>
                            <div class="flex flex-wrap gap-2">
                                {towns_list_html}
                            </div>
                        </div>

                        <!-- CTA Row -->
                        <div class="pt-4 flex flex-col sm:flex-row gap-4">
                            <a href="https://wa.me/254722753819?text={encoded_whatsapp_hero}" target="_blank" rel="noopener noreferrer" class="inline-flex items-center justify-center gap-2.5 px-6 py-4 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-bold text-base shadow-lg shadow-blue-600/25 transition-all">
                                <span>Get a Free Quote on WhatsApp</span>
                                <span>&rarr;</span>
                            </a>
                            <a href="/pricing" class="inline-flex items-center justify-center gap-2 px-6 py-4 rounded-xl bg-white hover:bg-slate-50 text-slate-800 font-bold text-base border border-slate-300 shadow-xs transition-all">
                                <span>View Published Pricing (from KES 15K)</span>
                            </a>
                        </div>
                    </div>

                    <!-- Highlight Card -->
                    <div class="lg:col-span-4">
                        <div class="county-highlight-card p-6 sm:p-8 space-y-6">
                            <div class="flex items-center gap-3 border-b border-slate-100 pb-4">
                                <div class="w-12 h-12 rounded-2xl bg-amber-50 text-amber-600 flex items-center justify-center text-2xl font-bold">🏆</div>
                                <div>
                                    <h3 class="font-bold text-slate-900 text-sm">Digitally Fit Award Winner</h3>
                                    <p class="text-xs text-slate-500">Top Web Firm of the Year</p>
                                </div>
                            </div>

                            <ul class="space-y-3.5 text-xs text-slate-700">
                                <li class="flex items-start gap-2.5">
                                    <svg class="w-4 h-4 text-emerald-500 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg>
                                    <span><strong class="text-slate-900">Sub-1.5s Load Times:</strong> Optimized for mobile visitors on Safaricom 4G/5G and Airtel Kenya networks</span>
                                </li>
                                <li class="flex items-start gap-2.5">
                                    <svg class="w-4 h-4 text-emerald-500 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg>
                                    <span><strong class="text-slate-900">Direct M-Pesa STK Push:</strong> Automatic customer checkout straight to your Till or Paybill</span>
                                </li>
                                <li class="flex items-start gap-2.5">
                                    <svg class="w-4 h-4 text-emerald-500 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg>
                                    <span><strong class="text-slate-900">Local SEO &amp; Google Maps:</strong> Dominate local search in {c["name"]} and nearby towns</span>
                                </li>
                                <li class="flex items-start gap-2.5">
                                    <svg class="w-4 h-4 text-emerald-500 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg>
                                    <span><strong class="text-slate-900">100% Code Ownership:</strong> No recurring builder lock-ins or monthly template rent</span>
                                </li>
                            </ul>

                            <div class="p-4 rounded-2xl bg-blue-50/80 border border-blue-100 text-xs">
                                <span class="font-bold text-blue-900">Economic Drivers in {c["name"]}:</span>
                                <p class="text-slate-700 mt-1">{c["economic_focus"]}</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Special KES 15,000 Landing Page Banner -->
        <section class="county-dark-banner py-12 px-4 sm:px-6 lg:px-8 bg-slate-900 text-white relative overflow-hidden">
            <div class="max-w-6xl mx-auto grid lg:grid-cols-12 gap-8 items-center">
                <div class="lg:col-span-8 space-y-3">
                    <span class="inline-block px-3 py-1 rounded-full bg-amber-400 text-slate-950 text-xs font-black uppercase tracking-wider">⚡ Special Offer &bull; Fastest Launch (3–5 Days)</span>
                    <h2 class="text-2xl sm:text-3xl font-extrabold text-white" style="color: #ffffff !important;">Express Sales Landing Page for {c["name"]} Businesses</h2>
                    <p class="text-slate-300 text-sm leading-relaxed" style="color: #cbd5e1 !important;">
                        Need sales inquiries and direct WhatsApp calls right now without spending KES 25K+ on a multi-page website? Includes 5 long-form conversion sections, 1-click WhatsApp inquiry widget, direct lead intake form, and sub-1.5s load speed.
                    </p>
                </div>
                <div class="lg:col-span-4 text-center lg:text-right">
                    <div class="text-3xl sm:text-4xl font-black text-amber-400 mb-2">KES 15,000</div>
                    <a href="https://wa.me/254722753819?text={encoded_whatsapp_express}" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-2 px-6 py-3.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-bold text-sm shadow-lg transition-all">
                        <span>Claim KES 15,000 Offer</span>
                        <span>&rarr;</span>
                    </a>
                    <p class="text-[11px] text-slate-400 mt-1.5" style="color: #94a3b8 !important;">Includes 100% upgrade credit guarantee</p>
                </div>
            </div>
        </section>

        <!-- Full Transparent Pricing Grid -->
        <section class="py-16 px-4 sm:px-6 lg:px-8 bg-white border-b border-slate-200">
            <div class="max-w-6xl mx-auto">
                <div class="text-center max-w-3xl mx-auto mb-12">
                    <span class="text-xs font-bold uppercase tracking-wider text-blue-600">Honest &amp; Transparent</span>
                    <h2 class="text-3xl font-bold text-slate-900 mt-1">Website Design Packages for {c["name"]} County</h2>
                    <p class="text-slate-600 text-sm mt-2">All packages include bespoke Figma UI/UX design, foundational on-page SEO, mobile responsiveness, and 100% source code ownership.</p>
                </div>

                <div class="grid md:grid-cols-3 gap-8">
                    <!-- Starter -->
                    <div class="p-6 sm:p-8 rounded-3xl bg-slate-50 border border-slate-200 flex flex-col justify-between">
                        <div>
                            <span class="text-xs font-bold uppercase tracking-widest text-blue-600">Starter Site</span>
                            <div class="text-3xl font-extrabold text-slate-900 mt-2">KES 25,000–45,500</div>
                            <p class="text-xs text-slate-500 mt-1">Delivered in 2–3 weeks</p>
                            <ul class="space-y-3 mt-6 text-sm text-slate-700">
                                <li class="flex items-start gap-2">✓ Up to 5 custom-designed pages</li>
                                <li class="flex items-start gap-2">✓ Bespoke Figma UI/UX design</li>
                                <li class="flex items-start gap-2">✓ 100% responsive mobile layout</li>
                                <li class="flex items-start gap-2">✓ WhatsApp chat widget</li>
                                <li class="flex items-start gap-2">✓ Foundational on-page SEO</li>
                            </ul>
                        </div>
                        <a href="https://wa.me/254722753819?text=Hi%20Xclusive%20Tech,%20I'm%20interested%20in%20the%20Starter%20Site%20package%20for%20my%20business%20in%20{c['name']}." target="_blank" rel="noopener noreferrer" class="mt-8 block text-center py-3 px-4 rounded-xl bg-white border border-slate-300 text-slate-900 font-bold text-sm hover:bg-slate-100 shadow-xs transition-colors">Choose Starter</a>
                    </div>

                    <!-- Business Growth -->
                    <div class="p-6 sm:p-8 rounded-3xl bg-blue-50/70 border-2 border-blue-500 flex flex-col justify-between relative shadow-xl">
                        <span class="absolute -top-3 left-1/2 -translate-x-1/2 px-3 py-1 rounded-full bg-blue-600 text-white text-[10px] font-extrabold uppercase tracking-wider">Most Popular</span>
                        <div>
                            <span class="text-xs font-bold uppercase tracking-widest text-blue-600">Business Growth</span>
                            <div class="text-3xl font-extrabold text-slate-900 mt-2">KES 49,000–62,000</div>
                            <p class="text-xs text-slate-500 mt-1">Delivered in 3–5 weeks</p>
                            <ul class="space-y-3 mt-6 text-sm text-slate-700">
                                <li class="flex items-start gap-2">✓ Up to 15 custom pages</li>
                                <li class="flex items-start gap-2">✓ Dynamic CMS blog engine</li>
                                <li class="flex items-start gap-2">✓ Advanced Local SEO &amp; Schema</li>
                                <li class="flex items-start gap-2">✓ Google Search Console setup</li>
                                <li class="flex items-start gap-2">✓ High-speed asset optimization</li>
                            </ul>
                        </div>
                        <a href="https://wa.me/254722753819?text=Hi%20Xclusive%20Tech,%20I'm%20interested%20in%20the%20Business%20Growth%20package%20for%20my%20business%20in%20{c['name']}." target="_blank" rel="noopener noreferrer" class="mt-8 block text-center py-3 px-4 rounded-xl bg-blue-600 text-white font-bold text-sm hover:bg-blue-700 shadow-md transition-colors">Choose Growth</a>
                    </div>

                    <!-- E-Commerce Pro -->
                    <div class="p-6 sm:p-8 rounded-3xl bg-slate-50 border border-slate-200 flex flex-col justify-between">
                        <div>
                            <span class="text-xs font-bold uppercase tracking-widest text-blue-600">E-Commerce Pro</span>
                            <div class="text-3xl font-extrabold text-slate-900 mt-2">KES 72,000–85,000</div>
                            <p class="text-xs text-slate-500 mt-1">Delivered in 5–7 weeks</p>
                            <ul class="space-y-3 mt-6 text-sm text-slate-700">
                                <li class="flex items-start gap-2">✓ Unlimited products &amp; categories</li>
                                <li class="flex items-start gap-2">✓ Automated Daraja M-Pesa STK Push</li>
                                <li class="flex items-start gap-2">✓ Automated PDF tax invoices</li>
                                <li class="flex items-start gap-2">✓ WhatsApp instant order alerts</li>
                                <li class="flex items-start gap-2">✓ Inventory stock control</li>
                            </ul>
                        </div>
                        <a href="https://wa.me/254722753819?text=Hi%20Xclusive%20Tech,%20I'm%20interested%20in%20an%20M-Pesa%20E-Commerce%20store%20for%20my%20business%20in%20{c['name']}." target="_blank" rel="noopener noreferrer" class="mt-8 block text-center py-3 px-4 rounded-xl bg-white border border-slate-300 text-slate-900 font-bold text-sm hover:bg-slate-100 shadow-xs transition-colors">Choose E-Commerce</a>
                    </div>
                </div>
            </div>
        </section>

        <!-- FAQs Section -->
        <section class="py-16 px-4 sm:px-6 lg:px-8 bg-slate-50 border-t border-b border-slate-200">
            <div class="max-w-4xl mx-auto">
                <div class="text-center mb-10">
                    <span class="text-xs font-bold uppercase tracking-wider text-blue-600">Frequently Asked Questions</span>
                    <h2 class="text-3xl font-bold text-slate-900 mt-1">Web Design in {c["name"]} County</h2>
                </div>

                <div class="space-y-4">
                    <div class="p-6 rounded-2xl bg-white border border-slate-200">
                        <h3 class="text-base font-bold text-slate-900">How much does a website cost in {c["name"]} County?</h3>
                        <p class="text-sm text-slate-600 mt-2 leading-relaxed">Website prices start at KES 15,000 for our Express Sales Landing Page. Multi-page business websites start at KES 25,000, and full e-commerce stores with Daraja M-Pesa integration start at KES 72,000. All prices are published transparently with zero hidden fees.</p>
                    </div>

                    <div class="p-6 rounded-2xl bg-white border border-slate-200">
                        <h3 class="text-base font-bold text-slate-900">Can I integrate M-Pesa for my customers in {c["name"]}?</h3>
                        <p class="text-sm text-slate-600 mt-2 leading-relaxed">Yes! We natively connect the official Safaricom Daraja M-Pesa API to your website. When customers buy from your site in {c["name"]} or across Kenya, they enter their phone number and receive an instant M-Pesa PIN prompt. Funds go straight to your Till or Paybill.</p>
                    </div>

                    <div class="p-6 rounded-2xl bg-white border border-slate-200">
                        <h3 class="text-base font-bold text-slate-900">Do I need to visit your Nairobi office to get started?</h3>
                        <p class="text-sm text-slate-600 mt-2 leading-relaxed">Not at all! We serve clients across all 47 counties remotely via WhatsApp, phone calls, Google Meet, and email. You will receive private Figma links to preview and approve designs before any code is built.</p>
                    </div>

                    <div class="p-6 rounded-2xl bg-white border border-slate-200">
                        <h3 class="text-base font-bold text-slate-900">Do you register .co.ke and .com domains for {c["name"]} businesses?</h3>
                        <p class="text-sm text-slate-600 mt-2 leading-relaxed">Yes. We register official .co.ke domains from KES 1,500/year and .com domains, paid directly via M-Pesa. You get complete administrative ownership of your domain credentials.</p>
                    </div>
                </div>
            </div>
        </section>

        <!-- Neighboring Counties in Region -->
        <section class="py-12 px-4 sm:px-6 lg:px-8 bg-white border-b border-slate-200">
            <div class="max-w-6xl mx-auto">
                <div class="flex items-center justify-between mb-6">
                    <div>
                        <h3 class="text-lg font-bold text-slate-900">Other Counties in the {c["region"]} Region</h3>
                        <p class="text-xs text-slate-500">Explore web design services in neighboring economic zones</p>
                    </div>
                    <a href="/locations/" class="text-xs font-bold text-blue-600 hover:underline">View All 47 Counties &rarr;</a>
                </div>
                <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
                    {neighbor_cards_html}
                </div>
            </div>
        </section>

        <!-- Direct Consultation Form Section -->
        <section class="county-dark-intake py-16 px-4 sm:px-6 lg:px-8 bg-slate-900 text-white">
            <div class="max-w-4xl mx-auto text-center space-y-6">
                <span class="inline-block px-3.5 py-1 rounded-full bg-blue-500/20 text-blue-300 text-xs font-bold uppercase tracking-wider">Direct Project Intake</span>
                <h2 class="text-3xl sm:text-4xl font-bold" style="color: #ffffff !important;">Ready to Launch Your Website in {c["name"]} County?</h2>
                <p class="text-slate-300 text-sm max-w-xl mx-auto" style="color: #cbd5e1 !important;">
                    Speak directly with lead developer Samuel Kidemi and our Nairobi engineering team. We deliver custom, high-converting websites on time and on budget.
                </p>
                <div class="pt-2 flex flex-col sm:flex-row gap-4 justify-center items-center">
                    <a href="https://wa.me/254722753819?text={encoded_whatsapp_hero}" target="_blank" rel="noopener noreferrer" class="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-8 py-4 rounded-xl bg-emerald-500 hover:bg-emerald-600 text-white font-bold text-base shadow-lg transition-all">
                        <span>Chat on WhatsApp (+254722753819)</span>
                    </a>
                    <a href="tel:+254722753819" class="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-8 py-4 rounded-xl bg-slate-800 hover:bg-slate-700 text-white font-bold text-base border border-slate-700 transition-all">
                        <span>Call Directly</span>
                    </a>
                </div>
            </div>
        </section>
    </main>

    <!-- Global Site Footer -->
    <footer class="site-footer">
        <div class="footer-container">
            <div class="footer-grid">
                <div class="footer-col">
                    <a href="/" class="footer-brand-logo" aria-label="Xclusive Tech Home">
                        <img src="../assets/icons/xclusivetech-footer-logo.svg" alt="Xclusive Tech logo" width="160" height="40" class="footer-brand-logo">
                    </a>
                    <p class="footer-desc">High-performance web applications, e-commerce storefronts, and structured local SEO engineering for ambitious enterprises across all 47 counties of Kenya.</p>
                </div>

                <div class="footer-col">
                    <h3 class="footer-heading">Navigation</h3>
                    <ul class="footer-nav-list">
                        <li><a href="/" class="footer-nav-link">Home</a></li>
                        <li><a href="/about" class="footer-nav-link">About Company</a></li>
                        <li><a href="/services" class="footer-nav-link">Engineering Services</a></li>
                        <li><a href="/frostwoodcrm" class="footer-nav-link font-semibold text-blue-400">Frostwood CRM</a></li>
                        <li><a href="/solutions" class="footer-nav-link">Solutions</a></li>
                        <li><a href="/locations/" class="footer-nav-link font-semibold text-emerald-400">All 47 Counties</a></li>
                        <li><a href="/pricing" class="footer-nav-link">Milestone Pricing</a></li>
                        <li><a href="/portfolio" class="footer-nav-link">Client Portfolio</a></li>
                        <li><a href="/blog/" class="footer-nav-link">Technical Blog</a></li>
                        <li><a href="/contact" class="footer-nav-link">Contact Intake</a></li>
                    </ul>
                </div>

                <div class="footer-col">
                    <h3 class="footer-heading">Services</h3>
                    <ul class="footer-nav-list">
                        <li><a href="/services" class="footer-nav-link">Web Design &amp; UI/UX</a></li>
                        <li><a href="/services" class="footer-nav-link">Full-Stack Development</a></li>
                        <li><a href="/services" class="footer-nav-link">E-commerce &amp; M-Pesa</a></li>
                        <li><a href="/services" class="footer-nav-link">SEO, GEO &amp; AEO Schema</a></li>
                        <li><a href="/pricing" class="footer-nav-link">Express KES 15,000 Offer</a></li>
                    </ul>
                </div>

                <div class="footer-col">
                    <h3 class="footer-heading">Office &amp; Contact</h3>
                    <ul class="footer-nav-list">
                        <li class="footer-contact-item">
                            <span>1st Floor, Suite F8, Wood Ave, Park Apartments, Kilimani, Nairobi, Kenya</span>
                        </li>
                        <li><a href="mailto:hello@xclusivetech.co.ke" class="footer-nav-link">hello@xclusivetech.co.ke</a></li>
                        <li><a href="tel:+254722753819" class="footer-nav-link">+254722753819</a></li>
                    </ul>
                </div>
            </div>

            <!-- Footer Bottom Legal Bar -->
            <div class="footer-bottom-bar">
                <p>&copy; 2026 Xclusive Tech. All rights reserved. Registered web development enterprise in Kenya.</p>
                <div class="footer-bottom-links">
                    <a href="/privacy" class="footer-bottom-link">Privacy Policy</a>
                    <a href="/terms" class="footer-bottom-link">Terms of Service</a>
                    <a href="/llms.txt" class="footer-bottom-link" title="LLM Context Specification">llms.txt</a>
                </div>
            </div>
        </div>
    </footer>

    <!-- WhatsApp Floating Action Button -->
    <a href="https://wa.me/254722753819?text={encoded_whatsapp_hero}" target="_blank" rel="noopener noreferrer" class="whatsapp-float-btn" aria-label="Contact lead engineer on WhatsApp" title="Chat on WhatsApp">
        <svg aria-hidden="true" fill="currentColor" viewBox="0 0 24 24"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.67-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.076 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421-7.403h-.004c-1.025 0-2.031.313-2.891.893L9.9 4.504C10.742 3.74 11.853 3.3 13.05 3.3c2.969 0 5.387 2.418 5.387 5.387 0 1.197-.46 2.307-1.224 3.15l.531 1.465c.592-.689.956-1.586.956-2.615 0-2.206-1.794-4-4-4zm0 0"/></svg>
    </a>

    <script src="../js/main.js?v=20260926d"></script>
    <script src="../js/animations.js"></script>
    <script src="../js/navigation.js"></script>
</body>
</html>'''
    return html_content

def render_locations_index():
    county_cards_html = ""
    for c in COUNTIES:
        towns_display = ", ".join(c["towns"][:3])
        county_cards_html += f'''
        <div class="county-card p-6 rounded-3xl bg-white border border-slate-200 hover:border-blue-500 hover:shadow-xl transition-all duration-300 flex flex-col justify-between" data-county="{c["name"].lower()}" data-region="{c["region"].lower()}" data-towns="{", ".join(c["towns"]).lower()}">
            <div>
                <div class="flex items-center justify-between mb-3">
                    <span class="county-card-badge px-2.5 py-1 rounded-full text-[10px] font-bold uppercase tracking-wider">County {c["code"]}</span>
                    <span class="text-xs font-semibold text-slate-500">{c["region"]}</span>
                </div>
                <h3 class="text-xl font-bold text-slate-900">{c["name"]} County</h3>
                <p class="text-xs font-medium text-blue-600 mt-0.5">Capital: {c["seat"]}</p>
                <p class="text-xs text-slate-600 mt-2.5 line-clamp-2">{c["tagline"]}</p>
                <div class="mt-3.5 pt-3 border-t border-slate-100 text-[11px] text-slate-500">
                    <strong class="text-slate-700">Key Centers:</strong> {towns_display}
                </div>
            </div>
            <a href="/locations/{c["slug"]}" class="county-card-btn mt-5 w-full text-center py-2.5 px-4 rounded-xl font-bold text-xs flex items-center justify-center gap-1.5" style="background-color: #2563eb !important; color: #ffffff !important;">
                <span style="color: #ffffff !important;">View {c["name"]} Services</span>
                <span style="color: #ffffff !important;">&rarr;</span>
            </a>
        </div>
        '''

    regions = ["All", "Nairobi", "Coast", "Central", "Rift Valley", "Western", "Nyanza", "Eastern", "North Eastern"]
    region_tabs_html = "".join([f'<button type="button" class="region-filter-btn px-4 py-2 rounded-xl text-xs font-bold transition-all {"active-tab" if r == "All" else ""}" data-region-tab="{r.lower()}">{r}</button>' for r in regions])

    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Web Design Across All 47 Counties in Kenya | Xclusive Tech</title>
    <meta name="description" content="Find trusted website developers, M-Pesa e-commerce engineers, and local SEO services across all 47 counties of Kenya. Transparent pricing from KES 15,000.">
    <meta name="keywords" content="web design kenya, website developers in kenya, web design all counties kenya, web designers nairobi, web design mombasa, web design nakuru, web design kisumu, web design eldoret">
    <meta name="author" content="Xclusive Tech">
    <link rel="canonical" href="https://www.xclusivetech.co.ke/locations/">
    <link rel="describedby" href="/llms.txt">
    <link rel="alternate" type="text/markdown" href="/llms.txt" title="LLMs.txt">

    <!-- Open Graph & Social Cards -->
    <meta property="og:title" content="Web Design Across All 47 Counties in Kenya | Xclusive Tech">
    <meta property="og:description" content="Local website design, e-commerce, and SEO services engineered for businesses across all 47 Kenyan counties. Transparent KES pricing from KES 15,000.">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://www.xclusivetech.co.ke/locations/">
    <meta property="og:image" content="../assets/images/og-preview.png">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Web Design in All 47 Counties in Kenya | Xclusive Tech">
    <meta name="twitter:description" content="Transparent website packages and local SEO engineering across Kenya.">
    <meta name="twitter:image" content="../assets/images/og-preview.png">

    <!-- Theme Enforcement: Strictly Light Mode -->
    <script>
        try {{
            localStorage.removeItem('xclusive_theme');
            document.documentElement.removeAttribute('data-theme');
            document.documentElement.classList.remove('dark');
            document.documentElement.classList.add('light');
        }} catch (e) {{}}
    </script>

    <!-- Tailwind CSS & Styles (Configured to ignore OS dark mode) -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            darkMode: 'class'
        }};
        document.documentElement.classList.remove('dark');
        document.documentElement.classList.add('light');
    </script>
    <link rel="icon" href="../assets/icons/xclusivetech-favicon.svg?v=2" type="image/svg+xml">
    <link rel="icon" type="image/png" sizes="96x96" href="../assets/icons/favicon-96x96.png?v=2">
    <link rel="apple-touch-icon" sizes="180x180" href="../assets/icons/apple-touch-icon.png?v=2">
    <link rel="manifest" href="../site.webmanifest">
    <link rel="stylesheet" href="../css/styles.css?v=20260926d">

    <!-- Structured Data: CollectionPage & BreadcrumbList -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@graph": [
            {{
                "@type": "BreadcrumbList",
                "@id": "https://www.xclusivetech.co.ke/locations/#breadcrumb",
                "itemListElement": [
                    {{
                        "@type": "ListItem",
                        "position": 1,
                        "name": "Home",
                        "item": "https://www.xclusivetech.co.ke/"
                    }},
                    {{
                        "@type": "ListItem",
                        "position": 2,
                        "name": "Locations",
                        "item": "https://www.xclusivetech.co.ke/locations/"
                    }}
                ]
            }},
            {{
                "@type": "CollectionPage",
                "@id": "https://www.xclusivetech.co.ke/locations/#webpage",
                "url": "https://www.xclusivetech.co.ke/locations/",
                "name": "Web Design Services Across All 47 Counties in Kenya",
                "description": "Comprehensive nationwide coverage of website design, e-commerce development, and local SEO for commercial enterprises in all 47 Kenyan counties.",
                "isPartOf": {{
                    "@type": "WebSite",
                    "@id": "https://www.xclusivetech.co.ke/#website",
                    "name": "Xclusive Tech"
                }}
            }}
        ]
    }}
    </script>
</head>
<body class="bg-white text-slate-900 overflow-x-hidden">

    <!-- Header & Navigation -->
    <header class="site-header">
        <nav id="navbar" class="nav-container" aria-label="Main navigation">
            <div class="nav-row">
                <a href="/" class="nav-logo" aria-label="Xclusive Tech home">
                    <img src="../assets/icons/xclusivetech-header-logo-light.svg" alt="Xclusive Tech logo" class="nav-logo-img nav-logo-light" width="160" height="40">
                    <img src="../assets/icons/xclusivetech-header-logo.svg" alt="Xclusive Tech logo" class="nav-logo-img nav-logo-dark" width="160" height="40">
                </a>

                <div class="nav-menu-desktop">
                    <a href="/" class="nav-link">Home</a>
                    <a href="/about" class="nav-link">About</a>
                    <a href="/services" class="nav-link">Services</a>
                    <div class="nav-dropdown">
                        <button type="button" class="nav-link" aria-expanded="false" aria-haspopup="true">
                            Solutions
                            <svg aria-hidden="true" class="w-3.5 h-3.5 transition-transform duration-200" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"/></svg>
                        </button>
                        <div class="nav-dropdown-menu">
                            <div class="nav-dropdown-inner">
                                <a href="/frostwoodcrm" class="nav-dropdown-item bg-blue-50/70 text-blue-700 font-semibold flex items-center justify-between">
                                    Frostwood CRM
                                    <span class="text-[9px] uppercase font-bold tracking-wider px-1.5 py-0.5 rounded bg-blue-600 text-white">Flagship SaaS</span>
                                </a>
                                <a href="/solutions" class="nav-dropdown-item">Solutions by Business Type</a>
                                <a href="/solutions#industries" class="nav-dropdown-item">Industries We Serve</a>
                                <a href="/locations/" class="nav-dropdown-item font-semibold text-emerald-600 flex items-center justify-between">
                                    All 47 Counties Coverage
                                    <span class="text-[9px] uppercase font-bold tracking-wider px-1.5 py-0.5 rounded bg-emerald-600 text-white">Kenya</span>
                                </a>
                            </div>
                        </div>
                    </div>
                    <a href="/pricing" class="nav-link">Pricing</a>
                    <a href="/portfolio" class="nav-link">Portfolio</a>
                    <a href="/locations/" class="nav-link active font-semibold text-blue-600" aria-current="page">Locations</a>
                    <a href="/blog/" class="nav-link">Blog</a>
                    <a href="/contact" class="nav-link">Contact</a>
                </div>

                <div class="nav-actions">
                    <a href="https://wa.me/254722753819?text=Hi%20Xclusive%20Tech,%20I'm%20looking%20for%20a%20website%20for%20my%20business%20in%20Kenya." target="_blank" rel="noopener noreferrer" class="nav-quote-btn">
                        <span>WhatsApp Us</span>
                        <svg aria-hidden="true" class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
                    </a>
                    <button type="button" id="mobile-menu-toggle" class="mobile-menu-btn" aria-label="Toggle navigation menu" aria-expanded="false" aria-controls="mobile-menu">
                        <span class="hamburger-line"></span>
                        <span class="hamburger-line"></span>
                        <span class="hamburger-line"></span>
                    </button>
                </div>
            </div>
        </nav>
    </header>

    <main class="min-h-screen py-16 px-4 sm:px-6 lg:px-8">
        <div class="max-w-7xl mx-auto">
            <!-- Hero Header -->
            <div class="text-center max-w-3xl mx-auto mb-12">
                <span class="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-full bg-emerald-50 text-emerald-800 border border-emerald-200 text-xs font-bold uppercase tracking-wider mb-4">
                    <span>🇰🇪 Nationwide Coverage</span>
                    <span>&bull;</span>
                    <span>All 47 Counties of Kenya</span>
                </span>
                <h1 class="text-3xl sm:text-5xl font-extrabold text-slate-900 tracking-tight">
                    Website Design Services Across Kenya
                </h1>
                <p class="text-base sm:text-lg text-slate-700 mt-4 leading-relaxed">
                    Explore tailored website development, Daraja M-Pesa integration, and local SEO engineered specifically for your county's economic landscape. Select a county below or search your town.
                </p>

                <!-- Search Input -->
                <div class="mt-8 max-w-xl mx-auto relative">
                    <input type="text" id="county-search" placeholder="Search by county name or town (e.g. Eldoret, Diani, Thika, Naivasha)..." class="w-full py-4 pl-12 pr-4 rounded-2xl bg-white border border-slate-300 text-sm text-slate-900 placeholder:text-slate-400 focus:outline-hidden focus:ring-2 focus:ring-blue-500 shadow-xs">
                    <svg class="w-5 h-5 text-slate-400 absolute left-4 top-1/2 -translate-y-1/2" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
                </div>

                <!-- Region Filter Tabs -->
                <div class="mt-6 flex flex-wrap gap-2 justify-center">
                    {region_tabs_html}
                </div>
            </div>

            <!-- County Cards Grid -->
            <div id="county-grid" class="grid sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
                {county_cards_html}
            </div>

            <!-- Empty Search State -->
            <div id="no-results" class="hidden text-center py-16">
                <p class="text-lg font-semibold text-slate-700">No matching county or town found.</p>
                <p class="text-sm text-slate-500 mt-1">Try searching for a county name (e.g. Mombasa, Nakuru) or town.</p>
            </div>
        </div>
    </main>

    <!-- Global Site Footer -->
    <footer class="site-footer">
        <div class="footer-container">
            <div class="footer-grid">
                <div class="footer-col">
                    <a href="/" class="footer-brand-logo" aria-label="Xclusive Tech Home">
                        <img src="../assets/icons/xclusivetech-footer-logo.svg" alt="Xclusive Tech logo" width="160" height="40" class="footer-brand-logo">
                    </a>
                    <p class="footer-desc">High-performance web applications, e-commerce storefronts, and structured local SEO engineering for ambitious enterprises across all 47 counties of Kenya.</p>
                </div>

                <div class="footer-col">
                    <h3 class="footer-heading">Navigation</h3>
                    <ul class="footer-nav-list">
                        <li><a href="/" class="footer-nav-link">Home</a></li>
                        <li><a href="/about" class="footer-nav-link">About Company</a></li>
                        <li><a href="/services" class="footer-nav-link">Engineering Services</a></li>
                        <li><a href="/frostwoodcrm" class="footer-nav-link font-semibold text-blue-400">Frostwood CRM</a></li>
                        <li><a href="/solutions" class="footer-nav-link">Solutions</a></li>
                        <li><a href="/locations/" class="footer-nav-link font-semibold text-emerald-400">All 47 Counties</a></li>
                        <li><a href="/pricing" class="footer-nav-link">Milestone Pricing</a></li>
                        <li><a href="/portfolio" class="footer-nav-link">Client Portfolio</a></li>
                        <li><a href="/blog/" class="footer-nav-link">Technical Blog</a></li>
                        <li><a href="/contact" class="footer-nav-link">Contact Intake</a></li>
                    </ul>
                </div>

                <div class="footer-col">
                    <h3 class="footer-heading">Services</h3>
                    <ul class="footer-nav-list">
                        <li><a href="/services" class="footer-nav-link">Web Design &amp; UI/UX</a></li>
                        <li><a href="/services" class="footer-nav-link">Full-Stack Development</a></li>
                        <li><a href="/services" class="footer-nav-link">E-commerce &amp; M-Pesa</a></li>
                        <li><a href="/services" class="footer-nav-link">SEO, GEO &amp; AEO Schema</a></li>
                        <li><a href="/pricing" class="footer-nav-link">Express KES 15,000 Offer</a></li>
                    </ul>
                </div>

                <div class="footer-col">
                    <h3 class="footer-heading">Office &amp; Contact</h3>
                    <ul class="footer-nav-list">
                        <li class="footer-contact-item">
                            <span>1st Floor, Suite F8, Wood Ave, Park Apartments, Kilimani, Nairobi, Kenya</span>
                        </li>
                        <li><a href="mailto:hello@xclusivetech.co.ke" class="footer-nav-link">hello@xclusivetech.co.ke</a></li>
                        <li><a href="tel:+254722753819" class="footer-nav-link">+254722753819</a></li>
                    </ul>
                </div>
            </div>

            <!-- Footer Bottom Legal Bar -->
            <div class="footer-bottom-bar">
                <p>&copy; 2026 Xclusive Tech. All rights reserved. Registered web development enterprise in Kenya.</p>
                <div class="footer-bottom-links">
                    <a href="/privacy" class="footer-bottom-link">Privacy Policy</a>
                    <a href="/terms" class="footer-bottom-link">Terms of Service</a>
                    <a href="/llms.txt" class="footer-bottom-link" title="LLM Context Specification">llms.txt</a>
                </div>
            </div>
        </div>
    </footer>

    <!-- Interactive Client Filtering Script -->
    <script>
        document.addEventListener('DOMContentLoaded', function() {{
            const searchInput = document.getElementById('county-search');
            const regionButtons = document.querySelectorAll('.region-filter-btn');
            const cards = document.querySelectorAll('.county-card');
            const noResults = document.getElementById('no-results');
            let currentRegion = 'all';

            function filterCards() {{
                const query = searchInput.value.toLowerCase().trim();
                let visibleCount = 0;

                cards.forEach(card => {{
                    const county = card.getAttribute('data-county');
                    const region = card.getAttribute('data-region');
                    const towns = card.getAttribute('data-towns');

                    const matchesSearch = !query || county.includes(query) || towns.includes(query);
                    const matchesRegion = (currentRegion === 'all') || (region === currentRegion);

                    if (matchesSearch && matchesRegion) {{
                        card.style.display = 'flex';
                        visibleCount++;
                    }} else {{
                        card.style.display = 'none';
                    }}
                }});

                if (visibleCount === 0) {{
                    noResults.classList.remove('hidden');
                }} else {{
                    noResults.classList.add('hidden');
                }}
            }}

            searchInput.addEventListener('input', filterCards);

            regionButtons.forEach(btn => {{
                btn.addEventListener('click', function() {{
                    regionButtons.forEach(b => b.classList.remove('active-tab'));
                    this.classList.add('active-tab');
                    currentRegion = this.getAttribute('data-region-tab');
                    filterCards();
                }});
            }});
        }});
    </script>

    <script src="../js/main.js?v=20260926d"></script>
    <script src="../js/animations.js"></script>
    <script src="../js/navigation.js"></script>
</body>
</html>'''
    return html_content

def urllib_quote(s):
    import urllib.parse
    return urllib.parse.quote(s)

def main():
    print(f"Generating 47 county landing pages in {LOCATIONS_DIR}...")
    for county in COUNTIES:
        filepath = os.path.join(LOCATIONS_DIR, f"{county['slug']}.html")
        content = render_county_page(county)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  -> Generated {county['slug']}.html (County {county['code']} - {county['name']})")

    print("\nGenerating County Directory Index at /locations/index.html...")
    index_filepath = os.path.join(LOCATIONS_DIR, "index.html")
    index_content = render_locations_index()
    with open(index_filepath, "w", encoding="utf-8") as f:
        f.write(index_content)
    print("  -> Generated locations/index.html successfully!")

    print(f"\nTotal 48 files generated in {LOCATIONS_DIR} successfully!")

if __name__ == '__main__':
    main()
