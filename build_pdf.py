from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, HRFlowable
)
from reportlab.graphics.shapes import Drawing, Rect, String
from reportlab.graphics import renderPDF

# Colors
RED = HexColor("#C8102E")
RED_DARK = HexColor("#8f0b20")
YELLOW = HexColor("#FFB81C")
GREEN = HexColor("#2e7d4f")
GRAY = HexColor("#5f5f5f")
LIGHT_BG = HexColor("#f7f5f2")
CARD_BG = HexColor("#ffffff")
BORDER = HexColor("#e7e2da")
LIGHT_YELLOW = HexColor("#fbf5e8")
LIGHT_GREEN = HexColor("#eef7f1")

W, H = A4

styles = getSampleStyleSheet()

# Custom styles
title_style = ParagraphStyle('CustomTitle', parent=styles['Title'],
    fontSize=20, textColor=white, alignment=TA_CENTER, spaceAfter=4, fontName='Helvetica-Bold')
subtitle_style = ParagraphStyle('Subtitle', parent=styles['Normal'],
    fontSize=10, textColor=white, alignment=TA_CENTER, spaceAfter=2)
badge_style = ParagraphStyle('Badge', parent=styles['Normal'],
    fontSize=8, textColor=HexColor("#dddddd"), alignment=TA_CENTER, spaceAfter=6)

section_head = ParagraphStyle('SectionHead', parent=styles['Heading2'],
    fontSize=14, textColor=RED_DARK, fontName='Helvetica-Bold', spaceBefore=16, spaceAfter=6,
    borderPadding=(0,0,2,0))
body_style = ParagraphStyle('Body', parent=styles['Normal'],
    fontSize=9.5, leading=14, textColor=HexColor("#221f1f"), spaceAfter=6)
small_style = ParagraphStyle('Small', parent=styles['Normal'],
    fontSize=8.5, leading=12, textColor=GRAY, spaceAfter=4)
quote_style = ParagraphStyle('Quote', parent=styles['Normal'],
    fontSize=8.5, leading=12, textColor=GRAY, fontName='Helvetica-Oblique',
    leftIndent=12, borderPadding=(0,0,0,8), spaceAfter=4)
solution_style = ParagraphStyle('Solution', parent=styles['Normal'],
    fontSize=9, leading=13, textColor=HexColor("#221f1f"), spaceAfter=6,
    backColor=LIGHT_GREEN, borderPadding=(6,8,6,8))
kpi_val = ParagraphStyle('KPIVal', parent=styles['Normal'],
    fontSize=18, fontName='Helvetica-Bold', textColor=RED, alignment=TA_CENTER)
kpi_lab = ParagraphStyle('KPILab', parent=styles['Normal'],
    fontSize=7.5, textColor=GRAY, alignment=TA_CENTER, leading=10)
note_style = ParagraphStyle('Note', parent=styles['Normal'],
    fontSize=8, leading=11, textColor=GRAY, backColor=LIGHT_YELLOW,
    borderPadding=(6,8,6,8), spaceAfter=6)
closing_style = ParagraphStyle('Closing', parent=styles['Normal'],
    fontSize=9.5, leading=14, textColor=HexColor("#221f1f"), spaceAfter=8)
sig_style = ParagraphStyle('Sig', parent=styles['Normal'],
    fontSize=9, textColor=GRAY, spaceAfter=2)


def build_bar_chart(data, max_val, bar_color=RED, label_width=90, chart_width=380):
    """Build a simple horizontal bar chart as a Table."""
    rows = []
    for item in data:
        label = item[0]
        val = item[1]
        pct = val / max_val if max_val > 0 else 0
        bar_w = max(2, int(pct * 200))

        d = Drawing(210, 14)
        d.add(Rect(0, 2, 200, 10, fillColor=HexColor("#efeae2"), strokeColor=None))
        d.add(Rect(0, 2, bar_w, 10, fillColor=bar_color, strokeColor=None))

        label_p = Paragraph(str(label), ParagraphStyle('bl', fontSize=8.5, textColor=GRAY))
        val_p = Paragraph(str(val), ParagraphStyle('bv', fontSize=8.5, textColor=HexColor("#221f1f")))

        rows.append([label_p, d, val_p])

    t = Table(rows, colWidths=[label_width, 215, 40])
    t.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 2),
        ('RIGHTPADDING', (0,0), (-1,-1), 2),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    return t


def header_footer(canvas, doc):
    """Draw the red header band on the first page only."""
    if doc.page == 1:
        canvas.saveState()
        canvas.setFillColor(RED)
        canvas.rect(0, H - 95*mm, W, 95*mm, fill=True, stroke=False)
        # Gradient overlay
        canvas.setFillColor(RED_DARK)
        canvas.rect(0, H - 95*mm, W, 30*mm, fill=True, stroke=False)
        canvas.restoreState()

    # Footer on every page
    canvas.saveState()
    canvas.setFont('Helvetica', 7)
    canvas.setFillColor(GRAY)
    canvas.drawCentredString(W/2, 15*mm,
        f"Marrybrown Swanston St — Customer Experience Brief  |  Page {doc.page}")
    canvas.restoreState()


def build():
    doc = SimpleDocTemplate(
        "/sessions/admiring-amazing-volta/mnt/outputs/marrybrown_review_insights.pdf",
        pagesize=A4,
        topMargin=100*mm,  # first page has header
        bottomMargin=25*mm,
        leftMargin=20*mm,
        rightMargin=20*mm,
    )

    story = []

    # ── HEADER CONTENT (sits inside the top margin area via Spacer trick) ──
    # We'll use the first-page template for the red band, and put title as flowables
    # Actually, let's reduce topMargin and add spacers

    # Title block
    story.append(Spacer(1, -55*mm))
    story.append(Paragraph("Marrybrown Swanston St", title_style))
    story.append(Paragraph("Customer Experience Brief", ParagraphStyle('s2',
        fontSize=13, textColor=white, alignment=TA_CENTER, spaceAfter=4, fontName='Helvetica')))
    story.append(Paragraph("1/339 Swanston St, Melbourne VIC 3000 (Melbourne Central precinct)", subtitle_style))
    story.append(Paragraph("Prepared by Luthfil Lawliet  ·  Google Maps review data, Jul 2026", badge_style))
    story.append(Spacer(1, 10))

    # ── ABOUT ME / INTRO ──
    story.append(Paragraph("<b>About me</b>", ParagraphStyle('intro_tag',
        fontSize=8, textColor=RED, fontName='Helvetica-Bold', spaceAfter=4)))
    story.append(Paragraph(
        "I'm Luthfil Lawliet — an international student based in Melbourne for the past six months, "
        "currently studying and actively looking to join a team where I can contribute from day one. "
        "I'm a hands-on problem solver who likes digging into data and turning it into something actionable, "
        "and I genuinely enjoy customer-facing work.",
        body_style))
    story.append(Paragraph(
        "Before applying to Marrybrown, I wanted to actually understand the store from a customer's perspective "
        "— not just the menu, but what people are saying after they visit. So I pulled the public Google reviews "
        "and turned them into the brief below: what's already working, where there's room to grow, and a few "
        "ideas I'd bring if I joined.",
        body_style))
    story.append(Spacer(1, 6))

    # ── KPIs ──
    kpi_data = [
        ("2.7★", "Overall rating"),
        ("125", "Total reviews"),
        ("27%", "Rate it 5 stars"),
        ("43%", "Growth opportunity\n(1-star visits)"),
    ]
    kpi_cells = []
    for val, lab in kpi_data:
        kpi_cells.append([
            Paragraph(val, kpi_val),
            Paragraph(lab, kpi_lab)
        ])

    # Transpose to 1 row of 4 columns
    kpi_row_vals = [c[0] for c in kpi_cells]
    kpi_row_labs = [c[1] for c in kpi_cells]
    kpi_table = Table([kpi_row_vals, kpi_row_labs], colWidths=[W/4 - 15*mm]*4)
    kpi_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('BOX', (0,0), (0,-1), 0.5, BORDER),
        ('BOX', (1,0), (1,-1), 0.5, BORDER),
        ('BOX', (2,0), (2,-1), 0.5, BORDER),
        ('BOX', (3,0), (3,-1), 0.5, BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('BACKGROUND', (0,0), (-1,-1), CARD_BG),
        ('ROUNDEDCORNERS', [4,4,4,4]),
    ]))
    story.append(kpi_table)
    story.append(Spacer(1, 10))

    # ── 1. RATING DISTRIBUTION ──
    story.append(Paragraph("1. Rating Distribution", section_head))
    story.append(Paragraph("Out of all 125 Google reviews for this location.", small_style))

    rating_data = [
        ("★★★★★", 34), ("★★★★☆", 16), ("★★★☆☆", 11),
        ("★★☆☆☆", 10), ("★☆☆☆☆", 54)
    ]
    max_r = 54
    chart_rows = []
    for label, count in rating_data:
        pct = round(count/125*100)
        chart_rows.append((label, count))

    story.append(build_bar_chart(
        [(f"{label}  ", count) for label, count in rating_data],
        max_r, bar_color=YELLOW
    ))
    story.append(Spacer(1, 8))

    # ── 2. TOP 10 WORDS ──
    story.append(Paragraph("2. Top 10 Most-Mentioned Words & Topics", section_head))
    story.append(Paragraph(
        "Based on Google's extracted review topics (aggregated across all 125 reviews) plus manual "
        "review-text analysis.", small_style))

    words = [
        ("friendly staff", 18), ("spicy food", 8), ("fried chicken", 7),
        ("missing (items)", 6), ("nasi lemak", 5), ("welcoming atmosphere", 5),
        ("chicken burger", 5), ("halal food", 4), ("cold (food)", 4), ("crispy chicken", 3)
    ]
    story.append(build_bar_chart(words, 18, bar_color=GREEN, label_width=110))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "Note: Full scrape of all 125 review texts was interrupted by a Google Maps rendering issue. "
        "This chart blends Google's own topic-tag counts (covering the full set) with word-frequency "
        "from a 10-review text sample. Treat exact counts as directional.", note_style))

    # ── 3. TOP 3 OPPORTUNITIES ──
    story.append(Paragraph("3. Top 3 Opportunities to Lift the Rating", section_head))
    story.append(Paragraph(
        "The themes that show up most often in lower-rated visits — and the ones that would move "
        "the needle fastest if addressed.", small_style))

    problems = [
        {
            "title": "Freshness & consistency",
            "desc": "A handful of reviews flag food arriving cold or not tasting right. This is usually "
                    "the fastest lever to pull — small process fixes tend to show up in ratings within weeks.",
            "quotes": [
                ("Ordered mashed potatoes takeaway — they'd gone off and had to be thrown away.", "BB Kd, 1★"),
                ("The food has way too much baking soda, leaving a strange aftertaste.", "Prathamesh Gaikwad, 1★"),
            ]
        },
        {
            "title": "Order accuracy & portions",
            "desc": "The most repeated theme in the lower-rated reviews: items missing from an order, or a "
                    "portion feeling smaller than expected. Very fixable with a simple check-before-handoff habit.",
            "quotes": [
                ("I ordered two large fries, but the portion was tiny — nothing close to 'large.'", "Jimmy Low, 1★"),
                ("I ordered the Nasi Kandar and it came without the curry sauce — not the first time.", "YiXuan Ong, 1★"),
            ]
        },
        {
            "title": "Service consistency",
            "desc": "Experience varies noticeably visit to visit. Standardizing the good moments could turn "
                    "more first-timers into regulars.",
            "quotes": [
                ("Asked them to cut the burger in half — the Melbourne Central branch always does it.", "Aiman Rashid, 1★"),
                ("Friendly, welcoming service comes up a lot in the positive reviews too — it's clearly there, just not every time.", "Based on 18 mentions"),
            ]
        },
    ]

    for i, p in enumerate(problems):
        story.append(Paragraph(f"<b>{i+1}. {p['title']}</b>", ParagraphStyle('pt',
            fontSize=10, fontName='Helvetica-Bold', textColor=RED_DARK, spaceBefore=8, spaceAfter=4)))
        story.append(Paragraph(p['desc'], body_style))
        for q_text, q_who in p['quotes']:
            story.append(Paragraph(f'"{q_text}" <font size="7" color="#a0a0a0">— {q_who}</font>', quote_style))

    # ── 4. WHERE I'D START ──
    story.append(Paragraph("4. Where I'd Start", section_head))
    story.append(Paragraph("Concrete, low-cost ideas tied to each opportunity above.", small_style))

    solutions = [
        ("Freshness & consistency", "A simple hot-holding temperature log for sides/gravy, plus a quick taste-check on batter seasoning at shift start, catches most of this before it reaches a customer."),
        ("Order accuracy & portions", "A 5-second visual check against the receipt before handoff, and standardized scoop sizes across shifts, would resolve the majority of these complaints at near-zero cost."),
        ("Service consistency", "Since friendly service already shows up often in the positive reviews, this is more about consistency than training from scratch — quick shift-start reminders and clear guidance on handling simple customer requests would go a long way."),
    ]
    for i, (title, desc) in enumerate(solutions):
        story.append(Paragraph(f"<b>{i+1}. {title}:</b> {desc}", solution_style))

    # ── 5. MARKET PENETRATION ──
    story.append(PageBreak())
    story.append(Paragraph("5. Untapped Market: Muslim Newcomers in Melbourne", section_head))
    story.append(Paragraph(
        "A market-penetration observation from someone who's lived it firsthand.", small_style))

    story.append(Paragraph(
        "Here's something I noticed as a newcomer myself: <b>I only discovered Marrybrown by accident.</b> "
        "After nearly six months living in Melbourne, I stumbled across the Swanston St store while passing "
        "through — I had no idea it was here, and more importantly, no idea it was halal. That's a missed "
        "connection, because finding reliable halal food is one of the first things international Muslim "
        "students and families do when they arrive.", body_style))

    story.append(Paragraph(
        "The way most newcomers find halal restaurants is through <b>community WhatsApp groups</b> — curated "
        "lists of halal spots circulated among new arrivals. I used one myself. Marrybrown wasn't on it. "
        "Meanwhile, competitors like <b>Nene Chicken</b> were mentioned repeatedly and had visible presence "
        "at community events.", body_style))

    story.append(Paragraph(
        "I've also attended several <b>iftar events</b> at university campuses and mosques/mushallahs around "
        "Melbourne. These gatherings draw hundreds of Muslim students and families — exactly the demographic "
        "Marrybrown serves. Yet every event I attended featured other brands. Marrybrown was nowhere to be seen.", body_style))

    story.append(Paragraph(
        "This represents a significant <b>low-cost, high-return market penetration opportunity</b>:", body_style))

    market_solutions = [
        ("Community list seeding", "Get Marrybrown onto the halal-food WhatsApp lists that circulate among new international students. A few outreach messages to Islamic student associations (ISOC) at Melbourne's major universities (UniMelb, RMIT, Monash City) could do this organically."),
        ("Campus & mosque event sponsorship", "Sponsor or cater iftar events, orientation-week food stalls, or Friday-prayer community lunches. These are high-trust environments where a single positive experience turns into word-of-mouth across an entire cohort of new arrivals."),
        ("Visible halal branding", "Make the halal certification more prominent in storefront signage and on Google Maps listing photos. Many Muslim customers specifically search 'halal' on Maps — Marrybrown should rank for it immediately."),
        ("Newcomer welcome offer", "A simple 'New to Melbourne?' discount card distributed at airport welcome desks, university orientation packs, or mosque noticeboards could drive first visits from people who would otherwise default to the brands they already know."),
    ]
    for i, (title, desc) in enumerate(market_solutions):
        story.append(Paragraph(f"<b>{i+1}. {title}:</b> {desc}", solution_style))

    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "Melbourne receives thousands of new Muslim international students every semester. Most are actively "
        "searching for halal dining options in their first weeks. Right now, Marrybrown is invisible to them. "
        "Fixing that is mostly a distribution and awareness problem — the product (affordable halal fried "
        "chicken in the CBD) already fits the demand perfectly.", small_style))

    # ── 6. SAMPLE REVIEWS ──
    story.append(Paragraph("6. Sample Reviews", section_head))
    story.append(Paragraph(
        "A balanced mix of praise and criticism from public Google reviews.", small_style))

    reviews = [
        ("Rocke", 5, "a year ago", "Best chicken burger for the price I've had. It's definitely better than a Zinger, actually spicy and bigger, too. That mayo they use is also amazing. The fried chicken is always cooked perfectly with a crispy coating."),
        ("Shai N", 4, "10 months ago", "It's located close to Melbourne Central. I enjoyed the Nasi Lemak because it was so spicy and service was fast."),
        ("Ashlee Jayde", 3, "3 months ago", "I visited Marrybrown for the first time in March 2026 on a Sunday evening for dinner with some friends. It's in a super central spot, with the State Library nearby."),
        ("kitty xin", 3, "3 months ago", "It was off peak time and I was waiting for 10 minutes for my simple side dishes. The gravy was almost cold and chips was smaller than before."),
        ("BB Kd", 1, "5 months ago", "Ordered mashed potatoes takeaway — all three were spoiled, with a rotten smell and sour taste. Completely inedible. Had to throw everything away."),
        ("Aiman Rashid", 1, "6 months ago", "Really bad experience — I asked them to cut the burger in half and the staff member was so rude. The Melbourne Central branch always does it when asked."),
        ("Jimmy Low", 1, "9 months ago", "I ordered two large fries, but the portion was tiny — nothing close to 'large.' The fries were cold and not fresh at all."),
        ("YiXuan Ong", 1, "9 months ago", "I've had repeated issues with missing items from my orders. Most recently, I ordered the Nasi Kandar and it came without the curry sauce."),
    ]

    for author, rating, time, text in reviews:
        stars = "★" * rating + "☆" * (5 - rating)
        story.append(Paragraph(
            f'<b>{author}</b>  <font color="#FFB81C">{stars}</font>  '
            f'<font size="7" color="#999">{time}</font>',
            ParagraphStyle('rh', fontSize=9, spaceAfter=2)))
        story.append(Paragraph(text, ParagraphStyle('rt', fontSize=8.5, leading=12,
            textColor=HexColor("#333"), spaceAfter=10)))

    # ── 7. WHY I'M APPLYING ──
    story.append(Spacer(1, 6))
    story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER, spaceAfter=10))
    story.append(Paragraph("7. Why I'm Applying", section_head))
    story.append(Paragraph(
        "I like that this role is equal parts people and process — and I think the biggest opportunities "
        "above (order accuracy, consistency, service) are all things a motivated team member can genuinely "
        "influence day to day, not just at the corporate level. I put this brief together the way I'd want "
        "to approach the job itself: look closely at what's actually happening, be honest about the gaps, "
        "and come with ideas rather than just observations.", closing_style))
    story.append(Paragraph(
        "I'd love the chance to talk more about the role and bring this kind of attention to the "
        "Swanston St team.", closing_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Luthfil Lawliet", sig_style))
    story.append(Paragraph("luthfillawliet23@gmail.com", sig_style))

    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER, spaceAfter=6))
    story.append(Paragraph(
        "This is a personal work sample built from publicly available Google reviews — not an official "
        "Marrybrown document.", ParagraphStyle('disc', fontSize=7, textColor=GRAY, alignment=TA_CENTER)))

    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print("PDF built successfully!")

build()
