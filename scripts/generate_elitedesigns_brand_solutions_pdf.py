#!/usr/bin/env python3
"""
Elite Designs Kenya — Corporate Brand Identity & Collateral Solutions Proposal
Tailored for Career Clinic: Translating Hope, Trust, and Care into Visual Authority.
Investment: KES 12,500 (Master Logo Evolution, Color Palette, Company Profile 6-8p, Services Brochure/Rate Card).
Calendar & Stationery removed per user instruction.
Features:
- Crisp, elegant 1-page executive presentation layout
- Faint centered Elite Designs logo watermark
- Exact KES 12,500 pricing (50% deposit = KES 6,250)
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, Table, TableStyle, HRFlowable
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
C_GOLD = colors.HexColor('#D97706')         # Warm Amber Gold
C_GOLD_LIGHT = colors.HexColor('#FEF3C7')   # Soft Amber Tint
C_DARK = colors.HexColor('#0F172A')         # Slate 900
C_BODY = colors.HexColor('#334155')         # Slate 700
C_MUTED = colors.HexColor('#64748B')        # Slate 500
C_BORDER = colors.HexColor('#E2E8F0')       # Slate 200
C_WHITE = colors.HexColor('#FFFFFF')

LOGO_PATH = 'assets/images/elitedesigns_logo.png'
OUTPUT_PDF = 'assets/documents/Elite_Designs_Brand_Solutions_Proposal.pdf'
os.makedirs(os.path.dirname(OUTPUT_PDF), exist_ok=True)

PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN_LEFT = 36
MARGIN_RIGHT = 36
MARGIN_TOP = 32
MARGIN_BOTTOM = 32
CONTENT_WIDTH = PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT # 523.28 pt


class EliteWatermarkedCanvas(canvas.Canvas):
    """Single-pass canvas with running header, footer, and faint centered logo watermark."""
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
            self.setFillAlpha(0.022) # Whisper-soft, luxury background watermark
            wm_w = 320
            wm_h = 80
            wm_x = (PAGE_WIDTH - wm_w) / 2
            wm_y = (PAGE_HEIGHT - wm_h) / 2
            self.drawImage(LOGO_PATH, wm_x, wm_y, width=wm_w, height=wm_h, preserveAspectRatio=True, mask='auto')
            self.restoreState()

        # Running Footer
        footer_y = MARGIN_BOTTOM - 14
        self.setStrokeColor(C_BORDER)
        self.setLineWidth(0.5)
        self.line(MARGIN_LEFT, footer_y + 11, PAGE_WIDTH - MARGIN_RIGHT, footer_y + 11)

        self.setFont('Comfortaa-Bold', 7)
        self.setFillColor(C_PRIMARY)
        self.drawString(MARGIN_LEFT, footer_y + 1, "ELITE DESIGNS KENYA")
        self.setFont('Comfortaa', 7)
        self.setFillColor(C_MUTED)
        self.drawString(MARGIN_LEFT + 92, footer_y + 1, "• Tailored Brand Identity & Collateral Proposal • +254 722 753 819")

        page_str = f"Page {page_num} of {total_pages}"
        self.setFont('Comfortaa-Bold', 7)
        self.setFillColor(C_DARK)
        self.drawRightString(PAGE_WIDTH - MARGIN_RIGHT, footer_y + 1, page_str)

        self.restoreState()


def get_styles():
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        'MainTitle',
        fontName='Comfortaa-Bold',
        fontSize=18,
        leading=23,
        textColor=C_DARK,
        alignment=TA_LEFT
    ))

    styles.add(ParagraphStyle(
        'MainSubtitle',
        fontName='Comfortaa',
        fontSize=8.5,
        leading=12.5,
        textColor=C_MUTED,
        alignment=TA_LEFT
    ))

    styles.add(ParagraphStyle(
        'SectionTitle',
        fontName='Comfortaa-Bold',
        fontSize=9.5,
        leading=13,
        textColor=C_PRIMARY,
        spaceBefore=6,
        spaceAfter=3
    ))

    styles.add(ParagraphStyle(
        'CardHeading',
        fontName='Comfortaa-Bold',
        fontSize=9.5,
        leading=13,
        textColor=C_DARK
    ))

    styles.add(ParagraphStyle(
        'CustomBody',
        fontName='Comfortaa',
        fontSize=7.8,
        leading=11.5,
        textColor=C_BODY
    ))

    styles.add(ParagraphStyle(
        'PillarText',
        fontName='Comfortaa',
        fontSize=7.5,
        leading=11,
        textColor=C_BODY
    ))

    styles.add(ParagraphStyle(
        'Badge',
        fontName='Comfortaa-Bold',
        fontSize=6.8,
        leading=9,
        textColor=C_PRIMARY
    ))

    styles.add(ParagraphStyle(
        'BadgeGold',
        fontName='Comfortaa-Bold',
        fontSize=7,
        leading=9.5,
        textColor=colors.HexColor('#92400E')
    ))

    styles.add(ParagraphStyle(
        'PriceDisplay',
        fontName='Comfortaa-Bold',
        fontSize=17,
        leading=20,
        textColor=C_ACCENT,
        alignment=TA_RIGHT
    ))

    styles.add(ParagraphStyle(
        'PriceSub',
        fontName='Comfortaa',
        fontSize=7,
        leading=9.5,
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

    # 1. Header Row
    if os.path.exists(LOGO_PATH):
        story.append(RLImage(LOGO_PATH, width=140, height=35))
    story.append(Spacer(1, 4))

    # Pill badge
    p_badge = Paragraph("<b>OFFICIAL BRAND IDENTITY &amp; COLLATERAL PROPOSAL</b>", styles['Badge'])
    t_badge = Table([[p_badge]], colWidths=[270])
    t_badge.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), C_PRIMARY_LIGHT),
        ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor('#C7D2FE')),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_badge)
    story.append(Spacer(1, 4))

    story.append(Paragraph("Brand Identity &amp; Corporate Collateral Suite", styles['MainTitle']))
    story.append(Paragraph("Translating Hope, Trust, and Care into an institutional visual ecosystem for career consulting.", styles['MainSubtitle']))
    story.append(Spacer(1, 6))

    # 2. Strategic Brand Soul Callout
    soul_text = (
        "<b>Strategic Brand Positioning: A Dedicated Clinic for Career Renewal</b><br/>"
        "Career Clinic is not an ordinary CV shop on LinkedIn. It is a vital haven and consulting clinic for professionals "
        "experiencing frustration, career stagnation, or hurt in their workplace journeys. Your clients seek reassurance, empathy, "
        "and transformative guidance. Elite Designs takes your complete draft materials and elevates them into a cohesive, warm, "
        "and distinctive brand presence that evokes <b>Hope, Trust, and Care</b> from their very first interaction."
    )
    p_soul = Paragraph(soul_text, styles['CustomBody'])
    t_soul = Table([[p_soul]], colWidths=[CONTENT_WIDTH])
    t_soul.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
        ('BOX', (0, 0), (-1, -1), 1, C_BORDER),
        ('LINEBEFORE', (0, 0), (0, -1), 3.5, C_PRIMARY),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(t_soul)
    story.append(Spacer(1, 8))

    # 3. SPOTLIGHT SUITE: KES 12,500 PACKAGE
    GOLD_PAD_X = 12
    GOLD_INNER_W = CONTENT_WIDTH - (GOLD_PAD_X * 2)

    p_gold_tag = Paragraph("★ TAILORED BRAND SPRINT &bull; CORE DELIVERABLES", styles['BadgeGold'])
    t_gold_tag = Table([[p_gold_tag]], colWidths=[205])
    t_gold_tag.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), C_GOLD_LIGHT),
        ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor('#FCD34D')),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))

    hdr_left = [
        t_gold_tag,
        Spacer(1, 2),
        Paragraph("Corporate Brand Identity &amp; Collateral Suite", styles['CardHeading']),
        Paragraph("<font color='#64748B'>Master Logo Evolution, Restorative Palette, Company Profile &amp; Services Brochure</font>", styles['CustomBody'])
    ]
    hdr_right = [
        Paragraph("KES 16,000", styles['PriceDisplay']),
        Paragraph("Complete Brand Sprint &bull; 3–4 Days Delivery", styles['PriceSub'])
    ]
    t_hdr = Table([[hdr_left, hdr_right]], colWidths=[330, GOLD_INNER_W - 330])
    t_hdr.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))

    # 4 Clean Deliverable Pillars
    GRID_GAP = 10
    col_w = (GOLD_INNER_W - GRID_GAP) / 2

    # Pillar 1
    p1_content = [
        Paragraph("<b>1. Master Logo Evolution (2 Concepts Upgraded)</b>", styles['CardHeading']),
        Spacer(1, 2),
        Paragraph(
            "&bull; <b>Upgraded from Your 2 Drafts:</b> We take your two existing draft logos and elevate them into polished, modern emblems "
            "symbolizing career healing, growth, and forward momentum.<br/>"
            "&bull; <b>Full Master Vectors:</b> Adobe Illustrator (AI), EPS, SVG, and high-res transparent PNGs (dark/light versions).",
            styles['PillarText']
        )
    ]
    t_p1 = Table([[p1_content]], colWidths=[col_w])
    t_p1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), C_WHITE),
        ('BOX', (0, 0), (-1, -1), 1, C_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))

    # Pillar 2
    p2_content = [
        Paragraph("<b>2. Color Psychology &amp; Typography</b>", styles['CardHeading']),
        Spacer(1, 2),
        Paragraph(
            "&bull; <b>Hope, Trust &amp; Care Palette:</b> Replacing plain corporate colors with psychology-backed restorative tones "
            "that blend institutional trust with approachable human warmth.<br/>"
            "&bull; <b>Usage Standards:</b> Calibrated CMYK for print, HEX/RGB for digital, and modern Google Font pairings.",
            styles['PillarText']
        )
    ]
    t_p2 = Table([[p2_content]], colWidths=[col_w])
    t_p2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), C_WHITE),
        ('BOX', (0, 0), (-1, -1), 1, C_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))

    # Pillar 3
    p3_content = [
        Paragraph("<b>3. Executive Company Profile (6–8 Pages)</b>", styles['CardHeading']),
        Spacer(1, 2),
        Paragraph(
            "&bull; <b>Visual Re-Architecture:</b> Restructuring your existing draft text into an authoritative, tender-ready B2B presentation.<br/>"
            "&bull; <b>Editorial Polish:</b> Professional typography pacing, service highlights, executive bios, and client journey flow.",
            styles['PillarText']
        )
    ]
    t_p3 = Table([[p3_content]], colWidths=[col_w])
    t_p3.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), C_WHITE),
        ('BOX', (0, 0), (-1, -1), 1, C_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))

    # Pillar 4
    p4_content = [
        Paragraph("<b>4. Services Brochure &amp; Rate Card Overhaul</b>", styles['CardHeading']),
        Spacer(1, 2),
        Paragraph(
            "&bull; <b>Pricing Matrices:</b> Elegant redesign of your CV &amp; coaching package rate card for effortless client decision-making.<br/>"
            "&bull; <b>Dual Formats:</b> Print-ready bi-fold brochure + interactive digital PDF with clickable WhatsApp links.",
            styles['PillarText']
        )
    ]
    t_p4 = Table([[p4_content]], colWidths=[col_w])
    t_p4.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), C_WHITE),
        ('BOX', (0, 0), (-1, -1), 1, C_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))

    t_grid_1 = Table([[t_p1, '', t_p2]], colWidths=[col_w, GRID_GAP, col_w])
    t_grid_1.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))

    t_grid_2 = Table([[t_p3, '', t_p4]], colWidths=[col_w, GRID_GAP, col_w])
    t_grid_2.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))

    gold_box = [
        t_hdr,
        Spacer(1, 6),
        HRFlowable(width="100%", thickness=0.75, color=colors.HexColor('#FDE68A'), spaceBefore=1, spaceAfter=6),
        t_grid_1,
        Spacer(1, 5),
        t_grid_2
    ]

    t_gold_wrapper = Table([[gold_box]], colWidths=[CONTENT_WIDTH])
    t_gold_wrapper.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#FFFDF9')),
        ('BOX', (0, 0), (-1, -1), 1.5, colors.HexColor('#F59E0B')),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), GOLD_PAD_X),
        ('RIGHTPADDING', (0, 0), (-1, -1), GOLD_PAD_X),
    ]))
    story.append(t_gold_wrapper)
    story.append(Spacer(1, 8))

    # 4. SPRINT TIMELINE (4 Steps)
    story.append(Paragraph("<b>4-PHASE PRODUCTION ROADMAP (3–4 DAYS)</b>", styles['SectionTitle']))
    roadmap_data = [
        [
            Paragraph("<b>PHASE 1: INTAKE (Day 1)</b><br/><font color='#64748B'>Review of your 2 logo drafts, copy files, and tonal priorities.</font>", styles['PillarText']),
            Paragraph("<b>PHASE 2: CONCEPTS (Days 1–2)</b><br/><font color='#64748B'>Receive 2 upgraded visual directions exploring Hope, Trust &amp; Care on mockups.</font>", styles['PillarText']),
            Paragraph("<b>PHASE 3: POLISH (Days 2–3)</b><br/><font color='#64748B'>Iterative layout refinement of your company profile &amp; rate card.</font>", styles['PillarText']),
            Paragraph("<b>PHASE 4: HANDOVER (Day 4)</b><br/><font color='#64748B'>Delivery of AI/EPS/SVG vectors, print PDFs, and full copyright.</font>", styles['PillarText']),
        ]
    ]
    step_w = CONTENT_WIDTH / 4
    t_road = Table(roadmap_data, colWidths=[step_w, step_w, step_w, step_w])
    t_road.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 1, C_BORDER),
        ('GRID', (0, 0), (-1, -1), 0.5, C_BORDER),
        ('BACKGROUND', (0, 0), (-1, -1), C_WHITE),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_road)
    story.append(Spacer(1, 8))

    # 5. TRANSPARENT TERMS & ACTIVATION (KES 16,000)
    cta_box_text = (
        "<font size='9.5' color='#3600DF'><b>Commercial Terms &amp; Project Activation:</b></font><br/>"
        "&bull; <b>Total Package Investment:</b> KES 16,000 (Covers Master Logo Evolution, Palette, 6–8p Company Profile &amp; Services Brochure).<br/>"
        "&bull; <b>50% Project Initiation Deposit (KES 8,000):</b> Reserves your senior design sprint and activates Phase 1 creative work.<br/>"
        "&bull; <b>50% Balance on Live Approval (KES 8,000):</b> Payable only after final inspection and your 100% satisfaction.<br/>"
        "&bull; <b>100% Full Vector Ownership:</b> All master vector files (AI, EPS, SVG) and commercial copyright transferred to Career Clinic.<br/><br/>"
        "<b>Lead Brand Designer:</b> Samuel Kidemi Kisaga &bull; <b>Agency Co-Founder:</b> David Esabwa &bull; <b>WhatsApp / Calls:</b> +254 722 753 819"
    )
    p_cta_box = Paragraph(cta_box_text, styles['CustomBody'])
    t_cta_box = Table([[p_cta_box]], colWidths=[CONTENT_WIDTH])
    t_cta_box.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#EEF2FF')),
        ('BOX', (0, 0), (-1, -1), 1.25, C_PRIMARY),
        ('LINEBEFORE', (0, 0), (0, -1), 3.5, C_ACCENT),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(t_cta_box)

    doc.build(story, canvasmaker=EliteWatermarkedCanvas)
    print(f"Generated 16K Proposal PDF: {OUTPUT_PDF} ({os.path.getsize(OUTPUT_PDF)} bytes)")


if __name__ == '__main__':
    build_proposal()
