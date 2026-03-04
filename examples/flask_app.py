#!/usr/bin/env python3
"""
Flask web application example with Kimi Authentication Bridge
"""

from flask import Flask, jsonify, render_template_string
from kimi_auth_bridge import KimiAuthBridge, KimiNotAuthenticatedError

app = Flask(__name__)
bridge = KimiAuthBridge()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Kimi Auth Bridge Demo</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
        .status { padding: 20px; border-radius: 8px; margin: 20px 0; }
        .authenticated { background: #d4edda; border: 1px solid #c3e6cb; }
        .not-authenticated { background: #f8d7da; border: 1px solid #f5c6cb; }
        code { background: #f4f4f4; padding: 2px 6px; border-radius: 3px; }
        .endpoint { background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>🌙 Kimi Device Auth Bridge</h1>
    
    <div class="status {{ 'authenticated' if authenticated else 'not-authenticated' }}">
        <h2>Status: {{ '✅ Authenticated' if authenticated else '❌ Not Authenticated' }}</h2>
        {% if authenticated %}
            <p><strong>Token:</strong> <code>{{ token_preview }}</code></p>
            <p><strong>API Base:</strong> <code>{{ api_base }}</code></p>
            <p><strong>Model:</strong> <code>{{ model }}</code></p>
        {% else %}
            <p>Please run <code>kimi login</code> in your terminal to authenticate.</p>
        {% endif %}
    </div>
    
    <h2>📡 API Endpoints</h2>
    
    <div class="endpoint">
        <h3>GET /api/status</h3>
        <p>Check authentication status</p>
    </div>
    
    <div class="endpoint">
        <h3>GET /api/token</h3>
        <p>Get access token (requires authentication)</p>
    </div>
    
    <div class="endpoint">
        <h3>GET /api/headers</h3>
        <p>Get complete auth headers (requires authentication)</p>
    </div>
    
    <footer style="margin-top: 50px; color: #666; font-size: 0.9em;">
        <p>Kimi Device Auth Bridge Example</p>
    </footer>
</body>
</html>
"""


@app.route('/')
def index():
    """Main page showing auth status"""
    return render_template_string(
        HTML_TEMPLATE,
        authenticated=bridge.is_authenticated(),
        token_preview=bridge.get_token_preview(),
        api_base=bridge.get_api_base(),
        model=bridge.get_default_model()
    )


@app.route('/api/status')
def api_status():
    """API endpoint for auth status"""
    return jsonify({
        'authenticated': bridge.is_authenticated(),
        'api_base': bridge.get_api_base(),
        'model': bridge.get_default_model(),
        'token_preview': bridge.get_token_preview()
    })


@app.route('/api/token')
def api_token():
    """API endpoint to get access token"""
    try:
        token = bridge.get_access_token()
        if not token:
            return jsonify({'error': 'Not authenticated'}), 401
        
        return jsonify({
            'token': token,
            'preview': bridge.get_token_preview()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/headers')
def api_headers():
    """API endpoint to get auth headers"""
    try:
        headers = bridge.get_auth_headers()
        return jsonify({'headers': headers})
    except KimiNotAuthenticatedError:
        return jsonify({'error': 'Not authenticated'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("🚀 Starting Flask app...")
    print("📍 Open http://localhost:5000")
    app.run(debug=True, port=5000)
