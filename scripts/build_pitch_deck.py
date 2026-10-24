#!/usr/bin/env python3
"""
build_pitch_deck.py
Generates the comprehensive, narrative-driven 14-slide academic presentation:
  Flat_Plate_Radiation_CFD_Pitch.pptx & Flat_Plate_Radiation_CFD_Pitch.pdf

Academic Project Details:
  Title: Boundary Layer on a Flat Plate with Radiation
  Presenter: JERSAM LITHIN L
  Register No: URK24AE1026
  Class: 3rd Year B.Tech, Aerospace Engineering
  Department: Department of Aerospace Engineering
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

# Design Tokens (Thermal Navy Theme from Pitch_Template.pptx)
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
    
    # 16:9 widescreen: 13.333 x 7.5 in
    prs.slide_width = Inches(13.333333)
    prs.slide_height = Inches(7.5)
    
    # Update running footer text on all slide layouts directly
    for layout in prs.slide_layouts:
        for shape in layout.shapes:
            if shape.has_text_frame and ('Flat-Plate' in shape.text_frame.text or 'Boundary Layer' in shape.text_frame.text):
                shape.text_frame.text = "Boundary Layer on a Flat Plate with Radiation  •  Jersam Lithin L (URK24AE1026)  •  Karunya"
                p = shape.text_frame.paragraphs[0]
                p.font.name = FONT_BODY
                p.font.size = Pt(11)
                p.font.color.rgb = COLOR_SLATE

    # Clear template dummy slides
    for i in range(len(prs.slides) - 1, -1, -1):
        rId = prs.slides._sldIdLst[i].rId
        prs.part.drop_rel(rId)
        del prs.slides._sldIdLst[i]
        
    print("Building 14 narrative story slides with prominent font sizes...")
    
    def set_bg(slide, color):
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = color

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

    def add_slide_num(slide, num, dark=False):
        num_box = slide.shapes.add_textbox(Inches(12.1), Inches(7.0), Inches(0.6), Inches(0.3))
        tf_n = num_box.text_frame
        tf_n.margin_left = tf_n.margin_top = tf_n.margin_right = tf_n.margin_bottom = 0
        p_n = tf_n.paragraphs[0]
        p_n.alignment = PP_ALIGN.RIGHT
        p_n.text = f"{num} / 14"
        p_n.font.name = FONT_BODY
        p_n.font.size = Pt(11)
        p_n.font.color.rgb = COLOR_SLATE

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
            fit_h = avail_h
            fit_w = fit_h * ar
            fit_top = card_top + pad_top
            fit_left = card_left + pad_x + (avail_w - fit_w) / 2
        else:
            fit_w = avail_w
            fit_h = fit_w / ar
            fit_left = card_left + pad_x
            fit_top = card_top + pad_top + (avail_h - fit_h) / 2

        slide.shapes.add_picture(img_path, fit_left, fit_top, fit_w, fit_h)

        cap_box = slide.shapes.add_textbox(card_left + pad_x, card_top + card_h - caption_h - Inches(0.12), card_w - (2 * pad_x), caption_h)
        tf = cap_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = caption_text
        p.font.name = FONT_BODY
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_SLATE

    def add_notes(slide, notes_text):
        notes_slide = slide.notes_slide
        tf = notes_slide.notes_text_frame
        tf.text = notes_text

    def add_bullet_list(tf, bullets, dark=False, font_size=16):
        assert len(bullets) <= 3, f"Too many bullets ({len(bullets)} > 3)"
        for i, text in enumerate(bullets):
            words = text.strip().split()
            assert len(words) <= 14, f"Bullet exceeds 14 words ({len(words)} words): '{text}'"
            if i == 0 and len(tf.paragraphs) == 1 and not tf.paragraphs[0].text:
                p = tf.paragraphs[0]
            else:
                p = tf.add_paragraph()
            p.text = f"•  {text}"
            p.font.name = FONT_BODY
            p.font.size = Pt(font_size)
            p.font.color.rgb = COLOR_WHITE if dark else COLOR_NAVY_DARK
            p.space_after = Pt(14)

    # =========================================================================
    # SLIDE 1: Title & Project Identification (Dark Navy)
    # =========================================================================
    s1 = prs.slides.add_slide(prs.slide_layouts[1])
    set_bg(s1, COLOR_NAVY_DARK)
    
    kicker_box = s1.shapes.add_textbox(Inches(0.8), Inches(0.8), Inches(6.8), Inches(0.4))
    tf_k = kicker_box.text_frame
    tf_k.margin_left = tf_k.margin_top = 0
    p = tf_k.paragraphs[0]
    p.text = "KARUNYA INSTITUTE OF TECHNOLOGY AND SCIENCES  •  AEROSPACE"
    p.font.name = FONT_BODY
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN

    t_box = s1.shapes.add_textbox(Inches(0.8), Inches(1.35), Inches(6.8), Inches(2.3))
    tf_t = t_box.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = tf_t.margin_top = 0
    p = tf_t.paragraphs[0]
    p.text = "Boundary Layer on a Flat Plate with Radiation"
    p.font.name = FONT_TITLE
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE

    sub_box = s1.shapes.add_textbox(Inches(0.8), Inches(3.85), Inches(6.8), Inches(0.9))
    tf_sub = sub_box.text_frame
    tf_sub.word_wrap = True
    tf_sub.margin_left = tf_sub.margin_top = 0
    p = tf_sub.paragraphs[0]
    p.text = "Coupled Surface Thermal Radiation Modeling in Laminar Boundary Layer Flows"
    p.font.name = FONT_BODY
    p.font.size = Pt(17)
    p.font.color.rgb = COLOR_LIGHT_BG

    pres_box = s1.shapes.add_textbox(Inches(0.8), Inches(4.95), Inches(6.8), Inches(2.0))
    tf_p = pres_box.text_frame
    tf_p.word_wrap = True
    tf_p.margin_left = tf_p.margin_top = 0
    
    p = tf_p.paragraphs[0]
    p.text = "JERSAM LITHIN L"
    p.font.name = FONT_TITLE
    p.font.size = Pt(26)
    p.font.bold = True
    p.font.color.rgb = COLOR_ORANGE
    p.space_after = Pt(3)

    p2 = tf_p.add_paragraph()
    p2.text = "Register No: URK24AE1026"
    p2.font.name = FONT_BODY
    p2.font.size = Pt(16)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_WHITE
    p2.space_after = Pt(3)

    p3 = tf_p.add_paragraph()
    p3.text = "3rd Year B.Tech, Aerospace Engineering  •  Department of Aerospace"
    p3.font.name = FONT_BODY
    p3.font.size = Pt(13)
    p3.font.color.rgb = COLOR_LIGHT_BG
    p3.space_after = Pt(2)

    p4 = tf_p.add_paragraph()
    p4.text = "Subject: Boundary Layer Theory  |  Course Project Presentation"
    p4.font.name = FONT_BODY
    p4.font.size = Pt(13)
    p4.font.color.rgb = COLOR_AMBER

    hero_path = os.path.join(FIG_DIR, 'four_case_temperature_zoom.png')
    hero_left = Inches(7.8)
    hero_top = Inches(1.1)
    hero_w = Inches(4.9)
    hero_h = Inches(5.3)
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

    cap_hero = s1.shapes.add_textbox(hero_left, fit_top + fit_h + Inches(0.1), hero_w, Inches(0.4))
    tf_ch = cap_hero.text_frame
    tf_ch.word_wrap = True
    tf_ch.margin_left = tf_ch.margin_top = 0
    p = tf_ch.paragraphs[0]
    p.text = "Fig. 1: Near-wall thermal boundary layer temperature fields across the 2 × 2 matrix."
    p.font.name = FONT_BODY
    p.font.size = Pt(12)
    p.font.color.rgb = COLOR_SLATE

    add_notes(s1,
              "Welcome. I am Jersam Lithin L, 3rd year Aerospace Engineering at Karunya Institute of Technology and Sciences. This project investigates coupled surface thermal radiation on a laminar flat-plate boundary layer using OpenFOAM 13. The hydrodynamic solver validates against exact Blasius similarity within 0.11%. Source: results/figures/four_case_temperature_zoom.png.")

    # =========================================================================
    # SLIDE 2: Problem Motivation — Trailing-Edge Resistance Rise (Light)
    # =========================================================================
    s2 = prs.slides.add_slide(prs.slide_layouts[2])
    set_bg(s2, COLOR_LIGHT_BG)
    add_title(s2, "The Trailing-Edge Problem: Convective Resistance Climbs Downstream")
    add_slide_num(s2, 2)
    
    add_contained_image(s2, Inches(0.6), Inches(1.5), Inches(7.2), Inches(5.2),
                        'wall_temperature_all_cases.png',
                        'Fig. 2: Streamwise wall temperature distribution along heated flat plate.')
    
    right_box = s2.shapes.add_textbox(Inches(8.2), Inches(1.6), Inches(4.5), Inches(3.4))
    tf_r2 = right_box.text_frame
    tf_r2.word_wrap = True
    tf_r2.margin_left = tf_r2.margin_top = 0
    
    p = tf_r2.paragraphs[0]
    p.text = "Convective Cooling Decays Downstream"
    p.font.name = FONT_TITLE
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY_DARK
    p.space_after = Pt(16)
    
    add_bullet_list(tf_r2, [
        "Plate wall temperature depends strictly on competing heat rejection pathways.",
        "Convective cooling drops downstream as hydrodynamic boundary layers thicken.",
        "Standard CFD workflows frequently omit radiation, overpredicting component peak temperatures."
    ], font_size=16)
    
    add_card(s2, Inches(8.2), Inches(5.2), Inches(4.5), Inches(1.2), bg_color=COLOR_WHITE, border_color=COLOR_BORDER)
    hc2 = s2.shapes.add_textbox(Inches(8.4), Inches(5.3), Inches(4.1), Inches(1.0))
    tf_hc2 = hc2.text_frame
    tf_hc2.word_wrap = True
    tf_hc2.margin_left = tf_hc2.margin_top = 0
    p = tf_hc2.paragraphs[0]
    p.text = "Heater Heat Flux: q″ = 1000 W/m²"
    p.font.name = FONT_TITLE
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = COLOR_ORANGE
    p2 = tf_hc2.add_paragraph()
    p2.text = "Uniform electric heating over 1.0 m plate with T_ambient = 300 K, U_inf = 2.0 m/s"
    p2.font.name = FONT_BODY
    p2.font.size = Pt(12)
    p2.font.color.rgb = COLOR_NAVY_DARK

    add_notes(s2,
              "In standard boundary layer heat transfer analyses, radiation is often neglected under the assumption that convection dominates. However, because local convective heat transfer coefficients decrease downstream proportional to x^(-0.5), convective resistance climbs toward the trailing edge. Radiation provides a crucial alternative heat path. Source: results/figures/wall_temperature_all_cases.png.")

    # =========================================================================
    # SLIDE 3: Aerospace & Thermal Systems Context (Light)
    # =========================================================================
    s3 = prs.slides.add_slide(prs.slide_layouts[2])
    set_bg(s3, COLOR_LIGHT_BG)
    add_title(s3, "Aerospace Context: When Convection Chokes, Radiation Dissipates")
    add_slide_num(s3, 3)

    add_contained_image(s3, Inches(0.6), Inches(1.5), Inches(7.2), Inches(5.2),
                        'research_paper_radiation_analogy.png',
                        'Fig. 3: Thermal resistance circuit showing convective and radiative pathways.')

    r3_box = s3.shapes.add_textbox(Inches(8.2), Inches(1.6), Inches(4.5), Inches(3.4))
    tf_r3 = r3_box.text_frame
    tf_r3.word_wrap = True
    tf_r3.margin_left = tf_r3.margin_top = 0
    p = tf_r3.paragraphs[0]
    p.text = "The Radiation Escape Hatch"
    p.font.name = FONT_TITLE
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY_DARK
    p.space_after = Pt(16)

    add_bullet_list(tf_r3, [
        "Aerospace skin cooling balances aerodynamic heating against atmospheric radiation emission.",
        "Avionics cold plates dissipate significant heat directly via grey surface radiation.",
        "Coupled solver captures non-linear radiation without heavy Monte Carlo computational overhead."
    ], font_size=16)

    add_card(s3, Inches(8.2), Inches(5.2), Inches(4.5), Inches(1.2), bg_color=COLOR_WHITE, border_color=COLOR_BORDER)
    hc3 = s3.shapes.add_textbox(Inches(8.4), Inches(5.3), Inches(4.1), Inches(1.0))
    tf_hc3 = hc3.text_frame
    tf_hc3.word_wrap = True
    tf_hc3.margin_left = tf_hc3.margin_top = 0
    p = tf_hc3.paragraphs[0]
    p.text = "Stefan-Boltzmann Quartic Law"
    p.font.name = FONT_TITLE
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN
    p2 = tf_hc3.add_paragraph()
    p2.text = "Radiation emission scales with (T_w⁴ − T_sur⁴), providing escalating relief as surface heats."
    p2.font.name = FONT_BODY
    p2.font.size = Pt(12)
    p2.font.color.rgb = COLOR_NAVY_DARK

    add_notes(s3,
              "In aerospace skin cooling and spacecraft thermal management, radiation acts as a parallel thermal path. When convective boundary layer resistance increases downstream, radiation emission carries a larger share of the thermal burden, stabilizing operating temperatures. Source: results/figures/research_paper_radiation_analogy.png.")

    # =========================================================================
    # SLIDE 4: Coupled Governing Equations & First-Law Closure (Light)
    # =========================================================================
    s4 = prs.slides.add_slide(prs.slide_layouts[2])
    set_bg(s4, COLOR_LIGHT_BG)
    add_title(s4, "Coupled Boundary Layer Formulation & First-Law Closure")
    add_slide_num(s4, 4)

    add_card(s4, Inches(0.6), Inches(1.5), Inches(6.8), Inches(5.2), bg_color=COLOR_WHITE)
    eq_box4 = s4.shapes.add_textbox(Inches(0.9), Inches(1.75), Inches(6.2), Inches(4.7))
    tf_eq4 = eq_box4.text_frame
    tf_eq4.word_wrap = True
    tf_eq4.margin_left = tf_eq4.margin_top = 0

    p = tf_eq4.paragraphs[0]
    p.text = "Governing Equations at Fluid-Solid Boundary"
    p.font.name = FONT_TITLE
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY_DARK
    p.space_after = Pt(12)

    p = tf_eq4.add_paragraph()
    p.text = "1. Navier-Stokes Momentum & Energy Equations:"
    p.font.name = FONT_BODY
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY_DARK
    p = tf_eq4.add_paragraph()
    p.text = "u ∂u/∂x + v ∂u/∂y = ν ∂²u/∂y²,   u ∂T/∂x + v ∂T/∂y = α ∂²T/∂y²"
    p.font.name = FONT_TITLE
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN
    p.space_after = Pt(10)

    p = tf_eq4.add_paragraph()
    p.text = "2. Conjugate Surface Energy Balance (Wall Boundary):"
    p.font.name = FONT_BODY
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY_DARK
    p = tf_eq4.add_paragraph()
    p.text = "q″_heater = −k (∂T/∂y)_wall + ε σ (T_w⁴ − T_sur⁴) = 1000 W/m²"
    p.font.name = FONT_TITLE
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_ORANGE
    p = tf_eq4.add_paragraph()
    p.text = "where ε = 0.80,  σ = 5.670 × 10⁻⁸ W/(m²·K⁴),  T_sur = 300 K"
    p.font.name = FONT_BODY
    p.font.size = Pt(12)
    p.font.color.rgb = COLOR_SLATE

    r4_title = s4.shapes.add_textbox(Inches(7.8), Inches(1.5), Inches(4.9), Inches(0.4))
    tf_r4t = r4_title.text_frame
    tf_r4t.margin_left = tf_r4t.margin_top = 0
    p = tf_r4t.paragraphs[0]
    p.text = "Conservation by Construction"
    p.font.name = FONT_TITLE
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY_DARK

    r4_box = s4.shapes.add_textbox(Inches(7.8), Inches(2.1), Inches(4.9), Inches(3.2))
    tf_r4 = r4_box.text_frame
    tf_r4.word_wrap = True
    tf_r4.margin_left = tf_r4.margin_top = 0
    add_bullet_list(tf_r4, [
        "Laminar Navier-Stokes fluid flow solved simultaneously with thermal energy transport.",
        "Surface radiation enters as a boundary heat flux balance at the wall.",
        "First-Law energy balance holds exactly at every finite volume cell face."
    ], font_size=16)

    add_notes(s4,
              "The governing equations consist of the steady laminar boundary layer equations with constant properties. The radiation boundary condition couples surface temperature to the external environment. First-Law energy conservation demands that total input electrical heat equals the sum of fluid conduction and net radiation at every single face. Source: cases/surfaceRadiation_fine/0/T.")

    # =========================================================================
    # SLIDE 5: In-Situ Newton-Raphson Wall Solver (Light)
    # =========================================================================
    s5 = prs.slides.add_slide(prs.slide_layouts[2])
    set_bg(s5, COLOR_LIGHT_BG)
    add_title(s5, "Numerical Implementation: In-Situ Newton-Raphson Wall Solver")
    add_slide_num(s5, 5)

    add_card(s5, Inches(0.6), Inches(1.5), Inches(6.8), Inches(5.2), bg_color=COLOR_WHITE)
    eq_box5 = s5.shapes.add_textbox(Inches(0.9), Inches(1.75), Inches(6.2), Inches(4.7))
    tf_eq5 = eq_box5.text_frame
    tf_eq5.word_wrap = True
    tf_eq5.margin_left = tf_eq5.margin_top = 0

    p = tf_eq5.paragraphs[0]
    p.text = "In-Situ Non-Linear Root Finding"
    p.font.name = FONT_TITLE
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY_DARK
    p.space_after = Pt(12)

    p = tf_eq5.add_paragraph()
    p.text = "1. Non-Linear Face Objective Function f(Tw) = 0:"
    p.font.name = FONT_BODY
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY_DARK
    p = tf_eq5.add_paragraph()
    p.text = "f(T_w) = −k (∂T/∂y)_w + ε σ (T_w⁴ − T_sur⁴) − q″_heater = 0"
    p.font.name = FONT_TITLE
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY_DARK
    p.space_after = Pt(10)

    p = tf_eq5.add_paragraph()
    p.text = "2. Analytical Derivative f′(Tw) > 0 (Monotonic):"
    p.font.name = FONT_BODY
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY_DARK
    p = tf_eq5.add_paragraph()
    p.text = "f′(T_w) = k / Δy₁ + 4 ε σ T_w³ > 0"
    p.font.name = FONT_TITLE
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN
    p.space_after = Pt(10)

    p = tf_eq5.add_paragraph()
    p.text = "3. Newton-Raphson Update Step:"
    p.font.name = FONT_BODY
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY_DARK
    p = tf_eq5.add_paragraph()
    p.text = "T_w,new = T_w,old − f(T_w) / f′(T_w)"
    p.font.name = FONT_TITLE
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_ORANGE

    r5_title = s5.shapes.add_textbox(Inches(7.8), Inches(1.5), Inches(4.9), Inches(0.4))
    tf_r5t = r5_title.text_frame
    tf_r5t.margin_left = tf_r5t.margin_top = 0
    p = tf_r5t.paragraphs[0]
    p.text = "Boundary Condition Mechanics"
    p.font.name = FONT_TITLE
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY_DARK

    r5_box = s5.shapes.add_textbox(Inches(7.8), Inches(2.05), Inches(4.9), Inches(2.2))
    tf_r5 = r5_box.text_frame
    tf_r5.word_wrap = True
    tf_r5.margin_left = tf_r5.margin_top = 0
    add_bullet_list(tf_r5, [
        "Solves non-linear quartic radiative flux at every boundary face.",
        "Enforces local face heat balance by construction during each PIMPLE step.",
        "Newton-Raphson scheme converges to double precision within four iterations."
    ], font_size=15)

    add_card(s5, Inches(7.8), Inches(4.8), Inches(2.35), Inches(1.9), bg_color=COLOR_WHITE, border_color=COLOR_BORDER)
    ch1 = s5.shapes.add_textbox(Inches(7.95), Inches(4.95), Inches(2.05), Inches(1.6))
    tf_ch1 = ch1.text_frame
    tf_ch1.margin_left = tf_ch1.margin_top = 0
    p = tf_ch1.paragraphs[0]
    p.text = "ε = 0.80"
    p.font.name = FONT_TITLE
    p.font.size = Pt(30)
    p.font.bold = True
    p.font.color.rgb = COLOR_ORANGE
    p2 = tf_ch1.add_paragraph()
    p2.text = "Grey-diffuse emissivity to 300 K external enclosure"
    p2.font.name = FONT_BODY
    p2.font.size = Pt(12)
    p2.font.color.rgb = COLOR_NAVY_DARK

    add_card(s5, Inches(10.35), Inches(4.8), Inches(2.35), Inches(1.9), bg_color=COLOR_WHITE, border_color=COLOR_BORDER)
    ch2 = s5.shapes.add_textbox(Inches(10.5), Inches(4.95), Inches(2.05), Inches(1.6))
    tf_ch2 = ch2.text_frame
    tf_ch2.margin_left = tf_ch2.margin_top = 0
    p = tf_ch2.paragraphs[0]
    p.text = "< 4 Iter"
    p.font.name = FONT_TITLE
    p.font.size = Pt(30)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN
    p2 = tf_ch2.add_paragraph()
    p2.text = "Fast quadratic convergence per boundary face"
    p2.font.name = FONT_BODY
    p2.font.size = Pt(12)
    p2.font.color.rgb = COLOR_NAVY_DARK

    add_notes(s5,
              "Because radiation depends on Tw to the fourth power, explicit evaluation would be numerically unstable. We implement an in-situ Newton-Raphson solver inside the OpenFOAM boundary condition. Because f-prime is strictly positive for positive temperatures, the scheme converges quadratically in fewer than four iterations. Source: cases/surfaceRadiation_fine/0/T.")

    # =========================================================================
    # SLIDE 6: Domain Architecture & 80:1 Inflation Mesh (Light)
    # =========================================================================
    s6 = prs.slides.add_slide(prs.slide_layouts[2])
    set_bg(s6, COLOR_LIGHT_BG)
    add_title(s6, "Domain Architecture & 80:1 Wall-Normal Inflation Mesh")
    add_slide_num(s6, 6)

    add_contained_image(s6, Inches(0.6), Inches(1.5), Inches(7.2), Inches(5.2),
                        'mesh_inflation_detail.png',
                        'Fig. 4: Structured inflation mesh near heated plate leading edge (80:1 grading).')

    r6_box = s6.shapes.add_textbox(Inches(8.2), Inches(1.6), Inches(4.5), Inches(3.4))
    tf_r6 = r6_box.text_frame
    tf_r6.word_wrap = True
    tf_r6.margin_left = tf_r6.margin_top = 0
    p = tf_r6.paragraphs[0]
    p.text = "Resolving the Thermal Sublayer"
    p.font.name = FONT_TITLE
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY_DARK
    p.space_after = Pt(16)

    add_bullet_list(tf_r6, [
        "Domain includes 1.0 m unheated inflow section to develop boundary layer.",
        "Geometric wall-normal grading of 80:1 concentrates 41 cells in 5 mm.",
        "Fine 64,000-cell mesh maintains zero non-orthogonality and skewness."
    ], font_size=16)

    add_card(s6, Inches(8.2), Inches(5.2), Inches(4.5), Inches(1.2), bg_color=COLOR_WHITE, border_color=COLOR_BORDER)
    hc6 = s6.shapes.add_textbox(Inches(8.4), Inches(5.3), Inches(4.1), Inches(1.0))
    tf_hc6 = hc6.text_frame
    tf_hc6.word_wrap = True
    tf_hc6.margin_left = tf_hc6.margin_top = 0
    p = tf_hc6.paragraphs[0]
    p.text = "First Cell Height: y₁ = 70.3 μm"
    p.font.name = FONT_TITLE
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = COLOR_ORANGE
    p2 = tf_hc6.add_paragraph()
    p2.text = "Places 41 structured cells inside the critical 5 mm thermal boundary layer."
    p2.font.name = FONT_BODY
    p2.font.size = Pt(12)
    p2.font.color.rgb = COLOR_NAVY_DARK

    add_notes(s6,
              "The domain geometry includes a 1.0 m unheated development section preceding the 1.0 m heated plate. This establishes a fully developed laminar Blasius velocity profile before heating begins. The 80:1 normal expansion ratio yields a first cell height of 70.3 micrometers, packing 41 cells inside the 5 mm boundary layer. Source: cases/surfaceRadiation_fine/system/blockMeshDict.")

    # =========================================================================
    # SLIDE 7: The 2 × 2 Factorial Simulation Matrix (Light)
    # =========================================================================
    s7 = prs.slides.add_slide(prs.slide_layouts[2])
    set_bg(s7, COLOR_LIGHT_BG)
    add_title(s7, "Systematic 2 × 2 Factorial Matrix: Isolating Physics from Discretization")
    add_slide_num(s7, 7)

    # 5-column Table
    t_shape7 = s7.shapes.add_table(5, 5, Inches(0.6), Inches(1.6), Inches(12.133), Inches(2.4))
    tbl7 = t_shape7.table
    tbl7.columns[0].width = Inches(3.3)
    tbl7.columns[1].width = Inches(2.0)
    tbl7.columns[2].width = Inches(2.0)
    tbl7.columns[3].width = Inches(2.4)
    tbl7.columns[4].width = Inches(2.4)

    headers7 = ["Case Identifier", "Grid (nx×ny)", "Total Cells", "Emissivity ε", "Trailing Tw (K)"]
    matrix_data7 = [
        ["noRadiation_coarse", "200 × 80", "16,000", "0.0 (Pure)", "394.90 K (+51.2 K spike)"],
        ["noRadiation_fine", "400 × 160", "64,000", "0.0 (Pure)", "343.68 K (Resolved)"],
        ["surfaceRadiation_coarse", "200 × 80", "16,000", "0.8 (Coupled)", "380.00 K (36% rad)"],
        ["surfaceRadiation_fine", "400 × 160", "64,000", "0.8 (Coupled)", "336.70 K (-6.98 K drop)"]
    ]

    for c_idx, h in enumerate(headers7):
        cell = tbl7.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_NAVY_DARK
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.name = FONT_BODY
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE
        p.alignment = PP_ALIGN.CENTER

    for r_idx, row in enumerate(matrix_data7):
        for c_idx, val in enumerate(row):
            cell = tbl7.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = COLOR_WHITE if r_idx % 2 == 0 else RGBColor(0xDE, 0xE5, 0xF0)
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.name = FONT_BODY
            p.font.size = Pt(13)
            p.font.color.rgb = COLOR_NAVY_DARK
            p.alignment = PP_ALIGN.LEFT if c_idx == 0 else PP_ALIGN.CENTER

    b_box7 = s7.shapes.add_textbox(Inches(0.6), Inches(4.3), Inches(12.133), Inches(2.2))
    tf_b7 = b_box7.text_frame
    tf_b7.word_wrap = True
    tf_b7.margin_left = tf_b7.margin_top = 0
    add_bullet_list(tf_b7, [
        "Coarse grid without radiation spikes to 394.90 K from under-resolved thermal gradients.",
        "Fine mesh captures steep wall conduction gradient, stabilizing at 343.68 K.",
        "Coupled surface radiation provides additional cooling, dropping trailing temperature to 336.70 K."
    ], font_size=16)

    add_notes(s7,
              "Our investigation executes a rigorous 2 by 2 factorial matrix. Comparing noRadiation_fine against surfaceRadiation_fine quantifies the pure physics of surface radiation: a 6.98 K temperature drop and 21.56% radiative offloading. Comparing coarse against fine discloses numerical discretization sensitivity. Source: results/case_audit.csv.")

    # =========================================================================
    # SLIDE 8: Hydrodynamic Verification — Blasius Similarity (Dark Navy)
    # =========================================================================
    s8 = prs.slides.add_slide(prs.slide_layouts[3])
    set_bg(s8, COLOR_NAVY_DARK)
    add_title(s8, "Hydrodynamic Verification: Exact Collapse on Blasius Similarity", dark=True)
    add_slide_num(s8, 8, dark=True)

    add_contained_image(s8, Inches(0.6), Inches(1.5), Inches(7.2), Inches(5.2),
                        'blasius_velocity_validation.png',
                        'Fig. 5: Non-dimensional streamwise velocity collapse vs exact Blasius curve.',
                        dark_card=True)

    chips_data_8 = [
        ("0.11%", COLOR_ORANGE, "Skin-friction relative error vs Blasius (Cf = 1.874e-3 vs 1.872e-3)"),
        ("1.26 × 10⁵", COLOR_CYAN, "Plate Reynolds number (Re_L = U_inf L / ν) confirms laminar flow"),
        ("8.17 mm", COLOR_AMBER, "Boundary layer thickness matches analytical Blasius law δ = 5.0 x / √Re_x")
    ]
    for idx, (val, col, desc) in enumerate(chips_data_8):
        top_y = Inches(1.5 + idx * 1.75)
        add_card(s8, Inches(8.2), top_y, Inches(4.5), Inches(1.55), bg_color=COLOR_NAVY_CARD, border_color=None)
        box = s8.shapes.add_textbox(Inches(8.5), top_y + Inches(0.18), Inches(3.9), Inches(1.2))
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
        p2.font.size = Pt(13)
        p2.font.color.rgb = COLOR_LIGHT_BG

    add_notes(s8,
              "Hydrodynamic solver accuracy is rigorously validated against the classical Blasius similarity solution. Trailing-edge skin friction matches analytical prediction with 0.11% relative error. All velocity profiles across different x-stations collapse onto the theoretical curve, giving complete confidence in the momentum solution. Source: results/figures/blasius_velocity_validation.png.")

    # =========================================================================
    # SLIDE 9: Hydrodynamic Decoupling — Velocity Invariance (Dark Navy)
    # =========================================================================
    s9 = prs.slides.add_slide(prs.slide_layouts[3])
    set_bg(s9, COLOR_NAVY_DARK)
    add_title(s9, "Momentum Decoupling: Velocity Invariant Under Radiation", dark=True)
    add_slide_num(s9, 9, dark=True)

    add_contained_image(s9, Inches(0.6), Inches(1.5), Inches(7.2), Inches(5.2),
                        'four_case_velocity_zoom.png',
                        'Fig. 6: Streamwise velocity boundary layer zoom across all four cases.',
                        dark_card=True)

    chips_data_9 = [
        ("Identical", COLOR_CYAN, "Velocity field u(x,y) unchanged between ε = 0 and ε = 0.8"),
        ("< 0.08 Pa", COLOR_ORANGE, "Streamwise pressure deviation remains negligible across domain"),
        ("Decoupled", COLOR_AMBER, "Constant air properties cleanly isolate thermal radiation physics")
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
        p2.font.size = Pt(13)
        p2.font.color.rgb = COLOR_LIGHT_BG

    add_notes(s9,
              "Because fluid transport properties are constant and buoyancy is absent, the momentum equation is decoupled from the energy equation. As shown in the figure, the velocity boundary layers are completely identical between the radiating and non-radiating cases. This cleanly isolates the thermal radiation coupling mechanism. Source: results/figures/four_case_velocity_zoom.png.")

    # =========================================================================
    # SLIDE 10: Thermal Discovery — Near-Wall Isotherm Suppression (Light)
    # =========================================================================
    s10 = prs.slides.add_slide(prs.slide_layouts[2])
    set_bg(s10, COLOR_LIGHT_BG)
    add_title(s10, "Thermal Boundary Layer Response: Direct Isotherm Suppression")
    add_slide_num(s10, 10)

    add_contained_image(s10, Inches(0.6), Inches(1.5), Inches(7.2), Inches(5.2),
                        'four_case_temperature_zoom.png',
                        'Fig. 7: Near-wall thermal boundary layer zoom across the four cases.')

    r10_box = s10.shapes.add_textbox(Inches(8.2), Inches(1.6), Inches(4.5), Inches(3.4))
    tf_r10 = r10_box.text_frame
    tf_r10.word_wrap = True
    tf_r10.margin_left = tf_r10.margin_top = 0
    p = tf_r10.paragraphs[0]
    p.text = "Direct Isotherm Suppression"
    p.font.name = FONT_TITLE
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY_DARK
    p.space_after = Pt(16)

    add_bullet_list(tf_r10, [
        "Radiation suppresses near-wall temperature contours across the entire heated length.",
        "Thermal boundary layer thickness remains virtually invariant (5.07 mm vs 5.18 mm).",
        "Demonstrates radiation acts as an in-situ heat shunt without disturbing boundary structure."
    ], font_size=16)

    add_card(s10, Inches(8.2), Inches(5.2), Inches(4.5), Inches(1.2), bg_color=COLOR_WHITE, border_color=COLOR_BORDER)
    hc10 = s10.shapes.add_textbox(Inches(8.4), Inches(5.3), Inches(4.1), Inches(1.0))
    tf_hc10 = hc10.text_frame
    tf_hc10.word_wrap = True
    tf_hc10.margin_left = tf_hc10.margin_top = 0
    p = tf_hc10.paragraphs[0]
    p.text = "Near-Wall Sublayer Relief"
    p.font.name = FONT_TITLE
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = COLOR_ORANGE
    p2 = tf_hc10.add_paragraph()
    p2.text = "Near-wall conductive gradient is relieved as 21.6% of heat radiates to surroundings."
    p2.font.name = FONT_BODY
    p2.font.size = Pt(12)
    p2.font.color.rgb = COLOR_NAVY_DARK

    add_notes(s10,
              "Looking at the near-wall temperature contours, we observe clear isotherm suppression in the radiating cases. Crucially, the outer boundary layer thickness does not thin; delta-T-99 is 5.07 mm without radiation and 5.17 mm with radiation. Radiation offloads heat at the surface without disrupting boundary layer structure. Source: results/figures/four_case_temperature_zoom.png.")

    # =========================================================================
    # SLIDE 11: Quantitative Temperature Drop — 6.98 K Cooling (Light)
    # =========================================================================
    s11 = prs.slides.add_slide(prs.slide_layouts[2])
    set_bg(s11, COLOR_LIGHT_BG)
    add_title(s11, "Surface Temperature Depression: Peak 6.98 K Cooling at Trailing Edge")
    add_slide_num(s11, 11)

    add_contained_image(s11, Inches(0.6), Inches(1.5), Inches(7.2), Inches(5.2),
                        'temperature_difference_zoom.png',
                        'Fig. 8: Boundary layer temperature difference field (T_radiation - T_baseline).')

    add_card(s11, Inches(8.2), Inches(1.5), Inches(4.5), Inches(1.5), bg_color=COLOR_WHITE, border_color=COLOR_BORDER)
    c11_box = s11.shapes.add_textbox(Inches(8.4), Inches(1.6), Inches(4.1), Inches(1.3))
    tf_c11 = c11_box.text_frame
    tf_c11.word_wrap = True
    tf_c11.margin_left = tf_c11.margin_top = 0
    p = tf_c11.paragraphs[0]
    p.text = "6.98 K Drop"
    p.font.name = FONT_TITLE
    p.font.size = Pt(38)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN
    p2 = tf_c11.add_paragraph()
    p2.text = "Peak Wall Temperature Reduction (Fine Grid)"
    p2.font.name = FONT_BODY
    p2.font.size = Pt(14)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_NAVY_DARK

    b11_box = s11.shapes.add_textbox(Inches(8.2), Inches(3.3), Inches(4.5), Inches(2.6))
    tf_b11 = b11_box.text_frame
    tf_b11.word_wrap = True
    tf_b11.margin_left = tf_b11.margin_top = 0
    add_bullet_list(tf_b11, [
        "Radiation lowers plate wall temperature along the entire heated length.",
        "Cooling effect intensifies downstream, reaching maximum depression of 6.98 K.",
        "Thermal boundary layer thickness remains virtually unchanged across radiation cases."
    ], font_size=15)

    p_fn = tf_b11.add_paragraph()
    p_fn.space_before = Pt(8)
    p_fn.text = "Fine grid trailing edge: 336.70 K vs 343.68 K pure convection."
    p_fn.font.name = FONT_BODY
    p_fn.font.size = Pt(12)
    p_fn.font.color.rgb = COLOR_SLATE

    add_notes(s11,
              "By directly subtracting the non-radiating temperature field from the radiating field, we obtain the spatial cooling footprint. The temperature depression starts at approximately -1.2 K near the leading edge and intensifies downstream, reaching -6.98 K at the trailing edge. This proves that radiation is most effective precisely where convection is weakest. Source: results/figures/temperature_difference_zoom.png.")

    # =========================================================================
    # SLIDE 12: Heat Flux Partitioning — Convection vs Radiation (Light)
    # =========================================================================
    s12 = prs.slides.add_slide(prs.slide_layouts[2])
    set_bg(s12, COLOR_LIGHT_BG)
    add_title(s12, "Streamwise Heat Flux Partitioning: Radiation Carries 21.6% of Load")
    add_slide_num(s12, 12)

    add_contained_image(s12, Inches(0.6), Inches(1.5), Inches(7.2), Inches(5.2),
                        'wall_heat_balance_and_nusselt.png',
                        'Fig. 9: Streamwise convective vs radiative heat-flux split and Nusselt number.')

    add_card(s12, Inches(8.2), Inches(1.5), Inches(4.5), Inches(1.4), bg_color=COLOR_WHITE, border_color=COLOR_BORDER)
    kpi1 = s12.shapes.add_textbox(Inches(8.4), Inches(1.6), Inches(4.1), Inches(1.2))
    tf_k1 = kpi1.text_frame
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

    add_card(s12, Inches(8.2), Inches(3.05), Inches(4.5), Inches(1.4), bg_color=COLOR_WHITE, border_color=COLOR_BORDER)
    kpi2 = s12.shapes.add_textbox(Inches(8.4), Inches(3.15), Inches(4.1), Inches(1.2))
    tf_k2 = kpi2.text_frame
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

    b12_box = s12.shapes.add_textbox(Inches(8.2), Inches(4.65), Inches(4.5), Inches(2.0))
    tf_b12 = b12_box.text_frame
    tf_b12.word_wrap = True
    tf_b12.margin_left = tf_b12.margin_top = 0
    add_bullet_list(tf_b12, [
        "Surface radiation relieves over one-fifth of the total heat dissipation load.",
        "Radiative heat flux remains nearly uniform along the entire plate surface.",
        "Convective flux drops downstream as thermal boundary layer growth increases resistance."
    ], font_size=14)

    add_notes(s12,
              "On the fine 64,000-cell mesh, surface radiation dissipates an integrated plate-averaged flux of 213.2 W/m² (21.32% of total heat), rising to 21.56% (215.59 W/m²) at the trailing edge. Convective flux steadily declines downstream, while radiative flux stays virtually uniform. The sum strictly closes to 1000.00 W/m² at every face. Source: results/figures/wall_heat_balance_and_nusselt.png.")

    # =========================================================================
    # SLIDE 13: Numerical Rigor — Grid Convergence & Residuals (Dark Navy)
    # =========================================================================
    s13 = prs.slides.add_slide(prs.slide_layouts[3])
    set_bg(s13, COLOR_NAVY_DARK)
    add_title(s13, "Numerical Rigor: Grid Convergence and Solver Stability", dark=True)
    add_slide_num(s13, 13, dark=True)

    add_contained_image(s13, Inches(0.6), Inches(1.5), Inches(7.2), Inches(5.2),
                        'convergence_histories_all4.png',
                        'Fig. 10: Solver residual histories for p, U, and T across all four cases.',
                        dark_card=True)

    chips_data_13 = [
        ("1.30 × 10⁻⁸", COLOR_CYAN, "Continuity residual confirms deep monotonic convergence"),
        ("1500 Iter", COLOR_ORANGE, "PIMPLE outer iterations achieve complete steady-state stability"),
        ("41 Cells", COLOR_AMBER, "Structured cells inside 5 mm sublayer accurately resolve wall flux")
    ]
    for idx, (val, col, desc) in enumerate(chips_data_13):
        top_y = Inches(1.5 + idx * 1.75)
        add_card(s13, Inches(8.2), top_y, Inches(4.5), Inches(1.55), bg_color=COLOR_NAVY_CARD, border_color=None)
        box = s13.shapes.add_textbox(Inches(8.5), top_y + Inches(0.18), Inches(3.9), Inches(1.2))
        tf = box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = 0
        p = tf.paragraphs[0]
        p.text = val
        p.font.name = FONT_TITLE
        p.font.size = Pt(34)
        p.font.bold = True
        p.font.color.rgb = col
        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.name = FONT_BODY
        p2.font.size = Pt(13)
        p2.font.color.rgb = COLOR_LIGHT_BG

    add_notes(s13,
              "Numerical rigor was audited across all runs. Linear solver residuals for pressure, velocity, and enthalpy all converge smoothly below 10⁻⁸ within 1500 iterations. The grid comparison highlights the importance of near-wall inflation: without sufficient resolution in the first 5 mm, conductive wall flux is miscalculated. Source: results/figures/convergence_histories_all4.png.")

    # =========================================================================
    # SLIDE 14: Project Conclusion & Academic Dossier (Dark Navy)
    # =========================================================================
    s14 = prs.slides.add_slide(prs.slide_layouts[1])
    set_bg(s14, COLOR_NAVY_DARK)

    k14 = s14.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.4))
    tf_k14 = k14.text_frame
    tf_k14.margin_left = tf_k14.margin_top = 0
    p = tf_k14.paragraphs[0]
    p.text = "PROJECT CONCLUSION & ACADEMIC DOSSIER  •  BOUNDARY LAYER THEORY"
    p.font.name = FONT_BODY
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN

    t14 = s14.shapes.add_textbox(Inches(0.8), Inches(0.8), Inches(11.7), Inches(1.0))
    tf_t14 = t14.text_frame
    tf_t14.word_wrap = True
    tf_t14.margin_left = tf_t14.margin_top = 0
    p = tf_t14.paragraphs[0]
    p.text = "Coupled Surface Radiation Is Critical for Accurate Boundary Layer CFD"
    p.font.name = FONT_TITLE
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE

    ask14 = s14.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.7), Inches(0.55))
    tf_ask14 = ask14.text_frame
    tf_ask14.word_wrap = True
    tf_ask14.margin_left = tf_ask14.margin_top = 0
    p = tf_ask14.paragraphs[0]
    p.text = "Objective Achieved: Successfully incorporated surface radiation and quantified its thermal boundary layer impact."
    p.font.name = FONT_BODY
    p.font.size = Pt(16)
    p.font.color.rgb = COLOR_LIGHT_BG

    add_card(s14, Inches(0.8), Inches(2.55), Inches(5.6), Inches(4.0), bg_color=COLOR_NAVY_CARD, border_color=None)
    find_card = s14.shapes.add_textbox(Inches(1.1), Inches(2.75), Inches(5.0), Inches(3.6))
    tf_fc = find_card.text_frame
    tf_fc.word_wrap = True
    tf_fc.margin_left = tf_fc.margin_top = 0

    p = tf_fc.paragraphs[0]
    p.text = "Key Findings & Numerical Insights"
    p.font.name = FONT_TITLE
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_ORANGE
    p.space_after = Pt(8)

    p_f1 = tf_fc.add_paragraph()
    p_f1.text = "1. Surface Radiation Impact:"
    p_f1.font.name = FONT_BODY
    p_f1.font.size = Pt(14)
    p_f1.font.bold = True
    p_f1.font.color.rgb = COLOR_WHITE
    p_f1_sub = tf_fc.add_paragraph()
    p_f1_sub.text = "Relieves 21.56% of total heat flux and cools peak wall by 6.98 K (336.70 K vs 343.68 K)."
    p_f1_sub.font.name = FONT_BODY
    p_f1_sub.font.size = Pt(12)
    p_f1_sub.font.color.rgb = COLOR_LIGHT_BG
    p_f1_sub.space_after = Pt(6)

    p_f2 = tf_fc.add_paragraph()
    p_f2.text = "2. Grid Sensitivity Disclosed:"
    p_f2.font.name = FONT_BODY
    p_f2.font.size = Pt(14)
    p_f2.font.bold = True
    p_f2.font.color.rgb = COLOR_CYAN
    p_f2_sub = tf_fc.add_paragraph()
    p_f2_sub.text = "Coarse (16k) overpredicts wall rise (394.9 K); fine grid (64k) resolves sublayer gradient."
    p_f2_sub.font.name = FONT_BODY
    p_f2_sub.font.size = Pt(12)
    p_f2_sub.font.color.rgb = COLOR_LIGHT_BG
    p_f2_sub.space_after = Pt(6)

    p_f3 = tf_fc.add_paragraph()
    p_f3.text = "3. Future Scope & Refinement:"
    p_f3.font.name = FONT_BODY
    p_f3.font.size = Pt(14)
    p_f3.font.bold = True
    p_f3.font.color.rgb = COLOR_AMBER
    p_f3_sub = tf_fc.add_paragraph()
    p_f3_sub.text = "Execute 3rd Richardson mesh for ASME GCI and incorporate variable air properties."
    p_f3_sub.font.name = FONT_BODY
    p_f3_sub.font.size = Pt(12)
    p_f3_sub.font.color.rgb = COLOR_LIGHT_BG

    add_card(s14, Inches(6.7), Inches(2.55), Inches(5.8), Inches(4.0), bg_color=COLOR_NAVY_CARD, border_color=None)
    cred_card = s14.shapes.add_textbox(Inches(6.9), Inches(2.75), Inches(5.4), Inches(3.6))
    tf_cc = cred_card.text_frame
    tf_cc.word_wrap = True
    tf_cc.margin_left = tf_cc.margin_top = 0

    p = tf_cc.paragraphs[0]
    p.text = "Student Credentials & References"
    p.font.name = FONT_TITLE
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_AMBER
    p.space_after = Pt(8)

    p_name = tf_cc.add_paragraph()
    p_name.text = "JERSAM LITHIN L"
    p_name.font.name = FONT_TITLE
    p_name.font.size = Pt(24)
    p_name.font.bold = True
    p_name.font.color.rgb = COLOR_WHITE

    p_reg = tf_cc.add_paragraph()
    p_reg.text = "Register No: URK24AE1026"
    p_reg.font.name = FONT_BODY
    p_reg.font.size = Pt(15)
    p_reg.font.bold = True
    p_reg.font.color.rgb = COLOR_CYAN

    p_dept = tf_cc.add_paragraph()
    p_dept.text = "3rd Year B.Tech, Aerospace Engineering  •  Karunya Institute of Tech"
    p_dept.font.name = FONT_BODY
    p_dept.font.size = Pt(13)
    p_dept.font.color.rgb = COLOR_LIGHT_BG

    p_subj = tf_cc.add_paragraph()
    p_subj.text = "Subject: Boundary Layer Theory  |  Course Project Presentation"
    p_subj.font.name = FONT_BODY
    p_subj.font.size = Pt(13)
    p_subj.font.color.rgb = COLOR_AMBER
    p_subj.space_after = Pt(10)

    p_ref = tf_cc.add_paragraph()
    p_ref.text = "Full OpenFOAM 13 cases, mesh scripts, and 61 figures preserved at:"
    p_ref.font.name = FONT_BODY
    p_ref.font.size = Pt(12)
    p_ref.font.color.rgb = COLOR_SLATE
    p_url = tf_cc.add_paragraph()
    p_url.text = "github.com/Jersam-l/flat-plate-with-radiation-cfd"
    p_url.font.name = FONT_BODY
    p_url.font.size = Pt(13)
    p_url.font.bold = True
    p_url.font.color.rgb = COLOR_WHITE

    add_notes(s14,
              "In conclusion, this project fulfills our Boundary Layer Theory course objectives: we successfully coupled non-linear surface radiation to a laminar boundary layer in OpenFOAM 13, demonstrated a 6.98 K temperature drop and 21.56% radiative offloading, and validated the momentum solver against Blasius within 0.11%. Thank you for your attention. Source: README.md, Flat_Plate_Radiation_CFD_Pitch.pdf.")

    prs.save(OUTPUT_PPTX)
    print(f"Successfully generated {OUTPUT_PPTX} with 14 story slides.")


if __name__ == '__main__':
    create_deck()
