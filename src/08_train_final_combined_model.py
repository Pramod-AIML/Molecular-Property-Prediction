import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


print("=" * 75)
print("FINAL MOLECULAR SOLUBILITY MODEL")
print("EXTRA TREES + DESCRIPTORS + MORGAN FINGERPRINTS")
print("=" * 75)


# =========================================================
# 1. Load datasets
# =========================================================

descriptor_file = "data/molecular_features.csv"
fingerprint_file = "data/morgan_fingerprints.csv"

df_desc = pd.read_csv(descriptor_file)
df_fp = pd.read_csv(fingerprint_file)

target_column = "measured log solubility in mols per litre"


print("\nDatasets loaded successfully.")

print(f"Descriptor dataset   : {df_desc.shape}")
print(f"Fingerprint dataset  : {df_fp.shape}")


# =========================================================
# 2. Select molecular descriptors
# =========================================================

descriptor_columns = [
    "Molecular_Weight",
    "LogP",
    "TPSA",
    "HBD",
    "HBA",
    "Ring_Count",
    "Aromatic_Ring_Count",
    "Aliphatic_Ring_Count",
    "Rotatable_Bonds",
    "Fraction_CSP3",
    "Heavy_Atom_Count",
    "Heteroatom_Count",
    "Formal_Charge",
    "N_Atoms",
    "O_Atoms",
    "S_Atoms",
    "F_Atoms",
    "Cl_Atoms",
    "Br_Atoms",
    "I_Atoms"
]


# =========================================================
# 3. Select ONLY 2048 fingerprint features
# =========================================================

fingerprint_columns = list(
    df_fp.columns[:2048]
)


print("\nFeature counts:")
print(f"Molecular descriptors : {len(descriptor_columns)}")
print(f"Morgan fingerprints   : {len(fingerprint_columns)}")
print(
    f"Total features        : "
    f"{len(descriptor_columns) + len(fingerprint_columns)}"
)


# =========================================================
# 4. Create combined feature matrix
# =========================================================

X_descriptor = df_desc[
    descriptor_columns
].values

X_fingerprint = df_fp[
    fingerprint_columns
].values

X = np.hstack([
    X_descriptor,
    X_fingerprint
])

y = df_desc[
    target_column
].values


print("\nCombined feature matrix:")
print(f"Shape: {X.shape}")


# =========================================================
# 5. Train/test split
# =========================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)


print("\nDataset split:")
print(f"Training samples : {len(X_train)}")
print(f"Testing samples  : {len(X_test)}")


# =========================================================
# 6. Create final Extra Trees model
# =========================================================

print("\nTraining final Extra Trees model...")

model = ExtraTreesRegressor(
    n_estimators=300,
    random_state=42,
    n_jobs=-1
)


# =========================================================
# 7. Train model
# =========================================================

model.fit(
    X_train,
    y_train
)

print("Training completed successfully.")


# =========================================================
# 8. Make predictions
# =========================================================

y_pred = model.predict(
    X_test
)


# =========================================================
# 9. Calculate evaluation metrics
# =========================================================

mae = mean_absolute_error(
    y_test,
    y_pred
)

rmse = np.sqrt(
    mean_squared_error(
        y_test,
        y_pred
    )
)

r2 = r2_score(
    y_test,
    y_pred
)


print("\n" + "=" * 75)
print("FINAL MODEL PERFORMANCE")
print("=" * 75)

print(f"MAE  : {mae:.4f}")
print(f"RMSE : {rmse:.4f}")
print(f"R²   : {r2:.4f}")


# =========================================================
# 10. Save metrics
# =========================================================

metrics = pd.DataFrame({
    "Metric": [
        "MAE",
        "RMSE",
        "R2"
    ],
    "Value": [
        mae,
        rmse,
        r2
    ]
})

metrics.to_csv(
    "results/final_combined_model_metrics.csv",
    index=False
)


# =========================================================
# 11. Save actual vs predicted values
# =========================================================

prediction_results = pd.DataFrame({
    "Actual_Solubility": y_test,
    "Predicted_Solubility": y_pred,
    "Error": y_test - y_pred
})

prediction_results.to_csv(
    "results/final_combined_predictions.csv",
    index=False
)


# =========================================================
# 12. Actual vs Predicted graph
# =========================================================

plt.figure(
    figsize=(8, 6)
)

plt.scatter(
    y_test,
    y_pred,
    alpha=0.7
)

minimum = min(
    y_test.min(),
    y_pred.min()
)

maximum = max(
    y_test.max(),
    y_pred.max()
)

plt.plot(
    [minimum, maximum],
    [minimum, maximum],
    linestyle="--"
)

plt.xlabel(
    "Actual Log Solubility"
)

plt.ylabel(
    "Predicted Log Solubility"
)

plt.title(
    "Final Model: Actual vs Predicted Solubility"
)

plt.tight_layout()

plt.savefig(
    "results/final_combined_actual_vs_predicted.png",
    dpi=300
)

plt.close()


# =========================================================
# 13. Residual plot
# =========================================================

residuals = y_test - y_pred

plt.figure(
    figsize=(8, 6)
)

plt.scatter(
    y_pred,
    residuals,
    alpha=0.7
)

plt.axhline(
    0,
    linestyle="--"
)

plt.xlabel(
    "Predicted Log Solubility"
)

plt.ylabel(
    "Residual"
)

plt.title(
    "Final Model Residual Analysis"
)

plt.tight_layout()

plt.savefig(
    "results/final_combined_residuals.png",
    dpi=300
)

plt.close()


# =========================================================
# 14. Feature importance
# =========================================================

feature_names = (
    descriptor_columns +
    fingerprint_columns
)

importance = model.feature_importances_

feature_importance = pd.DataFrame({
    "Feature": feature_names,
    "Importance": importance
})

feature_importance = feature_importance.sort_values(
    by="Importance",
    ascending=False
)

feature_importance.to_csv(
    "results/final_combined_feature_importance.csv",
    index=False
)


# =========================================================
# 15. Plot top 20 important features
# =========================================================

top_features = feature_importance.head(20)

plt.figure(
    figsize=(10, 7)
)

plt.barh(
    top_features["Feature"][::-1],
    top_features["Importance"][::-1]
)

plt.xlabel(
    "Feature Importance"
)

plt.ylabel(
    "Feature"
)

plt.title(
    "Top 20 Features - Final Combined Model"
)

plt.tight_layout()

plt.savefig(
    "results/final_combined_feature_importance.png",
    dpi=300
)

plt.close()


# =========================================================
# 16. Save final model
# =========================================================

joblib.dump(
    model,
    "models/final_combined_solubility_model.pkl"
)


# =========================================================
# 17. Save feature information
# =========================================================

with open(
    "models/final_combined_feature_columns.txt",
    "w"
) as file:

    for feature in feature_names:
        file.write(
            feature + "\n"
        )


# =========================================================
# 18. Final summary
# =========================================================

print("\nFiles saved:")
print("models/final_combined_solubility_model.pkl")
print("models/final_combined_feature_columns.txt")
print("results/final_combined_model_metrics.csv")
print("results/final_combined_predictions.csv")
print("results/final_combined_actual_vs_predicted.png")
print("results/final_combined_residuals.png")
print("results/final_combined_feature_importance.csv")
print("results/final_combined_feature_importance.png")

print("\n" + "=" * 75)
print("FINAL MODEL TRAINING COMPLETED")
print("=" * 75)