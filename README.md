# AI-Powered Invoice Anomaly Detection (P2P)

This is a project I built to simulate a **real consulting engagement in Finance Transformation**. The goal was to explore how finance teams can reduce the manual effort in invoice review by combining **traditional accounting controls** with **unsupervised machine learning**.

In many organizations, Procure-to-Pay (P2P) is still heavily manual: invoices are checked line by line for duplicates, unusual amounts, or missing purchase orders. This is time-consuming, error-prone, and expensive. My project automates that process.

---

## Motivation

I wanted to practice applying data + analytics to a **real business problem**. Duplicate invoices, policy breaches, and vendor fraud are common risks in finance operations. At the same time, consultants help clients embed analytics and AI into their finance processes. This project was my way of building something that feels like a **mini consulting deliverable**.

---

## What the Pipeline Does

1. **Synthetic Invoice Data**  
   Generates realistic P2P invoices (vendors, GL codes, amounts, PO numbers, dates). All data is **synthetic** for confidentiality.

2. **Anomaly Injection**  
   Simulates real failure modes:
   - Duplicate invoices  
   - Policy breaches (amount > 1.5× policy limit)  
   - Weekend submissions  
   - Round-number suspicious amounts (e.g., $10,000)  
   - Inflated vs vendor median  
   - New vendors (<60 days) and missing POs  

3. **Feature Engineering**  
   Creates risk signals:
   - `amt_to_policy` (policy pressure)  
   - Robust z-scores by vendor & GL (median + MAD)  
   - Duplicate/near-duplicate flags  
   - Weekend / new vendor flags  

4. **Rules Engine (Explainable Controls)**  
   Scores invoices based on accounting-style rules (duplicates, policy breaches, etc.).  

5. **Unsupervised ML Models**  
   - **Isolation Forest** → global outliers  
   - **Local Outlier Factor (LOF)** → local density anomalies  

6. **Score Blending**  
   Final anomaly score = weighted mix of rules + ML.  
   (Example: `0.5*IF + 0.3*LOF + 0.2*Rules`)  

7. **Outputs for Review**  
   - `invoices_with_scores.csv` – full dataset with features + scores  
   - `top_anomalies_review_list.csv` – top N suspicious invoices with flag reasons  
   - `eda_summary.csv` – quick overview (row counts, vendor count, date range, avg score)  
   - `final_score_hist.png` – histogram of anomaly scores  

---

## What I Learned

- How Procure-to-Pay (P2P) works in practice (requisitions → POs → invoices → payments).  
- Why **robust z-scores** (median + MAD) outperform mean/std in skewed financial data.  
- How to combine **auditable rules** with **unsupervised ML** for explainability + coverage.  
- Basics of **Isolation Forest** and **LOF** for anomaly detection.  
- How to make results **actionable** for finance managers in **Power BI**.  

---

## Sample Output

Histogram of final anomaly scores (most invoices are low risk, but a small tail are flagged):

![Final Score Histogram](out/final_score_hist.png)

---

## How to Run

Clone this repo and run the pipeline locally:

```bash
# (optional) create virtual environment
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate

# install dependencies
pip install -r requirements.txt

# run pipeline (outputs go to ./out)
python -m p2p_anomaly.cli --outdir out --n_invoices 8000 --seed 42 --topn 150
```

---

## FAQ

**Q: Is this based on real company data?**  
A: No, all data is **synthetic** but generated to be statistically realistic (log-normal spend distributions, vendor creation dates, GL category limits, etc.). This avoids confidentiality issues while still demonstrating methodology.

**Q: Why combine rules with machine learning?**  
A: Rules (like duplicate invoice detection or policy limit breaches) are **explainable** and align with existing accounting controls. Machine learning (Isolation Forest + LOF) captures subtler anomalies. Together, they balance **coverage + explainability**.

**Q: Why Isolation Forest and Local Outlier Factor?**  
A: Isolation Forest is efficient on tabular data and good for global outliers. LOF captures **local density anomalies** (odd relative to peers). Using both gives complementary coverage.

**Q: How do you know it works without labeled fraud data?**  
A: I validate against **injected anomalies** (duplicates, inflated amounts, weekend spikes) and check that they rank in the top results. In a real deployment, finance teams would label cases, and we’d monitor **precision@K** and feedback loops.

**Q: What would you do next if this were for a client?**  
A:  
- Integrate OCR/NLP to flag suspicious invoice descriptions.  
- Link invoices to payments to detect duplicate *payments*, not just invoices.  
- Deploy the scoring pipeline in the cloud (e.g., Azure Functions + Power BI auto-refresh).  
- Add human-in-the-loop feedback to improve thresholds over time.  
