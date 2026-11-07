import os
import joblib
import numpy as np
import pandas as pd

from rdkit import Chem
from rdkit.Chem import Descriptors, rdFingerprintGenerator
from rdkit.DataStructs import ConvertToNumpyArray

from sklearn.model_selection import train_test_split
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.metrics import accuracy_score, roc_auc_score, f1_score

print("=" * 75)
print("EXPANDED ADMET TRAINING: CLINICAL TOXICITY & P53 GENOTOXICITY")
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


# 1. Train ClinTox Model
print("\n" + "-" * 75)
print("1. TRAINING CLINTOX (CLINICAL TRIAL TOXICITY FAILURE) MODEL")
print("-" * 75)

clintox_path = "data/clintox_raw.csv"
if os.path.exists(clintox_path):
    df_clintox = pd.read_csv(clintox_path).dropna(subset=["smiles", "CT_TOX"])
    print(f"Loaded {len(df_clintox)} compounds from {clintox_path}.")
    X_clintox, valid_clintox_idx = compute_features(df_clintox["smiles"].values)
    y_clintox = df_clintox["CT_TOX"].iloc[valid_clintox_idx].astype(int).values

    X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(
        X_clintox, y_clintox, test_size=0.20, random_state=42, stratify=y_clintox
    )

    clintox_model = ExtraTreesClassifier(
        n_estimators=150,
        max_features=0.85,
        max_depth=16,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    )
    clintox_model.fit(X_train_c, y_train_c)

    y_pred_c = clintox_model.predict(X_test_c)
    y_prob_c = clintox_model.predict_proba(X_test_c)[:, 1]

    c_acc = accuracy_score(y_test_c, y_pred_c)
    c_auc = roc_auc_score(y_test_c, y_prob_c)
    c_f1 = f1_score(y_test_c, y_pred_c, zero_division=0)

    print(f"ClinTox Metrics -> Accuracy: {c_acc:.4f} | ROC-AUC: {c_auc:.4f} | F1: {c_f1:.4f}")
    joblib.dump(clintox_model, "models/clintox_model.pkl")

    pd.DataFrame([{
        "Property": "Clinical Toxicity (ClinTox)",
        "Task": "Classification",
        "Accuracy": c_acc,
        "ROC_AUC": c_auc,
        "F1": c_f1
    }]).to_csv("results/clintox_metrics.csv", index=False)


# 2. Train Tox21 p53 Genotoxicity Model
print("\n" + "-" * 75)
print("2. TRAINING TOX21 p53 GENOTOXICITY/DNA-DAMAGE MODEL")
print("-" * 75)

tox21_path = "data/tox21_raw.csv"
if os.path.exists(tox21_path):
    df_tox21 = pd.read_csv(tox21_path).dropna(subset=["smiles", "SR-p53"])
    print(f"Loaded {len(df_tox21)} compounds from {tox21_path}.")
    X_p53, valid_p53_idx = compute_features(df_tox21["smiles"].values)
    y_p53 = df_tox21["SR-p53"].iloc[valid_p53_idx].astype(int).values

    X_train_p, X_test_p, y_train_p, y_test_p = train_test_split(
        X_p53, y_p53, test_size=0.20, random_state=42, stratify=y_p53
    )

    p53_model = ExtraTreesClassifier(
        n_estimators=150,
        max_features=0.85,
        max_depth=16,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    )
    p53_model.fit(X_train_p, y_train_p)

    y_pred_p = p53_model.predict(X_test_p)
    y_prob_p = p53_model.predict_proba(X_test_p)[:, 1]

    p_acc = accuracy_score(y_test_p, y_pred_p)
    p_auc = roc_auc_score(y_test_p, y_prob_p)
    p_f1 = f1_score(y_test_p, y_pred_p, zero_division=0)

    print(f"p53 Tox Metrics -> Accuracy: {p_acc:.4f} | ROC-AUC: {p_auc:.4f} | F1: {p_f1:.4f}")
    joblib.dump(p53_model, "models/p53_toxicity_model.pkl")

    pd.DataFrame([{
        "Property": "p53 Genotoxicity (Tox21)",
        "Task": "Classification",
        "Accuracy": p_acc,
        "ROC_AUC": p_auc,
        "F1": p_f1
    }]).to_csv("results/p53_metrics.csv", index=False)

print("\n" + "=" * 75)
print("EXPANDED ADMET MODELS SUCCESSFULLY SAVED!")
print("=" * 75)
