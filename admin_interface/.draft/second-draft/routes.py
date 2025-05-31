from flask import Blueprint, render_template, request, redirect, flash, url_for
from models import Rule, ChangeLog, db
from modsec_utils import generate_modsec_config, validate_modsec_config

waf_bp = Blueprint('waf', __name__)

# your routes here
@waf_bp.route('/rules')
def list_rules():
    page = request.args.get('page', 1, type=int)
    severity_filter = request.args.get('severity')
    enabled_filter = request.args.get('enabled')

    query = Rule.query

    if severity_filter:
        query = query.filter_by(severity=severity_filter)
    if enabled_filter in ['true', 'false']:
        query = query.filter_by(enabled=(enabled_filter == 'true'))

    pagination = query.order_by(Rule.rule_id).paginate(page=page, per_page=10)
    return render_template('rules_list.html', pagination=pagination, rules=pagination.items)

@waf_bp.route('/rules/<int:rule_id>/toggle', methods=['POST'])
def toggle_rule(rule_id):
    rule = Rule.query.get_or_404(rule_id)
    rule.enabled = not rule.enabled
    db.session.commit()
    flash(f"Rule {rule.rule_id} {'enabled' if rule.enabled else 'disabled'}.", "success")
    return redirect(url_for('waf.list_rules'))

@waf_bp.route('/rules/<int:rule_id>/edit', methods=['GET', 'POST'])
def edit_rule(rule_id):
    rule = Rule.query.get_or_404(rule_id)

    if request.method == 'POST':
        rule.description = request.form.get('description', rule.description)
        rule.content = request.form.get('content', rule.content)
        rule.severity = request.form.get('severity', rule.severity)
        # Optionally: update tags, enabled, etc.

        db.session.commit()
        flash(f"Rule {rule.rule_id} updated successfully.", "success")
        return redirect(url_for('waf.list_rules'))

    return render_template('edit_rule.html', rule=rule)