# Levannta Demo Project

This is a demo project for Levannta, built with Django and DRF. The project simulates the process of requesting an advance based on a subscription portfolio and includes the following functionality:

- Submit a portfolio of clients.
- Apply for a loan based on the portfolio.
- Retrieve the status of the loan application.

## Setup Instructions

### Prerequisites
- Python 3.11.x (or higher)
- pip (for managing dependencies)

### 1. Clone the repository
```bash
git clone https://github.com/vpdlr/levannta-demo.git
cd levannta_demo
```

### 2. Set up a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run migrations
```bash
python manage.py migrate
```

### 5. Start the development server
```bash
python manage.py runserver
```
The application will now be running at http://127.0.0.1:8000.

## Endpoints

### POST /api/advances/portfolio
Uploads a client portfolio and calculates the maximum advance.

### POST /api/advances/apply-loan
Submits a loan request based on the portfolio data.

### GET /api/advances/loan-status
Checks the status of the loan application.

## Technologies Used
- Django 5.1
- Django REST Framework (DRF)

