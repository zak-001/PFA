@app.route('/exclude_local', methods=['POST'])
@login_required
def exclude_local():
    try:
        id_rand = request.form['id_rand']
        ruleid = request.form['ruleid']
        attack_name = request.form['attack_name'].rstrip()
        path = request.form['path']
        rule_type = int(request.form['type'])
    except (KeyError, ValueError):
        return jsonify({'error': 'Invalid input data'}), 400

    # You need to implement the Filtro class methods or equivalent validation in Flask
    filter_obj = Filtro()
    if not (filter_obj.check_str(id_rand) and filter_obj.check_rule(ruleid) and filter_obj.check_name(attack_name) and filter_obj.check_path(path)):
        return jsonify({'error': 'Validation failed'}), 400

    # Check exclusions in DB using SQLAlchemy (adapt model names)
    existing = Exclusion.query.filter_by(
        id_rand=id_rand, 
        type=rule_type, 
        rules_id=ruleid,
        local_path=path
    ).first()

    if existing:
        return jsonify({'message': 'Rule ID or Path already excluded'}), 400

    # Insert new exclusion
    custom_id = random.randint(0, 99999999)
    new_exclusion = Exclusion(
        rules_id=ruleid,
        id_rand=id_rand,
        custom_id=custom_id,
        local_path=path,
        type=rule_type,
        attack_name=attack_name,
        user=current_user.username
    )
    db.session.add(new_exclusion)
    db.session.commit()

    # Query updated rules for this id_rand and type
    exclusions = Exclusion.query.filter_by(id_rand=id_rand, type=rule_type).all()

    # Build new rules string
    rules = '#ExclusionLocal\n'
    for exclusion in exclusions:
        rules += f'SecRule REQUEST_URI "@beginswith {exclusion.local_path}" "id:{exclusion.custom_id},phase:1,pass,nolog, ctl:ruleRemoveById={exclusion.rules_id}"\n'

    # Fetch modsec_conf (assuming a one-to-one relation)
    production = Production.query.filter_by(id_rand=id_rand).first()
    if not production:
        return jsonify({'error': 'Production app not found'}), 404

    # Replace old rules block with new one using regex
    pattern = re.compile(r'^(##\w+Local\w+##\n).*(##\w+Local\w+##)', re.S | re.M)
    new_modsec_conf_data = pattern.sub(r'\1' + rules + r'\2', production.modsec_conf_data)

    production.modsec_conf_data = new_modsec_conf_data
    db.session.commit()

    # Update config files and reload Nginx - implement these methods accordingly
    update_files = CreateFiles()
    try:
        update_files.create_modsec_conf(production.app_name, new_modsec_conf_data)
        nginx = Nginx()
        nginx.reload()
    except Exception as e:
        flash(str(e), 'danger')
        return jsonify({'error': 'Failed to update configuration'}), 500

    return jsonify({'message': 'Rule has been excluded locally'})
