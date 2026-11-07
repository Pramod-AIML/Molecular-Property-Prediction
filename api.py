"""
Molecular Property Prediction & ADMET Intelligence REST API
Production-grade FastAPI Microservice with OpenAPI / Swagger Documentation.
"""

from typing import List, Optional
import os
import uvicorn
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from rdkit import Chem

from src.admet_engine import predict_full_admet
from src.lead_optimizer import generate_lead_analogs
from src.explainability_engine import explain_molecule_features, generate_attribution_map_base64


app = FastAPI(
    title="Molecular Property Prediction & In-Silico ADMET API",
    description=(
        "Production AI/ML Microservice for Molecular Property Prediction, "
        "Aqueous Solubility (LogS), Multi-Endpoint ADMET Profiling, "
        "Explainable AI (XAI) Attribution, and Generative Lead Optimization."
    ),
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for cross-origin frontend or dashboard access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
# API ROUTES
# ---------------------------------------------------------------------------
@app.get("/", tags=["General"])
def root():
    return {
        "platform": "Molecular Property Prediction & ADMET Intelligence Platform",
        "version": "2.0.0",
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
            "Generative Lead Optimization & Bioisosteres"
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


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("api:app", host="0.0.0.0", port=port)
