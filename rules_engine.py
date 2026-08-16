"""
rules_engine.py
Pure rule-based logic mapping a business profile -> registration requirements,
estimated tax, and unlocked government benefits.

No ML here on purpose: correctness matters more than novelty for this piece.
"""

import json
import os

RULES_PATH = os.path.join(os.path.dirname(__file__), "data", "tax_rules.json")

with open(RULES_PATH, "r") as f:
    RULES = json.load(f)


def check_gst_requirement(annual_revenue: int, business_type: str, state: str | None) -> dict:
    thresholds = RULES["gst_thresholds"]
    is_special_state = state in thresholds["special_category_states"] if state else False

    if business_type == "services":
        limit = thresholds["services_special_states"] if is_special_state else thresholds["services"]
    else:
        limit = thresholds["goods_special_states"] if is_special_state else thresholds["goods_normal_states"]

    required = annual_revenue is not None and annual_revenue >= limit

    return {
        "required": required,
        "threshold": limit,
        "is_special_state": is_special_state,
    }


def calculate_presumptive_tax(annual_revenue: int, business_type: str) -> dict:
    """
    Applies Section 44AD (goods/trade) or 44ADA (professional services) logic.
    """
    if annual_revenue is None:
        return {"applicable": False, "reason": "Revenue not specified"}

    if business_type == "services":
        rule = RULES["presumptive_taxation_44ADA"]
        if annual_revenue > rule["eligible_max_turnover"]:
            return {"applicable": False, "reason": "Turnover exceeds 44ADA limit of ₹75 lakh"}
        deemed_profit = annual_revenue * rule["profit_rate"]
        section = "44ADA"
    else:
        rule = RULES["presumptive_taxation_44AD"]
        if annual_revenue > rule["digital_receipts_max_turnover"]:
            return {"applicable": False, "reason": "Turnover exceeds 44AD limit of ₹3 crore"}
        # Assume cash-heavy (conservative) profit rate unless we know otherwise
        deemed_profit = annual_revenue * rule["profit_rate_cash"]
        section = "44AD"

    tax_owed = calculate_income_tax(deemed_profit)

    return {
        "applicable": True,
        "section": section,
        "deemed_profit": round(deemed_profit),
        "estimated_tax": tax_owed,
    }


def calculate_income_tax(taxable_income: float) -> int:
    """New regime slab calculation with Section 87A rebate."""
    slabs = RULES["income_tax_slabs_new_regime_2024"]
    rebate_limit = RULES["rebate_87A_limit"]

    if taxable_income <= rebate_limit:
        return 0

    tax = 0.0
    prev_limit = 0
    for slab in slabs:
        upto = slab["upto"]
        rate = slab["rate"]
        if upto is None:
            tax += max(0, taxable_income - prev_limit) * rate
            break
        if taxable_income > upto:
            tax += (upto - prev_limit) * rate
            prev_limit = upto
        else:
            tax += (taxable_income - prev_limit) * rate
            break

    return round(tax)


def classify_udyam_tier(annual_revenue: int) -> str | None:
    if annual_revenue is None:
        return None
    tiers = RULES["udyam_msme_tiers"]
    if annual_revenue <= tiers["micro"]["turnover_max"]:
        return "Micro"
    elif annual_revenue <= tiers["small"]["turnover_max"]:
        return "Small"
    elif annual_revenue <= tiers["medium"]["turnover_max"]:
        return "Medium"
    return "Above MSME threshold"


def get_eligible_benefits(profile: dict) -> list[dict]:
    revenue = profile.get("annual_revenue")
    eligible = []

    for b in RULES["benefits"]:
        req = b["requires"]
        matched = False

        if req == "any_business":
            matched = True
        elif req == "annual_turnover_below_1000000" and revenue is not None:
            matched = revenue < 1_000_000
        elif req == "annual_turnover_1000000_to_5000000" and revenue is not None:
            matched = 1_000_000 <= revenue < 500_000 * 10
        elif req == "annual_turnover_above_5000000_below_10000000" and revenue is not None:
            matched = 5_000_000 <= revenue < 10_000_000
        elif req == "new_business_manufacturing_or_service":
            matched = profile.get("is_new_business", False)
        elif req == "sc_st_woman_entrepreneur":
            matched = profile.get("is_sc_st", False) or profile.get("is_woman_owned", False)
        elif req == "turnover_below_20000000" and revenue is not None:
            matched = revenue < 20_000_000

        if matched:
            eligible.append(b)

    return eligible


def build_full_report(profile: dict) -> dict:
    """Ties everything together into one report dict consumed by the UI."""
    revenue = profile.get("annual_revenue")
    business_type = profile.get("business_type", "goods")
    state = profile.get("state")

    gst = check_gst_requirement(revenue, business_type, state) if revenue else None
    presumptive = calculate_presumptive_tax(revenue, business_type) if revenue else None
    udyam_tier = classify_udyam_tier(revenue) if revenue else None
    benefits = get_eligible_benefits(profile)

    return {
        "profile": profile,
        "gst": gst,
        "presumptive_tax": presumptive,
        "udyam_tier": udyam_tier,
        "benefits": benefits,
    }
