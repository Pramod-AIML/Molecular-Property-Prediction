import pandas as pd
import numpy as np
import joblib

from rdkit import Chem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdFingerprintGenerator


print("=" * 75)
print("MOLECULAR PROPERTY PREDICTION - FINAL LIVE PREDICTION")
print("=" * 75)


# =========================================================
# 1. Load final trained model
# =========================================================

model_path = "models/final_combined_solubility_model.pkl"

model = joblib.load(model_path)

print("\nFinal model loaded successfully.")
print("Model: Extra Trees Regressor")
print("Features: 2068")


# =========================================================
# 2. Molecular descriptor calculation
# =========================================================

def calculate_descriptors(molecule):

    descriptors = [
        Descriptors.MolWt(molecule),
        Descriptors.MolLogP(molecule),
        Descriptors.TPSA(molecule),
        Descriptors.NumHDonors(molecule),
        Descriptors.NumHAcceptors(molecule),
        Descriptors.RingCount(molecule),
        Descriptors.NumAromaticRings(molecule),
        Descriptors.NumAliphaticRings(molecule),
        Descriptors.NumRotatableBonds(molecule),
        Descriptors.FractionCSP3(molecule),
        Descriptors.HeavyAtomCount(molecule),
        Descriptors.NumHeteroatoms(molecule),
        Chem.GetFormalCharge(molecule),
        sum(
            1 for atom in molecule.GetAtoms()
            if atom.GetSymbol() == "N"
        ),
        sum(
            1 for atom in molecule.GetAtoms()
            if atom.GetSymbol() == "O"
        ),
        sum(
            1 for atom in molecule.GetAtoms()
            if atom.GetSymbol() == "S"
        ),
        sum(
            1 for atom in molecule.GetAtoms()
            if atom.GetSymbol() == "F"
        ),
        sum(
            1 for atom in molecule.GetAtoms()
            if atom.GetSymbol() == "Cl"
        ),
        sum(
            1 for atom in molecule.GetAtoms()
            if atom.GetSymbol() == "Br"
        ),
        sum(
            1 for atom in molecule.GetAtoms()
            if atom.GetSymbol() == "I"
        )
    ]

    return descriptors


# =========================================================
# 3. Morgan fingerprint generator
# =========================================================

fingerprint_generator = (
    rdFingerprintGenerator.GetMorganGenerator(
        radius=2,
        fpSize=2048
    )
)


# =========================================================
# 4. Prediction function
# =========================================================

def predict_solubility(smiles):

    # Convert SMILES to molecule
    molecule = Chem.MolFromSmiles(smiles)

    if molecule is None:
        return None, "Invalid SMILES"


    # ---------------------------------------------
    # Calculate 20 molecular descriptors
    # ---------------------------------------------

    descriptors = calculate_descriptors(
        molecule
    )


    # ---------------------------------------------
    # Generate 2048-bit Morgan fingerprint
    # ---------------------------------------------

    fingerprint = fingerprint_generator.GetFingerprint(
        molecule
    )

    fingerprint_array = np.zeros(
        (2048,),
        dtype=np.int8
    )

    from rdkit.DataStructs import ConvertToNumpyArray

    ConvertToNumpyArray(
        fingerprint,
        fingerprint_array
    )


    # ---------------------------------------------
    # Combine descriptors + fingerprint
    # ---------------------------------------------

    combined_features = np.concatenate([
        np.array(descriptors),
        fingerprint_array
    ])


    # Reshape for model
    X = combined_features.reshape(
        1,
        -1
    )


    # ---------------------------------------------
    # Prediction
    # ---------------------------------------------

    prediction = model.predict(X)[0]


    return prediction, None


# =========================================================
# 5. Interactive prediction
# =========================================================

while True:

    print("\n" + "-" * 75)

    smiles = input(
        "Enter SMILES (or type 'exit' to quit): "
    ).strip()


    # Exit option
    if smiles.lower() == "exit":
        print("\nPrediction system closed.")
        break


    # Empty input
    if not smiles:
        print("Please enter a SMILES string.")
        continue


    # Predict
    prediction, error = predict_solubility(
        smiles
    )


    # Invalid molecule
    if error is not None:

        print("\nERROR:", error)
        print("Please enter a valid SMILES string.")
        continue


    # Display prediction
    print("\n" + "=" * 50)
    print("PREDICTION RESULT")
    print("=" * 50)

    print(f"SMILES                : {smiles}")
    print(
        f"Predicted LogS        : "
        f"{prediction:.4f}"
    )

    print(
        "Predicted Log Solubility "
        "(mol/L): "
        f"{prediction:.4f}"
    )

    print("=" * 50)