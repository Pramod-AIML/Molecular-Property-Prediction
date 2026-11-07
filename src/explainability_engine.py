"""
Explainable AI (XAI) & Chemical Attribution Engine
Generates Atom-Level Solubility/Lipophilicity Heatmaps and Highlights Toxicophores.
"""

import io
import base64
from typing import Dict, Any, List, Optional, Tuple

from rdkit import Chem
from rdkit.Chem import rdMolDescriptors, AllChem
from rdkit.Chem.Draw import rdMolDraw2D, SimilarityMaps


def _resolve_mol(mol):
    if isinstance(mol, str):
        m = Chem.MolFromSmiles(mol.strip())
        if m is None:
            raise ValueError(f"Invalid SMILES string: {mol}")
        return m
    return mol


def get_atom_solubility_weights(mol) -> List[float]:
    """
    Computes atomic contribution weights to aqueous solubility.
    Negative Crippen LogP and high polar surface / charge contribute positively to aqueous solubility.
    """
    mol = _resolve_mol(mol)
    contribs = rdMolDescriptors._CalcCrippenContribs(mol)
    try:
        AllChem.ComputeGasteigerCharges(mol)
    except Exception:
        pass

    weights = []
    for idx, atom in enumerate(mol.GetAtoms()):
        logp_contrib = contribs[idx][0]
        try:
            charge = float(atom.GetProp('_GasteigerCharge'))
        except Exception:
            charge = 0.0

        # High polarity and negative logP enhance hydration/solubility
        # Green / positive = favors solubility, Red / negative = opposes solubility
        w = (-1.2 * logp_contrib) + (0.8 * abs(charge))
        weights.append(float(w))

    return weights


def generate_attribution_map_base64(
    mol,
    width: int = 500,
    height: int = 420
) -> str:
    """
    Renders 2D molecule with atom-level contour similarity map.
    Returns base64 PNG data URI.
    """
    mol = _resolve_mol(mol)
    weights = get_atom_solubility_weights(mol)
    
    # Modern RDKit MolDraw2DCairo
    d2d = rdMolDraw2D.MolDraw2DCairo(width, height)
    dopts = d2d.drawOptions()
    dopts.clearBackground = False
    
    SimilarityMaps.GetSimilarityMapFromWeights(
        mol,
        weights,
        draw2d=d2d,
        contourLines=8,
        alpha=0.45,
        coordScale=1.4
    )
    d2d.FinishDrawing()
    png_bytes = d2d.GetDrawingText()
    
    b64 = base64.b64encode(png_bytes).decode("ascii")
    return f"data:image/png;base64,{b64}"


def generate_highlighted_molecule_svg(
    mol,
    highlight_atoms: Optional[List[int]] = None,
    width: int = 450,
    height: int = 350
) -> str:
    """
    Renders crisp SVG depiction of molecule with optional highlighted alert atoms.
    """
    mol = _resolve_mol(mol)
    d2d = rdMolDraw2D.MolDraw2DSVG(width, height)
    dopts = d2d.drawOptions()
    dopts.bondLineWidth = 2.0
    dopts.clearBackground = False
    
    if highlight_atoms:
        d2d.DrawMolecule(mol, highlightAtoms=highlight_atoms)
    else:
        d2d.DrawMolecule(mol)
        
    d2d.FinishDrawing()
    return d2d.GetDrawingText()


def explain_molecule_features(mol) -> Dict[str, Any]:
    """
    Returns breakdown of functional groups and atom-level insights.
    """
    mol = _resolve_mol(mol)
    weights = get_atom_solubility_weights(mol)
    
    solubilizing_atoms = []
    insolubilizing_atoms = []
    
    for idx, (atom, w) in enumerate(zip(mol.GetAtoms(), weights)):
        info = {
            "atom_idx": idx,
            "symbol": atom.GetSymbol(),
            "weight": round(w, 3),
            "is_aromatic": atom.GetIsAromatic()
        }
        if w > 0.15:
            solubilizing_atoms.append(info)
        elif w < -0.15:
            insolubilizing_atoms.append(info)
            
    # Sort by impact
    solubilizing_atoms.sort(key=lambda x: x["weight"], reverse=True)
    insolubilizing_atoms.sort(key=lambda x: x["weight"])
    
    return {
        "Solubilizing_Moieties_Count": len(solubilizing_atoms),
        "Top_Solubilizing_Atoms": solubilizing_atoms[:5],
        "Insolubilizing_Moieties_Count": len(insolubilizing_atoms),
        "Top_Insolubilizing_Atoms": insolubilizing_atoms[:5]
    }
