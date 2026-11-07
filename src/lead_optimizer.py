"""
AI Molecular Lead Optimizer & Bioisosteric Replacement Engine
Generates intelligent medicinal chemistry structural modifications,
evaluates in silico ADMET improvements, and ranks optimized lead candidates.
Lead Developer: M. Pramod (24BAI1417)
"""

from typing import Dict, Any, List, Optional
from rdkit import Chem
from rdkit.Chem import AllChem

from src.admet_engine import predict_full_admet


# Curated Medicinal Chemistry Transformation Library
MEDCHEM_RULES = [
    {
        "id": "tetrazole_bioisostere",
        "name": "Carboxylic Acid -> 1H-Tetrazole Bioisostere",
        "rationale": "Maintains planar acidic pharmacophore (pKa ~4.8) while increasing lipophilic permeability and reducing glucuronidation.",
        "smarts": "[C:1](=[O:2])[OH:3]>>[c:1]1nnn[nH]1"
    },
    {
        "id": "primary_amide",
        "name": "Carboxylic Acid -> Primary Amide",
        "rationale": "Eliminates negative charge at physiological pH, improving passive membrane permeability.",
        "smarts": "[C:1](=[O:2])[OH:3]>>[C:1](=[O:2])N"
    },
    {
        "id": "aromatic_fluorination",
        "name": "Metabolic C-F Fluorine Scan",
        "rationale": "Blocks oxidative cytochrome P450 soft-spots without introducing steric clash, improving metabolic half-life.",
        "smarts": "[c;H1:1]>>[c:1]F"
    },
    {
        "id": "aromatic_hydroxylation",
        "name": "Polar Hydroxyl (-OH) Grafting",
        "rationale": "Directly enhances aqueous hydration enthalpy and lowers LogP for poorly soluble candidates.",
        "smarts": "[c;H1:1]>>[c:1]O"
    },
    {
        "id": "aromatic_cyanation",
        "name": "Nitrile (-C#N) Polar Bioisostere",
        "rationale": "Introduces linear dipole for target hydrogen bonding while improving metabolic clearance.",
        "smarts": "[c;H1:1]>>[c:1]C#N"
    },
    {
        "id": "aza_bioisostere",
        "name": "Benzene -> Pyridine Aza-Bioisostere",
        "rationale": "Replaces aromatic CH with basic nitrogen, lowering LogP by ~0.8 units and enhancing aqueous solubility.",
        "smarts": "[c:1]1[c:2][c:3][c:4][c:5][c:6]1>>[c:1]1[c:2][n:3][c:4][c:5][c:6]1"
    },
    {
        "id": "o_methylation",
        "name": "Phenol / Alcohol O-Methylation",
        "rationale": "Protects labile phenolic hydroxyls from Phase II glucuronidation / sulfation.",
        "smarts": "[O;H1:1]>>[O:1]C"
    },
    {
        "id": "n_methylation",
        "name": "Amide / Amine N-Methylation",
        "rationale": "Removes intermolecular H-bond donor, boosting blood-brain barrier and intestinal permeability.",
        "smarts": "[N;H1,H2:1]>>[N:1]C"
    },
    {
        "id": "morpholine_tail",
        "name": "Morpholine Solubilizing Tail",
        "rationale": "Incorporates basic oxygen-heterocycle for substantial aqueous solubility and PK improvement.",
        "smarts": "[c:1][C:2](=[O:3])[OH:4]>>[c:1][C:2](=[O:3])N1CCOCC1"
    },
    {
        "id": "piperazine_tail",
        "name": "N-Methylpiperazine Solubilizing Tail",
        "rationale": "Enables ionizable tertiary amine salt formation, dramatically increasing LogS.",
        "smarts": "[c:1][C:2](=[O:3])[OH:4]>>[c:1][C:2](=[O:3])N1CCN(C)CC1"
    },
    {
        "id": "ester_to_oxadiazole",
        "name": "Ester -> 1,2,4-Oxadiazole Bioisostere",
        "rationale": "Prevents rapid esterase cleavage in human plasma.",
        "smarts": "[C:1](=[O:2])O[C:3]>>[c:1]1nc([C:3])no1"
    },
    {
        "id": "aromatic_amination",
        "name": "Aromatic Amination (-NH2)",
        "rationale": "Adds basic hydrogen bond donor/acceptor center to enhance target potency and solubility.",
        "smarts": "[c;H1:1]>>[c:1]N"
    },
    {
        "id": "aliphatic_hydroxylation",
        "name": "Aliphatic C-H Hydroxylation",
        "rationale": "Converts inert hydrocarbon positions to polar carbinols, enhancing solubility.",
        "smarts": "[C;H2,H3:1]>>[C:1]O"
    }
]


def generate_lead_analogs(smiles: str, max_analogs: int = 6) -> Dict[str, Any]:
    """
    Applies medchem transformations to parent molecule, computes full ADMET,
    and returns ranked analog candidates with delta improvements.
    """
    clean_smi = smiles.strip()
    parent_mol = Chem.MolFromSmiles(clean_smi)
    if parent_mol is None:
        raise ValueError("Invalid parent SMILES.")

    parent_admet = predict_full_admet(clean_smi)
    parent_logs = parent_admet["Predictions"]["Solubility_LogS"]
    parent_qed = parent_admet["Drug_Likeness"]["QED"]
    parent_score = parent_admet["Overall_Candidate_Score"]

    generated_analogs = []
    seen_smiles = {parent_admet["Canonical_SMILES"], clean_smi}

    for rule in MEDCHEM_RULES:
        try:
            rxn = AllChem.ReactionFromSmarts(rule["smarts"])
            products = rxn.RunReactants((parent_mol,))
            
            if not products:
                continue

            for p_tuple in products:
                p_mol = p_tuple[0]
                try:
                    Chem.SanitizeMol(p_mol)
                    p_smiles = Chem.MolToSmiles(p_mol)
                except Exception:
                    continue

                if p_smiles in seen_smiles or len(p_smiles) < 3:
                    continue

                # Run full ADMET on analog
                try:
                    p_admet = predict_full_admet(p_smiles)
                except Exception:
                    continue

                seen_smiles.add(p_smiles)

                p_logs = p_admet["Predictions"]["Solubility_LogS"]
                p_qed = p_admet["Drug_Likeness"]["QED"]
                p_score = p_admet["Overall_Candidate_Score"]

                delta_logs = round(p_logs - parent_logs, 3)
                delta_qed = round(p_qed - parent_qed, 3)
                delta_score = round(p_score - parent_score, 1)

                analog_entry = {
                    "Rule_Applied": rule["name"],
                    "Rule_Rationale": rule["rationale"],
                    "Analog_SMILES": p_smiles,
                    "Formula": p_admet["Formula"],
                    "ADMET": p_admet,
                    "Delta_Solubility_LogS": delta_logs,
                    "Delta_QED": delta_qed,
                    "Delta_Overall_Score": delta_score,
                    "Solubility_Improved": delta_logs > 0,
                    "DrugLikeness_Improved": delta_qed > 0,
                    "Score_Improved": delta_score > 0
                }
                generated_analogs.append(analog_entry)

                if len(generated_analogs) >= max_analogs * 3:
                    break
        except Exception:
            continue

    # Sort analogs by overall candidate score improvement
    generated_analogs.sort(key=lambda x: x["Delta_Overall_Score"], reverse=True)
    top_analogs = generated_analogs[:max_analogs]

    # Identify best in categories
    best_solubility_analog = None
    if top_analogs:
        best_solubility_analog = max(top_analogs, key=lambda x: x["Delta_Solubility_LogS"])

    return {
        "Parent_Molecule": parent_admet,
        "Analogs_Count": len(top_analogs),
        "Analogs": top_analogs,
        "Best_Solubility_Analog": best_solubility_analog,
        "Best_Overall_Lead": top_analogs[0] if top_analogs else None
    }
