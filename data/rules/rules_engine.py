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
    sunita = {"state": "Maharashtra", "crop": "cotton", "land_acres": 2,
              "is_insured": True, "days_since_event": 1}
    late = {"state": "Maharashtra", "crop": "cotton", "land_acres": 2,
            "is_insured": True, "days_since_event": 10}
    print("Sunita:", json.dumps(check_eligibility("pmfby_crop_damage", sunita), indent=2, ensure_ascii=False))
    print("Late:", json.dumps(check_eligibility("pmfby_crop_damage", late), indent=2, ensure_ascii=False))