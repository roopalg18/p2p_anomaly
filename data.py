from __future__ import annotations
import random
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from faker import Faker
from .config import GL_POLICY_LIMITS, CATEGORY_SCALES, GenParams

fake = Faker()

def _rand_date(start: datetime, end: datetime) -> datetime:
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days))

def _invoice_num() -> str:
    return f"INV-{random.randint(100000, 999999)}"

def _po_num(p: float = 0.7) -> str:
    return f"PO-{random.randint(10000, 99999)}" if random.random() < p else ""

def generate_synthetic(gen: GenParams) -> pd.DataFrame:
    random.seed(gen.seed)
    np.random.seed(gen.seed)
    start = datetime.fromisoformat(gen.start_date)
    end = datetime.fromisoformat(gen.end_date)

    vendors = []
    for vid in range(1, gen.n_vendors + 1):
        days_ago = random.randint(30, 900)
        created_date = end - timedelta(days=days_ago)
        vendors.append({
            "vendor_id": f"V{vid:04d}",
            "vendor_name": fake.company(),
            "vendor_created_date": created_date.date(),
            "vendor_country": random.choice(["CA","US","MX","UK","DE","IN","PH","IE"]),
            "vendor_high_risk_bank_change": random.random() < 0.03
        })
    vendor_df = pd.DataFrame(vendors)

    gl_df = pd.DataFrame({
        "gl_code": list(GL_POLICY_LIMITS.keys()),
        "policy_limit": list(GL_POLICY_LIMITS.values())
    })
    gl_codes = gl_df["gl_code"].tolist()

    records = []
    for i in range(gen.n_invoices):
        v = vendor_df.sample(1).iloc[0]
        glc = random.choice(gl_codes)
        cat = glc.split("-", 1)[1]
        scale = CATEGORY_SCALES[cat]

        amount = float(np.round(np.random.lognormal(mean=np.log(scale), sigma=0.5), 2))
        date_sub = _rand_date(start, end)
        if random.random() < 0.12:
            date_paid = pd.NaT
        else:
            date_paid = date_sub + timedelta(days=random.randint(10, 35))

        records.append({
            "invoice_id": f"INV{i+1:06d}",
            "vendor_id": v["vendor_id"],
            "vendor_name": v["vendor_name"],
            "invoice_num": _invoice_num(),
            "po_num": _po_num(),
            "date_submitted": date_sub.date(),
            "date_paid": pd.NaT if pd.isna(date_paid) else date_paid.date(),
            "amount": amount,
            "currency": gen.currency,
            "gl_code": glc,
            "policy_limit": GL_POLICY_LIMITS[glc],
            "vendor_created_date": v["vendor_created_date"],
            "vendor_country": v["vendor_country"],
            "vendor_high_risk_bank_change": bool(v["vendor_high_risk_bank_change"]),
            "description": fake.sentence(nb_words=6)
        })
    return pd.DataFrame(records)

def inject_anomalies(df: pd.DataFrame,
                     dup_rate=0.006, infl_rate=0.008, weekend_rate=0.03,
                     round_rate=0.01, policy_rate=0.012, seed=1) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    out = df.copy()

    # Duplicates (same vendor+invoice_num)
    dup_idx = out.sample(int(dup_rate * len(out)), random_state=seed).index
    dups = out.loc[dup_idx].copy()
    for idx in dups.index:
        dups.at[idx, "invoice_id"] = f"DUP{idx:06d}"
        shift_days = random.choice([-3,-2,-1,1,2,3])
        d = pd.to_datetime(dups.at[idx, "date_submitted"])
        dups.at[idx, "date_submitted"] = (d + timedelta(days=shift_days)).date()
    out = pd.concat([out, dups], ignore_index=True)

    # Inflated amounts vs vendor median
    vendor_medians = out.groupby("vendor_id")["amount"].median()
    infl_idx = out.sample(int(infl_rate * len(out)), random_state=seed+1).index
    for idx in infl_idx:
        vid = out.at[idx, "vendor_id"]
        med = vendor_medians.get(vid, out["amount"].median())
        out.at[idx, "amount"] = float(np.round(med * random.uniform(5.0, 9.0), 2))

    # Weekend submissions
    weekend_idx = out.sample(int(weekend_rate * len(out)), random_state=seed+2).index
    for idx in weekend_idx:
        d = pd.to_datetime(out.at[idx, "date_submitted"])
        target = random.choice([5, 6])  # Sat/Sun
        shift = (target - d.weekday()) % 7
        out.at[idx, "date_submitted"] = (d + timedelta(days=shift)).date()

    # Round-number spikes
    round_idx = out.sample(int(round_rate * len(out)), random_state=seed+3).index
    for idx in round_idx:
        out.at[idx, "amount"] = float(random.choice([1000,2000,3000,5000,10000,20000]))

    # Policy breaches >1.5x
    policy_idx = out.sample(int(policy_rate * len(out)), random_state=seed+4).index
    for idx in policy_idx:
        lim = out.at[idx, "policy_limit"]
        out.at[idx, "amount"] = float(np.round(lim * random.uniform(1.6, 2.5), 2))

    return out
