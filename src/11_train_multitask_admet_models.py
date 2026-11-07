import os
import joblib
import numpy as np
import pandas as pd

from rdkit import Chem
from rdkit.Chem import Descriptors, rdFingerprintGenerator
from rdkit.DataStructs import ConvertToNumpyArray

from sklearn.model_selection import train_test_split
from sklearn.ensemble import ExtraTreesRegressor, ExtraTreesClassifier
from sklearn.metrics import (
    mean_absolute_error, root_mean_squared_error, r2_score,
    accuracy_score, roc_auc_score, f1_score, classification_report
)

print("=" * 75)
print("MOLECULAR PROPERTY PREDICTION - MULTI-ENDPOINT ADMET TRAINING")
print("Training Models for Lipophilicity (LogD) & Blood-Brain Barrier (BBBP)")
print("=" * 75)

fp_gen = rdFingerprintGenerator.GetMorganGenerator(radius=2, fpSize=2048)

def compute_features(smiles_list):
    valid_features = []
    valid_indices = []

    for idx, smi in enumerate(smiles_list):
        if not isinstance(smi, str):
            continue
        mol = Chem.MolFromSmiles(smi)
        if mol is None:
            continue

        desc = [
            Descriptors.MolWt(mol),
            Descriptors.MolLogP(mol),
            Descriptors.TPSA(mol),
            Descriptors.NumHDonors(mol),
            Descriptors.NumHAcceptors(mol),
            Descriptors.RingCount(mol),
            Descriptors.NumAromaticRings(mol),
            Descriptors.NumAliphaticRings(mol),
            Descriptors.NumRotatableBonds(mol),
            Descriptors.FractionCSP3(mol),
            Descriptors.HeavyAtomCount(mol),
            Descriptors.NumHeteroatoms(mol),
            Chem.GetFormalCharge(mol),
            sum(1 for a in mol.GetAtoms() if a.GetSymbol() == "N"),
            sum(1 for a in mol.GetAtoms() if a.GetSymbol() == "O"),
            sum(1 for a in mol.GetAtoms() if a.GetSymbol() == "S"),
            sum(1 for a in mol.GetAtoms() if a.GetSymbol() == "F"),
            sum(1 for a in mol.GetAtoms() if a.GetSymbol() == "Cl"),
            sum(1 for a in mol.GetAtoms() if a.GetSymbol() == "Br"),
            sum(1 for a in mol.GetAtoms() if a.GetSymbol() == "I")
        ]

        fp = fp_gen.GetFingerprint(mol)
        fp_arr = np.zeros((2048,), dtype=np.int8)
        ConvertToNumpyArray(fp, fp_arr)

        combined = np.concatenate([np.array(desc), fp_arr])
        valid_features.append(combined)
        valid_indices.append(idx)

    return np.array(valid_features), valid_indices


# =========================================================
# 1. Train Lipophilicity (LogD) Model
# =========================================================
print("\n" + "-" * 75)
print("1. TRAINING LIPOPHILICITY (LogD) REGRESSION MODEL")
print("-" * 75)

lipo_path = "data/lipophilicity_raw.csv"
df_lipo = pd.read_csv(lipo_path).dropna(subset=["smiles", "exp"])
print(f"Loaded {len(df_lipo)} compounds from {lipo_path}.")

X_lipo, valid_lipo_idx = compute_features(df_lipo["smiles"].values)
y_lipo = df_lipo["exp"].iloc[valid_lipo_idx].values

X_train_lipo, X_test_lipo, y_train_lipo, y_test_lipo = train_test_split(
    X_lipo, y_lipo, test_size=0.20, random_state=42
)

print(f"Training samples: {len(X_train_lipo)}, Test samples: {len(X_test_lipo)}")

lipo_model = ExtraTreesRegressor(
    n_estimators=150,
    max_features=0.85,
    max_depth=16,
    random_state=42,
    n_jobs=-1
)
lipo_model.fit(X_train_lipo, y_train_lipo)

y_pred_lipo = lipo_model.predict(X_test_lipo)
lipo_mae = mean_absolute_error(y_test_lipo, y_pred_lipo)
lipo_rmse = root_mean_squared_error(y_test_lipo, y_pred_lipo)
lipo_r2 = r2_score(y_test_lipo, y_pred_lipo)

print(f"Lipophilicity Test Metrics -> MAE: {lipo_mae:.4f} | RMSE: {lipo_rmse:.4f} | R²: {lipo_r2:.4f}")

os.makedirs("models", exist_ok=True)
os.makedirs("results", exist_ok=True)
joblib.dump(lipo_model, "models/lipophilicity_model.pkl")

df_lipo_metrics = pd.DataFrame([
    {"Property": "Lipophilicity (LogD)", "Task": "Regression", "MAE": lipo_mae, "RMSE": lipo_rmse, "R2": lipo_r2}
])
df_lipo_metrics.to_csv("results/lipophilicity_metrics.csv", index=False)


# =========================================================
# 2. Train Blood-Brain Barrier Penetration (BBBP) Model
# =========================================================
print("\n" + "-" * 75)
print("2. TRAINING BLOOD-BRAIN BARRIER PENETRATION (BBBP) MODEL")
print("-" * 75)

bbbp_path = "data/bbbp_raw.csv"
df_bbbp = pd.read_csv(bbbp_path).dropna(subset=["smiles", "p_np"])
print(f"Loaded {len(df_bbbp)} compounds from {bbbp_path}.")

X_bbbp, valid_bbbp_idx = compute_features(df_bbbp["smiles"].values)
y_bbbp = df_bbbp["p_np"].iloc[valid_bbbp_idx].astype(int).values

X_train_bbbp, X_test_bbbp, y_train_bbbp, y_test_bbbp = train_test_split(
    X_bbbp, y_bbbp, test_size=0.20, random_state=42, stratify=y_bbbp
)

print(f"Training samples: {len(X_train_bbbp)}, Test samples: {len(X_test_bbbp)}")

bbbp_model = ExtraTreesClassifier(
    n_estimators=150,
    max_features=0.85,
    max_depth=16,
    random_state=42,
    n_jobs=-1
)
bbbp_model.fit(X_train_bbbp, y_train_bbbp)

y_pred_bbbp = bbbp_model.predict(X_test_bbbp)
y_prob_bbbp = bbbp_model.predict_proba(X_test_bbbp)[:, 1]

bbbp_acc = accuracy_score(y_test_bbbp, y_pred_bbbp)
bbbp_auc = roc_auc_score(y_test_bbbp, y_prob_bbbp)
bbbp_f1 = f1_score(y_test_bbbp, y_pred_bbbp)

print(f"BBBP Test Metrics -> Accuracy: {bbbp_acc:.4f} | ROC-AUC: {bbbp_auc:.4f} | F1: {bbbp_f1:.4f}")

joblib.dump(bbbp_model, "models/bbbp_model.pkl")

df_bbbp_metrics = pd.DataFrame([
    {"Property": "Blood-Brain Barrier (BBBP)", "Task": "Classification", "Accuracy": bbbp_acc, "ROC_AUC": bbbp_auc, "F1": bbbp_f1}
])
df_bbbp_metrics.to_csv("results/bbbp_metrics.csv", index=False)

print("\n" + "=" * 75)
print("ALL MULTI-ENDPOINT MODELS SUCCESSFULLY TRAINED AND SAVED!")
print("Saved models: models/lipophilicity_model.pkl, models/bbbp_model.pkl")
print("=" * 75)
