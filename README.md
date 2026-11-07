# Molecular Property Prediction & In-Silico ADMET Intelligence Platform

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![RDKit](https://img.shields.io/badge/RDKit-2023.9+-005A9C?style=for-the-badge&logo=chemistry&logoColor=white)](https://www.rdkit.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.4+-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white)](https://scikit-learn.org/)

**B.Tech Computer Science and Engineering (Specialization in Artificial Intelligence & Machine Learning)**  

### Author & Lead Researcher
- **M. Pramod** — `24BAI1417`

---

## 1. Executive Summary & Clinical Motivation

More than **40% of newly discovered chemical compounds fail clinical translation** due to unfavorable Absorption, Distribution, Metabolism, Excretion, and Toxicity (**ADMET**) profiles, with poor aqueous solubility ($\text{LogS}$) standing as the primary culprit behind formulation attrition.

This repository hosts an **End-to-End Enterprise Cheminformatics & In-Silico Drug Discovery Platform** fusing:
1. **Multi-Endpoint AI/ML Models**: Predicting Aqueous Solubility ($\text{LogS}$), Lipophilicity ($\text{LogD}_{7.4}$), Blood-Brain Barrier Penetration ($\text{BBBP}$), Clinical Trial Toxicity Failure ($\text{ClinTox}$), and $\text{p53}$ DNA Damage / Genotoxicity ($\text{Tox21}$).
2. **Interactive 2D ChemDraw Studio (JSME)**: Browser-based chemical sketcher allowing researchers to draw molecular structures with mouse and predict ADMET properties with 1 click.
3. **Local Explainable AI (XAI)**: High-resolution atom-level contour attribution maps revealing exactly which functional groups promote or hinder aqueous solubility.
4. **Generative Lead Optimizer**: Medicinal chemistry AI applying verified bioisosteric transformations (e.g. Carboxylic Acid $\to$ 1H-Tetrazole, Fluorine scanning, Morpholine solubilization, Cyclopropyl rigidification) to rescue failing drug candidates.
5. **Real-Time Web Platform & Microservice**: Interactive Single-Page Web Application served directly via FastAPI (`http://localhost:8000`) featuring real-time 3D WebGL molecular rotation (3Dmol.js), 2D vector topology, live ADMET radar charts, Local Explainable AI contour heatmaps, generative bioisosteres, batch screening, and OpenAPI Swagger (`/docs`). Also includes Streamlit Research Dashboard (`app.py`).

---

## 2. Multi-Endpoint Machine Learning Benchmarks

All models utilize a **2,068-dimensional hybrid feature representation** (20 macroscopic physicochemical RDKit descriptors + 2,048-bit Morgan circular topological fingerprints [ECFP4]):

| Target Property | Task Type | Benchmark Dataset | Production Algorithm | Key Test Metric | Benchmark Performance |
| :--- | :--- | :--- | :--- | :---: | :---: |
| **Aqueous Solubility ($\text{LogS}$)** | Regression | Delaney ESOL ($N=1,128$) | Hybrid Extra Trees | $R^2$ / $\text{MAE}$ | **$R^2 = 0.9029$** ($\text{MAE} = 0.4628$) |
| **Lipophilicity ($\text{LogD}_{7.4}$)** | Regression | ChEMBL Lipophilicity ($N=4,200$) | Hybrid Extra Trees | $R^2$ / $\text{MAE}$ | **$R^2 = 0.6015$** ($\text{MAE} = 0.5021$) |
| **Blood-Brain Barrier ($\text{BBBP}$)** | Classification | MoleculeNet BBBP ($N=2,050$) | Hybrid Extra Trees | $\text{ROC-AUC}$ / $\text{Acc}$ | **$\text{ROC-AUC} = 0.9042$** ($\text{Acc} = 88.5\%$) |
| **Clinical Toxicity ($\text{ClinTox}$)** | Classification | FDA / MoleculeNet ($N=1,484$) | Hybrid Extra Trees | $\text{ROC-AUC}$ / $\text{Acc}$ | **$\text{ROC-AUC} = 0.9249$** ($\text{Acc} = 89.9\%$) |
| **p53 Genotoxicity / Stress** | Classification | Tox21 Challenge ($N=6,774$) | Hybrid Extra Trees | $\text{ROC-AUC}$ / $\text{Acc}$ | **$\text{ROC-AUC} = 0.8767$** ($\text{Acc} = 92.1\%$) |

---

## 3. Platform Architecture

```
                                   ┌───────────────────────────────────┐
                                   │  Chemical Input: SMILES / JSME   │
                                   └─────────────────┬─────────────────┘
                                                     │
                                                     ▼
                                   ┌───────────────────────────────────┐
                                   │      Hybrid Feature Extraction    │
                                   │  • 20 RDKit Molecular Descriptors │
                                   │  • 2,048-bit Morgan Circular FPs  │
                                   └─────────────────┬─────────────────┘
                                                     │
                        ┌────────────────────────────┼────────────────────────────┐
                        ▼                            ▼                            ▼
        ┌──────────────────────────────┐ ┌──────────────────────┐ ┌──────────────────────────────┐
        │   Multi-Endpoint ML Suite    │ │ Local XAI Heatmaps   │ │   AI Lead Optimizer (SAR)    │
        │ • Solubility LogS (R²=0.90)  │ │ • SimilarityMaps     │ │ • 1H-Tetrazole Bioisostere   │
        │ • Lipophilicity LogD         │ │ • Crippen LogP Map   │ │ • Metabolic Fluorine Scan    │
        │ • Blood-Brain Barrier (BBBP) │ │ • Gasteiger Charges  │ │ • Morpholine Solubilizing    │
        │ • ClinTox Failure Risk       │ │ • PAINS Highlight    │ │ • Cyclopropyl Rigidification │
        │ • Tox21 p53 Genotoxicity     │ │ • Brenk Toxicophores │ │ • Side-by-Side Δ Evaluation  │
        └───────────────┬──────────────┘ └──────────┬───────────┘ └──────────────┬───────────────┘
                        │                           │                            │
                        └───────────────────────────┼────────────────────────────┘
                                                    │
                                                    ▼
                        ┌─────────────────────────────────────────────────────────┐
                        │              Production Application Layer               │
                        │  1. Streamlit Dashboard (14 Dedicated Research Pages)   │
                        │  2. FastAPI Production REST API (OpenAPI /docs)         │
                        │  3. Preclinical Regulatory Dossier Generator (HTML/PDF) │
                        └─────────────────────────────────────────────────────────┘
```

---

## 4. Key Platform Capabilities

### 1. 🎨 2D Molecule Canvas (ChemDraw Studio)
- Full-featured **JSME JavaScript Molecular Editor** embedded directly inside the web dashboard.
- Draw structures, add rings, bonds, heteroatoms with mouse, extract SMILES, and run full ADMET screening in real time.

### 2. 🔬 AI Molecular Lead Optimizer & Bioisostere Generator
- Automatic medicinal chemistry SAR generator:
  - **Carboxylic Acid $\to$ 1H-Tetrazole**: Preserves acidity ($\text{p}K_a \sim 4.8$) while lowering polar desolvation penalty.
  - **Metabolic Fluorination**: Blocks oxidative CYP450 soft-spots without substantial steric clash.
  - **Morpholine & Piperazine Solubilization**: Dramatically boosts aqueous solubility via salt formation.
  - **Cyclopropyl Rigidification**: Enforces bioactive conformation, reducing entropic penalty of binding.
- Computes real-time $\Delta \text{LogS}$, $\Delta \text{QED}$, $\Delta \text{Overall Score}$, and generates a ranked comparative lead optimization table.

### 3. 🔍 Explainable AI (XAI) & Chemical Attribution Maps
- Renders high-resolution 2D contour similarity maps:
  - 🟢 **Green/Cyan Contours**: Hydrophilic/polar moieties (hydroxyl, amino, carbonyl) favoring solubility.
  - 🔴 **Orange/Red Contours**: Hydrophobic bulk (aromatic carbons, alkyl chains) opposing solubility.
- Real-time screening of **PAINS** (Pan-Assay Interference Compounds) and **Brenk** structural alerts with atomic highlight subgraphs.

### 4. 📄 One-Click Preclinical Regulatory Dossier Export
- Generates a standalone, styled HTML discovery dossier containing:
  - Complete Physicochemical Characterization (MW, TPSA, LogP, HBD, HBA, Fsp3)
  - Pharmacokinetics Profile (Caco-2 Permeability, HIA %, PPB %, CYP1A2/2C9/2D6/3A4)
  - Toxicology & Safety Evaluation (ClinTox, p53 Genotoxicity, PAINS, Brenk)
  - Drug-Likeness Compliance (Lipinski Rule of 5, Veber, Ghose, Egan, QED, Pfizer CNS MPO Score)

### 5. 🚀 Virtual High-Throughput Screening (Batch vHTS)
- Screen 45+ reference FDA drugs across 9 therapeutic categories or upload custom CSV/TXT batch files.
- Real-time multi-metric scatter plots, hit-list filters, and 1-click comprehensive CSV export.

---

## 5. Project Directory Structure

```
Molecular_Property_Prediction/
├── app.py                             # 14-page Streamlit Research Dashboard
├── api.py                             # Production FastAPI Microservice (/docs)
├── requirements.txt                   # Verified environment dependencies
├── Dockerfile                         # Cloud & Container Deployment image
├── docker-compose.yml                 # Multi-container orchestration
├── run_dashboard.bat                  # 1-Click Windows Dashboard Launcher
├── run_api.bat                        # 1-Click Windows FastAPI Launcher
├── README.md                          # Comprehensive Documentation
├── .streamlit/
│   └── config.toml                    # Modern Dark Theme Configuration
├── data/
│   ├── delaney-processed.csv          # Delaney ESOL raw dataset
│   ├── lipophilicity_raw.csv          # ChEMBL Lipophilicity dataset
│   ├── bbbp_raw.csv                   # Blood-Brain Barrier dataset
│   ├── clintox_raw.csv                # Clinical Toxicity Failure dataset
│   ├── tox21_raw.csv                  # Tox21 Challenge dataset
│   └── molecular_features.csv         # 20 extracted RDKit descriptors
├── models/
│   ├── final_combined_solubility_model.pkl # Delaney Extra Trees (R²=0.9029)
│   ├── lipophilicity_model.pkl        # Lipophilicity Extra Trees
│   ├── bbbp_model.pkl                 # Blood-Brain Barrier Extra Trees
│   ├── clintox_model.pkl              # Clinical Trial Toxicity Extra Trees
│   └── p53_toxicity_model.pkl         # Tox21 p53 Genotoxicity Extra Trees
├── src/
│   ├── admet_engine.py                # Core multi-endpoint ADMET prediction engine
│   ├── explainability_engine.py       # XAI atom attribution heatmaps & toxicophores
│   ├── lead_optimizer.py              # AI Bioisosteric analog generator (SAR)
│   ├── dossier_generator.py           # Preclinical regulatory HTML dossier export
│   ├── 01_data_preparation.py         # SMILES ingestion & descriptor extraction
│   ├── 08_train_final_combined_model.py # Production Delaney hybrid model training
│   ├── 11_train_multitask_admet_models.py # Lipophilicity & BBBP training
│   └── 12_train_expanded_admet_models.py  # ClinTox & Tox21 p53 training
└── results/                           # Benchmark CSVs, ROC curves, feature importance
```

---

## 6. How to Run & Deploy

### A. Local Run (Windows / Linux / macOS)

1. **Activate Virtual Environment**:
   ```bash
   # Windows
   .\venv\Scripts\activate

   # Linux / macOS
   source venv/bin/activate
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch the Streamlit Research Dashboard**:
   ```bash
   # Double click run_dashboard.bat OR run:
   streamlit run app.py
   ```
   Open `http://localhost:8501` in your browser.

4. **Launch the Production FastAPI REST API**:
   ```bash
   # Double click run_api.bat OR run:
   uvicorn api:app --host 0.0.0.0 --port 8000 --reload
   ```
   Open `http://localhost:8000/docs` to interact with Swagger UI.

---

### B. Containerized Deployment (Docker)

Build and run using Docker Compose:
```bash
docker-compose up --build
```
- **Streamlit Dashboard:** `http://localhost:8501`
- **FastAPI REST API:** `http://localhost:8000/docs`

---

### C. 1-Click Free Cloud Deployment (Streamlit Community Cloud & Hugging Face)

#### Deploy to Streamlit Cloud:
1. Push this repository to your GitHub account.
2. Go to [share.streamlit.io](https://share.streamlit.io/) and click **"New App"**.
3. Select your repository, branch `main`, and main file path `app.py`.
4. Click **Deploy!** Your app is live with a public URL in ~2 minutes!

#### Deploy to Hugging Face Spaces:
1. Create a new Space on [huggingface.co/spaces](https://huggingface.co/spaces) (Select **Streamlit** SDK or **Docker**).
2. Push repository code to the Hugging Face Space git remote.
3. Hugging Face builds and hosts the app with free cloud GPU/CPU and instant sharing!

---

## 7. REST API Endpoints Overview

| Method | Endpoint | Description | Sample Payload |
| :---: | :--- | :--- | :--- |
| `GET` | `/health` | Health check & model status | None |
| `POST` | `/api/v1/predict/admet` | Full ADMET characterization | `{"smiles": "CC(=O)Oc1ccccc1C(=O)O"}` |
| `POST` | `/api/v1/optimize/lead` | Generate bioisosteric analogs | `{"smiles": "CC(=O)Oc1ccccc1C(=O)O"}` |
| `POST` | `/api/v1/explain/attribution` | Atom attribution heatmap & weights | `{"smiles": "CC(=O)Oc1ccccc1C(=O)O"}` |
| `POST` | `/api/v1/screening/batch` | Batch virtual screening (up to 100) | `{"molecules": [{"id": "1", "smiles": "CCO"}]}` |

---

## 8. Academic Attribution & Viva Defense

This project was developed as a flagship AI/ML research initiative under the **B.Tech Computer Science and Engineering (AI & ML)** program by:
- **M. Pramod** — `24BAI1417`
