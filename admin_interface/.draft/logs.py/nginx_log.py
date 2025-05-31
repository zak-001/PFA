@app.route('/nginx_log')
@login_required
def nginx_log():
    try:
        result = subprocess.run(['tac', '/opt/waf/nginx/var/log/error'], capture_output=True, text=True)
        lines = result.stdout.splitlines()
        log_lines = lines[:600]
    except Exception as e:
        flash(str(e), 'danger')
        log_lines = []

    return render_template('nginx_log.html', log_lines=log_lines, page="NGINX logs", icon="fa fa-search", title="NGINX Logs")
