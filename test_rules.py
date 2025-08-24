import pandas as pd
from p2p_anomaly.rules import compute_rule_score, flag_reason_strings

def test_rule_score_and_reasons():
    df = pd.DataFrame({
        "amount": [2000, 10000],
        "policy_limit": [1500, 5000],
        "amt_to_policy": [2000/1500, 10000/5000],
        "dup_exact_invoice_num": [True, False],
        "near_dup_window": [False, True],
        "is_weekend": [True, False],
        "is_round_1000": [True, False],
        "is_new_vendor_60": [False, True],
        "no_po": [True, False],
        "vendor_high_risk_bank_change": [False, True],
    })
    scored = compute_rule_score(df)
    assert "rule_score" in scored.columns
    reasons = flag_reason_strings(scored)
    assert isinstance(reasons.iloc[0], str) and "Duplicate" in reasons.iloc[0]
