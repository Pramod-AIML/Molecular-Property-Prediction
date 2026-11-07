"""
Molecular Property Prediction & In-Silico ADMET Intelligence Platform
Production FastAPI Web Server & Microservice with Interactive Real-Time UI.
Lead Developer: M. Pramod (24BAI1417)
"""

from typing import List, Optional
import os
import uvicorn
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.Draw import rdMolDraw2D

from src.admet_engine import predict_full_admet
from src.lead_optimizer import generate_lead_analogs
from src.explainability_engine import explain_molecule_features, generate_attribution_map_base64
from src.dossier_generator import generate_dossier_html


app = FastAPI(
    title="Molecular Property Prediction & In-Silico ADMET Platform",
    description=(
        "Production AI/ML Web Application and Microservice for Molecular Property Prediction, "
        "Aqueous Solubility (LogS), Multi-Endpoint ADMET Profiling, "
        "Explainable AI (XAI) Attribution, and Generative Lead Optimization. "
        "Developed by M. Pramod (24BAI1417)."
    ),
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for cross-origin frontend or external API access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount results directory to serve plots and architecture diagrams
if os.path.exists("results"):
    app.mount("/results", StaticFiles(directory="results"), name="results")


# ---------------------------------------------------------------------------
# PYDANTIC SCHEMAS
# ---------------------------------------------------------------------------
class SmilesRequest(BaseModel):
    smiles: str = Field(..., example="CC(=O)Oc1ccccc1C(=O)O", description="Valid chemical SMILES string")

class BatchSmilesRequest(BaseModel):
    molecules: List[dict] = Field(
        ...,
        example=[
            {"id": "Aspirin", "smiles": "CC(=O)Oc1ccccc1C(=O)O"},
            {"id": "Ibuprofen", "smiles": "CC(C)Cc1ccc(cc1)C(C)C(=O)O"},
            {"id": "Paracetamol", "smiles": "CC(=O)Nc1ccc(O)cc1"}
        ],
        description="List of compound dictionaries containing 'id' and 'smiles'"
    )


# ---------------------------------------------------------------------------
# WEB APPLICATION ROUTE
# ---------------------------------------------------------------------------
@app.get("/", response_class=HTMLResponse, tags=["Web Application"])
def serve_website():
    """
    Serves the real-time interactive chemical studio web application.
    """
    html_path = os.path.join("templates", "index.html")
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>Molecular Property Prediction Platform</h1><p>Frontend template not found.</p>"


@app.get("/api", tags=["General"])
def api_root():
    """
    JSON API capabilities summary.
    """
    return {
        "platform": "Molecular Property Prediction & In-Silico ADMET Intelligence Platform",
        "version": "2.0.0",
        "author": "M. Pramod (24BAI1417)",
        "status": "online",
        "documentation": "/docs",
        "capabilities": [
            "Aqueous Solubility (LogS) Prediction",
            "Lipophilicity (LogD7.4)",
            "Blood-Brain Barrier Penetration (BBBP)",
            "Clinical Trial Toxicity Risk (ClinTox)",
            "Tox21 p53 Genotoxicity",
            "Pharmacokinetics (Caco-2, HIA, PPB, CYP450)",
            "Medicinal Chemistry Rules (Lipinski, Veber, Ghose, QED, CNS MPO)",
            "Explainable AI (XAI) Contour Heatmaps",
            "Generative Lead Optimization & Bioisosteres",
            "Interactive 3D WebGL Conformer (MMFF94)",
            "High-Throughput Batch Virtual Screening"
        ]
    }


@app.get("/health", tags=["General"])
def health_check():
    return {
        "status": "healthy",
        "solubility_model": os.path.exists("models/final_combined_solubility_model.pkl"),
        "lipophilicity_model": os.path.exists("models/lipophilicity_model.pkl"),
        "bbbp_model": os.path.exists("models/bbbp_model.pkl"),
        "clintox_model": os.path.exists("models/clintox_model.pkl"),
        "p53_model": os.path.exists("models/p53_toxicity_model.pkl")
    }


# ---------------------------------------------------------------------------
# PREDICTION & ADMET ENDPOINTS
# ---------------------------------------------------------------------------
@app.post("/api/v1/predict/admet", tags=["Predictions"])
def predict_admet_endpoint(payload: SmilesRequest):
    """
    Predicts complete Physicochemical, Pharmacokinetic, and ADMET profile for a single molecule.
    """
    try:
        results = predict_full_admet(payload.smiles)
        return {"success": True, "data": results}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/v1/molecule/conformer-3d", tags=["Visualization"])
def get_3d_conformer(payload: SmilesRequest):
    """
    Generates an optimized 3D molecular conformer (MMFF94 force field) for 3Dmol.js WebGL visualization.
    """
    try:
        mol = Chem.MolFromSmiles(payload.smiles.strip())
        if mol is None:
            raise ValueError("Invalid SMILES string.")
        mol_h = Chem.AddHs(mol)
        res = AllChem.EmbedMolecule(mol_h, randomSeed=42)
        if res != 0:
            AllChem.EmbedMolecule(mol_h, useRandomCoords=True, randomSeed=42)
        try:
            AllChem.MMFFOptimizeMolecule(mol_h, maxIters=200)
        except Exception:
            pass
        mol_block = Chem.MolToMolBlock(mol_h)
        return {"success": True, "mol_block": mol_block, "atoms": mol.GetNumAtoms()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/v1/molecule/svg-2d", tags=["Visualization"])
def get_2d_svg(payload: SmilesRequest):
    """
    Renders high-contrast 2D chemical structure in vector SVG format.
    """
    try:
        mol = Chem.MolFromSmiles(payload.smiles.strip())
        if mol is None:
            raise ValueError("Invalid SMILES string.")
        drawer = rdMolDraw2D.MolDraw2DSVG(380, 260)
        opts = drawer.drawOptions()
        opts.clearBackground = True
        drawer.DrawMolecule(mol)
        drawer.FinishDrawing()
        svg = drawer.GetDrawingText()
        return {"success": True, "svg": svg}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/v1/optimize/lead", tags=["Lead Optimization"])
def optimize_lead_endpoint(payload: SmilesRequest, max_analogs: int = Query(6, ge=1, le=12)):
    """
    Generates intelligent bioisosteric structural analogs, ranks them by overall score improvement,
    and returns delta improvements over parent candidate.
    """
    try:
        results = generate_lead_analogs(payload.smiles, max_analogs=max_analogs)
        return {"success": True, "data": results}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/v1/explain/attribution", tags=["Explainable AI"])
def explain_attribution_endpoint(payload: SmilesRequest):
    """
    Computes atom-level attribution weights and returns a base64 contour heatmap.
    """
    try:
        mol = Chem.MolFromSmiles(payload.smiles.strip())
        if mol is None:
            raise ValueError("Invalid chemical SMILES.")

        explanation = explain_molecule_features(mol)
        heatmap_b64 = generate_attribution_map_base64(mol)

        return {
            "success": True,
            "explanation": explanation,
            "heatmap_data_uri": heatmap_b64
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/v1/screening/batch", tags=["Virtual Screening"])
def batch_screening_endpoint(payload: BatchSmilesRequest):
    """
    Batch virtual high-throughput screening for up to 100 compounds.
    """
    if len(payload.molecules) > 100:
        raise HTTPException(status_code=400, detail="Batch size limited to 100 molecules per request.")

    screened_results = []
    for item in payload.molecules:
        cmpd_id = item.get("id", "Unknown")
        smi = item.get("smiles", "")
        try:
            admet = predict_full_admet(smi)
            screened_results.append({
                "id": cmpd_id,
                "smiles": smi,
                "success": True,
                "formula": admet["Formula"],
                "logS": admet["Predictions"]["Solubility_LogS"],
                "solubility_class": admet["Predictions"]["Solubility_Class"],
                "logD": admet["Predictions"]["Lipophilicity_LogD"],
                "bbbp": admet["Predictions"]["BBBP_Penetration"],
                "clintox": admet["Predictions"]["ClinTox_Risk"],
                "p53_tox": admet["Predictions"]["p53_Genotoxicity"],
                "qed": admet["Drug_Likeness"]["QED"],
                "lipinski_pass": admet["Drug_Likeness"]["Lipinski_Pass"],
                "pains_safe": admet["Structural_Alerts"]["PAINS_Safe"],
                "overall_score": admet["Overall_Candidate_Score"]
            })
        except Exception as e:
            screened_results.append({
                "id": cmpd_id,
                "smiles": smi,
                "success": False,
                "error": str(e)
            })

    return {
        "success": True,
        "total_screened": len(screened_results),
        "results": screened_results
    }


@app.post("/api/v1/dossier/download", tags=["Reporting"])
def download_dossier(payload: SmilesRequest, name: Optional[str] = "Candidate"):
    """
    Generates and downloads a complete, standalone Preclinical Regulatory Dossier HTML.
    """
    try:
        clean_name = name or "Candidate"
        admet = predict_full_admet(payload.smiles.strip())
        html_content = generate_dossier_html(clean_name, payload.smiles.strip(), admet)
        return Response(
            content=html_content,
            media_type="text/html",
            headers={"Content-Disposition": f'attachment; filename="{clean_name}_ADMET_Dossier.html"'}
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ---------------------------------------------------------------------------
# APPLICATION ENTRYPOINT
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("api:app", host="0.0.0.0", port=port)
