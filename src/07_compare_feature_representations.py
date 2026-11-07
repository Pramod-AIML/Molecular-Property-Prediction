import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


print("=" * 75)
print("MOLECULAR PROPERTY PREDICTION - FEATURE REPRESENTATION COMPARISON")
print("=" * 75)


# =========================================================
# 1. Load descriptor dataset
# =========================================================

descriptor_file = "data/molecular_features.csv"

df_desc = pd.read_csv(descriptor_file)

target_column = "measured log solubility in mols per litre"

print("\nDescriptor dataset:")
print(f"Shape: {df_desc.shape}")


# 20 molecular descriptor columns
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
# 2. Load Morgan fingerprint dataset
# =========================================================

fingerprint_file = "data/morgan_fingerprints.csv"

df_fp = pd.read_csv(fingerprint_file)

print("\nMorgan fingerprint dataset:")
print(f"Shape: {df_fp.shape}")


# The fingerprint file contains:
# 2048 fingerprint columns + 1 target column

# The Morgan fingerprint file contains 2048 fingerprint
# columns followed by the target column.
#
# Select only the first 2048 columns as fingerprint features.

fingerprint_columns = list(df_fp.columns[:2048])


print(f"Morgan fingerprint features: {len(fingerprint_columns)}")


# =========================================================
# 3. Prepare target
# =========================================================

y = df_desc[target_column].values


# =========================================================
# 4. Same train/test split for every experiment
# =========================================================

indices = np.arange(len(df_desc))

train_idx, test_idx = train_test_split(
    indices,
    test_size=0.20,
    random_state=42
)

print("\nData split:")
print(f"Training molecules: {len(train_idx)}")
print(f"Testing molecules : {len(test_idx)}")


# =========================================================
# 5. Prepare feature sets
# =========================================================

X_descriptor = df_desc[descriptor_columns].values

X_fingerprint = df_fp[fingerprint_columns].values

X_combined = np.hstack([
    X_descriptor,
    X_fingerprint
])


print("\nFeature representations:")
print(f"Descriptors : {X_descriptor.shape}")
print(f"Fingerprints: {X_fingerprint.shape}")
print(f"Combined    : {X_combined.shape}")


# =========================================================
# 6. Function for model evaluation
# =========================================================

def evaluate_model(name, X):

    print("\n" + "-" * 75)
    print(f"Training: {name}")
    print("-" * 75)

    X_train = X[train_idx]
    X_test = X[test_idx]

    y_train = y[train_idx]
    y_test = y[test_idx]

    model = ExtraTreesRegressor(
        n_estimators=300,
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    mae = mean_absolute_error(
        y_test,
        predictions
    )

    rmse = np.sqrt(
        mean_squared_error(
            y_test,
            predictions
        )
    )

    r2 = r2_score(
        y_test,
        predictions
    )

    print(f"MAE  : {mae:.4f}")
    print(f"RMSE : {rmse:.4f}")
    print(f"R²   : {r2:.4f}")

    return {
        "Feature_Representation": name,
        "Number_of_Features": X.shape[1],
        "MAE": mae,
        "RMSE": rmse,
        "R2": r2
    }


# =========================================================
# 7. Run three experiments
# =========================================================

results = []

results.append(
    evaluate_model(
        "20 Molecular Descriptors",
        X_descriptor
    )
)

results.append(
    evaluate_model(
        "Morgan Fingerprints",
        X_fingerprint
    )
)

results.append(
    evaluate_model(
        "Descriptors + Morgan Fingerprints",
        X_combined
    )
)


# =========================================================
# 8. Create comparison table
# =========================================================

results_df = pd.DataFrame(results)

results_df = results_df.sort_values(
    by="R2",
    ascending=False
)

print("\n")
print("=" * 75)
print("FEATURE REPRESENTATION COMPARISON")
print("=" * 75)

print(
    results_df.to_string(
        index=False,
        float_format=lambda x: f"{x:.4f}"
    )
)


# =========================================================
# 9. Save results
# =========================================================

results_df.to_csv(
    "results/feature_representation_comparison.csv",
    index=False
)


# =========================================================
# 10. Identify best representation
# =========================================================

best = results_df.iloc[0]

print("\n" + "=" * 75)
print("BEST FEATURE REPRESENTATION")
print("=" * 75)

print(f"Method   : {best['Feature_Representation']}")
print(f"Features : {int(best['Number_of_Features'])}")
print(f"MAE      : {best['MAE']:.4f}")
print(f"RMSE     : {best['RMSE']:.4f}")
print(f"R²       : {best['R2']:.4f}")

print("\nResults saved to:")
print("results/feature_representation_comparison.csv")

print("\n" + "=" * 75)
print("EXPERIMENT COMPLETED")
print("=" * 75)