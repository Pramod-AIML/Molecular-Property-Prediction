"""
Script to generate the standardized 9-slide Academic Defense Presentation for:
Molecular Property Prediction & In-Silico ADMET Intelligence Platform

Strictly adheres to the required 9-slide evaluation structure:
1. Title Slide: Assignment/project title, your name, and the names of all group members.
2. Introduction: A brief introduction to your problem and proposed work.
3. Problem Statement: Clearly explain the problem identified through your literature survey submitted in the first PPT.
4. Research Gaps: Explain the gaps identified from your literature survey.
5. Research Objectives: Present objectives that directly address the identified research gaps.
6. Architecture Diagram: Include the architecture of your proposed system.
7. Methodology and Implementation: Explain the steps followed for execution, preprocessing techniques, algorithms used, and the number of algorithms implemented.
8. Dataset: Mention the dataset(s) used for implementation and evaluation.
9. Results and Outcomes: Present the key results and outcomes achieved. Include relevant graphs from your experiments in the PPT.
"""

import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def build_presentation():
    prs = Presentation()
    # 16:9 Widescreen standard
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Professional Color Palette
    NAVY = RGBColor(15, 23, 42)          # #0F172A
    DEEP_BLUE = RGBColor(30, 41, 59)     # #1E293B
    ACCENT_BLUE = RGBColor(2, 132, 199)  # #0284C7 (Sky/Cyan Accent)
    CARD_BG = RGBColor(255, 255, 255)    # Clean White
    BORDER_COLOR = RGBColor(226, 232, 240)# Soft Slate Border
    DARK_TEXT = RGBColor(15, 23, 42)     # Deep Charcoal
    MUTED_TEXT = RGBColor(100, 116, 139) # Secondary Slate Text
    WHITE = RGBColor(255, 255, 255)
    EMERALD = RGBColor(5, 150, 105)      # Positive / Objectives
    ROSE = RGBColor(225, 29, 72)         # Problem / Attrition
    AMBER = RGBColor(217, 119, 6)        # Gaps / Warnings
    PURPLE = RGBColor(124, 58, 237)      # Architecture / XAI

    results_dir = os.path.abspath("results")

    # Helper: Consistent Header
    def add_header(slide, tag_text, title_text, subtitle_text=""):
        header_box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.18))
        header_box.fill.solid()
        header_box.fill.fore_color.rgb = NAVY
        header_box.line.color.rgb = ACCENT_BLUE
        header_box.line.width = Pt(1.5)

        tf = header_box.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.8)
        tf.margin_top = Inches(0.12)
        tf.margin_right = Inches(0.8)
        tf.margin_bottom = Inches(0.08)

        p_tag = tf.paragraphs[0]
        p_tag.text = tag_text.upper()
        p_tag.font.name = "Calibri"
        p_tag.font.size = Pt(10)
        p_tag.font.bold = True
        p_tag.font.color.rgb = ACCENT_BLUE

        p_title = tf.add_paragraph()
        p_title.text = title_text
        p_title.font.name = "Calibri"
        p_title.font.size = Pt(20)
        p_title.font.bold = True
        p_title.font.color.rgb = WHITE

        if subtitle_text:
            p_sub = tf.add_paragraph()
            p_sub.text = subtitle_text
            p_sub.font.name = "Calibri"
            p_sub.font.size = Pt(11)
            p_sub.font.color.rgb = RGBColor(148, 163, 184)

    # Helper: Clean Standard Footer
    def add_footer(slide, slide_num):
        footer_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.12), Inches(11.733), Inches(0.32))
        tf = footer_box.text_frame
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = f"B.Tech CSE (AI & ML) | Candidate: M. Pramod (24BAI1417) | Slide {slide_num} of 9"
        p.font.name = "Calibri"
        p.font.size = Pt(9)
        p.font.color.rgb = MUTED_TEXT

    # Helper: Card Shape
    def add_card(slide, left, top, width, height, title="", bg_color=CARD_BG, border_color=BORDER_COLOR, title_color=NAVY):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1.2)

        if title:
            tb = slide.shapes.add_textbox(left + Inches(0.18), top + Inches(0.12), width - Inches(0.36), Inches(0.4))
            tf = tb.text_frame
            tf.word_wrap = True
            tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
            p = tf.paragraphs[0]
            p.text = title
            p.font.name = "Calibri"
            p.font.size = Pt(13)
            p.font.bold = True
            p.font.color.rgb = title_color
        return card

    # Helper: Bullet List
    def add_bullet_list(slide, left, top, width, height, items, font_size=10.5, space_after=5):
        tb = slide.shapes.add_textbox(left, top, width, height)
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        for i, item in enumerate(items):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.space_after = Pt(space_after)
            p.level = 0
            
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

    # Helper: Speaker Notes
    def add_notes(slide, notes_content):
        notes_slide = slide.notes_slide
        tf = notes_slide.notes_text_frame
        tf.text = notes_content

    # =========================================================================
    # SLIDE 1: Title Slide (Assignment/Project Title & Group Members)
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    bg1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = NAVY
    bg1.line.fill.background()

    card1 = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.7), Inches(11.733), Inches(6.1))
    card1.fill.solid()
    card1.fill.fore_color.rgb = DEEP_BLUE
    card1.line.color.rgb = ACCENT_BLUE
    card1.line.width = Pt(2)

    tb1 = slide1.shapes.add_textbox(Inches(1.2), Inches(0.95), Inches(10.933), Inches(5.6))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "PROJECT PRESENTATION & TECHNICAL DEFENSE"
    p.font.name = "Calibri"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = ACCENT_BLUE
    p.space_after = Pt(8)

    p = tf1.add_paragraph()
    p.text = "Molecular Property Prediction &\nIn-Silico ADMET Intelligence Platform"
    p.font.name = "Calibri"
    p.font.size = Pt(27)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.space_after = Pt(10)

    p = tf1.add_paragraph()
    p.text = "An End-to-End Multi-Endpoint Machine Learning Architecture for Aqueous Solubility (LogS), Lipophilicity, Pharmacokinetics, Toxicity Profiling, Local Explainability (XAI), and Generative Lead Optimization"
    p.font.name = "Calibri"
    p.font.size = Pt(12.5)
    p.font.color.rgb = RGBColor(203, 213, 225)
    p.space_after = Pt(16)

    # Key highlight badge ribbon
    p = tf1.add_paragraph()
    p.text = "★ KEY RESULTS: Solubility R² = 0.9029 | ClinTox AUC = 0.9249 | BBBP AUC = 0.9042 | 2,068D Hybrid Features | 10 ML Algorithms Benchmarked"
    p.font.name = "Calibri"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = EMERALD
    p.space_after = Pt(24)

    p = tf1.add_paragraph()
    p.text = "RESEARCH CANDIDATE DETAILS:"
    p.font.name = "Calibri"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = RGBColor(148, 163, 184)
    p.space_after = Pt(6)

    p = tf1.add_paragraph()
    p.text = "• M. Pramod       —   Registration Number: 24BAI1417\nProgram: B.Tech Computer Science and Engineering (Specialization in AI & ML)\nDepartment: School of Computer Science and Engineering (SCOPE)"
    p.font.name = "Calibri"
    p.font.size = Pt(11.5)
    p.font.color.rgb = WHITE

    add_notes(slide1, """[SLIDE 1 PRESENTATION SCRIPT]:
"Good morning, respected Sir. Today, I am pleased to present my project: 'Molecular Property Prediction & In-Silico ADMET Intelligence Platform'.

In this project, we address a primary bottleneck in pharmaceutical drug development: predicting whether a candidate small molecule will dissolve in human blood, reach its target organ, and be safe without fatal toxicity.

We engineered an end-to-end AI platform that takes raw chemical structures, transforms them into a novel 2,068-dimensional hybrid feature representation, benchmarks 10 distinct machine learning algorithms, scales across 5 ADMET clinical endpoints, and achieves state-of-the-art predictive performance (R² = 0.9029 on solubility, and ROC-AUC over 92% on clinical toxicity).

Allow us to walk you step-by-step through our introduction, problem statement, research gaps, objectives, system architecture, methodology, datasets, and empirical experimental results."
""")

    # =========================================================================
    # SLIDE 2: Introduction (Brief Intro to Problem and Proposed Work)
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    add_header(slide2, "1. Introduction", "Introduction to Molecular Property Prediction & In-Silico ADMET Intelligence", "Accelerating drug discovery through computational cheminformatics and machine learning")
    add_footer(slide2, 2)

    w3 = Inches(3.64)
    h_card = Inches(5.5)
    y_card = Inches(1.4)

    # Card 1: Biomedical Importance
    add_card(slide2, Inches(0.8), y_card, w3, h_card, "1. The Biomedical Context", CARD_BG, ACCENT_BLUE)
    add_bullet_list(slide2, Inches(1.0), y_card + Inches(0.55), w3 - Inches(0.4), h_card - Inches(0.7), [
        ("Aqueous Solubility (LogS): ", "Primary physicochemical determinant of oral bioavailability. An oral pill must dissolve in gastrointestinal fluids to enter systemic circulation."),
        ("Membrane Permeability (LogD): ", "Molecules must balance aqueous dissolution with lipophilic partition to permeate cell membranes."),
        ("ADMET Pharmacokinetics: ", "Absorption, Distribution, Metabolism, Excretion, and Toxicity govern whether a drug reaches target tissues safely."),
        ("The Molecular Reality: ", "A potent inhibitor against a disease receptor is clinically useless if it precipitates out of solution or induces organ toxicity.")
    ], 10.5, 8)

    # Card 2: The Pharmaceutical Bottleneck
    add_card(slide2, Inches(4.84), y_card, w3, h_card, "2. The Pharmaceutical Crisis", CARD_BG, ROSE)
    add_bullet_list(slide2, Inches(5.04), y_card + Inches(0.55), w3 - Inches(0.4), h_card - Inches(0.7), [
        ("High Candidate Attrition: ", "Over 90% of newly discovered drug candidates fail during development, never reaching approval."),
        ("Preclinical Solubility Failure: ", "Over 40% of small-molecule candidates fail preclinically due to poor aqueous solubility."),
        ("Clinical ADMET Failure: ", "Over 80% of clinical trial failures stem from poor pharmacokinetic bioavailability or unexpected toxicity."),
        ("Enormous Financial Burden: ", "Developing a single approved drug requires 10 to 15 years and exceeds $2.6 Billion in cost."),
        ("Wet-Lab Limitations: ", "Physical synthesis and animal assays cannot scale to screen millions of candidate compounds.")
    ], 10.5, 8)

    # Card 3: Our Proposed In-Silico Solution
    add_card(slide2, Inches(8.88), y_card, w3, h_card, "3. Proposed In-Silico Work", CARD_BG, EMERALD)
    add_bullet_list(slide2, Inches(9.08), y_card + Inches(0.55), w3 - Inches(0.4), h_card - Inches(0.7), [
        ("2,068D Hybrid Engineering: ", "Concatenates 20 macroscopic descriptors with 2,048-bit Morgan circular fingerprints (ECFP4) to bridge thermodynamics and topology."),
        ("10-Model Benchmark: ", "Systematic evaluation of 10 ML algorithms across 6 diverse paradigm families (Tree Ensembles, Kernels, Deep Learning, Meta-Learners)."),
        ("5-Endpoint ADMET Suite: ", "Scales from solubility (LogS) to lipophilicity (LogD), blood-brain barrier (BBBP), clinical toxicity (ClinTox), and genotoxicity (Tox21)."),
        ("Local XAI & Lead Optimizer: ", "Generates atom-level contour attribution maps and executes 8 automated bioisosteric reaction transforms to fix liabilities."),
        ("Production Deployment: ", "14-page Streamlit research dashboard and high-throughput FastAPI REST microservice.")
    ], 10.5, 8)

    add_notes(slide2, """[SLIDE 2 PRESENTATION SCRIPT]:
"Sir, on this slide, we introduce the scientific context and our proposed solution:

1. Biomedical Context: For any oral drug to work in the human body, it must first dissolve in gastric fluids (measured by LogS) and balance lipophilicity to cross biological membranes.
2. The Crisis: The pharmaceutical industry suffers from a massive attrition rate: over 40% of molecules fail preclinically due to low solubility, and 80% fail in clinical trials due to ADMET pharmacokinetics and toxicity. Bringing one approved drug to market takes over 10-15 years and $2.6 Billion. Wet-lab testing millions of compounds is physically impossible.
3. Our Proposed In-Silico Platform: We designed an automated machine learning platform that screens chemical compounds in milliseconds. We construct a 2,068-dimensional hybrid representation fusing macroscopic thermodynamics with circular fingerprints, benchmark 10 diverse ML models, predict 5 clinical ADMET endpoints, provide Explainable AI contour maps, and automate lead optimization."
""")

    # =========================================================================
    # SLIDE 3: Problem Statement (Identified Through Literature Survey)
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    add_header(slide3, "2. Problem Statement", "Problem Statement Identified Through Literature Survey", "Critical bottlenecks and limitations identified from prior literature in molecular property modeling")
    add_footer(slide3, 3)

    # 3 Focused Cards
    add_card(slide3, Inches(0.8), y_card, w3, h_card, "1. Candidate Attrition Bottleneck", CARD_BG, ROSE)
    add_bullet_list(slide3, Inches(1.0), y_card + Inches(0.55), w3 - Inches(0.4), h_card - Inches(0.7), [
        ("Late-Stage Clinical Failures: ", "Literature reveals that >80% of drug candidate failures in Phase II/III clinical trials are caused by poor ADMET profiles and safety liabilities rather than target efficacy."),
        ("Insoluble Lead Compounds: ", "Combinatorial chemistry and high-throughput screening often yield lipophilic, insoluble hits (>40% failure), leading to poor oral absorption and crystal precipitation in vivo."),
        ("Experimental Screening Barrier: ", "Physical synthesis, crystallization assays, and animal pharmacokinetics cost millions of dollars per compound and take weeks per assay."),
        ("Urgent Need: ", "Early computational screening to fail unviable compounds virtually on Day 1.")
    ], 10.5, 8)

    add_card(slide3, Inches(4.84), y_card, w3, h_card, "2. Single-Modality Representation Flaws", CARD_BG, AMBER)
    add_bullet_list(slide3, Inches(5.04), y_card + Inches(0.55), w3 - Inches(0.4), h_card - Inches(0.7), [
        ("Descriptor-Only Blindness: ", "Conventional QSAR models rely exclusively on 1D/2D bulk descriptors (e.g., MolWt, LogP). They cannot distinguish positional isomers with identical molecular weight but radically different solubility."),
        ("Fingerprint-Only Limitations: ", "Circular topological bit vectors (Morgan/ECFP) identify localized functional groups but lose global thermodynamic scaling, mass, and crystal packing energy."),
        ("Multicollinearity & Singular Inversion: ", "Expanding chemical feature dimensions causes severe multicollinearity, leading to rank deficiency and mathematical collapse in standard linear models (p > n).")
    ], 10.5, 8)

    add_card(slide3, Inches(8.88), y_card, w3, h_card, "3. Black-Box & Siloed Architectures", CARD_BG, ACCENT_BLUE)
    add_bullet_list(slide3, Inches(9.08), y_card + Inches(0.55), w3 - Inches(0.4), h_card - Inches(0.7), [
        ("Lack of Mechanistic Interpretability: ", "Existing neural network and ensemble models operate as black boxes, outputting scalar values without explaining WHICH specific atoms or functional groups cause insolubility or toxicity."),
        ("Regulatory & Medicinal Chemistry Barrier: ", "Regulatory agencies (FDA/EMA) and medicinal chemists require clear mechanistic rationales before synthesis."),
        ("Single-Property Isolation: ", "Most prior academic projects model aqueous solubility in isolation, ignoring correlated downstream pharmacokinetic and toxicity endpoints."),
        ("No Structural Remediation: ", "Existing tools predict liabilities but offer no automated chemistry solutions to fix them.")
    ], 10.5, 8)

    add_notes(slide3, """[SLIDE 3 PRESENTATION SCRIPT]:
"Sir, based on our literature survey, we identified three core problems:

1. The Attrition Crisis: Over 40% of candidates fail preclinically due to poor solubility, and over 80% fail in human clinical trials due to pharmacokinetic ADMET issues or unexpected toxicity. Developing physical compounds only to fail in Phase II or Phase III costs billions of dollars.
2. Cheminformatics Representation Deficiencies: Existing literature shows that classical models suffer from single-modality representations:
   - Using only 20 physical descriptors makes the model completely blind to structural isomers that have the exact same molecular weight.
   - Using only binary circular fingerprints loses the macroscopic thermodynamic context of overall molecular bulk and crystalline lattice packing.
   - When scaling features, unregularized linear models mathematically collapse due to rank-deficient multicollinearity (p > n).
3. Black-Box Silos: Prior machine learning systems provide predictions without explaining the underlying chemical mechanism (lack of XAI) and focus on a single isolated property without multi-endpoint ADMET coverage or automated lead remediation."
""")

    # =========================================================================
    # SLIDE 4: Research Gaps (Identified from Literature Survey)
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    add_header(slide4, "3. Research Gaps", "Research Gaps Identified from Literature Survey", "Four fundamental technical and methodological gaps observed in current molecular property prediction systems")
    add_footer(slide4, 4)

    w2 = Inches(5.6)
    h_gap = Inches(2.65)
    y1 = Inches(1.4)
    y2 = Inches(4.25)

    # Gap 1
    add_card(slide4, Inches(0.8), y1, w2, h_gap, "Gap 1: Representation Trade-off (Local vs. Global)", CARD_BG, AMBER)
    add_bullet_list(slide4, Inches(1.0), y1 + Inches(0.45), w2 - Inches(0.4), h_gap - Inches(0.55), [
        ("Literature Status: ", "Prior studies predominantly utilize either macroscopic physical descriptors OR bit-based circular fingerprints in isolation."),
        ("Unresolved Gap: ", "Lack of a unified, empirically validated hybrid feature representation that simultaneously captures global thermodynamic bulk (crystalline packing) and fine-grained localized topological substructures without information loss.")
    ], 10.5, 6)

    # Gap 2
    add_card(slide4, Inches(6.8), y1, w2, h_gap, "Gap 2: Algorithm Scalability in High Dimensions", CARD_BG, AMBER)
    add_bullet_list(slide4, Inches(7.0), y1 + Inches(0.45), w2 - Inches(0.4), h_gap - Inches(0.55), [
        ("Literature Status: ", "Most publications report single-algorithm implementations (e.g., standard Random Forest or Support Vector Regression) on low-dimensional features."),
        ("Unresolved Gap: ", "Absence of systematic, multi-family benchmarking (comparing bagging, boosting, kernel methods, deep learning, and meta-ensembles) to identify which learning paradigm resists overfitting in high-dimensional sparse chemical spaces (p > 2,000).")
    ], 10.5, 6)

    # Gap 3
    add_card(slide4, Inches(0.8), y2, w2, h_gap, "Gap 3: Isolated Single-Endpoint Modeling", CARD_BG, AMBER)
    add_bullet_list(slide4, Inches(1.0), y2 + Inches(0.45), w2 - Inches(0.4), h_gap - Inches(0.55), [
        ("Literature Status: ", "Prior academic benchmarks typically focus exclusively on aqueous solubility (e.g., Delaney ESOL) as an isolated regression task."),
        ("Unresolved Gap: ", "Neglect of concurrent multi-endpoint ADMET modeling—failing to evaluate how changes in solubility concurrently impact lipophilicity (LogD), blood-brain barrier permeability (BBBP), clinical trial toxicity (ClinTox), and p53 genotoxicity.")
    ], 10.5, 6)

    # Gap 4
    add_card(slide4, Inches(6.8), y2, w2, h_gap, "Gap 4: Absence of Explainability & Generative Remediation", CARD_BG, AMBER)
    add_bullet_list(slide4, Inches(7.0), y2 + Inches(0.45), w2 - Inches(0.4), h_gap - Inches(0.55), [
        ("Literature Status: ", "Existing computational tools output opaque numerical predictions without visual atom-level rationales or actionable structural feedback."),
        ("Unresolved Gap: ", "Critical lack of Local Explainable AI (XAI) contour attribution maps showing which functional groups cause liabilities, combined with an absence of automated generative bioisosteric SAR engines to remediate flagged liabilities.")
    ], 10.5, 6)

    add_notes(slide4, """[SLIDE 4 PRESENTATION SCRIPT]:
"Sir, from our comprehensive literature survey, we synthesized four distinct research gaps:

- Gap 1 (Representation Trade-off): Studies either use 20 bulk descriptors or 2,048 bit fingerprints. There is no unified hybrid representation proven to balance macroscopic thermodynamics with localized topological connectivity.
- Gap 2 (Algorithm Scalability): Most literature only tests one or two algorithms (like basic RF or SVR). There is a lack of rigorous benchmarking across diverse machine learning families (linear, kernel, neural nets, bagging, boosting, and meta-ensembles) when handling 2,000+ sparse chemical features.
- Gap 3 (Isolated Single-Endpoint Silos): Academic works model solubility in isolation, ignoring that a drug candidate must simultaneously satisfy lipophilicity, blood-brain barrier penetration, and non-toxicity to succeed in humans.
- Gap 4 (Lack of XAI & Remediation): Prior systems act as black boxes. They do not tell the medicinal chemist which specific atoms make the molecule insoluble or toxic, and they provide zero automated bioisosteric suggestions to fix the problem."
""")

    # =========================================================================
    # SLIDE 5: Research Objectives (Directly Addressing Research Gaps)
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    add_header(slide5, "4. Research Objectives", "Research Objectives Directly Addressing Identified Gaps", "Targeted, measurable technical objectives formulated to overcome each identified research gap")
    add_footer(slide5, 5)

    h_obj = Inches(1.0)
    w_obj = Inches(11.733)
    y_start = Inches(1.35)
    gap_y = Inches(1.12)

    objs = [
        ("Objective 1: Engineer a 2,068-Dimensional Hybrid Feature Representation (Addresses Gap 1)",
         "Design, implement, and validate a unified hybrid feature vector concatenating 20 macroscopic RDKit physicochemical descriptors (MW, LogP, TPSA, HBD, HBA) with 2,048-bit Morgan circular topological fingerprints (ECFP4, radius=2) to simultaneously capture global thermodynamics and fine local topology.",
         EMERALD),
        ("Objective 2: Systematic 10-Algorithm Machine Learning Benchmark (Addresses Gap 2)",
         "Implement, hyperparameter-tune, and evaluate 10 distinct algorithms across 6 machine learning families (Linear OLS, Ridge, SVR RBF, KNN, MLP Neural Net, Random Forest, Extra Trees, Gradient Boosting, HistGradientBoosting, and Stacking Regressor) on held-out test data and 5-fold cross-validation.",
         ACCENT_BLUE),
        ("Objective 3: Construct a Multi-Endpoint ADMET Prediction Suite (Addresses Gap 3)",
         "Expand the predictive architecture beyond solubility to 5 critical pharmacokinetic and safety endpoints: Aqueous Solubility (LogS), Physiological Lipophilicity (LogD7.4), Blood-Brain Barrier Penetration (BBBP), Clinical Toxicity Failure (ClinTox), and Tox21 p53 Genotoxicity.",
         PURPLE),
        ("Objective 4: Implement Local Explainable AI (XAI) & Generative SAR Engine (Addresses Gap 4)",
         "Develop atom-level 2D contour attribution maps fusing Wildman-Crippen LogP and Gasteiger partial charges to visualize atomic contributions, and engineer a generative lead optimization engine applying 8 medicinal chemistry bioisosteric reaction transforms to remediate molecular liabilities.",
         EMERALD),
        ("Objective 5: Full-Stack Deployment & Automated Regulatory Dossier Generation",
         "Deploy a publication-grade 14-page interactive Streamlit research dashboard (featuring a 2D JSME ChemDraw canvas and 3D conformer viewer), a containerized FastAPI REST microservice with OpenAPI Swagger docs, and automated one-click PDF/HTML preclinical dossier generation.",
         DEEP_BLUE)
    ]

    for idx, (title, desc, color) in enumerate(objs):
        y_pos = y_start + (idx * gap_y)
        add_card(slide5, Inches(0.8), y_pos, w_obj, h_obj, title, CARD_BG, color, color)
        # Text inside card
        tb = slide5.shapes.add_textbox(Inches(1.0), y_pos + Inches(0.38), w_obj - Inches(0.4), Inches(0.55))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = desc
        p.font.name = "Calibri"
        p.font.size = Pt(10)
        p.font.color.rgb = DARK_TEXT

    add_notes(slide5, """[SLIDE 5 PRESENTATION SCRIPT]:
"Sir, our research objectives directly map to each of the four research gaps we identified:

1. Objective 1 directly solves Gap 1: We engineer a 2,068-dimensional hybrid feature vector fusing 20 macroscopic descriptors with 2,048-bit Morgan circular fingerprints (ECFP4).
2. Objective 2 directly solves Gap 2: We conduct a comprehensive benchmark across 10 distinct algorithms spanning 6 machine learning families, validating which algorithms withstand high-dimensional sparse spaces.
3. Objective 3 directly solves Gap 3: We expand from single-endpoint solubility to 5 multi-endpoint ADMET models: Solubility, Lipophilicity, Blood-Brain Barrier Penetration, Clinical Toxicity, and p53 DNA damage.
4. Objective 4 directly solves Gap 4: We integrate Local Explainable AI (XAI) contour heatmaps to mechanistically explain predictions at the individual atom level and build a generative SAR engine with 8 bioisosteric transformations to automatically propose improved drug analogs.
5. Objective 5: We deploy the platform into an interactive 14-page Streamlit research dashboard and a production FastAPI REST microservice."
""")

    # =========================================================================
    # SLIDE 6: Architecture Diagram (Proposed System Architecture)
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    add_header(slide6, "5. Architecture Diagram", "Architecture of the Proposed In-Silico ADMET Platform", "High-throughput end-to-end computational pipeline from chemical structure ingestion to multi-endpoint inference and export")
    add_footer(slide6, 6)

    # Left: Structured Pipeline Execution Cards (width ~4.9 in)
    w_arch_text = Inches(4.9)
    add_card(slide6, Inches(0.8), Inches(1.35), w_arch_text, Inches(5.6), "End-to-End Computational Pipeline", CARD_BG, BORDER_COLOR)
    add_bullet_list(slide6, Inches(1.0), Inches(1.85), w_arch_text - Inches(0.4), Inches(4.95), [
        ("Layer 1: Ingestion & Preprocessing: ", "Accepts 1D SMILES, 45+ curated FDA drug library, or interactive 2D JSME ChemDraw sketching. RDKit validates valences, kekulizes aromatic systems, and sanitizes stereochemistry."),
        ("Layer 2: Hybrid Feature Extraction: ", "Extracts 20 macroscopic descriptors + 2,048-bit Morgan circular fingerprints (ECFP4, r=2) concatenated into a 2,068D hybrid vector."),
        ("Layer 3: Multi-Endpoint ML Engine: ", "Concurrent inference across 5 tuned tree ensembles: Solubility (LogS), Lipophilicity (LogD), BBBP, ClinTox, and Tox21 p53."),
        ("Layer 4: Explainability & Safety: ", "Atom-level SimilarityMaps contour heatmaps (Crippen LogP + Gasteiger charges), 480 PAINS filters, Brenk toxicophores, and Lipinski/Veber rule compliance."),
        ("Layer 5: Generative Bioisosteric SAR: ", "8 SMARTS bioisostere transforms generate ranked analogs with real-time delta improvements (Delta LogS, Delta QED)."),
        ("Layer 6: Application & Serving: ", "Interactive 14-page Streamlit dashboard, FastAPI REST API (Swagger at /docs), and automated preclinical dossier PDF/HTML export.")
    ], 10, 5)

    # Right: High-Resolution Pipeline Architecture Diagram Image (width ~6.6 in)
    img_arch = os.path.join(results_dir, "pipeline_architecture_diagram.png")
    if os.path.exists(img_arch):
        slide6.shapes.add_picture(img_arch, Inches(5.9), Inches(1.35), Inches(6.633), Inches(5.6))

    add_notes(slide6, """[SLIDE 6 PRESENTATION SCRIPT]:
"Sir, this slide displays the complete system architecture of our proposed platform:

1. Ingestion: The user inputs a chemical structure via a 1D SMILES string, selects from our library of 45 reference FDA drugs, or draws any novel molecule on our embedded 2D JSME ChemDraw canvas.
2. Sanitization: RDKit sanitizes the structure, checking strict chemical valences (carbon=4, nitrogen=3/5, oxygen=2) and kekulizing aromatic rings.
3. Feature Pipeline: We compute 20 macroscopic descriptors (mass, polar surface area, hydrogen bond counts) and 2,048-bit Morgan circular fingerprints (ECFP4), concatenating them into a 2,068-dimensional hybrid feature vector.
4. Multi-Endpoint ML Engine: The 2,068D vector is dispatched simultaneously to 5 production tree-ensemble models: Aqueous Solubility (LogS), Lipophilicity (LogD), Blood-Brain Barrier (BBBP), Clinical Toxicity (ClinTox), and Tox21 p53 DNA damage.
5. XAI & Safety: In parallel, our explainability engine maps Crippen LogP and Gasteiger charges into 2D contour heatmaps showing which atoms hurt or help solubility, while screening 480 PAINS filters and drug-likeness rules.
6. Generative Lead Optimizer: If liabilities exist, 8 medicinal chemistry bioisostere transforms generate and rank improved analogs.
7. Serving Layer: All capabilities are surfaced through a 14-page Streamlit research dashboard, a production FastAPI microservice, and a 1-click regulatory dossier generator."
""")

    # =========================================================================
    # SLIDE 7: Methodology and Implementation (Steps, Preprocessing, Algorithms)
    # =========================================================================
    slide7 = prs.slides.add_slide(blank_layout)
    add_header(slide7, "6. Methodology & Implementation", "Methodology, Preprocessing Techniques & Algorithms Implemented", "Systematic execution workflow, chemical data preprocessing, and 10 machine learning algorithms evaluated")
    add_footer(slide7, 7)

    w3_m = Inches(3.64)

    # Panel 1: Execution Steps
    add_card(slide7, Inches(0.8), y_card, w3_m, h_card, "1. Execution Steps Followed", CARD_BG, ACCENT_BLUE)
    add_bullet_list(slide7, Inches(1.0), y_card + Inches(0.55), w3_m - Inches(0.4), h_card - Inches(0.7), [
        ("Step 1 (Ingestion & Sanitization): ", "Parse 1D SMILES; validate atomic valences, stereochemistry, and ring aromaticity via RDKit."),
        ("Step 2 (Feature Engineering): ", "Extract 20 macroscopic descriptors and compute 2,048-bit Morgan circular fingerprints (ECFP4, r=2) -> 2,068D vector."),
        ("Step 3 (Partitioning & CV): ", "80% training / 20% held-out test split (seed=42) combined with 5-fold cross-validation for strict generalization."),
        ("Step 4 (Hyperparameter Tuning): ", "GridSearchCV and RandomizedSearchCV over tree depth, estimator count, and split criteria."),
        ("Step 5 (Multi-Endpoint Training): ", "Train and calibrate 5 specialized ADMET models."),
        ("Step 6 (XAI & Generative SAR): ", "Compute Crippen-Gasteiger atomic weight matrices for contour heatmaps and execute 8 SMARTS transforms.")
    ], 10, 6)

    # Panel 2: Preprocessing Techniques
    add_card(slide7, Inches(4.84), y_card, w3_m, h_card, "2. Preprocessing Techniques", CARD_BG, EMERALD)
    add_bullet_list(slide7, Inches(5.04), y_card + Inches(0.55), w3_m - Inches(0.4), h_card - Inches(0.7), [
        ("Valence & Stereochemical Sanitization: ", "Rejects chemically invalid structures (e.g., pentavalent carbon). Aromatic rings kekulized to establish explicit single/double bond alternation."),
        ("Log-Scale Target Normalization: ", "Solubility transformed to Log10(mol/L), normalizing exponential 12-order variation into a smooth Gaussian distribution."),
        ("Z-Score Standardization: ", "Continuous descriptors standardized (mean=0, std=1) for distance-sensitive algorithms (KNN, SVR, Ridge, MLP)."),
        ("Modulo Hashing: ", "Maps radial atom neighborhoods into a fixed 2,048-length binary vector via modulo hashing: bit = hash % 2048."),
        ("Class-Weight Balancing: ", "Applied balanced class weights on ClinTox and Tox21 to overcome severe positive-case scarcity (toxic compounds <10%).")
    ], 10, 6)

    # Panel 3: 10 Implemented Algorithms
    add_card(slide7, Inches(8.88), y_card, w3_m, h_card, "3. 10 Implemented Algorithms", CARD_BG, PURPLE)
    add_bullet_list(slide7, Inches(9.08), y_card + Inches(0.55), w3_m - Inches(0.4), h_card - Inches(0.7), [
        ("Tree Ensembles (Production Engine): ", ""),
        ("1. Extra Trees Regressor/Classifier: ", "150 randomized trees, bootstrap=False. Selected production model for all 5 ADMET tasks."),
        ("2. Random Forest: ", "100 bagged trees with optimal threshold splits."),
        ("3. Gradient Boosting & HistGradientBoosting: ", "Sequential residual boosting with 256 integer binning."),
        ("Meta-Ensemble Architectures: ", ""),
        ("4. Stacking Regressor: ", "Level-0: ET + HGB + RF -> Level-1: Ridge Meta-Learner (Benchmark Leader)."),
        ("5. Voting Regressor: ", "Weighted ensemble average."),
        ("Baseline Paradigm Families: ", ""),
        ("6. SVR (RBF Kernel): ", "Support Vector Regression."),
        ("7. MLP Neural Net: ", "Feedforward Deep Neural Network."),
        ("8. KNN: ", "Instance-based k-nearest neighbors."),
        ("9. Ridge Regression: ", "L2 regularized linear model."),
        ("10. Linear Regression (OLS): ", "Ordinary least squares.")
    ], 9.5, 4)

    add_notes(slide7, """[SLIDE 7 PRESENTATION SCRIPT]:
"Sir, on this slide we present our methodology, preprocessing techniques, and all 10 algorithms implemented:

1. Execution Steps: Ingestion and valence check -> 2,068D hybrid feature extraction -> 80/20 train/test split with 5-fold cross-validation -> hyperparameter tuning -> multi-endpoint model training -> XAI contour generation and generative lead optimization.
2. Preprocessing Techniques:
   - Chemical valence validation and aromatic kekulization via RDKit.
   - Target normalization: taking Log10 of solubility normalizes an exponential 12-order magnitude range into a smooth Gaussian distribution.
   - Z-score standard scaling for distance and linear models.
   - Modulo hashing for circular fingerprints.
   - Class-weight balancing to handle clinical toxicity imbalance.
3. 10 Implemented Algorithms across 6 Paradigm Families:
   - Tree Ensembles: Extra Trees (our production engine), Random Forest, Gradient Boosting, HistGradientBoosting.
   - Meta-Ensembles: Stacking Regressor (Level-0: ET+HGB+RF combined via Ridge meta-learner) and Voting Regressor.
   - Kernel & Distance Methods: Support Vector Regressor (SVR RBF) and KNN.
   - Deep Learning: Multi-Layer Perceptron (MLP) Neural Net.
   - Linear Models: Ridge Regression and Ordinary Least Squares."
""")

    # =========================================================================
    # SLIDE 8: Dataset (Datasets Used for Implementation and Evaluation)
    # =========================================================================
    slide8 = prs.slides.add_slide(blank_layout)
    add_header(slide8, "7. Dataset", "Benchmark Datasets Used for Implementation & Evaluation", "Five peer-reviewed public datasets spanning physicochemical, pharmacokinetic, and toxicological endpoints")
    add_footer(slide8, 8)

    w_top_card = Inches(11.733)
    add_card(slide8, Inches(0.8), Inches(1.35), w_top_card, Inches(4.2), "The 5 Multi-Endpoint Benchmark Datasets", CARD_BG, BORDER_COLOR)

    # Create structured table of datasets
    shape_table = slide8.shapes.add_table(6, 6, Inches(1.0), Inches(1.85), Inches(11.333), Inches(3.5))
    table = shape_table.table
    table.columns[0].width = Inches(1.8) # Dataset
    table.columns[1].width = Inches(2.2) # Endpoint Task
    table.columns[2].width = Inches(1.2) # Sample Size
    table.columns[3].width = Inches(2.3) # Target Description
    table.columns[4].width = Inches(1.8) # Primary Source
    table.columns[5].width = Inches(2.033) # Evaluation Metrics

    headers = ["Dataset Name", "Endpoint / Task", "Samples (N)", "Target Property / Unit", "Literature Source", "Evaluation Metrics"]
    for col_idx, h in enumerate(headers):
        cell = table.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.name = "Calibri"
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = WHITE
        p.alignment = PP_ALIGN.CENTER

    dataset_rows = [
        ("Delaney ESOL", "Aqueous Solubility (LogS)\n[Continuous Regression]", "1,128", "Log10 molar solubility (mol/L) at 25°C\nRange: -11.6 to +1.58", "Delaney et al. (2004)\nMoleculeNet Benchmark", "R², MAE, RMSE\n(5-Fold CV & Held-Out Test)"),
        ("ChEMBL Lipophilicity", "Distribution Coeff (LogD7.4)\n[Continuous Regression]", "4,200", "Octanol/water distribution at pH 7.4\nMembrane permeability proxy", "EMBL-EBI ChEMBL\nMoleculeNet Benchmark", "R², MAE, RMSE\n(5-Fold CV & Held-Out Test)"),
        ("MoleculeNet BBBP", "Blood-Brain Barrier Permeability\n[Binary Classification]", "2,050", "Permeant (1) vs Non-permeant (0)\nCNS active therapeutic filter", "Martins et al. (2012)\nMoleculeNet Benchmark", "ROC-AUC, Accuracy, F1\nPrecision, Recall"),
        ("FDA ClinTox", "Clinical Trial Toxicity Failure\n[Binary Classification]", "1,484", "Failed clinical trial toxicity (1)\nvs FDA approved drugs (0)", "FDA AERS Database\nMoleculeNet Benchmark", "ROC-AUC, Accuracy, F1\nBalanced Sensitivity"),
        ("NIH Tox21 p53", "p53 Genotoxicity / DNA Damage\n[Binary Classification]", "6,774", "Transcriptional p53 cellular stress\nactivation (DNA repair pathway)", "NIH Tox21 Data Challenge\nNational Toxicology Program", "ROC-AUC, Accuracy, F1\nBalanced Specificity")
    ]

    for row_idx, row in enumerate(dataset_rows, start=1):
        bg_col = CARD_BG if row_idx % 2 == 1 else RGBColor(241, 245, 249)
        for col_idx, val in enumerate(row):
            cell = table.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg_col
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.name = "Calibri"
            p.font.size = Pt(9.5)
            p.font.color.rgb = DARK_TEXT
            if col_idx in [0, 2]:
                p.font.bold = True
                p.alignment = PP_ALIGN.CENTER
            elif col_idx in [1, 5]:
                p.alignment = PP_ALIGN.CENTER

    # Bottom summary card: Data Curation & Validation Protocol
    add_card(slide8, Inches(0.8), Inches(5.65), w_top_card, Inches(1.35), "Data Curation & Validation Protocol", CARD_BG, ACCENT_BLUE)
    add_bullet_list(slide8, Inches(1.0), Inches(6.05), w_top_card - Inches(0.4), Inches(0.85), [
        ("Chemical Diversity: ", "Encompasses small organic fragments, agrochemicals, FDA approved therapeutics, natural products, and synthetic drug candidates."),
        ("Strict Validation Standard: ", "Every dataset partitioned into 80% Training and 20% Held-Out Test sets (seed=42) alongside 5-Fold Cross-Validation to prevent data leakage."),
        ("Cheminformatics Curation: ", "Salt stripping, inorganic removal, duplicate SMILES resolution, and explicit valence verification applied across all datasets.")
    ], 10, 4)

    add_notes(slide8, """[SLIDE 8 PRESENTATION SCRIPT]:
"Sir, on this slide we present the 5 peer-reviewed benchmark datasets used in our implementation:

1. Delaney ESOL (1,128 compounds): The gold-standard benchmark for aqueous solubility (LogS), ranging from freely soluble (+1.58) to virtually insoluble (-11.60 mol/L).
2. ChEMBL Lipophilicity (4,200 compounds): Measures the distribution coefficient (LogD) at physiological pH 7.4 from the European Bioinformatics Institute, determining membrane permeability.
3. MoleculeNet BBBP (2,050 compounds): Curated clinical dataset determining whether compounds penetrate the blood-brain barrier to target CNS diseases or avoid central neurotoxicity.
4. FDA ClinTox (1,484 compounds): Contains FDA-approved drugs compared against clinical candidates that failed clinical trials due to unexpected human toxicity.
5. NIH Tox21 p53 Challenge (6,774 compounds): Evaluates whether a compound triggers the cellular p53 tumor suppressor pathway, acting as an early biomarker for DNA damage and mutagenicity.

All datasets were curated with salt stripping, duplicate resolution, an 80/20 train/test partition, and 5-fold cross-validation."
""")

    # =========================================================================
    # SLIDE 9: Results and Outcomes (Key Results, Graphs, Clear & Focused)
    # =========================================================================
    slide9 = prs.slides.add_slide(blank_layout)
    add_header(slide9, "8. Results & Outcomes", "Key Results, Experimental Graphs & Platform Outcomes", "State-of-the-art predictive accuracy, empirical ablation validation, and full-stack software deliverables")
    add_footer(slide9, 9)

    w_left_res = Inches(5.5)

    # Left Column: Key Results & Outcomes Summary Card
    add_card(slide9, Inches(0.8), Inches(1.35), w_left_res, Inches(5.6), "Key Results & Platform Outcomes", CARD_BG, BORDER_COLOR)
    add_bullet_list(slide9, Inches(1.0), Inches(1.85), w_left_res - Inches(0.4), Inches(4.95), [
        ("State-of-the-Art Solubility (LogS): ", "Extra Trees achieves R² = 0.9029, MAE = 0.4628, and RMSE = 0.6775 on Delaney ESOL. Our error is within experimental wet-lab assay variance (±0.50 log units). Stacking Regressor achieves R² = 0.9090 (MAE = 0.4490)."),
        ("Empirical Feature Ablation: ", "Combining macroscopic descriptors with circular fingerprints cut prediction error by 52% and boosted R² from 0.6389 (Fingerprints Only) to 0.9029 (Hybrid 2,068D)."),
        ("Multi-Endpoint ADMET Classification: ", ""),
        ("• ClinTox (Clinical Toxicity): ", "ROC-AUC = 0.9249 | Accuracy = 89.9%"),
        ("• BBBP (Blood-Brain Barrier): ", "ROC-AUC = 0.9042 | Accuracy = 88.5%"),
        ("• Tox21 p53 (Genotoxicity): ", "ROC-AUC = 0.8767 | Accuracy = 92.1%"),
        ("• Lipophilicity (LogD7.4): ", "R² = 0.6015 | MAE = 0.5021 | RMSE = 0.7182"),
        ("Explainable AI (XAI) Outcome: ", "Generates 2D atom contour heatmaps (Crippen LogP + Gasteiger charges) revealing exact solubilizing vs insolubilizing functional groups."),
        ("Generative Lead Optimization: ", "Successfully executes 8 bioisosteric transformations, producing ranked drug analogs with positive Delta LogS and drug-likeness improvements."),
        ("Deployed Production Deliverables: ", "14-page Streamlit research dashboard with 2D/3D viewers, production FastAPI REST microservice, and automated regulatory dossier export.")
    ], 9.8, 4)

    # Right Column: Two prominent research experiment graphs
    img_comp = os.path.join(results_dir, "expanded_model_comparison.png")
    img_roc = os.path.join(results_dir, "multi_endpoint_roc_curves.png")

    if os.path.exists(img_comp):
        # Top right graph: 10-Algorithm Comparison Chart (width ~6.0 in, height ~2.7 in)
        slide9.shapes.add_picture(img_comp, Inches(6.5), Inches(1.35), Inches(6.033), Inches(2.7))

    if os.path.exists(img_roc):
        # Bottom right graph: Multi-Endpoint ROC Curves (width ~6.0 in, height ~2.7 in)
        slide9.shapes.add_picture(img_roc, Inches(6.5), Inches(4.2), Inches(6.033), Inches(2.75))

    add_notes(slide9, """[SLIDE 9 PRESENTATION SCRIPT]:
"Sir, to conclude our presentation, here are our key results, experimental graphs, and platform outcomes:

1. Quantitative Results:
   - On Aqueous Solubility (Delaney ESOL), our Extra Trees production model achieves R² = 0.9029 and MAE = 0.4628 log units. Our prediction error is lower than the inherent physical variability of wet-lab experimental assays (±0.50 log units). Stacking Regressor achieves R² = 0.9090.
   - On the top right graph, you can observe our 10-algorithm benchmark: Tree ensembles and meta-learners vastly outperform linear and neural network baselines on this sparse chemical feature space.
   - On the bottom right graph, you can see our multi-endpoint ROC curves: We achieve outstanding discrimination with ROC-AUC of 0.9249 on Clinical Toxicity (ClinTox), 0.9042 on Blood-Brain Barrier Penetration (BBBP), and 0.8767 on Tox21 p53 Genotoxicity.
2. Empirical Ablation Finding: Fusing 20 macroscopic descriptors with 2,048 circular fingerprints cut prediction error by 52% and broke past the prestigious 0.90 R² threshold.
3. Software Engineering Outcomes:
   - We delivered a production 14-page Streamlit research dashboard with an interactive 2D JSME ChemDraw canvas and hardware-accelerated 3D conformer viewer.
   - We built a high-throughput FastAPI REST microservice with interactive OpenAPI Swagger documentation.
   - We integrated Local Explainable AI contour heatmaps and an automated generative SAR engine executing 8 bioisosteric transformations.

Thank you, respected Sir. I am now eager and ready to answer any questions you may have regarding my research, methodology, or live system demonstration."
""")

    # Save to both target file and a clean backup file
    target_path = "Molecular_Property_Prediction_Presentation.pptx"
    backup_path = "Molecular_Property_Prediction_9Slides.pptx"

    prs.save(target_path)
    print(f"[SUCCESS] Saved master presentation to: {target_path}")

    prs.save(backup_path)
    print(f"[SUCCESS] Saved backup presentation to: {backup_path}")

if __name__ == "__main__":
    build_presentation()
