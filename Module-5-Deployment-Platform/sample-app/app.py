#!/usr/bin/env python3
"""
Sample Flask Application for Bob Deployment Workshop
A simple web application to demonstrate automated deployment
"""

from flask import Flask, jsonify, render_template_string
import os
import socket
from datetime import datetime

app = Flask(__name__)

# HTML template for the home page
HOME_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sample Flask App - Bob Workshop</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            padding: 40px;
            max-width: 600px;
            width: 100%;
        }
        h1 {
            color: #667eea;
            margin-bottom: 10px;
            font-size: 2.5em;
        }
        .subtitle {
            color: #666;
            margin-bottom: 30px;
            font-size: 1.1em;
        }
        .info-box {
            background: #f8f9fa;
            border-left: 4px solid #667eea;
            padding: 15px;
            margin: 15px 0;
            border-radius: 5px;
        }
        .info-label {
            font-weight: bold;
            color: #667eea;
            margin-bottom: 5px;
        }
        .info-value {
            color: #333;
            font-family: 'Courier New', monospace;
        }
        .status {
            display: inline-block;
            background: #10b981;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            margin-top: 20px;
        }
        .footer {
            text-align: center;
            margin-top: 30px;
            color: #999;
            font-size: 0.9em;
        }
        .api-link {
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
            text-decoration: none;
            margin-top: 20px;
            transition: background 0.3s;
        }
        .api-link:hover {
            background: #764ba2;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Sample Flask App</h1>
        <p class="subtitle">Bob Deployment Workshop</p>
        
        <div class="info-box">
            <div class="info-label">Hostname:</div>
            <div class="info-value">{{ hostname }}</div>
        </div>
        
        <div class="info-box">
            <div class="info-label">Environment:</div>
            <div class="info-value">{{ environment }}</div>
        </div>
        
        <div class="info-box">
            <div class="info-label">Deployed At:</div>
            <div class="info-value">{{ timestamp }}</div>
        </div>
        
        <div class="info-box">
            <div class="info-label">Version:</div>
            <div class="info-value">{{ version }}</div>
        </div>
        
        <span class="status">✓ Running</span>
        
        <div style="text-align: center;">
            <a href="/health" class="api-link">Check Health</a>
            <a href="/api/info" class="api-link">API Info</a>
        </div>
        
        <div class="footer">
            Deployed with Bob Deployment Platform
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    """Home page with application information"""
    return render_template_string(
        HOME_TEMPLATE,
        hostname=socket.gethostname(),
        environment=os.environ.get('ENVIRONMENT', 'production'),
        timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        version=os.environ.get('APP_VERSION', '1.0.0')
    )

@app.route('/health')
def health():
    """Health check endpoint for Kubernetes probes"""
    return jsonify({
        'status': 'healthy',
        'service': 'sample-flask-app',
        'timestamp': datetime.now().isoformat(),
        'hostname': socket.gethostname()
    }), 200

@app.route('/api/info')
def info():
    """API endpoint with application information"""
    return jsonify({
        'application': 'Sample Flask App',
        'version': os.environ.get('APP_VERSION', '1.0.0'),
        'environment': os.environ.get('ENVIRONMENT', 'production'),
        'hostname': socket.gethostname(),
        'timestamp': datetime.now().isoformat(),
        'endpoints': {
            'home': '/',
            'health': '/health',
            'info': '/api/info'
        }
    }), 200

@app.route('/api/echo/<message>')
def echo(message):
    """Echo endpoint for testing"""
    return jsonify({
        'message': message,
        'timestamp': datetime.now().isoformat(),
        'hostname': socket.gethostname()
    }), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
