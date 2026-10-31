import json
from pathlib import Path

RULES_DIR = Path(__file__).parent

OPS = {
    "==": lambda a, b: a == b,
    "!=": lambda a, b: a != b,
    "<=": lambda a, b: a <= b,
    ">=": lambda a, b: a >= b,
    "<": lambda a, b: a < b,
    ">": lambda a, b: a > b,
    "in": lambda a, b: a in b,
}


def load_rule(scheme):
    path = RULES_DIR / (scheme + ".json")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def check_eligibility(scheme, facts):
    rule = load_rule(scheme)
    reasons = []
    eligible = True
    for cond in rule["conditions"]:
        field = cond["field"]
        if field not in facts:
            eligible = False
            reasons.append("Missing information: " + field)
            continue
        if OPS[cond["op"]](facts[field], cond["value"]):
            reasons.append("OK: " + cond["reason_en"])
        else:
            eligible = False
            reasons.append("NOT MET: " + cond["reason_en"])
    return {
        "eligible": eligible,
        "reasons": reasons,
        "source": rule["source"],
        "verified": "NEEDS HUMAN VERIFICATION" not in rule["last_verified"],
    }


if __name__ == "__main__":
    base = {"state": "Maharashtra", "crop": "cotton", "land_acres": 2,
            "is_insured": True, "premium_paid_before_event": True}
    cases = {
        "Sunita (hailstorm, 1 day)": dict(base, cause="hailstorm", days_since_event=1),
        "Late (hailstorm, 10 days)": dict(base, cause="hailstorm", days_since_event=10),
        "Rain only (not a covered cause)": dict(base, cause="rain", days_since_event=1),
    }
    for name, facts in cases.items():
        r = check_eligibility("pmfby_crop_damage", facts)
        print(name, "->", "ELIGIBLE" if r["eligible"] else "NOT ELIGIBLE")
