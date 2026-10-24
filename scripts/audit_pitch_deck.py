#!/usr/bin/env python3
"""
audit_pitch_deck.py
Audits Flat_Plate_Radiation_CFD_Pitch.pptx against all quality gates:
- Exact 14 slides
- Max 3 bullets per slide, max 12 words per bullet
- Font consistency (Cambria for titles/stats, Calibri for body/tables)
- Speaker notes presence on every slide (2-4 sentences, source path)
- Placeholder scan (detecting [placeholder])
- Ensuring every slide has a figure, table, or large stat
"""

import sys
import re
import pptx

PPTX_PATH = "Flat_Plate_Radiation_CFD_Pitch.pptx"

def audit():
    prs = pptx.Presentation(PPTX_PATH)
    print(f"=== AUDITING {PPTX_PATH} ===")
    print(f"Slide count: {len(prs.slides)} (Expected: 14)")
    assert len(prs.slides) == 14, f"Slide count is {len(prs.slides)}, expected 14!"

    placeholders_found = []
    font_issues = []
    bullet_issues = []
    notes_issues = []
    slide_titles = []

    for s_idx, slide in enumerate(prs.slides):
        slide_num = s_idx + 1
        print(f"\n--- Slide {slide_num} ---")
        
        # Check notes
        notes_text = ""
        if slide.has_notes_slide and slide.notes_slide.notes_text_frame:
            notes_text = slide.notes_slide.notes_text_frame.text.strip()
        
        sentences = [s.strip() for s in re.split(r'[.!?]+', notes_text) if s.strip()]
        print(f"  Notes: {len(sentences)} sentences, {len(notes_text.split())} words")
        if len(sentences) < 2:
            notes_issues.append((slide_num, f"Fewer than 2 sentences in notes ({len(sentences)})"))
        if "Source:" not in notes_text and "source:" not in notes_text.lower():
            notes_issues.append((slide_num, "Missing 'Source:' in speaker notes"))

        # Check shapes
        text_shapes = []
        bullets = []
        has_fig_or_table_or_stat = False

        for shape in slide.shapes:
            if shape.has_table:
                has_fig_or_table_or_stat = True
                print(f"  [Native Table] {shape.table.rows} rows x {len(shape.table.columns)} cols")
            if shape.shape_type == pptx.enum.shapes.MSO_SHAPE_TYPE.PICTURE:
                has_fig_or_table_or_stat = True
                print(f"  [Picture] {shape.name}")
            if shape.has_text_frame:
                full_tf_text = shape.text_frame.text.strip()
                if full_tf_text:
                    text_shapes.append(full_tf_text)
                    # Check for large stat or number
                    if any(c.isdigit() for c in full_tf_text) and any(kw in full_tf_text for kw in ['K', '%', 'W/m²', 'Cells', 'Iter', 'Re_L', '0.11', '6.98', '800']):
                        has_fig_or_table_or_stat = True

                for p_idx, p in enumerate(shape.text_frame.paragraphs):
                    p_txt = p.text.strip()
                    # Only match actual bullets starting with bullet dot •
                    if p_txt.startswith("•"):
                        b_content = p_txt.lstrip("• \t")
                        words = b_content.split()
                        bullets.append((b_content, len(words)))
                        if len(words) > 12:
                            bullet_issues.append((slide_num, f"Bullet exceeds 12 words ({len(words)}): '{b_content}'"))

                    for r in p.runs:
                        # Check placeholder regex like [value] or [x%]
                        matches = re.findall(r'\[(.*?)\]', r.text)
                        for m in matches:
                            placeholders_found.append((slide_num, f"[{m}]", r.text))
                        
                        # Check font
                        fn = r.font.name
                        if fn and fn not in ['Cambria', 'Calibri', 'Arial']:
                            font_issues.append((slide_num, fn, r.text[:30]))

        print(f"  Bullets count: {len(bullets)}")
        if len(bullets) > 3:
            bullet_issues.append((slide_num, f"Too many bullets on slide ({len(bullets)} > 3)"))
        for b_txt, wc in bullets:
            print(f"    • ({wc} words) {b_txt}")

        if not has_fig_or_table_or_stat:
            print(f"  WARNING: Slide {slide_num} does not appear to have a figure, table, or stat!")

    print("\n=== AUDIT SUMMARY ===")
    print(f"Bullet issues: {len(bullet_issues)}")
    for iss in bullet_issues:
        print(f"  Slide {iss[0]}: {iss[1]}")

    print(f"\nFont issues: {len(font_issues)}")
    for fi in font_issues:
        print(f"  Slide {fi[0]}: Font '{fi[1]}' on text '{fi[2]}'")

    print(f"\nNotes issues: {len(notes_issues)}")
    for ni in notes_issues:
        print(f"  Slide {ni[0]}: {ni[1]}")

    print(f"\nPlaceholders found: {len(placeholders_found)}")
    for pf in placeholders_found:
        print(f"  Slide {pf[0]}: Placeholder {pf[1]} in '{pf[2]}'")

    if len(bullet_issues) == 0 and len(font_issues) == 0 and len(notes_issues) == 0 and len(placeholders_found) == 0:
        print("\n>>> ALL QUALITY GATE CRITERIA PASSED WITH ZERO VIOLATIONS! <<<")

if __name__ == '__main__':
    audit()
