# School Recommendation Engine

A specialized microservice designed to rank educational institutions based on user preferences and historical performance data. The engine employs a hybrid scoring strategy that combines traditional weighted heuristics with a machine learning model that evolves through a continuous feedback loop.

---

## Features

- **Hybrid Scoring System**: Combines weighted heuristic scoring with ML-based predictions
- **Adaptive Learning**: Improves over time by learning from user interactions and feedback
- **Automated Retraining**: Scheduled model retraining using APScheduler
- **RESTful API**: FastAPI-based HTTP interface for recommendations and feedback
- **Fallback Mechanism**: Gracefully degrades to heuristic scoring when ML model is unavailable
- **Comprehensive Feature Engineering**: 17 different features including curriculum match, budget fit, distance, ratings, and more
- **Docker Support**: Containerized deployment ready

---

## Architecture

The system is built using:

- **FastAPI** for high-performance HTTP communication
- **Scikit-Learn** for predictive modeling (`RandomForestClassifier`)
- **APScheduler** for automated lifecycle management
- **Pandas / NumPy** for data processing

### Core Components

```text
┌─────────────────┐
│   FastAPI       │
│   (main.py)     │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
┌───▼───┐ ┌──▼─────────┐
│ Scoring│ │ Auto-Trainer│
│ Engine │ │ (Scheduler) │
└───┬───┘ └──┬─────────┘
    │         │
┌───▼────┐ ┌─▼──────────┐
│ ML     │ │ Feedback   │
│ Model  │ │ Store      │
└────────┘ └────────────┘
```

---

## Installation

### Prerequisites

- Python 3.11+
- pip

### Setup

#### 1. Clone the repository

```bash
git clone <repository-url>
cd Recommendation_Engine
```

#### 2. Install dependencies

```bash
pip install -r requirements.txt
```

#### 3. Set up environment variables (optional)

```bash
cp .env.example .env
# Edit .env with your configuration
```

#### 4. Create required directories

```bash
mkdir -p models data
```

---

## Configuration

The service can be configured via environment variables:

| Variable | Default | Description |
|---|---|---|
| `MODEL_PATH` | `models/recommender.pkl` | Path to ML model file |
| `FEEDBACK_PATH` | `data/feedback.csv` | Path to feedback storage |
| `TRAINING_DATA_PATH` | `data/training_dataset.csv` | Path to training dataset |
| `BACKEND_API_URL` | `http://localhost:5050` | Backend API URL for data fetching |
| `MIN_TRAINING_SAMPLES` | `100` | Minimum samples required for ML training |
| `RETRAIN_INTERVAL_HOURS` | `24` | Interval for automatic retraining |

---

## Usage

### Running the Service

#### Development

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Production

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

#### Docker

```bash
docker build -t recommendation-engine .
docker run -p 8000:8000 recommendation-engine
```

---

## API Endpoints

### Health Check

```http
GET /health
```

Returns service health status.

---

### Model Status

```http
GET /model-status
```

Returns current ML model status and training information.

---

### Get Recommendations

```http
POST /recommend
Content-Type: application/json
```

#### Request Body

```json
{
  "parent_id": 123,
  "preferences": {
    "curriculum": "British",
    "min_budget": 5000,
    "max_budget": 15000,
    "distance_km": 25.0,
    "lat": 40.7128,
    "lng": -74.0060,
    "school_type": "private",
    "school_level": "secondary"
  },
  "schools": [
    {
      "id": 1,
      "name": "Example School",
      "curriculum": "British",
      "tuition_fee": 10000,
      "rating": 4.5,
      "facilities": "library,sports,lab",
      "verification_status": "verified",
      "latitude": 40.7200,
      "longitude": -74.0100,
      "school_type": "private",
      "school_level": "secondary",
      "passing_rate": 85.0,
      "national_exam_score": 78.0
    }
  ]
}
```

---

### Submit Feedback

```http
POST /feedback
Content-Type: application/json
```

#### Request Body

```json
{
  "recommendation_id": 456,
  "parent_id": 123,
  "school_id": 1,
  "result": "opened"
}
```

---

### Manual Retraining

```http
POST /retrain
```

Manually triggers model retraining.

---

## Scoring Features

The engine uses 17 weighted features for school scoring:

| Feature | Weight | Description |
|---|---|---|
| Curriculum Match | 9% | Exact match with user preference |
| Budget Fit | 15% | Within user's budget range |
| Distance | 11% | Proximity to user's location |
| Rating | 10% | Overall school rating |
| Facilities | 5% | Number and quality of facilities |
| Verification Status | 4% | Whether school is verified |
| School Type | 5% | Match with preferred school type |
| Passing Rate | 5% | Academic performance metric |
| National Exam Score | 5% | Standardized test performance |
| Total Students | 1% | School size (logarithmic scaling) |
| Gender Balance | 1% | Gender distribution balance |
| Achievement Score | 5% | Normalized achievement metrics |
| Achievement Count | 3% | Number of achievements |
| Staff Quality | 5% | Teaching staff quality score |
| Follower Count | 4% | Social media presence |
| Review Count | 2% | Number of reviews |
| Total Achievement Score | 3% | Comprehensive achievement metric |

---

## Project Structure

```text
Recommendation_Engine/
├── app/
│   ├── main.py              # FastAPI application and endpoints
│   ├── model.py             # Scoring engine and ML model loading
│   ├── features.py          # Feature engineering functions
│   ├── trainer.py           # ML model training logic
│   ├── auto_trainer.py      # Automated training orchestration
│   ├── build_dataset.py     # Dataset acquisition and preparation
│   ├── feedback_store.py    # Feedback persistence
│   ├── schemas.py           # Pydantic data models
│   └── config.py            # Configuration management
├── models/                  # ML model storage
├── data/                    # Data storage (feedback, training datasets)
├── requirements.txt         # Python dependencies
├── dockerfile               # Docker configuration
└── README.md                # Project documentation
```

---

## ML Training Pipeline

The system features an automated training pipeline that:

1. Fetches training data from the backend API
2. Merges historical user feedback with training data
3. Trains a `RandomForestClassifier` with 100 estimators
4. Splits data into 80/20 training and validation sets
5. Persists the trained model to disk
6. Automatically retrains based on the configured interval

---

## Technology Stack

| Component | Technology |
|---|---|
| API Framework | FastAPI |
| Machine Learning | Scikit-Learn |
| Scheduling | APScheduler |
| Data Processing | Pandas, NumPy |
| Validation | Pydantic |
| Deployment | Docker |
| Language | Python 3.11+ |

---

## Future Improvements

- Add deep learning recommendation models
- Introduce collaborative filtering
- Real-time recommendation streaming
- Multi-language support
- Explainable AI scoring breakdown
- Advanced analytics dashboard

---

## License

TBD.

---
