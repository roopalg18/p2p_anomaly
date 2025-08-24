import pandas as pd
from p2p_anomaly.features import vendor_gl_features

def test_vendor_gl_features_shapes():
    df = pd.DataFrame({
        "invoice_id": ["1","2","3","4"],
        "vendor_id": ["A","A","B","B"],
        "vendor_name": ["x","x","y","y"],
        "invoice_num": ["i1","i2","i3","i4"],
        "po_num": ["PO-1","","PO-2",""],
        "date_submitted": pd.to_datetime(["2024-01-01","2024-01-03","2024-01-02","2024-01-04"]),
        "amount": [100, 120, 3000, 3100],
        "currency": ["CAD"]*4,
        "gl_code": ["6110-OfficeSupplies","6110-OfficeSupplies","6150-IT-Software","6150-IT-Software"],
        "policy_limit": [1500,1500,20000,20000],
        "vendor_created_date": pd.to_datetime(["2023-12-01"]*4),
        "vendor_country": ["CA"]*4,
        "vendor_high_risk_bank_change": [False]*4,
        "description": ["a","b","c","d"]
    })
    out = vendor_gl_features(df)
    for col in ["vendor_amt_rZ","gl_amt_rZ","amt_to_policy","is_weekend","vendor_age_days",
                "is_new_vendor_60","is_round_1000","no_po","dup_exact_invoice_num","near_dup_window"]:
        assert col in out.columns
