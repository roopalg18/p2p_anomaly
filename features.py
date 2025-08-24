from __future__ import annotations
import numpy as np
import pandas as pd

def vendor_gl_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

    # Robust z vs vendor
    vendor_grp = out.groupby("vendor_id")["amount"]
    v_med = vendor_grp.transform("median")
    v_mad = vendor_grp.transform(lambda s: (np.abs(s - np.median(s))).median() + 1e-6)
    out["vendor_amt_rZ"] = (out["amount"] - v_med) / (1.4826 * v_mad)

    # Robust z vs GL
    gl_grp = out.groupby("gl_code")["amount"]
    g_med = gl_grp.transform("median")
    g_mad = gl_grp.transform(lambda s: (np.abs(s - np.median(s))).median() + 1e-6)
    out["gl_amt_rZ"] = (out["amount"] - g_med) / (1.4826 * g_mad)

    # Policy pressure
    out["amt_to_policy"] = out["amount"] / out["policy_limit"].replace(0, np.nan)

    # Temporal flags
    ds = pd.to_datetime(out["date_submitted"])
    out["is_weekend"] = ds.dt.weekday >= 5

    # Vendor age
    vcd = pd.to_datetime(out["vendor_created_date"])
    out["vendor_age_days"] = (ds - vcd).dt.days.clip(lower=0)
    out["is_new_vendor_60"] = out["vendor_age_days"] < 60

    # Round-number & PO flags
    out["is_round_1000"] = (out["amount"] % 1000).round(2) == 0
    out["no_po"] = out["po_num"].fillna("").eq("")

    # Duplicates
    out["dup_exact_invoice_num"] = out.duplicated(subset=["vendor_id", "invoice_num"], keep=False)

    # Near-duplicate by (vendor, amount) within ±3 days
    sorted_df = out.sort_values(["vendor_id", "amount", "date_submitted"]).copy()
    sorted_df["prev_date"] = sorted_df.groupby(["vendor_id","amount"])["date_submitted"].shift(1)
    sorted_df["next_date"] = sorted_df.groupby(["vendor_id","amount"])["date_submitted"].shift(-1)
    prev_diff = (pd.to_datetime(sorted_df["date_submitted"]) - pd.to_datetime(sorted_df["prev_date"])).dt.days.abs()
    next_diff = (pd.to_datetime(sorted_df["next_date"]) - pd.to_datetime(sorted_df["date_submitted"])).dt.days.abs()
    sorted_df["near_dup_window"] = ((prev_diff <= 3) | (next_diff <= 3)).fillna(False)
    out["near_dup_window"] = sorted_df["near_dup_window"].values

    return out
