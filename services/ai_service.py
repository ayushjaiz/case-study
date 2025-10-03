from google import genai
import os
from models.schemas import SuggestionsList

class AIService:
    def __init__(self):
        """Initialize the Google Gen AI client for structured output."""
        self.client = genai.Client(api_key=os.getenv('GEMINI_API_KEY', 'demo-key'))

    def generate_suggestions(self, product_data, score, rating):
        """
        Generate sustainability suggestions using structured output.
        Returns list of suggestions as strings.
        """
        prompt = f"""
        Analyze this product sustainability data and provide 2-3 specific, actionable suggestions to improve sustainability.
        
        Product Analysis:
        - Product: {product_data['product_name']}
        - Materials: {', '.join(product_data['materials'])}
        - Weight: {product_data['weight_grams']}g
        - Transport: {product_data['transport']}
        - Packaging: {product_data['packaging']}
        - GWP: {product_data['gwp']}
        - Cost: {product_data['cost']}
        - Circularity: {product_data['circularity']}%
        - Sustainability Score: {score:.1f}/100 (Rating: {rating})
        
        Each suggestion should be:
        - Specific and actionable
        - Under 50 characters for clarity
        - Focused on the most impactful improvements
        
        Examples: "Use recycled materials", "Switch to rail transport", "Reduce packaging"
        """
        
        try:
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config={
                    'response_mime_type': 'application/json',
                    'response_schema': SuggestionsList,
                }
            )
            return response.parsed.suggestions
        except Exception:
            # Fallback to basic suggestions
            return [
                "Use eco-friendly materials",
                "Optimize transportation",
                "Improve packaging sustainability"
            ]