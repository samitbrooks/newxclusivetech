#!/usr/bin/env python3
"""
Career Clinic: Meta Campaign Proposal — Elite Designs Edition
Redesigns the generic Meta Campaign Proposal document with:
- Comfortaa typography throughout
- Official Elite Designs logo and corporate color palette (Royal Indigo, Crimson Red, Slate)
- Exact verbatim content preserved 100%
- Faint, elegant centered Elite Designs watermark
- Professional executive table and clean deliverable cards
- Perfectly proportioned single-page executive document
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

# 2. Elite Designs Brand Palette
C_PRIMARY = colors.HexColor('#3600DF')      # Electric Royal Indigo
C_PRIMARY_DARK = colors.HexColor('#22008F') # Deep Royal Indigo
C_PRIMARY_LIGHT = colors.HexColor('#EEF2FF')# Soft Indigo Tint
C_ACCENT = colors.HexColor('#F22732')       # Crimson Red
C_DARK = colors.HexColor('#0F172A')         # Slate 900
C_BODY = colors.HexColor('#334155')         # Slate 700
C_MUTED = colors.HexColor('#64748B')        # Slate 500
C_BORDER = colors.HexColor('#CBD5E1')       # Slate 300
C_BORDER_LIGHT = colors.HexColor('#E2E8F0') # Slate 200
C_CARD_BG = colors.HexColor('#F8FAFC')      # Slate 50
C_WHITE = colors.HexColor('#FFFFFF')

LOGO_PATH = 'assets/images/elitedesigns_logo.png'
OUTPUT_PDF = 'assets/documents/Career_Clinic_Meta_Campaign_Proposal.pdf'
DOWNLOADS_PDF = '/Users/app/Downloads/Career_Clinic_Meta_Campaign_Proposal.pdf'
os.makedirs(os.path.dirname(OUTPUT_PDF), exist_ok=True)

PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN_LEFT = 36
MARGIN_RIGHT = 36
MARGIN_TOP = 28
MARGIN_BOTTOM = 28
CONTENT_WIDTH = PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT # 523.28 pt


class EliteWatermarkedCanvas(canvas.Canvas):
    """Canvas with top brand stripes, faint centered logo watermark, and running footer."""
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

        # Top Accent Stripes
        self.saveState()
        self.setFillColor(C_PRIMARY)
        self.rect(0, PAGE_HEIGHT - 4, PAGE_WIDTH, 4, fill=1, stroke=0)
        self.setFillColor(C_ACCENT)
        self.rect(0, PAGE_HEIGHT - 6, 160, 2, fill=1, stroke=0)

        # Faint Centered Logo Watermark (Middle of Page)
        if os.path.exists(LOGO_PATH):
            self.saveState()
            self.setFillAlpha(0.022) # Soft, luxury background watermark
            wm_w = 330
            wm_h = 82
            wm_x = (PAGE_WIDTH - wm_w) / 2
            wm_y = (PAGE_HEIGHT - wm_h) / 2
            self.drawImage(LOGO_PATH, wm_x, wm_y, width=wm_w, height=wm_h, preserveAspectRatio=True, mask='auto')
            self.restoreState()

        # Running Footer
        footer_y = MARGIN_BOTTOM - 14
        self.setStrokeColor(C_BORDER_LIGHT)
        self.setLineWidth(0.5)
        self.line(MARGIN_LEFT, footer_y + 11, PAGE_WIDTH - MARGIN_RIGHT, footer_y + 11)

        self.setFont('Comfortaa-Bold', 7)
        self.setFillColor(C_PRIMARY)
        self.drawString(MARGIN_LEFT, footer_y + 1, "ELITE DESIGNS KENYA")
        self.setFont('Comfortaa', 7)
        self.setFillColor(C_MUTED)
        self.drawString(MARGIN_LEFT + 92, footer_y + 1, "• Career Clinic: Meta Campaign Proposal • Paid Media & Growth")

        page_str = f"Page {page_num} of {total_pages}"
        self.setFont('Comfortaa-Bold', 7)
        self.setFillColor(C_DARK)
        self.drawRightString(PAGE_WIDTH - MARGIN_RIGHT, footer_y + 1, page_str)

        self.restoreState()


def get_styles():
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        'DocTitle',
        fontName='Comfortaa-Bold',
        fontSize=18,
        leading=22,
        textColor=C_DARK,
        alignment=TA_LEFT
    ))

    styles.add(ParagraphStyle(
        'DocDate',
        fontName='Comfortaa',
        fontSize=8,
        leading=11,
        textColor=C_MUTED,
        alignment=TA_LEFT
    ))

    styles.add(ParagraphStyle(
        'SectionHeading',
        fontName='Comfortaa-Bold',
        fontSize=11,
        leading=15,
        textColor=C_PRIMARY,
        spaceBefore=6,
        spaceAfter=3
    ))

    styles.add(ParagraphStyle(
        'SubSectionHeading',
        fontName='Comfortaa-Bold',
        fontSize=8.5,
        leading=12,
        textColor=C_DARK,
        spaceBefore=4,
        spaceAfter=2
    ))

    styles.add(ParagraphStyle(
        'CustomBody',
        fontName='Comfortaa',
        fontSize=7.8,
        leading=11.6,
        textColor=C_BODY
    ))

    styles.add(ParagraphStyle(
        'BulletText',
        fontName='Comfortaa',
        fontSize=7.5,
        leading=10.8,
        textColor=C_BODY
    ))

    styles.add(ParagraphStyle(
        'TableHeader',
        fontName='Comfortaa-Bold',
        fontSize=8,
        leading=10.5,
        textColor=C_DARK
    ))

    styles.add(ParagraphStyle(
        'TableCell',
        fontName='Comfortaa',
        fontSize=7.8,
        leading=11,
        textColor=C_BODY
    ))

    styles.add(ParagraphStyle(
        'TableCellBold',
        fontName='Comfortaa-Bold',
        fontSize=8,
        leading=11,
        textColor=C_DARK
    ))

    styles.add(ParagraphStyle(
        'TableCellAmount',
        fontName='Comfortaa-Bold',
        fontSize=8.5,
        leading=11,
        textColor=C_PRIMARY,
        alignment=TA_RIGHT
    ))

    styles.add(ParagraphStyle(
        'TableCellAmountTotal',
        fontName='Comfortaa-Bold',
        fontSize=9,
        leading=12,
        textColor=C_ACCENT,
        alignment=TA_RIGHT
    ))

    styles.add(ParagraphStyle(
        'BadgeText',
        fontName='Comfortaa-Bold',
        fontSize=6.8,
        leading=9,
        textColor=C_PRIMARY
    ))

    return styles


def build_meta_proposal():
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

    # 1. Header with Elite Designs Logo and Metadata
    if os.path.exists(LOGO_PATH):
        story.append(RLImage(LOGO_PATH, width=135, height=34))
    story.append(Spacer(1, 4))

    # Pill badge
    p_badge = Paragraph("<b>PAID MEDIA STRATEGY &bull; CAMPAIGN PROPOSAL</b>", styles['BadgeText'])
    t_badge = Table([[p_badge]], colWidths=[240])
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

    # Title & Date
    story.append(Paragraph("Career Clinic: Meta Campaign Proposal", styles['DocTitle']))
    story.append(Paragraph("Date: October 19, 2026", styles['DocDate']))
    story.append(Spacer(1, 6))

    # 2. Overview Section
    story.append(Paragraph("Overview", styles['SectionHeading']))
    overview_p1 = (
        "This proposal outlines the paid media investment and the work to be delivered to launch and run a "
        "Meta (Facebook and Instagram) advertising campaign for <b>Career Clinic</b>. The campaign will build awareness "
        "of the product and generate qualified leads and sign-ups from job seekers and professionals looking for career support."
    )
    overview_p2 = (
        "The strategy is also tailored for schools that need Career Clinic, as there is a product made specifically "
        "for them. Messaging, creative and targeting will address both individual job seekers and schools."
    )
    story.append(Paragraph(overview_p1, styles['CustomBody']))
    story.append(Spacer(1, 3))
    story.append(Paragraph(overview_p2, styles['CustomBody']))
    story.append(Spacer(1, 7))

    # 3. Investment Summary Table
    story.append(Paragraph("Investment Summary", styles['SectionHeading']))
    
    table_data = [
        [
            Paragraph("Item", styles['TableHeader']),
            Paragraph("Description", styles['TableHeader']),
            Paragraph("Amount", ParagraphStyle('TableHeaderRight', parent=styles['TableHeader'], alignment=TA_RIGHT))
        ],
        [
            Paragraph("<b>Meta media budget</b>", styles['TableCell']),
            Paragraph("Ad spend paid directly to Meta for campaign delivery", styles['TableCell']),
            Paragraph("Ksh. 30,000", styles['TableCellAmount'])
        ],
        [
            Paragraph("<b>Stipend for work done</b>", styles['TableCell']),
            Paragraph("Fee for strategy, creative, setup, management and reporting", styles['TableCell']),
            Paragraph("Ksh. 27,500", styles['TableCellAmount'])
        ],
        [
            Paragraph("<b>Total investment</b>", styles['TableCellBold']),
            Paragraph("Comprehensive media spend and full campaign execution", styles['TableCell']),
            Paragraph("Ksh. 57,500", styles['TableCellAmountTotal'])
        ]
    ]

    col_item = 135
    col_amount = 100
    col_desc = CONTENT_WIDTH - col_item - col_amount # 288.28 pt

    t_invest = Table(table_data, colWidths=[col_item, col_desc, col_amount])
    t_invest.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F1F5F9')),
        ('BOX', (0, 0), (-1, -1), 1, C_BORDER),
        ('GRID', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('BACKGROUND', (0, 3), (-1, 3), colors.HexColor('#EEF2FF')),
        ('TOPPADDING', (0, 0), (-1, -1), 4.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t_invest)
    story.append(Spacer(1, 7))

    # 4. Deliverables Section
    story.append(Paragraph("Deliverables", styles['SectionHeading']))

    # To balance and keep uncluttered, we present the 5 Deliverables in 2 columns:
    # Left Column: 1. Strategy and Planning & 2. Creative Development
    # Right Column: 3. Campaign Setup & 4. Campaign Management & 5. Reporting
    left_deliverables = [
        Paragraph("1. Strategy and Planning", styles['SubSectionHeading']),
        Paragraph("&bull; Campaign strategy, objectives and success metrics (KPIs)", styles['BulletText']),
        Paragraph("&bull; Audience research and targeting plan (job seekers, early and mid-career professionals, career changers) and schools that need the school-specific Career Clinic product", styles['BulletText']),
        Paragraph("&bull; Budget allocation across campaign stages and placements", styles['BulletText']),
        Spacer(1, 5),
        Paragraph("2. Creative Development", styles['SubSectionHeading']),
        Paragraph("&bull; Ad copy and messaging tailored to Career Clinic, including its school-specific product", styles['BulletText']),
        Paragraph("&bull; Static and short-form video ad creatives for Facebook and Instagram feeds, Stories and Reels", styles['BulletText']),
        Paragraph("&bull; Call-to-action and landing page recommendations", styles['BulletText']),
    ]

    right_deliverables = [
        Paragraph("3. Campaign Setup", styles['SubSectionHeading']),
        Paragraph("&bull; Meta Business Manager and ad account configuration", styles['BulletText']),
        Paragraph("&bull; Pixel and conversion tracking setup", styles['BulletText']),
        Paragraph("&bull; Lead forms and/or landing page integration", styles['BulletText']),
        Spacer(1, 5),
        Paragraph("4. Campaign Management and Optimisation", styles['SubSectionHeading']),
        Paragraph("&bull; Day-to-day management of the Ksh. 30,000 media budget", styles['BulletText']),
        Paragraph("&bull; A/B testing of creatives, audiences and messaging", styles['BulletText']),
        Paragraph("&bull; Ongoing optimisation to improve cost per lead and conversion rate", styles['BulletText']),
        Spacer(1, 5),
        Paragraph("5. Reporting", styles['SubSectionHeading']),
        Paragraph("&bull; Weekly performance snapshots", styles['BulletText']),
        Paragraph("&bull; Final campaign report with results, insights and recommendations for next steps", styles['BulletText']),
    ]

    deliv_col_w = (CONTENT_WIDTH - 10) / 2
    t_deliv_left = Table([[left_deliverables]], colWidths=[deliv_col_w])
    t_deliv_left.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#FFFFFF')),
        ('BOX', (0, 0), (-1, -1), 1, C_BORDER_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))

    t_deliv_right = Table([[right_deliverables]], colWidths=[deliv_col_w])
    t_deliv_right.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#FFFFFF')),
        ('BOX', (0, 0), (-1, -1), 1, C_BORDER_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))

    t_deliv_grid = Table([[t_deliv_left, '', t_deliv_right]], colWidths=[deliv_col_w, 10, deliv_col_w])
    t_deliv_grid.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))
    story.append(t_deliv_grid)
    story.append(Spacer(1, 7))

    # 5. Terms and Next Steps
    story.append(Paragraph("Terms and Next Steps", styles['SectionHeading']))
    terms_text = (
        "&bull; The Ksh. 30,000 media budget is spent on Meta ads only and is not part of the stipend.<br/>"
        "&bull; The Ksh. 27,500 stipend covers work delivered as outlined above.<br/>"
        "&bull; Campaign start date, duration and payment schedule: [to be confirmed on approval].<br/><br/>"
        "<b>To proceed, please confirm approval of this proposal and we will begin setup immediately.</b>"
    )
    p_terms = Paragraph(terms_text, styles['CustomBody'])
    t_terms = Table([[p_terms]], colWidths=[CONTENT_WIDTH])
    t_terms.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
        ('BOX', (0, 0), (-1, -1), 1, C_BORDER_LIGHT),
        ('LINEBEFORE', (0, 0), (0, -1), 3.5, C_PRIMARY),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(t_terms)

    doc.build(story, canvasmaker=EliteWatermarkedCanvas)
    print(f"Generated Meta Proposal PDF: {OUTPUT_PDF} ({os.path.getsize(OUTPUT_PDF)} bytes)")


if __name__ == '__main__':
    build_meta_proposal()
