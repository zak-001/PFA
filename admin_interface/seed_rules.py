import re
import os
from app import create_app
from db import engine
from models import rule_table
from sqlalchemy import select, insert

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
    with engine.begin() as conn:
        total = 0
        for rule_file in RULE_FILES:
            rules = parse_rules(rule_file)
            for rule in rules:
                exists = conn.execute(
                    select(rule_table.c.id).where(rule_table.c.rule_id == rule["rule_id"])
                ).first()
                if not exists:
                    conn.execute(insert(rule_table).values(**rule))
                    total += 1

        print(f"✅ Imported {total} new rules.")
