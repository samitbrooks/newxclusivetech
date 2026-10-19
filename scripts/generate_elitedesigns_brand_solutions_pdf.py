#!/usr/bin/env python3
"""
Elite Designs Kenya — Corporate Brand Identity & Collateral Solutions Proposal
Refined, elegant, and uncluttered layout tailored specifically for purpose-driven
consultancies (Career Clinic) translating Hope, Trust, and Care into institutional visual prestige.
Features:
- Uncluttered, spacious typography & elegant cards
- Centered, faint Elite Designs logo watermark across all pages
- 35K Gold Growth Suite spotlighted with precision
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily

# 1. Register Comfortaa Fonts
FONT_DIR = 'assets/fonts/comfortaa'
pdfmetrics.registerFont(TTFont('Comfortaa', os.path.join(FONT_DIR, 'Comfortaa-Regular.ttf')))
pdfmetrics.registerFont(TTFont('Comfortaa-Bold', os.path.join(FONT_DIR, 'Comfortaa-Bold.ttf')))
pdfmetrics.registerFont(TTFont('Comfortaa-Light', os.path.join(FONT_DIR, 'Comfortaa-Light.ttf')))
registerFontFamily('Comfortaa', normal='Comfortaa', bold='Comfortaa-Bold', italic='Comfortaa', boldItalic='Comfortaa-Bold')

# 2. Brand Palette derived from Elite Designs logo
C_PRIMARY = colors.HexColor('#3600DF')      # Electric Royal Indigo
C_PRIMARY_DARK = colors.HexColor('#22008F') # Deep Royal Indigo
C_PRIMARY_LIGHT = colors.HexColor('#EEF2FF')# Soft Indigo Tint
C_ACCENT = colors.HexColor('#F22732')       # Vibrant Crimson Red
C_ACCENT_LIGHT = colors.HexColor('#FFF1F2') # Soft Rose Tint
C_GOLD = colors.HexColor('#D97706')         # Warm Amber Gold
C_GOLD_LIGHT = colors.HexColor('#FEF3C7')   # Soft Amber Tint
C_DARK = colors.HexColor('#0F172A')         # Slate 900
C_BODY = colors.HexColor('#334155')         # Slate 700
C_MUTED = colors.HexColor('#64748B')        # Slate 500
C_BORDER = colors.HexColor('#E2E8F0')       # Slate 200
C_CARD_BG = colors.HexColor('#FFFFFF')      # White Card
C_SOFT_BG = colors.HexColor('#F8FAFC')      # Slate 50
C_WHITE = colors.HexColor('#FFFFFF')

LOGO_PATH = 'assets/images/elitedesigns_logo.png'
OUTPUT_PDF = 'assets/documents/Elite_Designs_Brand_Solutions_Proposal.pdf'
os.makedirs(os.path.dirname(OUTPUT_PDF), exist_ok=True)

PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN_LEFT = 40
MARGIN_RIGHT = 40
MARGIN_TOP = 42
MARGIN_BOTTOM = 42
CONTENT_WIDTH = PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT # 515.28 pt


class EliteWatermarkedCanvas(canvas.Canvas):
    """Two-pass canvas for running header/footer and a centered, faint Elite Designs watermark."""
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
            self.draw_decorations_and_watermark(num_pages)
            super().showPage()
        super().save()

    def draw_decorations_and_watermark(self, total_pages):
        page_num = self._pageNumber

        # Top Accent Stripe
        self.saveState()
        self.setFillColor(C_PRIMARY)
        self.rect(0, PAGE_HEIGHT - 4, PAGE_WIDTH, 4, fill=1, stroke=0)
        self.setFillColor(C_ACCENT)
        self.rect(0, PAGE_HEIGHT - 6, 160, 2, fill=1, stroke=0)

        # Faint Centered Logo Watermark (Middle of Page)
        if os.path.exists(LOGO_PATH):
            self.saveState()
            self.setFillAlpha(0.045) # Faded, elegant agency watermark
            wm_w = 320
            wm_h = 80
            wm_x = (PAGE_WIDTH - wm_w) / 2
            wm_y = (PAGE_HEIGHT - wm_h) / 2
            self.drawImage(LOGO_PATH, wm_x, wm_y, width=wm_w, height=wm_h, preserveAspectRatio=True, mask='auto')
            self.restoreState()

        # Running Header on Page 2+
        if page_num > 1:
            header_y = PAGE_HEIGHT - 28
            if os.path.exists(LOGO_PATH):
                self.drawImage(LOGO_PATH, MARGIN_LEFT, header_y - 2, width=80, height=20, preserveAspectRatio=True, mask='auto')

            self.setFont('Comfortaa-Bold', 7.5)
            self.setFillColor(C_PRIMARY)
            self.drawRightString(PAGE_WIDTH - MARGIN_RIGHT, header_y + 4, "ELITE DESIGNS • BRAND IDENTITY & COLLATERAL SOLUTIONS")
            
            self.setStrokeColor(C_BORDER)
            self.setLineWidth(0.5)
            self.line(MARGIN_LEFT, header_y - 6, PAGE_WIDTH - MARGIN_RIGHT, header_y - 6)

        # Running Footer
        footer_y = MARGIN_BOTTOM - 16
        self.setStrokeColor(C_BORDER)
        self.setLineWidth(0.5)
        self.line(MARGIN_LEFT, footer_y + 12, PAGE_WIDTH - MARGIN_RIGHT, footer_y + 12)

        self.setFont('Comfortaa-Bold', 7.5)
        self.setFillColor(C_PRIMARY)
        self.drawString(MARGIN_LEFT, footer_y + 1, "ELITE DESIGNS KENYA")
        self.setFont('Comfortaa', 7.5)
        self.setFillColor(C_MUTED)
        self.drawString(MARGIN_LEFT + 98, footer_y + 1, "• Good Design is Good Business • +254 722 753 819")

        page_str = f"Page {page_num} of {total_pages}"
        self.setFont('Comfortaa-Bold', 7.5)
        self.setFillColor(C_DARK)
        self.drawRightString(PAGE_WIDTH - MARGIN_RIGHT, footer_y + 1, page_str)

        self.restoreState()


def get_styles():
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        'MainTitle',
        fontName='Comfortaa-Bold',
        fontSize=20,
        leading=26,
        textColor=C_DARK,
        alignment=TA_LEFT
    ))

    styles.add(ParagraphStyle(
        'MainSubtitle',
        fontName='Comfortaa',
        fontSize=9.5,
        leading=14.5,
        textColor=C_MUTED,
        alignment=TA_LEFT
    ))

    styles.add(ParagraphStyle(
        'SectionTitle',
        fontName='Comfortaa-Bold',
        fontSize=11,
        leading=15,
        textColor=C_PRIMARY,
        spaceBefore=10,
        spaceAfter=4
    ))

    styles.add(ParagraphStyle(
        'CardHeading',
        fontName='Comfortaa-Bold',
        fontSize=10,
        leading=14,
        textColor=C_DARK
    ))

    styles.add(ParagraphStyle(
        'CustomBody',
        fontName='Comfortaa',
        fontSize=8.2,
        leading=12.8,
        textColor=C_BODY
    ))

    styles.add(ParagraphStyle(
        'PillarText',
        fontName='Comfortaa',
        fontSize=8,
        leading=12.2,
        textColor=C_BODY
    ))

    styles.add(ParagraphStyle(
        'Badge',
        fontName='Comfortaa-Bold',
        fontSize=7.2,
        leading=9.5,
        textColor=C_PRIMARY
    ))

    styles.add(ParagraphStyle(
        'BadgeGold',
        fontName='Comfortaa-Bold',
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor('#92400E')
    ))

    styles.add(ParagraphStyle(
        'PriceDisplay',
        fontName='Comfortaa-Bold',
        fontSize=18,
        leading=22,
        textColor=C_ACCENT,
        alignment=TA_RIGHT
    ))

    styles.add(ParagraphStyle(
        'PriceSub',
        fontName='Comfortaa',
        fontSize=7.5,
        leading=10.5,
        textColor=C_MUTED,
        alignment=TA_RIGHT
    ))

    return styles


def build_proposal():
    doc = SimpleDocTemplate(
        OUTPUT_PDF,
        pagesize=A4,
        leftMargin=MARGIN_LEFT,
        rightMargin=MARGIN_RIGHT,
        topMargin=MARGIN_TOP,
        bottomMargin=MARGIN_BOTTOM
    )

    styles = get_styles()
    story = []

    # =========================================================================
    # PAGE 1: STRATEGIC POSITIONING & CORE BRAND DELIVERABLES
    # =========================================================================
    if os.path.exists(LOGO_PATH):
        story.append(RLImage(LOGO_PATH, width=155, height=39))
    story.append(Spacer(1, 8))

    # Pill badge
    p_badge = Paragraph("<b>EXECUTIVE BRAND IDENTITY &amp; COLLATERAL PROPOSAL</b>", styles['Badge'])
    t_badge = Table([[p_badge]], colWidths=[290])
    t_badge.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), C_PRIMARY_LIGHT),
        ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor('#C7D2FE')),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t_badge)
    story.append(Spacer(1, 6))

    story.append(Paragraph("Strategic Brand Architecture &amp; Corporate Collateral", styles['MainTitle']))
    story.append(Paragraph("Crafted for purpose-driven consultancies to establish unshakeable market trust, empathy, and institutional prestige.", styles['MainSubtitle']))
    story.append(Spacer(1, 10))

    # Strategic Foundation: Beyond a Regular CV Shop
    soul_text = (
        "<b>The Brand Vision: Translating Hope, Trust &amp; Care into Visual Authority</b><br/>"
        "Your business is not a transactional CV writing service on LinkedIn. It is a dedicated clinic for individuals "
        "experiencing frustration and hurt in their professional journeys. Clients seeking career transition, senior leadership "
        "roles, or guidance require more than text on a page — they need to feel immediate <b>reassurance, dignity, and deep trust</b>.<br/><br/>"
        "Elite Designs elevates your existing drafts into a cohesive, warm, and distinctive visual ecosystem: replacing raw templates "
        "with psychological color harmony, refined typography, and executive layouts that inspire confidence from day one."
    )
    p_soul = Paragraph(soul_text, styles['CustomBody'])
    t_soul = Table([[p_soul]], colWidths=[CONTENT_WIDTH])
    t_soul.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
        ('BOX', (0, 0), (-1, -1), 1, C_BORDER),
        ('LINEBEFORE', (0, 0), (0, -1), 3.5, C_PRIMARY),
        ('TOPPADDING', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 9),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ]))
    story.append(t_soul)
    story.append(Spacer(1, 12))

    # SPOTLIGHT HEADER: Gold Growth Brand Suite (KES 35,000)
    p_gold_tag = Paragraph("★ RECOMMENDED COMPREHENSIVE SPRINT", styles['BadgeGold'])
    t_gold_tag = Table([[p_gold_tag]], colWidths=[205])
    t_gold_tag.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), C_GOLD_LIGHT),
        ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor('#FCD34D')),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))

    hdr_left = [
        t_gold_tag,
        Spacer(1, 3),
        Paragraph("Gold Growth Brand Suite", styles['CardHeading']),
        Paragraph("<font color='#64748B'>Full Visual Identity, Company Profile &amp; Services Collateral</font>", styles['CustomBody'])
    ]
    hdr_right = [
        Paragraph("KES 35,000", styles['PriceDisplay']),
        Paragraph("Complete Brand Overhaul &bull; 4–5 Days Turnaround", styles['PriceSub'])
    ]
    t_hdr = Table([[hdr_left, hdr_right]], colWidths=[315, CONTENT_WIDTH - 315])
    t_hdr.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))

    # 4 Clean Deliverable Pillars (Uncluttered 2x2 Layout)
    col_w = (CONTENT_WIDTH - 12) / 2

    # Pillar 1
    p1_content = [
        Paragraph("<b>1. Master Logo Development (3 Concepts)</b>", styles['CardHeading']),
        Spacer(1, 3),
        Paragraph(
            "&bull; <b>Evolution of Your 2 Drafts:</b> We review and refine your existing logo directions to craft a modern, "
            "warm emblem symbolizing guidance, healing, and forward career momentum.<br/>"
            "&bull; <b>Infinite Vector Scalability:</b> Master files delivered in Adobe Illustrator (AI), EPS, SVG, and high-res "
            "PNGs with transparent light/dark variations.",
            styles['PillarText']
        )
    ]
    t_p1 = Table([[p1_content]], colWidths=[col_w])
    t_p1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), C_WHITE),
        ('BOX', (0, 0), (-1, -1), 1, C_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))

    # Pillar 2
    p2_content = [
        Paragraph("<b>2. Color Psychology &amp; Typography System</b>", styles['CardHeading']),
        Spacer(1, 3),
        Paragraph(
            "&bull; <b>Restorative Color Harmony:</b> Formulating a tailored brand palette that embodies <i>Hope, Trust, and Care</i> — "
            "grounding deep trust tones with warm, approachable human accents.<br/>"
            "&bull; <b>Official Values:</b> Calibrated CMYK for print, HEX/RGB for digital web use, and Google font pairings for corporate documents.",
            styles['PillarText']
        )
    ]
    t_p2 = Table([[p2_content]], colWidths=[col_w])
    t_p2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), C_WHITE),
        ('BOX', (0, 0), (-1, -1), 1, C_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))

    # Pillar 3
    p3_content = [
        Paragraph("<b>3. Executive Company Profile (6–8 Pages)</b>", styles['CardHeading']),
        Spacer(1, 3),
        Paragraph(
            "&bull; <b>Visual Re-Architecture:</b> We take your existing draft content and restructure it into an elegant, "
            "tender- and B2B-ready corporate presentation.<br/>"
            "&bull; <b>Editorial Polish:</b> Thoughtful layout pacing, refined service pillars, executive bios, and client journey diagrams.",
            styles['PillarText']
        )
    ]
    t_p3 = Table([[p3_content]], colWidths=[col_w])
    t_p3.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), C_WHITE),
        ('BOX', (0, 0), (-1, -1), 1, C_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))

    # Pillar 4
    p4_content = [
        Paragraph("<b>4. Services Brochure &amp; Rate Card Overhaul</b>", styles['CardHeading']),
        Spacer(1, 3),
        Paragraph(
            "&bull; <b>Coaching &amp; CV Packages:</b> Clear, structured redesign of your pricing tiers and service matrices "
            "to make decision-making effortless for prospective clients.<br/>"
            "&bull; <b>Multi-Format Delivery:</b> Print-ready bi-fold brochure layout + interactive PDF with clickable WhatsApp links.",
            styles['PillarText']
        )
    ]
    t_p4 = Table([[p4_content]], colWidths=[col_w])
    t_p4.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), C_WHITE),
        ('BOX', (0, 0), (-1, -1), 1, C_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))

    t_grid_1 = Table([[t_p1, t_p2]], colWidths=[col_w, col_w])
    t_grid_1.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))

    t_grid_2 = Table([[t_p3, t_p4]], colWidths=[col_w, col_w])
    t_grid_2.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))

    gold_box = [
        t_hdr,
        Spacer(1, 8),
        HRFlowable(width="100%", thickness=0.75, color=colors.HexColor('#FDE68A'), spaceBefore=2, spaceAfter=8),
        t_grid_1,
        Spacer(1, 6),
        t_grid_2
    ]

    t_gold_wrapper = Table([[gold_box]], colWidths=[CONTENT_WIDTH])
    t_gold_wrapper.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#FFFDF9')),
        ('BOX', (0, 0), (-1, -1), 1.5, colors.HexColor('#F59E0B')),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ]))
    story.append(t_gold_wrapper)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: STATIONERY, CALENDAR, WORKFLOW & ENGAGEMENT TERMS
    # =========================================================================
    story.append(Paragraph("Complete Stationery, Client Presence &amp; Roadmap", styles['MainTitle']))
    story.append(Paragraph("Extending your visual identity seamlessly into institutional print, digital touchpoints, and everyday client presence.", styles['MainSubtitle']))
    story.append(Spacer(1, 10))

    # Pillar 5 & 6 (Stationery Suite & Annual Presence)
    p5_content = [
        Paragraph("<b>5. Executive Corporate Stationery Suite</b>", styles['CardHeading']),
        Spacer(1, 3),
        Paragraph(
            "&bull; <b>Business Cards:</b> Double-sided executive cards (up to 3 team members) with 300 DPI CMYK print calibration.<br/>"
            "&bull; <b>Official Letterhead:</b> Delivered in editable MS Word format (.docx) + high-res vector PDF.<br/>"
            "&bull; <b>Envelopes &amp; Folders:</b> Branded DL/C5 envelopes and A4 presentation folder cover for contracts &amp; reports.<br/>"
            "&bull; <b>Digital Touchpoints:</b> Interactive clickable HTML email signature + Smart QR Digital Card for contactless sharing.",
            styles['PillarText']
        )
    ]
    t_p5 = Table([[p5_content]], colWidths=[col_w])
    t_p5.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
        ('BOX', (0, 0), (-1, -1), 1, C_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))

    p6_content = [
        Paragraph("<b>6. 365-Day Presence &amp; Brand Manual</b>", styles['CardHeading']),
        Spacer(1, 3),
        Paragraph(
            "&bull; <b>Custom Corporate Calendar:</b> Bespoke 12-month desk or wall calendar layout featuring inspiring career milestones, "
            "keeping your brand on your clients' desks all year long.<br/>"
            "&bull; <b>Master Brand Guidelines Sheet:</b> Clear reference documentation specifying logo clear space, forbidden distortions, "
            "color pairings, and font hierarchies.<br/>"
            "&bull; <b>Free Printer Handover:</b> Direct technical consultation with your local print shop to ensure zero color shifts.",
            styles['PillarText']
        )
    ]
    t_p6 = Table([[p6_content]], colWidths=[col_w])
    t_p6.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
        ('BOX', (0, 0), (-1, -1), 1, C_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))

    t_grid_second = Table([[t_p5, t_p6]], colWidths=[col_w, col_w])
    t_grid_second.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))
    story.append(t_grid_second)
    story.append(Spacer(1, 10))

    # SPRINT TIMELINE (4 Phases)
    story.append(Paragraph("<b>OUR 4-PHASE DESIGN SPRINT WORKFLOW</b>", styles['SectionTitle']))
    roadmap_data = [
        [
            Paragraph("<b>PHASE 1: BRIEFING &amp; DRAFT INTAKE (Day 1)</b><br/><font color='#64748B'>Comprehensive intake of your 2 logo drafts, copy materials, and instructional notes.</font>", styles['PillarText']),
            Paragraph("<b>PHASE 2: 3D CONCEPT PRESENTATION (Days 2–3)</b><br/><font color='#64748B'>Receive 3 distinct visual directions exploring Hope, Trust &amp; Care rendered on realistic mockups.</font>", styles['PillarText']),
        ],
        [
            Paragraph("<b>PHASE 3: PROFILE &amp; BROCHURE REFINEMENT (Days 4–5)</b><br/><font color='#64748B'>Iterative layout polishing of your company profile pages and service rate cards through up to 3 review rounds.</font>", styles['PillarText']),
            Paragraph("<b>PHASE 4: MASTER VECTOR ASSET HANDOVER (Day 5)</b><br/><font color='#64748B'>Delivery of full source vectors (AI, EPS, SVG), print-ready PDFs (300 DPI CMYK), and full commercial copyright.</font>", styles['PillarText']),
        ]
    ]
    t_road = Table(roadmap_data, colWidths=[CONTENT_WIDTH / 2, CONTENT_WIDTH / 2])
    t_road.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 1, C_BORDER),
        ('GRID', (0, 0), (-1, -1), 0.5, C_BORDER),
        ('BACKGROUND', (0, 0), (-1, -1), C_WHITE),
        ('TOPPADDING', (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
        ('LEFTPADDING', (0, 0), (-1, -1), 9),
        ('RIGHTPADDING', (0, 0), (-1, -1), 9),
    ]))
    story.append(t_road)
    story.append(Spacer(1, 10))

    # TRANSPARENT TERMS & NEXT STEPS
    cta_box_text = (
        "<font size='10.5' color='#3600DF'><b>Transparent Commercial Terms &amp; Activation:</b></font><br/>"
        "&bull; <b>Total Package Investment:</b> KES 35,000 (Covers complete Master Logo, Profile, Rate Card, Stationery &amp; Calendar).<br/>"
        "&bull; <b>50% Project Initiation Deposit (KES 17,500):</b> Reserves your senior design sprint and activates creative production immediately.<br/>"
        "&bull; <b>50% Balance on Live Approval (KES 17,500):</b> Payable only after you review, inspect, and approve your completed brand suite.<br/>"
        "&bull; <b>Alternative Tiers:</b> Silver Starter (KES 22,500 &bull; 3-Day Turnaround) &bull; Platinum Enterprise (KES 55,000 &bull; Includes 16-Page Catalog &amp; Roll-Up Banner).<br/><br/>"
        "<b>Lead Brand Designer:</b> Samuel Kidemi Kisaga &bull; <b>Agency Co-Founder:</b> David Esabwa<br/>"
        "<b>Direct Phone / WhatsApp:</b> +254 722 753 819 &bull; <b>Digital Portfolio:</b> www.xclusivetech.co.ke"
    )
    p_cta_box = Paragraph(cta_box_text, styles['CustomBody'])
    t_cta_box = Table([[p_cta_box]], colWidths=[CONTENT_WIDTH])
    t_cta_box.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#EEF2FF')),
        ('BOX', (0, 0), (-1, -1), 1.25, C_PRIMARY),
        ('LINEBEFORE', (0, 0), (0, -1), 3.5, C_ACCENT),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ]))
    story.append(t_cta_box)

    doc.build(story, canvasmaker=EliteWatermarkedCanvas)
    print(f"Generated Elegant Proposal PDF: {OUTPUT_PDF} ({os.path.getsize(OUTPUT_PDF)} bytes)")


if __name__ == '__main__':
    build_proposal()
