from sqlalchemy import Table, Column, Integer, String, Text, DateTime, Boolean
from db import metadata  # your engine

from datetime import datetime, timezone

WAFLog = Table(
    "waf_logs",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("client_ip", String(45)),
    Column("host_cible", String(255)),
    Column("uri", Text),
    Column("method", String(10)),
    Column("attack_type", String(100)),
    Column("status", String(10)),
    Column("created_at", DateTime, default=datetime.now(timezone.utc))
)

rule_table = Table(
    "rule", metadata,
    Column("id", Integer, primary_key=True),
    Column("rule_id", String(50), unique=True),
    Column("content", Text),
    Column("enabled", Boolean, default=True),
    Column("source", String(20), default="custom"),  # "default" or "custom"
    Column("description", String(255)),
    Column("severity", String(20)),
    Column("tags", String(100)),
    Column("created_at", DateTime, default=lambda: datetime.now(timezone.utc)),
    Column("updated_at", DateTime, onupdate=lambda: datetime.now(timezone.utc))
)

changelog_table = Table(
    "change_log", metadata,
    Column("id", Integer, primary_key=True),
    Column("rule_id", String(50)),
    Column("action", String(20)),  # 'created', 'updated', 'deleted'
    Column("changed_by", String(100)),
    Column("timestamp", DateTime, default=datetime.now(timezone.utc)),
    Column("diff", Text)  # Optional: store what changed
)