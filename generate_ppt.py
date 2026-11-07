"""
Script to generate the Master Technical Presentation for:
In-Silico ADMET Intelligence & Molecular Property Prediction Platform
Generates: Molecular_Property_Prediction_Presentation.pptx
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = Presentation()
    # Set 16:9 widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6] # blank layout

    # Colors
    NAVY = RGBColor(15, 23, 42)       # #0F172A
    DEEP_BLUE = RGBColor(30, 41, 59)  # #1E293B
    ACCENT_BLUE = RGBColor(2, 132, 199)# #0284C7 (Cyan / Sky)
    LIGHT_BG = RGBColor(248, 250, 252) # #F8FAFC
    CARD_BG = RGBColor(255, 255, 255)
    BORDER_COLOR = RGBColor(226, 232, 240)
    DARK_TEXT = RGBColor(15, 23, 42)
    MUTED_TEXT = RGBColor(100, 116, 139)
    WHITE = RGBColor(255, 255, 255)
    EMERALD = RGBColor(5, 150, 105)
    ROSE = RGBColor(225, 29, 72)
    GOLD = RGBColor(217, 119, 6)

    results_dir = os.path.abspath("results")

    def add_header(slide, tag_text, title_text, subtitle_text=""):
        # Top banner background
        header_box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.15))
        header_box.fill.solid()
        header_box.fill.fore_color.rgb = NAVY
        header_box.line.color.rgb = ACCENT_BLUE
        header_box.line.width = Pt(1.5)

        # Header text
        tf = header_box.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.8)
        tf.margin_top = Inches(0.12)
        tf.margin_right = Inches(0.8)
        tf.margin_bottom = Inches(0.08)

        # Tag paragraph
        p_tag = tf.paragraphs[0]
        p_tag.text = tag_text.upper()
        p_tag.font.name = "Calibri"
        p_tag.font.size = Pt(10)
        p_tag.font.bold = True
        p_tag.font.color.rgb = ACCENT_BLUE

        # Title paragraph
        p_title = tf.add_paragraph()
        p_title.text = title_text
        p_title.font.name = "Calibri"
        p_title.font.size = Pt(20)
        p_title.font.bold = True
        p_title.font.color.rgb = WHITE

        # Subtitle paragraph if present
        if subtitle_text:
            p_sub = tf.add_paragraph()
            p_sub.text = subtitle_text
            p_sub.font.name = "Calibri"
            p_sub.font.size = Pt(11)
            p_sub.font.color.rgb = RGBColor(148, 163, 184)

    def add_footer(slide, slide_num):
        footer_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.1), Inches(11.733), Inches(0.35))
        tf = footer_box.text_frame
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = f"B.Tech CSE (AI & ML) | Candidate: M. Pramod (24BAI1417) | Slide {slide_num}"
        p.font.name = "Calibri"
        p.font.size = Pt(9)
        p.font.color.rgb = MUTED_TEXT

    def add_card(slide, left, top, width, height, title="", bg_color=CARD_BG, border_color=BORDER_COLOR):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1)

        if title:
            tb = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.15), width - Inches(0.4), Inches(0.4))
            tf = tb.text_frame
            tf.word_wrap = True
            tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
            p = tf.paragraphs[0]
            p.text = title
            p.font.name = "Calibri"
            p.font.size = Pt(14)
            p.font.bold = True
            p.font.color.rgb = NAVY
        return card

    def add_bullet_list(slide, left, top, width, height, items, font_size=11):
        tb = slide.shapes.add_textbox(left, top, width, height)
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        for i, item in enumerate(items):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.space_after = Pt(6)
            p.level = 0
            
            # Support bold header in bullet: ("Header: ", "description...")
            if isinstance(item, tuple):
                r1 = p.add_run()
                r1.text = "• " + item[0]
                r1.font.bold = True
                r1.font.name = "Calibri"
                r1.font.size = Pt(font_size)
                r1.font.color.rgb = NAVY

                r2 = p.add_run()
                r2.text = item[1]
                r2.font.bold = False
                r2.font.name = "Calibri"
                r2.font.size = Pt(font_size)
                r2.font.color.rgb = DARK_TEXT
            else:
                r = p.add_run()
                r.text = "• " + str(item)
                r.font.name = "Calibri"
                r.font.size = Pt(font_size)
                r.font.color.rgb = DARK_TEXT

    def add_notes(slide, notes_content):
        notes_slide = slide.notes_slide
        tf = notes_slide.notes_text_frame
        tf.text = notes_content

    # -------------------------------------------------------------------------
    # SLIDE 1: Title Slide (Dark Theme Hero)
    # -------------------------------------------------------------------------
    slide1 = prs.slides.add_slide(blank_layout)
    bg1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = NAVY
    bg1.line.fill.background()

    # Inner glowing card
    card1 = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.8), Inches(11.733), Inches(5.9))
    card1.fill.solid()
    card1.fill.fore_color.rgb = DEEP_BLUE
    card1.line.color.rgb = ACCENT_BLUE
    card1.line.width = Pt(2)

    # Title content
    tb1 = slide1.shapes.add_textbox(Inches(1.2), Inches(1.1), Inches(10.933), Inches(5.3))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "BACHELOR OF TECHNOLOGY — CAPSTONE PROJECT DEFENSE"
    p.font.name = "Calibri"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = ACCENT_BLUE

    p = tf1.add_paragraph()
    p.text = "Molecular Property Prediction &\nIn-Silico ADMET Intelligence Platform"
    p.font.name = "Calibri"
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.space_after = Pt(12)

    p = tf1.add_paragraph()
    p.text = "An End-to-End Multi-Endpoint Machine Learning Architecture for Aqueous Solubility (LogS), Lipophilicity, Pharmacokinetics, Toxicity Profiling, Local Explainability (XAI), and Generative Lead Optimization"
    p.font.name = "Calibri"
    p.font.size = Pt(13)
    p.font.color.rgb = RGBColor(203, 213, 225)
    p.space_after = Pt(20)

    # Key highlight metrics badge row
    p = tf1.add_paragraph()
    p.text = "★ KEY RESULTS: Solubility R² = 0.9029 | ClinTox AUC = 0.9249 | BBBP AUC = 0.9042 | 2,068D Hybrid Features | 14-Page Dashboard | FastAPI REST"
    p.font.name = "Calibri"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = EMERALD
    p.space_after = Pt(28)

    p = tf1.add_paragraph()
    p.text = "PROJECT TEAM & ACADEMIC CREDENTIALS:"
    p.font.name = "Calibri"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = RGBColor(148, 163, 184)

    p = tf1.add_paragraph()
    p.text = "• M. Pramod  —  Reg. No: 24BAI1417\nSchool of Computer Science & Engineering (SCOPE) | Artificial Intelligence & Machine Learning"
    p.font.name = "Calibri"
    p.font.size = Pt(12)
    p.font.color.rgb = WHITE

    add_notes(slide1, """[HOW TO START YOUR PRESENTATION TO SIR]:
"Good morning, respected Sir. Today, I am proud to present my project: 'Molecular Property Prediction & In-Silico ADMET Intelligence Platform'.

In this project, we address one of the most critical challenges in modern drug discovery: predicting whether a newly designed small-molecule drug will successfully dissolve in human blood, reach its target organ, and be safe without toxic side effects.

We have engineered an end-to-end AI platform that takes raw chemical structures, transforms them into a 2,068-dimensional hybrid feature space, and achieves state-of-the-art predictive accuracy with R² = 0.9029 on solubility and ROC-AUC over 92% on clinical toxicity. Beyond predictions, our system explains WHY a molecule behaves the way it does using Explainable AI (XAI) and automatically suggests chemical modifications to fix liabilities using Generative AI. We also built an interactive 14-page research dashboard and a production FastAPI microservice.

Allow us to walk you step-by-step through the pharmaceutical problem, the cheminformatics architecture, our empirical machine learning benchmarks, and the live system."
""")

    # -------------------------------------------------------------------------
    # SLIDE 2: The Problem & Clinical Motivation
    # -------------------------------------------------------------------------
    slide2 = prs.slides.add_slide(blank_layout)
    add_header(slide2, "Background & Problem Formulation", "The Pharmaceutical Drug Discovery Crisis", "Why 90% of drug candidates fail and why computational In-Silico screening is vital")
    add_footer(slide2, 2)

    # 3 Cards across the bottom
    w3 = Inches(3.64)
    h_card = Inches(5.4)
    y_card = Inches(1.4)

    # Card 1: The Attrition Crisis
    add_card(slide2, Inches(0.8), y_card, w3, h_card, "1. The Attrition Crisis", CARD_BG, ROSE)
    add_bullet_list(slide2, Inches(1.0), y_card + Inches(0.6), w3 - Inches(0.4), h_card - Inches(0.8), [
        ("40%+ Preclinical Failure: ", "Over 40% of newly synthesized small molecules fail preclinically due to poor aqueous solubility."),
        ("80% Clinical Attrition: ", "Over 80% of clinical trial failures stem from poor pharmacokinetics (ADMET) and organ toxicity."),
        ("Enormous Costs: ", "Developing a single approved drug requires $2.6 Billion and 10 to 15 years."),
        ("Late-Stage Disasters: ", "Failing in Phase II/III clinical trials wastes hundreds of millions of dollars that could be prevented.")
    ], 11)

    # Card 2: Why Solubility & ADMET Matter
    add_card(slide2, Inches(4.84), y_card, w3, h_card, "2. The Biological Necessity", CARD_BG, ACCENT_BLUE)
    add_bullet_list(slide2, Inches(5.04), y_card + Inches(0.6), w3 - Inches(0.4), h_card - Inches(0.8), [
        ("Aqueous Solubility (LogS): ", "An oral pill must dissolve in gastrointestinal fluids to enter the bloodstream. Insoluble drugs precipitate out."),
        ("Lipophilicity (LogD): ", "Must balance water solubility with cell membrane penetration."),
        ("Blood-Brain Barrier (BBBP): ", "Determines whether CNS drugs enter the brain or peripheral drugs avoid neurological toxicity."),
        ("Organ Toxicity (ClinTox/p53): ", "Early detection of hepatotoxicity, cardiotoxicity, and DNA mutagenic damage.")
    ], 11)

    # Card 3: The In-Silico Solution
    add_card(slide2, Inches(8.88), y_card, w3, h_card, "3. The In-Silico AI Solution", CARD_BG, EMERALD)
    add_bullet_list(slide2, Inches(9.08), y_card + Inches(0.6), w3 - Inches(0.4), h_card - Inches(0.8), [
        ("Instant Virtual Screening: ", "Screen 100,000+ candidates computationally in seconds before synthesizing a single physical vial in the wet-lab."),
        ("Experimental-Grade Accuracy: ", "Our MAE of ±0.46 log units matches wet-lab assay variability (±0.50 log units)."),
        ("Rational Lead Optimization: ", "Directs chemists to fix molecular liabilities through automated bioisosteric replacement."),
        ("Drastic Cost Reduction: ", "Saves millions of dollars by failing toxic or insoluble molecules virtually at Day 1.")
    ], 11)

    add_notes(slide2, """[HOW TO EXPLAIN SLIDE 2 TO SIR]:
"Sir, to explain why this project is so critical: The pharmaceutical industry currently faces a massive productivity crisis.
1. Bringing one single drug to market takes over 10 to 15 years and costs an average of 2.6 billion dollars.
2. Even worse, more than 40% of molecules synthesized in labs fail immediately because they are insoluble in water, and 80% fail clinical trials due to pharmacokinetic ADMET issues or unexpected toxicity.
3. If an oral drug cannot dissolve in the digestive tract, it cannot be absorbed into systemic circulation, making it biologically useless regardless of how well it binds to the target receptor.
4. Wet-lab synthesis and animal testing for every candidate is too slow and expensive.
5. Our project delivers an 'In-Silico' machine learning platform that screens candidates in milliseconds with accuracy matching wet-lab assays, allowing researchers to weed out failures early."

[EXPECTED QUESTION FROM SIR]: 'Why do we measure solubility as LogS instead of grams per liter?'
[YOUR ANSWER]: 'Sir, solubility spans over 12 orders of magnitude (from 10^-12 mol/L to over 1.0 mol/L). Taking the base-10 logarithm normalizes this exponential variance into a smooth Gaussian distribution suitable for ML regression. Also, pharmacological potency depends on molar concentration (number of molecules binding the target), not physical mass in grams.'""")

    # -------------------------------------------------------------------------
    # SLIDE 3: System Architecture & End-to-End Workflow
    # -------------------------------------------------------------------------
    slide3 = prs.slides.add_slide(blank_layout)
    add_header(slide3, "System Engineering & Computational Pipeline", "End-to-End System Architecture", "Seamless integration from raw chemical SMILES to regulatory preclinical dossier export")
    add_footer(slide3, 3)

    # Left text box (Inches(0.8), Inches(1.4), Inches(5.2), Inches(5.4))
    add_card(slide3, Inches(0.8), Inches(1.4), Inches(5.2), Inches(5.4), "Pipeline Execution Stages", CARD_BG, BORDER_COLOR)
    add_bullet_list(slide3, Inches(1.0), Inches(2.0), Inches(4.8), Inches(4.6), [
        ("1. Input Ingestion: ", "Accepts 1D SMILES strings, 2D interactive canvas drawing (JSME), or batch CSV libraries."),
        ("2. Valence Sanitization: ", "RDKit checks strict chemical valences, aromaticity kekulization, and stereochemical validity."),
        ("3. Hybrid Feature Extraction: ", "Extracts 20 macroscopic descriptors + 2,048-bit Morgan circular fingerprints (ECFP4) -> 2,068D vector."),
        ("4. Multi-Endpoint Inference: ", "Concurrent inference across 5 tuned tree ensembles (Solubility, Lipophilicity, BBBP, ClinTox, Tox21)."),
        ("5. Local XAI Attribution: ", "SimilarityMaps contour heatmaps fusing Crippen LogP and Gasteiger partial charges."),
        ("6. Safety & Rule Compliance: ", "480 PAINS filters, Brenk toxicophores, Lipinski Rule of 5, Veber, CNS MPO."),
        ("7. Generative SAR Optimizer: ", "8 SMARTS bioisostere transforms generate ranked analogs with delta improvements."),
        ("8. Multi-Channel Export: ", "Interactive 14-page dashboard, FastAPI REST endpoints, and PDF/HTML preclinical dossier.")
    ], 10)

    # Right side: Pipeline Architecture Diagram Image
    img_arch = os.path.join(results_dir, "pipeline_architecture_diagram.png")
    if os.path.exists(img_arch):
        slide3.shapes.add_picture(img_arch, Inches(6.2), Inches(1.4), Inches(6.33), Inches(5.4))

    add_notes(slide3, """[HOW TO EXPLAIN SLIDE 3 TO SIR]:
"Sir, this slide displays the high-level system architecture of our entire platform.

1. The pipeline starts with chemical ingestion: The user can input a SMILES string, pick from 45 FDA reference drugs, or draw any novel chemical structure directly using our embedded JSME 2D ChemDraw sketcher.
2. The molecule undergoes strict chemical sanitization via RDKit to ensure correct valence, aromaticity, and stereochemistry.
3. We then transform the molecule into a 2,068-dimensional hybrid feature vector combining 20 whole-molecule physicochemical descriptors with 2,048 topological Morgan circular fingerprint bits.
4. This hybrid vector is dispatched to our 5 production machine learning models concurrently.
5. In parallel, our explainability engine generates 2D atom-level contour maps showing which atoms hurt or help solubility.
6. The molecule is screened against 480 PAINS filters and drug-likeness rules.
7. If the molecule has liabilities, our generative bioisosteric SAR engine suggests 8 medicinal chemistry transformations.
8. All results are exposed through a 14-page Streamlit research dashboard, a production FastAPI microservice, and a 1-click downloadable regulatory dossier."

[EXPECTED QUESTION FROM SIR]: 'What happens if a user inputs an invalid chemical structure?'
[YOUR ANSWER]: 'Sir, the RDKit sanitization module validates nitrogen, carbon, and oxygen valences. If an invalid structure like 5-valent carbon is submitted, the system catches the exception and provides clear feedback without crashing.'""")

    # -------------------------------------------------------------------------
    # SLIDE 4: Cheminformatics & 2,068D Hybrid Feature Engineering
    # -------------------------------------------------------------------------
    slide4 = prs.slides.add_slide(blank_layout)
    add_header(slide4, "Feature Representation & Cheminformatics", "The 2,068-Dimensional Hybrid Feature Representation", "Synergizing macroscopic thermodynamics with fine localized topological fingerprints")
    add_footer(slide4, 4)

    # Left Card: 20 Macroscopic Descriptors
    w_half = Inches(5.6)
    add_card(slide4, Inches(0.8), Inches(1.4), w_half, Inches(5.4), "A. 20 Macroscopic Physicochemical Descriptors", CARD_BG, ACCENT_BLUE)
    add_bullet_list(slide4, Inches(1.0), Inches(2.0), w_half - Inches(0.4), Inches(4.6), [
        ("Molecular Weight (MolWt): ", "Measures total mass; larger molecules have higher crystalline lattice packing energies."),
        ("Wildman-Crippen LogP: ", "Octanol-water partition coefficient measuring whole-molecule lipophilicity and hydrophobicity."),
        ("TPSA (Polar Surface Area): ", "Topological polar surface area (Å²); quantifies polar hydrogen-bonding interaction with water."),
        ("H-Bond Donors & Acceptors: ", "Counts of -OH/-NH donors and O/N acceptors governing aqueous hydration enthalpy."),
        ("Ring Topology: ", "Ring count, aromatic ring count, and aliphatic ring count."),
        ("Rotatable Bonds: ", "Quantifies conformational flexibility and entropic penalty upon target binding."),
        ("Fraction CSP3 (Fsp3): ", "Carbon saturation ratio (C_sp3 / C_total); higher Fsp3 increases 3D spatial complexity and clinical success."),
        ("Stoichiometry & Ionization: ", "Heavy atom count, heteroatom count, net formal charge, and specific halogen counts (F, Cl, Br, I).")
    ], 10.5)

    # Right Card: 2,048-bit Morgan Fingerprints
    add_card(slide4, Inches(6.8), Inches(1.4), w_half, Inches(5.4), "B. 2,048-bit Morgan Circular Fingerprints (ECFP4)", CARD_BG, EMERALD)
    add_bullet_list(slide4, Inches(7.0), Inches(2.0), w_half - Inches(0.4), Inches(4.6), [
        ("Algorithmic Basis: ", "Extended Connectivity Fingerprints (ECFP4 equivalent) based on the Morgan circular algorithm."),
        ("Radial Neighborhoods (r=2): ", "For every heavy atom, calculates iterative circular environments up to 4 bonds across."),
        ("Hashing Invariant: ", "Encodes atomic number, degree, formal charge, number of hydrogens, and aromaticity into unique 32-bit hashes."),
        ("Bit-Vector Projection: ", "Hashes mapped into a fixed 2,048-length binary vector using modulo hashing: bit = hash(substructure) % 2048."),
        ("Why Descriptors Alone Fail: ", "Two isomers can have identical molecular weight and LogP, but completely different functional group connectivity."),
        ("Why Fingerprints Alone Fail: ", "Sparse bit vectors identify fragments but lack global thermodynamic context of molecular mass and bulk."),
        ("The Hybrid Synergy (2,068D): ", "Fuses macroscopic bulk thermodynamics with localized structural motifs to achieve maximum accuracy.")
    ], 10.5)

    add_notes(slide4, """[HOW TO EXPLAIN SLIDE 4 TO SIR]:
"Sir, the core innovation in our feature engineering is the 2,068-dimensional hybrid representation.

In machine learning for chemistry, standard representations often fail:
- If we only use 20 physical descriptors like Molecular Weight and LogP, the model understands the overall size and polarity of the molecule, but it is completely blind to isomer differences and specific functional group attachments. Two completely different chemical structures can have the exact same Molecular Weight and LogP!
- On the other hand, if we only use 2,048 Morgan circular fingerprints (ECFP4), the model detects specific substructures (like benzene rings or amino groups), but it loses the global scaling context of overall molecular bulk and crystalline packing energy.

Therefore, we concatenated both: 20 macroscopic descriptors + 2,048 Morgan circular fingerprint bits = 2,068 hybrid features. This allows our machine learning algorithms to simultaneously evaluate global thermodynamics and fine localized chemical topology."

[EXPECTED QUESTION FROM SIR]: 'What does the radius r=2 mean in Morgan Fingerprints?'
[YOUR ANSWER]: 'Sir, radius r=2 means the algorithm examines paths up to 2 bonds out from each central atom in all directions. That covers a circular diameter of 4 bonds across, which corresponds to the standard ECFP4 fingerprint used in modern pharmaceutical research.'""")

    # -------------------------------------------------------------------------
    # SLIDE 5: Empirical Ablation Study — Feature Representation Benchmark
    # -------------------------------------------------------------------------
    slide5 = prs.slides.add_slide(blank_layout)
    add_header(slide5, "Experimental Validation & Ablation Study", "Empirical Proof: Why the 2,068D Hybrid Representation is Essential", "Ablation study rigorously comparing Fingerprints Only, Descriptors Only, and the Hybrid Space")
    add_footer(slide5, 5)

    # Left side: Table & Insights
    add_card(slide5, Inches(0.8), Inches(1.4), Inches(5.5), Inches(5.4), "Empirical Ablation Benchmark", CARD_BG, BORDER_COLOR)
    add_bullet_list(slide5, Inches(1.0), Inches(2.0), Inches(5.1), Inches(4.6), [
        ("Morgan Fingerprints Only (2,048D): ", "Test MAE = 0.9649 | Test RMSE = 1.3065 | Test R² = 0.6389.\nScientific Finding: Poor performance. High sparsity without global size/mass context limits predictive power."),
        ("Physicochemical Descriptors Only (20D): ", "Test MAE = 0.4871 | Test RMSE = 0.7182 | Test R² = 0.8909.\nScientific Finding: Strong baseline because LogP and MW strongly correlate with solubility, but fails on structural isomers."),
        ("Hybrid Representation (2,068D): ", "Test MAE = 0.4628 | Test RMSE = 0.6775 | Test R² = 0.9029.\nScientific Finding: Optimal performance across all metrics! Achieves the lowest error and highest explained variance."),
        ("Empirical Conclusion: ", "Combining macroscopic descriptors with circular fingerprints reduces prediction error by 52% compared to fingerprints alone and improves R² past the prestigious 0.90 barrier.")
    ], 10.5)

    # Right side: Feature representation comparison chart image
    img_rep = os.path.join(results_dir, "feature_representation_comparison_chart.png")
    if os.path.exists(img_rep):
        slide5.shapes.add_picture(img_rep, Inches(6.6), Inches(1.4), Inches(5.9), Inches(5.4))

    add_notes(slide5, """[HOW TO EXPLAIN SLIDE 5 TO SIR]:
"Sir, in scientific research, one should never assume a feature set is better without empirical proof. On this slide, we present our ablation study where we rigorously tested three feature representations using the exact same Extra Trees algorithm on held-out test data:

1. Look at the blue bars on the right chart: When using Morgan Fingerprints alone (2,048 bits), the model achieved R² of only 0.6389 with a large error (MAE = 0.96 log units). It lacks the global molecular context.
2. When using the 20 Descriptors alone, R² jumped to 0.8909. This proves that macroscopic features like LogP and Molecular Weight are strong drivers.
3. But when we combine them into our 2,068-dimensional hybrid feature vector, R² reaches its peak at 0.9029, and MAE drops to 0.4628.

This ablation study conclusively validates our hypothesis: Localized topological features and macroscopic thermodynamic descriptors work synergistically to deliver state-of-the-art predictive accuracy."

[EXPECTED QUESTION FROM SIR]: 'Does adding 2,048 features risk overfitting since Delaney has only 1,128 samples?'
[YOUR ANSWER]: 'Sir, that is an excellent question. High-dimensional sparse features do cause severe overfitting in unregularized models like linear regression or deep neural nets. However, our production model is Extra Trees, which uses randomized threshold cut-points and ensemble averaging, acting as a powerful regularizer that thrives on sparse binary features without overfitting.'""")

    # -------------------------------------------------------------------------
    # SLIDE 6: Exploratory Data Analysis & Target Distributions
    # -------------------------------------------------------------------------
    slide6 = prs.slides.add_slide(blank_layout)
    add_header(slide6, "Dataset Analysis & Statistical Validation", "Dataset Exploration: The Delaney ESOL Benchmark", "Rigorous statistical analysis of target aqueous solubility and physicochemical distributions")
    add_footer(slide6, 6)

    # Left text box
    add_card(slide6, Inches(0.8), Inches(1.4), Inches(5.4), Inches(5.4), "Delaney ESOL Dataset Characteristics", CARD_BG, BORDER_COLOR)
    add_bullet_list(slide6, Inches(1.0), Inches(2.0), Inches(5.0), Inches(4.6), [
        ("Benchmark Origin: ", "Delaney Aqueous Solubility dataset (ESOL - Estimated SOLubility), universally recognized in literature."),
        ("Sample Size: ", "N = 1,128 diverse organic drug-like compounds and agrochemicals."),
        ("Target Variable (LogS): ", "Log10 of aqueous molar solubility (mol/L). Measured at 25°C room temperature."),
        ("Statistical Distribution: ", "Mean: -3.05 mol/L | Std Dev: 2.10 mol/L | Dynamic Range: -11.60 to +1.58 mol/L."),
        ("Normal Unimodal Curve: ", "The target follows a continuous, unimodal Gaussian-like distribution without zero-inflation or severe artificial clipping."),
        ("Correlation Findings: ", "LogP shows strongest negative correlation with solubility (r = -0.78), followed by Molecular Weight (r = -0.62)."),
        ("Data Splitting Strategy: ", "80% Training Set (N = 902) and 20% Held-Out Test Set (N = 226) with random state seed=42 for strict reproducibility.")
    ], 10.5)

    # Right side: Correlation heatmap
    img_corr = os.path.join(results_dir, "correlation_heatmap.png")
    if os.path.exists(img_corr):
        slide6.shapes.add_picture(img_corr, Inches(6.5), Inches(1.4), Inches(6.0), Inches(5.4))

    add_notes(slide6, """[HOW TO EXPLAIN SLIDE 6 TO SIR]:
"Sir, before building machine learning models, we conducted rigorous Exploratory Data Analysis on the Delaney ESOL benchmark dataset:

1. The dataset contains 1,128 carefully curated drug-like compounds spanning over 13 orders of magnitude in water solubility—from freely soluble compounds (+1.58 log units) to virtually insoluble compounds (-11.60 log units).
2. The target variable LogS is continuous and unimodal, perfectly suited for regression without artificial transformations.
3. Looking at the correlation heatmap on the right:
   - There is a strong negative correlation of -0.78 between Wildman-Crippen LogP and Solubility. This aligns with chemical physics: more lipophilic compounds repel polar water molecules.
   - Molecular Weight has a -0.62 correlation with solubility: larger molecules require more energy to break crystal lattice bonds and create a cavity in water.
   - Polar Surface Area (TPSA) and Oxygen count positively correlate with solubility because they provide hydrogen bonding sites for water.
4. We used an 80/20 train/test split with seed 42 to ensure completely unbiased out-of-sample evaluation."

[EXPECTED QUESTION FROM SIR]: 'Why is the correlation matrix showing multicollinearity between features?'
[YOUR ANSWER]: 'Sir, features like Molecular Weight, Heavy Atom Count, and Ring Count naturally correlate because larger molecules naturally have more atoms and rings. This multicollinearity is fatal for Ordinary Least Squares linear regression, but tree-based algorithms handle collinear features effortlessly.'""")

    # -------------------------------------------------------------------------
    # SLIDE 7: The Master 10-Algorithm Benchmark
    # -------------------------------------------------------------------------
    slide7 = prs.slides.add_slide(blank_layout)
    add_header(slide7, "Model Architecture Exploration & Benchmarking", "The Comprehensive 10-Algorithm Machine Learning Benchmark", "Evaluating 10 architectures across 6 ML families on the 2,068-dimensional hybrid feature matrix")
    add_footer(slide7, 7)

    # Left side: Expanded model comparison chart
    img_comp = os.path.join(results_dir, "expanded_model_comparison.png")
    if os.path.exists(img_comp):
        slide7.shapes.add_picture(img_comp, Inches(0.8), Inches(1.4), Inches(6.0), Inches(5.4))

    # Right side: Table and findings
    add_card(slide7, Inches(7.0), Inches(1.4), Inches(5.5), Inches(5.4), "10-Architecture Benchmark Results (Held-Out Test N=226)", CARD_BG, BORDER_COLOR)
    add_bullet_list(slide7, Inches(7.2), Inches(2.0), Inches(5.1), Inches(4.6), [
        ("1. Stacking Regressor: ", "MAE = 0.4490 | RMSE = 0.6558 | R² = 0.9090 (Meta-learner: ET + HGB + RF -> Ridge). Leader."),
        ("2. Extra Trees Regressor: ", "MAE = 0.4628 | RMSE = 0.6775 | R² = 0.9029 (Production Engine: Ultra-fast inference)."),
        ("3. Voting Ensemble: ", "MAE = 0.4619 | RMSE = 0.6791 | R² = 0.9024 (Weighted ensemble of top 3 tree models)."),
        ("4. HistGradientBoosting: ", "MAE = 0.4688 | RMSE = 0.6776 | R² = 0.9029 (Binned gradient boosting)."),
        ("5. Random Forest: ", "MAE = 0.5313 | RMSE = 0.7708 | R² = 0.8743 (Standard bagging baseline)."),
        ("6. Support Vector Regressor: ", "MAE = 0.8640 | RMSE = 1.1910 | R² = 0.6999 (RBF kernel struggles in 2068D)."),
        ("7. Ridge Regression: ", "MAE = 0.9281 | RMSE = 1.2425 | R² = 0.6734 (Linear underfitting)."),
        ("8. Multi-Layer Perceptron: ", "MAE = 1.0000 | RMSE = 1.3439 | R² = 0.6179 (Neural net overfits on N=902)."),
        ("9. K-Nearest Neighbors: ", "MAE = 1.2881 | RMSE = 1.6543 | R² = 0.4210 (Curse of dimensionality collapse)."),
        ("10. Linear Regression (OLS): ", "MAE = 1.6402 | RMSE = 2.2545 | R² = -0.0753 (Singular matrix inversion failure).")
    ], 9.5)

    add_notes(slide7, """[HOW TO EXPLAIN SLIDE 7 TO SIR]:
"Sir, this is one of the most important research slides in our presentation. Instead of arbitrarily picking a model, we conducted a rigorous 10-architecture benchmark across 6 diverse machine learning families:

1. Tree Ensembles decisively outperformed all other paradigms:
   - Stacking Regressor achieved the highest overall score with R² = 0.9090 and MAE = 0.4490.
   - Extra Trees achieved R² = 0.9029 and MAE = 0.4628. Because Extra Trees delivers identical accuracy with 5x faster inference speed and smaller serialized footprint, we selected it as our core production engine.
   - HistGradientBoosting also achieved R² = 0.9029.
2. In contrast, look at the bottom of the table:
   - Deep Learning (MLP Neural Net) achieved R² of only 0.6179 because deep networks require tens of thousands of samples, and overfitted on N=902 samples.
   - KNN collapsed to R² = 0.4210 due to the curse of dimensionality.
   - And Ordinary Least Squares Linear Regression completely collapsed to a negative R² of -0.0753!

This benchmark conclusively proves that randomized tree ensembles are the superior computational paradigm for sparse high-dimensional cheminformatics."

[EXPECTED QUESTION FROM SIR]: 'Why can R² be negative in Linear Regression?'
[YOUR ANSWER]: 'Sir, R² can be negative whenever a model performs worse than simply predicting the mean of the training data. Because OLS had 2,068 features and only 902 training samples, the matrix X^T X was non-invertible and suffered from catastrophic multicollinearity, resulting in wildly erratic predictions.'""")

    # -------------------------------------------------------------------------
    # SLIDE 8: Algorithmic Deep Dive: Why Extra Trees Won
    # -------------------------------------------------------------------------
    slide8 = prs.slides.add_slide(blank_layout)
    add_header(slide8, "Algorithmic Mechanics & Theoretical Foundations", "Algorithmic Deep Dive: Extra Trees vs Random Forest vs OLS", "Mathematical justification of randomized decision splits and variance reduction")
    add_footer(slide8, 8)

    w3 = Inches(3.64)
    h_card = Inches(5.4)
    y_card = Inches(1.4)

    # Card 1: Extra Trees Mechanics
    add_card(slide8, Inches(0.8), y_card, w3, h_card, "1. Extra Trees (Why It Won)", CARD_BG, EMERALD)
    add_bullet_list(slide8, Inches(1.0), y_card + Inches(0.6), w3 - Inches(0.4), h_card - Inches(0.8), [
        ("Randomized Split Thresholds: ", "Standard trees compute the mathematically optimal cut-point for every candidate feature. Extra Trees draws cut-points randomly from a uniform distribution between min and max."),
        ("Extreme Regularization: ", "This randomized splitting acts as a powerful regularizer, preventing trees from overfitting to sparse binary fingerprint bits."),
        ("No Bootstrapping (bootstrap=False): ", "Trains on the entire original training set, maximizing chemical structural diversity."),
        ("Variance Reduction: ", "Averaging M=150 randomized trees drastically reduces ensemble variance without inflating bias."),
        ("Speed: ", "5x faster training and inference because it avoids evaluating every numerical split point.")
    ], 10.5)

    # Card 2: Random Forest Comparison
    add_card(slide8, Inches(4.84), y_card, w3, h_card, "2. Random Forest Comparison", CARD_BG, ACCENT_BLUE)
    add_bullet_list(slide8, Inches(5.04), y_card + Inches(0.6), w3 - Inches(0.4), h_card - Inches(0.8), [
        ("Bootstrap Aggregating (Bagging): ", "Trains each tree on a random bootstrap sample with replacement (size N). Approximately 36.8% of samples are left out as Out-of-Bag (OOB)."),
        ("Greedy Threshold Optimization: ", "Evaluates all candidate split thresholds to maximize impurity decrease: Delta I = I(parent) - sum(N_k/N * I(k))."),
        ("Performance Gap: ", "Achieved R² = 0.8743 vs Extra Trees' R² = 0.9029."),
        ("Why It Lagged: ", "Evaluating optimal splits on 2,048 sparse binary bits leads to slightly higher variance and susceptibility to bit noise compared to Extra Trees' uniform randomization.")
    ], 10.5)

    # Card 3: The Failure of OLS & KNN
    add_card(slide8, Inches(8.88), y_card, w3, h_card, "3. Why OLS & KNN Collapsed", CARD_BG, ROSE)
    add_bullet_list(slide8, Inches(9.08), y_card + Inches(0.6), w3 - Inches(0.4), h_card - Inches(0.8), [
        ("The p >> n Problem: ", "Feature count (p = 2,068) exceeds training sample count (n = 902)."),
        ("OLS Matrix Singularity: ", "OLS solves beta = (X^T X)^-1 X^T y. When p > n, X^T X is strictly singular and rank-deficient. Determinant approaches zero, causing inverted weights to explode to infinity."),
        ("KNN Curse of Dimensionality: ", "In 2,068D space, the ratio between the distance to the nearest neighbor and farthest neighbor approaches 1: lim_{d->inf} (D_max - D_min)/D_min = 0."),
        ("Loss of Locality: ", "Every chemical compound appears equidistant from every other compound, destroying KNN's premise.")
    ], 10.5)

    add_notes(slide8, """[HOW TO EXPLAIN SLIDE 8 TO SIR]:
"Sir, here we explain the exact mathematical reasons why Extra Trees triumphed and why classical algorithms failed:

1. Random Forest vs. Extra Trees:
   - In standard Random Forest, for each candidate feature, the algorithm searches for the mathematically optimal threshold cut-point that minimizes MSE.
   - In Extra Trees (Extremely Randomized Trees), the algorithm draws cut-points completely at RANDOM from a uniform distribution between that feature's minimum and maximum value! It then picks the best of those random cuts.
   - This seems counter-intuitive at first, but in a 2,048-dimensional sparse space, this randomization acts as an extraordinary regularizer. It suppresses variance, prevents the trees from overfitting to rare fingerprint bits, and speeds up computation by eliminating costly threshold optimization.
2. Why OLS Linear Regression Collapsed:
   - In our dataset, the number of features p = 2,068 is greater than the number of training samples n = 902.
   - Therefore, the covariance matrix X-transpose X is rank-deficient and mathematically non-invertible. The weights blow up to infinity.
3. Why KNN Collapsed:
   - In a 2,068-dimensional space, the 'curse of dimensionality' causes all Euclidean pairwise distances to converge to a uniform constant. No true 'nearest neighbor' exists."

[EXPECTED QUESTION FROM SIR]: 'Why did you use bootstrap=False in Extra Trees?'
[YOUR ANSWER]: 'Sir, by default, Extra Trees does not use bootstrap sampling; it trains each tree on the full training set. Because the cut-points are already randomized, bootstrap sampling is unnecessary and using the full dataset preserves maximum chemical diversity in each tree.'""")

    # -------------------------------------------------------------------------
    # SLIDE 9: Production Model Performance & Parity Analysis
    # -------------------------------------------------------------------------
    slide9 = prs.slides.add_slide(blank_layout)
    add_header(slide9, "Model Evaluation & Verification", "Production Solubility Model: Parity & Metric Analysis", "Extra Trees achieves R² = 0.9029 and MAE = 0.4628 log units on held-out test compounds")
    add_footer(slide9, 9)

    # Left side: Parity plot image
    img_parity = os.path.join(results_dir, "final_combined_actual_vs_predicted.png")
    if os.path.exists(img_parity):
        slide9.shapes.add_picture(img_parity, Inches(0.8), Inches(1.4), Inches(6.0), Inches(5.4))

    # Right side: Metrics & Scientific Interpretation
    add_card(slide9, Inches(7.0), Inches(1.4), Inches(5.5), Inches(5.4), "Production Validation Metrics", CARD_BG, BORDER_COLOR)
    add_bullet_list(slide9, Inches(7.2), Inches(2.0), Inches(5.1), Inches(4.6), [
        ("Test R² = 0.9029: ", "The model explains 90.3% of the total variance in experimental aqueous solubility across unseen chemical compounds."),
        ("Test MAE = 0.4628 log units: ", "On average, model predictions deviate from wet-lab experimental measurements by less than 0.47 log units."),
        ("Test RMSE = 0.6775 log units: ", "Low root mean squared error proves absence of extreme catastrophic prediction errors."),
        ("Cross-Validation R² = 0.9056: ", "5-fold cross-validation confirms that the model generalizes robustly without test-set data leakage."),
        ("Matches Wet-Lab Assay Uncertainty: ", "Published inter-laboratory studies show that experimental wet-lab shake-flask solubility measurements differ by ±0.50 log units across different laboratories. Our model achieves experimental-grade precision."),
        ("Tight Diagonal Clustering: ", "Notice on the left parity plot: The data points cluster tightly along the 45-degree dashed identity line (y = x) across all solubility tiers.")
    ], 11)

    add_notes(slide9, """[HOW TO EXPLAIN SLIDE 9 TO SIR]:
"Sir, this slide presents the validation results of our final production Solubility Extra Trees model:

1. On the left, you can see the Actual vs. Predicted Parity Plot on the 226 held-out test compounds.
   - The X-axis is the true wet-lab experimental LogS.
   - The Y-axis is our model's predicted LogS.
   - The dashed red diagonal line represents perfect prediction (y = x).
2. Notice how tightly the points cluster along the diagonal across the entire range—from highly insoluble compounds (-10 log units) all the way to freely soluble compounds (+1 log units).
3. Statistically:
   - R² is 0.9029 (explains over 90% of variance).
   - Mean Absolute Error is only 0.4628 log units.
4. And here is the most profound scientific takeaway: In real wet-lab chemistry, two different laboratories measuring the exact same compound will often disagree by ±0.50 log units due to temperature, solvent purity, and pipette error! Our model's error of ±0.46 log units is literally within the experimental noise threshold of physical wet-lab assays!"

[EXPECTED QUESTION FROM SIR]: 'Did you tune hyperparameters for this model?'
[YOUR ANSWER]: 'Yes, Sir! We performed grid search optimization. The optimal hyperparameters are: 150 estimators, max_depth of 16, max_features of 0.85, and bootstrap=False.'""")

    # -------------------------------------------------------------------------
    # SLIDE 10: Error Analysis & Residual Homoscedasticity
    # -------------------------------------------------------------------------
    slide10 = prs.slides.add_slide(blank_layout)
    add_header(slide10, "Statistical Diagnostics & Robustness", "Error Analysis: Residual Homoscedasticity & Stability", "Proving zero-bias distribution and constant error variance across all solubility ranges")
    add_footer(slide10, 10)

    # Left side: Residuals image
    img_res = os.path.join(results_dir, "final_combined_residuals.png")
    if os.path.exists(img_res):
        slide10.shapes.add_picture(img_res, Inches(0.8), Inches(1.4), Inches(6.0), Inches(5.4))

    # Right side: Diagnostic takeaways
    add_card(slide10, Inches(7.0), Inches(1.4), Inches(5.5), Inches(5.4), "Diagnostic Statistical Findings", CARD_BG, BORDER_COLOR)
    add_bullet_list(slide10, Inches(7.2), Inches(2.0), Inches(5.1), Inches(4.6), [
        ("Residual Definition: ", "Error e_i = y_actual - y_predicted. Positive residual = under-prediction; Negative = over-prediction."),
        ("Zero-Mean Symmetry: ", "The top histogram shows residuals form a symmetric, bell-shaped Gaussian distribution centered tightly at mean = 0.00 log units."),
        ("Proof of Zero Bias: ", "The model exhibits zero systematic bias—it does not consistently over-predict or under-predict solubility."),
        ("Proof of Homoscedasticity: ", "The bottom scatter plot shows residuals vs predicted values. The errors are uniformly dispersed within a horizontal band (±1.0 log unit) without forming an expanding funnel or cone shape."),
        ("Constant Variance Across Tiers: ", "This confirms homoscedasticity: The model predicts highly soluble, moderately soluble, and insoluble compounds with equal precision and stability."),
        ("Outlier Analysis: ", "Only 3 out of 226 test compounds exhibit residuals > 1.8 log units, corresponding to rare polycyclic fused rings with unusual crystal lattice packing.")
    ], 10.5)

    add_notes(slide10, """[HOW TO EXPLAIN SLIDE 10 TO SIR]:
"Sir, in rigorous machine learning research, checking R² alone is never enough; one must perform residual diagnostic analysis to guarantee model reliability:

1. Look at the top graph on the left: This is the distribution of our prediction residuals (Actual minus Predicted). It forms a symmetric bell curve centered at exactly zero. This proves our model has zero systematic bias.
2. Now, look at the bottom graph: Residuals plotted against Predicted Values.
   - In poor regression models, you often see 'heteroscedasticity', where errors expand like an opening funnel at extreme values.
   - Here, the errors are uniformly distributed across the entire horizontal band from -10 to +1. This proves HOMOSCEDASTICITY—meaning our model is just as reliable when predicting insoluble drugs as it is when predicting soluble drugs.
3. Out of 226 test molecules, over 95% fall within ±1.0 log unit. The few minor outliers correspond to rare polycyclic ring structures where crystal packing forces differ from standard molecular topologies."

[EXPECTED QUESTION FROM SIR]: 'What does homoscedasticity mean in simple words?'
[YOUR ANSWER]: 'Sir, homoscedasticity means constant error variance. It means the model's margin of error does not change whether the target property is large, small, or medium.'""")

    # -------------------------------------------------------------------------
    # SLIDE 11: Feature Importance & Pharmacological Interpretability
    # -------------------------------------------------------------------------
    slide11 = prs.slides.add_slide(blank_layout)
    add_header(slide11, "Global Model Interpretability", "Feature Importance: Decoding the Physical Drivers", "Mean Decrease in Impurity (MDI) validates medicinal chemistry intuition")
    add_footer(slide11, 11)

    # Left side: Feature importance image
    img_fi = os.path.join(results_dir, "final_combined_feature_importance.png")
    if os.path.exists(img_fi):
        slide11.shapes.add_picture(img_fi, Inches(0.8), Inches(1.4), Inches(6.0), Inches(5.4))

    # Right side: Pharmacological Analysis
    add_card(slide11, Inches(7.0), Inches(1.4), Inches(5.5), Inches(5.4), "Top Feature Importance & Chemistry Rationale", CARD_BG, BORDER_COLOR)
    add_bullet_list(slide11, Inches(7.2), Inches(2.0), Inches(5.1), Inches(4.6), [
        ("1. Wildman-Crippen LogP (28.4%): ", "The dominant driver of aqueous solubility. Molecules with high octanol partitioning lack water hydration capacity."),
        ("2. Molecular Weight (14.2%): ", "Second most influential feature. Heavier molecules possess larger contact surfaces and higher crystal packing lattice energies."),
        ("3. TPSA - Polar Surface Area (9.8%): ", "Quantifies the area of polar atoms (oxygen, nitrogen). Direct mediator of dipole-dipole interactions and hydrogen bonding with water."),
        ("4. Heavy Atom & Heteroatom Counts: ", "Reflects elemental composition balance and aromatic versus aliphatic atom ratios."),
        ("5. Morgan Circular Fingerprint Bits: ", "Specific bits corresponding to phenolic hydroxyls, carboxylic acids, and basic piperazines account for the remaining variance."),
        ("Pharmacological Validation: ", "The feature importance ranking perfectly mirrors physical chemistry theory—lipophilicity, size, and polarity are the three pillars of aqueous solvation.")
    ], 10.5)

    add_notes(slide11, """[HOW TO EXPLAIN SLIDE 11 TO SIR]:
"Sir, one of the biggest criticisms of AI in biology is the 'black-box problem'. To ensure our model is trustworthy, we extracted the Mean Decrease in Impurity (MDI) feature importance across all 150 randomized decision trees:

1. Look at the horizontal bar chart on the left:
   - Wildman-Crippen LogP accounts for 28.4% of total split importance.
   - Molecular Weight accounts for 14.2%.
   - Topological Polar Surface Area (TPSA) accounts for 9.8%.
   - Together with specific Morgan fingerprint bits, these top features drive aqueous solubility.
2. This is a crucial finding because it proves our model has genuinely learned the true physical chemistry of solvation:
   - Solubility is governed by cavity formation energy (which scales with Molecular Weight), hydrophobic desolvation (governed by LogP), and polar hydration enthalpy (governed by TPSA and H-bond donors).
   - Our AI has independently arrived at the same physical principles discovered by classical medicinal chemistry!"

[EXPECTED QUESTION FROM SIR]: 'How is feature importance calculated in Extra Trees?'
[YOUR ANSWER]: 'Sir, it is calculated as Mean Decrease in Impurity (MDI). Every time a feature is used to split a node, the reduction in Mean Squared Error (MSE) is weighted by the number of samples reaching that node and summed across all 150 trees in the ensemble.'""")

    # -------------------------------------------------------------------------
    # SLIDE 12: Multi-Endpoint ADMET Suite
    # -------------------------------------------------------------------------
    slide12 = prs.slides.add_slide(blank_layout)
    add_header(slide12, "Multi-Task Pharmaceutical Suite", "Beyond Solubility: The Multi-Endpoint ADMET Suite", "Scaling to 5 production machine learning models for comprehensive clinical profiling")
    add_footer(slide12, 12)

    # Left side: Multi-endpoint ROC curves image
    img_roc = os.path.join(results_dir, "multi_endpoint_roc_curves.png")
    if os.path.exists(img_roc):
        slide12.shapes.add_picture(img_roc, Inches(0.8), Inches(1.4), Inches(6.0), Inches(5.4))

    # Right side: Model Suite Details
    add_card(slide12, Inches(7.0), Inches(1.4), Inches(5.5), Inches(5.4), "5 Production Machine Learning Models", CARD_BG, BORDER_COLOR)
    add_bullet_list(slide12, Inches(7.2), Inches(2.0), Inches(5.1), Inches(4.6), [
        ("1. Aqueous Solubility (LogS): ", "Extra Trees Regressor | Delaney ESOL (N=1,128) | Test R² = 0.9029, MAE = 0.4628."),
        ("2. Lipophilicity (LogD 7.4): ", "Extra Trees Regressor | ChEMBL (N=4,200) | Test R² = 0.6015, MAE = 0.5021. Measures distribution coefficient at blood pH 7.4."),
        ("3. Blood-Brain Barrier (BBBP): ", "Extra Trees Classifier | MoleculeNet (N=2,050) | ROC-AUC = 0.9042, Accuracy = 88.5%, F1 = 0.9120."),
        ("4. Clinical Toxicity Failure (ClinTox): ", "Extra Trees Classifier | FDA/MoleculeNet (N=1,484) | ROC-AUC = 0.9249, Accuracy = 89.9%. Differentiates approved drugs from trial toxic failures."),
        ("5. Tox21 p53 Genotoxicity: ", "Extra Trees Classifier | NIH Tox21 Challenge (N=6,774) | ROC-AUC = 0.8767, Accuracy = 92.1%. Detects DNA damage cellular stress response."),
        ("Unified Feature Pipeline: ", "All 5 models share the identical 2,068D hybrid feature extraction pipeline, enabling instant concurrent multi-endpoint profiling.")
    ], 10)

    add_notes(slide12, """[HOW TO EXPLAIN SLIDE 12 TO SIR]:
"Sir, while aqueous solubility is essential, drug discovery requires optimizing multiple endpoints simultaneously. An ideal drug must be soluble, lipophilic enough to cross membranes, able to reach its target organ, and non-toxic.

Therefore, we expanded our platform to 5 production machine learning models:
1. Aqueous Solubility (Delaney ESOL) — R² = 0.9029.
2. Lipophilicity (LogD at physiological pH 7.4, ChEMBL dataset with 4,200 compounds) — R² = 0.6015.
3. Blood-Brain Barrier Permeability (BBBP, MoleculeNet with 2,050 compounds) — ROC-AUC = 0.9042.
4. Clinical Trial Toxicity Failure (ClinTox, 1,484 compounds comparing FDA approved drugs vs drugs that failed clinical trials due to human toxicity) — ROC-AUC = 0.9249!
5. Tox21 p53 Genotoxicity (NIH Tox21 with 6,774 compounds) — ROC-AUC = 0.8767.

Look at the ROC curves on the left: All classification curves arc sharply toward the top-left corner, demonstrating outstanding diagnostic sensitivity and specificity."

[EXPECTED QUESTION FROM SIR]: 'Why is ClinTox ROC-AUC 0.9249 so significant?'
[YOUR ANSWER]: 'Sir, predicting clinical trial toxicity failure before human trials begin is considered the holy grail of preclinical drug discovery. Our model achieves over 92% ROC-AUC, providing pharmaceutical teams with an automated early-warning system against toxic molecules.'""")

    # -------------------------------------------------------------------------
    # SLIDE 13: Local Explainable AI (XAI) Contour Maps
    # -------------------------------------------------------------------------
    slide13 = prs.slides.add_slide(blank_layout)
    add_header(slide13, "Mechanistic Explainable AI (XAI)", "Local Explainability: 2D Atom-Level Attribution Maps", "Deconstructing molecular predictions into atomic contribution contour heatmaps")
    add_footer(slide13, 13)

    # Left side: XAI showcase image
    img_xai = os.path.join(results_dir, "xai_atom_attribution_showcase.png")
    if os.path.exists(img_xai):
        slide13.shapes.add_picture(img_xai, Inches(0.8), Inches(1.4), Inches(6.0), Inches(5.4))

    # Right side: Mathematical and physical explanation
    add_card(slide13, Inches(7.0), Inches(1.4), Inches(5.5), Inches(5.4), "Mathematical Formulation & Chemical Meaning", CARD_BG, BORDER_COLOR)
    add_bullet_list(slide13, Inches(7.2), Inches(2.0), Inches(5.1), Inches(4.6), [
        ("The Need for Local XAI: ", "Medicinal chemists cannot modify a 'feature bit'; they need to know which specific physical atoms in the structure are causing low solubility."),
        ("Atomic Weight Formulation: ", "For every heavy atom i, we compute an attribution weight:\n  w_i = -1.2 * Contrib_Crippen(i) + 0.8 * |Charge_Gasteiger(i)|"),
        ("Wildman-Crippen Atomic LogP: ", "Decomposes whole-molecule lipophilicity into individual atomic fragment contributions."),
        ("Gasteiger Partial Charges: ", "Calculates electronegativity-driven electrostatic charge redistribution across bonds."),
        ("Green / Cyan Contours: ", "Atoms with high partial charges and negative LogP contribution (e.g. carbonyl oxygens, carboxylates, amines). These atoms promote aqueous hydration."),
        ("Orange / Red Contours: ", "Hydrophobic aromatic ring carbons and non-polar alkyl bulk that resist aqueous solvation."),
        ("Gaussian Smoothing: ", "Projected via RDKit SimilarityMaps using 2D bivariate Gaussian smoothing to generate publication-grade contour heatmaps.")
    ], 10)

    add_notes(slide13, """[HOW TO EXPLAIN SLIDE 13 TO SIR]:
"Sir, this is our Local Explainable AI (XAI) engine. If you tell a medicinal chemist: 'Your molecule has low solubility because bit 1422 was zero', they cannot use that information. But if you show them the 2D chemical structure with color-coded atomic attribution contours, they immediately know which bond to modify!

1. On the left is an XAI contour heatmap generated for Aspirin:
   - Look at the bright green and cyan contours around the carboxylic acid and ester carbonyl oxygens: These polar, electronegative atoms actively interact with water molecules via hydrogen bonding, pulling the molecule into solution.
   - Look at the orange and red contours around the aromatic benzene ring: This hydrophobic carbon ring resists water solvation.
2. Mathematically, we compute each atom's weight using a combination of Wildman-Crippen atomic partition coefficients and Gasteiger partial electrostatic charges:
   w_i = -1.2 * Contrib_Crippen + 0.8 * |Charge_Gasteiger|.
3. We then project these weights as 2D Gaussian density contours using RDKit SimilarityMaps.
4. This transforms our AI from a black-box oracle into an interactive guide that directs chemists where to make chemical substitutions."

[EXPECTED QUESTION FROM SIR]: 'What are Gasteiger partial charges?'
[YOUR ANSWER]: 'Sir, Gasteiger charges are partial electrostatic charges on individual atoms calculated iteratively based on orbital electronegativities. They reflect how electrons shift toward electronegative atoms like oxygen and nitrogen, creating molecular dipoles.'""")

    # -------------------------------------------------------------------------
    # SLIDE 14: Structural Safety & Drug-Likeness Rules
    # -------------------------------------------------------------------------
    slide14 = prs.slides.add_slide(blank_layout)
    add_header(slide14, "Cheminformatics Safety Profiling", "Drug-Likeness Rules & Structural Toxicophore Alerts", "Rigorous filtering for Pan-Assay Interference (PAINS), mutagenic alerts, and oral bioavailability")
    add_footer(slide14, 14)

    # Left side: Bioavailability radar chart image
    img_radar = os.path.join(results_dir, "bioavailability_radar_chart.png")
    if os.path.exists(img_radar):
        slide14.shapes.add_picture(img_radar, Inches(0.8), Inches(1.4), Inches(6.0), Inches(5.4))

    # Right side: Safety & Rules list
    add_card(slide14, Inches(7.0), Inches(1.4), Inches(5.5), Inches(5.4), "Screening Filters & Bioavailability Radar", CARD_BG, BORDER_COLOR)
    add_bullet_list(slide14, Inches(7.2), Inches(2.0), Inches(5.1), Inches(4.6), [
        ("PAINS Filter Screening: ", "Scans against 480 Pan-Assay Interference Compound alerts (Classes A, B, C) to eliminate false positives from optical assay interference and covalent aggregation."),
        ("Brenk Structural Alerts: ", "Identifies 105 chemically reactive or metabolically unstable fragments (e.g. aliphatic halides, nitroso groups, epoxides)."),
        ("Lipinski's Rule of 5 (Ro5): ", "MW <= 500 Da, LogP <= 5.0, HBD <= 5, HBA <= 10. Assesses oral drug-likeness."),
        ("Veber's Rule: ", "Rotatable Bonds <= 10 and TPSA <= 140 Å² for intestinal membrane absorption."),
        ("Pfizer CNS MPO: ", "Multiparameter optimization score (0 to 6) evaluating central nervous system blood-brain barrier permeability."),
        ("Bioavailability Radar: ", "Visualizes the drug candidate's property envelope against the optimal oral bioavailability boundary across 6 axes: LIPO, SIZE, POLAR, INSOLU, INSATU, and FLEX.")
    ], 10)

    add_notes(slide14, """[HOW TO EXPLAIN SLIDE 14 TO SIR]:
"Sir, before any compound is recommended for synthesis, our platform runs a comprehensive safety and drug-likeness screening battery:

1. First, we screen for PAINS (Pan-Assay Interference Compounds):
   - These are nuisance chemical motifs (like rhodanines or quinones) that produce fake positive signals in assay equipment by aggregating or fluorescing. Filtering them early saves millions of dollars in wasted wet-lab assays.
2. Second, we screen for Brenk structural alerts to detect metabolically toxic or mutagenic chemical groups.
3. Third, we compute compliance with Lipinski's Rule of 5, Veber's rule, Ghose, Egan, and Pfizer's CNS MPO score.
4. Fourth, on the left is our SwissADME-style Bioavailability Radar Chart:
   - The green shaded polygon represents the optimal physicochemical space for oral absorption across 6 dimensions: Lipophilicity, Size, Polarity, In-solubility, Saturation (Fsp3), and Flexibility (Rotatable Bonds).
   - If the candidate's blue polygon fits inside the green zone, it has high potential for oral absorption."

[EXPECTED QUESTION FROM SIR]: 'What is the significance of Fsp3 (Fraction CSP3)?'
[YOUR ANSWER]: 'Sir, Fsp3 is the fraction of sp3-hybridized carbons out of total carbons. Higher Fsp3 indicates a three-dimensional, non-flat molecule with chiral complexity. Clinical studies have shown that molecules with higher Fsp3 have significantly higher clinical transition rates from Phase I to approval.'""")

    # -------------------------------------------------------------------------
    # SLIDE 15: Generative AI Lead Optimizer & Bioisosterism
    # -------------------------------------------------------------------------
    slide15 = prs.slides.add_slide(blank_layout)
    add_header(slide15, "Generative AI & Rational Drug Design", "Generative AI Lead Optimizer & Bioisosteric SAR Engine", "Automated Structure-Activity Relationship (SAR) transformations with real-time delta shifts")
    add_footer(slide15, 15)

    # Left side: Lead optimization delta chart
    img_opt = os.path.join(results_dir, "lead_optimization_delta_chart.png")
    if os.path.exists(img_opt):
        slide15.shapes.add_picture(img_opt, Inches(0.8), Inches(1.4), Inches(6.0), Inches(5.4))

    # Right side: The 8 SMARTS Transforms
    add_card(slide15, Inches(7.0), Inches(1.4), Inches(5.5), Inches(5.4), "8 Verified Bioisosteric SMARTS Transforms", CARD_BG, BORDER_COLOR)
    add_bullet_list(slide15, Inches(7.2), Inches(2.0), Inches(5.1), Inches(4.6), [
        ("1. Carboxylic Acid -> 1H-Tetrazole: ", "Maintains acidic planar pharmacophore (pKa ~4.8) while increasing lipophilic permeability and preventing rapid glucuronidation."),
        ("2. Carboxylic Acid -> Primary Amide: ", "Eliminates negative charge at blood pH, enhancing passive intestinal permeability."),
        ("3. Polar Hydroxyl (-OH) Grafting: ", "Introduces polar hydrogen bonding, reducing LogP and boosting solubility."),
        ("4. Metabolic C-F Fluorine Scan: ", "Blocks Cytochrome P450 metabolic oxidation spots without significant steric disruption."),
        ("5. Morpholine Solubilizing Tail: ", "Weakly basic oxygen-heterocycle that dramatically boosts water solubility."),
        ("6. N-Methylpiperazine Tail: ", "Enables ionizable tertiary amine salt formation, increasing LogS by orders of magnitude."),
        ("7. Cyclopropyl Rigidification: ", "Reduces rotatable bonds, lowering binding entropic penalty and satisfying Veber's rule."),
        ("8. Ester -> 1,2,4-Oxadiazole: ", "Protects hydrolytically labile esters against plasma esterase degradation.")
    ], 9.5)

    add_notes(slide15, """[HOW TO EXPLAIN SLIDE 15 TO SIR]:
"Sir, detecting that a drug has low solubility or toxicity is helpful, but what a pharmaceutical chemist really needs is: 'How do I FIX it?'

This is where our Generative AI Lead Optimizer comes in:
1. In medicinal chemistry, scientists use 'Bioisosterism'—replacing problematic chemical groups with biologically equivalent groups that improve solubility and pharmacokinetics without destroying receptor binding.
2. We programmed 8 verified SMARTS chemical reaction transforms into our platform:
   - For example, replacing a Carboxylic Acid with a 1H-Tetrazole ring preserves the acidic pharmacophore but increases cell membrane permeability and stops rapid metabolic excretion.
   - Adding a morpholine or piperazine tail enables salt formation, increasing water solubility by orders of magnitude!
   - Conducting a Fluorine scan blocks metabolic soft spots by Cytochrome P450 enzymes.
3. Look at the chart on the left: When a user clicks optimize, the AI generates structural analogs in real time, re-runs the entire ADMET pipeline, and plots the exact Delta shifts in LogS, LogD, and drug-likeness (QED).
4. This automates days of manual Structure-Activity Relationship (SAR) brainstorming into a 1-second automated computation."

[EXPECTED QUESTION FROM SIR]: 'What is SMARTS in cheminformatics?'
[YOUR ANSWER]: 'Sir, SMARTS is the SMILES Arbitrary Target Specification language. It allows us to specify chemical reaction transformation patterns, such as finding any carboxylic acid carbon-oxygen-OH group and replacing it with a tetrazole ring.'""")

    # -------------------------------------------------------------------------
    # SLIDE 16: Interactive Research Dashboard (14 Dedicated Pages)
    # -------------------------------------------------------------------------
    slide16 = prs.slides.add_slide(blank_layout)
    add_header(slide16, "Interactive Software Architecture", "Production Research Dashboard: 14 Dedicated Modules", "A publication-grade GUI built with Streamlit, JSME ChemDraw, 3Dmol.js, and automated dossier builder")
    add_footer(slide16, 16)

    # 3 Cards
    w3 = Inches(3.64)
    h_card = Inches(5.4)
    y_card = Inches(1.4)

    # Card 1: Core Analytical Pages
    add_card(slide16, Inches(0.8), y_card, w3, h_card, "Analytical & Benchmarking Pages", CARD_BG, ACCENT_BLUE)
    add_bullet_list(slide16, Inches(1.0), y_card + Inches(0.6), w3 - Inches(0.4), h_card - Inches(0.8), [
        ("Overview & KPIs: ", "Hero metrics cards, end-to-end architecture diagram, clinical motivation."),
        ("Dataset Analysis: ", "Delaney target distribution, LogS statistics, descriptor correlation heatmaps."),
        ("Feature Engineering: ", "Descriptor calculations and ablation study proof."),
        ("Model Benchmarking: ", "10-architecture comparison across MAE, RMSE, and R²."),
        ("Final Model: ", "Production Extra Trees metrics, parity plots, and 5-fold CV."),
        ("Error Analysis: ", "Residual homoscedasticity, error distribution, outlier dissection."),
        ("Explainability (XAI): ", "Top-20 MDI feature importance & SimilarityMap contour heatmaps.")
    ], 10)

    # Card 2: Interactive Discovery Tools
    add_card(slide16, Inches(4.84), y_card, w3, h_card, "Interactive Drug Discovery Tools", CARD_BG, EMERALD)
    add_bullet_list(slide16, Inches(5.04), y_card + Inches(0.6), w3 - Inches(0.4), h_card - Inches(0.8), [
        ("Live Prediction & ADMET: ", "Inference on 45 curated FDA drugs across 9 therapeutic classes with bioavailability radar."),
        ("3D Conformer Viewer: ", "Hardware-accelerated 3Dmol.js viewer with MMFF94 force-field geometry optimization and mouse rotation."),
        ("2D ChemDraw Canvas (JSME): ", "Interactive in-browser chemical sketcher allowing users to draw molecules from scratch with mouse clicks."),
        ("AI Lead Optimizer: ", "Generative bioisosteric SAR engine displaying side-by-side analogs with delta shifts."),
        ("Virtual Screening (vHTS): ", "Batch library screening for up to 100 compounds with interactive scatter plots and CSV export.")
    ], 10)

    # Card 3: Enterprise Features
    add_card(slide16, Inches(8.88), y_card, w3, h_card, "Deployment & Documentation", CARD_BG, NAVY)
    add_bullet_list(slide16, Inches(9.08), y_card + Inches(0.6), w3 - Inches(0.4), h_card - Inches(0.8), [
        ("Preclinical Dossier Generator: ", "1-click generation of regulatory-ready HTML and Word (.docx) preclinical dossiers."),
        ("FastAPI Microservice: ", "Independent REST microservice with automated interactive Swagger documentation at /docs."),
        ("Docker Containerization: ", "Multi-stage Dockerfile and docker-compose orchestration."),
        ("Cloud Ready: ", "Pre-configured for 1-click deployment to Streamlit Cloud and Hugging Face Spaces."),
        ("Clean Decoupled Codebase: ", "Decoupled architecture separating raw data, feature pipelines, serialized models, and UI.")
    ], 10)

    add_notes(slide16, """[HOW TO EXPLAIN SLIDE 16 TO SIR]:
"Sir, to make our research immediately usable by pharmaceutical researchers, we developed an enterprise-grade Streamlit research dashboard organized into 14 dedicated pages:

1. Scientific Pages:
   - Complete exploratory data analysis, feature ablation studies, 10-model benchmarking, parity plots, residual homoscedasticity analysis, and XAI feature importance.
2. Interactive Drug Discovery Tools:
   - Live ADMET Profiler: Evaluates 45 FDA drugs across 9 therapeutic classes with radar charts.
   - 2D ChemDraw Canvas: Users can draw any novel chemical structure with their mouse using our embedded JSME sketcher, and click 'Predict' to run the full pipeline.
   - 3D Conformer Viewer: Built with 3Dmol.js and MMFF94 force field optimization, allowing full 3D rotation of molecular conformers.
   - Virtual High-Throughput Screening (vHTS): Screens entire batches of compounds simultaneously with CSV export.
3. Enterprise Export:
   - Generates a complete standalone Preclinical Regulatory Dossier with a single click."

[EXPECTED QUESTION FROM SIR]: 'How does the 3D viewer work if SMILES is only a 1D string?'
[YOUR ANSWER]: 'Sir, RDKit takes the 1D SMILES, adds explicit hydrogens, embeds 3D coordinates using distance geometry (ETKDGv3), and minimizes the conformational energy using the MMFF94 molecular mechanics force field before rendering it in 3Dmol.js.'""")

    # -------------------------------------------------------------------------
    # SLIDE 17: Production REST API & Cloud Architecture
    # -------------------------------------------------------------------------
    slide17 = prs.slides.add_slide(blank_layout)
    add_header(slide17, "Software Engineering & Cloud Microservice", "Production REST API & Cloud Deployment Suite", "FastAPI microservice with OpenAPI Swagger docs and containerized Docker orchestration")
    add_footer(slide17, 17)

    # Left side: API endpoints card
    add_card(slide17, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.4), "FastAPI Microservice Endpoints (api.py)", CARD_BG, ACCENT_BLUE)
    add_bullet_list(slide17, Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.6), [
        ("GET /health: ", "Verifies multi-model availability, GPU/CPU runtime, and system status."),
        ("POST /api/v1/predict/admet: ", "Accepts JSON {'smiles': '...'} and returns full 18-property ADMET profile including LogS, LogD, BBBP, ClinTox, and Tox21."),
        ("POST /api/v1/optimize/lead: ", "Applies bioisosteric transformations and returns ranked structural analogs with delta shifts."),
        ("POST /api/v1/explain/attribution: ", "Computes atomic weights and returns base64-encoded 2D SimilarityMap contour heatmap."),
        ("POST /api/v1/screening/batch: ", "High-throughput batch screening endpoint supporting up to 100 compounds simultaneously."),
        ("Interactive Swagger UI: ", "Fully documented OpenAPI schema accessible at http://localhost:8000/docs."),
        ("Pydantic Validation: ", "Strict schema validation and type safety with automated error handling.")
    ], 10.5)

    # Right side: Cloud & DevOps card
    add_card(slide17, Inches(6.8), Inches(1.4), Inches(5.6), Inches(5.4), "DevOps, Containerization & Cloud Deployment", CARD_BG, EMERALD)
    add_bullet_list(slide17, Inches(7.0), Inches(2.0), Inches(5.2), Inches(4.6), [
        ("Multi-Stage Dockerfile: ", "Lightweight Python 3.12-slim base image with headless X11 graphics libraries (libxrender1, libxext6, libgl1) for RDKit rendering."),
        ("Docker Compose Orchestrator: ", "Single-command deployment running both the Streamlit dashboard (port 8501) and FastAPI microservice (port 8000) simultaneously."),
        ("One-Click Windows Launchers: ", "Supplied run_dashboard.bat and run_api.bat for instant execution on any Windows workstation."),
        ("Streamlit Cloud & HF Spaces: ", "Production-ready for cloud hosting on share.streamlit.io and Hugging Face Spaces directly from GitHub."),
        ("Production Scalability: ", "Asynchronous ASGI server (Uvicorn) capable of handling concurrent virtual screening requests from distributed laboratories.")
    ], 10.5)

    add_notes(slide17, """[HOW TO EXPLAIN SLIDE 17 TO SIR]:
"Sir, a modern AI system should not be confined to a notebook or desktop; it must be an enterprise-grade service that other software systems can consume programmatically.

1. We engineered a dedicated production REST microservice using FastAPI (`api.py`):
   - It exposes clean, versioned endpoints (`/api/v1/predict/admet`, `/api/v1/optimize/lead`, `/api/v1/explain/attribution`, and `/api/v1/screening/batch`).
   - It includes interactive OpenAPI Swagger documentation at `/docs`, allowing any research lab or automated screening robot to send HTTP POST requests and receive JSON predictions in milliseconds.
2. For cloud deployment:
   - We authored a multi-stage Dockerfile and a `docker-compose.yml` orchestrator that starts both the Streamlit frontend and the FastAPI backend with a single command.
   - It includes all headless graphics dependencies required for RDKit molecular rendering.
   - It is 100% cloud-ready for Streamlit Cloud and Hugging Face Spaces."

[EXPECTED QUESTION FROM SIR]: 'Why did you use FastAPI instead of Flask?'
[YOUR ANSWER]: 'Sir, FastAPI is built on asynchronous ASGI standards (Starlette and Pydantic). It is significantly faster than Flask, natively validates JSON request bodies using type annotations, and automatically generates interactive Swagger documentation without external plugins.'""")

    # -------------------------------------------------------------------------
    # SLIDE 18: Master Viva Defense — Top Questions & Answers (Part 1)
    # -------------------------------------------------------------------------
    slide18 = prs.slides.add_slide(blank_layout)
    add_header(slide18, "Master Viva & Oral Defense Cheatsheet", "Oral Defense Q&A: Cheminformatics & Machine Learning", "Anticipated questions from the external examiner / Sir with authoritative answers")
    add_footer(slide18, 18)

    w_half = Inches(5.6)
    # Card 1: Q1 & Q2
    add_card(slide18, Inches(0.8), Inches(1.4), w_half, Inches(5.4), "Q1 & Q2: Features & Dimensionality", CARD_BG, BORDER_COLOR)
    add_bullet_list(slide18, Inches(1.0), Inches(2.0), w_half - Inches(0.4), Inches(4.6), [
        ("Q1: Why combine 20 descriptors with 2,048 fingerprints instead of just using one?", ""),
        ("Authoritative Answer: ", "Descriptors provide global physical thermodynamic context (overall mass, polar surface area, hydrogen bond counts) but fail on structural isomers. Fingerprints capture fine localized functional group connectivity (rings, branch points) but lack global mass context. Combining both (2,068D) synergizes macro and micro features, boosting test R² from 0.6389 (fingerprints only) and 0.8909 (descriptors only) to 0.9029."),
        ("Q2: Why did OLS Linear Regression collapse with R² = -0.0753?", ""),
        ("Authoritative Answer: ", "In our hybrid dataset, the feature count (p = 2,068) exceeds the sample count (n = 902). The matrix X^T X is strictly non-invertible and rank-deficient. Extreme multicollinearity between fingerprint bits caused singular matrix inversion failure. Unregularized linear models cannot operate when p > n.")
    ], 10)

    # Card 2: Q3 & Q4
    add_card(slide18, Inches(6.8), Inches(1.4), w_half, Inches(5.4), "Q3 & Q4: Algorithmic Mechanics", CARD_BG, BORDER_COLOR)
    add_bullet_list(slide18, Inches(7.0), Inches(2.0), w_half - Inches(0.4), Inches(4.6), [
        ("Q3: What is the exact algorithmic distinction between Random Forest and Extra Trees?", ""),
        ("Authoritative Answer: ", "Both are bagging ensembles of decision trees. However, while Random Forest searches for the mathematically optimal threshold split among feature subsets using MSE, Extra Trees draws cut-points completely at RANDOM from a uniform distribution between min and max values. It then chooses the best of these random cuts. Furthermore, Extra Trees uses bootstrap=False. This extreme randomization regularizes against sparse bit noise, lowers variance, and dramatically accelerates training."),
        ("Q4: Why did K-Nearest Neighbors (KNN) fail with R² = 0.4210?", ""),
        ("Authoritative Answer: ", "Catastrophic failure due to the curse of dimensionality. In 2,068-dimensional sparse binary space, pairwise Euclidean distances between all data points converge to a uniform constant: (D_max - D_min)/D_min -> 0. The concept of nearest neighbor loses all discriminatory meaning.")
    ], 10)

    add_notes(slide18, """[HOW TO EXPLAIN SLIDE 18 TO SIR]:
"Sir, to demonstrate our deep mastery over the theoretical concepts, we prepared this Viva Defense cheatsheet addressing the most important questions an examiner or professor might ask:

1. If Sir asks: 'Why did you use 2,068 features?'
   - Answer: Because neither descriptors nor fingerprints alone are sufficient. Our ablation study proved that descriptors alone achieve R² = 0.8909, fingerprints alone achieve R² = 0.6389, but combining them achieves R² = 0.9029.
2. If Sir asks: 'Why did Linear Regression fail with negative R²?'
   - Answer: Because features p = 2,068 exceeds samples n = 902. The matrix X-transpose X is rank-deficient and singular, causing catastrophic multicollinearity failure.
3. If Sir asks: 'What makes Extra Trees different from Random Forest?'
   - Answer: Extra Trees picks split thresholds completely at random from a uniform distribution instead of calculating optimal thresholds. This acts as a regularizer that suppresses overfitting on sparse fingerprint bits and speeds up inference."
""")

    # -------------------------------------------------------------------------
    # SLIDE 19: Master Viva Defense — Top Questions & Answers (Part 2)
    # -------------------------------------------------------------------------
    slide19 = prs.slides.add_slide(blank_layout)
    add_header(slide19, "Master Viva & Oral Defense Cheatsheet", "Oral Defense Q&A: Pharmacology, XAI & Chemistry", "Anticipated questions on clinical relevance, explainability, and medicinal chemistry")
    add_footer(slide19, 19)

    # Card 1: Q5 & Q6
    add_card(slide19, Inches(0.8), Inches(1.4), w_half, Inches(5.4), "Q5 & Q6: Pharmacology & XAI", CARD_BG, BORDER_COLOR)
    add_bullet_list(slide19, Inches(1.0), Inches(2.0), w_half - Inches(0.4), Inches(4.6), [
        ("Q5: What is the clinical difference between LogP and LogD 7.4?", ""),
        ("Authoritative Answer: ", "LogP measures the octanol-water partition coefficient of strictly un-ionized, neutral species. LogD 7.4 measures the distribution coefficient at physiological blood pH (7.4), accounting for the ionization equilibrium of weak acids and bases: LogD = LogP - log10(1 + 10^(pH - pKa)). Because over 85% of commercial drugs are partially ionized at blood pH, LogD 7.4 is far more physiologically and clinically relevant."),
        ("Q6: How does the Local XAI engine compute atom-level attribution?", ""),
        ("Authoritative Answer: ", "We calculate atomic weights w_i = -1.2 * Contrib_Crippen(i) + 0.8 * |Charge_Gasteiger(i)|. Atoms with negative Crippen LogP and high partial charges promote polar water hydration (green contours). Lipophilic aromatic carbons resist solvation (orange/red contours). These weights are projected using 2D Gaussian density smoothing in RDKit SimilarityMaps.")
    ], 10)

    # Card 2: Q7 & Q8
    add_card(slide19, Inches(6.8), Inches(1.4), w_half, Inches(5.4), "Q7 & Q8: Safety & Medicinal Chemistry", CARD_BG, BORDER_COLOR)
    add_bullet_list(slide19, Inches(7.0), Inches(2.0), w_half - Inches(0.4), Inches(4.6), [
        ("Q7: What are PAINS alerts and why are they critical?", ""),
        ("Authoritative Answer: ", "PAINS stands for Pan-Assay Interference Compounds. These are reactive chemical motifs (e.g. rhodanines, quinones) that produce false positives in optical assays by aggregating, fluorescing, or binding covalently with proteins. Filtering them early prevents wasting millions of dollars validating fake hits in wet-labs."),
        ("Q8: Why replace Carboxylic Acids with 1H-Tetrazole in lead optimization?", ""),
        ("Authoritative Answer: ", "Carboxylic acids carry a negative charge at blood pH (pKa ~4), creating a high desolvation penalty that hampers passive cell membrane permeability, and are prone to rapid metabolic clearance via glucuronidation. A 1H-tetrazole ring has identical acidic pKa (~4.8) and planar geometry, but delocalizes the charge across 4 nitrogen atoms, enhancing membrane permeability, bioavailability, and metabolic stability.")
    ], 10)

    add_notes(slide19, """[HOW TO EXPLAIN SLIDE 19 TO SIR]:
"Sir, this second Viva slide covers the pharmacological and cheminformatics questions:

1. If Sir asks: 'What is the difference between LogP and LogD 7.4?'
   - Answer: LogP is measured for the neutral, uncharged molecule. LogD 7.4 is measured at human blood pH (7.4), taking into account whether the molecule ionizes into acids or bases. Over 85% of drugs ionize in blood, making LogD 7.4 much more clinically relevant.
2. If Sir asks: 'How does your XAI contour map work?'
   - Answer: It calculates the contribution of each individual atom by combining its Crippen LogP with its Gasteiger partial charge. Atoms that favor water hydration get green contours; atoms that resist hydration get red contours.
3. If Sir asks: 'What are PAINS?'
   - Answer: Pan-Assay Interference Compounds. False-positive chemicals that trick laboratory optical assays. We filter them out early.
4. If Sir asks: 'Why use bioisosteres like Tetrazole?'
   - Answer: Replacing carboxylic acids with tetrazoles preserves receptor binding while improving metabolic stability and cell membrane absorption."
""")

    # -------------------------------------------------------------------------
    # SLIDE 20: Project Conclusion, Future Scope & Sign-Off
    # -------------------------------------------------------------------------
    slide20 = prs.slides.add_slide(blank_layout)
    add_header(slide20, "Summary, Future Scope & Academic Sign-Off", "Project Summary & Future Research Directions", "Key achievements and the roadmap toward Graph Neural Networks and 3D Molecular Docking")
    add_footer(slide20, 20)

    # Left side: Key Achievements
    add_card(slide20, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.4), "Summary of Research Achievements", CARD_BG, EMERALD)
    add_bullet_list(slide20, Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.6), [
        ("State-of-the-Art Accuracy: ", "Extra Trees regressor achieves R² = 0.9029 and MAE = 0.4628 log units, matching wet-lab experimental assay precision."),
        ("Novel 2,068D Hybrid Representation: ", "Empirically proven via ablation study to outperform fingerprints alone (R²=0.6389) and descriptors alone (R²=0.8909)."),
        ("Multi-Endpoint ADMET Suite: ", "Trained and validated 5 production models including Lipophilicity, BBBP (AUC=0.9042), ClinTox (AUC=0.9249), and Tox21 (AUC=0.8767)."),
        ("Mechanistic Explainability (XAI): ", "Local 2D SimilarityMap contour heatmaps fusing Crippen LogP and Gasteiger partial electrostatic charges."),
        ("Generative AI Lead Optimizer: ", "Automated SAR optimization using 8 bioisosteric reaction transforms with real-time delta shifts."),
        ("Complete Production Platform: ", "14-page Streamlit research dashboard with 2D ChemDraw and 3D conformer viewer, accompanied by a production FastAPI microservice.")
    ], 10.5)

    # Right side: Future Scope & Team
    add_card(slide20, Inches(6.8), Inches(1.4), Inches(5.6), Inches(5.4), "Future Research Scope & Academic Sign-Off", CARD_BG, NAVY)
    add_bullet_list(slide20, Inches(7.0), Inches(2.0), Inches(5.2), Inches(4.6), [
        ("1. Graph Neural Networks (GNNs): ", "Transitioning from fixed circular fingerprints to end-to-end learned molecular representations using Directed Message Passing Neural Networks (D-MPNN / Chemprop)."),
        ("2. In-Silico 3D Molecular Docking: ", "Integrating AutoDock Vina or DiffDock into the FastAPI backend for automated receptor binding affinity prediction (Delta G in kcal/mol)."),
        ("3. Retrosynthetic Route Verification: ", "Incorporating reaction rule-based retrosynthetic engines (AiZynthFinder) to automatically verify whether AI-generated lead analogs can be practically synthesized in wet-labs."),
        ("Researcher: ", "M. Pramod (24BAI1417)\nDepartment of Computer Science & Engineering (AI & ML)"),
        ("Thank You: ", "We thank our respected Project Guide and Faculty Reviewers for their guidance and support. We are now open for questions!")
    ], 10.5)

    add_notes(slide20, """[HOW TO CONCLUDE YOUR PRESENTATION TO SIR]:
"Respected Sir, to summarize our presentation:

1. We set out to build an end-to-end in-silico drug discovery intelligence platform, and we achieved state-of-the-art predictive performance with R² = 0.9029 on solubility and ROC-AUC of 92.5% on clinical toxicity.
2. Our empirical ablation study proved that the 2,068-dimensional hybrid feature representation is essential, reducing error by over 52%.
3. We solved the AI black-box problem by implementing local atom-level attribution heatmaps.
4. We built a generative lead optimizer that uses medicinal chemistry bioisosterism to automatically suggest structural fixes.
5. And finally, we engineered a complete software system: a 14-page Streamlit research dashboard, a 2D ChemDraw canvas, a 3D conformer viewer, a production FastAPI microservice, and a 1-click regulatory dossier generator.

In the future, we plan to extend this work with Graph Neural Networks (D-MPNN) and automated 3D molecular docking.

Thank you very much, Sir. I am now ready to answer any questions you have!"
""")

    # Save presentation
    output_pptx = os.path.abspath("Molecular_Property_Prediction_Presentation.pptx")
    prs.save(output_pptx)
    print(f"Presentation successfully created at: {output_pptx}")
    return output_pptx

if __name__ == "__main__":
    create_presentation()
