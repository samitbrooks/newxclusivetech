#!/usr/bin/env python3
"""
Elite Designs Kenya — Corporate Brand Identity & Collateral Solutions Proposal
Tailored for growing service enterprises and startups (like Career Clinic)
to transition from raw working drafts into a cohesive, warm, and distinctive market leader.
Engineered with ReportLab, Comfortaa font, and official Elite Designs branding.
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
MARGIN_LEFT = 36
MARGIN_RIGHT = 36
MARGIN_TOP = 38
MARGIN_BOTTOM = 38
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

        # Cover top stripe
        self.saveState()
        self.setFillColor(C_PRIMARY)
        self.rect(0, PAGE_HEIGHT - 5, PAGE_WIDTH, 5, fill=1, stroke=0)
        self.setFillColor(C_ACCENT)
        self.rect(0, PAGE_HEIGHT - 7, 150, 2, fill=1, stroke=0)

        # Running header on Page 2+
        if page_num > 1:
            header_y = PAGE_HEIGHT - 26
            if os.path.exists(LOGO_PATH):
                self.drawImage(LOGO_PATH, MARGIN_LEFT, header_y - 3, width=75, height=18, preserveAspectRatio=True, mask='auto')

            self.setFont('Comfortaa-Bold', 7.5)
            self.setFillColor(C_PRIMARY)
            self.drawRightString(PAGE_WIDTH - MARGIN_RIGHT, header_y + 3, "ELITE DESIGNS • CORPORATE BRANDING SOLUTIONS")
            
            self.setStrokeColor(C_BORDER)
            self.setLineWidth(0.5)
            self.line(MARGIN_LEFT, header_y - 6, PAGE_WIDTH - MARGIN_RIGHT, header_y - 6)

        # Running Footer
        footer_y = MARGIN_BOTTOM - 14
        self.setStrokeColor(C_BORDER)
        self.setLineWidth(0.5)
        self.line(MARGIN_LEFT, footer_y + 12, PAGE_WIDTH - MARGIN_RIGHT, footer_y + 12)

        self.setFont('Comfortaa-Bold', 7.5)
        self.setFillColor(C_PRIMARY)
        self.drawString(MARGIN_LEFT, footer_y + 1, "ELITE DESIGNS KENYA")
        self.setFont('Comfortaa', 7.5)
        self.setFillColor(C_MUTED)
        self.drawString(MARGIN_LEFT + 98, footer_y + 1, "• Tailored Brand Identity & Collateral Proposal")

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
        fontSize=20,
        leading=25,
        textColor=C_DARK,
        alignment=TA_LEFT
    ))

    styles.add(ParagraphStyle(
        'DocSubtitle',
        fontName='Comfortaa',
        fontSize=9.5,
        leading=14,
        textColor=C_MUTED,
        alignment=TA_LEFT
    ))

    styles.add(ParagraphStyle(
        'SectionHeader',
        fontName='Comfortaa-Bold',
        fontSize=11,
        leading=15,
        textColor=C_DARK,
        spaceBefore=6,
        spaceAfter=3
    ))

    styles.add(ParagraphStyle(
        'BodyRegular',
        fontName='Comfortaa',
        fontSize=8,
        leading=12,
        textColor=C_BODY
    ))

    styles.add(ParagraphStyle(
        'BodyBold',
        fontName='Comfortaa-Bold',
        fontSize=8,
        leading=12,
        textColor=C_DARK
    ))

    styles.add(ParagraphStyle(
        'TierTitle',
        fontName='Comfortaa-Bold',
        fontSize=12,
        leading=15,
        textColor=C_DARK
    ))

    styles.add(ParagraphStyle(
        'PriceTag',
        fontName='Comfortaa-Bold',
        fontSize=15,
        leading=18,
        textColor=C_PRIMARY
    ))

    styles.add(ParagraphStyle(
        'PriceTagGold',
        fontName='Comfortaa-Bold',
        fontSize=16,
        leading=19,
        textColor=C_ACCENT
    ))

    styles.add(ParagraphStyle(
        'BadgeText',
        fontName='Comfortaa-Bold',
        fontSize=7,
        leading=9,
        textColor=C_PRIMARY
    ))

    styles.add(ParagraphStyle(
        'BadgeTextGold',
        fontName='Comfortaa-Bold',
        fontSize=7,
        leading=9,
        textColor=colors.HexColor('#92400E')
    ))

    styles.add(ParagraphStyle(
        'ListBulletItem',
        fontName='Comfortaa',
        fontSize=7.8,
        leading=11.5,
        textColor=C_BODY
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
    # PAGE 1: STRATEGIC OVERVIEW & FLAGSHIP SOLUTION SPOTLIGHT
    # =========================================================================
    if os.path.exists(LOGO_PATH):
        story.append(RLImage(LOGO_PATH, width=155, height=39))
    story.append(Spacer(1, 6))

    # Pill badge
    badge_p = Paragraph("<font color='#3600DF'><b>OFFICIAL BRAND IDENTITY &amp; COLLATERAL SOLUTIONS</b></font>", styles['BadgeText'])
    t_badge = Table([[badge_p]], colWidths=[310])
    t_badge.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), C_PRIMARY_LIGHT),
        ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor('#C7D2FE')),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t_badge)
    story.append(Spacer(1, 4))

    story.append(Paragraph("Strategic Brand Design &amp; Corporate Collateral Packages", styles['DocTitle']))
    story.append(Paragraph("Transforming working draft materials into an authoritative, warm, and cohesive market leader.", styles['DocSubtitle']))
    story.append(Spacer(1, 8))

    # Executive Overview Callout
    intro_txt = (
        "<b>Executive Solution Scope:</b> When introducing high-touch professional services — such as career consulting, "
        "executive coaching, or talent advisories — clients make subconscious assessments regarding your competence within "
        "seconds of reviewing your profile, rate card, or business card. Working drafts convey early ambition, but a calibrated, "
        "warm, and distinctive brand system secures high-ticket corporate contracts. Elite Designs bridges this transformation: "
        "re-architecting your draft copy, establishing psychological color harmony, and engineering print &amp; digital collateral "
        "that commands market trust from day one."
    )
    p_intro = Paragraph(intro_txt, styles['BodyRegular'])
    t_intro = Table([[p_intro]], colWidths=[CONTENT_WIDTH])
    t_intro.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
        ('BOX', (0, 0), (-1, -1), 1, C_BORDER),
        ('LINEBEFORE', (0, 0), (0, -1), 3.5, C_PRIMARY),
        ('TOPPADDING', (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(t_intro)
    story.append(Spacer(1, 10))

    # SPOTLIGHT CARD: THE GOLD GROWTH BRAND SUITE (Tailored exactly to Step 3)
    spotlight_badge = Paragraph("<b>★ RECOMMENDED SOLUTION &bull; FULL CORPORATE SPRINT</b>", styles['BadgeTextGold'])
    tb_badge = Table([[spotlight_badge]], colWidths=[240])
    tb_badge.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), C_GOLD_LIGHT),
        ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor('#FCD34D')),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))

    gold_header_left = [
        tb_badge,
        Spacer(1, 3),
        Paragraph("Gold Growth Brand Suite", styles['TierTitle']),
        Paragraph("Complete Brand Identity, Company Profile Overhaul &amp; Collateral Suite", styles['BodyRegular'])
    ]
    gold_header_right = [
        Paragraph("KES 35,000", styles['PriceTagGold']),
        Paragraph("<font color='#64748B'>Turnaround: 4–5 Days &bull; 3 Rounds</font>", styles['BodyRegular'])
    ]
    t_gold_hdr = Table([[gold_header_left, gold_header_right]], colWidths=[330, CONTENT_WIDTH - 330])
    t_gold_hdr.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))

    # Gold Deliverables 2-column list
    col1_items = [
        Paragraph("<b>1. Master Logo Architecture &amp; Identity:</b><br/>"
                  "&bull; 3 bespoke creative concepts (icon + wordmark + emblem)<br/>"
                  "&bull; Master vector exports (AI, EPS, SVG) scalable infinitely<br/>"
                  "&bull; Transparent dark, light, and monochrome PNG variations", styles['ListBulletItem']),
        Spacer(1, 4),
        Paragraph("<b>2. Brand Design System &amp; Color Psychology:</b><br/>"
                  "&bull; Curated palette balancing executive trust &amp; human warmth<br/>"
                  "&bull; Exact CMYK (print), HEX/RGB (digital) &amp; Pantone equivalents<br/>"
                  "&bull; Primary &amp; secondary typography pairings for all documents", styles['ListBulletItem']),
        Spacer(1, 4),
        Paragraph("<b>3. Executive Corporate Profile (6–8 Pages):</b><br/>"
                  "&bull; Complete aesthetic re-architecture of your working draft text<br/>"
                  "&bull; Strategic visual hierarchy, pull-quotes &amp; case highlights<br/>"
                  "&bull; Formatted for corporate procurement, tenders &amp; B2B pitches", styles['ListBulletItem']),
    ]

    col2_items = [
        Paragraph("<b>4. Services Brochure &amp; Rate Card Overhaul:</b><br/>"
                  "&bull; Redesign of your CV &amp; coaching package pricing matrices<br/>"
                  "&bull; Bi-fold / tri-fold commercial brochure with high-converting layout<br/>"
                  "&bull; Interactive digital PDF with clickable WhatsApp &amp; web links", styles['ListBulletItem']),
        Spacer(1, 4),
        Paragraph("<b>5. Complete Corporate Stationery Suite:</b><br/>"
                  "&bull; Executive double-sided business cards (up to 3 staff members)<br/>"
                  "&bull; Official editable MS Word letterhead (.docx) + Vector PDF<br/>"
                  "&bull; DL/C5 Corporate Envelopes + A4 Presentation Folder Cover", styles['ListBulletItem']),
        Spacer(1, 4),
        Paragraph("<b>6. Physical &amp; Digital Value Multipliers:</b><br/>"
                  "&bull; Custom Corporate Desk/Wall Calendar (365-day client presence)<br/>"
                  "&bull; Interactive clickable HTML email signature + Smart QR Digital Card<br/>"
                  "&bull; 1-Page Master Brand Specifications Sheet", styles['ListBulletItem']),
    ]

    t_gold_cols = Table([[col1_items, col2_items]], colWidths=[CONTENT_WIDTH / 2 - 8, CONTENT_WIDTH / 2 - 8])
    t_gold_cols.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))

    gold_box_content = [
        t_gold_hdr,
        Spacer(1, 6),
        HRFlowable(width="100%", thickness=0.75, color=colors.HexColor('#FDE68A'), spaceBefore=2, spaceAfter=6),
        t_gold_cols
    ]

    t_gold_card = Table([[gold_box_content]], colWidths=[CONTENT_WIDTH])
    t_gold_card.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#FFFDF7')),
        ('BOX', (0, 0), (-1, -1), 1.5, colors.HexColor('#F59E0B')),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ]))
    story.append(t_gold_card)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: COMPARATIVE TIERS, WORKFLOW & ENGAGEMENT STEPS
    # =========================================================================
    story.append(Paragraph("Alternative Package Options &amp; Scope Comparison", styles['DocTitle']))
    story.append(Paragraph("Scale your brand presence according to your current organizational phase.", styles['DocSubtitle']))
    story.append(Spacer(1, 8))

    # 2 Cards Side-by-Side: Silver Starter vs. Platinum Enterprise
    silver_content = [
        Paragraph("<font color='#3600DF'><b>ESSENTIAL ENTRY TIER</b></font>", styles['BadgeText']),
        Spacer(1, 2),
        Paragraph("Silver Starter Suite", styles['TierTitle']),
        Paragraph("<b>KES 22,500</b> &bull; Turnaround: 3 Days", styles['BodyBold']),
        Spacer(1, 4),
        Paragraph("Ideal for focused market entry with foundational collateral:", styles['BodyRegular']),
        Spacer(1, 3),
        Paragraph("&bull; 3 Master Logo Concepts (Full Vector AI, EPS, SVG, PNG)", styles['ListBulletItem']),
        Paragraph("&bull; Brand Color Palette &amp; Corporate Typography Guide", styles['ListBulletItem']),
        Paragraph("&bull; Executive Business Cards (1 Staff Version, Print-Ready CMYK)", styles['ListBulletItem']),
        Paragraph("&bull; Official Letterhead (Editable Word .docx + Vector PDF)", styles['ListBulletItem']),
        Paragraph("&bull; Bi-Fold Services Brochure / Rate Flyer", styles['ListBulletItem']),
        Paragraph("&bull; Interactive Clickable Corporate Email Signature", styles['ListBulletItem']),
        Paragraph("&bull; 2 Structured Revision Rounds", styles['ListBulletItem']),
    ]

    platinum_content = [
        Paragraph("<font color='#DC2626'><b>MAXIMUM INSTITUTIONAL IMPACT</b></font>", styles['BadgeText']),
        Spacer(1, 2),
        Paragraph("Platinum Enterprise Suite", styles['TierTitle']),
        Paragraph("<b>KES 55,000</b> &bull; Turnaround: 7 Days", styles['BodyBold']),
        Spacer(1, 4),
        Paragraph("Everything in Gold, scaled for major industry dominance:", styles['BodyRegular']),
        Spacer(1, 3),
        Paragraph("&bull; Master Company Profile expanded to <b>12–16 Pages</b>", styles['ListBulletItem']),
        Paragraph("&bull; Comprehensive Multi-Page Product &amp; Service Catalog", styles['ListBulletItem']),
        Paragraph("&bull; Large-Format <b>85×200cm Roll-Up Pull-Up Banner</b>", styles['ListBulletItem']),
        Paragraph("&bull; Branded Staff Kit (Polo Shirt, Ceramic Mug, Kraft Bags)", styles['ListBulletItem']),
        Paragraph("&bull; 16-Page Master Corporate Brand Identity Manual", styles['ListBulletItem']),
        Paragraph("&bull; Both Desk &amp; Wall Calendar Variations", styles['ListBulletItem']),
        Paragraph("&bull; Executive Cards for up to 6 Staff &bull; Unlimited Revisions", styles['ListBulletItem']),
    ]

    card_width = (CONTENT_WIDTH - 12) / 2
    t_silver = Table([[silver_content]], colWidths=[card_width])
    t_silver.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
        ('BOX', (0, 0), (-1, -1), 1, C_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))

    t_platinum = Table([[platinum_content]], colWidths=[card_width])
    t_platinum.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#FFF1F2')),
        ('BOX', (0, 0), (-1, -1), 1.25, colors.HexColor('#FECDD3')),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))

    t_compare_row = Table([[t_silver, t_platinum]], colWidths=[card_width, card_width])
    t_compare_row.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))
    story.append(t_compare_row)
    story.append(Spacer(1, 10))

    # PRODUCTION SPRINT ROADMAP
    story.append(Paragraph("<b>OUR 4-PHASE DESIGN SPRINT PROCESS</b>", styles['SectionHeader']))
    roadmap_data = [
        [
            Paragraph("<b>PHASE 1: BRAND DISCOVERY (Day 1)</b><br/><font color='#64748B'>Review of your draft documents, core service pillars, target audience demographics, and tonal benchmarks.</font>", styles['BodyRegular']),
            Paragraph("<b>PHASE 2: 3D CONCEPT PRESENTATION (Days 2–3)</b><br/><font color='#64748B'>Receive 3 distinct visual directions presented on real-world mockups (stationery, profile cover &amp; brochure).</font>", styles['BodyRegular']),
        ],
        [
            Paragraph("<b>PHASE 3: PROFILE &amp; COLLATERAL REFINEMENT (Days 4–5)</b><br/><font color='#64748B'>Iterative layout polish on your company profile pages, service matrices, typography, and color consistency.</font>", styles['BodyRegular']),
            Paragraph("<b>PHASE 4: MASTER VECTOR ASSET HANDOVER (Day 5)</b><br/><font color='#64748B'>Delivery of high-resolution master vectors (AI, EPS, SVG), 300 DPI CMYK print files, and 100% copyright ownership.</font>", styles['BodyRegular']),
        ]
    ]
    t_road = Table(roadmap_data, colWidths=[CONTENT_WIDTH / 2, CONTENT_WIDTH / 2])
    t_road.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 1, C_BORDER),
        ('GRID', (0, 0), (-1, -1), 0.5, C_BORDER),
        ('BACKGROUND', (0, 0), (-1, -1), C_WHITE),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t_road)
    story.append(Spacer(1, 8))

    # ENGAGEMENT TERMS & CALL TO ACTION
    cta_box_text = (
        "<font size='10.5' color='#3600DF'><b>How to Activate Your Branding Sprint:</b></font><br/>"
        "&bull; <b>50% Project Initiation Deposit:</b> Locks in your dedicated design team and initiates Phase 1 immediately.<br/>"
        "&bull; <b>50% Balance on Live Approval:</b> Payable only after final inspection and your 100% satisfaction.<br/>"
        "&bull; <b>Direct M-Pesa / Bank Dispatch:</b> Invoicing details provided upon package confirmation.<br/><br/>"
        "<b>Lead Brand Designer:</b> Samuel Kidemi Kisaga &bull; <b>Agency Co-Founder:</b> David Esabwa<br/>"
        "<b>Direct Phone / WhatsApp:</b> +254 722 753 819 &bull; <b>Digital Portfolio:</b> www.xclusivetech.co.ke"
    )
    p_cta_box = Paragraph(cta_box_text, styles['BodyRegular'])
    t_cta_box = Table([[p_cta_box]], colWidths=[CONTENT_WIDTH])
    t_cta_box.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#EEF2FF')),
        ('BOX', (0, 0), (-1, -1), 1.25, C_PRIMARY),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ]))
    story.append(t_cta_box)

    doc.build(story, canvasmaker=EliteNumberedCanvas)
    print(f"Generated Proposal PDF: {OUTPUT_PDF} ({os.path.getsize(OUTPUT_PDF)} bytes)")


if __name__ == '__main__':
    build_proposal()
