# SlotSnap – Smart Token Wait-Time Estimator

## Project Overview

SlotSnap is a backend REST API application developed using Python and FastAPI. It estimates how long a customer needs to wait before their token is served.

The application calculates estimated waiting time using the currently served token, target token, and average service duration.

It also supports dynamic average service-time calculation using historical records and handles skipped or cancelled tokens.

## Technologies Used

* Python
* FastAPI
* Uvicorn
* Pydantic
* Pytest
* HTTPX

## Features

* REST API development using FastAPI.
* Estimated customer waiting-time calculation.
* Current token management.
* Input validation and error handling.
* Dynamic average service-time calculation.
* Historical service-duration tracking.
* Skipped and cancelled token handling.
* Automated unit and API testing.
* Interactive API documentation using Swagger UI.

## Project Structure

```text
slotsnap/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── calculator.py
│   └── services.py
│
├── tests/
│   ├── test_calculator.py
│   └── test_api.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Navigate to the project

```bash
cd slotsnap
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the environment

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 6. Start the application

```bash
python -m uvicorn app.main:app --reload
```

## API Documentation

After starting the application, open:

http://127.0.0.1:8000/docs

Swagger UI provides interactive documentation for all available API endpoints.

## API Endpoints

| Method | Endpoint                   | Description                  |
| ------ | -------------------------- | ---------------------------- |
| GET    | /                          | Application homepage         |
| GET    | /current-token             | Get current token            |
| PUT    | /update-token/{new_token}  | Update current token         |
| POST   | /estimate                  | Calculate waiting time       |
| POST   | /service-duration          | Record service duration      |
| GET    | /average-service-time      | Calculate historical average |
| POST   | /skip-token/{token_number} | Skip or cancel a token       |

## Sample API Request

POST /estimate

```json
{
    "target_token": 15,
    "average_service_time": 6
}
```

## Sample API Response

```json
{
    "current_token": 10,
    "target_token": 15,
    "average_service_time": 6,
    "average_source": "Manually provided average",
    "skipped_tokens": [],
    "estimated_wait_minutes": 30
}
```

## Waiting-Time Calculation

Basic formula:

Estimated Waiting Time = (Target Token - Current Token) × Average Service Time

Skipped tokens are excluded from the number of service slots.

## Running Automated Tests

Execute:

```bash
python -m pytest -v
```

The project includes unit tests and API tests using Pytest.

## Future Improvements

* Persistent database integration.
* Real-time token updates.
* Historical service-time analytics.
* Improved waiting-time predictions using machine learning.
* Multi-service-provider support.

## Author

Abhinav Kante

GitHub: https://github.com/abhinav-kante
