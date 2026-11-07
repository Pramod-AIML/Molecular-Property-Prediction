import pandas as pd
import joblib

from rdkit import Chem
from rdkit.Chem import Descriptors, Lipinski, Crippen, rdMolDescriptors


# =========================================================
# MOLECULAR PROPERTY PREDICTION
# PREDICTION MODULE
# =========================================================

MODEL_FILE = "models/random_forest_solubility_model.pkl"


# =========================================================
# 1. Load trained model
# =========================================================

model = joblib.load(MODEL_FILE)

print("=" * 70)
print("MOLECULAR PROPERTY PREDICTION SYSTEM")
print("=" * 70)

print("\nTrained Random Forest model loaded successfully.")


# =========================================================
# 2. Get SMILES input
# =========================================================

smiles = input("\nEnter molecule SMILES: ").strip()


# =========================================================
# 3. Validate SMILES
# =========================================================

molecule = Chem.MolFromSmiles(smiles)

if molecule is None:
    print("\nERROR: Invalid SMILES string.")
    print("Please enter a valid molecular SMILES.")
    exit()


print("\nValid molecule detected.")


# =========================================================
# 4. Calculate molecular descriptors
# =========================================================

molecular_weight = Descriptors.MolWt(molecule)

logp = Crippen.MolLogP(molecule)

tpsa = rdMolDescriptors.CalcTPSA(molecule)

hbd = Lipinski.NumHDonors(molecule)

hba = Lipinski.NumHAcceptors(molecule)

ring_count = Lipinski.RingCount(molecule)

rotatable_bonds = Lipinski.NumRotatableBonds(molecule)

fraction_csp3 = rdMolDescriptors.CalcFractionCSP3(molecule)


# =========================================================
# 5. Create feature dataframe
# =========================================================

features = pd.DataFrame([{
    "Molecular_Weight": molecular_weight,
    "LogP": logp,
    "TPSA": tpsa,
    "HBD": hbd,
    "HBA": hba,
    "Ring_Count": ring_count,
    "Rotatable_Bonds": rotatable_bonds,
    "Fraction_CSP3": fraction_csp3
}])


# =========================================================
# 6. Predict molecular property
# =========================================================

prediction = model.predict(features)[0]


# =========================================================
# 7. Display results
# =========================================================

print("\n" + "=" * 70)
print("MOLECULAR ANALYSIS")
print("=" * 70)

print(f"\nSMILES: {smiles}")

print("\nMolecular Descriptors:")

print(f"  Molecular Weight : {molecular_weight:.3f}")

print(f"  LogP             : {logp:.3f}")

print(f"  TPSA             : {tpsa:.3f}")

print(f"  H-Bond Donors    : {hbd}")

print(f"  H-Bond Acceptors : {hba}")

print(f"  Ring Count       : {ring_count}")

print(f"  Rotatable Bonds  : {rotatable_bonds}")

print(f"  Fraction CSP3    : {fraction_csp3:.3f}")


print("\n" + "=" * 70)
print("PREDICTION RESULT")
print("=" * 70)

print(f"\nPredicted Log Solubility: {prediction:.4f}")

print("\nPrediction completed successfully.")

print("=" * 70)