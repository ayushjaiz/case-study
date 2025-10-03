# API Test Requests

## Start the Server First
```bash
python app.py
```
The server will run on `http://localhost:5000`

## 1. POST /score - Calculate Sustainability Score

### Basic Product Request
```bash
curl -X POST http://localhost:5000/score \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "Reusable Water Bottle",
    "materials": ["aluminum", "plastic"],
    "weight_grams": 300,
    "transport": "air",
    "packaging": "recyclable",
    "gwp": 5.0,
    "cost": 10.0,
    "circularity": 80.0
  }'
```

### Eco-Friendly Product
```bash
curl -X POST http://localhost:5000/score \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "Bamboo Coffee Cup",
    "materials": ["bamboo", "glass"],
    "weight_grams": 150,
    "transport": "rail",
    "packaging": "biodegradable",
    "gwp": 1.5,
    "cost": 8.0,
    "circularity": 95.0
  }'
```

### High-Impact Product
```bash
curl -X POST http://localhost:5000/score \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "Disposable Container",
    "materials": ["styrofoam", "plastic"],
    "weight_grams": 800,
    "transport": "air",
    "packaging": "non-recyclable",
    "gwp": 25.0,
    "cost": 50.0,
    "circularity": 10.0
  }'
```

### Product with Custom Weights
```bash
curl -X POST http://localhost:5000/score \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "Solar Panel",
    "materials": ["aluminum", "glass"],
    "weight_grams": 2000,
    "transport": "ship",
    "packaging": "recyclable",
    "gwp": 15.0,
    "cost": 200.0,
    "circularity": 70.0,
    "weights": {
      "gwp_weight": 0.5,
      "circularity_weight": 0.3,
      "cost_weight": 0.2
    }
  }'
```

## 2. GET /history - Get Recent Submissions

```bash
curl -X GET http://localhost:5000/history
```

## 3. GET /score-summary - Get Summary Statistics

```bash
curl -X GET http://localhost:5000/score-summary
```

## Error Testing

### Missing Required Field
```bash
curl -X POST http://localhost:5000/score \
  -H "Content-Type: application/json" \
  -d '{
    "materials": ["aluminum"],
    "weight_grams": 300,
    "transport": "air",
    "packaging": "recyclable",
    "gwp": 5.0,
    "cost": 10.0,
    "circularity": 80.0
  }'
```

### Invalid Transport Method
```bash
curl -X POST http://localhost:5000/score \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "Test Product",
    "materials": ["aluminum"],
    "weight_grams": 300,
    "transport": "teleportation",
    "packaging": "recyclable",
    "gwp": 5.0,
    "cost": 10.0,
    "circularity": 80.0
  }'
```

### Invalid Weight Sum
```bash
curl -X POST http://localhost:5000/score \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "Test Product",
    "materials": ["aluminum"],
    "weight_grams": 300,
    "transport": "ship",
    "packaging": "recyclable",
    "gwp": 5.0,
    "cost": 10.0,
    "circularity": 80.0,
    "weights": {
      "gwp_weight": 0.6,
      "circularity_weight": 0.3,
      "cost_weight": 0.3
    }
  }'
```

## Expected Response Formats

### Successful Score Response
```json
{
  "product_name": "Reusable Water Bottle",
  "sustainability_score": 72.5,
  "rating": "B",
  "suggestions": [
    "Avoid air transport - use ground or sea shipping",
    "Replace plastic with sustainable alternatives",
    "Consider materials with lower Global Warming Potential"
  ]
}
```

### History Response
```json
[
  {
    "id": 1,
    "timestamp": "2025-10-03T10:30:00",
    "product_name": "Reusable Water Bottle",
    "materials": ["aluminum", "plastic"],
    "weight_grams": 300,
    "transport": "air",
    "packaging": "recyclable",
    "gwp": 5.0,
    "cost": 10.0,
    "circularity": 80.0,
    "sustainability_score": 72.5,
    "rating": "B",
    "suggestions": ["Avoid air transport", "Replace plastic"]
  }
]
```

### Summary Response
```json
{
  "total_products": 3,
  "average_score": 68.3,
  "ratings": {
    "A": 1,
    "B": 1,
    "D": 1
  },
  "top_issues": [
    "Air transport",
    "Plastic/Styrofoam used",
    "High GWP materials"
  ]
}
```

### Error Response
```json
{
  "error": "Validation failed",
  "details": {
    "product_name": ["Missing data for required field."]
  }
}
```

## Material Options
- aluminum, steel, plastic, glass, wood, bamboo, cardboard, styrofoam

## Transport Options  
- air, truck, ship, rail, local

## Packaging Options
- non-recyclable, recyclable, biodegradable, reusable

## Rating Scale
- A: 80-100 (Excellent)
- B: 60-79 (Good) 
- C: 40-59 (Average)
- D: 0-39 (Poor)