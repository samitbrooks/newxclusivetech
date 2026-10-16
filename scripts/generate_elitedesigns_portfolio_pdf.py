#!/usr/bin/env python3
"""
Elite Designs Kenya — Official Client Portfolio & Case Studies PDF Generator
Generated exclusively with ReportLab (No Chromium).
Branded with official Elite Designs logo and colors derived from logo:
- Primary: #3600DF (Electric Royal Indigo)
- Accent: #F22732 (Vibrant Crimson)
- Dark: #0F172A (Deep Slate/Charcoal)
- Muted: #475569 (Cool Grey)
- Card Bg: #F8FAFC / Border: #E2E8F0
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas
from PIL import Image as PILImage

# Brand Palette derived from official Elite Designs logo
C_PRIMARY = colors.HexColor('#3600DF')      # Vibrant Royal Indigo
C_PRIMARY_DARK = colors.HexColor('#240099') # Deep Indigo
C_PRIMARY_LIGHT = colors.HexColor('#EEF2FF')# Soft Indigo Tint
C_ACCENT = colors.HexColor('#F22732')       # Energetic Crimson Red
C_ACCENT_LIGHT = colors.HexColor('#FFF1F2') # Soft Rose Tint
C_DARK = colors.HexColor('#0F172A')         # Slate 900
C_BODY = colors.HexColor('#334155')         # Slate 700
C_MUTED = colors.HexColor('#64748B')        # Slate 500
C_BORDER = colors.HexColor('#E2E8F0')       # Slate 200
C_CARD_BG = colors.HexColor('#F8FAFC')      # Slate 50
C_WHITE = colors.HexColor('#FFFFFF')
C_GREEN = colors.HexColor('#059669')

LOGO_PATH = 'assets/images/elitedesigns_logo.png'
OUTPUT_PDF = 'Elite_Designs_Portfolio_2026.pdf'
ASSETS_DIR = 'assets/images/portfolio_pdf'

PAGE_WIDTH, PAGE_HEIGHT = A4 # 595.27 x 841.89 pt
MARGIN_LEFT = 36
MARGIN_RIGHT = 36
MARGIN_TOP = 40
MARGIN_BOTTOM = 40
CONTENT_WIDTH = PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT # 523.27 pt

class EliteNumberedCanvas(canvas.Canvas):
    """Two-pass canvas for total page count and professional running headers/footers."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, total_pages):
        page_num = self._pageNumber

        # Cover Page (Page 1) Header & Footer
        if page_num == 1:
            # Top decorative stripes
            self.setFillColor(C_PRIMARY)
            self.rect(0, PAGE_HEIGHT - 6, PAGE_WIDTH, 6, fill=1, stroke=0)
            self.setFillColor(C_ACCENT)
            self.rect(0, PAGE_HEIGHT - 9, PAGE_WIDTH * 0.35, 3, fill=1, stroke=0)

            # Bottom stripe
            self.setFillColor(C_PRIMARY)
            self.rect(0, 0, PAGE_WIDTH, 6, fill=1, stroke=0)
            self.setFillColor(C_ACCENT)
            self.rect(PAGE_WIDTH * 0.65, 0, PAGE_WIDTH * 0.35, 6, fill=1, stroke=0)
            return

        # Running Header (Pages 2+)
        self.saveState()
        # Top gradient-like bar
        self.setFillColor(C_PRIMARY)
        self.rect(0, PAGE_HEIGHT - 4, PAGE_WIDTH, 4, fill=1, stroke=0)
        self.setFillColor(C_ACCENT)
        self.rect(0, PAGE_HEIGHT - 6, 120, 2, fill=1, stroke=0)

        # Header content
        header_y = PAGE_HEIGHT - 30
        if os.path.exists(LOGO_PATH):
            self.drawImage(LOGO_PATH, MARGIN_LEFT, header_y - 2, width=80, height=20, preserveAspectRatio=True, mask='auto')

        self.setFont('Helvetica-Bold', 8)
        self.setFillColor(C_PRIMARY)
        self.drawRightString(PAGE_WIDTH - MARGIN_RIGHT, header_y + 6, "ELITE DESIGNS KENYA • CLIENT PORTFOLIO")
        
        self.setFont('Helvetica', 7.5)
        self.setFillColor(C_MUTED)
        self.drawRightString(PAGE_WIDTH - MARGIN_RIGHT, header_y - 3, "High-Impact NGOs, Healthcare Societies & Enterprise Platforms")

        # Header divider line
        self.setStrokeColor(C_BORDER)
        self.setLineWidth(0.75)
        self.line(MARGIN_LEFT, header_y - 8, PAGE_WIDTH - MARGIN_RIGHT, header_y - 8)

        # Running Footer
        footer_y = 22
        self.setStrokeColor(C_BORDER)
        self.setLineWidth(0.75)
        self.line(MARGIN_LEFT, footer_y + 12, PAGE_WIDTH - MARGIN_RIGHT, footer_y + 12)

        self.setFont('Helvetica', 8)
        self.setFillColor(C_MUTED)
        # Footer Text
        self.drawString(MARGIN_LEFT, footer_y, "www.elitedesigns.co.ke  •  hello@elitedesigns.co.ke  •  Nairobi, Kenya")

        page_str = f"Page {page_num} of {total_pages}"
        self.setFont('Helvetica-Bold', 8)
        self.setFillColor(C_PRIMARY)
        self.drawRightString(PAGE_WIDTH - MARGIN_RIGHT, footer_y, page_str)

        self.restoreState()


def build_portfolio_pdf():
    os.makedirs(os.path.dirname(OUTPUT_PDF) or '.', exist_ok=True)
    doc = SimpleDocTemplate(
        OUTPUT_PDF,
        pagesize=A4,
        leftMargin=MARGIN_LEFT,
        rightMargin=MARGIN_RIGHT,
        topMargin=MARGIN_TOP,
        bottomMargin=MARGIN_BOTTOM
    )

    styles = getSampleStyleSheet()

    # Custom typography styles
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=C_DARK,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=C_PRIMARY,
        spaceAfter=15
    )

    section_header_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=C_DARK,
        spaceBefore=8,
        spaceAfter=3
    )

    section_desc_style = ParagraphStyle(
        'SectionDesc',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=C_MUTED,
        spaceAfter=10
    )

    project_title_style = ParagraphStyle(
        'ProjectTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=C_DARK,
        spaceAfter=2
    )

    project_category_style = ParagraphStyle(
        'ProjectCategory',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=10,
        textColor=C_PRIMARY,
        spaceAfter=4
    )

    project_desc_style = ParagraphStyle(
        'ProjectDesc',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.2,
        leading=11.5,
        textColor=C_BODY,
        spaceAfter=5
    )

    project_tags_style = ParagraphStyle(
        'ProjectTags',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.2,
        leading=9.5,
        textColor=C_MUTED,
        spaceAfter=6
    )

    story = []

    # =========================================================================
    # PAGE 1: COVER PAGE
    # =========================================================================
    story.append(Spacer(1, 15))

    # Logo row
    if os.path.exists(LOGO_PATH):
        story.append(RLImage(LOGO_PATH, width=175, height=44, kind='proportional'))
    else:
        story.append(Paragraph("<b><font color='#3600df' size='22'>ELITE DESIGNS</font></b>", title_style))
    story.append(Spacer(1, 15))

    # Badge Pill: 2026 OFFICIAL PORTFOLIO & CASE STUDIES
    badge_html = f"""
    <font color="#3600df"><b>OFFICIAL PORTFOLIO &amp; SHOWCASE</b></font>
    &nbsp;&nbsp;•&nbsp;&nbsp;
    <font color="#64748b">EAST AFRICA &amp; GLOBAL IMPACT</font>
    """
    badge_table = Table([[Paragraph(badge_html, ParagraphStyle('BStyle', fontName='Helvetica-Bold', fontSize=8, leading=10, textColor=C_PRIMARY))]],
                        colWidths=[CONTENT_WIDTH])
    badge_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), C_PRIMARY_LIGHT),
        ('BOX', (0, 0), (-1, -1), 0.75, C_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ]))
    story.append(badge_table)
    story.append(Spacer(1, 14))

    # Title & Subtitle
    story.append(Paragraph("High-Impact Digital Platforms for NGOs, Non-Profits &amp; Leading Kenyan Enterprises", title_style))
    story.append(Paragraph("Strategic Web Architecture • Donor &amp; Stakeholder Credibility • Enterprise Scalability", subtitle_style))

    # Executive Overview Card
    overview_text = """
    <b>Elite Designs Kenya</b> is a premier digital agency in Nairobi recognized for building robust, secure, and conversion-focused web platforms. We specialize in engineering <b>donor-credible web ecosystems for international NGOs, health research societies, community organizations, and growth-driven corporate institutions</b> across Kenya and the broader African continent.<br/><br/>
    Each platform in this showcase is engineered for <b>exceptional speed, mobile responsiveness, M-Pesa/card donation processing, stakeholder transparency, and high search visibility (SEO &amp; AEO)</b>. Below is a curated selection of our live portfolio projects with direct clickable links to inspect each website.
    """
    overview_p = Paragraph(overview_text, ParagraphStyle('ExecP', fontName='Helvetica', fontSize=8.8, leading=13, textColor=C_BODY))
    overview_table = Table([[overview_p]], colWidths=[CONTENT_WIDTH])
    overview_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), C_CARD_BG),
        ('BOX', (0, 0), (-1, -1), 1, C_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ]))
    story.append(overview_table)
    story.append(Spacer(1, 14))

    # Key Metrics Bar (4 Columns)
    kpis = [
        ("<b>120+</b>", "Platforms Delivered"),
        ("<b>99.9%</b>", "Uptime & Reliability"),
        ("<b>&lt; 1.5s</b>", "Mobile Page Speeds"),
        ("<b>5★ Rated</b>", "Digitally Fit Nominee")
    ]
    kpi_cells = []
    for num, lbl in kpis:
        cell_p = Paragraph(f"<font color='#3600df' size='13'>{num}</font><br/><font color='#64748b' size='7'>{lbl}</font>", 
                           ParagraphStyle('KPICell', alignment=1, leading=10))
        kpi_cells.append(cell_p)
    kpi_table = Table([kpi_cells], colWidths=[CONTENT_WIDTH/4.0]*4)
    kpi_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#FAFAFA')),
        ('BOX', (0, 0), (-1, -1), 0.5, C_BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, C_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ]))
    story.append(kpi_table)
    story.append(Spacer(1, 14))

    # Table of Contents / Showcase Overview
    toc_html = """
    <b>PORTFOLIO CONTENTS AT A GLANCE:</b><br/>
    <b>• Section 1 (Pages 2–5):</b> <b>NGOs, Non-Profits, Global Health &amp; Community Foundations</b> (Primary Highlights: <i>RBA Initiative, OPSOK, CAK, Teria CBO, SEDHURO, GHSD, Israel Universal Church, Transformation Ark Hub</i>)<br/>
    <b>• Section 2 (Page 6):</b> <b>Healthcare Societies, Clinical Institutions &amp; Higher Education</b> (<i>GLUK Dentistry, Numeru Institute, Purymax Therapy</i>)<br/>
    <b>• Section 3 (Page 7):</b> <b>Renewable Energy, Corporate, Legal &amp; Digital Platforms</b> (<i>Greenhunt Energy, Lusweti &amp; Nabutola, Kenya Remote Jobs, Sherrane Homes, Billan Beauty</i>)<br/>
    <b>• Section 4 (Page 8):</b> <b>Why Leading Organizations Choose Elite Designs &amp; Next Steps</b>
    """
    story.append(Paragraph(toc_html, ParagraphStyle('TOC', fontName='Helvetica', fontSize=8, leading=12, textColor=C_BODY)))
    story.append(Spacer(1, 12))

    # Contact & Agency Credentials Bar
    cred_html = """
    <b>Agency:</b> Elite Designs Kenya &nbsp;&nbsp;|&nbsp;&nbsp; 
    <b>Web:</b> <a href="https://www.elitedesigns.co.ke" color="#3600df"><b>www.elitedesigns.co.ke</b></a> &nbsp;&nbsp;|&nbsp;&nbsp; 
    <b>Email:</b> <a href="mailto:hello@elitedesigns.co.ke" color="#3600df">hello@elitedesigns.co.ke</a> &nbsp;&nbsp;|&nbsp;&nbsp; 
    <b>Hotline:</b> +254 722 753 819
    """
    story.append(Paragraph(cred_html, ParagraphStyle('Cred', fontName='Helvetica', fontSize=7.8, leading=10, textColor=C_MUTED, alignment=1)))

    story.append(PageBreak())

    # =========================================================================
    # PROJECT CARD HELPER FUNCTION
    # =========================================================================
    def create_project_card(p_data):
        img_file = os.path.join(ASSETS_DIR, f"{p_data['key']}.png")
        if not os.path.exists(img_file):
            img_file = os.path.join('assets/images/portfolio', f"{p_data['key']}.png")

        # Image Flowable
        if os.path.exists(img_file):
            img_flow = RLImage(img_file, width=195, height=122, kind='proportional')
        else:
            img_flow = Paragraph(f"<b>[Image: {p_data['key']}]</b>", project_title_style)

        # Right Column Content
        content_cells = []
        
        # Tag & Title
        content_cells.append(Paragraph(f"<font color='#3600df'><b>[ {p_data['category'].upper()} ]</b></font>", project_category_style))
        content_cells.append(Paragraph(f"<b>{p_data['title']}</b>", project_title_style))
        content_cells.append(Spacer(1, 2))
        
        # Description
        content_cells.append(Paragraph(p_data['description'], project_desc_style))
        
        # Key Features / Highlights
        feats_html = "<b>Key Deliverables:</b> " + " &bull; ".join(p_data['highlights'])
        content_cells.append(Paragraph(feats_html, project_tags_style))
        content_cells.append(Spacer(1, 3))
        
        # Clickable Live Link Button (Standard ASCII & HTML Entities for Universal PDF Compatibility)
        url = p_data['url']
        link_btn_html = f"""
        <font color="#ffffff"><b>&nbsp;&nbsp;VISIT LIVE PLATFORM: {p_data['display_url']} &nbsp;&rarr;&nbsp;&nbsp;</b></font>
        """
        btn_table = Table([[Paragraph(f'<a href="{url}">{link_btn_html}</a>', 
                                      ParagraphStyle('BtnStyle', fontName='Helvetica-Bold', fontSize=7.5, leading=9, textColor=C_WHITE))]],
                          colWidths=[290])
        btn_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), C_PRIMARY),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ]))
        content_cells.append(btn_table)

        # Card container table: Left column image (205 pt), Right column text (305 pt)
        card_table = Table([[img_flow, content_cells]], colWidths=[205, 305])
        card_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), C_CARD_BG),
            ('BOX', (0, 0), (-1, -1), 1, C_BORDER),
            ('LINELEFT', (1, 0), (1, -1), 0.5, C_BORDER),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        return card_table

    # =========================================================================
    # SECTION 1: NGOs, NON-PROFITS & COMMUNITY (8 PROJECTS, 2 PER PAGE)
    # =========================================================================
    ngo_projects = [
        # Page 2: RBA Initiative & OPSOK
        [
            {
                'key': 'rbainitiative',
                'title': 'RBA Initiative (Rights-Based Approach)',
                'category': 'Global Health NGO • Antimicrobial Resistance Research',
                'description': 'An international non-governmental health research initiative combating Antimicrobial Resistance (AMR) globally through policy research, health worker education, and cross-border scientific partnerships.',
                'highlights': ['Global AMR Research Hub', 'Partner Collaboration Portal', 'Scientific Publications'],
                'url': 'https://rbainitiative.org',
                'display_url': 'rbainitiative.org'
            },
            {
                'key': 'opsok',
                'title': 'Oncology Pharmacists Society of Kenya (OPSOK)',
                'category': 'Healthcare Society • Medical Non-Profit',
                'description': 'The national professional society uniting clinical oncology pharmacists across Kenya. Facilitates cancer pharmacotherapy standards, continuous medical training, clinical trials research, and annual oncology conferences.',
                'highlights': ['Clinical Cancer Care Standards', 'Member Directory', 'Symposium Registration'],
                'url': 'https://opsok.org',
                'display_url': 'opsok.org'
            }
        ],
        # Page 3: CAK & Teria CBO
        [
            {
                'key': 'cak',
                'title': 'Charities Association of Kenya (CAK)',
                'category': 'NGO Umbrella Body • Civil Society Advocacy',
                'description': 'The premier national membership body serving registered charities, NGOs, and Public Benefit Organizations (PBOs) in Kenya. Centralizes governance resources, legal advocacy, and donor funding compliance.',
                'highlights': ['Institutional Member Portal', '5 Core NGO Services', 'Regulatory Compliance Knowledgebase'],
                'url': 'https://cak.co.ke',
                'display_url': 'cak.co.ke'
            },
            {
                'key': 'teriacbo',
                'title': 'Teria Community-Based Organization',
                'category': 'Community Development • Child Welfare NGO',
                'description': 'A grassroots community organization dedicated to poverty alleviation, vulnerable orphan education, clean borehole water initiatives, and sustainable rural economic empowerment.',
                'highlights': ['Direct Online Donation Integration', 'Community Impact Showcase', 'Mobile M-Pesa Support'],
                'url': 'https://teriacbo.org',
                'display_url': 'teriacbo.org'
            }
        ],
        # Page 4: SEDHURO & GHSD
        [
            {
                'key': 'sedhuro',
                'title': 'SEDHURO (Socio-Economic Dev. & Human Rights)',
                'category': 'Human Rights NGO • Humanitarian Relief',
                'description': 'A regional humanitarian and human rights non-profit providing emergency famine relief, primary community healthcare, legal aid, and civic protection across vulnerable East African communities.',
                'highlights': ['Humanitarian Emergency Response', 'Health Outreach Programs', 'Donor Accountability Reports'],
                'url': 'https://sedhuro.org',
                'display_url': 'sedhuro.org'
            },
            {
                'key': 'globalhealthsd',
                'title': 'Global Health & Sustainable Development (GHSD)',
                'category': 'Public Health NGO • International Development',
                'description': 'A pan-African development organization driving maternal-child health programs, epidemic resilience frameworks, and sustainable community development aligned with UN SDG targets.',
                'highlights': ['UN SDG Impact Framework', 'Cross-Border Health Programs', 'Grant-Ready Research Portals'],
                'url': 'https://globalhealthandsustainabledevelopment.com',
                'display_url': 'globalhealthandsustainabledevelopment.com'
            }
        ],
        # Page 5: Israel Universal Church & Transformation Ark Hub
        [
            {
                'key': 'israeluniversalchurch',
                'title': 'Israel Universal Church',
                'category': 'Faith-Based Organization • Digital Ministry',
                'description': 'A multi-congregation faith-based portal featuring live-stream service broadcasts, community charity updates, sacred calendar management, and online donations.',
                'highlights': ['Live Streaming Broadcasts', 'Event Liturgical Calendar', 'Secure Online Giving & Tithes'],
                'url': 'https://israeluniversalchurch.org',
                'display_url': 'israeluniversalchurch.org'
            },
            {
                'key': 'transformationarkhub',
                'title': 'Transformation Ark Hub',
                'category': 'Social Development • Youth & Leadership Mentorship',
                'description': 'A capacity-building and leadership development institute offering executive coaching, ethical governance seminars, and youth mentorship programs for high-potential professionals.',
                'highlights': ['Leadership Masterclasses', 'Youth Career Mentorship', 'Curriculum Resource Center'],
                'url': 'https://transformationarkhub.co.ke',
                'display_url': 'transformationarkhub.co.ke'
            }
        ]
    ]

    for p_idx, page_pair in enumerate(ngo_projects, start=1):
        story.append(Paragraph("SECTION 1: NGOs, NON-PROFITS &amp; COMMUNITY FOUNDATIONS", section_header_style))
        story.append(Paragraph(
            "Donor-credible, mission-first platforms engineered with M-Pesa/card donation processing, impact reports, and stakeholder portals.", 
            section_desc_style
        ))
        story.append(Spacer(1, 4))

        # First card
        story.append(create_project_card(page_pair[0]))
        story.append(Spacer(1, 14))

        # Second card
        story.append(create_project_card(page_pair[1]))
        story.append(PageBreak())

    # =========================================================================
    # SECTION 2: HEALTHCARE, CLINICAL & HIGHER EDUCATION (3 PROJECTS, 1 PAGE)
    # =========================================================================
    story.append(Paragraph("SECTION 2: HEALTHCARE INSTITUTIONS &amp; HIGHER EDUCATION", section_header_style))
    story.append(Paragraph(
        "Institutional portals designed for medical schools, patient-first therapy practices, and healthcare societies.", 
        section_desc_style
    ))
    story.append(Spacer(1, 4))

    edu_health_projects = [
        {
            'key': 'gluksdbs',
            'title': 'GLUK School of Dentistry &amp; Biomedical Sciences',
            'category': 'Medical Education • University Faculty Portal',
            'description': 'The official academic platform for Great Lakes University’s dental school, detailing accredited BDS degrees, clinical teaching hospital facilities, and online student admissions.',
            'highlights': ['Degree Curriculum Breakdown', 'Student Admissions Portal', 'Hospital Clinic Profiles'],
            'url': 'https://gluksdbs.org',
            'display_url': 'gluksdbs.org'
        },
        {
            'key': 'numeruinstitute',
            'title': 'Numeru Health Care Training Institute',
            'category': 'Vocational Healthcare College • Admissions Portal',
            'description': 'An accredited tertiary health training institute offering certified programs in Health Assistance, Phlebotomy, and Theatre Technology, complete with downloadable fee structures.',
            'highlights': ['Online Course Registration', 'Fee Structure Downloads', 'Graduate Placement Testimonials'],
            'url': 'https://numeruinstitute.co.ke',
            'display_url': 'numeruinstitute.co.ke'
        },
        {
            'key': 'purymaxtherapy',
            'title': 'Purymax Exercise Therapy &amp; Sports Rehab',
            'category': 'Sports Rehabilitation • Physical Therapy Clinic',
            'description': 'A patient-centric healthcare platform educating visitors on specialized physiotherapy and sports science treatments with clinician bios and direct appointment booking.',
            'highlights': ['Therapy Treatment Guides', 'Clinician Credential Bios', 'Direct WhatsApp / Call Booking'],
            'url': 'https://purymaxtherapy.com',
            'display_url': 'purymaxtherapy.com'
        }
    ]

    for proj in edu_health_projects:
        story.append(create_project_card(proj))
        story.append(Spacer(1, 10))

    story.append(PageBreak())

    # =========================================================================
    # SECTION 3: RENEWABLE ENERGY, CORPORATE & ENTERPRISE (5 PROJECTS, 1 PAGE)
    # =========================================================================
    story.append(Paragraph("SECTION 3: RENEWABLE ENERGY, LEGAL &amp; ENTERPRISE PLATFORMS", section_header_style))
    story.append(Paragraph(
        "High-performance digital ecosystems for EPRA-certified clean tech, premier corporate law firms, and marketplaces.", 
        section_desc_style
    ))
    story.append(Spacer(1, 4))

    enterprise_projects = [
        {
            'key': 'greenhuntenergy',
            'title': 'Greenhunt Energy Limited',
            'category': 'Renewable Energy Engineering • EPRA Certified',
            'description': 'A premier EPRA-certified solar contractor delivering commercial &amp; residential solar PV installations, hybrid inverter systems, energy audits, and warranty support.',
            'highlights': ['Solar PV System Catalog', 'Commercial Portfolio Gallery', 'Energy Audit Calculator'],
            'url': 'https://greenhuntenergy.co.ke',
            'display_url': 'greenhuntenergy.co.ke'
        },
        {
            'key': 'lusweti',
            'title': 'Lusweti &amp; Nabutola Advocates',
            'category': 'Corporate Law Firm • Regulatory Compliance',
            'description': 'A top-tier corporate legal consultancy platform highlighting commercial arbitration, constitutional litigation, conveyancing, and regulatory compliance advisory.',
            'highlights': ['Partner Credential Profiles', 'Legal Practice Areas', 'Client Consultations'],
            'url': 'https://luswetinabutola.com',
            'display_url': 'luswetinabutola.com'
        },
        {
            'key': 'kenyaremotejobs',
            'title': 'Kenya Remote Jobs',
            'category': 'National Employment Portal • Tech Talent Marketplace',
            'description': 'High-traffic recruitment and telecommuting platform connecting Kenyan developers, designers, and managers with global employers offering remote roles.',
            'highlights': ['Live Automated Job Board', 'Resume Submissions', 'Employer Posting Dashboard'],
            'url': 'https://kenyaremotejobs.com',
            'display_url': 'kenyaremotejobs.com'
        }
    ]

    for proj in enterprise_projects:
        story.append(create_project_card(proj))
        story.append(Spacer(1, 10))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 8: CLOSING PAGE & WHY ELITE DESIGNS
    # =========================================================================
    story.append(Spacer(1, 10))
    story.append(Paragraph("WHY LEADING NGOS &amp; ENTERPRISES PARTNER WITH ELITE DESIGNS", title_style))
    story.append(Paragraph("Engineering Trust, Speed, and Measurable Outcomes for Over 120 Organizations Across Africa", subtitle_style))

    reasons = [
        ("1. Donor & Stakeholder Credibility", 
         "NGOs and institutions require immediate trust. We design institutional-grade interfaces that communicate legitimacy to donors, government regulators, and international partners."),
        ("2. Extreme Performance & Mobile Optimization", 
         "Over 82% of African web visitors browse via mobile networks. Our websites load in under 1.5 seconds on 3G/4G networks, maximizing engagement and minimizing bounce rates."),
        ("3. Seamless M-Pesa & International Giving", 
         "We natively integrate STK push M-Pesa, card payments, PayPal, and international donor gateways for instant, frictionless fundraising and fee collections."),
        ("4. AI-Optimized Search Visibility (SEO & AEO)", 
         "Our platforms are structured for modern search engines and AI assistants (Google, ChatGPT, Perplexity), ensuring your organization dominates search results for your sector.")
    ]

    reason_cells = []
    for title, desc in reasons:
        rc = [
            Paragraph(f"<font color='#3600df'><b>{title}</b></font>", ParagraphStyle('RT', fontName='Helvetica-Bold', fontSize=10, leading=13)),
            Paragraph(desc, ParagraphStyle('RD', fontName='Helvetica', fontSize=8.2, leading=11.5, textColor=C_BODY))
        ]
        reason_cells.append(rc)

    # 2x2 grid for reasons
    grid_data = [
        [reason_cells[0], reason_cells[1]],
        [reason_cells[2], reason_cells[3]]
    ]
    grid_table = Table(grid_data, colWidths=[CONTENT_WIDTH/2.0 - 5, CONTENT_WIDTH/2.0 - 5])
    grid_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), C_CARD_BG),
        ('BOX', (0, 0), (-1, -1), 1, C_BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, C_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(grid_table)
    story.append(Spacer(1, 16))

    # Additional Client Showcase Row
    add_clients_html = """
    <b>ADDITIONAL CLIENT PLATFORMS IN OUR REPERTOIRE (120+ TOTAL):</b><br/>
    <font color="#475569" size="8">
    &bull; <b>Sherrane Homes</b> (sherranehomes.co.ke) &mdash; Luxury Property Development<br/>
    &bull; <b>Billan Beauty</b> (billanbeauty.co.uk) &mdash; International Skincare E-Commerce<br/>
    &bull; <b>Santorini Queen</b> (santoriniqueen.com) &mdash; Luxury Travel &amp; Yacht Charters<br/>
    &bull; <b>Hometime Investments</b> (hometime.co.ke) &mdash; Coastal Real Estate &amp; AirBnB<br/>
    &bull; <b>Dealforge Procurement</b> (dealforge.org) &mdash; Institutional Supplies &amp; B2B Logistics<br/>
    &bull; <b>Diani Elite Taxi</b> (dianielitetaxi.co.ke) &mdash; Coastal Airport Transfers &amp; Chauffeur Fleet
    </font>
    """
    story.append(Paragraph(add_clients_html, ParagraphStyle('AddClients', fontName='Helvetica', fontSize=8, leading=12, textColor=C_DARK)))
    story.append(Spacer(1, 16))

    # Call-to-Action Box
    cta_html = f"""
    <font color="#ffffff" size="14"><b>Ready to Elevate Your Organization's Digital Presence?</b></font><br/><br/>
    <font color="#e0e7ff" size="9">Let's discuss your upcoming website, portal, or digital campaign. We provide free consultations, wireframes, and fixed-price proposals for NGOs, health institutions, and businesses.</font><br/><br/>
    <font color="#ffffff" size="9.5">
    <b>Website:</b> <a href="https://www.elitedesigns.co.ke"><font color="#fecdd3"><b><u>www.elitedesigns.co.ke</u></b></font></a> &nbsp;&nbsp;&bull;&nbsp;&nbsp;
    <b>Email:</b> <a href="mailto:hello@elitedesigns.co.ke"><font color="#fecdd3"><b><u>hello@elitedesigns.co.ke</u></b></font></a> &nbsp;&nbsp;&bull;&nbsp;&nbsp;
    <b>WhatsApp / Call:</b> <a href="https://wa.me/254722753819"><font color="#fecdd3"><b><u>+254 722 753 819</u></b></font></a>
    </font>
    """
    cta_table = Table([[Paragraph(cta_html, ParagraphStyle('CTA', fontName='Helvetica', alignment=1, leading=14))]], 
                      colWidths=[CONTENT_WIDTH])
    cta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), C_PRIMARY),
        ('BOX', (0, 0), (-1, -1), 2, C_PRIMARY_DARK),
        ('TOPPADDING', (0, 0), (-1, -1), 14),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 14),
        ('LEFTPADDING', (0, 0), (-1, -1), 16),
        ('RIGHTPADDING', (0, 0), (-1, -1), 16),
    ]))
    story.append(cta_table)

    # Build PDF with Custom Numbered Canvas
    doc.build(story, canvasmaker=EliteNumberedCanvas)
    print(f"Generated official Elite Designs Portfolio PDF: {OUTPUT_PDF} ({os.path.getsize(OUTPUT_PDF)} bytes)")

    # Also copy to assets/documents/
    os.makedirs('assets/documents', exist_ok=True)
    import shutil
    shutil.copyfile(OUTPUT_PDF, 'assets/documents/Elite_Designs_Portfolio_2026.pdf')
    print("Copied to assets/documents/Elite_Designs_Portfolio_2026.pdf")


if __name__ == '__main__':
    build_portfolio_pdf()
