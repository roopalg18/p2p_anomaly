from __future__ import annotations
import pandas as pd

def compute_rule_score(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["rule_score"] = (
        5.0*out["dup_exact_invoice_num"].astype(int) +
        3.0*out["near_dup_window"].astype(int) +
        4.0*(out["amt_to_policy"] > 1.5).astype(int) +
        2.0*((out["amt_to_policy"] > 1.2) & (out["amt_to_policy"] <= 1.5)).astype(int) +
        0.5*out["is_weekend"].astype(int) +
        1.0*out["is_round_1000"].astype(int) +
        2.0*out["is_new_vendor_60"].astype(int) +
        1.0*out["no_po"].astype(int) +
        1.5*(out["no_po"] & (out["amount"] > 5000)).astype(int) +
        2.0*out["vendor_high_risk_bank_change"].astype(int)
    )
    return out

def flag_reason_strings(df: pd.DataFrame, max_reasons: int = 4) -> pd.Series:
    reasons = []
    for row in df.itertuples(index=False):
        r = []
        if row.dup_exact_invoice_num: r.append("Duplicate invoice#")
        if getattr(row, "near_dup_window", False): r.append("Near-duplicate (±3d)")
        if getattr(row, "amt_to_policy", 0) > 1.5: r.append("Policy breach >1.5x")
        elif getattr(row, "amt_to_policy", 0) > 1.2: r.append("Policy breach >1.2x")
        if getattr(row, "is_new_vendor_60", False): r.append("New vendor <60d")
        if getattr(row, "no_po", False): r.append("No PO")
        if getattr(row, "is_round_1000", False): r.append("Round $1k")
        if getattr(row, "is_weekend", False): r.append("Weekend")
        reasons.append(" • ".join(r[:max_reasons]))
    return pd.Series(reasons, index=df.index, name="flag_reason")
