#!/usr/bin/env python3
"""
Elite Designs Kenya — Official Graphic Design Portfolio & Rate Card (2026 Edition)
Engineered exclusively with ReportLab (Zero Chromium).
Branded with official transparent Elite Designs logo and brand colors derived from logo:
- Primary: #3600DF (Electric Royal Indigo / Blue)
- Accent: #F22732 (Vibrant Crimson Red)
- Typography: Comfortaa (Light, Regular, Bold)
Content isolated exclusively for Graphic Design from https://creativekigen.com/graphic-design-services-in-kenya/
"""

import os
import re
from PIL import Image as PILImage
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

# 2. Brand Palette derived from official Elite Designs logo
C_PRIMARY = colors.HexColor('#3600DF')      # Electric Royal Indigo / Blue
C_PRIMARY_DARK = colors.HexColor('#22008F') # Deep Indigo
C_PRIMARY_LIGHT = colors.HexColor('#EEF2FF')# Soft Indigo Tint
C_ACCENT = colors.HexColor('#F22732')       # Vibrant Crimson Red
C_ACCENT_LIGHT = colors.HexColor('#FFF1F2') # Soft Rose Tint
C_DARK = colors.HexColor('#0F172A')         # Slate 900
C_BODY = colors.HexColor('#334155')         # Slate 700
C_MUTED = colors.HexColor('#64748B')        # Slate 500
C_BORDER = colors.HexColor('#E2E8F0')       # Slate 200
C_CARD_BG = colors.HexColor('#FFFFFF')      # Pure White Card
C_SOFT_BG = colors.HexColor('#F8FAFC')      # Slate 50
C_WHITE = colors.HexColor('#FFFFFF')
C_GREEN = colors.HexColor('#059669')

LOGO_PATH = 'assets/images/elitedesigns_logo.png'
OUTPUT_PDF = 'assets/documents/Elite_Designs_Graphic_Design_Portfolio_2026.pdf'
os.makedirs(os.path.dirname(OUTPUT_PDF), exist_ok=True)

PAGE_WIDTH, PAGE_HEIGHT = A4 # 595.28 x 841.89 pt
MARGIN_LEFT = 36
MARGIN_RIGHT = 36
MARGIN_TOP = 40
MARGIN_BOTTOM = 40
CONTENT_WIDTH = PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT # 523.28 pt


class EliteNumberedCanvas(canvas.Canvas):
    """Two-pass canvas for total page count and professional running headers/footers in Comfortaa."""
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

        # Cover Page (Page 1)
        if page_num == 1:
            # Top decorative bars
            self.setFillColor(C_PRIMARY)
            self.rect(0, PAGE_HEIGHT - 8, PAGE_WIDTH, 8, fill=1, stroke=0)
            self.setFillColor(C_ACCENT)
            self.rect(0, PAGE_HEIGHT - 12, PAGE_WIDTH * 0.4, 4, fill=1, stroke=0)

            # Bottom decorative bars
            self.setFillColor(C_PRIMARY)
            self.rect(0, 0, PAGE_WIDTH, 8, fill=1, stroke=0)
            self.setFillColor(C_ACCENT)
            self.rect(PAGE_WIDTH * 0.6, 0, PAGE_WIDTH * 0.4, 8, fill=1, stroke=0)
            return

        # Running Header (Pages 2+)
        self.saveState()
        # Top gradient-like stripe
        self.setFillColor(C_PRIMARY)
        self.rect(0, PAGE_HEIGHT - 4, PAGE_WIDTH, 4, fill=1, stroke=0)
        self.setFillColor(C_ACCENT)
        self.rect(0, PAGE_HEIGHT - 6, 120, 2, fill=1, stroke=0)

        # Header bar
        header_y = PAGE_HEIGHT - 28
        if os.path.exists(LOGO_PATH):
            self.drawImage(LOGO_PATH, MARGIN_LEFT, header_y - 4, width=80, height=20, preserveAspectRatio=True, mask='auto')

        self.setFont('Comfortaa-Bold', 7.5)
        self.setFillColor(C_PRIMARY)
        self.drawRightString(PAGE_WIDTH - MARGIN_RIGHT, header_y + 3, "ELITE DESIGNS KENYA • GRAPHIC DESIGN RATE CARD")
        
        self.setStrokeColor(C_BORDER)
        self.setLineWidth(0.5)
        self.line(MARGIN_LEFT, header_y - 8, PAGE_WIDTH - MARGIN_RIGHT, header_y - 8)

        # Running Footer (Pages 2+)
        footer_y = MARGIN_BOTTOM - 14
        self.setStrokeColor(C_BORDER)
        self.setLineWidth(0.5)
        self.line(MARGIN_LEFT, footer_y + 14, PAGE_WIDTH - MARGIN_RIGHT, footer_y + 14)

        self.setFont('Comfortaa-Bold', 7.5)
        self.setFillColor(C_PRIMARY)
        self.drawString(MARGIN_LEFT, footer_y + 2, "ELITE DESIGNS")
        self.setFont('Comfortaa', 7.5)
        self.setFillColor(C_MUTED)
        self.drawString(MARGIN_LEFT + 72, footer_y + 2, "• Good Design is Good Business • +254 722 753 819")

        page_str = f"Page {page_num} of {total_pages}"
        self.setFont('Comfortaa-Bold', 7.5)
        self.setFillColor(C_DARK)
        self.drawRightString(PAGE_WIDTH - MARGIN_RIGHT, footer_y + 2, page_str)

        self.restoreState()


def get_custom_styles():
    """Build typography hierarchy using Comfortaa."""
    styles = getSampleStyleSheet()

    # Cover Title
    styles.add(ParagraphStyle(
        'CoverTitle',
        fontName='Comfortaa-Bold',
        fontSize=24,
        leading=30,
        textColor=C_DARK,
        alignment=TA_CENTER
    ))

    # Cover Subtitle
    styles.add(ParagraphStyle(
        'CoverSubtitle',
        fontName='Comfortaa',
        fontSize=11,
        leading=16,
        textColor=C_MUTED,
        alignment=TA_CENTER
    ))

    # Category Section Header Title
    styles.add(ParagraphStyle(
        'CategoryTitle',
        fontName='Comfortaa-Bold',
        fontSize=16,
        leading=20,
        textColor=C_DARK
    ))

    # Category Subtitle
    styles.add(ParagraphStyle(
        'CategorySubtitle',
        fontName='Comfortaa',
        fontSize=9.5,
        leading=14,
        textColor=C_MUTED
    ))

    # Category Badge Pill
    styles.add(ParagraphStyle(
        'CategoryBadge',
        fontName='Comfortaa-Bold',
        fontSize=7.5,
        leading=10,
        textColor=C_PRIMARY,
        alignment=TA_LEFT
    ))

    # Service Card Title
    styles.add(ParagraphStyle(
        'CardTitle',
        fontName='Comfortaa-Bold',
        fontSize=10,
        leading=13,
        textColor=C_DARK
    ))

    # Service Card Price
    styles.add(ParagraphStyle(
        'CardPrice',
        fontName='Comfortaa-Bold',
        fontSize=9,
        leading=12,
        textColor=C_ACCENT,
        alignment=TA_LEFT
    ))

    # Card Deliverables Text
    styles.add(ParagraphStyle(
        'CardDeliverables',
        fontName='Comfortaa',
        fontSize=7.5,
        leading=10.5,
        textColor=C_BODY
    ))

    # Body Text
    styles.add(ParagraphStyle(
        'BodyRegular',
        fontName='Comfortaa',
        fontSize=9,
        leading=14,
        textColor=C_BODY
    ))

    styles.add(ParagraphStyle(
        'BodyBold',
        fontName='Comfortaa-Bold',
        fontSize=9,
        leading=14,
        textColor=C_DARK
    ))

    return styles


def create_category_header(badge_text, title_text, subtitle_text, styles):
    """Generate a high-end category banner card with brand colors."""
    badge_html = f"<font color='#3600DF'><b>{badge_text.upper()}</b></font>"
    p_badge = Paragraph(badge_html, styles['CategoryBadge'])
    p_title = Paragraph(title_text, styles['CategoryTitle'])
    p_sub = Paragraph(subtitle_text, styles['CategorySubtitle'])

    data = [
        [p_badge],
        [p_title],
        [Spacer(1, 2)],
        [p_sub]
    ]

    table = Table(data, colWidths=[CONTENT_WIDTH])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
        ('BOX', (0, 0), (-1, -1), 1, C_BORDER),
        ('LINEBEFORE', (0, 0), (0, -1), 4, C_PRIMARY),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 14),
        ('RIGHTPADDING', (0, 0), (-1, -1), 14),
    ]))
    return table


def create_service_card(title, price, image_path, deliverables, styles, card_width=254):
    """Generate an elegant, bordered product card with thumbnail, title, price pill, and scope."""
    # Ensure image exists and has valid aspect ratio
    img_element = Spacer(card_width - 16, 120)
    if os.path.exists(image_path):
        try:
            # We fix image dimensions inside card: 236 pt wide x 110 pt high
            img_element = RLImage(image_path, width=card_width - 20, height=110)
        except Exception:
            pass

    p_title = Paragraph(title, styles['CardTitle'])
    
    # Sleek Price Pill Table
    price_html = f"<font color='#F22732'><b>{price}</b></font>"
    p_price = Paragraph(price_html, styles['CardPrice'])
    
    price_table = Table([[p_price]], colWidths=[card_width - 20])
    price_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#FFF1F2')),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#FECDD3')),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))

    # Deliverables snippet
    deliv_html = f"<font color='#475569'>&bull; {deliverables}</font>"
    p_deliv = Paragraph(deliv_html, styles['CardDeliverables'])

    card_data = [
        [img_element],
        [Spacer(1, 4)],
        [p_title],
        [Spacer(1, 3)],
        [price_table],
        [Spacer(1, 4)],
        [p_deliv]
    ]

    card_table = Table(card_data, colWidths=[card_width])
    card_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), C_CARD_BG),
        ('BOX', (0, 0), (-1, -1), 1, C_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    return card_table


def create_two_column_row(card_left, card_right):
    """Layout 2 cards side by side with consistent gutter."""
    gutter = 15.28
    col_w = (CONTENT_WIDTH - gutter) / 2 # 254 pt
    row_table = Table([[card_left, card_right]], colWidths=[col_w, col_w])
    row_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))
    return row_table


def build_pdf():
    doc = SimpleDocTemplate(
        OUTPUT_PDF,
        pagesize=A4,
        leftMargin=MARGIN_LEFT,
        rightMargin=MARGIN_RIGHT,
        topMargin=MARGIN_TOP,
        bottomMargin=MARGIN_BOTTOM
    )

    styles = get_custom_styles()
    story = []

    # =========================================================================
    # PAGE 1: COVER PAGE
    # =========================================================================
    story.append(Spacer(1, 20))
    if os.path.exists(LOGO_PATH):
        story.append(RLImage(LOGO_PATH, width=240, height=60))
    story.append(Spacer(1, 25))

    # Decorative Badge Pill
    badge_html = "<font color='#3600DF'><b>OFFICIAL 2026 COMMERCIAL RATE CARD &bull; GRAPHIC DESIGN</b></font>"
    p_badge = Paragraph(badge_html, styles['CoverSubtitle'])
    pill_table = Table([[p_badge]], colWidths=[360])
    pill_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), C_PRIMARY_LIGHT),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#C7D2FE')),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ]))
    story.append(pill_table)
    story.append(Spacer(1, 20))

    story.append(Paragraph("Graphic Design Services<br/>&amp; Pricing Portfolio", styles['CoverTitle']))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Visual Identity, Product Packaging, Marketing Collateral &amp; Social Creatives", styles['CoverSubtitle']))
    story.append(Spacer(1, 25))

    # Dual-Color Gradient Accent Line
    line_data = [['', '']]
    line_table = Table(line_data, colWidths=[CONTENT_WIDTH * 0.45, CONTENT_WIDTH * 0.55], rowHeights=[3])
    line_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), C_ACCENT),
        ('BACKGROUND', (1, 0), (1, 0), C_PRIMARY),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))
    story.append(line_table)
    story.append(Spacer(1, 25))

    # Overview Card
    overview_text = (
        "<b>Elite Designs Kenya</b> delivers institutional-grade visual design and branding systems for Kenyan enterprises, "
        "retailers, manufacturers, and corporate brands. As recipients of the prestigious <b>Digitally Fit Awards — Top Web &amp; "
        "Design Firm of the Year</b>, we craft memorable logos, customer-winning product packaging, high-converting social media creatives, "
        "and executive corporate stationery. This document presents our transparent standard pricing, complete service structures, "
        "and client deliverables for 2026."
    )
    p_over = Paragraph(overview_text, styles['BodyRegular'])
    over_table = Table([[p_over]], colWidths=[CONTENT_WIDTH])
    over_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), C_SOFT_BG),
        ('BOX', (0, 0), (-1, -1), 1, C_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 14),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 14),
        ('LEFTPADDING', (0, 0), (-1, -1), 18),
        ('RIGHTPADDING', (0, 0), (-1, -1), 18),
    ]))
    story.append(over_table)
    story.append(Spacer(1, 25))

    # Metadata & Credentials Grid
    meta_data = [
        [
            Paragraph("<b>AGENCY LEADERSHIP</b><br/><font color='#64748B'>Samuel Kidemi &amp; David Esabwa<br/>Co-Founders &bull; Elite Designs</font>", styles['BodyRegular']),
            Paragraph("<b>NATIONAL RECOGNITION</b><br/><font color='#64748B'>Digitally Fit Awards Kenya<br/>Top Web &amp; Design Firm Winner</font>", styles['BodyRegular']),
            Paragraph("<b>DIRECT CONTACT</b><br/><font color='#64748B'>+254 722 753 819<br/>www.xclusivetech.co.ke</font>", styles['BodyRegular']),
        ]
    ]
    meta_table = Table(meta_data, colWidths=[CONTENT_WIDTH / 3, CONTENT_WIDTH / 3, CONTENT_WIDTH / 3])
    meta_table.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 1, C_BORDER),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#FFFFFF')),
        ('LINEBEFORE', (1, 0), (1, -1), 1, C_BORDER),
        ('LINEBEFORE', (2, 0), (2, -1), 1, C_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ]))
    story.append(meta_table)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: TABLE OF CONTENTS & DESIGN PHILOSOPHY
    # =========================================================================
    story.append(Spacer(1, 10))
    story.append(Paragraph("Catalog Overview &amp; Contents", styles['CategoryTitle']))
    story.append(Paragraph("Navigating our 6 specialized graphic design service pillars", styles['CategorySubtitle']))
    story.append(Spacer(1, 15))

    toc_data = [
        [
            Paragraph("<b>01. Brand Identity &amp; Logos</b>", styles['BodyBold']),
            Paragraph("Logos, Business Cards, Stationery Packages, Social Bundles &amp; Email Signatures", styles['BodyRegular']),
            Paragraph("<font color='#3600DF'><b>Page 3</b></font>", styles['BodyBold'])
        ],
        [
            Paragraph("<b>02. Packaging &amp; Labels</b>", styles['BodyBold']),
            Paragraph("Product Labels, Retail Packaging, Book Covers &amp; Custom Shopping Bags", styles['BodyRegular']),
            Paragraph("<font color='#3600DF'><b>Page 4</b></font>", styles['BodyBold'])
        ],
        [
            Paragraph("<b>03. Social Media &amp; Digital</b>", styles['BodyBold']),
            Paragraph("Posts, Facebook &amp; LinkedIn Covers, YouTube Banners, IG Highlights &amp; Monthly Retainers", styles['BodyRegular']),
            Paragraph("<font color='#3600DF'><b>Pages 5–6</b></font>", styles['BodyBold'])
        ],
        [
            Paragraph("<b>04. Marketing Collateral</b>", styles['BodyBold']),
            Paragraph("Company Profiles, Flyers, Posters, Bi-Fold/Tri-Fold Brochures, Restaurant Menus &amp; Banners", styles['BodyRegular']),
            Paragraph("<font color='#3600DF'><b>Pages 7–8</b></font>", styles['BodyBold'])
        ],
        [
            Paragraph("<b>05. Corporate Stationery</b>", styles['BodyBold']),
            Paragraph("Luxury Business Cards, Letterheads, Compliment Slips, Certificates &amp; Corporate Calendars", styles['BodyRegular']),
            Paragraph("<font color='#3600DF'><b>Page 9</b></font>", styles['BodyBold'])
        ],
        [
            Paragraph("<b>06. Merchandise &amp; Loyalty</b>", styles['BodyBold']),
            Paragraph("Customer Loyalty Cards, Thank You Notes, Apparel T-Shirts, Branded Mugs &amp; Packaging", styles['BodyRegular']),
            Paragraph("<font color='#3600DF'><b>Page 10</b></font>", styles['BodyBold'])
        ],
    ]
    toc_table = Table(toc_data, colWidths=[140, 310, 73.28])
    toc_table.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 1, C_BORDER),
        ('BACKGROUND', (0, 0), (-1, -1), C_WHITE),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [C_WHITE, C_SOFT_BG]),
        ('GRID', (0, 0), (-1, -1), 0.5, C_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 9),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(toc_table)
    story.append(Spacer(1, 20))

    # Elite Design Philosophy Box
    philosophy_html = (
        "<b>The Elite Designs Standard: Good Design is Good Business</b><br/><br/>"
        "In modern commerce, design is never merely decorative — it is your most powerful sales asset. "
        "A poorly constructed logo or pixelated marketing flyer instantly lowers your perceived market value, allowing competitors "
        "to undercut your prices. Every asset produced by Elite Designs adheres to four strict professional guarantees:<br/><br/>"
        "&bull; <b>100% Vector Scalability:</b> Master files delivered in industry-standard Adobe Illustrator (AI), EPS, and SVG formats.<br/>"
        "&bull; <b>Print-Ready Calibration:</b> CMYK color profiles, 300+ DPI resolution, bleed and crop marks for flawless commercial printing.<br/>"
        "&bull; <b>Digital Optimization:</b> Web-optimized sRGB, lightweight PNG, WebP, and social-ready aspect ratios.<br/>"
        "&bull; <b>Full Ownership Transfer:</b> Complete copyright and commercial usage rights assigned to your company upon project completion."
    )
    p_phil = Paragraph(philosophy_html, styles['BodyRegular'])
    phil_table = Table([[p_phil]], colWidths=[CONTENT_WIDTH])
    phil_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
        ('BOX', (0, 0), (-1, -1), 1, C_BORDER),
        ('LINEBEFORE', (0, 0), (0, -1), 4, C_ACCENT),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('LEFTPADDING', (0, 0), (-1, -1), 16),
        ('RIGHTPADDING', (0, 0), (-1, -1), 16),
    ]))
    story.append(phil_table)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: CATEGORY 01 — BRAND IDENTITY & LOGO DESIGN
    # =========================================================================
    story.append(create_category_header(
        badge_text="Category 01 • Brand Identity & Logos",
        title_text="Start with a Logo",
        subtitle_text="Choose a logo offer that grabs attention and makes a strong first impression.",
        styles=styles
    ))
    story.append(Spacer(1, 14))

    # Row 1: Logo Design & Logo + Business Card
    c1 = create_service_card(
        title="Logo Design",
        price="Starting at: Ksh. 6,500",
        image_path="assets/images/creativekigen/logo_design.png",
        deliverables="3 unique design concepts, full vector source files (AI, EPS, SVG), high-res PNG & brand color palette.",
        styles=styles
    )
    c2 = create_service_card(
        title="Logo Design & Business Card",
        price="Starting at: Ksh. 8,000",
        image_path="assets/images/creativekigen/logo_design___business_card.png",
        deliverables="Bespoke logo identity package paired with double-sided print-ready business cards (300 DPI CMYK).",
        styles=styles
    )
    story.append(create_two_column_row(c1, c2))
    story.append(Spacer(1, 12))

    # Row 2: Logo + Stationery & Logo + Social Media
    c3 = create_service_card(
        title="Logo Design & Stationery",
        price="Starting at: Ksh. 9,500",
        image_path="assets/images/creativekigen/logo_design___stationery.jpg",
        deliverables="Complete primary identity: logo, official letterhead (Word/PDF), corporate business cards & branded envelopes.",
        styles=styles
    )
    c4 = create_service_card(
        title="Logo Design & Social Media",
        price="Starting at: Ksh. 13,500",
        image_path="assets/images/creativekigen/logo_design___social_media.png",
        deliverables="Master logo package plus complete social branding suite: profile avatars, banners for FB, IG, Twitter & LinkedIn.",
        styles=styles
    )
    story.append(create_two_column_row(c3, c4))
    story.append(Spacer(1, 12))

    # Row 3: Email Signature (Single card spanning left column with description on right)
    c5 = create_service_card(
        title="Email Signature Design",
        price="Starting at: Ksh. 2,500",
        image_path="assets/images/creativekigen/email_signature.png",
        deliverables="Interactive, clickable corporate email signature with logo, social icons, mobile number & disclaimer.",
        styles=styles
    )
    # Right column explanatory note
    note_html = (
        "<b>Brand Identity Deliverables Standard</b><br/><br/>"
        "Every logo crafted by Elite Designs includes:<br/>"
        "&bull; <b>Master Vector Files:</b> Infinite scalability without pixelation (AI, EPS, SVG).<br/>"
        "&bull; <b>Transparent PNGs:</b> Dark, light, and monochrome variations for any background.<br/>"
        "&bull; <b>Brand Palette Sheet:</b> Exact HEX, RGB, and CMYK color codes.<br/>"
        "&bull; <b>Typography Pairing:</b> Recommended Google/Web fonts for your corporate documents."
    )
    p_note = Paragraph(note_html, styles['BodyRegular'])
    note_table = Table([[p_note]], colWidths=[254])
    note_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
        ('BOX', (0, 0), (-1, -1), 1, C_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ]))
    story.append(create_two_column_row(c5, note_table))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: CATEGORY 02 — PACKAGING & PRODUCT BRANDING
    # =========================================================================
    story.append(create_category_header(
        badge_text="Category 02 • Packaging & Labels",
        title_text="Launch Your Product",
        subtitle_text="Choose a product offer that will convince customers to buy.",
        styles=styles
    ))
    story.append(Spacer(1, 14))

    # Row 1: Label Design & Packaging Design
    p1 = create_service_card(
        title="Product Label Design",
        price="Starting at: Ksh. 3,000",
        image_path="assets/images/creativekigen/label_design.jpg",
        deliverables="Custom die-cut bottle, jar, can or pouch labels with barcode zones, nutrition tables & compliance text.",
        styles=styles
    )
    p2 = create_service_card(
        title="Packaging Box & Container Design",
        price="Starting at: Ksh. 8,000",
        image_path="assets/images/creativekigen/packaging_design.jpg",
        deliverables="3D packaging architecture, dielines, folding box templates & 3D realistic retail shelf mockups.",
        styles=styles
    )
    story.append(create_two_column_row(p1, p2))
    story.append(Spacer(1, 14))

    # Row 2: Book Cover Design & Shopping Bag Design
    p3 = create_service_card(
        title="Book Cover Design",
        price="Starting at: Ksh. 4,500",
        image_path="assets/images/creativekigen/book_cover_design.jpg",
        deliverables="Full jacket design (front, spine, back), ISBN barcode integration, Amazon KDP & print-ready PDF formats.",
        styles=styles
    )
    p4 = create_service_card(
        title="Shopping Bag Design",
        price="Starting at: Ksh. 1,000",
        image_path="assets/images/creativekigen/shopping_bag_design.jpg",
        deliverables="Branded retail kraft paper bags, luxury boutique tote layouts, handle placements & spot UV specifications.",
        styles=styles
    )
    story.append(create_two_column_row(p3, p4))
    story.append(Spacer(1, 14))

    # Technical Quality Guarantee for Packaging
    pkg_note_html = (
        "<b>Manufacturing &amp; Print-Ready Guarantee:</b> "
        "All packaging designs are engineered to exact printer dielines with calibrated 3mm bleed tolerances, "
        "CMYK spot colors, and vector finish layers (embossing, foil stamping, spot UV) ready for any commercial printer in Kenya."
    )
    p_pnote = Paragraph(pkg_note_html, styles['BodyRegular'])
    pnote_table = Table([[p_pnote]], colWidths=[CONTENT_WIDTH])
    pnote_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
        ('BOX', (0, 0), (-1, -1), 1, C_BORDER),
        ('LINEBEFORE', (0, 0), (0, -1), 3, C_PRIMARY),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 14),
        ('RIGHTPADDING', (0, 0), (-1, -1), 14),
    ]))
    story.append(pnote_table)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 5: CATEGORY 03 — SOCIAL MEDIA & DIGITAL (PART 1)
    # =========================================================================
    story.append(create_category_header(
        badge_text="Category 03 • Social Media & Digital (Part 1)",
        title_text="Shine on Social Media",
        subtitle_text="Improve your social media presence with stunning graphics.",
        styles=styles
    ))
    story.append(Spacer(1, 14))

    # Row 1: Social Media Design & Facebook Cover
    s1 = create_service_card(
        title="Social Media Post Design",
        price="Starting at: Ksh. 1,500",
        image_path="assets/images/creativekigen/social_media_design.jpg",
        deliverables="High-converting single post graphic for Instagram/FB/LinkedIn with custom copy hook and branding.",
        styles=styles
    )
    s2 = create_service_card(
        title="Facebook Cover Design",
        price="Starting at: Ksh. 1,500",
        image_path="assets/images/creativekigen/facebook_cover_design.jpg",
        deliverables="Mobile & desktop responsive Facebook cover banner highlighting your core offer and call-to-action.",
        styles=styles
    )
    story.append(create_two_column_row(s1, s2))
    story.append(Spacer(1, 12))

    # Row 2: Instagram Highlight & YouTube Banner
    s3 = create_service_card(
        title="Instagram Highlight Cover Design",
        price="Starting at: Ksh. 1,500",
        image_path="assets/images/creativekigen/instagram_highlight_cover_design.jpg",
        deliverables="Cohesive set of custom vector icons and covers tailored to your brand aesthetic.",
        styles=styles
    )
    s4 = create_service_card(
        title="YouTube Banner Design",
        price="Starting at: Ksh. 1,500",
        image_path="assets/images/creativekigen/youtube_banner_design.png",
        deliverables="Ultra HD channel art with safe-area optimization across TV, laptop, tablet, and mobile screens.",
        styles=styles
    )
    story.append(create_two_column_row(s3, s4))
    story.append(Spacer(1, 12))

    # Row 3: Social Media Calendar & Strategy Note
    s5 = create_service_card(
        title="Social Media Content Calendar",
        price="Starting at: Ksh. 1,500",
        image_path="assets/images/creativekigen/social_media_calendar.png",
        deliverables="Monthly content roadmap with daily post themes, caption prompts, and hashtag recommendations.",
        styles=styles
    )
    sm_note_html = (
        "<b>High-Engagement Digital Creative Standards:</b><br/><br/>"
        "Our social media designs are crafted specifically to stop the thumb scroll in Kenyan feeds:<br/>"
        "&bull; Optimized for Retina mobile screens (1080×1080 px &amp; 1080×1350 px portrait).<br/>"
        "&bull; High-contrast brand typography that reads clearly on small smartphone screens.<br/>"
        "&bull; Clear, unmissable Call to Action (WhatsApp, website link, or direct call)."
    )
    p_smnote = Paragraph(sm_note_html, styles['BodyRegular'])
    smnote_table = Table([[p_smnote]], colWidths=[254])
    smnote_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
        ('BOX', (0, 0), (-1, -1), 1, C_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ]))
    story.append(create_two_column_row(s5, smnote_table))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 6: CATEGORY 03 — SOCIAL MEDIA & DIGITAL (PART 2)
    # =========================================================================
    story.append(create_category_header(
        badge_text="Category 03 • Social Media & Digital (Part 2)",
        title_text="Scale Your Digital Reach",
        subtitle_text="Strategic marketing campaigns, executive profiles, and monthly creative retainers.",
        styles=styles
    ))
    story.append(Spacer(1, 14))

    # Row 1: Social Media Marketing & Social Media Management
    s6 = create_service_card(
        title="Social Media Marketing Campaign",
        price="Starting at: Ksh. 15,000",
        image_path="assets/images/creativekigen/social_media_marketing.png",
        deliverables="Targeted creative campaign bundle: ad banners, carousel ad sets, story creatives & conversion copywriting.",
        styles=styles
    )
    s7 = create_service_card(
        title="Monthly Social Media Management",
        price="Starting at: Ksh. 22,000",
        image_path="assets/images/creativekigen/social_media_management.jpg",
        deliverables="Full monthly creative retainer: 12–16 custom branded graphics, scheduled publishing, reels/stories & analytics.",
        styles=styles
    )
    story.append(create_two_column_row(s6, s7))
    story.append(Spacer(1, 14))

    # Row 2: LinkedIn Banner & Digital Business Card
    s8 = create_service_card(
        title="LinkedIn Banner Design",
        price="Starting at: Ksh. 1,500",
        image_path="assets/images/creativekigen/linkedin_banner_design.png",
        deliverables="Executive personal branding banner showcasing your value proposition, speaking topics, or corporate bio.",
        styles=styles
    )
    s9 = create_service_card(
        title="Digital Business Card Design",
        price="Starting at: Ksh. 8,500",
        image_path="assets/images/creativekigen/digital_business_card.png",
        deliverables="Interactive contactless digital card with QR code, 1-tap WhatsApp, vCard contact download & portfolio links.",
        styles=styles
    )
    story.append(create_two_column_row(s8, s9))
    story.append(Spacer(1, 14))

    retainer_html = (
        "<b>Monthly Creative Retainer Value:</b> "
        "For growing brands needing continuous social content, our monthly management retainers eliminate the cost of hiring "
        "a full-time in-house graphic designer (saving up to KES 45,000/month) while providing faster, agency-grade creative output."
    )
    p_ret = Paragraph(retainer_html, styles['BodyRegular'])
    ret_table = Table([[p_ret]], colWidths=[CONTENT_WIDTH])
    ret_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
        ('BOX', (0, 0), (-1, -1), 1, C_BORDER),
        ('LINEBEFORE', (0, 0), (0, -1), 3, C_ACCENT),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 14),
        ('RIGHTPADDING', (0, 0), (-1, -1), 14),
    ]))
    story.append(ret_table)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 7: CATEGORY 04 — MARKETING COLLATERAL & PRINT (PART 1)
    # =========================================================================
    story.append(create_category_header(
        badge_text="Category 04 • Marketing Collateral (Part 1)",
        title_text="Generate Awareness Offline",
        subtitle_text="Marketing materials to convey your message to customers.",
        styles=styles
    ))
    story.append(Spacer(1, 14))

    # Row 1: Company Profile & Flyer/Poster
    m1 = create_service_card(
        title="Company Profile Design",
        price="Starting at: Ksh. 6,500",
        image_path="assets/images/creativekigen/company_profile_design.jpg",
        deliverables="High-impact 8–16 page corporate capability profile, executive bios, past project showcases & tender-ready layout.",
        styles=styles
    )
    m2 = create_service_card(
        title="Flyer / Poster Design",
        price="Starting at: Ksh. 8,000",
        image_path="assets/images/creativekigen/flyer_poster_design.jpg",
        deliverables="Eye-catching promotional flyers (A5/A4/A3) formatted for high-volume street distribution and digital sharing.",
        styles=styles
    )
    story.append(create_two_column_row(m1, m2))
    story.append(Spacer(1, 14))

    # Row 2: Brochure Design & Restaurant Menu
    m3 = create_service_card(
        title="Brochure Design (Bi-Fold / Tri-Fold)",
        price="Starting at: Ksh. 4,000",
        image_path="assets/images/creativekigen/brochure_design.jpg",
        deliverables="Double-sided folded sales brochure with organized product tiers, benefit matrices, and corporate styling.",
        styles=styles
    )
    m4 = create_service_card(
        title="Restaurant / Cafe Menu Design",
        price="Starting at: Ksh. 4,000",
        image_path="assets/images/creativekigen/menu_design.jpg",
        deliverables="Appetizing multi-page food & beverage menu layout with price formatting, category grouping & photo retouching.",
        styles=styles
    )
    story.append(create_two_column_row(m3, m4))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 8: CATEGORY 04 — MARKETING COLLATERAL & PRINT (PART 2)
    # =========================================================================
    story.append(create_category_header(
        badge_text="Category 04 • Marketing Collateral (Part 2)",
        title_text="Print & Signage Collateral",
        subtitle_text="Digital menus, product catalogs, and large-format promotional banners.",
        styles=styles
    ))
    story.append(Spacer(1, 14))

    # Row 1: Digital Menu & Catalog Design
    m5 = create_service_card(
        title="Digital Menu Design",
        price="Starting at: Ksh. 6,000",
        image_path="assets/images/creativekigen/digital_menu_design.jpg",
        deliverables="High-definition landscape layout for TV display boards and tablet menus in restaurants and cafes.",
        styles=styles
    )
    m6 = create_service_card(
        title="Product Catalog Design",
        price="Starting at: Ksh. 4,500",
        image_path="assets/images/creativekigen/catalog_design.jpg",
        deliverables="Multi-page comprehensive inventory catalog with SKU tables, specification sheets, and clickable PDF links.",
        styles=styles
    )
    story.append(create_two_column_row(m5, m6))
    story.append(Spacer(1, 14))

    # Row 2: Large Format Banner Design & Print Specs Note
    m7 = create_service_card(
        title="Banner Design (Roll-Up / Outdoor)",
        price="Starting at: Ksh. 4,500",
        image_path="assets/images/creativekigen/banner_design.jpg",
        deliverables="Large-format roll-up teardrop or outdoor PVC billboard banners with crystal clear typography at 150–300 DPI.",
        styles=styles
    )
    banner_note_html = (
        "<b>Large-Format Print Specifications:</b><br/><br/>"
        "Banners, roll-up stands, and event backdrops require precise resolution management to prevent pixelation at scale:<br/>"
        "&bull; Color-calibrated CMYK profiles preventing muddy print shifts.<br/>"
        "&bull; 100% vector typography ensuring needle-sharp readability from across a conference hall.<br/>"
        "&bull; Standard eyelet, hem, and stand cartridge margin allowances built directly into output files."
    )
    p_bnote = Paragraph(banner_note_html, styles['BodyRegular'])
    bnote_table = Table([[p_bnote]], colWidths=[254])
    bnote_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
        ('BOX', (0, 0), (-1, -1), 1, C_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ]))
    story.append(create_two_column_row(m7, bnote_table))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 9: CATEGORY 05 — CORPORATE STATIONERY & SUITE
    # =========================================================================
    story.append(create_category_header(
        badge_text="Category 05 • Corporate Stationery",
        title_text="Make a Lasting Impression",
        subtitle_text="Stationery design packages to improve your business image.",
        styles=styles
    ))
    story.append(Spacer(1, 14))

    # Row 1: Business Card & Stationery Package
    st1 = create_service_card(
        title="Business Card Design",
        price="Starting at: Ksh. 1,500",
        image_path="assets/images/creativekigen/business_card_design.jpg",
        deliverables="Double-sided executive business cards, QR code links, foil/matte finish specifications & print-ready PDF.",
        styles=styles
    )
    st2 = create_service_card(
        title="Stationery Package Design",
        price="Starting at: Ksh. 3,000",
        image_path="assets/images/creativekigen/stationery_package_design.jpg",
        deliverables="Comprehensive corporate suite: business cards, letterhead, official envelopes & folder covers.",
        styles=styles
    )
    story.append(create_two_column_row(st1, st2))
    story.append(Spacer(1, 12))

    # Row 2: Letterhead & Compliment Slip
    st3 = create_service_card(
        title="Official Letterhead Design",
        price="Starting at: Ksh. 1,500",
        image_path="assets/images/creativekigen/letterhead_design.jpg",
        deliverables="Delivered in editable Microsoft Word (.docx) format and high-res vector PDF with registration details.",
        styles=styles
    )
    st4 = create_service_card(
        title="Compliment Slip Design",
        price="Starting at: Ksh. 1,000",
        image_path="assets/images/creativekigen/compliment_slip__design.jpg",
        deliverables="Personalized branded DL compliment slips for deliveries, contracts, gifts, and client correspondence.",
        styles=styles
    )
    story.append(create_two_column_row(st3, st4))
    story.append(Spacer(1, 12))

    # Row 3: Certificate & Calendar Design
    st5 = create_service_card(
        title="Certificate Design",
        price="Starting at: Ksh. 1,500",
        image_path="assets/images/creativekigen/certificate_design.jpg",
        deliverables="Prestige certificates of completion, appreciation, or membership with watermark borders and seal zones.",
        styles=styles
    )
    st6 = create_service_card(
        title="Corporate Calendar Design",
        price="Starting at: Ksh. 2,500",
        image_path="assets/images/creativekigen/calender_design.jpg",
        deliverables="Custom 12-month desk or wall calendar layout featuring your products, company milestones & Kenyan holidays.",
        styles=styles
    )
    story.append(create_two_column_row(st5, st6))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 10: CATEGORY 06 — MERCHANDISE, LOYALTY & CLIENT RETENTION
    # =========================================================================
    story.append(create_category_header(
        badge_text="Category 06 • Merchandise & Loyalty",
        title_text="Build Customer Loyalty",
        subtitle_text="Choose an item that will improve customer loyalty and drive referrals.",
        styles=styles
    ))
    story.append(Spacer(1, 14))

    # Row 1: Thank You Card & Loyalty Card
    l1 = create_service_card(
        title="Thank You Card Design",
        price="Starting at: Ksh. 1,500",
        image_path="assets/images/creativekigen/thank_you_card_design.jpg",
        deliverables="Warm, personalized e-commerce packaging insert cards with discount codes and social review prompts.",
        styles=styles
    )
    l2 = create_service_card(
        title="Loyalty Card Design",
        price="Starting at: Ksh. 1,500",
        image_path="assets/images/creativekigen/loyalty_card_design.jpg",
        deliverables="Stamp-card or digital barcode loyalty card designed to incentivize repeat client purchases.",
        styles=styles
    )
    story.append(create_two_column_row(l1, l2))
    story.append(Spacer(1, 12))

    # Row 2: Compliment Slip (Loyalty) & T-Shirt Design
    l3 = create_service_card(
        title="VIP Compliment Slip Design",
        price="Starting at: Ksh. 1,500",
        image_path="assets/images/creativekigen/compliment_slip_design.jpg",
        deliverables="High-end presentation note for luxury product unboxing and corporate executive gifting.",
        styles=styles
    )
    l4 = create_service_card(
        title="Corporate T-Shirt / Apparel Design",
        price="Starting at: Ksh. 2,500",
        image_path="assets/images/creativekigen/tshirt_design.jpg",
        deliverables="Screen-print and embroidery-ready vector artwork (front, back, sleeve) with color separation layers.",
        styles=styles
    )
    story.append(create_two_column_row(l3, l4))
    story.append(Spacer(1, 12))

    # Row 3: Branded Mug & Takeaway Bag
    l5 = create_service_card(
        title="Branded Mug Design",
        price="Starting at: Ksh. 1,000",
        image_path="assets/images/creativekigen/mug_design.jpg",
        deliverables="360° sublimation wrap graphic calibrated for ceramic coffee mugs, travel tumblers, and water bottles.",
        styles=styles
    )
    l6 = create_service_card(
        title="Takeaway & Food Bag Design",
        price="Starting at: Ksh. 1,500",
        image_path="assets/images/creativekigen/takeaway_bag_design.jpg",
        deliverables="Greaseproof paper bag and box packaging layout for restaurants, bakeries, and fast-food takeaway.",
        styles=styles
    )
    story.append(create_two_column_row(l5, l6))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 11: ENGAGEMENT TERMS & NEXT STEPS
    # =========================================================================
    story.append(Spacer(1, 10))
    story.append(create_category_header(
        badge_text="Working with Elite Designs",
        title_text="Commercial Terms &amp; Project Workflow",
        subtitle_text="Transparent milestones, rapid turnaround times, and hassle-free asset delivery.",
        styles=styles
    ))
    story.append(Spacer(1, 16))

    # 4-Step Process Grid
    steps_data = [
        [
            Paragraph("<b>STEP 1: BRIEFING</b><br/><font color='#64748B'>Submit your brand vision, reference samples, content, and specific deliverables on WhatsApp or email.</font>", styles['BodyRegular']),
            Paragraph("<b>STEP 2: CONCEPTS</b><br/><font color='#64748B'>Within 48–72 hours, receive initial design drafts formatted as real-world 3D mockups for review.</font>", styles['BodyRegular']),
        ],
        [
            Paragraph("<b>STEP 3: REVISIONS</b><br/><font color='#64748B'>We refine your chosen concept with up to 3 rounds of iterative revisions until you are 100% delighted.</font>", styles['BodyRegular']),
            Paragraph("<b>STEP 4: HANDOVER</b><br/><font color='#64748B'>Full transfer of master source vectors (AI, EPS, SVG, PDF) and full commercial rights upon final approval.</font>", styles['BodyRegular']),
        ]
    ]
    steps_table = Table(steps_data, colWidths=[CONTENT_WIDTH / 2, CONTENT_WIDTH / 2])
    steps_table.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 1, C_BORDER),
        ('GRID', (0, 0), (-1, -1), 0.5, C_BORDER),
        ('BACKGROUND', (0, 0), (-1, -1), C_WHITE),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('LEFTPADDING', (0, 0), (-1, -1), 14),
        ('RIGHTPADDING', (0, 0), (-1, -1), 14),
    ]))
    story.append(steps_table)
    story.append(Spacer(1, 20))

    # Payment Terms & Reversal Guarantee
    terms_html = (
        "<b>Milestone Payment Terms:</b><br/>"
        "&bull; <b>50% Project Initiation Deposit:</b> Locks in your design sprint and allocates our senior graphic artists.<br/>"
        "&bull; <b>50% Balance on Live Approval:</b> Payable ONLY after you have reviewed and approved your final designs.<br/>"
        "&bull; <b>Turnaround Speed:</b> Individual collateral items delivered in <b>24–48 hours</b>; comprehensive brand packages in <b>3–5 business days</b>.<br/>"
        "&bull; <b>Accepted Payment Methods:</b> M-Pesa Buy Goods / Till, M-Pesa Paybill, Bank Transfer (EFT/RTGS), and International Card/PayPal."
    )
    p_terms = Paragraph(terms_html, styles['BodyRegular'])
    terms_table = Table([[p_terms]], colWidths=[CONTENT_WIDTH])
    terms_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
        ('BOX', (0, 0), (-1, -1), 1, C_BORDER),
        ('LINEBEFORE', (0, 0), (0, -1), 4, C_PRIMARY),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('LEFTPADDING', (0, 0), (-1, -1), 16),
        ('RIGHTPADDING', (0, 0), (-1, -1), 16),
    ]))
    story.append(terms_table)
    story.append(Spacer(1, 25))

    # Call to Action Card
    cta_html = (
        "<font size='14' color='#3600DF'><b>Ready to elevate your company's visual identity?</b></font><br/><br/>"
        "<font color='#334155'>Connect directly with our co-founder and lead designer for instant consultation, custom package quotes, and rapid project initiation.</font><br/><br/>"
        "<b>Direct WhatsApp &amp; Calls:</b> +254 722 753 819<br/>"
        "<b>Digital Portfolio &amp; Web Services:</b> https://www.xclusivetech.co.ke/<br/>"
        "<b>Studio Location:</b> Nairobi, Kenya &bull; Servicing Clients Countrywide &amp; Across the Global Diaspora"
    )
    p_cta = Paragraph(cta_html, styles['BodyRegular'])
    cta_table = Table([[p_cta]], colWidths=[CONTENT_WIDTH])
    cta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#EEF2FF')),
        ('BOX', (0, 0), (-1, -1), 1.5, C_PRIMARY),
        ('TOPPADDING', (0, 0), (-1, -1), 16),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 16),
        ('LEFTPADDING', (0, 0), (-1, -1), 18),
        ('RIGHTPADDING', (0, 0), (-1, -1), 18),
    ]))
    story.append(cta_table)

    # Build the document
    doc.build(story, canvasmaker=EliteNumberedCanvas)
    print(f"Generated successfully: {OUTPUT_PDF} ({os.path.getsize(OUTPUT_PDF)} bytes)")


if __name__ == '__main__':
    build_pdf()
