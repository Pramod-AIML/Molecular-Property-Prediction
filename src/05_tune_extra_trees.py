import os
import joblib
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# =========================================================
# EXTRA TREES HYPERPARAMETER OPTIMIZATION
# =========================================================

print("=" * 75)
print("EXTRA TREES HYPERPARAMETER OPTIMIZATION")
print("=" * 75)


# =========================================================
# 1. Load dataset
# =========================================================

df = pd.read_csv("data/molecular_features.csv")

print(f"\nDataset: {len(df)} molecules")


# =========================================================
# 2. Define features
# =========================================================

feature_columns = [
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

target_column = "measured log solubility in mols per litre"

X = df[feature_columns]
y = df[target_column]


# =========================================================
# 3. Train-test split
# =========================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

print(f"Training samples: {len(X_train)}")
print(f"Testing samples : {len(X_test)}")


# =========================================================
# 4. Define Extra Trees model
# =========================================================

extra_trees = ExtraTreesRegressor(
    random_state=42,
    n_jobs=-1
)


# =========================================================
# 5. Define hyperparameter search space
# =========================================================

parameter_grid = {

    "n_estimators": [
        200,
        300,
        500,
        700
    ],

    "max_depth": [
        None,
        10,
        15,
        20,
        25,
        30
    ],

    "min_samples_split": [
        2,
        4,
        6,
        8
    ],

    "min_samples_leaf": [
        1,
        2,
        3,
        4
    ],

    "max_features": [
        0.5,
        0.7,
        0.9,
        1.0,
        "sqrt"
    ],

    "bootstrap": [
        False,
        True
    ]
}


# =========================================================
# 6. Randomized hyperparameter search
# =========================================================

print("\n" + "-" * 75)
print("STARTING HYPERPARAMETER SEARCH")
print("-" * 75)

print("\nTesting 30 parameter combinations")
print("Using 5-fold cross-validation")
print("Please wait...")

search = RandomizedSearchCV(
    estimator=extra_trees,
    param_distributions=parameter_grid,
    n_iter=30,
    scoring="r2",
    cv=5,
    random_state=42,
    n_jobs=-1,
    verbose=1
)

search.fit(X_train, y_train)


# =========================================================
# 7. Display best parameters
# =========================================================

print("\n" + "=" * 75)
print("BEST HYPERPARAMETERS")
print("=" * 75)

print("\nBest parameters:")

for parameter, value in search.best_params_.items():
    print(f"  {parameter}: {value}")

print(
    f"\nBest 5-Fold CV R²: "
    f"{search.best_score_:.4f}"
)


# =========================================================
# 8. Evaluate optimized model
# =========================================================

best_model = search.best_estimator_

predictions = best_model.predict(X_test)

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


print("\n" + "=" * 75)
print("TUNED EXTRA TREES PERFORMANCE")
print("=" * 75)

print(f"\nMAE  : {mae:.4f}")
print(f"RMSE : {rmse:.4f}")
print(f"R²   : {r2:.4f}")


# =========================================================
# 9. Compare with previous Extra Trees
# =========================================================

previous_mae = 0.4871
previous_rmse = 0.7182
previous_r2 = 0.8909

print("\n" + "-" * 75)
print("COMPARISON WITH PREVIOUS EXTRA TREES")
print("-" * 75)

print(f"\nPrevious Extra Trees R² : {previous_r2:.4f}")
print(f"Tuned Extra Trees R²    : {r2:.4f}")

print(f"\nPrevious MAE            : {previous_mae:.4f}")
print(f"Tuned MAE               : {mae:.4f}")

print(f"\nPrevious RMSE           : {previous_rmse:.4f}")
print(f"Tuned RMSE              : {rmse:.4f}")


if r2 > previous_r2:
    print("\n✓ Hyperparameter tuning improved the model.")

elif r2 == previous_r2:
    print("\n✓ Performance remained the same.")

else:
    print("\n! Previous model performed better.")
    print("  We will keep the previous model.")


# =========================================================
# 10. Save results
# =========================================================

os.makedirs("results", exist_ok=True)
os.makedirs("models", exist_ok=True)


metrics = pd.DataFrame({
    "Metric": [
        "MAE",
        "RMSE",
        "R2",
        "CV_R2"
    ],
    "Value": [
        mae,
        rmse,
        r2,
        search.best_score_
    ]
})

metrics.to_csv(
    "results/tuned_extra_trees_metrics.csv",
    index=False
)


# Save best parameters
parameters = pd.DataFrame(
    list(search.best_params_.items()),
    columns=["Parameter", "Value"]
)

parameters.to_csv(
    "results/extra_trees_best_parameters.csv",
    index=False
)


# Save model
joblib.dump(
    best_model,
    "models/tuned_extra_trees_model.pkl"
)


# Save predictions
prediction_results = pd.DataFrame({
    "Actual": y_test.values,
    "Predicted": predictions
})

prediction_results.to_csv(
    "results/tuned_extra_trees_predictions.csv",
    index=False
)


# =========================================================
# 11. Final message
# =========================================================

print("\n" + "=" * 75)
print("EXTRA TREES OPTIMIZATION COMPLETED")
print("=" * 75)

print("\nSaved files:")

print("  ✓ models/tuned_extra_trees_model.pkl")
print("  ✓ results/tuned_extra_trees_metrics.csv")
print("  ✓ results/extra_trees_best_parameters.csv")
print("  ✓ results/tuned_extra_trees_predictions.csv")

print("\nOptimization finished successfully.")
print("=" * 75)