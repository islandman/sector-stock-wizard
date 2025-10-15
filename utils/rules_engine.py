import yaml

def load_rules(path="rules/rules.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)

def evaluate_rule(rule, indicators):
    try:
        return eval(rule["condition"], {}, indicators)
    except Exception:
        return False

def evaluate_rules(rules, indicators):
    results = []
    for rule in rules:
        passed = evaluate_rule(rule, indicators)
        results.append({"name": rule["name"], "passed": passed})
    return results
