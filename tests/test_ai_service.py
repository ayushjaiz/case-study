import unittest
import os
from unittest.mock import patch, MagicMock
from services.ai_service import AIService

class TestAIService(unittest.TestCase):
    def setUp(self):
        self.ai_service = AIService()
        self.sample_product = {
            'product_name': 'Reusable Bottle',
            'materials': ['aluminum', 'plastic'],
            'weight_grams': 300,
            'transport': 'ship',
            'packaging': 'recyclable',
            'gwp': 5.0,
            'cost': 10.0,
            'circularity': 80.0
        }
    
    def test_ai_service_initialization(self):
        """Test that AIService initializes correctly"""
        self.assertIsNotNone(self.ai_service.client)
    
    @patch.dict(os.environ, {'GEMINI_API_KEY': 'test-key'})
    def test_generate_suggestions_fallback(self):
        """Test that fallback suggestions are returned when API fails"""
        # This will use the fallback since we don't have a real API key
        suggestions = self.ai_service.generate_suggestions(
            self.sample_product, 72.5, 'B'
        )
        
        self.assertIsInstance(suggestions, list)
        self.assertGreaterEqual(len(suggestions), 2)
        self.assertLessEqual(len(suggestions), 3)
        
        # Check that all suggestions are strings
        for suggestion in suggestions:
            self.assertIsInstance(suggestion, str)
            self.assertGreater(len(suggestion), 0)
    
    @patch('services.ai_service.genai.Client')
    def test_generate_suggestions_success(self, mock_client_class):
        """Test successful API response with structured output"""
        # Mock the client and response
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        
        # Mock the response with parsed suggestions
        mock_response = MagicMock()
        mock_response.parsed.suggestions = [
            "Avoid air transport",
            "Use biodegradable packaging"
        ]
        
        mock_client.models.generate_content.return_value = mock_response
        
        # Create a new AI service instance with mocked client
        ai_service = AIService()
        suggestions = ai_service.generate_suggestions(
            self.sample_product, 72.5, 'B'
        )
        
        self.assertEqual(suggestions, ["Avoid air transport", "Use biodegradable packaging"])
        
        # Verify the client was called with correct parameters
        mock_client.models.generate_content.assert_called_once()
        call_args = mock_client.models.generate_content.call_args
        
        self.assertEqual(call_args[1]['model'], 'gemini-2.5-flash')
        self.assertEqual(call_args[1]['config']['response_mime_type'], 'application/json')
        self.assertIn('Reusable Bottle', call_args[1]['contents'])
    
    def test_generate_suggestions_response_format(self):
        """Test that suggestions match expected format"""
        suggestions = self.ai_service.generate_suggestions(
            self.sample_product, 72.5, 'B'
        )
        
        # Verify response format matches expected output
        self.assertIsInstance(suggestions, list)
        
        # Check that suggestions are reasonable length (under 50 chars as specified)
        for suggestion in suggestions:
            self.assertIsInstance(suggestion, str)
            self.assertLess(len(suggestion), 60)  # Allow some buffer
            self.assertGreater(len(suggestion), 5)  # Should be meaningful

if __name__ == '__main__':
    unittest.main()