import os
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split, cross_val_score, RandomizedSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import (
    RandomForestRegressor,
    ExtraTreesRegressor,
    GradientBoostingRegressor,
    HistGradientBoostingRegressor
)

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)


# =========================================================
# MOLECULAR PROPERTY PREDICTION
# ADVANCED MODEL TRAINING AND COMPARISON
# =========================================================

print("=" * 75)
print("MOLECULAR PROPERTY PREDICTION - ADVANCED MODEL TRAINING")
print("=" * 75)


# =========================================================
# 1. Load dataset
# =========================================================

INPUT_FILE = "data/molecular_features.csv"

df = pd.read_csv(INPUT_FILE)

print(f"\nDataset loaded successfully.")
print(f"Number of molecules: {len(df)}")
print(f"Number of columns : {len(df.columns)}")


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

print("\nNumber of molecular features:", len(feature_columns))


# =========================================================
# 3. Train-test split
# =========================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

print("\n" + "-" * 75)
print("TRAIN-TEST SPLIT")
print("-" * 75)

print(f"Training samples: {len(X_train)}")
print(f"Testing samples : {len(X_test)}")


# =========================================================
# 4. Define models
# =========================================================

models = {

    "Linear Regression": Pipeline([
        ("scaler", StandardScaler()),
        ("model", LinearRegression())
    ]),

    "Ridge Regression": Pipeline([
        ("scaler", StandardScaler()),
        ("model", Ridge(alpha=10.0))
    ]),

    "Random Forest": RandomForestRegressor(
        n_estimators=300,
        random_state=42,
        n_jobs=-1
    ),

    "Extra Trees": ExtraTreesRegressor(
        n_estimators=300,
        random_state=42,
        n_jobs=-1
    ),

    "Gradient Boosting": GradientBoostingRegressor(
        n_estimators=200,
        learning_rate=0.05,
        max_depth=3,
        random_state=42
    ),

    "Hist Gradient Boosting": HistGradientBoostingRegressor(
        max_iter=200,
        learning_rate=0.05,
        max_leaf_nodes=15,
        random_state=42
    )
}


# =========================================================
# 5. Train and evaluate models
# =========================================================

results = []

trained_models = {}

print("\n" + "=" * 75)
print("MODEL COMPARISON")
print("=" * 75)

for name, model in models.items():

    print(f"\nTraining: {name}...")

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)

    rmse = np.sqrt(
        mean_squared_error(y_test, predictions)
    )

    r2 = r2_score(y_test, predictions)

    # 5-fold cross validation
    cv_scores = cross_val_score(
        model,
        X,
        y,
        cv=5,
        scoring="r2",
        n_jobs=-1
    )

    cv_mean = cv_scores.mean()
    cv_std = cv_scores.std()

    results.append({
        "Model": name,
        "MAE": mae,
        "RMSE": rmse,
        "R2": r2,
        "CV_R2_Mean": cv_mean,
        "CV_R2_STD": cv_std
    })

    trained_models[name] = model

    print(f"  MAE     : {mae:.4f}")
    print(f"  RMSE    : {rmse:.4f}")
    print(f"  R2      : {r2:.4f}")
    print(f"  CV R2   : {cv_mean:.4f} ± {cv_std:.4f}")


# =========================================================
# 6. Create comparison dataframe
# =========================================================

results_df = pd.DataFrame(results)

results_df = results_df.sort_values(
    by="R2",
    ascending=False
).reset_index(drop=True)


print("\n" + "=" * 75)
print("MODEL PERFORMANCE COMPARISON")
print("=" * 75)

print(
    results_df.to_string(
        index=False,
        float_format=lambda x: f"{x:.4f}"
    )
)


# =========================================================
# 7. Hyperparameter tuning - Random Forest
# =========================================================

print("\n" + "=" * 75)
print("RANDOM FOREST HYPERPARAMETER TUNING")
print("=" * 75)

rf = RandomForestRegressor(
    random_state=42,
    n_jobs=-1
)

rf_parameters = {
    "n_estimators": [200, 300, 500],
    "max_depth": [None, 10, 15, 20, 25],
    "min_samples_split": [2, 4, 6],
    "min_samples_leaf": [1, 2, 4],
    "max_features": ["sqrt", "log2", 0.7, 1.0]
}

rf_search = RandomizedSearchCV(
    rf,
    rf_parameters,
    n_iter=20,
    cv=5,
    scoring="r2",
    random_state=42,
    n_jobs=-1
)

print("\nSearching for better Random Forest parameters...")

rf_search.fit(X_train, y_train)

best_rf = rf_search.best_estimator_

print("\nBest Random Forest parameters:")
print(rf_search.best_params_)

print(f"\nBest cross-validation R2: {rf_search.best_score_:.4f}")


# =========================================================
# 8. Evaluate tuned Random Forest
# =========================================================

rf_predictions = best_rf.predict(X_test)

rf_mae = mean_absolute_error(
    y_test,
    rf_predictions
)

rf_rmse = np.sqrt(
    mean_squared_error(
        y_test,
        rf_predictions
    )
)

rf_r2 = r2_score(
    y_test,
    rf_predictions
)


print("\nTUNED RANDOM FOREST RESULTS")

print(f"MAE  : {rf_mae:.4f}")
print(f"RMSE : {rf_rmse:.4f}")
print(f"R2   : {rf_r2:.4f}")


# =========================================================
# 9. Add tuned model to comparison
# =========================================================

tuned_row = pd.DataFrame([{
    "Model": "Tuned Random Forest",
    "MAE": rf_mae,
    "RMSE": rf_rmse,
    "R2": rf_r2,
    "CV_R2_Mean": rf_search.best_score_,
    "CV_R2_STD": np.nan
}])

results_df = pd.concat(
    [results_df, tuned_row],
    ignore_index=True
)

results_df = results_df.sort_values(
    by="R2",
    ascending=False
).reset_index(drop=True)


# =========================================================
# 10. Create output directories
# =========================================================

os.makedirs("results", exist_ok=True)
os.makedirs("models", exist_ok=True)


# =========================================================
# 11. Save comparison
# =========================================================

results_df.to_csv(
    "results/model_comparison.csv",
    index=False
)


# =========================================================
# 12. Select best model
# =========================================================

best_model_name = results_df.iloc[0]["Model"]

print("\n" + "=" * 75)
print("BEST MODEL")
print("=" * 75)

print(f"\nBest model based on test R2: {best_model_name}")


if best_model_name == "Tuned Random Forest":

    final_model = best_rf

else:

    final_model = trained_models[best_model_name]


# =========================================================
# 13. Generate final predictions
# =========================================================

final_predictions = final_model.predict(X_test)

final_mae = mean_absolute_error(
    y_test,
    final_predictions
)

final_rmse = np.sqrt(
    mean_squared_error(
        y_test,
        final_predictions
    )
)

final_r2 = r2_score(
    y_test,
    final_predictions
)


# =========================================================
# 14. Actual vs predicted graph
# =========================================================

plt.figure(figsize=(8, 6))

plt.scatter(
    y_test,
    final_predictions,
    alpha=0.7
)

minimum = min(
    y_test.min(),
    final_predictions.min()
)

maximum = max(
    y_test.max(),
    final_predictions.max()
)

plt.plot(
    [minimum, maximum],
    [minimum, maximum],
    linestyle="--"
)

plt.xlabel("Actual Log Solubility")
plt.ylabel("Predicted Log Solubility")

plt.title(
    f"Actual vs Predicted - {best_model_name}"
)

plt.tight_layout()

plt.savefig(
    "results/final_actual_vs_predicted.png",
    dpi=300
)

plt.close()


# =========================================================
# 15. Feature importance
# =========================================================

if hasattr(final_model, "feature_importances_"):

    importance = pd.DataFrame({
        "Feature": feature_columns,
        "Importance": final_model.feature_importances_
    })

    importance = importance.sort_values(
        by="Importance",
        ascending=False
    )

    print("\n" + "=" * 75)
    print("FINAL MODEL FEATURE IMPORTANCE")
    print("=" * 75)

    print(
        importance.to_string(
            index=False
        )
    )

    plt.figure(figsize=(10, 7))

    plt.barh(
        importance["Feature"],
        importance["Importance"]
    )

    plt.xlabel("Importance")
    plt.ylabel("Molecular Descriptor")
    plt.title(
        f"Feature Importance - {best_model_name}"
    )

    plt.gca().invert_yaxis()

    plt.tight_layout()

    plt.savefig(
        "results/final_feature_importance.png",
        dpi=300
    )

    plt.close()

    importance.to_csv(
        "results/feature_importance.csv",
        index=False
    )


# =========================================================
# 16. Save predictions
# =========================================================

prediction_results = pd.DataFrame({
    "Actual_Solubility": y_test.values,
    "Predicted_Solubility": final_predictions
})

prediction_results.to_csv(
    "results/final_predictions.csv",
    index=False
)


# =========================================================
# 17. Save final metrics
# =========================================================

final_metrics = pd.DataFrame({
    "Metric": [
        "MAE",
        "RMSE",
        "R2"
    ],
    "Value": [
        final_mae,
        final_rmse,
        final_r2
    ]
})

final_metrics.to_csv(
    "results/final_metrics.csv",
    index=False
)


# =========================================================
# 18. Save best model
# =========================================================

joblib.dump(
    final_model,
    "models/best_solubility_model.pkl"
)


# Save feature list
with open(
    "models/feature_columns.txt",
    "w"
) as file:

    for feature in feature_columns:
        file.write(feature + "\n")


# =========================================================
# 19. Final report
# =========================================================

print("\n" + "=" * 75)
print("ADVANCED MODEL TRAINING COMPLETED")
print("=" * 75)

print(f"\nBest Model : {best_model_name}")
print(f"MAE        : {final_mae:.4f}")
print(f"RMSE       : {final_rmse:.4f}")
print(f"R2         : {final_r2:.4f}")

print("\nSaved files:")

print("  ✓ results/model_comparison.csv")
print("  ✓ results/final_actual_vs_predicted.png")
print("  ✓ results/final_predictions.csv")
print("  ✓ results/final_metrics.csv")
print("  ✓ models/best_solubility_model.pkl")
print("  ✓ models/feature_columns.txt")

if hasattr(final_model, "feature_importances_"):
    print("  ✓ results/final_feature_importance.png")
    print("  ✓ results/feature_importance.csv")

print("\nAdvanced machine-learning pipeline completed.")
print("=" * 75)