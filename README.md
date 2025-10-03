# Sustainability Score API

A lightweight Flask API that computes sustainability scores for physical products based on materials, transport, packaging, and other environmental factors.

## Features

- **POST /score**: Calculate sustainability score with AI-powered suggestions
- **GET /history**: Retrieve recent product submissions
- **GET /score-summary**: Get aggregated statistics across all products
- Configurable scoring weights for GWP, Circularity, and Cost factors
- AI-powered insights using Google Gemini 1.5 Flash
- Input validation and error handling
- Unit tests included

## Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd case-study-2
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) Set Gemini API key for AI suggestions:
```bash
set GEMINI_API_KEY=your_api_key_here
```

4. Run the application:
```bash
python app.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### POST /score
Calculate sustainability score for a product.

**Request Body:**
```json
{
  "product_name": "Reusable Bottle",
  "materials": ["aluminum", "plastic"],
  "weight_grams": 300,
  "transport": "air",
  "packaging": "recyclable",
  "gwp": 5.0,
  "cost": 10.0,
  "circularity": 80.0,
  "weights": {
    "gwp_weight": 0.4,
    "circularity_weight": 0.3,
    "cost_weight": 0.3
  }
}
```

**Response:**
```json
{
  "product_name": "Reusable Bottle",
  "sustainability_score": 72.5,
  "rating": "B",
  "suggestions": ["Avoid air transport", "Use biodegradable packaging"]
}
```

### GET /history
Returns recent product submissions.

### GET /score-summary
Returns aggregated statistics:
```json
{
  "total_products": 12,
  "average_score": 68.3,
  "ratings": {"A": 2, "B": 5, "C": 4, "D": 1},
  "top_issues": ["Plastic used", "Air transport"]
}
```

## Scoring Logic

The sustainability score is calculated using:
- **GWP Impact** (40% default): Global Warming Potential penalty
- **Circularity** (30% default): Product circularity and end-of-life considerations
- **Cost Efficiency** (30% default): Economic sustainability factor

Additional penalties for:
- Unsustainable materials (plastic, styrofoam)
- High-impact transport methods (air transport)
- Non-recyclable packaging
- Excessive product weight

## Testing

Run unit tests:
```bash
python -m pytest tests/
```

Or run individual test files:
```bash
python tests/test_api.py
python tests/test_scorer.py
```

## Configuration

Modify scoring parameters in `config.py`:
- Material penalties/bonuses
- Transport impact factors
- Packaging sustainability ratings
- Weight thresholds
- Score rating boundaries

## Project Structure

```
case-study-2/
├── app.py                 # Main Flask application
├── config.py             # Scoring configuration
├── requirements.txt      # Dependencies
├── models/
│   └── schemas.py        # Data validation schemas
├── services/
│   ├── scorer.py         # Sustainability scoring logic
│   ├── ai_service.py     # AI-powered suggestions
│   └── storage.py        # In-memory data storage
├── routes/
│   ├── score_routes.py   # Score calculation endpoints
│   ├── history_routes.py # History endpoints
│   └── summary_routes.py # Summary statistics endpoints
└── tests/
    ├── test_api.py       # API endpoint tests
    └── test_scorer.py    # Scoring logic tests
```

## Example Usage

```bash
# Calculate score for a product
curl -X POST http://localhost:5000/score \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "Eco Bottle",
    "materials": ["bamboo", "glass"],
    "weight_grams": 250,
    "transport": "rail",
    "packaging": "biodegradable",
    "gwp": 2.0,
    "cost": 15.0,
    "circularity": 90.0
  }'

# Get submission history
curl http://localhost:5000/history

# Get summary statistics
curl http://localhost:5000/score-summary
```