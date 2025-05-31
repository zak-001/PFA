@app.route('/download_error/<id_rand>')
@login_required
def download_error(id_rand):
    filter_obj = Filtro()
    if not filter_obj.check_str(id_rand):
        flash('Invalid data supplied', 'danger')
        return redirect(url_for('websites'))

    production = Production.query.filter_by(id_rand=id_rand).first()
    if not production:
        flash('Application not found', 'danger')
        return redirect(url_for('websites'))

    random_suffix = random.randint(0, 999999999)
    tarball_name = f'error_logs_{production.app_name}_{random_suffix}.tar.gz'
    tarball_path = os.path.join('/home/www-data/waf2py_community/applications/Waf2Py/static/logs', tarball_name)

    # Create tar.gz archive
    cmd = [
        '/usr/bin/tar', '-czvf', tarball_path,
        '-C', f'/opt/waf/nginx/var/log/{production.app_name}/',
        f'{production.app_name}_error.log'
    ]
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode != 0:
        flash('Failed to create archive', 'danger')
        return redirect(url_for('websites'))

    return send_from_directory(directory=os.path.dirname(tarball_path), filename=tarball_name, as_attachment=True)
