"""
API REST local para Guardian.
Permite integración con otras aplicaciones.
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import threading
import json
from src.utils.settings_manager import (
    load_settings, save_settings, get_blocked_apps,
    add_blocked_app, remove_blocked_app, get_session_stats
)
from src.features.reports import get_daily_stats, get_weekly_stats, get_top_blocked_apps
from src.utils.logger import read_logs
from src.integrations.dashboard import get_dashboard_html
from src.features.gamification import get_gamification_status

app = Flask(__name__)
CORS(app)

# ========== RUTAS DE INFORMACIÓN ==========

@app.route('/api/status', methods=['GET'])
def get_status():
    """Obtiene el estado actual de Guardian."""
    settings = load_settings()
    return jsonify({
        'enabled': settings['enabled'],
        'profile': settings['current_profile'],
        'blocked_apps_count': len(get_blocked_apps())
    })

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Obtiene estadísticas de la sesión."""
    return jsonify(get_session_stats())

@app.route('/api/stats/daily', methods=['GET'])
def get_daily():
    """Obtiene estadísticas del día actual."""
    return jsonify(get_daily_stats())

@app.route('/api/stats/weekly', methods=['GET'])
def get_weekly():
    """Obtiene estadísticas semanales."""
    stats = get_weekly_stats()
    return jsonify([s for s in stats])

@app.route('/api/stats/top-apps', methods=['GET'])
def get_top_apps():
    """Obtiene las apps más bloqueadas."""
    days = request.args.get('days', 7, type=int)
    apps = get_top_blocked_apps(days)
    return jsonify({
        'top_blocked': [{'app': app, 'count': count} for app, count in apps]
    })

# ========== RUTAS DE CONFIGURACIÓN ==========

@app.route('/api/config/blocked-apps', methods=['GET'])
def get_blocked():
    """Obtiene lista de apps bloqueadas."""
    return jsonify({'apps': get_blocked_apps()})

@app.route('/api/config/blocked-apps', methods=['POST'])
def add_app():
    """Agrega una app a la lista de bloqueadas."""
    data = request.json
    if 'app' not in data:
        return jsonify({'error': 'App name required'}), 400
    
    if add_blocked_app(data['app']):
        return jsonify({'success': True, 'message': f"App {data['app']} agregada"}), 201
    return jsonify({'error': 'App already exists'}), 409

@app.route('/api/config/blocked-apps/<app_name>', methods=['DELETE'])
def remove_app(app_name):
    """Elimina una app de la lista de bloqueadas."""
    if remove_blocked_app(app_name):
        return jsonify({'success': True, 'message': f"App {app_name} removida"}), 200
    return jsonify({'error': 'App not found'}), 404

@app.route('/api/config/settings', methods=['GET'])
def get_settings():
    """Obtiene la configuración actual."""
    settings = load_settings()
    # No devolver contraseña por seguridad
    if 'password' in settings:
        del settings['password']
    return jsonify(settings)

@app.route('/api/config/settings', methods=['PUT'])
def update_settings():
    """Actualiza la configuración."""
    data = request.json
    settings = load_settings()
    settings.update(data)
    save_settings(settings)
    return jsonify({'success': True, 'message': 'Settings actualizado'})

@app.route('/api/config/profiles', methods=['GET'])
def get_profiles():
    """Obtiene todos los perfiles."""
    settings = load_settings()
    return jsonify(settings['profiles'])

@app.route('/api/config/profile/<profile_name>', methods=['POST'])
def switch_profile(profile_name):
    """Cambia el perfil activo."""
    settings = load_settings()
    if profile_name not in settings['profiles']:
        return jsonify({'error': 'Profile not found'}), 404
    
    settings['current_profile'] = profile_name
    save_settings(settings)
    return jsonify({'success': True, 'message': f"Perfil cambiado a {profile_name}"})

# ========== RUTAS DE CONTROL ==========

@app.route('/api/control/enable', methods=['POST'])
def enable_guardian():
    """Activa Guardian."""
    settings = load_settings()
    settings['enabled'] = True
    save_settings(settings)
    return jsonify({'success': True, 'message': 'Guardian activado'})

@app.route('/api/control/disable', methods=['POST'])
def disable_guardian():
    """Desactiva Guardian."""
    password = request.json.get('password', '') if request.json else ''
    settings = load_settings()
    
    if settings.get('password') and settings['password'] != password:
        return jsonify({'error': 'Password incorrect'}), 403
    
    settings['enabled'] = False
    save_settings(settings)
    return jsonify({'success': True, 'message': 'Guardian desactivado'})

@app.route('/api/control/logs', methods=['GET'])
def get_logs():
    """Obtiene los logs."""
    days = request.args.get('days', 1, type=int)
    logs = read_logs(days)
    return jsonify({'logs': logs})


@app.route('/dashboard', methods=['GET'])
def dashboard_page():
    """Sirve el HTML del dashboard web."""
    html = get_dashboard_html()
    return html, 200, {'Content-Type': 'text/html; charset=utf-8'}


@app.route('/api/gamification', methods=['GET'])
def api_gamification():
    """Retorna datos de gamificación para el dashboard."""
    try:
        data = get_gamification_status()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ========== MANEJO DE ERRORES ==========

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Internal server error'}), 500

def start_api(port=5000):
    """Inicia el servidor API en un thread daemon."""
    def run():
        app.run(host='127.0.0.1', port=port, debug=False, use_reloader=False)
    
    thread = threading.Thread(target=run, daemon=True)
    thread.start()
    print(f"✓ API REST iniciada en http://127.0.0.1:{port}")

if __name__ == '__main__':
    start_api()
