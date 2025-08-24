from __future__ import annotations
import os
import pandas as pd
from .config import GenParams
from .data import generate_synthetic, inject_anomalies
from .features import vendor_gl_features
from .rules import compute_rule_score, flag_reason_strings
from .models import score_ml
from .evaluate import eda_summary, export_topN, plot_hist

def run_pipeline(outdir: str,
                 n_invoices: int = 8000,
                 n_vendors: int = 220,
                 seed: int = 42,
                 topn: int = 150) -> dict:
    os.makedirs(outdir, exist_ok=True)
    params = GenParams(n_invoices=n_invoices, n_vendors=n_vendors, seed=seed)

    # 1) Generate + 2) Inject anomalies
    raw = generate_synthetic(params)
    raw_path = os.path.join(outdir, "invoices_raw.csv")
    raw.to_csv(raw_path, index=False)

    data = inject_anomalies(raw, seed=seed)

    # 3) Feature engineering
    feats = vendor_gl_features(data)
    feats_path = os.path.join(outdir, "invoices_with_features.csv")
    feats.to_csv(feats_path, index=False)

    # 4) Rules
    ruled = compute_rule_score(feats)
    ruled["flag_reason"] = flag_reason_strings(ruled)

    # 5) ML scoring + blend
    scored = score_ml(ruled, seed=seed)
    scored_path = os.path.join(outdir, "invoices_with_scores.csv")
    scored.to_csv(scored_path, index=False)

    # 6) EDA + exports
    eda = eda_summary(scored)
    eda_path = os.path.join(outdir, "eda_summary.csv")
    eda.to_csv(eda_path, index=False)

    top_path = export_topN(scored, outdir, topn=topn)
    hist_path = plot_hist(scored, outdir)

    return {
        "raw": raw_path,
        "features": feats_path,
        "scored": scored_path,
        "top": top_path,
        "eda": eda_path,
        "hist": hist_path
    }
