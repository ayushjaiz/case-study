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
        self.assertIn('sustainability_score', data)
        self.assertIn('rating', data)
        self.assertIn('suggestions', data)
    
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

if __name__ == '__main__':
    unittest.main()