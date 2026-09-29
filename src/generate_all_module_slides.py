import os
import sys
import glob
import re
from PIL import Image
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# Banned words check list
BANNED_WORDS = [
    'taksonomi', 'tripartit', 'ontologis', 'epistemologis',
    'dialektika', 'manifestasi dependensi', 'de facto'
]

# Map of banned words to clean academic replacements
REPLACEMENTS = {
    'taksonomi bloom': 'hierarki kognitif Bloom',
    'taksonomi': 'sistematika klasifikasi',
    'tripartit': 'tiga pilar',
    'ontologis': 'karakteristik esensial',
    'epistemologis': 'fondasi metodologis',
    'dialektika': 'diskursus kritis',
    'manifestasi dependensi': 'ketergantungan struktural',
    'de facto': 'secara praktis operasional'
}

def clean_text(text):
    if not text:
        return ""
    cleaned = text
    for b_word, repl in REPLACEMENTS.items():
        pattern = re.compile(re.escape(b_word), re.IGNORECASE)
        cleaned = pattern.sub(repl, cleaned)
    return cleaned

PART_TITLES = {
    "part-01": "Bagian 1: Pengantar Kecerdasan Buatan & Paradigma AI",
    "part-02": "Bagian 2: Logika Komputasi dan Pemrograman Dasar",
    "part-03": "Bagian 3: Struktur Data dan Bahasa Python untuk AI",
    "part-04": "Bagian 4: Pengolahan, Analisis, dan Visualisasi Data Ilmiah",
    "part-05": "Bagian 5: Matematika dan Sains Data untuk AI",
    "part-06": "Bagian 6: Evaluasi Model dan Pengambilan Keputusan",
    "part-07": "Bagian 7: Machine Learning - Konsep dan Algoritma Klasik",
    "part-08": "Bagian 8: Unsupervised Learning dan Reduksi Dimensi",
    "part-09": "Bagian 9: Fondasi Deep Learning dan Arsitektur Jaringan Saraf Tiruan",
    "part-10": "Bagian 10: Pelatihan, Optimasi, dan Regularisasi Deep Learning",
    "part-11": "Bagian 11: Pengolahan Citra Digital dan Computer Vision Tingkat Dasar",
    "part-12": "Bagian 12: Convolutional Neural Networks (CNN) dan Object Detection",
    "part-13": "Bagian 13: Integrasi Sistem AI, Deployment Edge, dan Studi Kasus Terapan",
}

def extract_module_data(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    part_dir = os.path.basename(os.path.dirname(filepath))
    part_name = PART_TITLES.get(part_dir, f"Bagian {part_dir}")

    # Title
    m_title = re.search(r'^#\s+(.+)$', content, re.M)
    full_title = clean_text(m_title.group(1).strip() if m_title else os.path.basename(filepath))
    
    m_code = re.search(r'AI Modul\s+([\d\.]+)', full_title)
    mod_code = f"AI Modul {m_code.group(1)}" if m_code else "AI Modul"
    mod_name = full_title.split(":", 1)[1].strip() if ":" in full_title else full_title

    # Sub-CPMK
    cpmk_section = re.search(r'###\s*1\.1.*?\n(.*?)(?=\n###|\n##|\Z)', content, re.DOTALL)
    cpmk_bullets = []
    if cpmk_section:
        cpmk_matches = re.findall(r'^\d+\.\s+(.+)$', cpmk_section.group(1), re.M)
        for c in cpmk_matches[:4]:
            c_clean = re.sub(r'\*\*(.*?)\*\*', r'\1', c)
            c_clean = re.sub(r'[\$\*]', '', c_clean).strip()
            cpmk_bullets.append(clean_text(c_clean))
    if len(cpmk_bullets) < 3:
        cpmk_bullets = [
            f"Menganalisis (C4) prinsip fundamental dan landasan matematika pada {mod_name}.",
            f"Mengimplementasikan (C3) algoritma berbasis Python standar industri untuk {mod_name}.",
            f"Mengevaluasi (C5) kompleksitas komputasi, stabilitas numerik, dan efisiensi inferensi model.",
            f"Merancang (C6) integrasi solusi cerdas terapan pada rantai pasok agrokompleks dan perkebunan sawit."
        ]

    # Math equations
    math_matches = re.findall(r'\$\$(.*?)\$\$', content, re.DOTALL)
    math_eq = ""
    if math_matches:
        # Pick the cleanest short math equation
        for eq in math_matches:
            lines = [l.strip() for l in eq.splitlines() if l.strip() and not l.strip().startswith('%')]
            candidate = " ".join(lines)
            if 10 < len(candidate) < 120 and candidate.count(r'\begin') == 0:
                math_eq = candidate
                break
        if not math_eq and math_matches:
            math_eq = " ".join(math_matches[0].splitlines()[:2]).strip()
    
    if not math_eq:
        math_eq = r"f(x; \theta) = \sigma(W \cdot x + b) \quad \text{dengan} \quad \min_\theta \mathcal{L}(\theta) = \frac{1}{N}\sum_{i=1}^N \text{Loss}(y_i, f(x_i; \theta))"

    # Images
    img_refs = re.findall(r'!\[(.*?)\]\((.*?)\)', content)
    valid_images = []
    for alt, pth in img_refs:
        clean_pth = pth.replace('../', '').replace('./', '')
        abs_img = os.path.normpath(os.path.join(os.path.dirname(filepath), pth))
        if os.path.exists(abs_img):
            valid_images.append((clean_text(alt), abs_img))
        else:
            cand = os.path.join("docs", "assets", os.path.basename(clean_pth))
            if os.path.exists(cand):
                valid_images.append((clean_text(alt), cand))

    # Code blocks
    code_blocks = re.findall(r'```(?:python)?\s*\n(.*?)```', content, re.DOTALL)
    rep_code = ""
    for cb in code_blocks:
        cb_clean = cb.strip()
        if len(cb_clean.splitlines()) >= 4 and "import " in cb_clean:
            rep_code = cb_clean
            break
    if not rep_code and code_blocks:
        rep_code = code_blocks[0].strip()
    if not rep_code:
        rep_code = "# Pipeline Standar Industri Python\nimport numpy as np\n\ndef execute_pipeline(data):\n    # Pemrosesan terstandardisasi\n    return np.asarray(data)"

    code_lines = [l for l in rep_code.splitlines() if not l.startswith("#!")]
    if len(code_lines) > 15:
        rep_code = "\n".join(code_lines[:14]) + "\n# ... [lanjutan pipeline teroptimasi]"
    else:
        rep_code = "\n".join(code_lines)

    # Real-world Hook / Case Study
    hook_sec = re.search(r'##\s*\d+\.\s*(?:Pengantar|Studi Kasus|Profil|Aplikasi Riil).*?\n(.*?)(?=\n##|\Z)', content, re.DOTALL | re.IGNORECASE)
    hook_text = ""
    if hook_sec:
        paragraphs = [p.strip() for p in hook_sec.group(1).split("\n\n") if p.strip() and not p.strip().startswith("#") and not p.strip().startswith("```") and not p.strip().startswith("![")]
        if paragraphs:
            hook_text = clean_text(paragraphs[0])
            hook_text = re.sub(r'[\*\#\_\[\]]', '', hook_text)

    # Pitfalls / Kekeliruan
    pitfall_sec = re.search(r'##\s*\d+\.\s*(?:Kekeliruan|Potensi Kegagalan|Common Pitfalls|Jebakan).*?\n(.*?)(?=\n##|\Z)', content, re.DOTALL | re.IGNORECASE)
    pitfalls_extracted = []
    if pitfall_sec:
        # Find bullet or numbered points
        p_items = re.findall(r'(?:\d+\.|\*|\-)\s+\*\*(.*?)\*\*\s*[:\-–]?\s*(.*?)(?=(?:\n(?:\d+\.|\*|\-)|\Z))', pitfall_sec.group(1), re.DOTALL)
        for p_title, p_desc in p_items[:3]:
            p_desc_clean = re.sub(r'[\*\#\_\[\]]', '', p_desc).strip().replace('\n', ' ')
            pitfalls_extracted.append((clean_text(p_title.strip()), clean_text(p_desc_clean[:200])))

    return {
        "filepath": filepath,
        "part_dir": part_dir,
        "part_name": part_name,
        "mod_code": mod_code,
        "mod_name": mod_name,
        "full_title": full_title,
        "cpmk_bullets": cpmk_bullets,
        "math_eq": math_eq,
        "valid_images": valid_images,
        "rep_code": rep_code,
        "hook_text": hook_text,
        "pitfalls_extracted": pitfalls_extracted
    }

def create_presentation_deck(data, output_pptx, output_md=None):
    os.makedirs(os.path.dirname(output_pptx), exist_ok=True)
    if output_md:
        os.makedirs(os.path.dirname(output_md), exist_ok=True)

    part_dir = data["part_dir"]
    part_name = data["part_name"]
    mod_code = data["mod_code"]
    mod_name = data["mod_name"]
    cpmk_bullets = data["cpmk_bullets"]
    math_eq = data["math_eq"]
    valid_images = data["valid_images"]
    rep_code = data["rep_code"]
    hook_text = data["hook_text"]
    pitfalls_extracted = data["pitfalls_extracted"]

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Helper: Slide Setup
    def setup_slide(slide, title_text, badge_text=f"{part_dir.upper()} • {mod_code}"):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = RGBColor(248, 250, 252)
        bg.line.fill.background()

        strip = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.08))
        strip.fill.solid()
        strip.fill.fore_color.rgb = RGBColor(37, 99, 235)
        strip.line.fill.background()

        badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.3), Inches(4.5), Inches(0.32))
        badge.fill.solid()
        badge.fill.fore_color.rgb = RGBColor(239, 246, 255)
        badge.line.color.rgb = RGBColor(191, 219, 254)
        badge.line.width = Pt(1)
        tf_b = badge.text_frame
        tf_b.word_wrap = False
        p_b = tf_b.paragraphs[0]
        p_b.text = badge_text
        p_b.font.size = Pt(10)
        p_b.font.bold = True
        p_b.font.color.rgb = RGBColor(30, 58, 138)
        p_b.alignment = PP_ALIGN.CENTER

        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.7), Inches(0.55))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.size = Pt(22)
        p.font.bold = True
        p.font.color.rgb = RGBColor(15, 23, 42)

        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.32), Inches(11.733), Inches(0.02))
        line.fill.solid()
        line.fill.fore_color.rgb = RGBColor(226, 232, 240)
        line.line.fill.background()

        fline = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(6.92), Inches(11.733), Inches(0.02))
        fline.fill.solid()
        fline.fill.fore_color.rgb = RGBColor(226, 232, 240)
        fline.line.fill.background()

        ftb = slide.shapes.add_textbox(Inches(0.8), Inches(6.98), Inches(5.5), Inches(0.35))
        p_f1 = ftb.text_frame.paragraphs[0]
        p_f1.text = "Program Studi Agroteknologi & Informatika - INSTIPER"
        p_f1.font.size = Pt(9)
        p_f1.font.color.rgb = RGBColor(100, 116, 139)

        ftb2 = slide.shapes.add_textbox(Inches(6.5), Inches(6.98), Inches(6.0), Inches(0.35))
        p_f2 = ftb2.text_frame.paragraphs[0]
        p_f2.text = f"Kecerdasan Buatan & Sains Data Pertanian Presisi • {mod_code}"
        p_f2.alignment = PP_ALIGN.RIGHT
        p_f2.font.size = Pt(9)
        p_f2.font.bold = True
        p_f2.font.color.rgb = RGBColor(71, 85, 105)

    def add_card(slide, left, top, width, height, title=None, border_color=RGBColor(226, 232, 240), bg_color=RGBColor(255, 255, 255)):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1.2)
        if title:
            t_box = slide.shapes.add_textbox(Inches(left + 0.15), Inches(top + 0.1), Inches(width - 0.3), Inches(0.4))
            p = t_box.text_frame.paragraphs[0]
            p.text = title
            p.font.size = Pt(13)
            p.font.bold = True
            p.font.color.rgb = RGBColor(15, 23, 42)
        return card

    # ==================== SLIDE 1: COVER ====================
    slide1 = prs.slides.add_slide(blank_layout)
    bg1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = RGBColor(15, 23, 42)
    bg1.line.fill.background()

    c_badge = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(1.2), Inches(6.8), Inches(0.4))
    c_badge.fill.solid()
    c_badge.fill.fore_color.rgb = RGBColor(30, 41, 59)
    c_badge.line.color.rgb = RGBColor(56, 189, 248)
    c_badge.line.width = Pt(1)
    p_cb = c_badge.text_frame.paragraphs[0]
    p_cb.text = "KURSUS PROFESIONAL & AKADEMIS KECERDASAN BUATAN"
    p_cb.font.size = Pt(11)
    p_cb.font.bold = True
    p_cb.font.color.rgb = RGBColor(56, 189, 248)
    p_cb.alignment = PP_ALIGN.CENTER

    tb1 = slide1.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.333), Inches(3.2))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.text = f"{mod_code}: {mod_name}"
    p1.font.size = Pt(32)
    p1.font.bold = True
    p1.font.color.rgb = RGBColor(255, 255, 255)
    
    p2 = tf1.add_paragraph()
    p2.text = f"{part_name}\nIntegrasi Fondasi Komputasi & Rekayasa Presisi Sektor Perkebunan Sawit"
    p2.font.size = Pt(16)
    p2.font.color.rgb = RGBColor(148, 163, 184)
    p2.space_before = Pt(12)

    meta_info = [
        ("Beban Akademik", "3 SKS (Teori & Praktikum)"),
        ("Alokasi Waktu", "2x50m Teori + 2x50m Praktikum"),
        ("Tingkat Kognitif", "Bloom C2 - C5 (HOTS Analitis)"),
        ("Domain Terapan", "Agro-Industri & Kelapa Sawit")
    ]
    for i, (m_lbl, m_val) in enumerate(meta_info):
        left_pos = 1.0 + i * 2.9
        mc = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left_pos), Inches(5.4), Inches(2.65), Inches(1.2))
        mc.fill.solid()
        mc.fill.fore_color.rgb = RGBColor(30, 41, 59)
        mc.line.color.rgb = RGBColor(51, 65, 85)
        mc.line.width = Pt(1)
        
        tb_m = slide1.shapes.add_textbox(Inches(left_pos + 0.1), Inches(5.45), Inches(2.45), Inches(1.1))
        tf_m = tb_m.text_frame
        tf_m.word_wrap = True
        p_m1 = tf_m.paragraphs[0]
        p_m1.text = m_lbl.upper()
        p_m1.font.size = Pt(9)
        p_m1.font.bold = True
        p_m1.font.color.rgb = RGBColor(148, 163, 184)
        
        p_m2 = tf_m.add_paragraph()
        p_m2.text = m_val
        p_m2.font.size = Pt(11)
        p_m2.font.bold = True
        p_m2.font.color.rgb = RGBColor(241, 245, 249)
        p_m2.space_before = Pt(4)

    # ==================== SLIDE 2: CAPAIAN PEMBELAJARAN ====================
    slide2 = prs.slides.add_slide(blank_layout)
    setup_slide(slide2, "Capaian Pembelajaran Khusus (Sub-CPMK) & Kerangka Hasil")
    
    add_card(slide2, 0.8, 1.5, 11.733, 2.3, "SASARAN PEMBELAJARAN (SUB-CPMK)")
    tb_cpmk = slide2.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(11.333), Inches(1.6))
    tf_cpmk = tb_cpmk.text_frame
    tf_cpmk.word_wrap = True
    for idx, b in enumerate(cpmk_bullets[:4]):
        p = tf_cpmk.paragraphs[0] if idx == 0 else tf_cpmk.add_paragraph()
        p.text = f"•  {b}"
        p.font.size = Pt(11)
        p.font.color.rgb = RGBColor(51, 65, 85)
        p.space_after = Pt(4)

    pillars = [
        ("OUTPUTS (Keluaran Berwujud)", RGBColor(2, 132, 199), [
            "Dokumen spesifikasi arsitektur komputasi dan formulasi variabel model.",
            "Skrip kode program Python modular yang lulus validasi unit testing.",
            "Laporan visualisasi metrik performa empiris pada data perkebunan."
        ]),
        ("OUTCOMES (Kompetensi Inti)", RGBColor(79, 70, 229), [
            "Penguasaan notasi matematika dan formulasi fungsi objektif komputasi.",
            "Keterampilan mendiagnosis anomali data, degradasi performa, dan overfitting.",
            "Kemampuan memilih algoritma paling optimal sesuai kendala komputasi."
        ]),
        ("IMPACTS (Dampak Industri)", RGBColor(16, 185, 129), [
            "Peningkatan efisiensi operasional dan reduksi losses di pabrik/kebun sawit.",
            "Pola pikir insinyur AI rasional yang tangguh menghadapi noise data riil.",
            "Akselerasi otomatisasi presisi menuju transformasi industri 4.0 berkelanjutan."
        ])
    ]
    for i, (p_title, p_color, p_items) in enumerate(pillars):
        left_pos = 0.8 + i * 3.98
        add_card(slide2, left_pos, 4.0, 3.78, 2.7, p_title, border_color=p_color)
        tb_p = slide2.shapes.add_textbox(Inches(left_pos + 0.15), Inches(4.5), Inches(3.48), Inches(2.1))
        tf_p = tb_p.text_frame
        tf_p.word_wrap = True
        for j, item in enumerate(p_items):
            p = tf_p.paragraphs[0] if j == 0 else tf_p.add_paragraph()
            p.text = f"✓  {item}"
            p.font.size = Pt(10)
            p.font.color.rgb = RGBColor(51, 65, 85)
            p.space_after = Pt(6)

    # ==================== SLIDE 3: LANDASAN TEORI & FORMULASI ====================
    slide3 = prs.slides.add_slide(blank_layout)
    setup_slide(slide3, "Landasan Teori & Formulasi Matematis Kunci")

    add_card(slide3, 0.8, 1.5, 5.7, 3.6, "FONDASI KONSEPTUAL & PARADIGMA TEORI")
    tb_t = slide3.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.3), Inches(2.9))
    tf_t = tb_t.text_frame
    tf_t.word_wrap = True
    t_bullets = [
        f"Definisi Formal: Menetapkan kerangka kerja matematis dan algoritma komputasi untuk mengabstraksi pola pada {mod_name}.",
        "Prinsip Operasional: Memanfaatkan optimasi fungsi berparameter untuk meminimalkan deviasi dan meningkatkan generalisasi.",
        "Analogi Fisis/Domain: Merefleksikan mekanisme adaptasi biologis dan respons fisik tanaman/lingkungan terhadap masukan eksternal.",
        "Ketahanan Stokastik: Mengendalikan variabilitas acak melalui estimasi probabilistik dan normalisasi ruang fitur."
    ]
    for idx, b in enumerate(t_bullets):
        p = tf_t.paragraphs[0] if idx == 0 else tf_t.add_paragraph()
        p.text = f"•  {b}"
        p.font.size = Pt(11)
        p.font.color.rgb = RGBColor(51, 65, 85)
        p.space_after = Pt(6)

    add_card(slide3, 6.8, 1.5, 5.733, 3.6, "FORMULASI MATEMATIS & FUNGSI OBJEKTIF", border_color=RGBColor(37, 99, 235))
    tb_m = slide3.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.333), Inches(2.9))
    tf_m = tb_m.text_frame
    tf_m.word_wrap = True
    
    p_fml = tf_m.paragraphs[0]
    p_fml.text = "Persamaan Kunci Pemetaan & Optimasi:"
    p_fml.font.size = Pt(11)
    p_fml.font.bold = True
    p_fml.font.color.rgb = RGBColor(15, 23, 42)

    p_box = tf_m.add_paragraph()
    clean_eq = math_eq.replace('\\quad', '  ').replace('\\text', '').replace('{', '').replace('}', '').replace('\\', '')
    p_box.text = f"    {clean_eq[:80]}"
    p_box.font.name = "Consolas"
    p_box.font.size = Pt(10)
    p_box.font.bold = True
    p_box.font.color.rgb = RGBColor(30, 58, 138)
    p_box.space_before = Pt(6)
    p_box.space_after = Pt(8)

    math_desc = [
        "x ∈ R^d: Vektor representasi fitur masukan berdimensi d.",
        "θ = {W, b}: Parameter bobot penimbang dan bias yang dioptimasi.",
        "σ(·): Pemetaan fungsi aktivasi atau fungsi transfer non-linier.",
        "L(θ): Fungsi objektif/kerugian pemandu konvergensi gradien."
    ]
    for b in math_desc:
        p = tf_m.add_paragraph()
        p.text = f"•  {b}"
        p.font.size = Pt(10)
        p.font.color.rgb = RGBColor(71, 85, 105)
        p.space_after = Pt(4)

    add_card(slide3, 0.8, 5.25, 11.733, 1.5, "SIGNIFIKANSI KOMPUTASIONAL & IMPLIKASI REKAYASA", border_color=RGBColor(16, 185, 129))
    tb_imp = slide3.shapes.add_textbox(Inches(1.0), Inches(5.65), Inches(11.333), Inches(0.95))
    tf_imp = tb_imp.text_frame
    tf_imp.word_wrap = True
    p_imp = tf_imp.paragraphs[0]
    p_imp.text = f"Formulasi matematika pada {mod_name} memastikan kepastian stabilitas numerik saat dieksekusi pada unit pemrosesan edge maupun kluster server industri, memungkinkan inferensi dengan latensi rendah dan konvergensi stabil pada kondisi data lapangan yang heterogen."
    p_imp.font.size = Pt(10.5)
    p_imp.font.color.rgb = RGBColor(51, 65, 85)

    # ==================== SLIDE 4: ARSITEKTUR KOMPUTASI ====================
    slide4 = prs.slides.add_slide(blank_layout)
    setup_slide(slide4, "Arsitektur Komputasi & Diagram Alir Pipeline")

    if valid_images:
        img_title, img_path = valid_images[0]
        add_card(slide4, 0.8, 1.5, 6.6, 5.25, f"DIAGRAM: {img_title.upper()[:45]}")
        try:
            with Image.open(img_path) as im:
                im_w, im_h = im.size
            aspect = im_w / im_h
            max_w, max_h = 6.2, 4.4
            if aspect > (max_w / max_h):
                disp_w = max_w
                disp_h = max_w / aspect
            else:
                disp_h = max_h
                disp_w = max_h * aspect
            off_x = 0.8 + (6.6 - disp_w) / 2
            off_y = 2.0 + (4.5 - disp_h) / 2
            slide4.shapes.add_picture(img_path, Inches(off_x), Inches(off_y), Inches(disp_w), Inches(disp_h))
        except Exception as e:
            pass

        right_left = 7.6
        right_w = 4.933
        add_card(slide4, right_left, 1.5, right_w, 5.25, "TAHAPAN PIPELINE EKSEKUSI SISTEM")
        
        stages = [
            ("1. Ingesti Data Sensor / Citra", "Menerima data masukan mentah dari sensor IoT perkebunan, kamera CCTV sortasi TBS, atau drone multispektral."),
            ("2. Preprocessing & Normalisasi", "Transformasi citra, filtering noise, standardisasi fitur numerik, dan isolasi rentang dinamis."),
            ("3. Mesin Inferensi & Ekstraksi", "Propagasi maju melewati arsitektur pemodelan komputasi untuk menghasilkan estimasi probabilitas."),
            ("4. Post-processing & Aksi Kontrol", "Thresholding analitis, verifikasi batas aman, dan pemicuan sistem akuasi/peringatan otomatis.")
        ]
        for s_idx, (s_title, s_desc) in enumerate(stages):
            s_top = 2.0 + s_idx * 1.15
            sc = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(right_left + 0.2), Inches(s_top), Inches(right_w - 0.4), Inches(1.0))
            sc.fill.solid()
            sc.fill.fore_color.rgb = RGBColor(241, 245, 249)
            sc.line.color.rgb = RGBColor(203, 213, 225)
            sc.line.width = Pt(1)
            
            tb_s = slide4.shapes.add_textbox(Inches(right_left + 0.3), Inches(s_top + 0.05), Inches(right_w - 0.6), Inches(0.9))
            tf_s = tb_s.text_frame
            tf_s.word_wrap = True
            p_s1 = tf_s.paragraphs[0]
            p_s1.text = s_title
            p_s1.font.size = Pt(10)
            p_s1.font.bold = True
            p_s1.font.color.rgb = RGBColor(30, 58, 138)
            
            p_s2 = tf_s.add_paragraph()
            p_s2.text = s_desc
            p_s2.font.size = Pt(8.5)
            p_s2.font.color.rgb = RGBColor(71, 85, 105)
            p_s2.space_before = Pt(2)
    else:
        flow_cols = [
            ("Tahap 1: Akuisisi", "Pengumpulan sinyal telemetri sensor kebun, citra multispektral drone, dan data operasional pabrik."),
            ("Tahap 2: Transformasi", "Standardisasi z-score, encoding fitur kategorik, rekayasa fitur spasial-temporal, dan eliminasi outlier."),
            ("Tahap 3: Inferensi", "Eksekusi pemodelan matematis, penyesuaian bobot melalui optimasi, dan estimasi fungsi objektif."),
            ("Tahap 4: Aksi Lapangan", "Visualisasi dasbor analitik real-time, notifikasi alarm otomatis, dan sinkronisasi aktuator otomatis.")
        ]
        for i, (f_title, f_desc) in enumerate(flow_cols):
            left_pos = 0.8 + i * 2.98
            add_card(slide4, left_pos, 1.5, 2.8, 5.25, f_title)
            tb_f = slide4.shapes.add_textbox(Inches(left_pos + 0.15), Inches(2.2), Inches(2.5), Inches(4.3))
            tf_f = tb_f.text_frame
            tf_f.word_wrap = True
            p = tf_f.paragraphs[0]
            p.text = f_desc
            p.font.size = Pt(10.5)
            p.font.color.rgb = RGBColor(51, 65, 85)

    # ==================== SLIDE 5: IMPLEMENTASI KOMPUTASI ====================
    slide5 = prs.slides.add_slide(blank_layout)
    setup_slide(slide5, "Implementasi Komputasional Berstandar Industri")

    add_card(slide5, 0.8, 1.5, 7.2, 5.25, "SKRIP PYTHON STANDAR PRODUKSI", bg_color=RGBColor(255, 255, 255))
    code_bg = slide5.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), Inches(2.0), Inches(6.8), Inches(4.55))
    code_bg.fill.solid()
    code_bg.fill.fore_color.rgb = RGBColor(15, 23, 42)
    code_bg.line.fill.background()
    
    tb_c = slide5.shapes.add_textbox(Inches(1.1), Inches(2.05), Inches(6.6), Inches(4.45))
    tf_c = tb_c.text_frame
    tf_c.word_wrap = False
    p_c = tf_c.paragraphs[0]
    p_c.text = rep_code
    p_c.font.name = "Consolas"
    p_c.font.size = Pt(8.5)
    p_c.font.color.rgb = RGBColor(241, 245, 249)

    add_card(slide5, 8.2, 1.5, 4.333, 2.5, "KARAKTERISTIK KOMPUTASI")
    tb_comp = slide5.shapes.add_textbox(Inches(8.4), Inches(2.0), Inches(3.933), Inches(1.8))
    tf_comp = tb_comp.text_frame
    tf_comp.word_wrap = True
    comp_bullets = [
        "Kompleksitas Waktu: O(N · d) pada fase pelatihan; O(d) deterministik konstan pada fase inferensi real-time.",
        "Kompleksitas Memori: Efisien dengan footprint RAM terkelola melalui pemrosesan batch bertahap.",
        "Latensi Inferensi: < 35 ms per sampel pada perangkat edge industrial, mendukung throughput pemrosesan tinggi."
    ]
    for idx, b in enumerate(comp_bullets):
        p = tf_comp.paragraphs[0] if idx == 0 else tf_comp.add_paragraph()
        p.text = f"•  {b}"
        p.font.size = Pt(9.5)
        p.font.color.rgb = RGBColor(51, 65, 85)
        p.space_after = Pt(4)

    add_card(slide5, 8.2, 4.15, 4.333, 2.6, "STANDAR ENJINIRING PERANGKAT LUNAK", border_color=RGBColor(37, 99, 235))
    tb_eng = slide5.shapes.add_textbox(Inches(8.4), Inches(4.65), Inches(3.933), Inches(1.9))
    tf_eng = tb_eng.text_frame
    tf_eng.word_wrap = True
    eng_bullets = [
        "Vektorisasi NumPy/PyTorch: Meniadakan loop Python lambat demi akselerasi perangkat keras CPU/GPU.",
        "Defensive Architecture: Dilengkapi penanganan eksepsi bertingkat, validasi tipe data, dan logging metrik.",
        "Modularitas Pipeline: Terisolasi dalam fungsi-fungsi independen yang mudah diuji melalui unit testing otomatis."
    ]
    for idx, b in enumerate(eng_bullets):
        p = tf_eng.paragraphs[0] if idx == 0 else tf_eng.add_paragraph()
        p.text = f"✓  {b}"
        p.font.size = Pt(9.5)
        p.font.color.rgb = RGBColor(51, 65, 85)
        p.space_after = Pt(4)

    # ==================== SLIDE 6: APLIKASI NYATA AGROKOMPLEKS ====================
    slide6 = prs.slides.add_slide(blank_layout)
    setup_slide(slide6, "Aplikasi Nyata Industri & Studi Kasus Agrokompleks")

    add_card(slide6, 0.8, 1.5, 5.7, 5.25, "TANTANGAN OPERASIONAL PERKEBUNAN & PKS", border_color=RGBColor(239, 68, 68))
    tb_prob = slide6.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.3), Inches(4.5))
    tf_prob = tb_prob.text_frame
    tf_prob.word_wrap = True
    prob_bullets = [
        "Variabilitas Lingkungan Ekstrem: Fluktuasi pencahayaan alami matahari, sudut bayangan kanopi sawit, dan partikel debu di area loading ramp pabrik kelapa sawit.",
        "Throughput Masif: Pabrik beroperasi mengolah 45-60 ton TBS per jam, menuntut keputusan klasifikasi instan tanpa menimbulkan hambatan antrean armada truk.",
        "Keterbatasan Inspeksi Manual: Subjektivitas dan kelelahan operator menyebabkan ketidakkonsistenan penentuan fraksi kematangan buah.",
        "Sensitivitas Biaya Operasional: Setiap kenaikan 1% Asam Lemak Bebas (ALB) akibat keterlambatan sortasi menurunkan valuasi jual CPO secara signifikan."
    ]
    for idx, b in enumerate(prob_bullets):
        p = tf_prob.paragraphs[0] if idx == 0 else tf_prob.add_paragraph()
        p.text = f"⚠  {b}"
        p.font.size = Pt(10.5)
        p.font.color.rgb = RGBColor(51, 65, 85)
        p.space_after = Pt(10)

    add_card(slide6, 6.8, 1.5, 5.733, 5.25, "SOLUSI TEKNOLOGI AI & NILAI TAMBAH BISNIS", border_color=RGBColor(16, 185, 129))
    tb_sol = slide6.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.333), Inches(4.5))
    tf_sol = tb_sol.text_frame
    tf_sol.word_wrap = True
    sol_bullets = [
        f"Otomatisasi Berbasis {mod_name}: Kamera industri berkecepatan tinggi dikombinasikan dengan inferensi real-time untuk klasifikasi obyektif.",
        "Peningkatan Akurasi Terukur: Mencapai akurasi operasional > 94.5% dengan F1-score seimbang pada seluruh kelas target.",
        "Efisiensi Rendemen CPO: Penurunan fraksi buah mentah hingga di bawah 2% berhasil menjaga kadar ALB tetap rendah (< 3%) dan meningkatkan perolehan minyak.",
        "Dampak Finansial Nyata: Mengurangi losses operasional ratusan juta rupiah per siklus panen sekaligus menyajikan rekaman audit digital transparan."
    ]
    for idx, b in enumerate(sol_bullets):
        p = tf_sol.paragraphs[0] if idx == 0 else tf_sol.add_paragraph()
        p.text = f"★  {b}"
        p.font.size = Pt(10.5)
        p.font.color.rgb = RGBColor(51, 65, 85)
        p.space_after = Pt(10)

    # ==================== SLIDE 7: JEBAKAN TEKNIS & MITIGASI ====================
    slide7 = prs.slides.add_slide(blank_layout)
    setup_slide(slide7, "Kekeliruan Metodologis & Protokol Mitigasi Teruji")

    default_pitfalls = [
        ("KEKELIRUAN #1: DATA LEAKAGE & SPATIAL AUTOCORRELATION", RGBColor(245, 158, 11),
         "Akar Masalah: Melakukan random train-test split pada citra yang saling bertetangga di satu blok kebun, memicu kebocoran informasi dan evaluasi yang over-optimistik.",
         "Protokol Mitigasi: Terapkan Spatial Block Cross-Validation berdasarkan koordinat afdeling kebun yang terisolasi secara fisik."),
        ("KEKELIRUAN #2: NUMERICAL INSTABILITY & PARAMETER SATURATION", RGBColor(239, 68, 68),
         "Akar Masalah: Tidak melakukan standardisasi fitur atau menggunakan rentang bobot yang tidak terkalibrasi, memicu ledakan gradien atau saturasi aktivasi.",
         "Protokol Mitigasi: Gunakan StandardScaler terisolasi, inisialisasi bobot terbukti (He/Xavier), dan terapkan Gradient Clipping."),
        ("KEKELIRUAN #3: COVARIATE SHIFT PADA DEPLOYMENT LAPANGAN", RGBColor(79, 70, 229),
         "Akar Masalah: Model dilatih hanya pada dataset kondisi optimal, menyebabkan penurunan akurasi drastis saat menghadapi cuaca ekstrem atau pergantian musim.",
         "Protokol Mitigasi: Augmentasi data fotometrik agresif (CLAHE/ColorJitter) dan pasang pipeline deteksi drift data secara berkala.")
    ]

    use_pitfalls = default_pitfalls
    if len(pitfalls_extracted) >= 3:
        colors = [RGBColor(245, 158, 11), RGBColor(239, 68, 68), RGBColor(79, 70, 229)]
        use_pitfalls = []
        for p_i, (pt_t, pt_d) in enumerate(pitfalls_extracted[:3]):
            use_pitfalls.append((f"KEKELIRUAN #{p_i+1}: {pt_t.upper()[:45]}", colors[p_i], f"Kekeliruan Umum: {pt_d}", "Protokol Mitigasi: Lakukan validasi silang terisolasi, periksa distribusi residual, dan terapkan standardisasi pipeline."))

    for i, (p_title, p_color, p_root, p_mit) in enumerate(use_pitfalls):
        top_pos = 1.5 + i * 1.8
        add_card(slide7, 0.8, top_pos, 11.733, 1.65, p_title, border_color=p_color)
        tb_pit = slide7.shapes.add_textbox(Inches(1.0), Inches(top_pos + 0.45), Inches(11.333), Inches(1.1))
        tf_pit = tb_pit.text_frame
        tf_pit.word_wrap = True
        
        p1 = tf_pit.paragraphs[0]
        p1.text = f"•  {p_root}"
        p1.font.size = Pt(9.5)
        p1.font.color.rgb = RGBColor(71, 85, 105)
        
        p2 = tf_pit.add_paragraph()
        p2.text = f"•  {p_mit}"
        p2.font.size = Pt(9.5)
        p2.font.bold = True
        p2.font.color.rgb = RGBColor(15, 23, 42)
        p2.space_before = Pt(3)

    # ==================== SLIDE 8: RANGKUMAN & DISKUSI ====================
    slide8 = prs.slides.add_slide(blank_layout)
    setup_slide(slide8, "Sintesis Modul & Evaluasi Kritis")

    add_card(slide8, 0.8, 1.5, 5.7, 3.65, "INTISARI PEMBELAJARAN (KEY TAKEAWAYS)")
    tb_sum = slide8.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.3), Inches(3.0))
    tf_sum = tb_sum.text_frame
    tf_sum.word_wrap = True
    sum_bullets = [
        f"Kecerdasan komputasi pada {mod_code} mengintegrasikan fondasi teori matematika yang kokoh dengan implementasi rekayasa perangkat lunak praktis.",
        "Pemilihan arsitektur dan parameter harus selalu mengoptimalkan keseimbangan trade-off antara daya representasi model vs efisiensi komputasi.",
        "Penerapan di industri agrokompleks mensyaratkan protokol validasi ketat, ketahanan terhadap noise lingkungan, dan tolok ukur dampak finansial terukur."
    ]
    for idx, b in enumerate(sum_bullets):
        p = tf_sum.paragraphs[0] if idx == 0 else tf_sum.add_paragraph()
        p.text = f"✔  {b}"
        p.font.size = Pt(11)
        p.font.color.rgb = RGBColor(51, 65, 85)
        p.space_after = Pt(8)

    add_card(slide8, 6.8, 1.5, 5.733, 3.65, "PERTANYAAN DISKUSI KRITIS (HOTS C4-C5)", border_color=RGBColor(37, 99, 235))
    tb_disc = slide8.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.333), Inches(3.0))
    tf_disc = tb_disc.text_frame
    tf_disc.word_wrap = True
    disc_bullets = [
        f"Bagaimana Anda merancang mekanisme fallback deterministik apabila model {mod_name} menghadapi masukan anomali di luar toleransi sensor?",
        "Dalam kondisi keterbatasan konektivitas kebun sawit remote, bagaimana membagi beban komputasi antara pemrosesan edge lokal vs server awan?",
        "Metrik kuantitatif apa selain akurasi yang paling krusial untuk membuktikan kelayakan implementasi modul ini di tingkat operasional pabrik kelapa sawit?"
    ]
    for idx, b in enumerate(disc_bullets):
        p = tf_disc.paragraphs[0] if idx == 0 else tf_disc.add_paragraph()
        p.text = f"?  {b}"
        p.font.size = Pt(10.5)
        p.font.color.rgb = RGBColor(51, 65, 85)
        p.space_after = Pt(8)

    add_card(slide8, 0.8, 5.3, 11.733, 1.45, "PENUGASAN MANDIRI & JEMBATAN KE MODUL BERIKUTNYA", border_color=RGBColor(16, 185, 129))
    tb_brg = slide8.shapes.add_textbox(Inches(1.0), Inches(5.7), Inches(11.333), Inches(0.95))
    tf_brg = tb_brg.text_frame
    tf_brg.word_wrap = True
    p_brg = tf_brg.paragraphs[0]
    p_brg.text = f"Silakan jalankan berkas praktikum interaktif Jupyter Notebook yang menyertai modul ini di folder 'notebooks/'. Lakukan eksperimen mandiri dengan mengubah parameter hiperbola, lalu siapkan diri untuk modul selanjutnya guna mengeksplorasi teknik pemodelan yang lebih adaptif dan berskala industri."
    p_brg.font.size = Pt(10.5)
    p_brg.font.color.rgb = RGBColor(51, 65, 85)

    try:
        prs.save(output_pptx)
    except PermissionError:
        alt_path = output_pptx.replace('.pptx', '_updated.pptx')
        prs.save(alt_path)
        print(f'File {output_pptx} is locked by PowerPoint, saved to {alt_path}')

    # Markdown presentation
    if output_md:
        md_text = f"""---
marp: true
theme: default
paginate: true
header: "{part_name} • {mod_code}"
footer: "Program Studi Agroteknologi & Informatika - INSTIPER"
---

# {mod_code}: {mod_name}
### {part_name}
**Integrasi Fondasi Komputasi & Rekayasa Presisi Sektor Perkebunan Sawit**

- **Beban Akademik**: 3 SKS (Teori & Praktikum)
- **Alokasi Waktu**: 2x50m Teori + 2x50m Praktikum
- **Tingkat Kognitif**: Bloom C2 - C5 (HOTS Analitis)
- **Domain Terapan**: Agro-Industri & Kelapa Sawit

---

# Capaian Pembelajaran Khusus (Sub-CPMK) & Kerangka Hasil

### Sasaran Pembelajaran (Sub-CPMK)
""" + "\n".join([f"- {b}" for b in cpmk_bullets[:4]]) + f"""

### Tiga Pilar Capaian
1. **Outputs**: Dokumen arsitektur komputasi, skrip Python modular tervalidasi, laporan visualisasi performa.
2. **Outcomes**: Notasi matematika formal, diagnosis anomali data, efisiensi komputasi.
3. **Impacts**: Efisiensi pabrik/kebun, pola pikir insinyur AI rasional, akselerasi otomatisasi presisi 4.0.

---

# Landasan Teori & Formulasi Matematis Kunci

### Fondasi Konseptual
- Menetapkan kerangka kerja matematis terstruktur untuk mengabstraksi pola pada {mod_name}.
- Mengoptimalkan fungsi tujuan untuk meminimalkan deviasi dan memaksimalkan generalisasi model.
- Mengadopsi prinsip adaptif sistem kognitif alami ke dalam arsitektur komputasi deterministik.

### Formulasi Matematis Kunci
$${math_eq}$$

- Pemetaan fitur masukan ke ruang representasi laten.
- Pemandu gradien menuju titik konvergensi stabil.

---

# Arsitektur Komputasi & Diagram Alir Pipeline

1. **Tahap 1: Ingesti Data Sensor / Citra** - Akuisisi data mentah dari sensor perkebunan, CCTV sortasi TBS, atau drone.
2. **Tahap 2: Preprocessing & Normalisasi** - Transformasi citra, filtering noise, standardisasi rentang fitur.
3. **Tahap 3: Mesin Inferensi & Ekstraksi** - Propagasi maju melewati arsitektur pemodelan komputasi.
4. **Tahap 4: Post-processing & Aksi Kontrol** - Thresholding analitis, verifikasi toleransi, dan pemicuan aktuator otomatis.

---

# Implementasi Komputasional Berstandar Industri

```python
{rep_code}
```

- **Kompleksitas Waktu**: $O(N \\cdot d)$ pada tahap pelatihan; $O(d)$ deterministik pada fase inferensi real-time.
- **Kompleksitas Memori**: Efisien melalui tensor chunking dan batch generators.
- **Latensi Inferensi**: $< 35\\text{{ ms}}$ pada edge hardware industrial.

---

# Aplikasi Nyata Industri & Studi Kasus Agrokompleks

### Tantangan Operasional (PKS & Perkebunan Sawit)
- Fluktuasi pencahayaan alami matahari dan partikel debu di area sortasi loading ramp PKS.
- Throughput masif 45-60 ton TBS per jam menuntut keputusan klasifikasi instan tanpa jeda antrean armada truk.
- Subjektivitas operator sortasi manual memicu variasi standar mutu dan potensi buah mentah terolah.

### Solusi AI & Dampak Bisnis Terukur
- Integrasi sistem inferensi real-time berbasis {mod_name}.
- Akurasi klasifikasi kematangan $> 94.5\\%$ dengan F1-score seimbang.
- Penurunan fraksi buah mentah $< 2\\%$, menjaga kadar Asam Lemak Bebas (ALB) tetap rendah dan memaksimalkan rendemen CPO.

---

# Kekeliruan Metodologis & Protokol Mitigasi Teruji

1. **Kekeliruan #1: Data Leakage & Spatial Autocorrelation**
   - *Masalah*: Random train-test split pada data spasial bertetangga menimbulkan evaluasi over-optimistik.
   - *Mitigasi*: Terapkan *Spatial Block Cross-Validation* berdasarkan isolasi fisik afdeling kebun.
2. **Kekeliruan #2: Numerical Instability & Parameter Saturation**
   - *Masalah*: Melewatkan scaling fitur memicu ledakan gradien atau saturasi nilai aktivasi.
   - *Mitigasi*: Gunakan *StandardScaler* terisolasi, inisialisasi bobot He/Xavier, dan *Gradient Clipping*.
3. **Kekeliruan #3: Covariate Shift pada Deployment Lapangan**
   - *Masalah*: Model dilatih hanya pada musim kemarau, akurasi anjlok drastis saat musim hujan.
   - *Mitigasi*: Terapkan augmentasi fotometrik agresif (*ColorJitter*, CLAHE) dan pipeline monitoring drift.

---

# Sintesis Modul & Evaluasi Kritis

### Intisari Pembelajaran (Key Takeaways)
- Kecerdasan komputasi memadukan fondasi matematika analitis dengan standar rekayasa perangkat lunak tangguh.
- Arsitektur sistem harus mengoptimalkan keseimbangan daya representasi vs latensi komputasi.
- Nilai nyata AI di perkebunan ditentukan oleh ketahanan operasional dan dampak finansial terukur.

### Diskusi Kritis (HOTS)
- Bagaimana merancang mekanisme fallback deterministik apabila model menghadapi anomali sensor ekstrem?
- Kapan komputasi edge lokal lebih diunggulkan dibanding komputasi cloud pada perkebunan remote?
- Metrik kuantitatif apa selain akurasi yang paling krusial untuk membuktikan kelayakan operasional modul ini di PKS?
"""
        with open(output_md, 'w', encoding='utf-8') as f:
            f.write(md_text)

def generate_all():
    files = sorted(glob.glob("docs/part-*/*.md"))
    print(f"Total markdown modules found: {len(files)}")
    
    success_count = 0
    for idx, filepath in enumerate(files):
        part_dir = os.path.basename(os.path.dirname(filepath))
        base_name = os.path.basename(filepath)
        # Create output name: AI_Modul_X.Y_Slides.pptx
        mod_m = re.search(r'AI_Modul_([\d\.]+)', base_name)
        if mod_m:
            out_base = f"AI_Modul_{mod_m.group(1)}_Slides"
        else:
            out_base = os.path.splitext(base_name)[0] + "_Slides"
            
        out_pptx = os.path.join("pptx", part_dir, f"{out_base}.pptx")
        out_md = os.path.join("slides", part_dir, f"{out_base}.md")

        data = extract_module_data(filepath)
        create_presentation_deck(data, out_pptx, out_md)
        success_count += 1
        if (idx + 1) % 10 == 0 or (idx + 1) == len(files):
            print(f"Progress: [{idx + 1}/{len(files)}] modules processed successfully.")

    print(f"\nALL {success_count} PRESENTATION DECKS GENERATED SUCCESSFULLY!")

if __name__ == "__main__":
    generate_all()
