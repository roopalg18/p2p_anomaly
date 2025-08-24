from __future__ import annotations
import os
import pandas as pd
import matplotlib.pyplot as plt

def eda_summary(df: pd.DataFrame) -> pd.DataFrame:
    s = pd.DataFrame({
        "rows_total": [len(df)],
        "vendors_unique": [df["vendor_id"].nunique()],
        "gl_unique": [df["gl_code"].nunique()],
        "date_min": [pd.to_datetime(df["date_submitted"]).min().date()],
        "date_max": [pd.to_datetime(df["date_submitted"]).max().date()],
        "avg_final_score": [float(df.get("final_score", pd.Series([0])).mean())]
    })
    return s

def export_topN(df: pd.DataFrame, outdir: str, topn: int = 150) -> str:
    cols_review = [
        "invoice_id","vendor_id","vendor_name","date_submitted","amount","currency",
        "gl_code","invoice_num","po_num","no_po","amt_to_policy","dup_exact_invoice_num",
        "near_dup_window","is_weekend","is_round_1000","is_new_vendor_60",
        "rule_score","if_score","lof_score","final_score","flag_reason"
    ]
    top = df.sort_values("final_score", ascending=False).head(topn).copy()
    path = os.path.join(outdir, "top_anomalies_review_list.csv")
    top[cols_review].to_csv(path, index=False)
    return path

def plot_hist(df: pd.DataFrame, outdir: str) -> str:
    plt.figure(figsize=(7,5))
    plt.hist(df["final_score"], bins=50)
    plt.title("Distribution of Final Anomaly Scores")
    plt.xlabel("final_score")
    plt.ylabel("count")
    plt.tight_layout()
    path = os.path.join(outdir, "final_score_hist.png")
    plt.savefig(path)
    plt.close()
    return path
