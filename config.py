from dataclasses import dataclass

GL_POLICY_LIMITS = {
    "6110-OfficeSupplies":       1500,
    "6120-Travel":               2000,
    "6130-MealsEntertainment":    500,
    "6140-Training":             2500,
    "6150-IT-Software":         20000,
    "6160-IT-Hardware":         15000,
    "6170-ProfessionalServices": 30000,
    "6180-Maintenance":         10000,
    "6190-Utilities":           50000,
    "6200-Marketing":           12000,
    "6210-Logistics":           25000,
    "6220-Rent":               100000,
    "6230-Legal":               40000,
    "6240-Consulting":          50000,
    "6250-HR-Recruiting":        8000,
    "6260-Other":                5000,
}

CATEGORY_SCALES = {
    "OfficeSupplies":         250,
    "Travel":                 800,
    "MealsEntertainment":     120,
    "Training":              1000,
    "IT-Software":           8000,
    "IT-Hardware":           6000,
    "ProfessionalServices": 12000,
    "Maintenance":           3000,
    "Utilities":            15000,
    "Marketing":             4000,
    "Logistics":             7000,
    "Rent":                 60000,
    "Legal":                 9000,
    "Consulting":           15000,
    "HR-Recruiting":         2500,
    "Other":                 1000,
}

@dataclass
class GenParams:
    n_invoices: int = 8000
    n_vendors: int = 220
    currency: str = "CAD"
    start_date: str = "2024-01-01"
    end_date: str = "2025-07-31"
    seed: int = 42
