from flask import Blueprint, jsonify
from services.storage import storage

summary_bp = Blueprint('summary', __name__)

@summary_bp.route('/score-summary', methods=['GET'])
def get_score_summary():
    try:
        summary_stats = storage.get_summary_stats()
        return jsonify(summary_stats), 200
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve summary', 'details': str(e)}), 500