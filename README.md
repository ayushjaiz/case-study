# SUSTAINABILITY SCORING API

#### This project focuses on Product Sustainability Assessment System that evaluates environmental impact of physical products with AI-powered recommendations using structured output.

## Table of Contents

- [Project Features](#project-features)
- [Tech Stack](#tech-stack)
- [Libraries Used](#libraries-used)
- [Setup and Installation](#setup-and-installation)
- [Environment Variables](#environment-variables)
- [API Endpoints and Sample Requests](#api-endpoints-and-sample-requests)
- [Development Choices](#development-choices)
- [Testing](#testing)
- [Acknowledgements](#acknowledgements)

---

## Project Features

- **Sustainability Scoring**: Calculate comprehensive sustainability scores based on materials, transport, packaging, and environmental factors
- **AI-Powered Suggestions**: Generate contextual improvement recommendations using Google Gemini with structured output
- **Product History**: Track and retrieve historical product submissions and scores
- **Analytics Dashboard**: View aggregated statistics and trends across all assessed products
- **Configurable Weights**: Customize scoring weights for GWP, Circularity, and Cost factors
- **Input Validation**: Robust data validation with detailed error handling

---

## Tech Stack

- **Backend**: Python, Flask
- **AI Integration**: Google Gemini 2.5 Flash with Structured Output
- **Data Storage**: In-memory storage (easily extendable to databases)
- **Testing**: PyTest, unittest

---

## Libraries Used

- **Flask**: Lightweight web framework for REST API development
- **google-genai**: Google Gemini API client for AI-powered structured output
- **marshmallow**: Data serialization and validation
- **pydantic**: Data validation and settings management with type hints
- **pytest**: Testing framework for comprehensive test coverage
- **gunicorn**: WSGI HTTP server for production deployment

---

## Setup and Installation

### Prerequisites

- Python 3.8+
- pip
- Google Gemini API Key (optional, for AI suggestions)

### Environment Variables

Create a `.env` file in the root directory:

```env
GEMINI_API_KEY=your_gemini_api_key_here
FLASK_ENV=development
```

### Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/ayushjaiz/case-study
   cd case-study-2
   ```

2. **Create Virtual Environment**:
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**:
   ```bash
   python app.py
   ```

- API service starts running at `http://localhost:5000`

---

## API Endpoints and Sample Requests

### POST /score
Calculate sustainability score and get AI-powered suggestions.

**Request:**
```json
{
  "product_name": "Reusable Bottle",
  "materials": ["aluminum", "plastic"],
  "weight_grams": 300,
  "transport": "ship",
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
Retrieve recent product submissions and their scores.

**Response:**
```json
[
  {
    "id": 1,
    "product_name": "Reusable Bottle",
    "sustainability_score": 72.5,
    "rating": "B",
    "timestamp": "2025-01-04T10:30:00Z"
  }
]
```

### GET /score-summary
Get aggregated analytics across all products.

**Response:**
```json
{
  "total_products": 12,
  "average_score": 68.3,
  "ratings": {"A": 2, "B": 5, "C": 4, "D": 1},
  "top_issues": ["Plastic materials", "Air transport", "Non-recyclable packaging"]
}
```

---

## Development Choices

### Why Python Flask?

- Lightweight and flexible for API development
- Excellent ecosystem for data processing and AI integration
- Easy deployment and scaling options
- Strong community support

### Why Google Gemini with Structured Output?

- Latest AI technology with reliable structured responses
- Built-in validation and type safety
- Consistent JSON output format
- Cost-effective compared to other AI services

### Why Pydantic for Data Validation?

- Type safety and runtime validation
- Automatic JSON schema generation
- Integration with modern Python type hints
- Better error messages for debugging

### Why In-Memory Storage?

- Fast read/write operations for prototyping
- No external database dependencies
- Easy to replace with persistent storage (PostgreSQL, MongoDB)
- Sufficient for current scale requirements

---

## Architecture

### Scoring Algorithm

The sustainability score is calculated using a weighted combination of:

1. **GWP Impact** (40% default): Global Warming Potential assessment
2. **Circularity Score** (30% default): End-of-life and recyclability factors
3. **Cost Efficiency** (30% default): Economic sustainability considerations

### AI Integration

- Uses Google Gemini 2.5 Flash with structured output
- Generates 2-3 contextual improvement suggestions
- Fallback to rule-based suggestions if AI is unavailable
- Structured output ensures consistent response format

### Project Structure

```
case-study-2/
├── app.py                    # Main Flask application
├── config.py                # Scoring configuration and constants
├── requirements.txt         # Python dependencies
├── models/
│   └── schemas.py           # Pydantic/Marshmallow schemas
├── services/
│   ├── ai_service.py        # AI-powered suggestions with structured output
│   ├── scorer.py            # Sustainability scoring logic
│   └── storage.py           # Data storage layer
├── routes/
│   ├── score_routes.py      # Score calculation endpoints
│   ├── history_routes.py    # Historical data endpoints
│   └── summary_routes.py    # Analytics and summary endpoints
└── tests/
    ├── test_api.py          # API integration tests
    ├── test_ai_service.py   # AI service unit tests
    ├── test_scorer.py       # Scoring logic tests
    └── test_integration.py  # End-to-end integration tests
```

---

## Testing

Run the complete test suite:
```bash
python -m pytest tests/ -v
```

Run specific test categories:
```bash
# API endpoint tests
python -m pytest tests/test_api.py -v

# AI service tests
python -m pytest tests/test_ai_service.py -v

# Integration tests
python -m pytest tests/test_integration.py -v
```

Test coverage includes:
- API endpoint functionality
- Data validation and error handling
- Scoring algorithm accuracy
- AI service integration and fallbacks
- End-to-end workflow validation

---

## Acknowledgements

This project was completed with the assistance of various online resources and documentation:

- Google Gemini API Documentation for structured output implementation
- Flask Documentation for web framework best practices
- Pydantic Documentation for data validation patterns

### What was the challenging part of the assignment?

- **AI Integration**: Implementing reliable AI suggestions with proper fallback mechanisms and structured output validation