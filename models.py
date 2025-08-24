from __future__ import annotations
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor

def _minmax(a: np.ndarray) -> np.ndarray:
    a = a.astype(float)
    return (a - a.min()) / (a.max() - a.min() + 1e-9)

def score_ml(df: pd.DataFrame,
             features=("amount","vendor_amt_rZ","gl_amt_rZ","amt_to_policy","vendor_age_days"),
             seed: int = 11) -> pd.DataFrame:
    out = df.copy()
    X = out[list(features)].replace([np.inf, -np.inf], np.nan).fillna(0.0).copy()
    X["log_amount"] = np.log1p(X["amount"])
    X = X.drop(columns=["amount"])

    scaler = StandardScaler()
    Xs = scaler.fit_transform(X)

    iso = IsolationForest(n_estimators=200, contamination=0.01, random_state=seed)
    if_scores_raw = -iso.fit(Xs).score_samples(Xs)

    lof = LocalOutlierFactor(n_neighbors=35, contamination=0.01)
    lof_labels = lof.fit_predict(Xs)
    lof_scores_raw = -lof.negative_outlier_factor_

    out["if_score"] = _minmax(if_scores_raw)
    out["lof_score"] = _minmax(lof_scores_raw)
    out["rule_score_norm"] = _minmax(out["rule_score"].values)
    out["final_score"] = 0.5*out["if_score"] + 0.3*out["lof_score"] + 0.2*out["rule_score_norm"]
    return out
