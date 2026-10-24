#!/usr/bin/env python3
"""
build_pitch_deck.py
Generates the 14-slide academic presentation matching Section 3 of the prompt:
  Flat_Plate_Radiation_CFD_Pitch.pptx & Flat_Plate_Radiation_CFD_Pitch.pdf

Adheres strictly to the design system:
  - Fonts: Cambria for titles/stats, Calibri for body/tables
  - Colors: Thermal Navy (0B1426, 16264A), Light BG (EEF2F7), White (FFFFFF),
            Orange (FF7A1A), Cyan (23B5D3), Amber (FFC24B), Slate (7C8DB5), Red (E5484D)
  - Layout: 16:9 widescreen (13.333 x 7.5 in)
  - Native tables, contained figures, cards, prominent typography
  - Maximum 3 bullets per slide, maximum 12 words per bullet
  - Speaker notes with >= 2 sentences and 'Source:' reference on every slide
"""

import os
import sys
from PIL import Image
import pptx
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor

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
    
    prs.slide_width = Inches(13.333333)
    prs.slide_height = Inches(7.5)
    
    # Update running footer text on layouts
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
        
    print("Building 14 aerospace technical review slides...")
    
    def set_bg(slide, color):
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = color

    def add_title(slide, title_text, dark=False):
        tx_box = slide.shapes.add_textbox(Inches(0.6), Inches(0.4), Inches(12.133), Inches(0.85))
        tf = tx_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.name = FONT_TITLE
        p.font.size = Pt(30)
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

        pad_x = Inches(0.18)
        pad_top = Inches(0.15)
        caption_h = Inches(0.32)
        avail_w = card_w - (2 * pad_x)
        avail_h = card_h - pad_top - caption_h - Inches(0.15)

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

        cap_box = slide.shapes.add_textbox(card_left + pad_x, card_top + card_h - caption_h - Inches(0.1), card_w - (2 * pad_x), caption_h)
        tf = cap_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = caption_text
        p.font.name = FONT_BODY
        p.font.size = Pt(11)
        p.font.color.rgb = COLOR_SLATE

    def add_notes(slide, notes_text):
        notes_slide = slide.notes_slide
        tf = notes_slide.notes_text_frame
        tf.text = notes_text

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

    # =========================================================================
    # SLIDE 1: Title (Dark Navy)
    # =========================================================================
    s1 = prs.slides.add_slide(prs.slide_layouts[1])
    set_bg(s1, COLOR_NAVY_DARK)
    
    kicker_box = s1.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(6.8), Inches(0.4))
    tf_k = kicker_box.text_frame
    tf_k.margin_left = tf_k.margin_top = 0
    p = tf_k.paragraphs[0]
    p.text = "KARUNYA INSTITUTE OF TECHNOLOGY AND SCIENCES  •  AEROSPACE"
    p.font.name = FONT_BODY
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN

    t_box = s1.shapes.add_textbox(Inches(0.8), Inches(1.2), Inches(6.8), Inches(2.2))
    tf_t = t_box.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = tf_t.margin_top = 0
    p = tf_t.paragraphs[0]
    p.text = "Boundary Layer Over a Heated Flat Plate with Surface Radiation"
    p.font.name = FONT_TITLE
    p.font.size = Pt(34)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE

    sub_box = s1.shapes.add_textbox(Inches(0.8), Inches(3.6), Inches(6.8), Inches(0.8))
    tf_sub = sub_box.text_frame
    tf_sub.word_wrap = True
    tf_sub.margin_left = tf_sub.margin_top = 0
    p = tf_sub.paragraphs[0]
    p.text = "OpenFOAM 13 | Steady Laminar Forced Convection | Grey-Diffuse Surface Radiation"
    p.font.name = FONT_BODY
    p.font.size = Pt(15)
    p.font.color.rgb = COLOR_LIGHT_BG

    pres_box = s1.shapes.add_textbox(Inches(0.8), Inches(4.7), Inches(6.8), Inches(2.2))
    tf_p = pres_box.text_frame
    tf_p.word_wrap = True
    tf_p.margin_left = tf_p.margin_top = 0
    
    p = tf_p.paragraphs[0]
    p.text = "Jersam Lithin L"
    p.font.name = FONT_TITLE
    p.font.size = Pt(26)
    p.font.bold = True
    p.font.color.rgb = COLOR_ORANGE
    p.space_after = Pt(2)

    p2 = tf_p.add_paragraph()
    p2.text = "Register No.: URK24AE1026"
    p2.font.name = FONT_BODY
    p2.font.size = Pt(15)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_WHITE
    p2.space_after = Pt(2)

    p3 = tf_p.add_paragraph()
    p3.text = "B.Tech Aerospace Engineering"
    p3.font.name = FONT_BODY
    p3.font.size = Pt(13)
    p3.font.color.rgb = COLOR_LIGHT_BG
    p3.space_after = Pt(2)

    p4 = tf_p.add_paragraph()
    p4.text = "Karunya Institute of Technology and Sciences"
    p4.font.name = FONT_BODY
    p4.font.size = Pt(13)
    p4.font.color.rgb = COLOR_AMBER

    add_contained_image(s1, Inches(7.8), Inches(1.1), Inches(4.9), Inches(5.6), 'four_case_temperature_zoom.png', 'Fig. 1: Near-wall temperature contours across cases.', dark_card=True)
    add_slide_num(s1, 1, dark=True)
    add_notes(s1, "This review presents our OpenFOAM 13 simulation of laminar convection with radiation. Source: cases/surfaceRadiation_fine/0/T and results/figures/four_case_temperature_zoom.png.")

    # =========================================================================
    # SLIDE 2: Problem Definition (Light)
    # =========================================================================
    s2 = prs.slides.add_slide(prs.slide_layouts[1])
    set_bg(s2, COLOR_LIGHT_BG)
    add_title(s2, "Problem Definition and Test Matrix", dark=False)
    add_contained_image(s2, Inches(0.6), Inches(1.4), Inches(6.5), Inches(5.4), 'wall_temperature_all_cases.png', 'Fig. 2: Streamwise wall temperature distribution along plate.')

    # Right Card: Question & Matrix
    add_card(s2, Inches(7.4), Inches(1.4), Inches(5.3), Inches(5.4))
    q_box = s2.shapes.add_textbox(Inches(7.7), Inches(1.6), Inches(4.7), Inches(1.3))
    tf_q = q_box.text_frame
    tf_q.word_wrap = True
    tf_q.margin_left = tf_q.margin_top = 0
    p = tf_q.paragraphs[0]
    p.text = "Core Engineering Question:"
    p.font.name = FONT_BODY
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_SLATE
    p2 = tf_q.add_paragraph()
    p2.text = "How does surface radiation change wall temperature under fixed flux?"
    p2.font.name = FONT_TITLE
    p2.font.size = Pt(19)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_ORANGE

    b_box = s2.shapes.add_textbox(Inches(7.7), Inches(3.1), Inches(4.7), Inches(2.3))
    tf_b = b_box.text_frame
    tf_b.word_wrap = True
    tf_b.margin_left = tf_b.margin_top = 0
    bullets_s2 = [
        "Compares emissivity levels of 0.0 and 0.8 across meshes.",
        "Evaluates 16,000-cell coarse and 64,000-cell fine structured grids.",
        "Assumes low-speed, constant-property air flow without buoyancy.",
    ]
    add_bullet_list(tf_b, bullets_s2, dark=False, font_size=15)

    c_box = s2.shapes.add_textbox(Inches(7.7), Inches(5.6), Inches(4.7), Inches(0.9))
    tf_c = c_box.text_frame
    tf_c.word_wrap = True
    tf_c.margin_left = tf_c.margin_top = 0
    p = tf_c.paragraphs[0]
    p.text = "Scope: Low-speed constant-property CFD. Not hypersonic or validated TPS."
    p.font.name = FONT_BODY
    p.font.size = Pt(12)
    p.font.color.rgb = COLOR_RED
    p.font.bold = True

    add_slide_num(s2, 2, dark=False)
    add_notes(s2, "The simulation compares emissivity levels and mesh resolutions under uniform heating. It assumes low-speed laminar air flow. Source: cases/template/caseParameters.txt and results/case_audit.csv.")

    # =========================================================================
    # SLIDE 3: Geometry and Input Parameters (Light)
    # =========================================================================
    s3 = prs.slides.add_slide(prs.slide_layouts[1])
    set_bg(s3, COLOR_LIGHT_BG)
    add_title(s3, "Geometry and Input Parameters", dark=False)
    add_contained_image(s3, Inches(0.6), Inches(1.4), Inches(5.6), Inches(5.4), 'mesh_full_domain.png', 'Fig. 3: Computational domain schematic (L = 1.0 m, H = 0.20 m).')

    # Native Table on Right
    table_card = add_card(s3, Inches(6.5), Inches(1.4), Inches(6.2), Inches(5.4))
    t_shape = s3.shapes.add_table(13, 3, Inches(6.7), Inches(1.55), Inches(5.8), Inches(5.0))
    table = t_shape.table
    table.columns[0].width = Inches(3.2)
    table.columns[1].width = Inches(1.6)
    table.columns[2].width = Inches(1.0)

    params_data = [
        ("Parameter", "Value", "Unit"),
        ("Plate length, L", "1.0", "m"),
        ("Domain height, H", "0.20", "m"),
        ("Inlet velocity, U_inf", "2.0", "m/s"),
        ("Inlet temperature, T_inf", "300.0", "K"),
        ("Surroundings temperature, T_sur", "300.0", "K"),
        ("Reference pressure, p_ref", "100.0", "kPa"),
        ("Applied heater flux, q''_heater", "1000.0", "W/m²"),
        ("Dynamic viscosity, mu", "1.846 x 10^-5", "kg/(m s)"),
        ("Thermal conductivity, k", "0.02613", "W/(m K)"),
        ("Specific heat capacity, cp", "1005.0", "J/(kg K)"),
        ("Prandtl number, Pr", "0.71", "—"),
        ("Density, rho", "1.1614", "kg/m³"),
    ]
    for r_idx, row in enumerate(params_data):
        for c_idx, val in enumerate(row):
            cell = table.cell(r_idx, c_idx)
            cell.text = val
            p = cell.text_frame.paragraphs[0]
            p.font.name = FONT_BODY
            p.font.size = Pt(10)
            if r_idx == 0:
                p.font.bold = True
                p.font.color.rgb = COLOR_WHITE
                cell.fill.solid()
                cell.fill.fore_color.rgb = COLOR_NAVY_DARK
            else:
                p.font.color.rgb = COLOR_NAVY_DARK
                if r_idx % 2 == 1:
                    cell.fill.solid()
                    cell.fill.fore_color.rgb = COLOR_WHITE
                else:
                    cell.fill.solid()
                    cell.fill.fore_color.rgb = RGBColor(0xE6, 0xEC, 0xF5)

    add_slide_num(s3, 3, dark=False)
    add_notes(s3, "Domain geometry is 1.0 m by 0.20 m with constant fluid properties. Values are verified from case dictionaries. Source: cases/template/constant/transportProperties.")

    # =========================================================================
    # SLIDE 4: Governing Equations and Assumptions (Light)
    # =========================================================================
    s4 = prs.slides.add_slide(prs.slide_layouts[1])
    set_bg(s4, COLOR_LIGHT_BG)
    add_title(s4, "Governing Equations and Physical Assumptions", dark=False)

    # Left: Equation Cards
    add_card(s4, Inches(0.6), Inches(1.4), Inches(6.5), Inches(5.4))
    eq_box = s4.shapes.add_textbox(Inches(0.9), Inches(1.6), Inches(5.9), Inches(4.9))
    tf_eq = eq_box.text_frame
    tf_eq.word_wrap = True
    tf_eq.margin_left = tf_eq.margin_top = 0

    p = tf_eq.paragraphs[0]
    p.text = "1. Continuity Equation (Incompressible):"
    p.font.name = FONT_BODY
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_SLATE
    p = tf_eq.add_paragraph()
    p.text = "div(U) = 0"
    p.font.name = FONT_TITLE
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY_DARK
    p.space_after = Pt(12)

    p = tf_eq.add_paragraph()
    p.text = "2. Momentum Conservation (Zero Buoyancy):"
    p.font.name = FONT_BODY
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_SLATE
    p = tf_eq.add_paragraph()
    p.text = "rho (U . grad) U = -grad(p) + mu laplacian(U)"
    p.font.name = FONT_TITLE
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY_DARK
    p.space_after = Pt(12)

    p = tf_eq.add_paragraph()
    p.text = "3. Thermal Energy Equation:"
    p.font.name = FONT_BODY
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_SLATE
    p = tf_eq.add_paragraph()
    p.text = "rho cp U . grad(T) = div(k grad(T))"
    p.font.name = FONT_TITLE
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY_DARK
    p.space_after = Pt(12)

    p = tf_eq.add_paragraph()
    p.text = "4. Plate Reynolds Number:"
    p.font.name = FONT_BODY
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_SLATE
    p = tf_eq.add_paragraph()
    p.text = "Re_L = (rho U_inf L) / mu = 1.258 x 10^5"
    p.font.name = FONT_TITLE
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_ORANGE

    # Right: Assumptions
    add_card(s4, Inches(7.4), Inches(1.4), Inches(5.3), Inches(5.4))
    as_box = s4.shapes.add_textbox(Inches(7.7), Inches(1.6), Inches(4.7), Inches(4.9))
    tf_as = as_box.text_frame
    tf_as.word_wrap = True
    tf_as.margin_left = tf_as.margin_top = 0
    p = tf_as.paragraphs[0]
    p.text = "Physical Assumptions & Limitations:"
    p.font.name = FONT_TITLE
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY_DARK
    p.space_after = Pt(14)

    bullets_s4 = [
        "Steady two-dimensional flow with constant fluid physical properties.",
        "Buoyancy forces neglected; natural convection effects are completely omitted.",
        "Re_L supports laminar flow, but ignores physical plate roughness.",
    ]
    add_bullet_list(tf_as, bullets_s4, dark=False, font_size=15)

    p_note = tf_as.add_paragraph()
    p_note.text = "Fluid medium is non-participating; no volumetric radiation absorption occurs."
    p_note.font.name = FONT_BODY
    p_note.font.size = Pt(12)
    p_note.font.color.rgb = COLOR_SLATE

    add_slide_num(s4, 4, dark=False)
    add_notes(s4, "Governing equations represent steady incompressible laminar flow. Re_L is 1.258e5. This supports laminar modeling but does not guarantee transition behavior on real plates. Source: cases/template/system/fvSchemes.")

    # =========================================================================
    # SLIDE 5: Boundary Conditions (Light)
    # =========================================================================
    s5 = prs.slides.add_slide(prs.slide_layouts[1])
    set_bg(s5, COLOR_LIGHT_BG)
    add_title(s5, "Boundary Conditions", dark=False)
    add_contained_image(s5, Inches(0.6), Inches(1.4), Inches(6.5), Inches(5.4), 'mesh_full_domain.png', 'Fig. 4: Boundary patch locations on computational domain.')

    # Right: Patch Explanations
    add_card(s5, Inches(7.4), Inches(1.4), Inches(5.3), Inches(5.4))
    bc_box = s5.shapes.add_textbox(Inches(7.7), Inches(1.6), Inches(4.7), Inches(4.9))
    tf_bc = bc_box.text_frame
    tf_bc.word_wrap = True
    tf_bc.margin_left = tf_bc.margin_top = 0

    p = tf_bc.paragraphs[0]
    p.text = "Configured OpenFOAM Patches:"
    p.font.name = FONT_TITLE
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY_DARK
    p.space_after = Pt(12)

    bullets_s5 = [
        "Inlet imposes uniform 2 m/s velocity and 300 K.",
        "Heated plate enforces no-slip and 1000 W/m² heater flux.",
        "Top boundary enforces slip velocity and zero thermal gradient.",
    ]
    add_bullet_list(tf_bc, bullets_s5, dark=False, font_size=15)

    p_extra = tf_bc.add_paragraph()
    p_extra.text = "Outlet: 100 kPa reference pressure with inletOutlet outflow condition.\nSides: Empty patch type enforcing two-dimensional planar behavior."
    p_extra.font.name = FONT_BODY
    p_extra.font.size = Pt(12)
    p_extra.font.color.rgb = COLOR_SLATE

    add_slide_num(s5, 5, dark=False)
    add_notes(s5, "Boundary conditions are configured directly in OpenFOAM 0 directory files. Inlet is uniform, plate is heated no-slip, top is slip, and outlet is pressure. Source: cases/template/0/U, 0/T, 0/p_rgh.")

    # =========================================================================
    # SLIDE 6: Surface Radiation Model (Light)
    # =========================================================================
    s6 = prs.slides.add_slide(prs.slide_layouts[1])
    set_bg(s6, COLOR_LIGHT_BG)
    add_title(s6, "Surface Radiation Model", dark=False)

    # Left: Equations
    add_card(s6, Inches(0.6), Inches(1.4), Inches(6.5), Inches(5.4))
    rad_box = s6.shapes.add_textbox(Inches(0.9), Inches(1.6), Inches(5.9), Inches(4.9))
    tf_rad = rad_box.text_frame
    tf_rad.word_wrap = True
    tf_rad.margin_left = tf_rad.margin_top = 0

    p = tf_rad.paragraphs[0]
    p.text = "Wall Energy Balance (First-Law Closure):"
    p.font.name = FONT_BODY
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_SLATE
    p = tf_rad.add_paragraph()
    p.text = "q''_heater = q''_conv + q''_rad"
    p.font.name = FONT_TITLE
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY_DARK
    p.space_after = Pt(14)

    p = tf_rad.add_paragraph()
    p.text = "Stefan-Boltzmann Radiation to Enclosure:"
    p.font.name = FONT_BODY
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_SLATE
    p = tf_rad.add_paragraph()
    p.text = "q''_rad = eps * sigma * (Tw^4 - T_sur^4)"
    p.font.name = FONT_TITLE
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = COLOR_ORANGE
    p.space_after = Pt(14)

    p = tf_rad.add_paragraph()
    p.text = "Objective Function Solved for Tw:"
    p.font.name = FONT_BODY
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_SLATE
    p = tf_rad.add_paragraph()
    p.text = "f(Tw) = -k (dT/dy)_w + eps sigma (Tw^4 - T_sur^4) - q''_heater = 0"
    p.font.name = FONT_BODY
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY_DARK

    # Right: Implementation details
    add_card(s6, Inches(7.4), Inches(1.4), Inches(5.3), Inches(5.4))
    r_box = s6.shapes.add_textbox(Inches(7.7), Inches(1.6), Inches(4.7), Inches(4.9))
    tf_r = r_box.text_frame
    tf_r.word_wrap = True
    tf_r.margin_left = tf_r.margin_top = 0
    p = tf_r.paragraphs[0]
    p.text = "Newton-Raphson Wall Solver:"
    p.font.name = FONT_TITLE
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY_DARK
    p.space_after = Pt(14)

    bullets_s6 = [
        "Uses codedFixedValue boundary condition with Newton-Raphson iteration.",
        "Emissivity equals 0.0 for baseline and 0.8 for radiation.",
        "Models radiation to 300 K surroundings without gas absorption.",
    ]
    add_bullet_list(tf_r, bullets_s6, dark=False, font_size=15)

    p_sub = tf_r.add_paragraph()
    p_sub.text = "Stefan-Boltzmann constant sigma = 5.670374 x 10^-8 W/(m² K⁴).\nSurrounding enclosure is held fixed at T_sur = 300 K."
    p_sub.font.name = FONT_BODY
    p_sub.font.size = Pt(12)
    p_sub.font.color.rgb = COLOR_SLATE

    add_slide_num(s6, 6, dark=False)
    add_notes(s6, "Surface radiation couples conduction to the quartic Stefan-Boltzmann emission term. In-situ Newton-Raphson iteration solves the nonlinear boundary condition. Source: cases/surfaceRadiation_fine/0/T.")

    # =========================================================================
    # SLIDE 7: CFD Solver and Numerical Setup (Light)
    # =========================================================================
    s7 = prs.slides.add_slide(prs.slide_layouts[1])
    set_bg(s7, COLOR_LIGHT_BG)
    add_title(s7, "CFD Solver and Numerical Setup", dark=False)

    # Full Native Table
    add_card(s7, Inches(0.6), Inches(1.4), Inches(12.133), Inches(5.4))
    t_shape7 = s7.shapes.add_table(9, 3, Inches(0.9), Inches(1.6), Inches(11.5), Inches(3.6))
    table7 = t_shape7.table
    table7.columns[0].width = Inches(3.2)
    table7.columns[1].width = Inches(3.8)
    table7.columns[2].width = Inches(4.5)

    solver_data = [
        ("Setting / Parameter", "Implementation", "Details / Configured Values"),
        ("CFD Framework", "OpenFOAM Foundation v13", "Standard finite volume formulation"),
        ("Mesh Generator", "blockMesh", "Parametric structured hexahedral generation"),
        ("Solver Application", "foamRun", "Incompressible steady/transient PIMPLE algorithm"),
        ("Divergence Schemes", "linearUpwind Gauss", "Second-order upwind for div(phi,U) and div(phi,T)"),
        ("Laplacian Schemes", "Gauss linear orthogonal", "Second-order central differencing with orthogonal correction"),
        ("Pressure Solver", "GAMG (DIC smoother)", "Tolerance: 10^-7, relative tolerance: 0.01"),
        ("Momentum & Energy Solver", "PBiCGStab (DILU)", "Tolerance: 10^-8, relative tolerance: 0.01"),
        ("Run Controls", "1500 iterations", "deltaT = 1, final time index = 1500"),
    ]
    for r_idx, row in enumerate(solver_data):
        for c_idx, val in enumerate(row):
            cell = table7.cell(r_idx, c_idx)
            cell.text = val
            p = cell.text_frame.paragraphs[0]
            p.font.name = FONT_BODY
            p.font.size = Pt(11)
            if r_idx == 0:
                p.font.bold = True
                p.font.color.rgb = COLOR_WHITE
                cell.fill.solid()
                cell.fill.fore_color.rgb = COLOR_NAVY_DARK
            else:
                p.font.color.rgb = COLOR_NAVY_DARK
                if r_idx % 2 == 1:
                    cell.fill.solid()
                    cell.fill.fore_color.rgb = COLOR_WHITE
                else:
                    cell.fill.solid()
                    cell.fill.fore_color.rgb = RGBColor(0xE6, 0xEC, 0xF5)

    s7_box = s7.shapes.add_textbox(Inches(0.9), Inches(5.4), Inches(11.5), Inches(1.2))
    tf_s7 = s7_box.text_frame
    tf_s7.word_wrap = True
    tf_s7.margin_left = tf_s7.margin_top = 0
    bullets_s7 = [
        "PIMPLE algorithm integrates pressure-velocity-energy coupling across 1500 iterations.",
        "Linear equation residuals drop below 10^-7 for all solved variables.",
        "Low linear solver residuals alone do not prove numerical convergence.",
    ]
    add_bullet_list(tf_s7, bullets_s7, dark=False, font_size=13)

    add_slide_num(s7, 7, dark=False)
    add_notes(s7, "OpenFOAM 13 foamRun executes with second-order schemes and GAMG/PBiCGStab solvers. Residuals drop below 1e-7. Low residuals do not guarantee complete convergence. Source: cases/template/system/controlDict, fvSchemes, fvSolution.")

    # =========================================================================
    # SLIDE 8: Mesh and Grid Sensitivity (Light)
    # =========================================================================
    s8 = prs.slides.add_slide(prs.slide_layouts[1])
    set_bg(s8, COLOR_LIGHT_BG)
    add_title(s8, "Mesh and Grid Sensitivity", dark=False)
    add_contained_image(s8, Inches(0.6), Inches(1.4), Inches(5.6), Inches(5.4), 'mesh_inflation_detail.png', 'Fig. 5: Near-wall mesh zoom showing 80:1 wall grading.')

    # Right: Native Table + Statement
    add_card(s8, Inches(6.5), Inches(1.4), Inches(6.2), Inches(5.4))
    t_shape8 = s8.shapes.add_table(5, 3, Inches(6.7), Inches(1.6), Inches(5.8), Inches(1.8))
    table8 = t_shape8.table
    table8.columns[0].width = Inches(2.6)
    table8.columns[1].width = Inches(1.6)
    table8.columns[2].width = Inches(1.6)

    mesh_data = [
        ("Quantity", "Coarse Mesh", "Fine Mesh"),
        ("Cells", "16,000", "64,000"),
        ("Grid dimensions", "200 x 80", "400 x 160"),
        ("First cell height", "142.5 µm", "70.3 µm"),
        ("Maximum aspect ratio", "36.63", "36.34"),
    ]
    for r_idx, row in enumerate(mesh_data):
        for c_idx, val in enumerate(row):
            cell = table8.cell(r_idx, c_idx)
            cell.text = val
            p = cell.text_frame.paragraphs[0]
            p.font.name = FONT_BODY
            p.font.size = Pt(11)
            if r_idx == 0:
                p.font.bold = True
                p.font.color.rgb = COLOR_WHITE
                cell.fill.solid()
                cell.fill.fore_color.rgb = COLOR_NAVY_DARK
            else:
                p.font.color.rgb = COLOR_NAVY_DARK
                if r_idx % 2 == 1:
                    cell.fill.solid()
                    cell.fill.fore_color.rgb = COLOR_WHITE
                else:
                    cell.fill.solid()
                    cell.fill.fore_color.rgb = RGBColor(0xE6, 0xEC, 0xF5)

    # Prominent Statement
    stmt_card = add_card(s8, Inches(6.7), Inches(3.6), Inches(5.8), Inches(1.0), bg_color=RGBColor(0xFF, 0xEE, 0xEE), border_color=COLOR_RED)
    stmt_box = s8.shapes.add_textbox(Inches(6.8), Inches(3.7), Inches(5.6), Inches(0.8))
    tf_stmt = stmt_box.text_frame
    tf_stmt.word_wrap = True
    tf_stmt.margin_left = tf_stmt.margin_top = 0
    p = tf_stmt.paragraphs[0]
    p.text = "Two meshes have been tested. Grid independence has not been demonstrated."
    p.font.name = FONT_TITLE
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_RED

    m_box = s8.shapes.add_textbox(Inches(6.7), Inches(4.75), Inches(5.8), Inches(1.9))
    tf_m = m_box.text_frame
    tf_m.word_wrap = True
    tf_m.margin_left = tf_m.margin_top = 0
    bullets_s8 = [
        "Without radiation, trailing-edge wall temperature drops 51.22 K on fine mesh.",
        "With radiation, trailing-edge wall temperature drops 27.68 K on fine mesh.",
        "A third systematically refined mesh and GCI study are required.",
    ]
    add_bullet_list(tf_m, bullets_s8, dark=False, font_size=13)

    add_slide_num(s8, 8, dark=False)
    add_notes(s8, "Mesh statistics are verified from checkMesh logs. Large wall temperature shifts between coarse and fine meshes demonstrate that grid independence is not yet achieved. Source: cases/noRadiation_fine/log.checkMesh, results/case_audit.csv.")

    # =========================================================================
    # SLIDE 9: Radiation Versus No-Radiation Results (Light)
    # =========================================================================
    s9 = prs.slides.add_slide(prs.slide_layouts[1])
    set_bg(s9, COLOR_LIGHT_BG)
    add_title(s9, "Radiation Versus No-Radiation Results", dark=False)
    add_contained_image(s9, Inches(0.6), Inches(1.4), Inches(5.8), Inches(5.4), 'four_case_temperature_zoom.png', 'Fig. 6: 2 x 2 thermal boundary layer comparison.')

    # Right: Native Table + Bullets
    add_card(s9, Inches(6.7), Inches(1.4), Inches(6.0), Inches(5.4))
    t_shape9 = s9.shapes.add_table(5, 2, Inches(6.9), Inches(1.6), Inches(5.6), Inches(2.0))
    table9 = t_shape9.table
    table9.columns[0].width = Inches(3.6)
    table9.columns[1].width = Inches(2.0)

    tw_data = [
        ("Case", "Reported Tw (x = 1.0 m)"),
        ("No radiation, coarse", "394.90 K"),
        ("Radiation, coarse", "364.38 K"),
        ("No radiation, fine", "343.68 K"),
        ("Radiation, fine", "336.70 K"),
    ]
    for r_idx, row in enumerate(tw_data):
        for c_idx, val in enumerate(row):
            cell = table9.cell(r_idx, c_idx)
            cell.text = val
            p = cell.text_frame.paragraphs[0]
            p.font.name = FONT_BODY
            p.font.size = Pt(12)
            if r_idx == 0:
                p.font.bold = True
                p.font.color.rgb = COLOR_WHITE
                cell.fill.solid()
                cell.fill.fore_color.rgb = COLOR_NAVY_DARK
            else:
                p.font.color.rgb = COLOR_NAVY_DARK
                if r_idx % 2 == 1:
                    cell.fill.solid()
                    cell.fill.fore_color.rgb = COLOR_WHITE
                else:
                    cell.fill.solid()
                    cell.fill.fore_color.rgb = RGBColor(0xE6, 0xEC, 0xF5)

    tw_box = s9.shapes.add_textbox(Inches(6.9), Inches(3.8), Inches(5.6), Inches(2.8))
    tf_tw = tw_box.text_frame
    tf_tw.word_wrap = True
    tf_tw.margin_left = tf_tw.margin_top = 0
    bullets_s9 = [
        "Radiation lowers reported wall temperature across both tested mesh levels.",
        "Temperature reduction is 30.52 K on coarse and 6.98 K on fine.",
        "Large grid difference prevents treating either reduction as mesh-independent.",
    ]
    add_bullet_list(tf_tw, bullets_s9, dark=False, font_size=14)

    add_slide_num(s9, 9, dark=False)
    add_notes(s9, "Radiation depresses trailing wall temperature by 30.52 K on coarse and 6.98 K on fine grid. The large mesh difference precludes treating either as grid-independent. Source: results/case_audit.csv.")

    # =========================================================================
    # SLIDE 10: Heat-Flux Partition (Light)
    # =========================================================================
    s10 = prs.slides.add_slide(prs.slide_layouts[1])
    set_bg(s10, COLOR_LIGHT_BG)
    add_title(s10, "Heat-Flux Partition", dark=False)
    add_contained_image(s10, Inches(0.6), Inches(1.4), Inches(5.8), Inches(5.4), 'wall_heat_flux_split.png', 'Fig. 7: Convective and radiative flux partition along plate.')

    # Right: Native Table + Explanation
    add_card(s10, Inches(6.7), Inches(1.4), Inches(6.0), Inches(5.4))
    t_shape10 = s10.shapes.add_table(5, 3, Inches(6.9), Inches(1.6), Inches(5.6), Inches(2.2))
    table10 = t_shape10.table
    table10.columns[0].width = Inches(2.8)
    table10.columns[1].width = Inches(1.4)
    table10.columns[2].width = Inches(1.4)

    flux_data = [
        ("Quantity (at x = 1.0 m)", "Coarse, eps=0.8", "Fine, eps=0.8"),
        ("Wall temperature", "364.38 K", "336.70 K"),
        ("Radiative heat flux", "432.21 W/m²", "215.59 W/m²"),
        ("Convective heat flux", "567.79 W/m²", "784.41 W/m²"),
        ("Radiative fraction", "43.22%", "21.56%"),
    ]
    for r_idx, row in enumerate(flux_data):
        for c_idx, val in enumerate(row):
            cell = table10.cell(r_idx, c_idx)
            cell.text = val
            p = cell.text_frame.paragraphs[0]
            p.font.name = FONT_BODY
            p.font.size = Pt(11)
            if r_idx == 0:
                p.font.bold = True
                p.font.color.rgb = COLOR_WHITE
                cell.fill.solid()
                cell.fill.fore_color.rgb = COLOR_NAVY_DARK
            else:
                p.font.color.rgb = COLOR_NAVY_DARK
                if r_idx % 2 == 1:
                    cell.fill.solid()
                    cell.fill.fore_color.rgb = COLOR_WHITE
                else:
                    cell.fill.solid()
                    cell.fill.fore_color.rgb = RGBColor(0xE6, 0xEC, 0xF5)

    fl_box = s10.shapes.add_textbox(Inches(6.9), Inches(4.0), Inches(5.6), Inches(2.6))
    tf_fl = fl_box.text_frame
    tf_fl.word_wrap = True
    tf_fl.margin_left = tf_fl.margin_top = 0
    bullets_s10 = [
        "Radiative fraction is defined as f_rad = (q''_rad / q''_heater) * 100%.",
        "Reported radiation fraction depends strongly on grid in current results.",
        "Flux sum balance is satisfied by construction, not independent proof.",
    ]
    add_bullet_list(tf_fl, bullets_s10, dark=False, font_size=14)

    add_slide_num(s10, 10, dark=False)
    add_notes(s10, "At the trailing edge, coarse predicts 43.22% radiation while fine predicts 21.56%. The flux identity was enforced by post-processing construction. Source: scripts/evidenceReport.py, results/case_audit.csv.")

    # =========================================================================
    # SLIDE 11: Velocity Field and Momentum Coupling (Dark Navy)
    # =========================================================================
    s11 = prs.slides.add_slide(prs.slide_layouts[1])
    set_bg(s11, COLOR_NAVY_DARK)
    add_title(s11, "Velocity Field and Momentum Coupling", dark=True)
    add_contained_image(s11, Inches(0.6), Inches(1.4), Inches(5.8), Inches(5.4), 'velocity_profiles.png', 'Fig. 8: Streamwise velocity profiles across stations.', dark_card=True)

    # Right: Decoupling card + Stat
    add_card(s11, Inches(6.7), Inches(1.4), Inches(6.0), Inches(5.4), bg_color=COLOR_NAVY_CARD, border_color=None)
    
    # Stat box
    stat_box = s11.shapes.add_textbox(Inches(7.0), Inches(1.6), Inches(5.4), Inches(1.5))
    tf_stat = stat_box.text_frame
    tf_stat.word_wrap = True
    tf_stat.margin_left = tf_stat.margin_top = 0
    p = tf_stat.paragraphs[0]
    p.text = "< 10^-12 m/s"
    p.font.name = FONT_TITLE
    p.font.size = Pt(40)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN
    p2 = tf_stat.add_paragraph()
    p2.text = "Maximum Velocity Field Difference |u_rad - u_norad|"
    p2.font.name = FONT_BODY
    p2.font.size = Pt(14)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_WHITE

    u_box = s11.shapes.add_textbox(Inches(7.0), Inches(3.3), Inches(5.4), Inches(3.3))
    tf_u = u_box.text_frame
    tf_u.word_wrap = True
    tf_u.margin_left = tf_u.margin_top = 0
    bullets_s11 = [
        "Constant density and viscosity decouple momentum from the thermal energy equation.",
        "Buoyancy is disabled, leaving momentum equations completely independent of temperature.",
        "Radiation changes thermal boundary layer without altering velocity solution.",
    ]
    add_bullet_list(tf_u, bullets_s11, dark=True, font_size=15)

    add_slide_num(s11, 11, dark=True)
    add_notes(s11, "Under constant fluid properties and zero buoyancy, the momentum equations do not contain temperature terms. Velocity is strictly decoupled. Source: cases/noRadiation_fine/1500/U, cases/surfaceRadiation_fine/1500/U.")

    # =========================================================================
    # SLIDE 12: Analytical Boundary-Layer Comparison (Light)
    # =========================================================================
    s12 = prs.slides.add_slide(prs.slide_layouts[1])
    set_bg(s12, COLOR_LIGHT_BG)
    add_title(s12, "Analytical Boundary-Layer Comparison", dark=False)
    add_contained_image(s12, Inches(0.6), Inches(1.4), Inches(5.8), Inches(5.4), 'blasius_velocity_validation.png', 'Fig. 9: Similarity profile comparison (eta vs u/U_inf).')

    # Right: Discrepancy KPI Cards
    add_card(s12, Inches(6.7), Inches(1.4), Inches(6.0), Inches(5.4))
    
    # KPI 1
    add_card(s12, Inches(7.0), Inches(1.6), Inches(5.4), Inches(1.5), bg_color=RGBColor(0xFF, 0xFB, 0xEB), border_color=COLOR_AMBER)
    kpi1_box = s12.shapes.add_textbox(Inches(7.2), Inches(1.7), Inches(5.0), Inches(1.3))
    tf_k1 = kpi1_box.text_frame
    tf_k1.word_wrap = True
    tf_k1.margin_left = tf_k1.margin_top = 0
    p = tf_k1.paragraphs[0]
    p.text = "5.38 mm vs 14.1 mm"
    p.font.name = FONT_TITLE
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = COLOR_ORANGE
    p2 = tf_k1.add_paragraph()
    p2.text = "Boundary-layer thickness delta_99 at x = 1.0 m (CFD reports 5.38 mm; Blasius predicts 14.1 mm)"
    p2.font.name = FONT_BODY
    p2.font.size = Pt(11)
    p2.font.color.rgb = COLOR_NAVY_DARK

    # KPI 2
    add_card(s12, Inches(7.0), Inches(3.3), Inches(5.4), Inches(1.5), bg_color=RGBColor(0xFF, 0xFB, 0xEB), border_color=COLOR_AMBER)
    kpi2_box = s12.shapes.add_textbox(Inches(7.2), Inches(3.4), Inches(5.0), Inches(1.3))
    tf_k2 = kpi2_box.text_frame
    tf_k2.word_wrap = True
    tf_k2.margin_left = tf_k2.margin_top = 0
    p = tf_k2.paragraphs[0]
    p.text = "875 vs 143"
    p.font.name = FONT_TITLE
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN
    p2 = tf_k2.add_paragraph()
    p2.text = "Trailing-edge Nusselt number Nu_L (CFD reports 875; laminar correlation predicts ~143)"
    p2.font.name = FONT_BODY
    p2.font.size = Pt(11)
    p2.font.color.rgb = COLOR_NAVY_DARK

    disc_box = s12.shapes.add_textbox(Inches(7.0), Inches(5.0), Inches(5.4), Inches(1.6))
    tf_d = disc_box.text_frame
    tf_d.word_wrap = True
    tf_d.margin_left = tf_d.margin_top = 0
    bullets_s12 = [
        "Similarity variable defined as eta = y * sqrt(U_inf / (nu x)).",
        "Discrepancies arise from domain height confinement and mesh resolution.",
        "Results are marked as provisional pending resolution of discrepancies.",
    ]
    add_bullet_list(tf_d, bullets_s12, dark=False, font_size=13)

    add_slide_num(s12, 12, dark=False)
    add_notes(s12, "Discrepancies in boundary-layer thickness and Nusselt number must be disclosed before claiming validation. Blasius predicts 14.1 mm while CFD reports 5.38 mm. Source: results/case_audit.csv, scripts/evidenceReport.py.")

    # =========================================================================
    # SLIDE 13: Numerical Audit and Limitations (Dark Navy)
    # =========================================================================
    s13 = prs.slides.add_slide(prs.slide_layouts[1])
    set_bg(s13, COLOR_NAVY_DARK)
    add_title(s13, "Numerical Audit and Limitations", dark=True)

    # 2-Column Layout: Verified vs Requires Further Verification
    # Column 1: Verified
    add_card(s13, Inches(0.6), Inches(1.4), Inches(5.8), Inches(4.5), bg_color=COLOR_NAVY_CARD, border_color=COLOR_CYAN)
    c1_box = s13.shapes.add_textbox(Inches(0.9), Inches(1.6), Inches(5.2), Inches(4.1))
    tf_c1 = c1_box.text_frame
    tf_c1.word_wrap = True
    tf_c1.margin_left = tf_c1.margin_top = 0
    p = tf_c1.paragraphs[0]
    p.text = "Verified from Current Files:"
    p.font.name = FONT_TITLE
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN
    p.space_after = Pt(14)
    items_c1 = [
        "Solver completed 1500 iterations with linear residuals below 10^-7.",
        "Newton-Raphson scheme converges non-linear wall energy equation.",
        "Momentum field decouples strictly under constant fluid properties.",
    ]
    for text in items_c1:
        p = tf_c1.add_paragraph()
        p.text = f"✓  {text}"
        p.font.name = FONT_BODY
        p.font.size = Pt(14)
        p.font.color.rgb = COLOR_WHITE
        p.space_after = Pt(14)

    # Column 2: Requires Further Verification
    add_card(s13, Inches(6.9), Inches(1.4), Inches(5.8), Inches(4.5), bg_color=COLOR_NAVY_CARD, border_color=COLOR_AMBER)
    c2_box = s13.shapes.add_textbox(Inches(7.2), Inches(1.6), Inches(5.2), Inches(4.1))
    tf_c2 = c2_box.text_frame
    tf_c2.word_wrap = True
    tf_c2.margin_left = tf_c2.margin_top = 0
    p = tf_c2.paragraphs[0]
    p.text = "Requires Further Verification:"
    p.font.name = FONT_TITLE
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_AMBER
    p.space_after = Pt(14)
    items_c2 = [
        "Grid independence: 51.22 K wall temperature shift between meshes.",
        "Discrepancy between 5.38 mm CFD thickness and 14.1 mm Blasius.",
        "Wall heat flux needs independent calculation from thermal gradient.",
    ]
    for text in items_c2:
        p = tf_c2.add_paragraph()
        p.text = f"!  {text}"
        p.font.name = FONT_BODY
        p.font.size = Pt(14)
        p.font.color.rgb = COLOR_WHITE
        p.space_after = Pt(14)

    # Bottom Banner
    b_banner = s13.shapes.add_textbox(Inches(0.6), Inches(6.1), Inches(12.133), Inches(0.8))
    tf_bb = b_banner.text_frame
    tf_bb.word_wrap = True
    tf_bb.margin_left = tf_bb.margin_top = 0
    p = tf_bb.paragraphs[0]
    p.text = "Classification Note: Unresolved numerical values are marked as provisional. Iterative convergence does not equal grid independence or experimental validation."
    p.font.name = FONT_BODY
    p.font.size = Pt(12)
    p.font.color.rgb = COLOR_SLATE

    add_slide_num(s13, 13, dark=True)
    add_notes(s13, "This slide separates verified simulation facts from items requiring further verification. Grid sensitivity and boundary-layer thickness discrepancies remain open. Source: cases/noRadiation_fine/log.foamRun, results/case_audit.csv.")

    # =========================================================================
    # SLIDE 14: Conclusions and Next Work (Dark Navy)
    # =========================================================================
    s14 = prs.slides.add_slide(prs.slide_layouts[1])
    set_bg(s14, COLOR_NAVY_DARK)
    add_title(s14, "Conclusions and Next Work", dark=True)

    # 6 Prioritized Action Cards
    priorities = [
        ("1. Resolve Discrepancies", "Investigate thickness (5.38 vs 14.1 mm) and Nusselt number (875 vs 143)."),
        ("2. Independent Heat Flux", "Calculate wall flux from -k(dT/dy)_w and check global energy balance."),
        ("3. Third Refined Mesh", "Execute an 800 x 320 structured grid to establish asymptotic convergence."),
        ("4. Formal GCI Study", "Compute ASME VV 20 Grid Convergence Index error bands for Tw and Nu."),
        ("5. Recheck Similarity", "Match domain height and inlet conditions to semi-infinite assumptions."),
        ("6. Parameter Sensitivity", "Vary emissivity (0 to 1) and flux (500 to 2000 W/m²) after verification."),
    ]
    card_w = Inches(3.8)
    card_h = Inches(1.8)
    for idx, (p_title, p_desc) in enumerate(priorities):
        row = idx // 3
        col = idx % 3
        left = Inches(0.6 + col * 4.15)
        top = Inches(1.4 + row * 2.1)
        add_card(s14, left, top, card_w, card_h, bg_color=COLOR_NAVY_CARD, border_color=COLOR_BORDER)
        
        p_box = s14.shapes.add_textbox(left + Inches(0.2), top + Inches(0.15), card_w - Inches(0.4), card_h - Inches(0.3))
        tf_pr = p_box.text_frame
        tf_pr.word_wrap = True
        tf_pr.margin_left = tf_pr.margin_top = 0
        p = tf_pr.paragraphs[0]
        p.text = p_title
        p.font.name = FONT_TITLE
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = COLOR_ORANGE if idx < 2 else COLOR_CYAN
        p.space_after = Pt(4)

        p2 = tf_pr.add_paragraph()
        p2.text = p_desc
        p2.font.name = FONT_BODY
        p2.font.size = Pt(12)
        p2.font.color.rgb = COLOR_LIGHT_BG

    # Bottom Presenter Dossier
    dos_box = s14.shapes.add_textbox(Inches(0.6), Inches(5.8), Inches(12.133), Inches(0.9))
    tf_dos = dos_box.text_frame
    tf_dos.word_wrap = True
    tf_dos.margin_left = tf_dos.margin_top = 0
    p = tf_dos.paragraphs[0]
    p.text = "Jersam Lithin L  •  Register No.: URK24AE1026  •  B.Tech Aerospace Engineering  •  Karunya Institute of Technology and Sciences"
    p.font.name = FONT_BODY
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE
    p2 = tf_dos.add_paragraph()
    p2.text = "Conclusion: Radiation methodology is established, but validation requires resolving grid sensitivity and analytical discrepancies."
    p2.font.name = FONT_BODY
    p2.font.size = Pt(12)
    p2.font.color.rgb = COLOR_SLATE

    add_slide_num(s14, 14, dark=True)
    add_notes(s14, "The simulation demonstrates radiation modeling, but validation requires resolving grid sensitivity and similarity discrepancies. Six priorities are defined. Source: README.md, results/case_audit.csv.")

    print(f"Saving updated deck to {OUTPUT_PPTX}...")
    prs.save(OUTPUT_PPTX)
    print("Done generating presentation!")


if __name__ == '__main__':
    create_deck()
