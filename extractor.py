"""
extractor.py
Converts a plain-language business description into structured fields.

Default mode: lightweight rule/regex-based extraction (no API key needed,
runs fully offline - good for hackathon demos).

Optional mode: if ANTHROPIC_API_KEY is set in the environment, swaps in an
LLM call for more robust extraction on messy real-world input.
"""

import re
import os
import json

GOODS_KEYWORDS = [
    "sell", "vendor", "shop", "store", "cart", "stall", "trader", "retail",
    "grocery", "vegetable", "fruit", "clothes", "clothing", "hardware",
    "manufacture", "manufacturing", "produce", "goods", "kirana"
]

SERVICES_KEYWORDS = [
    "consult", "consultant", "freelance", "freelancer", "repair", "tailor",
    "salon", "tuition", "tutor", "driver", "delivery", "service", "plumber",
    "electrician", "designer", "developer", "photographer", "carpenter"
]

STATE_LIST = [
    "manipur", "mizoram", "nagaland", "tripura", "arunachal pradesh",
    "meghalaya", "sikkim", "uttarakhand", "assam", "himachal pradesh",
    "jammu and kashmir", "rajasthan", "maharashtra", "delhi", "karnataka",
    "tamil nadu", "gujarat", "west bengal", "uttar pradesh", "punjab",
    "kerala", "telangana", "haryana", "bihar", "odisha", "madhya pradesh"
]

WOMAN_KEYWORDS = ["woman", "woman-owned", "female entrepreneur", "she runs", "her business"]
SC_ST_KEYWORDS = ["sc entrepreneur", "st entrepreneur", "sc/st", "scheduled caste", "scheduled tribe"]
NEW_BUSINESS_KEYWORDS = ["starting", "new business", "about to start", "planning to open", "just started"]


def _extract_monthly_or_annual_revenue(text: str):
    """
    Looks for numeric revenue mentions like '15,000/month', '₹2 lakh a year',
    '3 lakh per month', '50000 monthly' etc. Returns ANNUAL revenue in INR.
    """
    text_l = text.lower().replace(",", "")

    # Pattern: number followed by lakh/lac/crore
    lakh_pattern = re.search(r'(\d+(?:\.\d+)?)\s*(lakh|lac|l)\b', text_l)
    crore_pattern = re.search(r'(\d+(?:\.\d+)?)\s*(crore|cr)\b', text_l)
    plain_number = re.search(r'(?:₹|rs\.?|inr)?\s*(\d{3,})', text_l)

    is_monthly = bool(re.search(r'month|monthly|/mo\b|per month', text_l))
    is_yearly = bool(re.search(r'year|yearly|annual|per year|/yr', text_l))

    amount = None
    if crore_pattern:
        amount = float(crore_pattern.group(1)) * 10_000_000
    elif lakh_pattern:
        amount = float(lakh_pattern.group(1)) * 100_000
    elif plain_number:
        amount = float(plain_number.group(1))

    if amount is None:
        return None

    # Convert to annual figure
    if is_monthly and not is_yearly:
        annual = amount * 12
    else:
        annual = amount

    return int(annual)


def _extract_business_type(text: str):
    text_l = text.lower()
    goods_score = sum(1 for kw in GOODS_KEYWORDS if kw in text_l)
    services_score = sum(1 for kw in SERVICES_KEYWORDS if kw in text_l)

    if goods_score == 0 and services_score == 0:
        return "goods"  # default assumption
    return "goods" if goods_score >= services_score else "services"


def _extract_state(text: str):
    text_l = text.lower()
    for state in STATE_LIST:
        if state in text_l:
            return state
    return None


def _extract_flags(text: str):
    text_l = text.lower()
    return {
        "is_woman_owned": any(kw in text_l for kw in WOMAN_KEYWORDS),
        "is_sc_st": any(kw in text_l for kw in SC_ST_KEYWORDS),
        "is_new_business": any(kw in text_l for kw in NEW_BUSINESS_KEYWORDS),
    }


def extract_business_profile(text: str) -> dict:
    """
    Main entry point. Returns a structured dict:
    {
        annual_revenue: int | None,
        business_type: 'goods' | 'services',
        state: str | None,
        is_woman_owned: bool,
        is_sc_st: bool,
        is_new_business: bool,
        raw_text: str
    }
    """
    if os.environ.get("ANTHROPIC_API_KEY"):
        try:
            return _extract_with_llm(text)
        except Exception:
            pass  # fall back silently to rule-based extraction

    profile = {
        "annual_revenue": _extract_monthly_or_annual_revenue(text),
        "business_type": _extract_business_type(text),
        "state": _extract_state(text),
        "raw_text": text,
    }
    profile.update(_extract_flags(text))
    return profile


def _extract_with_llm(text: str) -> dict:
    """Optional LLM-backed extraction for messier real-world input."""
    import anthropic

    client = anthropic.Anthropic()
    prompt = f"""Extract structured data from this small-business description.
Return ONLY valid JSON, no preamble, matching this exact schema:
{{
  "annual_revenue": <integer INR or null>,
  "business_type": "goods" or "services",
  "state": <lowercase Indian state name or null>,
  "is_woman_owned": <boolean>,
  "is_sc_st": <boolean>,
  "is_new_business": <boolean>
}}

Description: "{text}"
"""
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    )
    raw = response.content[0].text.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()
    data = json.loads(raw)
    data["raw_text"] = text
    return data
