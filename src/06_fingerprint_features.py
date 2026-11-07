import pandas as pd
import numpy as np

from rdkit import Chem
from rdkit.Chem import rdFingerprintGenerator


# =========================================================
# MOLECULAR FINGERPRINT GENERATION
# =========================================================

print("=" * 75)
print("MOLECULAR PROPERTY PREDICTION - FINGERPRINT GENERATION")
print("=" * 75)


# =========================================================
# 1. Load original dataset
# =========================================================

INPUT_FILE = "data/delaney-processed.csv"

df = pd.read_csv(INPUT_FILE)

print(f"\nOriginal molecules: {len(df)}")


# =========================================================
# 2. Convert SMILES to molecules
# =========================================================

molecules = []

valid_indices = []

for index, smiles in enumerate(df["smiles"]):

    molecule = Chem.MolFromSmiles(smiles)

    if molecule is not None:

        molecules.append(molecule)
        valid_indices.append(index)


print(f"Valid molecules: {len(molecules)}")


# =========================================================
# 3. Generate Morgan fingerprints
# =========================================================


print("\nGenerating Morgan fingerprints...")

# Create Morgan fingerprint generator
generator = rdFingerprintGenerator.GetMorganGenerator(
    radius=2,
    fpSize=2048
)

fingerprints = []

for molecule in molecules:

    # Generate fingerprint for current molecule
    fingerprint = generator.GetFingerprint(molecule)

    # Convert fingerprint to NumPy array
    array = np.zeros(
        (2048,),
        dtype=np.int8
    )

    from rdkit.DataStructs import ConvertToNumpyArray

    ConvertToNumpyArray(
        fingerprint,
        array
    )

    fingerprints.append(array)


fingerprints = np.array(fingerprints)

print("\nFingerprint generation completed.")
print(f"Fingerprint matrix shape: {fingerprints.shape}")


# =========================================================
# 4. Create fingerprint column names
# =========================================================

fingerprint_columns = [
    f"FP_{i}"
    for i in range(2048)
]


fingerprint_df = pd.DataFrame(
    fingerprints,
    columns=fingerprint_columns
)


# =========================================================
# 5. Add target
# =========================================================

target = df.loc[
    valid_indices,
    "measured log solubility in mols per litre"
].reset_index(drop=True)


fingerprint_df[
    "Target_Solubility"
] = target


# =========================================================
# 6. Save fingerprint dataset
# =========================================================

OUTPUT_FILE = "data/morgan_fingerprints.csv"

fingerprint_df.to_csv(
    OUTPUT_FILE,
    index=False
)


# =========================================================
# 7. Display information
# =========================================================

print("\n" + "=" * 75)
print("FINGERPRINT DATASET CREATED")
print("=" * 75)

print(f"\nNumber of molecules : {len(fingerprint_df)}")
print(f"Fingerprint bits    : 2048")
print(f"Dataset shape       : {fingerprint_df.shape}")

print(f"\nSaved to:")
print(OUTPUT_FILE)

print("\n" + "=" * 75)