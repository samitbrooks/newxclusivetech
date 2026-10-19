#!/usr/bin/env python3
"""
Elite Designs Kenya — Client Pitch & Presentation Script Guide (PDF)
A high-converting, word-for-word spoken & text script guide for presenting
the official Graphic Design Portfolio & Rate Card to Kenyan businesses.
Engineered with ReportLab, Comfortaa font, and official Elite Designs branding.
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, Table, TableStyle, PageBreak, KeepTogether
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
C_PRIMARY = colors.HexColor('#3600DF')      # Electric Royal Indigo / Blue
C_PRIMARY_DARK = colors.HexColor('#22008F') # Deep Indigo
C_PRIMARY_LIGHT = colors.HexColor('#EEF2FF')# Soft Indigo Tint
C_ACCENT = colors.HexColor('#F22732')       # Vibrant Crimson Red
C_ACCENT_LIGHT = colors.HexColor('#FFF1F2') # Soft Rose Tint
C_DARK = colors.HexColor('#0F172A')         # Slate 900
C_BODY = colors.HexColor('#334155')         # Slate 700
C_MUTED = colors.HexColor('#64748B')        # Slate 500
C_BORDER = colors.HexColor('#CBD5E1')       # Slate 300
C_CARD_BG = colors.HexColor('#FFFFFF')      # White Card
C_SOFT_BG = colors.HexColor('#F8FAFC')      # Slate 50
C_SCRIPT_BG = colors.HexColor('#F1F5F9')    # Script highlight background
C_GREEN = colors.HexColor('#059669')

LOGO_PATH = 'assets/images/elitedesigns_logo.png'
OUTPUT_PDF = 'assets/documents/Elite_Designs_Presentation_Guide.pdf'
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
        self.rect(0, PAGE_HEIGHT - 7, 140, 2, fill=1, stroke=0)

        # Running header on Page 2+
        if page_num > 1:
            header_y = PAGE_HEIGHT - 26
            if os.path.exists(LOGO_PATH):
                self.drawImage(LOGO_PATH, MARGIN_LEFT, header_y - 3, width=75, height=18, preserveAspectRatio=True, mask='auto')

            self.setFont('Comfortaa-Bold', 7.5)
            self.setFillColor(C_PRIMARY)
            self.drawRightString(PAGE_WIDTH - MARGIN_RIGHT, header_y + 3, "ELITE DESIGNS • CLIENT PRESENTATION CHEAT SHEET")
            
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
        self.drawString(MARGIN_LEFT + 95, footer_y + 1, "• Word-for-Word Pitch & Objection Handling Scripts")

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
        fontSize=10,
        leading=14,
        textColor=C_MUTED,
        alignment=TA_LEFT
    ))

    styles.add(ParagraphStyle(
        'SectionHeading',
        fontName='Comfortaa-Bold',
        fontSize=12,
        leading=16,
        textColor=C_PRIMARY,
        spaceBefore=8,
        spaceAfter=4
    ))

    styles.add(ParagraphStyle(
        'ScriptBoxText',
        fontName='Comfortaa',
        fontSize=8.5,
        leading=13,
        textColor=C_DARK
    ))

    styles.add(ParagraphStyle(
        'ScriptLabel',
        fontName='Comfortaa-Bold',
        fontSize=8.5,
        leading=11,
        textColor=C_ACCENT
    ))

    styles.add(ParagraphStyle(
        'NormalBody',
        fontName='Comfortaa',
        fontSize=8.5,
        leading=12.5,
        textColor=C_BODY
    ))

    return styles


def create_script_box(label, script_text, notes, styles, accent_color=C_PRIMARY):
    """Render a high-contrast speech bubble / script card."""
    p_label = Paragraph(f"<b><font color='{accent_color.hexval()}'>{label.upper()}</font></b>", styles['ScriptLabel'])
    p_script = Paragraph(f'<i>"{script_text}"</i>', styles['ScriptBoxText'])
    
    note_p = None
    if notes:
        note_p = Paragraph(f"<font color='#64748B'><b>Pro-Tip:</b> {notes}</font>", styles['NormalBody'])

    content = [
        [p_label],
        [p_script]
    ]
    if note_p:
        content.append([Spacer(1, 2)])
        content.append([note_p])

    table = Table(content, colWidths=[CONTENT_WIDTH])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
        ('BOX', (0, 0), (-1, -1), 1, C_BORDER),
        ('LINEBEFORE', (0, 0), (0, -1), 3.5, accent_color),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ]))
    return table


def build_guide():
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
    # PAGE 1: THE OPENING, WHATSAPP DISPATCH & CORE VALUE ANCHOR
    # =========================================================================
    # Header Branding Row
    if os.path.exists(LOGO_PATH):
        story.append(RLImage(LOGO_PATH, width=160, height=40))
    story.append(Spacer(1, 8))

    story.append(Paragraph("Graphic Design Presentation &amp; Sales Pitch Guide", styles['DocTitle']))
    story.append(Paragraph("Word-for-Word Verbal &amp; WhatsApp Scripts to Confidently Present the 2026 Catalog", styles['DocSubtitle']))
    story.append(Spacer(1, 10))

    # Introductory Context Bar
    intro_html = (
        "<b>How to Use This Guide:</b> Whenever a prospect inquires about graphic design, logos, packaging, "
        "or social media branding, send the official <b>Elite Designs Portfolio PDF</b> alongside these exact scripts. "
        "These words anchor your work as an investment that drives customer acquisition rather than a cheap expense."
    )
    p_intro = Paragraph(intro_html, styles['NormalBody'])
    t_intro = Table([[p_intro]], colWidths=[CONTENT_WIDTH])
    t_intro.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#EEF2FF')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#C7D2FE')),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(t_intro)
    story.append(Spacer(1, 10))

    # SECTION 1: WHATSAPP DISPATCH SCRIPT
    story.append(Paragraph("1. The Instant WhatsApp / Email Dispatch Script", styles['SectionHeading']))
    script_wa = (
        "Hi [Client Name]! As promised, attached is the official 2026 Graphic Design Catalog and Rate Card from "
        "Elite Designs Kenya.<br/><br/>"
        "Inside, you will find our complete published pricing and deliverables across all 6 visual design pillars — "
        "from brand identity and high-impact product packaging to print collateral and social media retainers.<br/><br/>"
        "Every asset we design includes full vector source files (AI/EPS), print-ready CMYK calibration, and 100% "
        "commercial ownership so your brand looks world-class from day one.<br/><br/>"
        "Take a quick flip through pages 3 to 10. Which specific item or package are you looking to execute first?"
    )
    story.append(create_script_box(
        label="Exact WhatsApp / Email Accompanying Script",
        script_text=script_wa,
        notes="Send this immediately along with the PDF attachment. It prompts the client to name their priority item right away.",
        styles=styles,
        accent_color=C_PRIMARY
    ))
    story.append(Spacer(1, 10))

    # SECTION 2: VERBAL OPENING FOR PHONE CALLS / IN-PERSON MEETINGS
    story.append(Paragraph("2. The Verbal Pitch Hook (Phone Calls &amp; Boardroom Pitch)", styles['SectionHeading']))
    script_verbal = (
        "Here is what most business owners overlook: Good design is never just decoration; it is your direct sales leverage. "
        "In Kenya today, customers judge your credibility within 3 seconds of seeing your logo, flyer, or packaging. "
        "If it looks amateur, they immediately assume your service is low quality and haggle down your price.<br/><br/>"
        "At Elite Designs, our goal is to make your business look like the undeniable premium authority in your industry "
        "so you can command higher prices with confidence."
    )
    story.append(create_script_box(
        label="The 30-Second Authority Pitch",
        script_text=script_verbal,
        notes="Memorize this hook. It stops price negotiations before they even start by framing design as price protection.",
        styles=styles,
        accent_color=C_ACCENT
    ))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: PRESENTING THE 6 SERVICE CATEGORIES
    # =========================================================================
    story.append(Paragraph("3. Category-by-Category Presentation Scripts", styles['DocTitle']))
    story.append(Paragraph("Use these exact spoken soundbites when walking a client through specific catalog pages.", styles['DocSubtitle']))
    story.append(Spacer(1, 10))

    # Category 1: Logos
    c1_script = (
        "When we design your logo (Page 3), we don't just send a flat JPEG. You get a complete master vector suite (AI, EPS, SVG) "
        "that you can scale from a WhatsApp profile picture to a 40-foot highway billboard without losing a single pixel of sharpness. "
        "Our Logo & Stationery package at Ksh. 9,500 gives you immediate corporate legitimacy with matching letterheads and executive cards."
    )
    story.append(create_script_box(
        label="When Pitching Category 01: Brand Identity & Logos (Ksh. 6,500 – 13,500)",
        script_text=c1_script,
        notes="Emphasize vector scalability and corporate legitimacy. Remind them that amateur logos become blurry on print.",
        styles=styles,
        accent_color=C_PRIMARY
    ))
    story.append(Spacer(1, 8))

    # Category 2: Packaging
    c2_script = (
        "For your product labels and packaging (Page 4), amateur artwork causes costly printer rejects and regulatory headaches. "
        "We build your packaging to exact printer dielines with calibrated bleed margins, spot UV layers, and barcode clearances. "
        "Whether it is retail boxes or jar labels from Ksh. 3,000, your product will stand out on any supermarket shelf."
    )
    story.append(create_script_box(
        label="When Pitching Category 02: Packaging & Labels (Ksh. 1,000 – 8,000)",
        script_text=c2_script,
        notes="Crucial for FMCG, food, cosmetics, and beverage clients. Emphasize printer compliance and shelf appeal.",
        styles=styles,
        accent_color=C_ACCENT
    ))
    story.append(Spacer(1, 8))

    # Category 3: Social Media
    c3_script = (
        "Hiring a full-time in-house graphic designer in Nairobi costs between Ksh. 35,000 and 50,000 a month plus overhead. "
        "With our Monthly Social Media Management retainer at Ksh. 22,000 (Page 6), you get up to 16 agency-grade, thumb-stopping "
        "creatives designed to turn mobile scrollers into paying WhatsApp customers, saving you over 50% on payroll."
    )
    story.append(create_script_box(
        label="When Pitching Category 03: Social Media & Creatives (Ksh. 1,500 – 22,000)",
        script_text=c3_script,
        notes="Anchor against the high cost of hiring an in-house employee. Business owners love saving money on overhead.",
        styles=styles,
        accent_color=C_PRIMARY
    ))
    story.append(Spacer(1, 8))

    # Category 4 & 5: Collateral & Stationery
    c4_script = (
        "Your Company Profile (Page 7, Ksh. 6,500) is your silent 24/7 salesperson in tenders and corporate procurement. "
        "We format it specifically to pass institutional vendor reviews. Combined with our matching executive stationery (Page 9), "
        "corporate clients will never question whether your firm is established."
    )
    story.append(create_script_box(
        label="When Pitching Categories 04 & 05: Collateral & Corporate Stationery",
        script_text=c4_script,
        notes="Use this for B2B service firms, consultants, contractors, NGOs, and medical clinics.",
        styles=styles,
        accent_color=C_ACCENT
    ))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: OBJECTION HANDLING & CLOSING SCRIPTS
    # =========================================================================
    story.append(Paragraph("4. Objection Handling &amp; Closing Frameworks", styles['DocTitle']))
    story.append(Paragraph("Word-for-word scripts to turn hesitation into paid deposits.", styles['DocSubtitle']))
    story.append(Spacer(1, 10))

    # Objection 1: "Can you do it cheaper / Give me a discount?"
    obj1_script = (
        "I completely respect your budget! Our rates are strictly calibrated to deliver senior-level, award-winning "
        "craftsmanship and full vector source ownership. If Ksh. [X] is slightly above your initial allocation today, "
        "we can start with [Alternative Item, e.g. express logo or single flyer at Ksh. 1,500] to get your campaign live, "
        "and upgrade as your revenue rolls in. Fair enough?"
    )
    story.append(create_script_box(
        label="Objection 1: 'Can you give me a discount?'",
        script_text=obj1_script,
        notes="Never drop your price without reducing scope. Offer an entry-level package instead to maintain your high-end positioning.",
        styles=styles,
        accent_color=C_ACCENT
    ))
    story.append(Spacer(1, 8))

    # Objection 2: "Someone on Facebook/Canva can do it for 500 bob"
    obj2_script = (
        "You certainly can find low-cost templates on Canva or Facebook, but here is what happens when you try to print "
        "them: the colors print muddy, the text is blurry, and you don't own the master vector rights. "
        "When you work with Elite Designs, you are getting print-calibrated, trademarkable artwork from the winners of "
        "the Digitally Fit Awards. That peace of mind protects your brand reputation permanently."
    )
    story.append(create_script_box(
        label="Objection 2: 'Why shouldn't I just use Canva or an amateur?'",
        script_text=obj2_script,
        notes="Remind them that cheap design costs 10x more when you have to throw away 5,000 badly printed flyers.",
        styles=styles,
        accent_color=C_PRIMARY
    ))
    story.append(Spacer(1, 8))

    # Objection 3: "What if I don't like the design?"
    obj3_script = (
        "That is exactly why we offer our Ironclad Risk Reversal: You only put down a 50% deposit to initiate the sprint. "
        "We present 3 unique creative concepts and refine your favorite option through up to 3 revision rounds. "
        "You clear the remaining 50% balance ONLY after you are 100% delighted with the final result."
    )
    story.append(create_script_box(
        label="Objection 3: 'What if I don't like the design?'",
        script_text=obj3_script,
        notes="The 50% live inspection guarantee completely removes fear and secures instant buy-in.",
        styles=styles,
        accent_color=C_ACCENT
    ))
    story.append(Spacer(1, 8))

    # THE CLOSING CALL TO ACTION SCRIPT
    close_script = (
        "To get your design sprint scheduled for this week, we just need your brand brief and the 50% initiation deposit. "
        "You will receive your first set of 3D concept mockups within 48 to 72 hours. Shall I send over the M-Pesa details so we begin?"
    )
    story.append(create_script_box(
        label="The 1-Click Closing Script (Closing the Deal)",
        script_text=close_script,
        notes="Direct, confident, and professional. Always assume the close and ask for the initiation deposit.",
        styles=styles,
        accent_color=C_PRIMARY
    ))

    # Build PDF
    doc.build(story, canvasmaker=EliteNumberedCanvas)
    print(f"Generated Presentation Guide successfully: {OUTPUT_PDF} ({os.path.getsize(OUTPUT_PDF)} bytes)")


if __name__ == '__main__':
    build_guide()
