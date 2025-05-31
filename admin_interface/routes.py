from flask import Blueprint, render_template, request, redirect, flash, url_for, session
from sqlalchemy import select, update
from werkzeug.security import check_password_hash
from models import rule_table
from db import engine

main_bp = Blueprint('main', __name__)
waf_bp = Blueprint('waf', __name__)

@main_bp.route('/')
def home():
    return render_template('signin.html')

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        with engine.connect() as conn:
            result = conn.execute(
                "SELECT id, email, password, nom, prenom FROM users WHERE email = %s", (email,)
            )
            user = result.fetchone()

        if user and check_password_hash(user[2], password):
            session['email'] = user[1]
            flash('Connexion réussie ✅', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Email ou mot de passe incorrect ❌', 'danger')

    return render_template('signin.html')

@main_bp.route('/dashboard')
def dashboard():
    if 'email' not in session:
        return redirect(url_for('main.login'))

    with engine.connect() as conn:
        email = session['email']
        user_data = conn.execute(
            "SELECT nom FROM users WHERE email = %s", (email,)
        ).fetchone()

        logs = conn.execute(
            "SELECT client_ip, host_cible, uri, method, attack_type, status, created_at FROM waf_logs ORDER BY created_at DESC LIMIT 3"
        ).fetchall()

    return render_template('index.html', nom=user_data[0], logs=logs) if user_data else redirect(url_for('main.login'))

@main_bp.route('/logs')
def logs():
    if 'email' not in session:
        return redirect(url_for('main.login'))

    with engine.connect() as conn:
        email = session['email']
        user_data = conn.execute("SELECT nom FROM users WHERE email = %s", (email,)).fetchone()
        logs = conn.execute(
            "SELECT client_ip, host_cible, uri, method, attack_type, status, created_at FROM waf_logs ORDER BY created_at DESC LIMIT 100"
        ).fetchall()

    return render_template('logs.html', nom=user_data[0], logs=logs)

@waf_bp.route('/waf')
def list_rules():
    page = request.args.get('page', 1, type=int)
    severity_filter = request.args.get('severity')
    enabled_filter = request.args.get('enabled')

    stmt = select(rule_table)

    if severity_filter:
        stmt = stmt.where(rule_table.c.severity == severity_filter)
    if enabled_filter in ['true', 'false']:
        stmt = stmt.where(rule_table.c.enabled == (enabled_filter == 'true'))

    stmt = stmt.order_by(rule_table.c.rule_id).limit(10).offset((page - 1) * 10)

    with engine.connect() as conn:
        rules = conn.execute(stmt).fetchall()

    return render_template('rules_list.html', rules=rules)

@waf_bp.route('/rules/<int:rule_id>/toggle', methods=['POST'])
def toggle_rule(rule_id):
    with engine.begin() as conn:
        result = conn.execute(select(rule_table).where(rule_table.c.id == rule_id)).first()
        if result:
            new_value = not result.enabled
            conn.execute(update(rule_table).where(rule_table.c.id == rule_id).values(enabled=new_value))
            flash(f"Rule {result.rule_id} {'enabled' if new_value else 'disabled'}.", "success")
    return redirect(url_for('waf.list_rules'))

@waf_bp.route('/rules/<int:rule_id>/edit', methods=['GET', 'POST'])
def edit_rule(rule_id):
    with engine.begin() as conn:
        rule = conn.execute(select(rule_table).where(rule_table.c.id == rule_id)).first()

        if request.method == 'POST':
            conn.execute(update(rule_table).where(rule_table.c.id == rule_id).values(
                description=request.form.get('description', rule.description),
                content=request.form.get('content', rule.content),
                severity=request.form.get('severity', rule.severity)
            ))
            flash(f"Rule {rule.rule_id} updated successfully.", "success")
            return redirect(url_for('waf.list_rules'))

    return render_template('edit_rule.html', rule=rule)
