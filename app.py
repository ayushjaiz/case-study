from flask import Flask, jsonify
from routes.score_routes import score_bp
from routes.history_routes import history_bp
from routes.summary_routes import summary_bp
from datetime import datetime

def create_app():
    app = Flask(__name__)
    
    # Health endpoint
    @app.route('/health', methods=['GET'])
    def health_check():
        """API health check endpoint"""
        return jsonify({
            'status': 'healthy',
            'message': 'API is running successfully',
            'timestamp': datetime.utcnow().isoformat(),
            'version': '1.0.0'
        }), 200
    
    app.register_blueprint(score_bp)
    app.register_blueprint(history_bp)
    app.register_blueprint(summary_bp)
    
    return app

# Create the app instance at module level for Gunicorn
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)