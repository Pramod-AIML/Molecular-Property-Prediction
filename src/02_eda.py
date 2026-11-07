import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------------------------------------------------
# 1. Load processed molecular dataset
# ---------------------------------------------------------

INPUT_FILE = "data/molecular_features.csv"

df = pd.read_csv(INPUT_FILE)

print("=" * 70)
print("MOLECULAR PROPERTY PREDICTION - EXPLORATORY DATA ANALYSIS")
print("=" * 70)

print(f"\nDataset shape: {df.shape}")

print("\nColumns:")
for column in df.columns:
    print(f"  - {column}")


# ---------------------------------------------------------
# 2. Basic statistics
# ---------------------------------------------------------

print("\nTarget variable statistics:")
print(df["measured log solubility in mols per litre"].describe())


# ---------------------------------------------------------
# 3. Create results directory
# ---------------------------------------------------------

import os

os.makedirs("results", exist_ok=True)


# ---------------------------------------------------------
# 4. Target distribution
# ---------------------------------------------------------

plt.figure(figsize=(9, 6))

sns.histplot(
    df["measured log solubility in mols per litre"],
    bins=30,
    kde=True
)

plt.title("Distribution of Molecular Solubility")
plt.xlabel("Measured Log Solubility (mol/L)")
plt.ylabel("Number of Molecules")
plt.tight_layout()

plt.savefig("results/solubility_distribution.png", dpi=300)
plt.show()

plt.close()


# ---------------------------------------------------------
# 5. Molecular weight distribution
# ---------------------------------------------------------

plt.figure(figsize=(9, 6))

sns.histplot(
    df["Molecular_Weight"],
    bins=30,
    kde=True
)

plt.title("Distribution of Molecular Weight")
plt.xlabel("Molecular Weight")
plt.ylabel("Number of Molecules")
plt.tight_layout()

plt.savefig("results/molecular_weight_distribution.png", dpi=300)
plt.show()

plt.close()


# ---------------------------------------------------------
# 6. LogP distribution
# ---------------------------------------------------------

plt.figure(figsize=(9, 6))

sns.histplot(
    df["LogP"],
    bins=30,
    kde=True
)

plt.title("Distribution of LogP")
plt.xlabel("LogP")
plt.ylabel("Number of Molecules")
plt.tight_layout()

plt.savefig("results/logp_distribution.png", dpi=300)
plt.show()

plt.close()


# ---------------------------------------------------------
# 7. Correlation heatmap
# ---------------------------------------------------------

descriptor_columns = [
    "measured log solubility in mols per litre",
    "Molecular_Weight",
    "LogP",
    "TPSA",
    "HBD",
    "HBA",
    "Ring_Count",
    "Rotatable_Bonds",
    "Fraction_CSP3"
]

correlation_matrix = df[descriptor_columns].corr()

plt.figure(figsize=(11, 8))

sns.heatmap(
    correlation_matrix,
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    center=0
)

plt.title("Correlation Between Molecular Descriptors and Solubility")
plt.tight_layout()

plt.savefig("results/correlation_heatmap.png", dpi=300)
plt.show()

plt.close()


# ---------------------------------------------------------
# 8. Molecular Weight vs Solubility
# ---------------------------------------------------------

plt.figure(figsize=(9, 6))

plt.scatter(
    df["Molecular_Weight"],
    df["measured log solubility in mols per litre"],
    alpha=0.6
)

plt.title("Molecular Weight vs Solubility")
plt.xlabel("Molecular Weight")
plt.ylabel("Measured Log Solubility")
plt.tight_layout()

plt.savefig("results/molecular_weight_vs_solubility.png", dpi=300)
plt.show()

plt.close()


# ---------------------------------------------------------
# 9. LogP vs Solubility
# ---------------------------------------------------------

plt.figure(figsize=(9, 6))

plt.scatter(
    df["LogP"],
    df["measured log solubility in mols per litre"],
    alpha=0.6
)

plt.title("LogP vs Solubility")
plt.xlabel("LogP")
plt.ylabel("Measured Log Solubility")
plt.tight_layout()

plt.savefig("results/logp_vs_solubility.png", dpi=300)
plt.show()

plt.close()


# ---------------------------------------------------------
# 10. Save correlation matrix
# ---------------------------------------------------------

correlation_matrix.to_csv(
    "results/correlation_matrix.csv"
)


# ---------------------------------------------------------
# 11. Completion message
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("EXPLORATORY DATA ANALYSIS COMPLETED")
print("=" * 70)

print("\nGenerated files:")

files = [
    "solubility_distribution.png",
    "molecular_weight_distribution.png",
    "logp_distribution.png",
    "correlation_heatmap.png",
    "molecular_weight_vs_solubility.png",
    "logp_vs_solubility.png",
    "correlation_matrix.csv"
]

for file in files:
    print(f"  ✓ results/{file}")

print("\nEDA completed successfully.")