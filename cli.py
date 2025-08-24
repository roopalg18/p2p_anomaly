from __future__ import annotations
import argparse
from .pipeline import run_pipeline

def main():
    p = argparse.ArgumentParser(
        description="AI-Powered Invoice Anomaly Detection (Rules + IsolationForest + LOF)"
    )
    p.add_argument("--outdir", type=str, default="out", help="Output directory")
    p.add_argument("--n_invoices", type=int, default=8000, help="Number of invoices to simulate")
    p.add_argument("--n_vendors", type=int, default=220, help="Number of vendors to simulate")
    p.add_argument("--seed", type=int, default=42, help="Random seed")
    p.add_argument("--topn", type=int, default=150, help="Top N invoices to export for review")
    args = p.parse_args()

    paths = run_pipeline(
        outdir=args.outdir,
        n_invoices=args.n_invoices,
        n_vendors=args.n_vendors,
        seed=args.seed,
        topn=args.topn
    )
    print("✅ Pipeline complete. Outputs:")
    for k, v in paths.items():
        print(f" - {k}: {v}")

if __name__ == "__main__":
    main()
