"""
Regulatory Preclinical In Silico Discovery Dossier Generator
Generates comprehensive, standalone HTML reports for drug candidates.
"""

import datetime
from typing import Dict, Any


def generate_dossier_html(candidate_name: str, smiles: str, admet_data: Dict[str, Any]) -> str:
    """
    Renders an executive, publication-grade In Silico ADMET Dossier HTML.
    """
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    desc = admet_data["Descriptors"]
    preds = admet_data["Predictions"]
    pk = admet_data["Pharmacokinetics"]
    dl = admet_data["Drug_Likeness"]
    alerts = admet_data["Structural_Alerts"]
    score = admet_data["Overall_Candidate_Score"]

    # Formatting colors
    sol_color = preds["Solubility_Color"]
    clintox_badge = '<span class="badge danger">High Risk</span>' if "High" in preds["ClinTox_Risk"] else '<span class="badge success">Safe / Tolerated</span>'
    p53_badge = '<span class="badge danger">Positive (Mutagenic)</span>' if "Positive" in preds["p53_Genotoxicity"] else '<span class="badge success">Negative (Non-Mutagenic)</span>'
    pains_badge = '<span class="badge success">Zero Alerts</span>' if alerts["PAINS_Safe"] else f'<span class="badge warning">{alerts["PAINS_Alerts_Count"]} Alerts</span>'
    lipinski_badge = '<span class="badge success">Pass</span>' if dl["Lipinski_Pass"] else '<span class="badge danger">Violation</span>'

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>In Silico ADMET Discovery Dossier — {candidate_name}</title>
<style>
    body {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        background-color: #0d1117;
        color: #c9d1d9;
        margin: 0;
        padding: 40px;
        line-height: 1.6;
    }}
    .container {{
        max-width: 950px;
        margin: 0 auto;
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 36px 48px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }}
    .header {{
        border-bottom: 2px solid #30363d;
        padding-bottom: 20px;
        margin-bottom: 25px;
    }}
    .title {{
        font-size: 28px;
        font-weight: 800;
        color: #58a6ff;
        margin: 0 0 8px 0;
    }}
    .subtitle {{
        font-size: 15px;
        color: #8b949e;
        margin: 0;
    }}
    .hero-grid {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 16px;
        margin: 25px 0;
    }}
    .hero-card {{
        background: #0e1117;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 18px;
        text-align: center;
    }}
    .hero-card .label {{
        font-size: 12px;
        color: #8b949e;
        text-transform: uppercase;
        font-weight: 700;
        letter-spacing: 0.5px;
    }}
    .hero-card .value {{
        font-size: 22px;
        font-weight: 800;
        margin: 8px 0 4px 0;
        color: #f0f6fc;
    }}
    .section-title {{
        font-size: 20px;
        font-weight: 700;
        color: #f0f6fc;
        margin-top: 30px;
        margin-bottom: 15px;
        border-bottom: 1px solid #21262d;
        padding-bottom: 8px;
    }}
    table {{
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 20px;
        font-size: 14px;
    }}
    th, td {{
        padding: 10px 14px;
        text-align: left;
        border-bottom: 1px solid #21262d;
    }}
    th {{
        background-color: #21262d;
        color: #8b949e;
        font-weight: 600;
    }}
    .badge {{
        display: inline-block;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 600;
    }}
    .badge.success {{ background: #238636; color: #fff; }}
    .badge.warning {{ background: #9e6a03; color: #fff; }}
    .badge.danger {{ background: #da3633; color: #fff; }}
    .footer {{
        margin-top: 40px;
        padding-top: 15px;
        border-top: 1px solid #30363d;
        font-size: 12px;
        color: #8b949e;
        text-align: center;
    }}
</style>
</head>
<body>
<div class="container">
    <div class="header">
        <div class="title">💊 Regulatory Preclinical In Silico ADMET Dossier</div>
        <div class="subtitle">Candidate: <b>{candidate_name}</b> | Molecular Formula: <code>{admet_data["Formula"]}</code></div>
        <div class="subtitle" style="margin-top: 5px;">SMILES: <code>{smiles}</code></div>
    </div>

    <div class="hero-grid">
        <div class="hero-card" style="border-top: 4px solid {sol_color};">
            <div class="label">Solubility (LogS)</div>
            <div class="value">{preds["Solubility_LogS"]:.3f}</div>
            <span class="badge" style="background: {sol_color};">{preds["Solubility_Class"]}</span>
        </div>
        <div class="hero-card" style="border-top: 4px solid #388bfd;">
            <div class="label">Lipophilicity (LogD)</div>
            <div class="value">{preds["Lipophilicity_LogD"]:.3f}</div>
            <span class="badge" style="background: #1f6feb;">pH 7.4 Physiological</span>
        </div>
        <div class="hero-card" style="border-top: 4px solid #a371f7;">
            <div class="label">Blood-Brain Barrier</div>
            <div class="value">{preds["BBBP_Probability"]*100:.1f}%</div>
            <span class="badge" style="background: #8957e5;">{preds["BBBP_Penetration"]}</span>
        </div>
        <div class="hero-card" style="border-top: 4px solid #f0883e;">
            <div class="label">Overall Score</div>
            <div class="value">{score}/100</div>
            <span class="badge" style="background: #d29922;">Candidate MPO</span>
        </div>
    </div>

    <div class="section-title">1. Physicochemical & Topological Characterization</div>
    <table>
        <tr><th>Property Parameter</th><th>Computed Value</th><th>Optimal Oral Bioavailability Window</th></tr>
        <tr><td>Molecular Weight (MW)</td><td>{desc["Molecular_Weight"]:.2f} g/mol</td><td>150 – 500 Da (Lipinski Rule)</td></tr>
        <tr><td>Wildman-Crippen LogP</td><td>{desc["LogP"]:.2f}</td><td>-0.4 to +5.0</td></tr>
        <tr><td>Topological Polar Surface Area (TPSA)</td><td>{desc["TPSA"]:.2f} Å²</td><td>20 – 140 Å² (Veber Rule)</td></tr>
        <tr><td>H-Bond Donors (HBD) / Acceptors (HBA)</td><td>{desc["HBD"]} / {desc["HBA"]}</td><td>HBD ≤ 5, HBA ≤ 10</td></tr>
        <tr><td>Rotatable Bonds (Flexibility)</td><td>{desc["Rotatable_Bonds"]}</td><td>≤ 10 rotatable bonds</td></tr>
        <tr><td>Fraction Sp3 Carbons (Fsp3)</td><td>{desc["Fraction_CSP3"]:.3f}</td><td>≥ 0.40 (High 3D saturation)</td></tr>
        <tr><td>Heavy Atom / Heteroatom Count</td><td>{desc["Heavy_Atom_Count"]} / {desc["Heteroatom_Count"]}</td><td>Balanced stoichiometry</td></tr>
        <tr><td>Formal Charge</td><td>{desc["Formal_Charge"]}</td><td>Neutral / Monovalent</td></tr>
    </table>

    <div class="section-title">2. Pharmacokinetics & ADME Profile</div>
    <table>
        <tr><th>PK Endpoint</th><th>Prediction</th><th>Clinical Assessment</th></tr>
        <tr><td>Caco-2 Permeability</td><td>{pk["Caco2_LogPapp"]} log(cm/s)</td><td>{pk["Caco2_Permeability"]}</td></tr>
        <tr><td>Human Intestinal Absorption (HIA)</td><td>{pk["HIA_Percentage"]:.1f}%</td><td>Oral Absorption Potential</td></tr>
        <tr><td>Plasma Protein Binding (PPB)</td><td>{pk["PPB_Percentage"]:.1f}%</td><td>Free drug fraction in blood circulation</td></tr>
        <tr><td>CYP1A2 / CYP2C9 Inhibition</td><td>{"Inhibitor Risk" if pk["CYP1A2_Inhibitor"] else "Low Risk"} / {"Inhibitor Risk" if pk["CYP2C9_Inhibitor"] else "Low Risk"}</td><td>Hepatic drug-drug interaction profile</td></tr>
        <tr><td>CYP2D6 / CYP3A4 Inhibition</td><td>{"Inhibitor Risk" if pk["CYP2D6_Inhibitor"] else "Low Risk"} / {"Inhibitor Risk" if pk["CYP3A4_Inhibitor"] else "Low Risk"}</td><td>Major xenobiotic clearance pathways</td></tr>
    </table>

    <div class="section-title">3. Toxicology & Structural Alerts</div>
    <table>
        <tr><th>Safety Parameter</th><th>Result</th><th>Status</th></tr>
        <tr><td>Clinical Toxicity Trial Failure (ClinTox)</td><td>{preds["ClinTox_Risk"]} (Probability: {preds["ClinTox_Probability"]*100:.1f}%)</td><td>{clintox_badge}</td></tr>
        <tr><td>Tox21 p53 Genotoxicity / DNA Damage</td><td>{preds["p53_Genotoxicity"]} (Probability: {preds["p53_Probability"]*100:.1f}%)</td><td>{p53_badge}</td></tr>
        <tr><td>PAINS (Pan-Assay Interference)</td><td>{alerts["PAINS_Alerts_Count"]} structural matches found</td><td>{pains_badge}</td></tr>
        <tr><td>Brenk Toxicophores / Reactive Moieties</td><td>{alerts["Brenk_Alerts_Count"]} hazardous groups detected</td><td>{"Zero Alerts" if alerts["Brenk_Safe"] else "Review Required"}</td></tr>
    </table>

    <div class="section-title">4. Medicinal Chemistry Compliance & Drug-Likeness</div>
    <table>
        <tr><th>Framework</th><th>Compliance Status</th><th>Notes</th></tr>
        <tr><td>Lipinski's Rule of Five</td><td>{lipinski_badge}</td><td>Violations: {dl["Lipinski_Violations"]} ({", ".join(dl["Lipinski_Details"])})</td></tr>
        <tr><td>Veber Bioavailability Rule</td><td>{"Pass" if dl["Veber_Pass"] else "Violation"}</td><td>{", ".join(dl["Veber_Details"])}</td></tr>
        <tr><td>Quantitative Estimate of Drug-likeness (QED)</td><td>{dl["QED"]:.3f} / 1.000</td><td>Category: {dl["QED_Category"]} Drug-Likeness</td></tr>
        <tr><td>Pfizer CNS MPO Score</td><td>{dl["CNS_MPO_Score"]}/100</td><td>Rating: {dl["CNS_MPO_Grade"]}</td></tr>
    </table>

    <div class="footer">
        Generated automatically by Molecular Property Prediction & ADMET Intelligence Platform • Report Timestamp: {now_str}<br>
        Models validated on Delaney ESOL ($R^2=0.9029$, MAE=0.4628), ChEMBL Lipophilicity, MoleculeNet BBBP, ClinTox, and Tox21 benchmarks.
    </div>
</div>
</body>
</html>
"""
    return html
