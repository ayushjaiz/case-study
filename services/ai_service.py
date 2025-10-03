import google.generativeai as genai
import os

class AIService:
    def __init__(self):
        genai.configure(api_key=os.getenv('GEMINI_API_KEY', 'demo-key'))
        self.model = genai.GenerativeModel('gemini-2.5-flash')
    
    def generate_insights(self, product_data, score, rating):
        prompt = f"""
        Analyze this product sustainability data and provide 2-3 actionable insights:
        
        Product: {product_data['product_name']}
        Materials: {', '.join(product_data['materials'])}
        Weight: {product_data['weight_grams']}g
        Transport: {product_data['transport']}
        Packaging: {product_data['packaging']}
        GWP: {product_data['gwp']}
        Cost: {product_data['cost']}
        Circularity: {product_data['circularity']}%
        
        Sustainability Score: {score:.1f}/100 (Rating: {rating})
        
        Provide specific, actionable suggestions to improve sustainability. Keep each suggestion under 10 words.
        """
        
        try:
            response = self.model.generate_content(prompt)
            suggestions = response.text.strip().split('\n')
            return [s.strip('- ').strip() for s in suggestions if s.strip()][:3]
        except (ConnectionError, TimeoutError, ValueError):
            return [
                "Consider eco-friendly material alternatives",
                "Optimize transportation method", 
                "Improve packaging sustainability"
            ]