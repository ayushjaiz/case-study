import unittest
from services.scorer import SustainabilityScorer

class TestSustainabilityScorer(unittest.TestCase):
    def setUp(self):
        self.sample_product = {
            'product_name': 'Test Product',
            'materials': ['aluminum'],
            'weight_grams': 300,
            'transport': 'ship',
            'packaging': 'recyclable',
            'gwp': 5.0,
            'cost': 10.0,
            'circularity': 80.0
        }
    
    def test_calculate_score(self):
        score = SustainabilityScorer.calculate_score(self.sample_product)
        self.assertIsInstance(score, float)
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)
    
    def test_get_rating(self):
        self.assertEqual(SustainabilityScorer.get_rating(85), 'A')
        self.assertEqual(SustainabilityScorer.get_rating(70), 'B')
        self.assertEqual(SustainabilityScorer.get_rating(50), 'C')
        self.assertEqual(SustainabilityScorer.get_rating(30), 'D')
    

    def test_material_penalties(self):
        plastic_product = self.sample_product.copy()
        plastic_product['materials'] = ['plastic']
        
        aluminum_product = self.sample_product.copy()
        aluminum_product['materials'] = ['aluminum']
        
        plastic_score = SustainabilityScorer.calculate_score(plastic_product)
        aluminum_score = SustainabilityScorer.calculate_score(aluminum_product)
        
        self.assertLess(plastic_score, aluminum_score)

if __name__ == '__main__':
    unittest.main()