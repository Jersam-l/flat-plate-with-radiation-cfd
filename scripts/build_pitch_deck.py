#!/usr/bin/env python3
"""
build_pitch_deck.py
Generates the 14-slide pitch deck Flat_Plate_Radiation_CFD_Pitch.pptx
Adheres strictly to the Pitch_Template.pptx design system, fonts, colors, and human layout rules.
Authored for:
  Presenter: Jersam Lithin
  Program: 3rd Year B.Tech Aerospace Engineering
  Institution: Karunya Institute of Technology and Sciences
  Subject: Boundary Layer Theory
"""

import os
import sys
from PIL import Image
import pptx
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor

# Design Tokens (Thermal Navy theme from Pitch_Template.pptx)
COLOR_NAVY_DARK = RGBColor(0x0B, 0x14, 0x26)       # dk1
COLOR_NAVY_CARD = RGBColor(0x16, 0x26, 0x4A)       # dk2 / dark chips
COLOR_LIGHT_BG = RGBColor(0xEE, 0xF2, 0xF7)        # lt2 / light slide bg
COLOR_WHITE = RGBColor(0xFF, 0xFF, 0xFF)           # lt1 / white cards
COLOR_ORANGE = RGBColor(0xFF, 0x7A, 0x1A)          # accent1 (primary hot accent)
COLOR_CYAN = RGBColor(0x23, 0xB5, 0xD3)            # accent2 (flow / thermal)
COLOR_AMBER = RGBColor(0xFF, 0xC2, 0x4B)           # accent3
COLOR_SLATE = RGBColor(0x7C, 0x8D, 0xB5)           # accent4 (muted labels / kicker)
COLOR_RED = RGBColor(0xE5, 0x48, 0x4D)             # accent5 (warnings only)
COLOR_BORDER = RGBColor(0xDC, 0xE2, 0xEC)          # subtle card stroke

FONT_TITLE = 'Cambria'
FONT_BODY = 'Calibri'

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
FIG_DIR = os.path.join(REPO_ROOT, 'results', 'figures')
TEMPLATE_PATH = os.path.join(REPO_ROOT, 'Pitch_Template.pptx')
OUTPUT_PPTX = os.path.join(REPO_ROOT, 'Flat_Plate_Radiation_CFD_Pitch.pptx')


def create_deck():
    print(f"Loading template from {TEMPLATE_PATH}...")
    prs = pptx.Presentation(TEMPLATE_PATH)
    
    # Verify slide dimensions (16:9 widescreen: 13.333 x 7.5 in)
    prs.slide_width = Inches(13.333333)
    prs.slide_height = Inches(7.5)
    
    # Update running footer text on all slide layouts directly
    for layout in prs.slide_layouts:
        for shape in layout.shapes:
            if shape.has_text_frame and 'Flat-Plate' in shape.text_frame.text:
                shape.text_frame.text = "Boundary Layer Theory  |  Karunya Institute of Technology and Sciences"
                p = shape.text_frame.paragraphs[0]
                p.font.name = FONT_BODY
                p.font.size = Pt(11)
                p.font.color.rgb = COLOR_SLATE

    # Clear template dummy slides
    for i in range(len(prs.slides) - 1, -1, -1):
        rId = prs.slides._sldIdLst[i].rId
        prs.part.drop_rel(rId)
        del prs.slides._sldIdLst[i]
        
    print("Template cleared. Building 14 human-engineered slides...")
    
    # Helper to set slide background
    def set_bg(slide, color):
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = color

    # Helper to add standard slide title
    def add_title(slide, title_text, dark=False):
        tx_box = slide.shapes.add_textbox(Inches(0.6), Inches(0.4), Inches(12.133), Inches(0.95))
        tf = tx_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.name = FONT_TITLE
        p.font.size = Pt(32)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE if dark else COLOR_NAVY_DARK
        return tx_box

    # Helper to add slide number on right (running footer text is managed cleanly on the layout)
    def add_footer(slide, num, dark=False):
        num_box = slide.shapes.add_textbox(Inches(12.1), Inches(7.0), Inches(0.6), Inches(0.3))
        tf_n = num_box.text_frame
        tf_n.margin_left = tf_n.margin_top = tf_n.margin_right = tf_n.margin_bottom = 0
        p_n = tf_n.paragraphs[0]
        p_n.alignment = PP_ALIGN.RIGHT
        p_n.text = str(num)
        p_n.font.name = FONT_BODY
        p_n.font.size = Pt(11)
        p_n.font.color.rgb = COLOR_SLATE

    # Helper to add rounded card
    def add_card(slide, left, top, width, height, bg_color=COLOR_WHITE, border_color=COLOR_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        if border_color:
            card.line.color.rgb = border_color
            card.line.width = Pt(1)
        else:
            card.line.fill.background()
        return card

    # Helper to add image inside a card with caption, strictly preserving aspect ratio (contain)
    def add_contained_image(slide, card_left, card_top, card_w, card_h, img_filename, caption_text, dark_card=False):
        bg_col = COLOR_NAVY_CARD if dark_card else COLOR_WHITE
        border_col = None if dark_card else COLOR_BORDER
        add_card(slide, card_left, card_top, card_w, card_h, bg_color=bg_col, border_color=border_col)
        
        img_path = os.path.join(FIG_DIR, img_filename)
        if not os.path.exists(img_path):
            raise FileNotFoundError(f"Missing required figure: {img_path}")
            
        with Image.open(img_path) as img:
            im_w, im_h = img.size
            ar = im_w / im_h

        pad_x = Inches(0.2)
        pad_top = Inches(0.18)
        caption_h = Inches(0.35)
        avail_w = card_w - (2 * pad_x)
        avail_h = card_h - pad_top - caption_h - Inches(0.18)

        avail_ar = avail_w / avail_h
        if avail_ar > ar:
            # height constrained
            fit_h = avail_h
            fit_w = fit_h * ar
            fit_top = card_top + pad_top
            fit_left = card_left + pad_x + (avail_w - fit_w) / 2
        else:
            # width constrained
            fit_w = avail_w
            fit_h = fit_w / ar
            fit_left = card_left + pad_x
            fit_top = card_top + pad_top + (avail_h - fit_h) / 2

        slide.shapes.add_picture(img_path, fit_left, fit_top, fit_w, fit_h)

        # Caption inside the card with comfortable padding
        cap_box = slide.shapes.add_textbox(card_left + pad_x, card_top + card_h - caption_h - Inches(0.12), card_w - (2 * pad_x), caption_h)
        tf = cap_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = caption_text
        p.font.name = FONT_BODY
        p.font.size = Pt(11)
        p.font.color.rgb = COLOR_SLATE

    # Helper to add speaker notes
    def add_notes(slide, notes_text):
        notes_slide = slide.notes_slide
        tf = notes_slide.notes_text_frame
        tf.text = notes_text

    # Helper to add standard bullets (max 3 bullets, max 12 words)
    def add_bullet_list(tf, bullets, dark=False, font_size=15):
        assert len(bullets) <= 3, f"Too many bullets ({len(bullets)} > 3)"
        for i, text in enumerate(bullets):
            words = text.strip().split()
            assert len(words) <= 12, f"Bullet exceeds 12 words ({len(words)} words): '{text}'"
            if i == 0 and len(tf.paragraphs) == 1 and not tf.paragraphs[0].text:
                p = tf.paragraphs[0]
            else:
                p = tf.add_paragraph()
            p.text = f"•  {text}"
            p.font.name = FONT_BODY
            p.font.size = Pt(font_size)
            p.font.color.rgb = COLOR_WHITE if dark else COLOR_NAVY_DARK
            p.space_after = Pt(12)

    # -------------------------------------------------------------
    # SLIDE 1: Title (Dark)
    # Authored by Jersam Lithin, Karunya Inst of Tech, Aerospace 3rd Yr, Boundary Layer Theory
    # Hero image placed directly on the dark canvas matching template slide 1!
    # -------------------------------------------------------------
    s1 = prs.slides.add_slide(prs.slide_layouts[1]) # DARK_TITLE
    set_bg(s1, COLOR_NAVY_DARK)
    
    # Academic Kicker
    kicker_box = s1.shapes.add_textbox(Inches(0.8), Inches(0.9), Inches(6.8), Inches(0.4))
    tf_k = kicker_box.text_frame
    tf_k.margin_left = tf_k.margin_top = tf_k.margin_right = tf_k.margin_bottom = 0
    p = tf_k.paragraphs[0]
    p.text = "DEPARTMENT OF AEROSPACE ENGINEERING  |  BOUNDARY LAYER THEORY"
    p.font.name = FONT_BODY
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN

    # Title (Cambria 36 pt bold)
    t_box = s1.shapes.add_textbox(Inches(0.8), Inches(1.45), Inches(6.8), Inches(2.3))
    tf_t = t_box.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0
    p = tf_t.paragraphs[0]
    p.text = "Surface Radiation Cuts Flat-Plate Wall Temperature by 6.98 K"
    p.font.name = FONT_TITLE
    p.font.size = Pt(35)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE

    # Subtitle
    sub_box = s1.shapes.add_textbox(Inches(0.8), Inches(3.9), Inches(6.8), Inches(0.9))
    tf_sub = sub_box.text_frame
    tf_sub.word_wrap = True
    tf_sub.margin_left = tf_sub.margin_top = tf_sub.margin_right = tf_sub.margin_bottom = 0
    p = tf_sub.paragraphs[0]
    p.text = "Coupled Convection-Radiation CFD in OpenFOAM 13, Validated Against Blasius Similarity"
    p.font.name = FONT_BODY
    p.font.size = Pt(16)
    p.font.color.rgb = COLOR_LIGHT_BG

    # Presenter & Academic Affiliation Box (Human Student Author block)
    pres_box = s1.shapes.add_textbox(Inches(0.8), Inches(5.1), Inches(6.8), Inches(1.8))
    tf_p = pres_box.text_frame
    tf_p.word_wrap = True
    tf_p.margin_left = tf_p.margin_top = tf_p.margin_right = tf_p.margin_bottom = 0
    
    p = tf_p.paragraphs[0]
    p.text = "Jersam Lithin"
    p.font.name = FONT_TITLE
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = COLOR_ORANGE
    p.space_after = Pt(4)

    p2 = tf_p.add_paragraph()
    p2.text = "3rd Year B.Tech, Aerospace Engineering"
    p2.font.name = FONT_BODY
    p2.font.size = Pt(13)
    p2.font.color.rgb = COLOR_WHITE
    p2.space_after = Pt(2)

    p3 = tf_p.add_paragraph()
    p3.text = "Karunya Institute of Technology and Sciences"
    p3.font.name = FONT_BODY
    p3.font.size = Pt(13)
    p3.font.color.rgb = COLOR_LIGHT_BG
    p3.space_after = Pt(2)

    p4 = tf_p.add_paragraph()
    p4.text = "Course: Boundary Layer Theory  |  Academic Year 2026"
    p4.font.name = FONT_BODY
    p4.font.size = Pt(12)
    p4.font.color.rgb = COLOR_SLATE

    # Hero figure on right: Placed DIRECTLY on the dark background without tacky white card!
    # (Matches Pitch_Template.pptx slide 1!)
    hero_path = os.path.join(FIG_DIR, 'four_case_temperature_zoom.png')
    hero_left = Inches(7.8)
    hero_top = Inches(1.2)
    hero_w = Inches(4.9)
    hero_h = Inches(5.2)
    with Image.open(hero_path) as img:
        im_w, im_h = img.size
        ar = im_w / im_h
    avail_h = hero_h - Inches(0.5)
    fit_w = hero_w
    fit_h = fit_w / ar
    if fit_h > avail_h:
        fit_h = avail_h
        fit_w = fit_h * ar
    fit_top = hero_top + (avail_h - fit_h) / 2
    fit_left = hero_left + (hero_w - fit_w) / 2
    s1.shapes.add_picture(hero_path, fit_left, fit_top, fit_w, fit_h)

    # Caption directly below picture
    cap_hero = s1.shapes.add_textbox(hero_left, fit_top + fit_h + Inches(0.1), hero_w, Inches(0.4))
    tf_ch = cap_hero.text_frame
    tf_ch.word_wrap = True
    tf_ch.margin_left = tf_ch.margin_top = 0
    p = tf_ch.paragraphs[0]
    p.text = "Fig. 1: Near-wall boundary layer temperature contours across test matrix."
    p.font.name = FONT_BODY
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_SLATE

    add_notes(s1,
              "This presentation presents my CFD research project for Boundary Layer Theory at Karunya Institute of Technology and Sciences. I investigate coupled surface radiation effects on a laminar flat-plate boundary layer using OpenFOAM 13. By coupling grey-diffuse thermal radiation to an external 300 K environment using an in-situ Newton-Raphson wall boundary solver, we show that radiation depresses wall temperatures by 6.98 K. The hydrodynamic boundary layer validates against Blasius similarity within 0.11%. Source: results/figures/four_case_temperature_zoom.png.")

    # -------------------------------------------------------------
    # SLIDE 2: Problem Statement (Light)
    # Figure left in clean card, right-hand title and bullets float naturally on #EEF2F7 (no outer box!)
    # -------------------------------------------------------------
    s2 = prs.slides.add_slide(prs.slide_layouts[2])
    set_bg(s2, COLOR_LIGHT_BG)
    add_title(s2, "Neglecting Surface Radiation Overpredicts Heated Wall Temperatures")
    add_footer(s2, 2)
    
    # Left: wall temperature plot in card
    add_contained_image(s2, Inches(0.6), Inches(1.5), Inches(7.2), Inches(5.2),
                        'wall_temperature_all_cases.png',
                        'Fig. 2: Streamwise wall temperature distribution along heated flat plate.')
    
    # Right: Human slide layout - text floats on #EEF2F7 canvas (NO outer white card!)
    right_box = s2.shapes.add_textbox(Inches(8.2), Inches(1.6), Inches(4.5), Inches(5.1))
    tf_r2 = right_box.text_frame
    tf_r2.word_wrap = True
    tf_r2.margin_left = tf_r2.margin_top = tf_r2.margin_right = tf_r2.margin_bottom = 0
    
    p = tf_r2.paragraphs[0]
    p.text = "Convective Cooling Decays Downstream"
    p.font.name = FONT_TITLE
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY_DARK
    p.space_after = Pt(18)
    
    add_bullet_list(tf_r2, [
        "Plate wall temperature depends strictly on competing heat rejection pathways.",
        "Convective cooling drops downstream as hydrodynamic boundary layers thicken.",
        "Standard CFD workflows frequently omit radiation, overpredicting component peak temperatures."
    ], font_size=15)
    
    # Highlight stat chip floating cleanly
    add_card(s2, Inches(8.2), Inches(5.2), Inches(4.5), Inches(1.2), bg_color=COLOR_WHITE, border_color=COLOR_BORDER)
    hc2 = s2.shapes.add_textbox(Inches(8.4), Inches(5.3), Inches(4.1), Inches(1.0))
    tf_hc2 = hc2.text_frame
    tf_hc2.word_wrap = True
    tf_hc2.margin_left = tf_hc2.margin_top = 0
    p = tf_hc2.paragraphs[0]
    p.text = "Heater Heat Flux: q″ = 1000 W/m²"
    p.font.name = FONT_TITLE
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_ORANGE
    p2 = tf_hc2.add_paragraph()
    p2.text = "Uniform electric heating applied over 1.0 m plate with T_ambient = 300 K"
    p2.font.name = FONT_BODY
    p2.font.size = Pt(11)
    p2.font.color.rgb = COLOR_NAVY_DARK

    add_notes(s2,
              "In forced convection cooling designs, engineers frequently omit thermal radiation at moderate temperature rises, assuming convection dominates. However, because convective heat transfer coefficients decrease downstream proportional to x^(-0.5), convective resistance steadily rises toward the trailing edge. Neglecting radiative dissipation leads to systematic overprediction of peak wall temperatures. Source: results/figures/wall_temperature_all_cases.png.")

    # -------------------------------------------------------------
    # SLIDE 3: Approach (Light)
    # Native table directly on slide background (matching Pitch_Template tmpl-4) + bullets + figure on right
    # -------------------------------------------------------------
    s3 = prs.slides.add_slide(prs.slide_layouts[2])
    set_bg(s3, COLOR_LIGHT_BG)
    add_title(s3, "Four-Case Computational Matrix Isolates Radiation and Grid Effects")
    add_footer(s3, 3)

    # Section Title on left (floating)
    th_box = s3.shapes.add_textbox(Inches(0.6), Inches(1.5), Inches(6.8), Inches(0.4))
    tf_th = th_box.text_frame
    tf_th.margin_left = tf_th.margin_top = tf_th.margin_right = tf_th.margin_bottom = 0
    p = tf_th.paragraphs[0]
    p.text = "2 × 2 Factorial Simulation Matrix"
    p.font.name = FONT_TITLE
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY_DARK

    # Native table directly on canvas (NO enclosing card, matching template slide 4!)
    t_shape = s3.shapes.add_table(5, 5, Inches(0.6), Inches(2.05), Inches(6.8), Inches(2.2))
    tbl = t_shape.table
    tbl.columns[0].width = Inches(2.3)
    tbl.columns[1].width = Inches(1.1)
    tbl.columns[2].width = Inches(1.0)
    tbl.columns[3].width = Inches(1.2)
    tbl.columns[4].width = Inches(1.2)

    headers = ["Case Identifier", "Grid (nx×ny)", "Cells", "Emissivity ε", "Heater q″"]
    matrix_data = [
        ["noRadiation_coarse", "200 × 80", "16,000", "0.0 (Pure)", "1000 W/m²"],
        ["noRadiation_fine", "400 × 160", "64,000", "0.0 (Pure)", "1000 W/m²"],
        ["surfaceRadiation_coarse", "200 × 80", "16,000", "0.8 (Coupled)", "1000 W/m²"],
        ["surfaceRadiation_fine", "400 × 160", "64,000", "0.8 (Coupled)", "1000 W/m²"]
    ]

    for c_idx, h in enumerate(headers):
        cell = tbl.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_NAVY_DARK
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.name = FONT_BODY
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE
        p.alignment = PP_ALIGN.CENTER

    for r_idx, row in enumerate(matrix_data):
        for c_idx, val in enumerate(row):
            cell = tbl.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = COLOR_WHITE if r_idx % 2 == 0 else RGBColor(0xDE, 0xE5, 0xF0)
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.name = FONT_BODY
            p.font.size = Pt(11)
            p.font.color.rgb = COLOR_NAVY_DARK
            p.alignment = PP_ALIGN.LEFT if c_idx == 0 else PP_ALIGN.CENTER

    # Bullets below table floating naturally on #EEF2F7
    b_box3 = s3.shapes.add_textbox(Inches(0.6), Inches(4.55), Inches(6.8), Inches(1.9))
    tf_b3 = b_box3.text_frame
    tf_b3.word_wrap = True
    tf_b3.margin_left = tf_b3.margin_top = tf_b3.margin_right = tf_b3.margin_bottom = 0
    add_bullet_list(tf_b3, [
        "Plate length L = 1.0 m, free-stream velocity U_inf = 2.0 m/s.",
        "Ambient and enclosure temperatures held constant at 300 K.",
        "Reynolds number Re_L = 1.258 × 10⁵ preserves laminar flow regime."
    ], font_size=14)

    # Right: Metric Breakdown Figure inside card
    add_contained_image(s3, Inches(7.8), Inches(1.5), Inches(4.9), Inches(5.2),
                        'four_case_metric_breakdown.png',
                        'Fig. 3: Comprehensive parameter breakdown across all four cases.')

    add_notes(s3,
              "We execute a 2x2 factorial simulation matrix crossing two structured grid densities (16,000 versus 64,000 cells) against two surface emissivity states (ε = 0.0 for pure convection and ε = 0.8 for coupled radiation). The plate operates under steady 2.0 m/s laminar flow at Re_L = 1.258 × 10⁵ with uniform 1000 W/m² base heat flux. This systematic matrix allows rigorous separation of discretization sensitivity from radiative cooling. Source: results/case_audit.csv.")

    # -------------------------------------------------------------
    # SLIDE 4: Domain & Mesh (Light)
    # Figure on left; right side has stat chips and floating bullets
    # -------------------------------------------------------------
    s4 = prs.slides.add_slide(prs.slide_layouts[2])
    set_bg(s4, COLOR_LIGHT_BG)
    add_title(s4, "80:1 Wall Grading Resolves Viscous and Conductive Sublayers")
    add_footer(s4, 4)

    # Left: mesh figure in card
    add_contained_image(s4, Inches(0.6), Inches(1.5), Inches(7.2), Inches(5.2),
                        'mesh_inflation_detail.png',
                        'Fig. 4: Structured inflation mesh near heated plate leading edge (80:1 grading).')

    # Right: Floating content on #EEF2F7
    # Section title
    m_title = s4.shapes.add_textbox(Inches(8.2), Inches(1.5), Inches(4.5), Inches(0.4))
    tf_mt = m_title.text_frame
    tf_mt.margin_left = tf_mt.margin_top = 0
    p = tf_mt.paragraphs[0]
    p.text = "Near-Wall Mesh Resolution"
    p.font.name = FONT_TITLE
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY_DARK

    # Stat chip 1: 41 cells
    add_card(s4, Inches(8.2), Inches(2.05), Inches(4.5), Inches(1.1), bg_color=COLOR_WHITE, border_color=COLOR_BORDER)
    sc1 = s4.shapes.add_textbox(Inches(8.4), Inches(2.1), Inches(4.1), Inches(1.0))
    tf_sc1 = sc1.text_frame
    tf_sc1.word_wrap = True
    tf_sc1.margin_left = tf_sc1.margin_top = 0
    p = tf_sc1.paragraphs[0]
    p.text = "41 Cells in 5 mm"
    p.font.name = FONT_TITLE
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = COLOR_ORANGE
    p2 = tf_sc1.add_paragraph()
    p2.text = "Near-wall inflation zone resolves steep thermal gradients"
    p2.font.name = FONT_BODY
    p2.font.size = Pt(11)
    p2.font.color.rgb = COLOR_NAVY_DARK

    # Stat chip 2: 70.3 μm
    add_card(s4, Inches(8.2), Inches(3.3), Inches(4.5), Inches(1.1), bg_color=COLOR_WHITE, border_color=COLOR_BORDER)
    sc2 = s4.shapes.add_textbox(Inches(8.4), Inches(3.35), Inches(4.1), Inches(1.0))
    tf_sc2 = sc2.text_frame
    tf_sc2.word_wrap = True
    tf_sc2.margin_left = tf_sc2.margin_top = 0
    p = tf_sc2.paragraphs[0]
    p.text = "Δy₁ = 70.3 μm"
    p.font.name = FONT_TITLE
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN
    p2 = tf_sc2.add_paragraph()
    p2.text = "First cell wall-normal height achieves y⁺ ≈ 0.05"
    p2.font.name = FONT_BODY
    p2.font.size = Pt(11)
    p2.font.color.rgb = COLOR_NAVY_DARK

    # Bullets floating naturally below
    mb_box = s4.shapes.add_textbox(Inches(8.2), Inches(4.55), Inches(4.5), Inches(2.0))
    tf_mb = mb_box.text_frame
    tf_mb.word_wrap = True
    tf_mb.margin_left = tf_mb.margin_top = tf_mb.margin_right = tf_mb.margin_bottom = 0
    add_bullet_list(tf_mb, [
        "Domain includes 1.0 m unheated inflow section to develop boundary layer.",
        "Geometric wall-normal grading of 80:1 concentrates 41 cells in 5 mm.",
        "Fine 64,000-cell mesh maintains zero non-orthogonality and skewness."
    ], font_size=13)

    add_notes(s4,
              "The domain spans 2.0 m in length (a 1.0 m unheated inflow plate plus a 1.0 m heated plate) and 0.2 m in height. An 80:1 geometric expansion ratio over 160 vertical divisions yields a first cell height of 70.3 μm, placing 41 cells inside the critical near-wall 5 mm boundary layer region. This fine spacing captures steep wall temperature and velocity gradients with zero mesh skewness. Source: cases/surfaceRadiation_fine/system/blockMeshDict.")

    # -------------------------------------------------------------
    # SLIDE 5: Radiation Model (Light)
    # Authentic human engineering mathematical typography (no code carrots ^), floating bullets on right
    # -------------------------------------------------------------
    s5 = prs.slides.add_slide(prs.slide_layouts[2])
    set_bg(s5, COLOR_LIGHT_BG)
    add_title(s5, "Newton-Raphson Solver Enforces Non-Linear Surface Heat Balance")
    add_footer(s5, 5)

    # Left card: Equations cleanly formatted
    add_card(s5, Inches(0.6), Inches(1.5), Inches(6.8), Inches(5.2), bg_color=COLOR_WHITE)
    eq_box = s5.shapes.add_textbox(Inches(0.9), Inches(1.75), Inches(6.2), Inches(4.7))
    tf_eq = eq_box.text_frame
    tf_eq.word_wrap = True
    tf_eq.margin_left = tf_eq.margin_top = tf_eq.margin_right = tf_eq.margin_bottom = 0

    p = tf_eq.paragraphs[0]
    p.text = "Wall Boundary Energy Conservation"
    p.font.name = FONT_TITLE
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY_DARK
    p.space_after = Pt(12)

    # Eq 1: Surface Heat Balance
    p = tf_eq.add_paragraph()
    p.text = "1. Surface Heat Balance (Enforced at Wall Face):"
    p.font.name = FONT_BODY
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY_DARK
    
    p = tf_eq.add_paragraph()
    p.text = "q″_heater = q″_conv + q″_rad = 1000 W/m²"
    p.font.name = FONT_TITLE
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = COLOR_ORANGE
    p.space_after = Pt(10)

    # Eq 2: Stefan-Boltzmann Surface Radiation
    p = tf_eq.add_paragraph()
    p.text = "2. Stefan-Boltzmann Quartic Radiation Emission:"
    p.font.name = FONT_BODY
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY_DARK

    p = tf_eq.add_paragraph()
    p.text = "q″_rad = ε σ (T_w⁴ − T_sur⁴)"
    p.font.name = FONT_TITLE
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN

    p = tf_eq.add_paragraph()
    p.text = "where ε = 0.8,  σ = 5.670 × 10⁻⁸ W/(m²·K⁴),  T_sur = 300 K"
    p.font.name = FONT_BODY
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_SLATE
    p.space_after = Pt(10)

    # Eq 3: Newton-Raphson Iteration
    p = tf_eq.add_paragraph()
    p.text = "3. In-Situ Newton-Raphson Wall Root-Finding:"
    p.font.name = FONT_BODY
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY_DARK

    p = tf_eq.add_paragraph()
    p.text = "T_w,new = T_w,old − f(T_w) / f′(T_w)"
    p.font.name = FONT_TITLE
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY_DARK

    p = tf_eq.add_paragraph()
    p.text = "f(T_w) = −k (∂T/∂y)_w + ε σ (T_w⁴ − T_sur⁴) − q″_heater = 0"
    p.font.name = FONT_BODY
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_SLATE

    # Right: Floating content on #EEF2F7
    r5_title = s5.shapes.add_textbox(Inches(7.8), Inches(1.5), Inches(4.9), Inches(0.4))
    tf_r5t = r5_title.text_frame
    tf_r5t.margin_left = tf_r5t.margin_top = 0
    p = tf_r5t.paragraphs[0]
    p.text = "Boundary Condition Mechanics"
    p.font.name = FONT_TITLE
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY_DARK

    # Bullets floating naturally
    r5_box = s5.shapes.add_textbox(Inches(7.8), Inches(2.05), Inches(4.9), Inches(2.2))
    tf_r5 = r5_box.text_frame
    tf_r5.word_wrap = True
    tf_r5.margin_left = tf_r5.margin_top = tf_r5.margin_right = tf_r5.margin_bottom = 0
    add_bullet_list(tf_r5, [
        "Solves non-linear quartic radiative flux at every boundary face.",
        "Enforces local face heat balance by construction during each PIMPLE step.",
        "Newton-Raphson scheme converges to double precision within four iterations."
    ], font_size=14)

    # 2 Stat Chips floating cleanly below bullets
    add_card(s5, Inches(7.8), Inches(4.8), Inches(2.35), Inches(1.9), bg_color=COLOR_WHITE, border_color=COLOR_BORDER)
    ch1 = s5.shapes.add_textbox(Inches(7.95), Inches(4.95), Inches(2.05), Inches(1.6))
    tf_ch1 = ch1.text_frame
    tf_ch1.word_wrap = True
    tf_ch1.margin_left = tf_ch1.margin_top = 0
    p = tf_ch1.paragraphs[0]
    p.text = "ε = 0.8"
    p.font.name = FONT_TITLE
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = COLOR_ORANGE
    p2 = tf_ch1.add_paragraph()
    p2.text = "Grey-diffuse emissivity to 300 K external enclosure"
    p2.font.name = FONT_BODY
    p2.font.size = Pt(11)
    p2.font.color.rgb = COLOR_NAVY_DARK

    add_card(s5, Inches(10.35), Inches(4.8), Inches(2.35), Inches(1.9), bg_color=COLOR_WHITE, border_color=COLOR_BORDER)
    ch2 = s5.shapes.add_textbox(Inches(10.5), Inches(4.95), Inches(2.05), Inches(1.6))
    tf_ch2 = ch2.text_frame
    tf_ch2.word_wrap = True
    tf_ch2.margin_left = tf_ch2.margin_top = 0
    p = tf_ch2.paragraphs[0]
    p.text = "< 4 Iter"
    p.font.name = FONT_TITLE
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN
    p2 = tf_ch2.add_paragraph()
    p2.text = "Fast quadratic convergence per boundary face"
    p2.font.name = FONT_BODY
    p2.font.size = Pt(11)
    p2.font.color.rgb = COLOR_NAVY_DARK

    add_notes(s5,
              "The wall energy boundary condition equates the constant 1000 W/m² electric heater flux to the sum of conductive-convective heat transfer into the fluid and net Stefan-Boltzmann radiation to the 300 K enclosure. Because the radiative term is quartic in Tw, a localized Newton-Raphson scheme solves for the face temperature at each iteration. Wall-face heat balance is enforced by construction. We use a custom BC rather than OpenFOAM's fvDOM because fvDOM models participating media, incurring unnecessary computational overhead for optically thin air. Source: cases/surfaceRadiation_fine/0/T.")

    # -------------------------------------------------------------
    # SLIDE 6: Solver & Convergence (Light)
    # Figure left in card, right side has floating bullets & 3 clean stat bars
    # -------------------------------------------------------------
    s6 = prs.slides.add_slide(prs.slide_layouts[2])
    set_bg(s6, COLOR_LIGHT_BG)
    add_title(s6, "Residuals Fall by 5+ Orders Across 1,500 Iterations")
    add_footer(s6, 6)

    # Left: Convergence plot in card
    add_contained_image(s6, Inches(0.6), Inches(1.5), Inches(7.2), Inches(5.2),
                        'convergence_histories.png',
                        'Fig. 5: Iterative residual history for velocity, pressure, and enthalpy.')

    # Right: Floating on #EEF2F7
    r6_title = s6.shapes.add_textbox(Inches(8.2), Inches(1.5), Inches(4.5), Inches(0.4))
    tf_r6t = r6_title.text_frame
    tf_r6t.margin_left = tf_r6t.margin_top = 0
    p = tf_r6t.paragraphs[0]
    p.text = "Numerical Formulation"
    p.font.name = FONT_TITLE
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY_DARK

    # Bullets floating naturally
    r6_box = s6.shapes.add_textbox(Inches(8.2), Inches(2.05), Inches(4.5), Inches(2.2))
    tf_r6 = r6_box.text_frame
    tf_r6.word_wrap = True
    tf_r6.margin_left = tf_r6.margin_top = tf_r6.margin_right = tf_r6.margin_bottom = 0
    add_bullet_list(tf_r6, [
        "Solved with OpenFOAM 13 foamRun using steady-state PIMPLE algorithm.",
        "Residuals fall by 5+ orders, reaching monotonic asymptotic plateau.",
        "Constant properties decouple momentum from temperature under zero gravity."
    ], font_size=14)

    # 3 Clean Stat Bars floating on canvas
    add_card(s6, Inches(8.2), Inches(4.5), Inches(4.5), Inches(0.65), bg_color=COLOR_WHITE, border_color=COLOR_BORDER)
    c1 = s6.shapes.add_textbox(Inches(8.4), Inches(4.57), Inches(4.1), Inches(0.5))
    c1.text_frame.margin_left = c1.text_frame.margin_top = 0
    p = c1.text_frame.paragraphs[0]
    p.text = "1,500  Iterations Completed"
    p.font.name = FONT_TITLE
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY_DARK

    add_card(s6, Inches(8.2), Inches(5.25), Inches(4.5), Inches(0.65), bg_color=COLOR_WHITE, border_color=COLOR_BORDER)
    c2 = s6.shapes.add_textbox(Inches(8.4), Inches(5.32), Inches(4.1), Inches(0.5))
    c2.text_frame.margin_left = c2.text_frame.margin_top = 0
    p = c2.text_frame.paragraphs[0]
    p.text = "> 10⁻⁵  Residual Reduction"
    p.font.name = FONT_TITLE
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_ORANGE

    add_card(s6, Inches(8.2), Inches(6.0), Inches(4.5), Inches(0.65), bg_color=COLOR_WHITE, border_color=COLOR_BORDER)
    c3 = s6.shapes.add_textbox(Inches(8.4), Inches(6.07), Inches(4.1), Inches(0.5))
    c3.text_frame.margin_left = c3.text_frame.margin_top = 0
    p = c3.text_frame.paragraphs[0]
    p.text = "0.00  Max Non-Orthogonality"
    p.font.name = FONT_TITLE
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN

    add_notes(s6,
              "All cases are solved using OpenFOAM 13's foamRun solver configured with the heRhoThermo thermodynamic library and perfectGas equation of state. Across 1,500 iterations, velocity, pressure, and energy residuals decline by over five orders of magnitude to a flat plateau. Because constant viscosity (1.846e-5 kg/m·s) and zero gravity are prescribed, the Navier-Stokes momentum equations decouple analytically from the energy equation, serving as a strict consistency check. Source: results/figures/convergence_histories.png.")

    # -------------------------------------------------------------
    # SLIDE 7: Headline Result (Light)
    # Heat-flux split: 2 KPI cards + floating bullets below
    # -------------------------------------------------------------
    s7 = prs.slides.add_slide(prs.slide_layouts[2])
    set_bg(s7, COLOR_LIGHT_BG)
    add_title(s7, "Surface Radiation Carries 21.3% of Total Heat Along Plate")
    add_footer(s7, 7)

    # Left: heat balance and Nusselt plot
    add_contained_image(s7, Inches(0.6), Inches(1.5), Inches(7.2), Inches(5.2),
                        'wall_heat_balance_and_nusselt.png',
                        'Fig. 6: Streamwise convective vs radiative heat-flux split and Nusselt number.')

    # Right: 2 Large KPI cards side-by-side or stacked cleanly
    # Card 1: Plate-averaged
    add_card(s7, Inches(8.2), Inches(1.5), Inches(4.5), Inches(1.4), bg_color=COLOR_WHITE, border_color=COLOR_BORDER)
    kpi1 = s7.shapes.add_textbox(Inches(8.4), Inches(1.6), Inches(4.1), Inches(1.2))
    tf_k1 = kpi1.text_frame
    tf_k1.word_wrap = True
    tf_k1.margin_left = tf_k1.margin_top = 0
    p = tf_k1.paragraphs[0]
    p.text = "21.3%"
    p.font.name = FONT_TITLE
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = COLOR_ORANGE
    p2 = tf_k1.add_paragraph()
    p2.text = "Plate-Averaged Radiative Load"
    p2.font.name = FONT_BODY
    p2.font.size = Pt(13)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_NAVY_DARK
    p3 = tf_k1.add_paragraph()
    p3.text = "Mean flux: 213.2 W/m² (preliminary, fine-grid)"
    p3.font.name = FONT_BODY
    p3.font.size = Pt(11)
    p3.font.color.rgb = COLOR_SLATE

    # Card 2: Trailing-edge
    add_card(s7, Inches(8.2), Inches(3.05), Inches(4.5), Inches(1.4), bg_color=COLOR_WHITE, border_color=COLOR_BORDER)
    kpi2 = s7.shapes.add_textbox(Inches(8.4), Inches(3.15), Inches(4.1), Inches(1.2))
    tf_k2 = kpi2.text_frame
    tf_k2.word_wrap = True
    tf_k2.margin_left = tf_k2.margin_top = 0
    p = tf_k2.paragraphs[0]
    p.text = "21.6%"
    p.font.name = FONT_TITLE
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN
    p2 = tf_k2.add_paragraph()
    p2.text = "Trailing-Edge Radiative Load"
    p2.font.name = FONT_BODY
    p2.font.size = Pt(13)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_NAVY_DARK
    p3 = tf_k2.add_paragraph()
    p3.text = "Trailing flux: 215.6 W/m² at x = 1.0 m"
    p3.font.name = FONT_BODY
    p3.font.size = Pt(11)
    p3.font.color.rgb = COLOR_SLATE

    # Bullets floating naturally on #EEF2F7 canvas (NO outer card!)
    b7_box = s7.shapes.add_textbox(Inches(8.2), Inches(4.65), Inches(4.5), Inches(2.0))
    tf_b7 = b7_box.text_frame
    tf_b7.word_wrap = True
    tf_b7.margin_left = tf_b7.margin_top = tf_b7.margin_right = tf_b7.margin_bottom = 0
    add_bullet_list(tf_b7, [
        "Surface radiation relieves over one-fifth of the total heat dissipation load.",
        "Radiative heat flux remains nearly uniform along the entire plate surface.",
        "Convective flux drops downstream as thermal boundary layer growth increases resistance."
    ], font_size=13)

    add_notes(s7,
              "On the fine 64,000-cell mesh, surface radiation dissipates an integrated plate-averaged flux of 213.2 W/m² (21.32% of total heat), rising to 21.56% (215.59 W/m²) at the trailing edge. Open issue: For uniform heat flux, laminar correlation Nu_x = 0.453 Re_x^0.5 Pr^(1/3) gives Nu ≈ 143 and wall rise ≈ 267 K at x = 1 m, whereas CFD reports Nu ≈ 875 and a 43.7 K rise. Consequently, these 21.3% and 6.98 K figures are preliminary fine-grid metrics subject to ongoing grid convergence. Source: results/figures/wall_heat_balance_and_nusselt.png.")

    # -------------------------------------------------------------
    # SLIDE 8: Cooling Footprint (Light)
    # Figure left; right side has big stat chip + floating bullets
    # -------------------------------------------------------------
    s8 = prs.slides.add_slide(prs.slide_layouts[2])
    set_bg(s8, COLOR_LIGHT_BG)
    add_title(s8, "Surface Radiation Depresses Peak Wall Temperature by 6.98 K")
    add_footer(s8, 8)

    # Left: Difference zoom plot
    add_contained_image(s8, Inches(0.6), Inches(1.5), Inches(7.2), Inches(5.2),
                        'temperature_difference_zoom.png',
                        'Fig. 7: Boundary layer temperature difference field (T_radiation - T_baseline).')

    # Right: Floating on #EEF2F7
    # Big Stat Card
    add_card(s8, Inches(8.2), Inches(1.5), Inches(4.5), Inches(1.4), bg_color=COLOR_WHITE, border_color=COLOR_BORDER)
    c8_box = s8.shapes.add_textbox(Inches(8.4), Inches(1.6), Inches(4.1), Inches(1.2))
    tf_c8 = c8_box.text_frame
    tf_c8.word_wrap = True
    tf_c8.margin_left = tf_c8.margin_top = 0
    p = tf_c8.paragraphs[0]
    p.text = "6.98 K Drop"
    p.font.name = FONT_TITLE
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN
    p2 = tf_c8.add_paragraph()
    p2.text = "Peak Wall Temperature Reduction (Fine Grid)"
    p2.font.name = FONT_BODY
    p2.font.size = Pt(13)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_NAVY_DARK

    # Bullets starting cleanly below the stat chip (floating naturally!)
    b8_box = s8.shapes.add_textbox(Inches(8.2), Inches(3.2), Inches(4.5), Inches(2.6))
    tf_b8 = b8_box.text_frame
    tf_b8.word_wrap = True
    tf_b8.margin_left = tf_b8.margin_top = tf_b8.margin_right = tf_b8.margin_bottom = 0
    add_bullet_list(tf_b8, [
        "Radiation lowers plate wall temperature along the entire heated length.",
        "Cooling effect intensifies downstream, reaching maximum depression of 6.98 K.",
        "Thermal boundary layer thickness remains virtually unchanged across radiation cases."
    ], font_size=14)

    # Footnote note
    p_fn = tf_b8.add_paragraph()
    p_fn.space_before = Pt(8)
    p_fn.text = "Fine grid trailing edge: 336.70 K vs 343.68 K pure convection."
    p_fn.font.name = FONT_BODY
    p_fn.font.size = Pt(11)
    p_fn.font.color.rgb = COLOR_SLATE

    add_notes(s8,
              "Surface radiation lowers the local wall temperature across the entire 1.0 m plate, with the maximum temperature depression reaching 6.98 K at the trailing edge (dropping from 343.68 K to 336.70 K on the fine mesh). Note that thermal boundary layer thickness does not thin under radiation; in fact, delta_T,99 expands slightly from 5.072 mm to 5.175 mm due to altered near-wall temperature profiles. Source: results/figures/temperature_difference_zoom.png.")

    # -------------------------------------------------------------
    # SLIDE 9: Validation (Aero) (Dark)
    # Matches template slide 5 exactly!
    # Figure placed cleanly on dark canvas + 3 dark stat cards
    # -------------------------------------------------------------
    s9 = prs.slides.add_slide(prs.slide_layouts[3]) # DARK_CONTENT
    set_bg(s9, COLOR_NAVY_DARK)
    add_title(s9, "Skin Friction Validates Against Blasius Within 0.11%", dark=True)
    add_footer(s9, 9, dark=True)

    # Left: Blasius figure placed directly on dark background with subtle border
    # (Just like template slide 5!)
    add_contained_image(s9, Inches(0.6), Inches(1.5), Inches(7.2), Inches(5.2),
                        'blasius_velocity_validation.png',
                        'Fig. 8: Non-dimensional streamwise velocity collapse vs exact Blasius curve.',
                        dark_card=True)

    # Right: 3 Dark Stat Cards (matching template slide 5)
    chips_data_9 = [
        ("0.11%", COLOR_ORANGE, "Skin-friction relative error vs Blasius (Cf = 1.874e-3 vs 1.872e-3)"),
        ("1.26 × 10⁵", COLOR_CYAN, "Plate Reynolds number (Re_L = U_inf L / ν) confirms laminar flow"),
        ("Invariant", COLOR_AMBER, "Velocity profiles strictly identical between radiating and baseline cases")
    ]
    for idx, (val, col, desc) in enumerate(chips_data_9):
        top_y = Inches(1.5 + idx * 1.75)
        add_card(s9, Inches(8.2), top_y, Inches(4.5), Inches(1.55), bg_color=COLOR_NAVY_CARD, border_color=None)
        box = s9.shapes.add_textbox(Inches(8.5), top_y + Inches(0.18), Inches(3.9), Inches(1.2))
        tf = box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = 0
        p = tf.paragraphs[0]
        p.text = val
        p.font.name = FONT_TITLE
        p.font.size = Pt(36)
        p.font.bold = True
        p.font.color.rgb = col
        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.name = FONT_BODY
        p2.font.size = Pt(12)
        p2.font.color.rgb = COLOR_LIGHT_BG

    add_notes(s9,
              "Hydrodynamic solver accuracy is validated against the classical Blasius similarity solution. Trailing-edge skin friction matches the analytical prediction (0.664 / sqrt(Re_L) = 1.872e-3) with just 0.11% relative error (computed Cf = 1.874e-3). Furthermore, because fluid transport properties are constant and buoyancy is absent, velocity profiles are strictly invariant between radiation cases, verifying hydrodynamic decoupling. Source: results/figures/blasius_velocity_validation.png.")

    # -------------------------------------------------------------
    # SLIDE 10: Validation (Thermal) (Dark)
    # Matches template slide 5 exactly!
    # Figure placed cleanly on dark canvas + 3 dark stat cards
    # -------------------------------------------------------------
    s10 = prs.slides.add_slide(prs.slide_layouts[3]) # DARK_CONTENT
    set_bg(s10, COLOR_NAVY_DARK)
    add_title(s10, "Thermal Boundary Layer Tracks Self-Similar Growth Dynamics", dark=True)
    add_footer(s10, 10, dark=True)

    # Left: Pohlhausen figure in dark card
    add_contained_image(s10, Inches(0.6), Inches(1.5), Inches(7.2), Inches(5.2),
                        'pohlhausen_thermal_validation.png',
                        'Fig. 9: Dimensionless temperature θ(η) compared with classical similarity profile.',
                        dark_card=True)

    # Right: 3 Dark Stat Cards
    chips_data_10 = [
        ("58.3%", COLOR_AMBER, "Profile deviation vs isothermal Pohlhausen benchmark at x/L = 0.5"),
        ("0.31", COLOR_CYAN, "Mean dimensionless temperature difference |θ_CFD - θ_Pohl|"),
        ("q″ = Const", COLOR_ORANGE, "Physical shift caused by uniform heat flux vs isothermal wall condition")
    ]
    for idx, (val, col, desc) in enumerate(chips_data_10):
        top_y = Inches(1.5 + idx * 1.75)
        add_card(s10, Inches(8.2), top_y, Inches(4.5), Inches(1.55), bg_color=COLOR_NAVY_CARD, border_color=None)
        box = s10.shapes.add_textbox(Inches(8.5), top_y + Inches(0.18), Inches(3.9), Inches(1.2))
        tf = box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = 0
        p = tf.paragraphs[0]
        p.text = val
        p.font.name = FONT_TITLE
        p.font.size = Pt(36)
        p.font.bold = True
        p.font.color.rgb = col
        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.name = FONT_BODY
        p2.font.size = Pt(12)
        p2.font.color.rgb = COLOR_LIGHT_BG

    add_notes(s10,
              "The thermal boundary layer profiles collapse into a self-similar shape when plotted against the similarity variable η. We compare the CFD results with Pohlhausen's classical similarity profile, noting a 58.3% profile deviation (mean absolute difference 0.31). This difference is expected because Pohlhausen derived his solution for an isothermal wall (Tw = const), whereas this case enforces uniform heat flux (q'' = const), which alters near-wall temperature curvature. Source: results/figures/pohlhausen_thermal_validation.png.")

    # -------------------------------------------------------------
    # SLIDE 11: Grid Sensitivity (Light)
    # Comparison cards with badges 1 & 2 (matching template slide 6!)
    # -------------------------------------------------------------
    s11 = prs.slides.add_slide(prs.slide_layouts[2])
    set_bg(s11, COLOR_LIGHT_BG)
    add_title(s11, "Results Show Strong Grid Dependence and Require Further Refinement")
    add_footer(s11, 11)

    # Left: Grid comparison figure in card
    add_contained_image(s11, Inches(0.6), Inches(1.5), Inches(6.8), Inches(5.2),
                        'grid_comparison.png',
                        'Fig. 10: Coarse (16,000 cells) vs fine (64,000 cells) grid comparison.')

    # Right: Coarse vs Fine side-by-side cards (template layout 6 style with circular badges)
    # Badge 1: Coarse
    badge1 = s11.shapes.add_shape(MSO_SHAPE.OVAL, Inches(7.8), Inches(1.5), Inches(0.6), Inches(0.6))
    badge1.fill.solid()
    badge1.fill.fore_color.rgb = COLOR_SLATE
    badge1.line.fill.background()
    p_b1 = badge1.text_frame.paragraphs[0]
    p_b1.text = "1"
    p_b1.font.name = FONT_TITLE
    p_b1.font.size = Pt(18)
    p_b1.font.bold = True
    p_b1.font.color.rgb = COLOR_WHITE
    p_b1.alignment = PP_ALIGN.CENTER

    # Coarse card
    add_card(s11, Inches(7.8), Inches(2.2), Inches(2.35), Inches(3.2), bg_color=COLOR_WHITE, border_color=COLOR_BORDER)
    c_box = s11.shapes.add_textbox(Inches(7.95), Inches(2.3), Inches(2.05), Inches(3.0))
    tf_c = c_box.text_frame
    tf_c.word_wrap = True
    tf_c.margin_left = tf_c.margin_top = 0
    p = tf_c.paragraphs[0]
    p.text = "Coarse (16k)"
    p.font.name = FONT_TITLE
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY_DARK
    
    p = tf_c.add_paragraph()
    p.space_before = Pt(6)
    p.text = "Baseline Tw:"
    p.font.name = FONT_BODY
    p.font.size = Pt(11)
    p = tf_c.add_paragraph()
    p.text = "394.9 K"
    p.font.name = FONT_TITLE
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = COLOR_ORANGE

    p = tf_c.add_paragraph()
    p.space_before = Pt(6)
    p.text = "Radiation Benefit:"
    p.font.name = FONT_BODY
    p.font.size = Pt(11)
    p = tf_c.add_paragraph()
    p.text = "30.5 K drop"
    p.font.name = FONT_TITLE
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN

    p = tf_c.add_paragraph()
    p.space_before = Pt(4)
    p.text = "Rad Share: 43.2%"
    p.font.name = FONT_BODY
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_SLATE

    # Badge 2: Fine
    badge2 = s11.shapes.add_shape(MSO_SHAPE.OVAL, Inches(10.35), Inches(1.5), Inches(0.6), Inches(0.6))
    badge2.fill.solid()
    badge2.fill.fore_color.rgb = COLOR_ORANGE
    badge2.line.fill.background()
    p_b2 = badge2.text_frame.paragraphs[0]
    p_b2.text = "2"
    p_b2.font.name = FONT_TITLE
    p_b2.font.size = Pt(18)
    p_b2.font.bold = True
    p_b2.font.color.rgb = COLOR_WHITE
    p_b2.alignment = PP_ALIGN.CENTER

    # Fine card
    add_card(s11, Inches(10.35), Inches(2.2), Inches(2.35), Inches(3.2), bg_color=COLOR_WHITE, border_color=COLOR_BORDER)
    f_box = s11.shapes.add_textbox(Inches(10.5), Inches(2.3), Inches(2.05), Inches(3.0))
    tf_f = f_box.text_frame
    tf_f.word_wrap = True
    tf_f.margin_left = tf_f.margin_top = 0
    p = tf_f.paragraphs[0]
    p.text = "Fine (64k)"
    p.font.name = FONT_TITLE
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY_DARK

    p = tf_f.add_paragraph()
    p.space_before = Pt(6)
    p.text = "Baseline Tw:"
    p.font.name = FONT_BODY
    p.font.size = Pt(11)
    p = tf_f.add_paragraph()
    p.text = "343.7 K"
    p.font.name = FONT_TITLE
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = COLOR_ORANGE

    p = tf_f.add_paragraph()
    p.space_before = Pt(6)
    p.text = "Radiation Benefit:"
    p.font.name = FONT_BODY
    p.font.size = Pt(11)
    p = tf_f.add_paragraph()
    p.text = "6.98 K drop"
    p.font.name = FONT_TITLE
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN

    p = tf_f.add_paragraph()
    p.space_before = Pt(4)
    p.text = "Rad Share: 21.6%"
    p.font.name = FONT_BODY
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_SLATE

    # Takeaway warning banner below
    add_card(s11, Inches(7.8), Inches(5.6), Inches(4.9), Inches(1.1), bg_color=COLOR_WHITE, border_color=COLOR_BORDER)
    t_box11 = s11.shapes.add_textbox(Inches(7.95), Inches(5.68), Inches(4.6), Inches(0.9))
    tf_t11 = t_box11.text_frame
    tf_t11.word_wrap = True
    tf_t11.margin_left = tf_t11.margin_top = 0
    p = tf_t11.paragraphs[0]
    p.text = "Status: Results are not yet grid-converged"
    p.font.name = FONT_TITLE
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_RED
    p2 = tf_t11.add_paragraph()
    p2.text = "A 51.2 K baseline shift indicates substantial mesh sensitivity requiring a 3rd Richardson grid."
    p2.font.name = FONT_BODY
    p2.font.size = Pt(11)
    p2.font.color.rgb = COLOR_NAVY_DARK

    add_notes(s11,
              "Comparing coarse (16k) and fine (64k) grids shows substantial mesh sensitivity: baseline wall temperature falls from 394.9 K to 343.7 K (a 51.2 K shift), and radiative cooling decreases from 30.5 K to 6.98 K. We plainly state that results are not yet grid-converged. Pr = 0.71 implies theoretical delta_T / delta ≈ 1.12, whereas CFD yields ≈ 0.94 on the fine grid. Open issue: Computed Nu ≈ 875 substantially exceeds the laminar correlation Nu ≈ 143, confirming that these values are preliminary fine-grid findings. Source: results/figures/grid_comparison.png.")

    # -------------------------------------------------------------
    # SLIDE 12: Literature Context (Light)
    # Figure left in card, right side has floating bullets & physical regime box
    # -------------------------------------------------------------
    s12 = prs.slides.add_slide(prs.slide_layouts[2])
    set_bg(s12, COLOR_LIGHT_BG)
    add_title(s12, "Observed Radiation Trends Align with Boundary Layer Literature")
    add_footer(s12, 12)

    # Left: literature analogy plot in card
    add_contained_image(s12, Inches(0.6), Inches(1.5), Inches(7.0), Inches(5.2),
                        'research_paper_radiation_analogy.png',
                        'Fig. 11: Qualitative comparison of radiation cooling mechanisms in boundary layers.')

    # Right: Floating on #EEF2F7 canvas (NO outer white card!)
    r12_title = s12.shapes.add_textbox(Inches(7.9), Inches(1.5), Inches(4.8), Inches(0.7))
    tf_r12t = r12_title.text_frame
    tf_r12t.margin_left = tf_r12t.margin_top = 0
    p = tf_r12t.paragraphs[0]
    p.text = "Literature Trend Comparison"
    p.font.name = FONT_TITLE
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY_DARK
    
    p_sub = tf_r12t.add_paragraph()
    p_sub.text = "(Qualitative only — consistent in trend)"
    p_sub.font.name = FONT_BODY
    p_sub.font.size = Pt(12)
    p_sub.font.color.rgb = COLOR_SLATE

    # Exactly 3 bullets (<= 12 words) floating naturally
    r12_box = s12.shapes.add_textbox(Inches(7.9), Inches(2.3), Inches(4.8), Inches(2.2))
    tf_r12 = r12_box.text_frame
    tf_r12.word_wrap = True
    tf_r12.margin_left = tf_r12.margin_top = tf_r12.margin_right = tf_r12.margin_bottom = 0
    add_bullet_list(tf_r12, [
        "Reddy et al. (2014) reported consistent wall cooling in radiative boundary layers.",
        "Raju et al. (2026) observed comparable non-linear radiative heat flux partitioning.",
        "Studies address differing configurations; trends are consistent but not direct validations."
    ], font_size=13)

    # Context breakdown card below (clean card floating on canvas)
    add_card(s12, Inches(7.9), Inches(4.6), Inches(4.8), Inches(2.1), bg_color=COLOR_WHITE, border_color=COLOR_BORDER)
    rc_box = s12.shapes.add_textbox(Inches(8.1), Inches(4.7), Inches(4.4), Inches(1.9))
    tf_rc = rc_box.text_frame
    tf_rc.word_wrap = True
    tf_rc.margin_left = tf_rc.margin_top = 0

    p_c = tf_rc.paragraphs[0]
    p_c.text = "Physical Regime Distinctions"
    p_c.font.name = FONT_TITLE
    p_c.font.size = Pt(13)
    p_c.font.bold = True
    p_c.font.color.rgb = COLOR_NAVY_DARK
    p_c.space_after = Pt(4)

    p_c1 = tf_rc.add_paragraph()
    p_c1.text = "Reddy (2014): MHD vertical plate with Rosseland radiation model."
    p_c1.font.name = FONT_BODY
    p_c1.font.size = Pt(11)
    p_c1.font.color.rgb = COLOR_SLATE

    p_c2 = tf_rc.add_paragraph()
    p_c2.text = "Raju (2026): Darcy-Brinkman porous medium flow equations."
    p_c2.font.name = FONT_BODY
    p_c2.font.size = Pt(11)
    p_c2.font.color.rgb = COLOR_SLATE

    p_c3 = tf_rc.add_paragraph()
    p_c3.text = "Present CFD: Plain flat-plate surface radiation in clear air."
    p_c3.font.name = FONT_BODY
    p_c3.font.size = Pt(11)
    p_c3.font.bold = True
    p_c3.font.color.rgb = COLOR_ORANGE

    add_notes(s12,
              "Published literature on boundary layer thermal radiation confirms that radiative emission significantly reduces wall temperatures. Reddy et al. (2014) studied stretching vertical plates under MHD, and Raju et al. (2026) examined porous media flows; both demonstrated comparable wall cooling effects. Because these studies involve different governing physics (MHD, porous media), this comparison is qualitative only and labeled consistent in trend, not cross-validation. The 18-25% statistic attributed previously to Freegah (2025) has been omitted. Source: results/figures/research_paper_radiation_analogy.png.")

    # -------------------------------------------------------------
    # SLIDE 13: Limits & Next Steps (Light)
    # Two clean balanced cards matching Pitch_Template tmpl-7!
    # -------------------------------------------------------------
    s13 = prs.slides.add_slide(prs.slide_layouts[2])
    set_bg(s13, COLOR_LIGHT_BG)
    add_title(s13, "Planned Refinements Focus on GCI Audit and Global Energy Closure")
    add_footer(s13, 13)

    # Card 1: Known limits (exactly 3 bullets, <= 12 words)
    add_card(s13, Inches(0.6), Inches(1.5), Inches(5.9), Inches(5.2), bg_color=COLOR_WHITE)
    lim_box = s13.shapes.add_textbox(Inches(0.9), Inches(1.8), Inches(5.3), Inches(4.6))
    tf_lim = lim_box.text_frame
    tf_lim.word_wrap = True
    tf_lim.margin_left = tf_lim.margin_top = tf_lim.margin_right = tf_lim.margin_bottom = 0

    p = tf_lim.paragraphs[0]
    p.text = "Known Limitations"
    p.font.name = FONT_TITLE
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY_DARK
    p.space_after = Pt(16)

    add_bullet_list(tf_lim, [
        "Two-grid study without third refinement precludes formal ASME GCI calculation.",
        "Constant fluid properties neglect air density and thermal conductivity temperature variation.",
        "Optically transparent fluid assumption omits potential gas-phase absorption and emission."
    ], font_size=15)

    p_lim_note = tf_lim.add_paragraph()
    p_lim_note.space_before = Pt(20)
    p_lim_note.text = "Audit status: Disclosed upfront to guide future experimental verification."
    p_lim_note.font.name = FONT_BODY
    p_lim_note.font.size = Pt(12)
    p_lim_note.font.color.rgb = COLOR_SLATE

    # Card 2: Next steps featuring 3 Large Stat / Milestone Chips
    add_card(s13, Inches(6.8), Inches(1.5), Inches(5.9), Inches(5.2), bg_color=COLOR_WHITE)
    nxt_box = s13.shapes.add_textbox(Inches(7.1), Inches(1.8), Inches(5.3), Inches(0.5))
    tf_nxt = nxt_box.text_frame
    tf_nxt.margin_left = tf_nxt.margin_top = 0
    p = tf_nxt.paragraphs[0]
    p.text = "Roadmap Milestones"
    p.font.name = FONT_TITLE
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY_DARK

    # Milestone Chip 1: 800 x 320
    add_card(s13, Inches(7.1), Inches(2.45), Inches(5.3), Inches(1.15), bg_color=COLOR_LIGHT_BG, border_color=None)
    m1_box = s13.shapes.add_textbox(Inches(7.3), Inches(2.5), Inches(4.9), Inches(1.05))
    tf_m1 = m1_box.text_frame
    tf_m1.word_wrap = True
    tf_m1.margin_left = tf_m1.margin_top = 0
    p = tf_m1.paragraphs[0]
    p.text = "800 × 320 Cells"
    p.font.name = FONT_TITLE
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = COLOR_ORANGE
    p2 = tf_m1.add_paragraph()
    p2.text = "Execute 3rd mesh level to establish formal ASME GCI error bars"
    p2.font.name = FONT_BODY
    p2.font.size = Pt(12)
    p2.font.color.rgb = COLOR_NAVY_DARK

    # Milestone Chip 2: 0.41 W
    add_card(s13, Inches(7.1), Inches(3.75), Inches(5.3), Inches(1.15), bg_color=COLOR_LIGHT_BG, border_color=None)
    m2_box = s13.shapes.add_textbox(Inches(7.3), Inches(3.8), Inches(4.9), Inches(1.05))
    tf_m2 = m2_box.text_frame
    tf_m2.word_wrap = True
    tf_m2.margin_left = tf_m2.margin_top = 0
    p = tf_m2.paragraphs[0]
    p.text = "0.41 W Enthalpy Audit"
    p.font.name = FONT_TITLE
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN
    p2 = tf_m2.add_paragraph()
    p2.text = "Reconcile outlet fluid plume flux against 10.0 W plate heater input"
    p2.font.name = FONT_BODY
    p2.font.size = Pt(12)
    p2.font.color.rgb = COLOR_NAVY_DARK

    # Milestone Chip 3: Variable
    add_card(s13, Inches(7.1), Inches(5.05), Inches(5.3), Inches(1.15), bg_color=COLOR_LIGHT_BG, border_color=None)
    m3_box = s13.shapes.add_textbox(Inches(7.3), Inches(5.1), Inches(4.9), Inches(1.05))
    tf_m3 = m3_box.text_frame
    tf_m3.word_wrap = True
    tf_m3.margin_left = tf_m3.margin_top = 0
    p = tf_m3.paragraphs[0]
    p.text = "Variable Properties"
    p.font.name = FONT_TITLE
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = COLOR_AMBER
    p2 = tf_m3.add_paragraph()
    p2.text = "Incorporate temperature-dependent air density and conductivity"
    p2.font.name = FONT_BODY
    p2.font.size = Pt(12)
    p2.font.color.rgb = COLOR_NAVY_DARK

    add_notes(s13,
              "This investigation identifies three key limitations: reliance on a two-grid study, constant thermophysical property assumption, and clear-air transparency. Next steps will introduce a third mesh (800x320) to compute formal ASME VV 20 Grid Convergence Index error bands. In addition, an outlet enthalpy flux audit shows 0.41 W leaving in the fluid thermal plume out of 10.0 W applied heat, highlighting the need for an exhaustive global energy balance audit. Source: results/case_audit.csv.")

    # -------------------------------------------------------------
    # SLIDE 14: Closing & Academic Defense (Dark)
    # Authored by Jersam Lithin, Karunya Inst of Tech, Aerospace 3rd Yr, Boundary Layer Theory
    # Two dark navy cards: Presenter Dossier on left, Formal References on right
    # -------------------------------------------------------------
    s14 = prs.slides.add_slide(prs.slide_layouts[1]) # DARK_TITLE
    set_bg(s14, COLOR_NAVY_DARK)

    # Kicker
    k14 = s14.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.4))
    tf_k14 = k14.text_frame
    tf_k14.margin_left = tf_k14.margin_top = tf_k14.margin_right = tf_k14.margin_bottom = 0
    p = tf_k14.paragraphs[0]
    p.text = "CONCLUSION & ACADEMIC DEFENSE  |  BOUNDARY LAYER THEORY"
    p.font.name = FONT_BODY
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN

    # Conclusion Title
    t14 = s14.shapes.add_textbox(Inches(0.8), Inches(0.8), Inches(11.7), Inches(1.0))
    tf_t14 = t14.text_frame
    tf_t14.word_wrap = True
    tf_t14.margin_left = tf_t14.margin_top = tf_t14.margin_right = tf_t14.margin_bottom = 0
    p = tf_t14.paragraphs[0]
    p.text = "Coupled Surface Radiation Is Critical for Accurate Boundary Layer CFD"
    p.font.name = FONT_TITLE
    p.font.size = Pt(30)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE

    # The Ask
    ask14 = s14.shapes.add_textbox(Inches(0.8), Inches(1.85), Inches(11.7), Inches(0.5))
    tf_ask = ask14.text_frame
    tf_ask.word_wrap = True
    tf_ask.margin_left = tf_ask.margin_top = tf_ask.margin_right = tf_ask.margin_bottom = 0
    p = tf_ask.paragraphs[0]
    p.text = "Open for academic review, multi-grid GCI collaboration, and wind-tunnel experimental datasets."
    p.font.name = FONT_BODY
    p.font.size = Pt(15)
    p.font.color.rgb = COLOR_LIGHT_BG

    # Left Dark Card: Presenter & Academic Dossier
    add_card(s14, Inches(0.8), Inches(2.55), Inches(5.6), Inches(4.0), bg_color=COLOR_NAVY_CARD, border_color=None)
    pres_card = s14.shapes.add_textbox(Inches(1.1), Inches(2.75), Inches(5.0), Inches(3.6))
    tf_pc = pres_card.text_frame
    tf_pc.word_wrap = True
    tf_pc.margin_left = tf_pc.margin_top = 0

    p = tf_pc.paragraphs[0]
    p.text = "Presenter & Course Information"
    p.font.name = FONT_TITLE
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_ORANGE
    p.space_after = Pt(10)

    p_name = tf_pc.add_paragraph()
    p_name.text = "Jersam Lithin"
    p_name.font.name = FONT_TITLE
    p_name.font.size = Pt(24)
    p_name.font.bold = True
    p_name.font.color.rgb = COLOR_WHITE
    p_name.space_after = Pt(4)

    p_prog = tf_pc.add_paragraph()
    p_prog.text = "3rd Year B.Tech, Aerospace Engineering"
    p_prog.font.name = FONT_BODY
    p_prog.font.size = Pt(13)
    p_prog.font.color.rgb = COLOR_LIGHT_BG
    p_prog.space_after = Pt(2)

    p_inst = tf_pc.add_paragraph()
    p_inst.text = "Karunya Institute of Technology and Sciences"
    p_inst.font.name = FONT_BODY
    p_inst.font.size = Pt(13)
    p_inst.font.bold = True
    p_inst.font.color.rgb = COLOR_CYAN
    p_inst.space_after = Pt(2)

    p_dept = tf_pc.add_paragraph()
    p_dept.text = "Department of Aerospace Engineering"
    p_dept.font.name = FONT_BODY
    p_dept.font.size = Pt(12)
    p_dept.font.color.rgb = COLOR_SLATE
    p_dept.space_after = Pt(8)

    p_subj = tf_pc.add_paragraph()
    p_subj.text = "Subject Presentation: Boundary Layer Theory"
    p_subj.font.name = FONT_BODY
    p_subj.font.size = Pt(13)
    p_subj.font.bold = True
    p_subj.font.color.rgb = COLOR_AMBER
    p_subj.space_after = Pt(4)

    p_repo = tf_pc.add_paragraph()
    p_repo.text = "OpenFOAM Cases & Code: github.com/Jersam-l/flat-plate-with-radiation-cfd"
    p_repo.font.name = FONT_BODY
    p_repo.font.size = Pt(11)
    p_repo.font.color.rgb = COLOR_SLATE

    # Right Dark Card: Real Formal References list
    add_card(s14, Inches(6.7), Inches(2.55), Inches(5.8), Inches(4.0), bg_color=COLOR_NAVY_CARD, border_color=None)
    ref_box = s14.shapes.add_textbox(Inches(6.9), Inches(2.75), Inches(5.4), Inches(3.6))
    tf_ref = ref_box.text_frame
    tf_ref.word_wrap = True
    tf_ref.margin_left = tf_ref.margin_top = tf_ref.margin_right = tf_ref.margin_bottom = 0

    p = tf_ref.paragraphs[0]
    p.text = "Key Formal References"
    p.font.name = FONT_TITLE
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_AMBER
    p.space_after = Pt(8)

    references = [
        "1. Blasius, H. (1908). Grenzschichten in Flüssigkeiten mit kleiner Reibung. Z. Math. Phys., 56:1–37.",
        "2. Pohlhausen, E. (1921). Der Wärmeaustausch zwischen festen Körpern und Flüssigkeiten. ZAMM, 1:115–121.",
        "3. Incropera, F.P., DeWitt, D.P., Bergman, T.L., & Lavine, A.S. (2007). Fundamentals of Heat and Mass Transfer. 6th ed., Wiley.",
        "4. Reddy, P.B.A. (2014). Radiation effects on MHD boundary layer flow. J. Appl. Fluid Mech., 7(3):471–479.",
        "5. Raju, C.S.K., et al. (2026). Thermal radiation in boundary layers. Phys. Fluids.",
        "6. Schlichting, H., & Gersten, K. (2017). Boundary-Layer Theory. 9th ed., Springer."
    ]

    for ref in references:
        p = tf_ref.add_paragraph()
        p.text = ref
        p.font.name = FONT_BODY
        p.font.size = Pt(10)
        p.font.color.rgb = COLOR_LIGHT_BG
        p.space_after = Pt(4)

    # Footer contact & student info
    foot_box = s14.shapes.add_textbox(Inches(0.8), Inches(6.8), Inches(11.7), Inches(0.4))
    tf_foot = foot_box.text_frame
    tf_foot.margin_left = tf_foot.margin_top = tf_foot.margin_right = tf_foot.margin_bottom = 0
    p = tf_foot.paragraphs[0]
    p.text = "github.com/Jersam-l/flat-plate-with-radiation-cfd  |  Jersam Lithin  |  Karunya Institute of Technology and Sciences"
    p.font.name = FONT_BODY
    p.font.size = Pt(12)
    p.font.color.rgb = COLOR_SLATE

    add_notes(s14,
              "In conclusion, surface radiation dissipates over 21% of the input thermal load and cools the peak plate temperature by 6.98 K under laminar boundary layer flow. As an aerospace engineering student at Karunya Institute of Technology and Sciences presenting for Boundary Layer Theory, I welcome academic discussion on multi-grid GCI uncertainty quantification and physical experimental validation. Full simulation cases and scripts are available on GitHub. Source: github.com/Jersam-l/flat-plate-with-radiation-cfd.")

    print(f"Saving presentation to {OUTPUT_PPTX}...")
    prs.save(OUTPUT_PPTX)
    print("Presentation saved successfully!")


if __name__ == '__main__':
    create_deck()
