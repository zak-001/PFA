from app import db
from datetime import datetime, timezone

class Rule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rule_id = db.Column(db.String(50), unique=True)
    content = db.Column(db.Text)
    enabled = db.Column(db.Boolean, default=True)
    source = db.Column(db.String(20), default="custom")  # "default" or "custom"
    description = db.Column(db.String(255))
    severity = db.Column(db.String(20))
    tags = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, onupdate=datetime.now(timezone.utc))

class ChangeLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rule_id = db.Column(db.String(50))
    action = db.Column(db.String(20))  # 'created', 'updated', 'deleted'
    changed_by = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    diff = db.Column(db.Text)  # Optional: store what changed
