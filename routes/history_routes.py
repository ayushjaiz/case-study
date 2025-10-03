from flask import Blueprint, jsonify
from services.storage import storage

history_bp = Blueprint('history', __name__)

@history_bp.route('/history', methods=['GET'])
def get_history():
    try:
        recent_submissions = storage.get_recent_submissions()
        return jsonify(recent_submissions), 200
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve history', 'details': str(e)}), 500