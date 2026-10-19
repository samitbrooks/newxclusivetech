#!/usr/bin/env python3
"""
Elite Designs Kenya — Startup Branding Executive Presentation Brief (PDF)
A high-impact executive brief summarizing the 3 Startup Branding Packages:
- Silver Starter (KES 22,500)
- Gold Growth (KES 35,000 - Flagship with Company Profile, Brochure, Calendar)
- Platinum Enterprise (KES 55,000 - Full Scale with 16pg Profile, Banner, Merch)
Built with ReportLab, Comfortaa font, and official Elite Designs branding.
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

# 2. Brand Palette
C_PRIMARY = colors.HexColor('#3600DF')      # Electric Royal Indigo
C_PRIMARY_DARK = colors.HexColor('#22008F') # Deep Indigo
C_PRIMARY_LIGHT = colors.HexColor('#EEF2FF')# Soft Indigo Tint
C_ACCENT = colors.HexColor('#F22732')       # Vibrant Crimson Red
C_ACCENT_LIGHT = colors.HexColor('#FFF1F2') # Soft Rose Tint
C_DARK = colors.HexColor('#0F172A')         # Slate 900
C_BODY = colors.HexColor('#334155')         # Slate 700
C_MUTED = colors.HexColor('#64748B')        # Slate 500
C_BORDER = colors.HexColor('#CBD5E1')       # Slate 300
C_WHITE = colors.HexColor('#FFFFFF')
C_SOFT_BG = colors.HexColor('#F8FAFC')
C_GOLD = colors.HexColor('#D97706')

LOGO_PATH = 'assets/images/elitedesigns_logo.png'
OUTPUT_PDF = 'assets/documents/Elite_Designs_Branding_Presentation_Brief.pdf'
DOWNLOADS_PDF = '/Users/app/Downloads/Elite_Designs_Branding_Presentation_Brief.pdf'
os.makedirs(os.path.dirname(OUTPUT_PDF), exist_ok=True)

PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN_LEFT = 36
MARGIN_RIGHT = 36
MARGIN_TOP = 34
MARGIN_BOTTOM = 34
CONTENT_WIDTH = PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT # 523.28 pt


class EliteNumberedCanvas(canvas.Canvas):
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

        self.saveState()
        self.setFillColor(C_PRIMARY)
        self.rect(0, PAGE_HEIGHT - 5, PAGE_WIDTH, 5, fill=1, stroke=0)
        self.setFillColor(C_ACCENT)
        self.rect(0, PAGE_HEIGHT - 7, 140, 2, fill=1, stroke=0)

        if page_num > 1:
            header_y = PAGE_HEIGHT - 25
            if os.path.exists(LOGO_PATH):
                self.drawImage(LOGO_PATH, MARGIN_LEFT, header_y - 3, width=75, height=18, preserveAspectRatio=True, mask='auto')

            self.setFont('Comfortaa-Bold', 7.5)
            self.setFillColor(C_PRIMARY)
            self.drawRightString(PAGE_WIDTH - MARGIN_RIGHT, header_y + 3, "ELITE DESIGNS KENYA • EXECUTIVE PRESENTATION BRIEF")
            
            self.setStrokeColor(C_BORDER)
            self.setLineWidth(0.5)
            self.line(MARGIN_LEFT, header_y - 5, PAGE_WIDTH - MARGIN_RIGHT, header_y - 5)

        footer_y = MARGIN_BOTTOM - 13
        self.setStrokeColor(C_BORDER)
        self.setLineWidth(0.5)
        self.line(MARGIN_LEFT, footer_y + 11, PAGE_WIDTH - MARGIN_RIGHT, footer_y + 11)

        self.setFont('Comfortaa-Bold', 7.5)
        self.setFillColor(C_PRIMARY)
        self.drawString(MARGIN_LEFT, footer_y + 1, "ELITE DESIGNS KENYA")
        self.setFont('Comfortaa', 7.5)
        self.setFillColor(C_MUTED)
        self.drawString(MARGIN_LEFT + 95, footer_y + 1, "• Good Design is Good Business • +254 722 753 819")

        page_str = f"Page {page_num} of {total_pages}"
        self.setFont('Comfortaa-Bold', 7.5)
        self.setFillColor(C_DARK)
        self.drawRightString(PAGE_WIDTH - MARGIN_RIGHT, footer_y + 1, page_str)

        self.restoreState()


def get_styles():
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        'DocTitle',
        fontName='Comfortaa-Bold',
        fontSize=19,
        leading=24,
        textColor=C_DARK,
        alignment=TA_LEFT
    ))

    styles.add(ParagraphStyle(
        'DocSubtitle',
        fontName='Comfortaa',
        fontSize=9,
        leading=13,
        textColor=C_MUTED,
        alignment=TA_LEFT
    ))

    styles.add(ParagraphStyle(
        'SectionHeader',
        fontName='Comfortaa-Bold',
        fontSize=11,
        leading=15,
        textColor=C_DARK
    ))

    styles.add(ParagraphStyle(
        'MatrixHeader',
        fontName='Comfortaa-Bold',
        fontSize=8,
        leading=10.5,
        textColor=C_DARK,
        alignment=TA_CENTER
    ))

    styles.add(ParagraphStyle(
        'MatrixItem',
        fontName='Comfortaa',
        fontSize=7.5,
        leading=10,
        textColor=C_BODY
    ))

    styles.add(ParagraphStyle(
        'MatrixCheck',
        fontName='Comfortaa-Bold',
        fontSize=8.5,
        leading=11,
        textColor=C_PRIMARY,
        alignment=TA_CENTER
    ))

    styles.add(ParagraphStyle(
        'MatrixCheckGold',
        fontName='Comfortaa-Bold',
        fontSize=8.5,
        leading=11,
        textColor=C_ACCENT,
        alignment=TA_CENTER
    ))

    styles.add(ParagraphStyle(
        'BodyRegular',
        fontName='Comfortaa',
        fontSize=8,
        leading=12,
        textColor=C_BODY
    ))

    styles.add(ParagraphStyle(
        'TierMeta',
        fontName='Comfortaa',
        fontSize=7.5,
        leading=10,
        textColor=C_MUTED
    ))

    return styles


def build_brief():
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
    # PAGE 1: EXECUTIVE BRIEF & COMPARISON MATRIX
    # =========================================================================
    if os.path.exists(LOGO_PATH):
        story.append(RLImage(LOGO_PATH, width=160, height=40))
    story.append(Spacer(1, 6))

    badge_html = "<font color='#3600DF'><b>EXECUTIVE CLIENT BRIEF &bull; STARTUP BRAND IDENTITY SUITES</b></font>"
    p_badge = Paragraph(badge_html, styles['TierMeta'])
    pill_table = Table([[p_badge]], colWidths=[380])
    pill_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), C_PRIMARY_LIGHT),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#C7D2FE')),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(pill_table)
    story.append(Spacer(1, 5))

    story.append(Paragraph("Startup Brand Identity &amp; Corporate Collateral Brief", styles['DocTitle']))
    story.append(Paragraph("Executive summary of deliverables, investment tiers, and strategic commercial impact for Kenyan enterprises.", styles['DocSubtitle']))
    story.append(Spacer(1, 8))

    # Strategic Value Proposition Callout
    why_text = (
        "<b>Why Unified Branding Matters for Your Bottom Line:</b> In high-stakes B2B negotiations, procurement tenders, "
        "and client pitches, prospective customers evaluate your stability and competence within seconds. Inconsistent or "
        "piecemeal branding erodes trust and invites aggressive price haggling. A cohesive identity suite — master logo, "
        "investor-ready company profile, executive stationery, brochures, and corporate calendars — establishes immediate "
        "institutional prestige, enabling your firm to command premium fees."
    )
    p_why = Paragraph(why_text, styles['BodyRegular'])
    t_why = Table([[p_why]], colWidths=[CONTENT_WIDTH])
    t_why.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
        ('BOX', (0, 0), (-1, -1), 1, C_BORDER),
        ('LINEBEFORE', (0, 0), (0, -1), 3.5, C_PRIMARY),
        ('TOPPADDING', (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(t_why)
    story.append(Spacer(1, 10))

    # Comprehensive Side-by-Side Deliverables Comparison Table
    story.append(Paragraph("<b>PACKAGE DELIVERABLES &amp; SCOPE COMPARISON MATRIX</b>", styles['SectionHeader']))
    story.append(Spacer(1, 4))

    matrix_data = [
        [
            Paragraph("<b>Deliverable Scope</b>", styles['MatrixHeader']),
            Paragraph("<b>Silver Starter</b><br/><font color='#3600DF'><b>KES 22,500</b></font>", styles['MatrixHeader']),
            Paragraph("<b>Gold Growth</b><br/><font color='#F22732'><b>KES 35,000</b></font>", styles['MatrixHeader']),
            Paragraph("<b>Platinum Scale</b><br/><font color='#3600DF'><b>KES 55,000</b></font>", styles['MatrixHeader']),
        ],
        [
            Paragraph("<b>Master Logo Suite</b> (3 Concepts, Vector AI, EPS, SVG, PNG)", styles['MatrixItem']),
            Paragraph("&bull; Included", styles['MatrixCheck']),
            Paragraph("&bull; Included", styles['MatrixCheckGold']),
            Paragraph("&bull; Included", styles['MatrixCheck']),
        ],
        [
            Paragraph("<b>Brand Color Palette &amp; Corporate Typography Guide</b>", styles['MatrixItem']),
            Paragraph("&bull; Included", styles['MatrixCheck']),
            Paragraph("&bull; Included", styles['MatrixCheckGold']),
            Paragraph("&bull; Included", styles['MatrixCheck']),
        ],
        [
            Paragraph("<b>Executive Business Cards</b> (Print-Ready 300 DPI CMYK)", styles['MatrixItem']),
            Paragraph("1 Staff Version", styles['MatrixCheck']),
            Paragraph("Up to 3 Staff", styles['MatrixCheckGold']),
            Paragraph("Up to 6 Staff", styles['MatrixCheck']),
        ],
        [
            Paragraph("<b>Official Letterhead</b> (Editable MS Word .docx + Vector PDF)", styles['MatrixItem']),
            Paragraph("&bull; Included", styles['MatrixCheck']),
            Paragraph("&bull; Included", styles['MatrixCheckGold']),
            Paragraph("&bull; Included", styles['MatrixCheck']),
        ],
        [
            Paragraph("<b>Services Brochure / Promotional Flyer</b>", styles['MatrixItem']),
            Paragraph("Bi-Fold / Flyer", styles['MatrixCheck']),
            Paragraph("Bi-Fold / Flyer", styles['MatrixCheckGold']),
            Paragraph("Multi-Page Catalog", styles['MatrixCheck']),
        ],
        [
            Paragraph("<b>Corporate Company Profile</b> (Tender &amp; Investor Ready)", styles['MatrixItem']),
            Paragraph("<font color='#94A3B8'>&mdash;</font>", styles['MatrixCheck']),
            Paragraph("<b>6–8 Pages</b>", styles['MatrixCheckGold']),
            Paragraph("<b>12–16 Pages</b>", styles['MatrixCheck']),
        ],
        [
            Paragraph("<b>Complete Stationery Suite</b> (Envelopes DL/C5, Compliment Slips, A4 Folder)", styles['MatrixItem']),
            Paragraph("<font color='#94A3B8'>&mdash;</font>", styles['MatrixCheck']),
            Paragraph("&bull; Included", styles['MatrixCheckGold']),
            Paragraph("&bull; Included", styles['MatrixCheck']),
        ],
        [
            Paragraph("<b>Custom Corporate Calendar</b> (Desk &amp; Wall Variations)", styles['MatrixItem']),
            Paragraph("<font color='#94A3B8'>&mdash;</font>", styles['MatrixCheck']),
            Paragraph("&bull; Included", styles['MatrixCheckGold']),
            Paragraph("&bull; Desk + Wall", styles['MatrixCheck']),
        ],
        [
            Paragraph("<b>Digital Brand Assets</b> (Clickable Email Signature, QR Digital Card)", styles['MatrixItem']),
            Paragraph("Email Signature", styles['MatrixCheck']),
            Paragraph("&bull; Full Suite", styles['MatrixCheckGold']),
            Paragraph("&bull; Full Suite", styles['MatrixCheck']),
        ],
        [
            Paragraph("<b>Large-Format Signage</b> (Roll-Up Pull-Up Banner 85×200cm CMYK)", styles['MatrixItem']),
            Paragraph("<font color='#94A3B8'>&mdash;</font>", styles['MatrixCheck']),
            Paragraph("<font color='#94A3B8'>&mdash;</font>", styles['MatrixCheckGold']),
            Paragraph("&bull; Included", styles['MatrixCheck']),
        ],
        [
            Paragraph("<b>Branded Merchandise &amp; Packaging</b> (Staff T-Shirt, Mug, Kraft Bag)", styles['MatrixItem']),
            Paragraph("<font color='#94A3B8'>&mdash;</font>", styles['MatrixCheck']),
            Paragraph("<font color='#94A3B8'>&mdash;</font>", styles['MatrixCheckGold']),
            Paragraph("&bull; T-Shirt, Mug, Bag", styles['MatrixCheck']),
        ],
        [
            Paragraph("<b>Master Brand Book Manual</b>", styles['MatrixItem']),
            Paragraph("Basic Palette", styles['MatrixCheck']),
            Paragraph("1-Page Sheet", styles['MatrixCheckGold']),
            Paragraph("16-Page Manual", styles['MatrixCheck']),
        ],
        [
            Paragraph("<b>Turnaround Schedule &amp; Revision Rounds</b>", styles['MatrixItem']),
            Paragraph("3 Days (2 Rounds)", styles['MatrixCheck']),
            Paragraph("4–5 Days (3 Rounds)", styles['MatrixCheckGold']),
            Paragraph("7 Days (Unlimited)", styles['MatrixCheck']),
        ],
    ]

    t_matrix = Table(matrix_data, colWidths=[205, 106, 106, 106])
    t_matrix.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 1, C_BORDER),
        ('GRID', (0, 0), (-1, -1), 0.5, C_BORDER),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F1F5F9')),
        ('BACKGROUND', (2, 0), (2, -1), colors.HexColor('#FFFDF5')), # Highlight Gold column
        ('LINEBEFORE', (2, 0), (2, -1), 1.5, C_ACCENT),
        ('LINEAFTER', (2, 0), (2, -1), 1.5, C_ACCENT),
        ('TOPPADDING', (0, 0), (-1, -1), 4.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t_matrix)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: TIMELINE, TERMS, QUALITY STANDARDS & ENGAGEMENT STEPS
    # =========================================================================
    story.append(Spacer(1, 4))
    story.append(Paragraph("Commercial Engagement &amp; Production Framework", styles['DocTitle']))
    story.append(Paragraph("How Elite Designs delivers your branding sprint seamlessly in 3 to 7 business days.", styles['DocSubtitle']))
    story.append(Spacer(1, 10))

    # 4-Phase Delivery Roadmap
    story.append(Paragraph("<b>1. PRODUCTION TIMELINE &amp; SPRINT PHASES</b>", styles['SectionHeader']))
    roadmap_data = [
        [
            Paragraph("<b>PHASE 01: DISCOVERY &amp; BRIEFING (Day 1)</b><br/><font color='#64748B'>Initial kickoff to define your market positioning, target demographics, aesthetic references, and deliverable priorities.</font>", styles['BodyRegular']),
            Paragraph("<b>PHASE 02: CONCEPT PRESENTATION (Days 2–3)</b><br/><font color='#64748B'>Receive 3 unique creative directions rendered as real-world 3D mockups (stationery, company profile cover, business cards).</font>", styles['BodyRegular']),
        ],
        [
            Paragraph("<b>PHASE 03: ITERATIVE REFINEMENT (Days 4–5)</b><br/><font color='#64748B'>We refine your chosen concept through structured review rounds to perfect color balance, typography, and layout details.</font>", styles['BodyRegular']),
            Paragraph("<b>PHASE 04: VECTOR &amp; ASSET HANDOVER (Days 5–7)</b><br/><font color='#64748B'>Final delivery of master vector source files (AI, EPS, SVG), print-ready PDFs (300 DPI CMYK), and full commercial rights transfer.</font>", styles['BodyRegular']),
        ]
    ]
    t_road = Table(roadmap_data, colWidths=[CONTENT_WIDTH / 2, CONTENT_WIDTH / 2])
    t_road.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 1, C_BORDER),
        ('GRID', (0, 0), (-1, -1), 0.5, C_BORDER),
        ('BACKGROUND', (0, 0), (-1, -1), C_WHITE),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(t_road)
    story.append(Spacer(1, 10))

    # Commercial Terms & Risk Reversal
    story.append(Paragraph("<b>2. TRANSPARENT COMMERCIAL TERMS &amp; RISK REVERSAL</b>", styles['SectionHeader']))
    terms_text = (
        "&bull; <b>50% Project Initiation Deposit:</b> Reserves your dedicated senior design sprint and activates creative production.<br/>"
        "&bull; <b>50% Balance on Live Approval:</b> Payable ONLY after you have reviewed, inspected, and approved your completed brand suite.<br/>"
        "&bull; <b>100% Full Ownership Transfer:</b> You own all master files, vector source codes, and intellectual property with zero royalties.<br/>"
        "&bull; <b>Commercial Printing Support:</b> Free technical printer handover to ensure your local print shop outputs calibrated CMYK colors without error."
    )
    p_terms = Paragraph(terms_text, styles['BodyRegular'])
    t_terms = Table([[p_terms]], colWidths=[CONTENT_WIDTH])
    t_terms.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
        ('BOX', (0, 0), (-1, -1), 1, C_BORDER),
        ('LINEBEFORE', (0, 0), (0, -1), 3.5, C_PRIMARY),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ]))
    story.append(t_terms)
    story.append(Spacer(1, 10))

    # Call to Action Card
    cta_text = (
        "<font size='12' color='#3600DF'><b>Ready to initiate your startup's branding sprint?</b></font><br/><br/>"
        "<font color='#334155'>Lock in your package choice today to secure your sprint slot for this week.</font><br/><br/>"
        "<b>Lead Designer:</b> Samuel Kidemi &bull; <b>Direct WhatsApp / Phone:</b> +254 722 753 819<br/>"
        "<b>National Distinction:</b> Digitally Fit Awards Winner &bull; Top Web &amp; Design Firm of the Year<br/>"
        "<b>Digital Portfolio:</b> https://www.xclusivetech.co.ke/ &bull; Nairobi, Kenya"
    )
    p_cta = Paragraph(cta_text, styles['BodyRegular'])
    t_cta = Table([[p_cta]], colWidths=[CONTENT_WIDTH])
    t_cta.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#EEF2FF')),
        ('BOX', (0, 0), (-1, -1), 1.5, C_PRIMARY),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('LEFTPADDING', (0, 0), (-1, -1), 14),
        ('RIGHTPADDING', (0, 0), (-1, -1), 14),
    ]))
    story.append(t_cta)

    doc.build(story, canvasmaker=EliteNumberedCanvas)
    print(f"Generated Presentation Brief PDF: {OUTPUT_PDF} ({os.path.getsize(OUTPUT_PDF)} bytes)")


if __name__ == '__main__':
    build_brief()
