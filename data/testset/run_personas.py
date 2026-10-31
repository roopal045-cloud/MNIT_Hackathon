import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "rules"))
from rules_engine import check_eligibility
data = json.load(open(Path(__file__).parent / "personas.json", encoding="utf-8"))
ok = 0
for p in data["personas"]:
    r = check_eligibility(p["scheme"], p["facts"])
    good = r["eligible"] == p["expected_eligible"]
    ok += good
    print(p["id"], "PASS" if good else "FAIL")
print(ok, "of", len(data["personas"]), "passed")