import unittest
import json
from app import create_app

class TestSustainabilityAPI(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True
        
        self.sample_product = {
            "product_name": "Test Bottle",
            "materials": ["aluminum", "plastic"],
            "weight_grams": 300,
            "transport": "air",
            "packaging": "recyclable",
            "gwp": 5.0,
            "cost": 10.0,
            "circularity": 80.0
        }
    
    def test_score_endpoint_success(self):
        response = self.client.post('/score', 
                data=json.dumps(self.sample_product),
                content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        # Check required fields are present
        self.assertIn('product_name', data)
        self.assertIn('sustainability_score', data)
        self.assertIn('rating', data)
        self.assertIn('suggestions', data)
        
        # Verify data types and formats
        self.assertIsInstance(data['product_name'], str)
        self.assertIsInstance(data['sustainability_score'], (int, float))
        self.assertIsInstance(data['rating'], str)
        self.assertIsInstance(data['suggestions'], list)
        
        # Check value ranges
        self.assertGreaterEqual(data['sustainability_score'], 0)
        self.assertLessEqual(data['sustainability_score'], 100)
        self.assertIn(data['rating'], ['A', 'B', 'C', 'D'])
        self.assertGreaterEqual(len(data['suggestions']), 2)
        self.assertLessEqual(len(data['suggestions']), 3)
        
        # Verify suggestions are meaningful strings
        for suggestion in data['suggestions']:
            self.assertIsInstance(suggestion, str)
            self.assertGreater(len(suggestion), 5)
    
    def test_score_endpoint_invalid_data(self):
        invalid_product = self.sample_product.copy()
        del invalid_product['product_name']
        
        response = self.client.post('/score',
                                  data=json.dumps(invalid_product),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 400)
    
    def test_history_endpoint(self):
        # First add a product
        self.client.post('/score',
                        data=json.dumps(self.sample_product),
                        content_type='application/json')
        
        # Then get history
        response = self.client.get('/history')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
    
    def test_summary_endpoint(self):
        response = self.client.get('/score-summary')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('total_products', data)
        self.assertIn('average_score', data)
        self.assertIn('ratings', data)
        self.assertIn('top_issues', data)
    
    def test_response_format_matches_requirement(self):
        """Test that the response format exactly matches the required format"""
        sample_product = {
            "product_name": "Reusable Bottle",
            "materials": ["aluminum", "plastic"],
            "weight_grams": 300,
            "transport": "ship",
            "packaging": "recyclable",
            "gwp": 5.0,
            "cost": 10.0,
            "circularity": 80.0
        }
        
        response = self.client.post('/score', 
                data=json.dumps(sample_product),
                content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        # Verify the response has exactly the required keys
        expected_keys = {'product_name', 'sustainability_score', 'rating', 'suggestions'}
        self.assertEqual(set(data.keys()), expected_keys)
        
        # Verify the expected format structure
        self.assertEqual(data['product_name'], "Reusable Bottle")
        self.assertIsInstance(data['sustainability_score'], (int, float))
        self.assertIsInstance(data['rating'], str)
        self.assertIsInstance(data['suggestions'], list)
        
        # Test with a different product name to ensure it's dynamic
        different_product = sample_product.copy()
        different_product['product_name'] = "Eco Cup"
        
        response2 = self.client.post('/score', 
                data=json.dumps(different_product),
                content_type='application/json')
        
        data2 = json.loads(response2.data)
        self.assertEqual(data2['product_name'], "Eco Cup")

if __name__ == '__main__':
    unittest.main()