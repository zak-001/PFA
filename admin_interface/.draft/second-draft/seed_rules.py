from app import create_app, db
from models import Rule
import re
import os

RULE_FILES = ["/path/to/default_rules.conf"]

rule_pattern = re.compile(r'SecRule.*?id:(\d+).*', re.DOTALL)

def parse_rules(file_path):
    rules = []
    with open(file_path) as f:
        file_name = os.path.basename(file_path)
        for line in f:
            if "SecRule" in line and "id:" in line:
                match = rule_pattern.search(line)
                if match:
                    rule_id = match.group(1)
                    rules.append({
                        "rule_id": rule_id,
                        "content": line.strip(),
                        "description": file_name,
                        "severity": "MEDIUM",
                        "tags": "imported",
                        "source": "default",
                        "enabled": True
                    })
    return rules

app = create_app()
with app.app_context():
    count = 0
    for rule_file in RULE_FILES:
        rules = parse_rules(rule_file)
        for r in rules:
            if not Rule.query.filter_by(rule_id=r["rule_id"]).first():
                db.session.add(Rule(**r))
        db.session.commit()
        count += len(rules)
    print(f"Imported {count} rules.")