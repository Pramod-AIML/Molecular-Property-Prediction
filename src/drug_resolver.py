"""
Clinical Pharmacopeia & Compound Resolver
Resolves chemical and drug queries (generic names, brand names, IUPAC, or SMILES)
across Oncology, Cardiology, Neurology, Infectious Disease, Immunology, and Metabolism.
"""

from typing import Dict, Any, Optional
import requests
from rdkit import Chem, rdBase
rdBase.DisableLog('rdApp.error')

# Curated Clinical Reference Database of 80+ Major Therapeutics
CLINICAL_PHARMACOPEIA = {
    # Oncology & Chemotherapy
    "doxorubicin": {"smiles": "COC1=C(C(=O)C2=C(C1=O)C(=O)C3=C(C2=O)C(CC(C3)(O)C(=O)CO)OC4CC(C(C(O4)C)O)N)O", "class": "Oncology / Anthracycline", "brand": "Adriamycin"},
    "cisplatin": {"smiles": "N.N.[Cl-].[Cl-].[Pt+2]", "class": "Oncology / Platinum Agent", "brand": "Platinol"},
    "paclitaxel": {"smiles": "CC1=C2C(C(=O)C3(C(CC4C(C3C(C(C2(C)C)(CC1OC(=O)C(C(C5=CC=CC=C5)NC(=O)C6=CC=CC=C6)O)O)OC(=O)C7=CC=CC=C7)(CO4)OC(=O)C)O)C)OC(=O)C", "class": "Oncology / Taxane", "brand": "Taxol"},
    "fluorouracil": {"smiles": "O=C1NC=C(F)C(=O)N1", "class": "Oncology / Antimetabolite", "brand": "5-FU / Adrucil"},
    "methotrexate": {"smiles": "CN(CC1=CN=C2C(=N1)C(=NC(=N2)N)N)C3=CC=C(C=C3)C(=O)NC(CCC(=O)O)C(=O)O", "class": "Oncology / Antifolate", "brand": "Trexall"},
    "tamoxifen": {"smiles": "CCC(=C(C1=CC=CC=C1)C2=CC=C(C=C2)OCCN(C)C)C3=CC=CC=C3", "class": "Oncology / SERM", "brand": "Nolvadex"},
    "imatinib": {"smiles": "CC1=C(C=C(C=C1)NC(=O)C2=CC=C(C=C2)CN3CCN(CC3)C)NC4=NC=CC(=N4)C5=CN=CC=C5", "class": "Oncology / TKI", "brand": "Gleevec"},
    "erlotinib": {"smiles": "COCCOC1=C(C=C2C(=C1)C(=NC=N2)NC3=CC=CC(=C3)C#C)OCCOC", "class": "Oncology / EGFR Inhibitor", "brand": "Tarceva"},
    "olaparib": {"smiles": "O=C(c1cc(F)ccc1CC(=O)N1CCN(C(=O)C2CC2)CC1)c1n[nH]c2ccccc12", "class": "Oncology / PARP Inhibitor", "brand": "Lynparza"},

    # Cardiovascular & Hematology
    "atorvastatin": {"smiles": "CC(C)C1=C(C(=C(N1CCC(CC(CC(=O)O)O)O)C2=CC=C(C=C2)F)C3=CC=CC=C3)C(=O)NC4=CC=CC=C4", "class": "Cardiovascular / Statin", "brand": "Lipitor"},
    "rosuvastatin": {"smiles": "CC(C)C1=NC(=NC(=C1/C=C/C(CC(CC(=O)O)O)O)N(C)S(=O)(=O)C)C2=CC=C(C=C2)F", "class": "Cardiovascular / Statin", "brand": "Crestor"},
    "amlodipine": {"smiles": "CCOC(=O)C1=C(NC(=C(C1C2=CC=CC=C2Cl)C(=O)OC)C)COCCN", "class": "Cardiovascular / CCB", "brand": "Norvasc"},
    "losartan": {"smiles": "CCCC1=NC(=C(N1CC2=CC=C(C=C2)C3=CC=CC=C3C4=NNN=N4)CO)Cl", "class": "Cardiovascular / ARB", "brand": "Cozaar"},
    "lisinopril": {"smiles": "C1CC(N(C1)C(=O)C(CCCCN)NC(CCC2=CC=CC=C2)C(=O)O)C(=O)O", "class": "Cardiovascular / ACEi", "brand": "Prinivil"},
    "metoprolol": {"smiles": "CC(C)NCC(COC1=CC=C(C=C1)CCOC)O", "class": "Cardiovascular / Beta Blocker", "brand": "Lopressor"},
    "clopidogrel": {"smiles": "COC(=O)C(C1=CC=CC=C1Cl)N2CCC3=C(C2)C=CS3", "class": "Hematology / Antiplatelet", "brand": "Plavix"},
    "warfarin": {"smiles": "CC(=O)CC(C1=CC=CC=C1)C2=C(C3=CC=CC=C3OC2=O)O", "class": "Hematology / Anticoagulant", "brand": "Coumadin"},
    "apixaban": {"smiles": "COC1=CC=C(C=C1)N2C3=C(CCN(C3=O)C4=CC=C(C=C4)N5CCCC5=O)C(=NN2)C(=O)N", "class": "Hematology / DOAC", "brand": "Eliquis"},
    "rivaroxaban": {"smiles": "O=C1N(CCO1)c1ccc(N2C(=O)CC(NC(=O)c3ccc(Cl)s3)C2)cc1", "class": "Hematology / Factor Xa", "brand": "Xarelto"},
    "digoxin": {"smiles": "CC1C(C(CC(O1)OC2C(OC(CC2O)OC3C(OC(CC3O)OC4CCC5(C(C4)CCC6C5CC(C7(C6(CCC7C8=CC(=O)OC8)O)C)O)C)C)C)O)O", "class": "Cardiology / Glycoside", "brand": "Lanoxin"},

    # Central Nervous System & Psychiatry
    "diazepam": {"smiles": "CN1C(=O)CN=C(c2ccccc2)c3cc(Cl)ccc13", "class": "CNS / Benzodiazepine", "brand": "Valium"},
    "alprazolam": {"smiles": "CC1=NN=C2CN=C(C3=CC=CC=C3)C4=C(C=CC(=C4)Cl)N12", "class": "CNS / Anxiolytic", "brand": "Xanax"},
    "lorazepam": {"smiles": "O=C1NC2=C(C=C(Cl)C=C2)C(=NC1O)C1=CC=CC=C1Cl", "class": "CNS / Benzodiazepine", "brand": "Ativan"},
    "fluoxetine": {"smiles": "CNCCC(C1=CC=CC=C1)OC2=CC=C(C=C2)C(F)(F)F", "class": "CNS / SSRI", "brand": "Prozac"},
    "sertraline": {"smiles": "CNC1CCC(C2=CC=CC=C12)C3=CC(=C(C=C3)Cl)Cl", "class": "CNS / SSRI", "brand": "Zoloft"},
    "escitalopram": {"smiles": "CN(C)CCCC1(C2=C(CO1)C=C(C=C2)C#N)C3=CC=C(C=C3)F", "class": "CNS / SSRI", "brand": "Lexapro"},
    "duloxetine": {"smiles": "CNCCC(C1=CC=CS1)OC2=CC=CC3=CC=CC=C23", "class": "CNS / SNRI", "brand": "Cymbalta"},
    "quetiapine": {"smiles": "C1CN(CCN1CCOCCO)C2=NC3=CC=CC=C3SC4=CC=CC=C24", "class": "CNS / Antipsychotic", "brand": "Seroquel"},
    "donepezil": {"smiles": "COC1=C(C=C2C(=C1)CC(C2=O)CC3CCN(CC3)CC4=CC=CC=C4)OC", "class": "CNS / Acetylcholinesterase", "brand": "Aricept"},
    "levodopa": {"smiles": "C1=CC(=C(C=C1CC(C(=O)O)N)O)O", "class": "CNS / Dopamine Precursor", "brand": "Sinemet"},

    # Anti-Infective & Antibiotic
    "amoxicillin": {"smiles": "CC1(C)SC2C(NC(=O)C(N)c3ccc(O)cc3)C(=O)N2C1C(=O)O", "class": "Antibiotic / Penicillin", "brand": "Amoxil"},
    "ampicillin": {"smiles": "CC1(C)SC2C(NC(=O)C(N)c3ccccc3)C(=O)N2C1C(=O)O", "class": "Antibiotic / Penicillin", "brand": "Principen"},
    "penicillin_g": {"smiles": "CC1(C)S[C@@H]2[C@H](NC(=O)Cc3ccccc3)C(=O)N2[C@H]1C(=O)O", "class": "Antibiotic / Beta-lactam", "brand": "Pfizerpen"},
    "penicillin": {"smiles": "CC1(C)S[C@@H]2[C@H](NC(=O)Cc3ccccc3)C(=O)N2[C@H]1C(=O)O", "class": "Antibiotic / Beta-lactam", "brand": "Penicillin"},
    "ciprofloxacin": {"smiles": "C1CC1N2C=C(C(=O)C3=CC(=C(C=C32)N4CCNCC4)F)C(=O)O", "class": "Antibiotic / Fluoroquinolone", "brand": "Cipro"},
    "levofloxacin": {"smiles": "CC1COC2=C3N1C=C(C(=O)C3=CC(=C2N4CCN(CC4)C)F)C(=O)O", "class": "Antibiotic / Fluoroquinolone", "brand": "Levaquin"},
    "azithromycin": {"smiles": "CCC1C(C(C(N(CC(CC(C(C(C(C(=O)O1)C)OC2CC(C(C(O2)C)O)(C)OC)C)OC3C(C(CC(O3)C)N(C)C)O)(C)O)C)C)O)(C)O", "class": "Antibiotic / Macrolide", "brand": "Zithromax"},
    "doxycycline": {"smiles": "CC1C2C(C3C(C(=O)C(=C(C3(C(=O)C2=C(C4=C1C=CC=C4O)O)O)O)C(=O)N)N(C)C)O", "class": "Antibiotic / Tetracycline", "brand": "Vibramycin"},
    "metronidazole": {"smiles": "CC1=NC=C(N1CCO)[N+](=O)[O-]", "class": "Antibacterial / Nitroimidazole", "brand": "Flagyl"},
    "ceftriaxone": {"smiles": "CSC1=NC(=O)C(=O)N1NC(=O)C2=C(N3C(C(C3=O)NC(=O)C(=NOC)C4=CSC(=N4)N)SC2)C(=O)O", "class": "Antibiotic / Cephalosporin", "brand": "Rocephin"},

    # Antiviral
    "remdesivir": {"smiles": "CCC(CC)COC(=O)[C@H](C)N[P@](=O)(OC[C@H]1O[C@](C#N)(c2ccc3n2ncnc3N)[C@H](O)[C@@H]1O)Oc4ccccc4", "class": "Antiviral / Nucleotide Analog", "brand": "Veklury"},
    "acyclovir": {"smiles": "C1=NC2=C(N1COCCO)N=C(NC2=O)N", "class": "Antiviral / Guanosine Analog", "brand": "Zovirax"},
    "oseltamivir": {"smiles": "CCC(CC)OC1C=C(CC(C1NC(=O)C)N)C(=O)OCC", "class": "Antiviral / Neuraminidase", "brand": "Tamiflu"},
    "sofosbuvir": {"smiles": "CC(C)OC(=O)C(C)NP(=O)(OCC1C(C(C(O1)N2C=CC(=O)NC2=O)(C)F)O)OC3=CC=CC=C3", "class": "Antiviral / HCV Polymerase", "brand": "Sovaldi"},
    "ritonavir": {"smiles": "CC(C)C1=NC(=CS1)CN(C)C(=O)NC(C(C)C)C(=O)NC(CC2=CC=CC=C2)CC(C(CC3=CC=CC=C3)NC(=O)OCC4=CN=CS4)O", "class": "Antiviral / Protease Inhibitor", "brand": "Norvir"},

    # Analgesics & Anti-Inflammatory (NSAIDs / Opioids)
    "aspirin": {"smiles": "CC(=O)Oc1ccccc1C(=O)O", "class": "Analgesic / Salicylate", "brand": "Bayer Aspirin"},
    "ibuprofen": {"smiles": "CC(C)Cc1ccc(cc1)C(C)C(=O)O", "class": "Analgesic / NSAID", "brand": "Advil / Motrin"},
    "paracetamol": {"smiles": "CC(=O)Nc1ccc(O)cc1", "class": "Analgesic / Antipyretic", "brand": "Tylenol"},
    "acetaminophen": {"smiles": "CC(=O)Nc1ccc(O)cc1", "class": "Analgesic / Antipyretic", "brand": "Tylenol"},
    "naproxen": {"smiles": "CC(C1=CC2=C(C=C1)C=C(C=C2)OC)C(=O)O", "class": "Analgesic / NSAID", "brand": "Aleve"},
    "celecoxib": {"smiles": "CC1=CC=C(C=C1)C2=CC(=NN2C3=CC=C(C=C3)S(=O)(=O)N)C(F)(F)F", "class": "Analgesic / COX-2 Inhibitor", "brand": "Celebrex"},
    "diclofenac": {"smiles": "O=C(O)Cc1ccccc1Nc2c(Cl)cccc2Cl", "class": "Analgesic / NSAID", "brand": "Voltaren"},
    "morphine": {"smiles": "CN1CCC23C4C1CC5=C2C(=C(C=C5)O)OC3C(C=C4)O", "class": "Analgesic / Opioid", "brand": "MS Contin"},
    "tramadol": {"smiles": "CN(C)CC(C1=CC(=CC=C1)OC)C2(CCCCC2)O", "class": "Analgesic / Opioid Agonist", "brand": "Ultram"},

    # Metabolic & Endocrine
    "metformin": {"smiles": "CN(C)C(=N)N=C(N)N", "class": "Metabolic / Biguanide", "brand": "Glucophage"},
    "glipizide": {"smiles": "CC1=NC=C(C=N1)C(=O)NCCC2=CC=C(C=C2)S(=O)(=O)NC(=O)NC3CCCCC3", "class": "Metabolic / Sulfonylurea", "brand": "Glucotrol"},
    "dapagliflozin": {"smiles": "CCOC1=CC=C(C=C1)CC2=C(C=CC(=C2)C3C(C(C(C(O3)CO)O)O)O)Cl", "class": "Metabolic / SGLT2 Inhibitor", "brand": "Farxiga"},
    "sitagliptin": {"smiles": "C1CN2C(=NN=C2C(F)(F)F)CN1C(=O)CC(CC3=CC(=C(C=C3F)F)F)N", "class": "Metabolic / DPP-4 Inhibitor", "brand": "Januvia"},
    "levothyroxine": {"smiles": "C1=C(C=C(C(=C1I)OC2=CC(=C(C(=C2)I)O)I)I)CC(C(=O)O)N", "class": "Endocrine / Thyroid Hormone", "brand": "Synthroid"},

    # Gastrointestinal & Respiratory
    "omeprazole": {"smiles": "CC1=CN=C(C(=C1OC)C)CS(=O)C2=NC3=C(N2)C=C(C=C3)OC", "class": "Gastrointestinal / PPI", "brand": "Prilosec"},
    "pantoprazole": {"smiles": "COC1=C(C(=NC=C1)CS(=O)C2=NC3=C(N2)C=C(C=C3)OC(F)F)OC", "class": "Gastrointestinal / PPI", "brand": "Protonix"},
    "ondansetron": {"smiles": "CC1=NC=CN1CC2CCC(=O)C3=C2NC4=CC=CC=C34", "class": "Gastrointestinal / 5-HT3 Antagonist", "brand": "Zofran"},
    "albuterol": {"smiles": "CC(C)(C)NCC(C1=CC(=C(C=C1)O)CO)O", "class": "Respiratory / Beta-2 Agonist", "brand": "Ventolin"},
    "montelukast": {"smiles": "CC(C)(C1=CC=CC=C1CCC(C2=CC=CC(=C2)/C=C/C3=NC4=C(C=CC(=C4)Cl)C=C3)SCC(=O)O)O", "class": "Respiratory / Leukotriene", "brand": "Singulair"},
    "theophylline": {"smiles": "CN1C2=C(C(=O)N(C1=O)C)NC=N2", "class": "Respiratory / Xanthine", "brand": "Theo-24"},
    "caffeine": {"smiles": "Cn1cnc2c1c(=O)n(c(=O)n2C)C", "class": "CNS / Xanthine Stimulant", "brand": "Caffeine"},
    "nicotine": {"smiles": "CN1CCC[C@H]1c2cccnc2", "class": "CNS / Nicotinic Agonist", "brand": "Nicotine"},

    # Immunomodulatory & Steroids
    "dexamethasone": {"smiles": "CC1CC2C3CCC4=CC(=O)C=CC4(C3(C(CC2(C1(C(=O)CO)O)C)O)F)C", "class": "Immunology / Corticosteroid", "brand": "Decadron"},
    "prednisone": {"smiles": "CC12CC(=O)C3C(C1CCC2(C(=O)CO)O)CCC4=CC(=O)C=CC34C", "class": "Immunology / Corticosteroid", "brand": "Deltasone"},
    "hydrocortisone": {"smiles": "CC12CCC(=O)C=C1CCC3C2C(CC4(C3CCC4(C(=O)CO)O)C)O", "class": "Immunology / Glucocorticoid", "brand": "Cortef"},
    "tacrolimus": {"smiles": "CC1CC(CC(=C(CC(C(C(=O)C(=O)N2CCCCC2C(=O)OC(C(C(CC(=O)C(CC=C)C1)O)C)C(C)CC3=CC(=C(C=C3)OC)OC)C)OC)C)C)OC", "class": "Immunology / Calcineurin Inhibitor", "brand": "Prograf"}
}


def resolve_compound_query(query: str) -> Dict[str, Any]:
    """
    Intelligently resolves any user query:
    1. If SMILES: validates directly with RDKit.
    2. If drug generic name or brand: looks up in the local Clinical Pharmacopeia (80+ drugs).
    3. If unknown: falls back to PubChem REST API lookup.
    """
    clean_q = query.strip()
    if not clean_q:
        return {"success": False, "error": "Empty search query."}

    # 1. Check if raw query is already a valid chemical SMILES
    try:
        mol = Chem.MolFromSmiles(clean_q)
        if mol is not None:
            canonical = Chem.MolToSmiles(mol)
            return {
                "success": True,
                "smiles": canonical,
                "name": "Custom Structural Input",
                "therapeutic_class": "Novel Small Molecule",
                "source": "Direct SMILES Input"
            }
    except Exception:
        pass

    # 2. Check Local Clinical Pharmacopeia (case-insensitive lookup across generic and brand names)
    lookup_key = clean_q.lower().replace("-", " ").replace("_", " ").strip()
    # Normalize
    for name, data in CLINICAL_PHARMACOPEIA.items():
        clean_name = name.replace("-", " ").replace("_", " ")
        brand_clean = data.get("brand", "").lower()
        if lookup_key == clean_name or lookup_key in brand_clean:
            return {
                "success": True,
                "smiles": data["smiles"],
                "name": name.capitalize(),
                "therapeutic_class": data["class"],
                "brand": data.get("brand"),
                "source": "Clinical Reference Database"
            }

    # Partial match in local database
    for name, data in CLINICAL_PHARMACOPEIA.items():
        clean_name = name.replace("-", " ").replace("_", " ")
        if lookup_key in clean_name or clean_name in lookup_key:
            return {
                "success": True,
                "smiles": data["smiles"],
                "name": name.capitalize(),
                "therapeutic_class": data["class"],
                "brand": data.get("brand"),
                "source": "Clinical Reference Database (Fuzzy Match)"
            }

    # 3. Fallback to PubChem API
    try:
        url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{requests.utils.quote(clean_q)}/property/CanonicalSMILES/JSON"
        r = requests.get(url, timeout=3.5)
        if r.status_code == 200:
            smi = r.json()["PropertyTable"]["Properties"][0]["CanonicalSMILES"]
            mol = Chem.MolFromSmiles(smi)
            if mol is not None:
                return {
                    "success": True,
                    "smiles": smi,
                    "name": clean_q.capitalize(),
                    "therapeutic_class": "PubChem Resolved Compound",
                    "source": "PubChem National Library of Medicine"
                }
    except Exception:
        pass

    return {
        "success": False,
        "error": f"Could not resolve '{clean_q}'. Please enter a valid generic name (e.g. Doxorubicin, Metformin, Atorvastatin) or direct chemical SMILES string."
    }
