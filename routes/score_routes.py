from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from models.schemas import ProductSchema, WeightsSchema
from services.scorer import SustainabilityScorer
from services.ai_service import AIService
from services.storage import storage

score_bp = Blueprint('score', __name__)
product_schema = ProductSchema()
weights_schema = WeightsSchema()
ai_service = AIService()

@score_bp.route('/score', methods=['POST'])
def calculate_score():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        # Validate product data
        product_data = product_schema.load(data)
        
        # Get custom weights if provided
        weights = None
        if 'weights' in data:
            weights = weights_schema.load(data['weights'])
            weights_schema.validate_weights_sum(weights)
        
        # Calculate score
        score = SustainabilityScorer.calculate_score(product_data, weights)
        rating = SustainabilityScorer.get_rating(score)
        
        # Generate suggestions
        basic_suggestions = SustainabilityScorer.generate_suggestions(product_data, score)
        ai_suggestions = ai_service.generate_insights(product_data, score, rating)
        
        # Combine suggestions (prefer AI, fallback to basic)
        suggestions = ai_suggestions if ai_suggestions else basic_suggestions
        
        # Store submission
        submission = storage.add_submission(product_data, score, rating, suggestions)
        
        response = {
            'product_name': product_data['product_name'],
            'sustainability_score': round(score, 1),
            'rating': rating,
            'suggestions': suggestions
        }
        
        return jsonify(response), 200
        
    except ValidationError as e:
        return jsonify({'error': 'Validation failed', 'details': e.messages}), 400
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500