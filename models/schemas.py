from marshmallow import Schema, fields, validate, ValidationError
from pydantic import BaseModel, Field
from typing import List

class ProductSchema(Schema):
    product_name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    materials = fields.List(fields.Str(), required=True, validate=validate.Length(min=1))
    weight_grams = fields.Float(required=True, validate=validate.Range(min=0.1))
    transport = fields.Str(required=True, validate=validate.OneOf(['air', 'truck', 'ship', 'rail', 'local']))
    packaging = fields.Str(required=True, validate=validate.OneOf(['non-recyclable', 'recyclable', 'biodegradable', 'reusable']))
    gwp = fields.Float(required=True, validate=validate.Range(min=0))
    cost = fields.Float(required=True, validate=validate.Range(min=0))
    circularity = fields.Float(required=True, validate=validate.Range(min=0, max=100))

class WeightsSchema(Schema):
    gwp_weight = fields.Float(validate=validate.Range(min=0, max=1), missing=0.4)
    circularity_weight = fields.Float(validate=validate.Range(min=0, max=1), missing=0.3)
    cost_weight = fields.Float(validate=validate.Range(min=0, max=1), missing=0.3)
    
    def validate_weights_sum(self, data, **_):
        total = data.get('gwp_weight', 0.4) + data.get('circularity_weight', 0.3) + data.get('cost_weight', 0.3)
        if abs(total - 1.0) > 0.01:
            raise ValidationError("Weights must sum to 1.0")

# Pydantic model for AI structured output
class SuggestionsList(BaseModel):
    """List of sustainability suggestions from AI using structured output"""
    suggestions: List[str] = Field(
        ..., 
        description="List of 2-3 specific actionable suggestions to improve sustainability", 
        min_length=2, 
        max_length=3
    )