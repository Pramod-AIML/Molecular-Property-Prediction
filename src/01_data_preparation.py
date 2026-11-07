import pandas as pd
import numpy as np
from rdkit import Chem
from rdkit.Chem import Descriptors, Lipinski, Crippen, rdMolDescriptors

# ---------------------------------------------------------
# 1. Load dataset
# ---------------------------------------------------------

INPUT_FILE = "data/delaney-processed.csv"
OUTPUT_FILE = "data/molecular_features.csv"

print("=" * 70)
print("MOLECULAR PROPERTY PREDICTION - DATA PREPARATION")
print("=" * 70)

df = pd.read_csv(INPUT_FILE)

print(f"\nOriginal dataset size: {df.shape}")
print(f"Number of molecules: {len(df)}")


# ---------------------------------------------------------
# 2. Select required columns
# ---------------------------------------------------------

smiles_column = "smiles"
target_column = "measured log solubility in mols per litre"

data = df[[smiles_column, target_column]].copy()

print("\nSelected columns:")
print(data.columns.tolist())


# ---------------------------------------------------------
# 3. Convert SMILES to RDKit molecules
# ---------------------------------------------------------

def smiles_to_molecule(smiles):
    try:
        return Chem.MolFromSmiles(smiles)
    except Exception:
        return None


data["Molecule"] = data[smiles_column].apply(smiles_to_molecule)

invalid_count = data["Molecule"].isna().sum()

print(f"\nInvalid molecules: {invalid_count}")


# Remove invalid molecules
data = data.dropna(subset=["Molecule"]).reset_index(drop=True)

print(f"Valid molecules remaining: {len(data)}")


# ---------------------------------------------------------
# 4. Calculate molecular descriptors
# ---------------------------------------------------------

def calculate_descriptors(molecule):

    return pd.Series({
        "Molecular_Weight": Descriptors.MolWt(molecule),
        "LogP": Crippen.MolLogP(molecule),
        "TPSA": rdMolDescriptors.CalcTPSA(molecule),

        "HBD": Lipinski.NumHDonors(molecule),
        "HBA": Lipinski.NumHAcceptors(molecule),

        "Ring_Count": Lipinski.RingCount(molecule),
        "Aromatic_Ring_Count": Lipinski.NumAromaticRings(molecule),
        "Aliphatic_Ring_Count": Lipinski.NumAliphaticRings(molecule),

        "Rotatable_Bonds": Lipinski.NumRotatableBonds(molecule),

        "Fraction_CSP3": rdMolDescriptors.CalcFractionCSP3(molecule),

        "Heavy_Atom_Count": Lipinski.HeavyAtomCount(molecule),

        "Heteroatom_Count": Lipinski.NumHeteroatoms(molecule),

        "Formal_Charge": Chem.GetFormalCharge(molecule),

        "N_Atoms": sum(
            1 for atom in molecule.GetAtoms()
            if atom.GetSymbol() == "N"
        ),

        "O_Atoms": sum(
            1 for atom in molecule.GetAtoms()
            if atom.GetSymbol() == "O"
        ),

        "S_Atoms": sum(
            1 for atom in molecule.GetAtoms()
            if atom.GetSymbol() == "S"
        ),

        "F_Atoms": sum(
            1 for atom in molecule.GetAtoms()
            if atom.GetSymbol() == "F"
        ),

        "Cl_Atoms": sum(
            1 for atom in molecule.GetAtoms()
            if atom.GetSymbol() == "Cl"
        ),

        "Br_Atoms": sum(
            1 for atom in molecule.GetAtoms()
            if atom.GetSymbol() == "Br"
        ),

        "I_Atoms": sum(
            1 for atom in molecule.GetAtoms()
            if atom.GetSymbol() == "I"
        )
    })

print("\nCalculating molecular descriptors...")

descriptor_data = data["Molecule"].apply(calculate_descriptors)

# Combine descriptors with original information
result = pd.concat(
    [
        data[[smiles_column, target_column]],
        descriptor_data
    ],
    axis=1
)


# ---------------------------------------------------------
# 5. Handle missing values
# ---------------------------------------------------------

result = result.replace([np.inf, -np.inf], np.nan)
result = result.dropna().reset_index(drop=True)


# ---------------------------------------------------------
# 6. Save processed dataset
# ---------------------------------------------------------

result.to_csv(OUTPUT_FILE, index=False)


# ---------------------------------------------------------
# 7. Display summary
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("DATA PREPARATION COMPLETED")
print("=" * 70)

print(f"\nProcessed dataset shape: {result.shape}")

print("\nGenerated molecular descriptors:")
for column in descriptor_data.columns:
    print(f"  - {column}")

print("\nFirst 5 processed molecules:")
print(result.head())

print("\nDataset statistics:")
print(result.describe())

print(f"\nProcessed dataset saved to:")
print(OUTPUT_FILE)

print("\n" + "=" * 70)