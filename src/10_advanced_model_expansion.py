import os
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

from sklearn.linear_model import LinearRegression, Ridge
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.neural_network import MLPRegressor
from sklearn.ensemble import (
    RandomForestRegressor,
    ExtraTreesRegressor,
    GradientBoostingRegressor,
    HistGradientBoostingRegressor,
    VotingRegressor,
    StackingRegressor
)
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score

print("=" * 75)
print("MOLECULAR PROPERTY PREDICTION - EXPANDED MODEL BENCHMARKING")
print("Evaluating Multi-Paradigm Machine Learning & Ensembles")
print("=" * 75)

# ---------------------------------------------------------
# 1. Load Data
# ---------------------------------------------------------
descriptor_file = "data/molecular_features.csv"
fingerprint_file = "data/morgan_fingerprints.csv"

df_desc = pd.read_csv(descriptor_file)
df_fp = pd.read_csv(fingerprint_file)
target_col = "measured log solubility in mols per litre"

descriptor_columns = [
    "Molecular_Weight", "LogP", "TPSA", "HBD", "HBA",
    "Ring_Count", "Aromatic_Ring_Count", "Aliphatic_Ring_Count",
    "Rotatable_Bonds", "Fraction_CSP3", "Heavy_Atom_Count",
    "Heteroatom_Count", "Formal_Charge", "N_Atoms", "O_Atoms",
    "S_Atoms", "F_Atoms", "Cl_Atoms", "Br_Atoms", "I_Atoms"
]

fingerprint_columns = list(df_fp.columns[:2048])

X_desc = df_desc[descriptor_columns].values
X_fp = df_fp[fingerprint_columns].values
X_combined = np.hstack([X_desc, X_fp])
y = df_desc[target_col].values

print(f"\nTotal molecules: {len(y)}")
print(f"Descriptor features: {X_desc.shape[1]}")
print(f"Fingerprint features: {X_fp.shape[1]}")
print(f"Combined features: {X_combined.shape[1]}")

# ---------------------------------------------------------
# 2. Train/Test Split
# ---------------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X_combined, y, test_size=0.20, random_state=42
)

print(f"Train samples: {len(X_train)}, Test samples: {len(X_test)}")

# ---------------------------------------------------------
# 3. Define Models across ML Paradigms
# ---------------------------------------------------------
# Base tree models
rf = RandomForestRegressor(n_estimators=200, random_state=42, n_jobs=-1)
et = ExtraTreesRegressor(n_estimators=300, max_features=0.9, max_depth=15, random_state=42, n_jobs=-1)
hgb = HistGradientBoostingRegressor(max_iter=200, random_state=42)

models = {
    "Linear Regression": Pipeline([
        ("scaler", StandardScaler()),
        ("model", LinearRegression())
    ]),
    "Ridge Regression": Pipeline([
        ("scaler", StandardScaler()),
        ("model", Ridge(alpha=1.0))
    ]),
    "K-Nearest Neighbors": Pipeline([
        ("scaler", StandardScaler()),
        ("model", KNeighborsRegressor(n_neighbors=5, weights="distance"))
    ]),
    "Support Vector Regressor (SVR)": Pipeline([
        ("scaler", StandardScaler()),
        ("model", SVR(C=10.0, epsilon=0.1))
    ]),
    "Neural Network (MLP)": Pipeline([
        ("scaler", StandardScaler()),
        ("model", MLPRegressor(hidden_layer_sizes=(128, 64), max_iter=400, random_state=42, early_stopping=True))
    ]),
    "Random Forest": rf,
    "Hist Gradient Boosting": hgb,
    "Extra Trees (Optimized)": et,
    "Voting Ensemble (ET + HGB + RF)": VotingRegressor(
        estimators=[("et", et), ("hgb", hgb), ("rf", rf)],
        weights=[0.5, 0.3, 0.2]
    ),
    "Stacking Regressor": StackingRegressor(
        estimators=[("et", et), ("hgb", hgb), ("rf", rf)],
        final_estimator=Ridge(alpha=1.0),
        cv=5,
        n_jobs=-1
    )
}

# ---------------------------------------------------------
# 4. Train & Evaluate All Models
# ---------------------------------------------------------
results = []

print("\n" + "-" * 75)
print(f"{'Model Architecture':<32} | {'MAE':<8} | {'RMSE':<8} | {'Test R²':<8}")
print("-" * 75)

for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    rmse = root_mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    results.append({
        "Model": name,
        "MAE": mae,
        "RMSE": rmse,
        "R2": r2
    })

    print(f"{name:<32} | {mae:.4f}   | {rmse:.4f}   | {r2:.4f}")

df_results = pd.DataFrame(results).sort_values("R2", ascending=False).reset_index(drop=True)

# ---------------------------------------------------------
# 5. Save Results & Visual Chart
# ---------------------------------------------------------
os.makedirs("results", exist_ok=True)
csv_out = "results/expanded_model_comparison.csv"
df_results.to_csv(csv_out, index=False)
print(f"\nExpanded model comparison saved to: {csv_out}")

# Plot comparison
plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
fig, ax1 = plt.subplots(figsize=(12, 6))

x = np.arange(len(df_results))
width = 0.38

bars1 = ax1.bar(x - width/2, df_results["R2"], width, label="Test R²", color="#1f77b4", alpha=0.85)
ax1.set_ylabel("R² Score (Higher is Better)", color="#1f77b4", fontsize=12, fontweight="bold")
ax1.set_ylim(0, 1.0)
ax1.set_xticks(x)
ax1.set_xticklabels(df_results["Model"], rotation=30, ha="right", fontsize=10)

ax2 = ax1.twinx()
bars2 = ax2.bar(x + width/2, df_results["RMSE"], width, label="Test RMSE", color="#d62728", alpha=0.85)
ax2.set_ylabel("RMSE (Lower is Better)", color="#d62728", fontsize=12, fontweight="bold")
ax2.set_ylim(0, max(df_results["RMSE"]) * 1.25)

plt.title("Comparative Performance Across 10 Machine Learning Architectures", fontsize=14, fontweight="bold", pad=15)
fig.tight_layout()

chart_out = "results/expanded_model_comparison.png"
plt.savefig(chart_out, dpi=300)
plt.close()
print(f"Comparison plot saved to: {chart_out}")

print("\n" + "=" * 75)
print("TOP PERFORMING ARCHITECTURES:")
for i, row in df_results.head(3).iterrows():
    print(f"Rank {i+1}: {row['Model']} (R²: {row['R2']:.4f}, RMSE: {row['RMSE']:.4f}, MAE: {row['MAE']:.4f})")
print("=" * 75)
