#!/usr/bin/env python3
"""
Elite Designs Kenya — Startup Branding Packages & Presentation Rate Card (2026)
Incorporating Company Profiles, Services Brochures, Full Stationery, Calendars.
3 Tiers (+10k adjusted):
- Silver Starter: KES 22,500
- Gold Growth (Flagship): KES 35,000
- Platinum Enterprise: KES 55,000
Built with ReportLab, Comfortaa font, and official transparent Elite Designs logo.
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

LOGO_PATH = 'assets/images/elitedesigns_logo.png'
OUTPUT_PDF = 'assets/documents/Elite_Designs_Startup_Branding_Packages.pdf'
DOWNLOADS_PDF = '/Users/app/Downloads/Elite_Designs_Startup_Branding_Packages.pdf'
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
            self.drawRightString(PAGE_WIDTH - MARGIN_RIGHT, header_y + 3, "ELITE DESIGNS KENYA • STARTUP BRANDING PACKAGES")
            
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
        'CoverTitle',
        fontName='Comfortaa-Bold',
        fontSize=19,
        leading=24,
        textColor=C_DARK,
        alignment=TA_LEFT
    ))

    styles.add(ParagraphStyle(
        'CoverSubtitle',
        fontName='Comfortaa',
        fontSize=9,
        leading=13,
        textColor=C_MUTED,
        alignment=TA_LEFT
    ))

    styles.add(ParagraphStyle(
        'TierTitle',
        fontName='Comfortaa-Bold',
        fontSize=12,
        leading=15,
        textColor=C_DARK,
        alignment=TA_LEFT
    ))

    styles.add(ParagraphStyle(
        'TierPrice',
        fontName='Comfortaa-Bold',
        fontSize=14,
        leading=17,
        textColor=C_PRIMARY,
        alignment=TA_LEFT
    ))

    styles.add(ParagraphStyle(
        'TierPriceGold',
        fontName='Comfortaa-Bold',
        fontSize=14,
        leading=17,
        textColor=C_ACCENT,
        alignment=TA_LEFT
    ))

    styles.add(ParagraphStyle(
        'TierMeta',
        fontName='Comfortaa',
        fontSize=7.5,
        leading=10,
        textColor=C_MUTED,
        alignment=TA_LEFT
    ))

    styles.add(ParagraphStyle(
        'FeatureItem',
        fontName='Comfortaa',
        fontSize=7.2,
        leading=10,
        textColor=C_BODY
    ))

    styles.add(ParagraphStyle(
        'SectionHeader',
        fontName='Comfortaa-Bold',
        fontSize=10.5,
        leading=14,
        textColor=C_DARK
    ))

    styles.add(ParagraphStyle(
        'ScriptBoxText',
        fontName='Comfortaa',
        fontSize=8,
        leading=11.5,
        textColor=C_DARK
    ))

    return styles


def build_branding_pdf():
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
    # PAGE 1: 3-TIER PACKAGES (SILVER 22.5k, GOLD 35k, PLATINUM 55k)
    # =========================================================================
    if os.path.exists(LOGO_PATH):
        story.append(RLImage(LOGO_PATH, width=160, height=40))
    story.append(Spacer(1, 6))

    badge_html = "<font color='#3600DF'><b>OFFICIAL 2026 COMMERCIAL PROPOSAL &bull; STARTUP BRAND IDENTITY SUITES</b></font>"
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

    story.append(Paragraph("Startup Brand Identity &amp; Corporate Collateral Packages", styles['CoverTitle']))
    story.append(Paragraph("Unified visual branding: Master logos, executive stationery, brochures, company profiles &amp; corporate calendars.", styles['CoverSubtitle']))
    story.append(Spacer(1, 8))

    col_w = (CONTENT_WIDTH - 14) / 3

    # CARD 1: SILVER STARTER BRAND (KES 22,500)
    silver_header = [
        Paragraph("<font color='#64748B'><b>TIER 01 &bull; ESSENTIAL</b></font>", styles['TierMeta']),
        Paragraph("Silver Starter", styles['TierTitle']),
        Paragraph("<font color='#3600DF'><b>KES 22,500</b></font>", styles['TierPrice']),
        Paragraph("Turnaround: <b>3 Business Days</b>", styles['TierMeta'])
    ]
    silver_features = [
        Paragraph("<b>1. Master Logo Suite:</b><br/>&bull; 3 Bespoke Design Concepts<br/>&bull; Vector Masters (AI, EPS, SVG)<br/>&bull; Transparent PNGs (Dark/Light)<br/>&bull; Color Codes (HEX, RGB, CMYK)", styles['FeatureItem']),
        Spacer(1, 3),
        Paragraph("<b>2. Core Corporate Stationery:</b><br/>&bull; Business Cards (Double-Sided CMYK)<br/>&bull; Official Letterhead (.docx + PDF)", styles['FeatureItem']),
        Spacer(1, 3),
        Paragraph("<b>3. Marketing Collateral:</b><br/>&bull; Bi-Fold Services Brochure OR<br/>&bull; 2-Sided Promotional Sales Flyer", styles['FeatureItem']),
        Spacer(1, 3),
        Paragraph("<b>4. Digital Touchpoints:</b><br/>&bull; Clickable Email Signature<br/>&bull; Social Media Profile Icons (All Apps)", styles['FeatureItem']),
        Spacer(1, 3),
        Paragraph("<b>5. Guarantees &amp; Rights:</b><br/>&bull; 2 Iterative Revision Rounds<br/>&bull; 100% Commercial Copyright", styles['FeatureItem']),
    ]
    silver_card_data = [
        [Table([[item] for item in silver_header], colWidths=[col_w - 14])],
        [HRFlowable(width="100%", thickness=1, color=C_BORDER, spaceBefore=3, spaceAfter=4)],
        [Table([[item] for item in silver_features], colWidths=[col_w - 14])]
    ]
    t_silver = Table(silver_card_data, colWidths=[col_w])
    t_silver.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), C_WHITE),
        ('BOX', (0, 0), (-1, -1), 1, C_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 7),
        ('RIGHTPADDING', (0, 0), (-1, -1), 7),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))

    # CARD 2: GOLD GROWTH BRAND (KES 35,000 - FLAGSHIP)
    gold_header = [
        Paragraph("<font color='#D97706'><b>MOST POPULAR &bull; COMPLETE</b></font>", styles['TierMeta']),
        Paragraph("Gold Growth", styles['TierTitle']),
        Paragraph("<font color='#F22732'><b>KES 35,000</b></font>", styles['TierPriceGold']),
        Paragraph("Turnaround: <b>4–5 Business Days</b>", styles['TierMeta'])
    ]
    gold_features = [
        Paragraph("<b>Everything in Silver, plus:</b>", styles['FeatureItem']),
        Spacer(1, 2),
        Paragraph("<b>1. Corporate Company Profile:</b><br/>&bull; <b>6–8 Page Company Profile</b><br/>&bull; Executive Bio, Services &amp; Tenders", styles['FeatureItem']),
        Spacer(1, 2),
        Paragraph("<b>2. Full Stationery &amp; Calendar Suite:</b><br/>&bull; Business Cards (Up to 3 Staff Members)<br/>&bull; Branded Envelopes (DL &amp; C5 Sizes)<br/>&bull; Corporate Compliment Slips<br/>&bull; Presentation Folder Cover (A4)<br/>&bull; <b>Custom Corporate Calendar</b> (Desk/Wall)", styles['FeatureItem']),
        Spacer(1, 2),
        Paragraph("<b>3. Interactive Brand Identity:</b><br/>&bull; Contactless Digital Card with QR Code<br/>&bull; Official Brand Style Sheet (Rules/Fonts)", styles['FeatureItem']),
        Spacer(1, 2),
        Paragraph("<b>4. Priority Support:</b><br/>&bull; 3 Iterative Revision Rounds", styles['FeatureItem']),
    ]
    gold_card_data = [
        [Table([[item] for item in gold_header], colWidths=[col_w - 14])],
        [HRFlowable(width="100%", thickness=1.5, color=C_ACCENT, spaceBefore=3, spaceAfter=4)],
        [Table([[item] for item in gold_features], colWidths=[col_w - 14])]
    ]
    t_gold = Table(gold_card_data, colWidths=[col_w])
    t_gold.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#FFFDF5')),
        ('BOX', (0, 0), (-1, -1), 2, C_ACCENT),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 7),
        ('RIGHTPADDING', (0, 0), (-1, -1), 7),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))

    # CARD 3: PLATINUM ENTERPRISE (KES 55,000 - MARKET LEADER)
    plat_header = [
        Paragraph("<font color='#3600DF'><b>TIER 03 &bull; MARKET LEADER</b></font>", styles['TierMeta']),
        Paragraph("Platinum Scale", styles['TierTitle']),
        Paragraph("<font color='#3600DF'><b>KES 55,000</b></font>", styles['TierPrice']),
        Paragraph("Turnaround: <b>7 Business Days</b>", styles['TierMeta'])
    ]
    plat_features = [
        Paragraph("<b>Everything in Gold, plus:</b>", styles['FeatureItem']),
        Spacer(1, 2),
        Paragraph("<b>1. Comprehensive Sales Collateral:</b><br/>&bull; <b>12–16 Page Master Company Profile</b><br/>&bull; Multi-Page Services Product Catalog<br/>&bull; <b>Roll-Up Banner</b> (85cm × 200cm CMYK)", styles['FeatureItem']),
        Spacer(1, 2),
        Paragraph("<b>2. Corporate Merch &amp; Packaging:</b><br/>&bull; Staff T-Shirt / Polo Embroidery Vector<br/>&bull; Branded Ceramic Coffee Mug Artwork<br/>&bull; Retail Kraft Shopping Bag Design", styles['FeatureItem']),
        Spacer(1, 2),
        Paragraph("<b>3. Brand Manual &amp; Calendars:</b><br/>&bull; Master 16-Page Brand Identity Book<br/>&bull; Wall &amp; Desk Calendar Suite", styles['FeatureItem']),
        Spacer(1, 2),
        Paragraph("<b>4. VIP Unlimited Revisions:</b><br/>&bull; Direct Lead Designer Sprint", styles['FeatureItem']),
    ]
    plat_card_data = [
        [Table([[item] for item in plat_header], colWidths=[col_w - 14])],
        [HRFlowable(width="100%", thickness=1, color=C_PRIMARY, spaceBefore=3, spaceAfter=4)],
        [Table([[item] for item in plat_features], colWidths=[col_w - 14])]
    ]
    t_plat = Table(plat_card_data, colWidths=[col_w])
    t_plat.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), C_WHITE),
        ('BOX', (0, 0), (-1, -1), 1, C_PRIMARY),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 7),
        ('RIGHTPADDING', (0, 0), (-1, -1), 7),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))

    grid_table = Table([[t_silver, t_gold, t_plat]], colWidths=[col_w, col_w, col_w])
    grid_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))
    story.append(grid_table)
    story.append(Spacer(1, 7))

    guar_html = (
        "<b>Institutional Creative Standard:</b> 100% vector scalability (AI, EPS, SVG), 300 DPI CMYK commercial print calibration, "
        "and complete copyright transfer assigned in writing upon final project sign-off."
    )
    p_guar = Paragraph(guar_html, styles['TierMeta'])
    t_guar = Table([[p_guar]], colWidths=[CONTENT_WIDTH])
    t_guar.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), C_SOFT_BG),
        ('BOX', (0, 0), (-1, -1), 1, C_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t_guar)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: MEETING TALKING POINTS & CLOSING SCRIPT
    # =========================================================================
    story.append(Spacer(1, 4))
    story.append(Paragraph("Meeting Talking Points &amp; Closing Words", styles['CoverTitle']))
    story.append(Paragraph("Read these exact word-for-word lines to present the packages and close the deal.", styles['CoverSubtitle']))
    story.append(Spacer(1, 8))

    # Point 1: The Pitch
    p1_text = (
        "When launching or growing your business, your branding directly determines your pricing power. "
        "If your visual identity, company profile, and stationery look pieced together or amateur, corporate clients "
        "assume you are a high-risk vendor and haggle down your fees. We created these all-inclusive packages so your "
        "business presents immediate institutional credibility in boardroom meetings, tenders, and client presentations."
    )
    story.append(Paragraph("<b>1. THE 20-SECOND VALUE PROPOSITION</b>", styles['SectionHeader']))
    p_p1 = Paragraph(f'<i>"{p1_text}"</i>', styles['ScriptBoxText'])
    t_p1 = Table([[p_p1]], colWidths=[CONTENT_WIDTH])
    t_p1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
        ('BOX', (0, 0), (-1, -1), 1, C_BORDER),
        ('LINEBEFORE', (0, 0), (0, -1), 3.5, C_PRIMARY),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(t_p1)
    story.append(Spacer(1, 7))

    # Point 2: The Gold Recommendation (KES 35,000)
    p2_text = (
        "Our flagship recommendation is the <b>Gold Growth Package at KES 35,000</b>. "
        "It gives you a complete corporate branding powerhouse: a master vector logo, an official <b>6–8 page Company Profile</b> "
        "for tenders and investors, executive business cards for up to 3 staff members, official letterhead, corporate envelopes, "
        "compliment slips, presentation folders, and your official <b>corporate calendar</b>. "
        "In 4 to 5 days, your startup looks like an established multi-million shilling enterprise."
    )
    story.append(Paragraph("<b>2. WHY THE GOLD PACKAGE (KES 35,000) IS THE RECOMMENDED CHOICE</b>", styles['SectionHeader']))
    p_p2 = Paragraph(f'<i>"{p2_text}"</i>', styles['ScriptBoxText'])
    t_p2 = Table([[p_p2]], colWidths=[CONTENT_WIDTH])
    t_p2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#FFFDF5')),
        ('BOX', (0, 0), (-1, -1), 1.5, C_ACCENT),
        ('LINEBEFORE', (0, 0), (0, -1), 4, C_ACCENT),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(t_p2)
    story.append(Spacer(1, 7))

    # Point 3: The Risk Reversal & Closing
    p3_text = (
        "<b>Zero Risk Commercial Terms:</b> You only pay a <b>50% deposit</b> to initiate the sprint. We present initial "
        "concept mockups within 48 to 72 hours, refine them through dedicated revision rounds, and you only clear "
        "the remaining 50% balance after you inspect and approve your final live brand suite.<br/><br/>"
        "<b>The Direct Closing Ask:</b><br/>"
        "<i>'Between the Silver at 22.5k and the Gold at 35k with the full Company Profile and Stationery, "
        "which one matches your immediate launch timeline best? We can lock in your 50% deposit today and start your concept sprint immediately.'</i>"
    )
    story.append(Paragraph("<b>3. RISK REVERSAL &amp; THE CLOSING ASK</b>", styles['SectionHeader']))
    p_p3 = Paragraph(p3_text, styles['ScriptBoxText'])
    t_p3 = Table([[p_p3]], colWidths=[CONTENT_WIDTH])
    t_p3.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#EEF2FF')),
        ('BOX', (0, 0), (-1, -1), 1.5, C_PRIMARY),
        ('LINEBEFORE', (0, 0), (0, -1), 4, C_PRIMARY),
        ('TOPPADDING', (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(t_p3)
    story.append(Spacer(1, 8))

    cred_html = (
        "<b>Elite Designs Kenya &bull; Top Web &amp; Design Firm (Digitally Fit Awards Winner)</b><br/>"
        "Direct Contact: Samuel Kidemi &bull; Phone / WhatsApp: <b>+254 722 753 819</b> &bull; Nairobi, Kenya &bull; www.xclusivetech.co.ke"
    )
    p_cred = Paragraph(cred_html, styles['TierMeta'])
    story.append(p_cred)

    doc.build(story, canvasmaker=EliteNumberedCanvas)
    print(f"Generated Startup Branding Packages PDF: {OUTPUT_PDF} ({os.path.getsize(OUTPUT_PDF)} bytes)")


if __name__ == '__main__':
    build_branding_pdf()
