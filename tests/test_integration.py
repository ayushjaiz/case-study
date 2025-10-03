import unittest
import json
import os
from unittest.mock import patch
from app import create_app

class TestStructuredOutputIntegration(unittest.TestCase):
    """Integration tests for the structured output functionality"""
    
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True
    
    def test_complete_workflow_with_structured_output(self):
        """Test the complete workflow from API request to structured output response"""
        # Sample product matching the required format
        product_data = {
            "product_name": "Reusable Bottle",
            "materials": ["aluminum", "plastic"],
            "weight_grams": 300,
            "transport": "ship",
            "packaging": "recyclable",
            "gwp": 5.0,
            "cost": 10.0,
            "circularity": 80.0
        }
        
        # Make the API request
        response = self.client.post('/score', 
                                  data=json.dumps(product_data),
                                  content_type='application/json')
        
        # Verify successful response
        self.assertEqual(response.status_code, 200)
        
        # Parse the response
        result = json.loads(response.data)
        
        # Verify the response matches the exact required format
        expected_format = {
            "product_name": "Reusable Bottle",
            "sustainability_score": "numeric_value",  # Will be actual number
            "rating": "letter_grade",  # Will be A, B, C, or D
            "suggestions": ["suggestion1", "suggestion2"]  # List of strings
        }
        
        # Check structure
        self.assertIn('product_name', result)
        self.assertIn('sustainability_score', result)
        self.assertIn('rating', result)
        self.assertIn('suggestions', result)
        
        # Verify types and values
        self.assertEqual(result['product_name'], "Reusable Bottle")
        self.assertIsInstance(result['sustainability_score'], (int, float))
        self.assertIn(result['rating'], ['A', 'B', 'C', 'D'])
        self.assertIsInstance(result['suggestions'], list)
        self.assertGreaterEqual(len(result['suggestions']), 2)
        self.assertLessEqual(len(result['suggestions']), 3)
        
        # Verify suggestions are AI-generated strings (not empty or default)
        for suggestion in result['suggestions']:
            self.assertIsInstance(suggestion, str)
            self.assertGreater(len(suggestion.strip()), 0)
        
        print(f"✅ Structured output test passed!")
        print(f"Response format: {json.dumps(result, indent=2)}")
    
    def test_ai_suggestions_are_contextual(self):
        """Test that AI suggestions are contextual to the product data"""
        # Test with a product that has clear improvement areas
        high_gwp_product = {
            "product_name": "High Impact Product",
            "materials": ["plastic", "steel"],
            "weight_grams": 1000,
            "transport": "air",  # High impact transport
            "packaging": "non-recyclable",  # Poor packaging
            "gwp": 15.0,  # High GWP
            "cost": 5.0,
            "circularity": 20.0  # Low circularity
        }
        
        response = self.client.post('/score', 
                                  data=json.dumps(high_gwp_product),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data)
        
        # The score should be low due to poor sustainability metrics
        self.assertLess(result['sustainability_score'], 60)
        self.assertIn(result['rating'], ['C', 'D'])
        
        # Suggestions should be present and meaningful
        self.assertIsInstance(result['suggestions'], list)
        self.assertGreaterEqual(len(result['suggestions']), 2)
        
        print(f"✅ Contextual suggestions test passed!")
        print(f"Low-scoring product got suggestions: {result['suggestions']}")

if __name__ == '__main__':
    unittest.main()