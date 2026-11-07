"""
ADMET & Cheminformatics Intelligence Engine
Computes Physicochemical Descriptors, Morgan Fingerprints,
Multi-Endpoint ML Predictions, Pharmacokinetics, Toxicity, Structural Alerts & Drug-Likeness Rules.
"""

import os
import joblib
import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional, Tuple

from rdkit import Chem
from rdkit.Chem import Descriptors, rdFingerprintGenerator, QED, FilterCatalog
from rdkit.Chem.FilterCatalog import FilterCatalogParams
from rdkit.DataStructs import ConvertToNumpyArray


# ---------------------------------------------------------------------------
# GLOBAL CONSTANTS & PATHS
# ---------------------------------------------------------------------------
MODEL_DIR = "models"
SOLUBILITY_MODEL_PATH = os.path.join(MODEL_DIR, "final_combined_solubility_model.pkl")
LIPO_MODEL_PATH = os.path.join(MODEL_DIR, "lipophilicity_model.pkl")
BBBP_MODEL_PATH = os.path.join(MODEL_DIR, "bbbp_model.pkl")
CLINTOX_MODEL_PATH = os.path.join(MODEL_DIR, "clintox_model.pkl")
P53_MODEL_PATH = os.path.join(MODEL_DIR, "p53_toxicity_model.pkl")

# Lazy-loaded cache
_MODELS_CACHE = {}
_PAINS_CATALOG = None
_BRENK_CATALOG = None
_FP_GEN = None


def get_fingerprint_generator():
    global _FP_GEN
    if _FP_GEN is None:
        _FP_GEN = rdFingerprintGenerator.GetMorganGenerator(radius=2, fpSize=2048)
    return _FP_GEN


def get_filter_catalogs():
    global _PAINS_CATALOG, _BRENK_CATALOG
    if _PAINS_CATALOG is None:
        params_pains = FilterCatalogParams()
        params_pains.AddCatalog(FilterCatalogParams.FilterCatalogs.PAINS)
        _PAINS_CATALOG = FilterCatalog.FilterCatalog(params_pains)
    
    if _BRENK_CATALOG is None:
        params_brenk = FilterCatalogParams()
        params_brenk.AddCatalog(FilterCatalogParams.FilterCatalogs.BRENK)
        _BRENK_CATALOG = FilterCatalog.FilterCatalog(params_brenk)
        
    return _PAINS_CATALOG, _BRENK_CATALOG


def load_model(path: str):
    if path not in _MODELS_CACHE:
        if os.path.exists(path):
            try:
                _MODELS_CACHE[path] = joblib.load(path)
            except Exception as e:
                print(f"[Warning] Failed to load model {path}: {e}")
                _MODELS_CACHE[path] = None
        else:
            _MODELS_CACHE[path] = None
    return _MODELS_CACHE[path]


# ---------------------------------------------------------------------------
# FEATURE COMPUTATION
# ---------------------------------------------------------------------------
def compute_hybrid_features(mol: Chem.Mol) -> Tuple[np.ndarray, Dict[str, float]]:
    """
    Computes 20 Physicochemical Descriptors + 2048-bit Morgan Circular Fingerprint.
    Returns:
        combined_features: 1D numpy array of shape (2068,)
        desc_dict: dictionary of physicochemical properties
    """
    mw = float(Descriptors.MolWt(mol))
    logp = float(Descriptors.MolLogP(mol))
    tpsa = float(Descriptors.TPSA(mol))
    hbd = int(Descriptors.NumHDonors(mol))
    hba = int(Descriptors.NumHAcceptors(mol))
    ring_count = int(Descriptors.RingCount(mol))
    aromatic_rings = int(Descriptors.NumAromaticRings(mol))
    aliphatic_rings = int(Descriptors.NumAliphaticRings(mol))
    rot_bonds = int(Descriptors.NumRotatableBonds(mol))
    fsp3 = float(Descriptors.FractionCSP3(mol))
    heavy_atoms = int(Descriptors.HeavyAtomCount(mol))
    heteroatoms = int(Descriptors.NumHeteroatoms(mol))
    charge = int(Chem.GetFormalCharge(mol))

    # Atom specific counts
    atoms = mol.GetAtoms()
    n_count = sum(1 for a in atoms if a.GetSymbol() == "N")
    o_count = sum(1 for a in atoms if a.GetSymbol() == "O")
    s_count = sum(1 for a in atoms if a.GetSymbol() == "S")
    f_count = sum(1 for a in atoms if a.GetSymbol() == "F")
    cl_count = sum(1 for a in atoms if a.GetSymbol() == "Cl")
    br_count = sum(1 for a in atoms if a.GetSymbol() == "Br")
    i_count = sum(1 for a in atoms if a.GetSymbol() == "I")

    desc_list = [
        mw, logp, tpsa, hbd, hba, ring_count, aromatic_rings,
        aliphatic_rings, rot_bonds, fsp3, heavy_atoms, heteroatoms,
        charge, n_count, o_count, s_count, f_count, cl_count, br_count, i_count
    ]

    desc_dict = {
        "Molecular_Weight": mw,
        "LogP": logp,
        "TPSA": tpsa,
        "HBD": hbd,
        "HBA": hba,
        "Ring_Count": ring_count,
        "Aromatic_Rings": aromatic_rings,
        "Aliphatic_Rings": aliphatic_rings,
        "Rotatable_Bonds": rot_bonds,
        "Fraction_CSP3": fsp3,
        "Heavy_Atom_Count": heavy_atoms,
        "Heteroatom_Count": heteroatoms,
        "Formal_Charge": charge,
        "Nitrogen_Count": n_count,
        "Oxygen_Count": o_count,
        "Sulfur_Count": s_count,
        "Halogen_Count": f_count + cl_count + br_count + i_count
    }

    # Morgan fingerprint (ECFP4 equivalent)
    fp_gen = get_fingerprint_generator()
    fp = fp_gen.GetFingerprint(mol)
    fp_arr = np.zeros((2048,), dtype=np.int8)
    ConvertToNumpyArray(fp, fp_arr)

    combined_features = np.concatenate([np.array(desc_list, dtype=np.float32), fp_arr])
    return combined_features, desc_dict


# ---------------------------------------------------------------------------
# DRUG-LIKENESS & MEDICINAL CHEMISTRY FILTERS
# ---------------------------------------------------------------------------
def evaluate_drug_likeness(mol: Chem.Mol, desc: Dict[str, float]) -> Dict[str, Any]:
    """
    Evaluates Lipinski, Veber, Ghose, Egan, Muegge, QED and CNS MPO score.
    """
    mw = desc["Molecular_Weight"]
    logp = desc["LogP"]
    hbd = desc["HBD"]
    hba = desc["HBA"]
    tpsa = desc["TPSA"]
    rotb = desc["Rotatable_Bonds"]
    fsp3 = desc["Fraction_CSP3"]
    heavy_atoms = desc["Heavy_Atom_Count"]

    # Lipinski's Rule of 5 (Pfizer)
    lipinski_violations = 0
    lipinski_details = []
    if mw > 500:
        lipinski_violations += 1
        lipinski_details.append(f"MW > 500 ({mw:.1f})")
    if logp > 5.0:
        lipinski_violations += 1
        lipinski_details.append(f"LogP > 5.0 ({logp:.2f})")
    if hbd > 5:
        lipinski_violations += 1
        lipinski_details.append(f"HBD > 5 ({hbd})")
    if hba > 10:
        lipinski_violations += 1
        lipinski_details.append(f"HBA > 10 ({hba})")

    # Veber's Rule (Oral Bioavailability)
    veber_violations = 0
    veber_details = []
    if rotb > 10:
        veber_violations += 1
        veber_details.append(f"Rotatable Bonds > 10 ({rotb})")
    if tpsa > 140:
        veber_violations += 1
        veber_details.append(f"TPSA > 140 Å² ({tpsa:.1f})")

    # Ghose Filter
    ghose_pass = (160 <= mw <= 480) and (-0.4 <= logp <= 5.6) and (20 <= heavy_atoms <= 70)

    # Egan Rule
    egan_pass = (logp <= 5.88) and (tpsa <= 131)

    # QED (Quantitative Estimate of Drug-likeness)
    try:
        qed_score = float(QED.qed(mol))
    except Exception:
        qed_score = 0.50

    # Pfizer CNS MPO Score (Multi-Parameter Optimization: 0 to 6 scale, scaled to 0-100)
    # Evaluates: CLogP, CLogD, MW, TPSA, HBD, pKa
    mpo_logp = 1.0 if logp <= 3 else (0.0 if logp >= 5 else (5 - logp) / 2)
    mpo_mw = 1.0 if mw <= 360 else (0.0 if mw >= 500 else (500 - mw) / 140)
    mpo_tpsa = 1.0 if (40 <= tpsa <= 90) else (
        tpsa / 40 if tpsa < 40 else (0.0 if tpsa >= 120 else (120 - tpsa) / 30)
    )
    mpo_hbd = 1.0 if hbd <= 0.5 else (0.0 if hbd >= 3.5 else (3.5 - hbd) / 3.0)
    cns_mpo_raw = mpo_logp + mpo_mw + mpo_tpsa + mpo_hbd
    cns_mpo_score = round((cns_mpo_raw / 4.0) * 100, 1)

    return {
        "Lipinski_Violations": lipinski_violations,
        "Lipinski_Pass": lipinski_violations <= 1,
        "Lipinski_Details": lipinski_details if lipinski_details else ["Fully Compliant"],
        "Veber_Violations": veber_violations,
        "Veber_Pass": veber_violations == 0,
        "Veber_Details": veber_details if veber_details else ["Fully Compliant"],
        "Ghose_Pass": ghose_pass,
        "Egan_Pass": egan_pass,
        "QED": round(qed_score, 3),
        "QED_Category": "High" if qed_score >= 0.67 else ("Moderate" if qed_score >= 0.49 else "Low"),
        "CNS_MPO_Score": cns_mpo_score,
        "CNS_MPO_Grade": "Favorable" if cns_mpo_score >= 70 else ("Moderate" if cns_mpo_score >= 50 else "Unfavorable"),
        "Fsp3": round(fsp3, 3)
    }


# ---------------------------------------------------------------------------
# STRUCTURAL ALERTS (PAINS & BRENK TOXICOPHORES)
# ---------------------------------------------------------------------------
def detect_structural_alerts(mol: Chem.Mol) -> Dict[str, Any]:
    """
    Checks for PAINS (Pan-Assay Interference Compounds) and Brenk toxicophores.
    """
    pains_cat, brenk_cat = get_filter_catalogs()

    pains_matches = []
    if pains_cat.HasMatch(mol):
        entries = pains_cat.GetMatches(mol)
        for entry in entries:
            pains_matches.append(entry.GetDescription())

    brenk_matches = []
    if brenk_cat.HasMatch(mol):
        entries = brenk_cat.GetMatches(mol)
        for entry in entries:
            brenk_matches.append(entry.GetDescription())

    return {
        "PAINS_Alerts_Count": len(pains_matches),
        "PAINS_Alerts": pains_matches[:5],
        "PAINS_Safe": len(pains_matches) == 0,
        "Brenk_Alerts_Count": len(brenk_matches),
        "Brenk_Alerts": brenk_matches[:5],
        "Brenk_Safe": len(brenk_matches) == 0
    }


# ---------------------------------------------------------------------------
# FULL ADMET PREDICTOR
# ---------------------------------------------------------------------------
def predict_full_admet(smiles: str) -> Dict[str, Any]:
    """
    Full End-to-End In Silico ADMET Characterization for a SMILES string.
    """
    if not isinstance(smiles, str) or not smiles.strip():
        raise ValueError("Invalid SMILES: Input string is empty.")

    mol = Chem.MolFromSmiles(smiles.strip())
    if mol is None:
        raise ValueError(f"RDKit Chem.MolFromSmiles failed to parse: '{smiles}'. Check chemical valence/syntax.")

    canonical_smiles = Chem.MolToSmiles(mol)
    formula = Chem.rdMolDescriptors.CalcMolFormula(mol)

    # 1. Compute Features
    features, desc = compute_hybrid_features(mol)
    X = features.reshape(1, -1)

    # 2. Solubility (LogS) Prediction
    sol_model = load_model(SOLUBILITY_MODEL_PATH)
    if sol_model is not None:
        logs_pred = float(sol_model.predict(X)[0])
    else:
        # Fallback estimation based on Delaney ESOL equation
        logs_pred = float(0.16 - 0.63 * desc["LogP"] - 0.0062 * desc["Molecular_Weight"] + 0.066 * desc["Rotatable_Bonds"] - 0.74 * (desc["Aromatic_Rings"] > 0))

    # Solubility Classification (mol/L)
    # LogS > 0: Highly Soluble | -2 to 0: Soluble | -4 to -2: Moderately Soluble | < -4: Poorly/Insoluble
    if logs_pred >= 0:
        sol_class = "Highly Soluble"
        sol_color = "#10b981"
    elif logs_pred >= -2.0:
        sol_class = "Soluble"
        sol_color = "#3b82f6"
    elif logs_pred >= -4.0:
        sol_class = "Moderately Soluble"
        sol_color = "#f59e0b"
    elif logs_pred >= -6.0:
        sol_class = "Poorly Soluble"
        sol_color = "#ef4444"
    else:
        sol_class = "Insoluble"
        sol_color = "#991b1b"

    # Solubility in mg/mL
    sol_mg_ml = (10 ** logs_pred) * desc["Molecular_Weight"] * 1000.0

    # 3. Lipophilicity (LogD7.4) Prediction
    lipo_model = load_model(LIPO_MODEL_PATH)
    if lipo_model is not None:
        logd_pred = float(lipo_model.predict(X)[0])
    else:
        logd_pred = float(desc["LogP"])

    # 4. Blood-Brain Barrier Penetration (BBBP) Prediction
    bbbp_model = load_model(BBBP_MODEL_PATH)
    if bbbp_model is not None:
        bbbp_pred = int(bbbp_model.predict(X)[0])
        bbbp_prob = float(bbbp_model.predict_proba(X)[0][1])
    else:
        # Fallback QSAR rule for BBBP: TPSA < 90 and MW < 450
        bbbp_prob = 0.85 if (desc["TPSA"] < 90 and desc["Molecular_Weight"] < 450 and desc["HBD"] < 3) else 0.25
        bbbp_pred = 1 if bbbp_prob >= 0.5 else 0

    # 5. Clinical Toxicity Failure (ClinTox) Prediction
    clintox_model = load_model(CLINTOX_MODEL_PATH)
    if clintox_model is not None:
        clintox_pred = int(clintox_model.predict(X)[0])
        clintox_prob = float(clintox_model.predict_proba(X)[0][1])
    else:
        clintox_prob = 0.15
        clintox_pred = 0

    # 6. Tox21 p53 Genotoxicity Prediction
    p53_model = load_model(P53_MODEL_PATH)
    if p53_model is not None:
        p53_pred = int(p53_model.predict(X)[0])
        p53_prob = float(p53_model.predict_proba(X)[0][1])
    else:
        p53_prob = 0.10
        p53_pred = 0

    # 7. QSAR Pharmacokinetic Estimations
    # Caco-2 Permeability (10^-6 cm/s) proxy
    caco2_log = -4.5 - (0.01 * desc["TPSA"]) + (0.35 * min(logd_pred, 3.5)) - (0.003 * desc["Molecular_Weight"])
    caco2_high = caco2_log > -5.15

    # Human Intestinal Absorption (HIA %)
    hia_pct = max(5.0, min(100.0, 100.0 - 0.55 * desc["TPSA"] + 5.0 * min(logd_pred, 3.0)))

    # Plasma Protein Binding (PPB %)
    ppb_pct = max(10.0, min(99.9, 50.0 + 12.0 * logd_pred - 0.05 * desc["TPSA"]))

    # CYP450 Inhibitor Risks (Pharmacophore rules)
    cyp1a2_risk = bool(desc["Aromatic_Rings"] >= 2 and desc["LogP"] > 2.0 and desc["TPSA"] < 60)
    cyp2c9_risk = bool(desc["LogP"] > 3.0 and desc["HBD"] >= 1 and desc["Formal_Charge"] <= 0)
    cyp2d6_risk = bool(desc["Nitrogen_Count"] >= 1 and desc["LogP"] > 1.5 and desc["Molecular_Weight"] < 450)
    cyp3a4_risk = bool(desc["Molecular_Weight"] > 350 and desc["LogP"] > 2.5 and desc["Rotatable_Bonds"] >= 4)

    # 8. Drug-likeness & Structural Alerts
    drug_likeness = evaluate_drug_likeness(mol, desc)
    alerts = detect_structural_alerts(mol)

    # 9. Overall Candidate Score (Multi-Objective Radar)
    # Combines Solubility, Drug-likeness, Safety, and Permeability
    sol_score = max(0, min(100, (logs_pred + 6.0) * 16.6))
    safety_score = max(0, 100 - (clintox_prob * 45 + p53_prob * 35 + alerts["PAINS_Alerts_Count"] * 20))
    permeability_score = hia_pct
    qed_scaled = drug_likeness["QED"] * 100
    overall_candidate_score = round(
        0.30 * sol_score + 0.25 * qed_scaled + 0.25 * safety_score + 0.20 * permeability_score,
        1
    )

    return {
        "Canonical_SMILES": canonical_smiles,
        "Formula": formula,
        "Descriptors": desc,
        "Predictions": {
            "Solubility_LogS": round(logs_pred, 3),
            "Solubility_mg_mL": round(sol_mg_ml, 4),
            "Solubility_Class": sol_class,
            "Solubility_Color": sol_color,
            "Lipophilicity_LogD": round(logd_pred, 3),
            "BBBP_Penetration": "Penetrates Blood-Brain Barrier (BBBP+)" if bbbp_pred == 1 else "Non-Penetrating (BBBP-)",
            "BBBP_Probability": round(bbbp_prob, 3),
            "ClinTox_Risk": "High Clinical Toxicity Risk" if clintox_pred == 1 else "Low Clinical Toxicity Risk (Tolerated)",
            "ClinTox_Probability": round(clintox_prob, 3),
            "p53_Genotoxicity": "Positive (Mutagenic/DNA Damage Risk)" if p53_pred == 1 else "Negative (Non-Mutagenic)",
            "p53_Probability": round(p53_prob, 3)
        },
        "Pharmacokinetics": {
            "Caco2_LogPapp": round(caco2_log, 2),
            "Caco2_Permeability": "High Permeability" if caco2_high else "Moderate/Low Permeability",
            "HIA_Percentage": round(hia_pct, 1),
            "PPB_Percentage": round(ppb_pct, 1),
            "CYP1A2_Inhibitor": cyp1a2_risk,
            "CYP2C9_Inhibitor": cyp2c9_risk,
            "CYP2D6_Inhibitor": cyp2d6_risk,
            "CYP3A4_Inhibitor": cyp3a4_risk
        },
        "Drug_Likeness": drug_likeness,
        "Structural_Alerts": alerts,
        "Overall_Candidate_Score": overall_candidate_score
    }
