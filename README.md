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
python manage.py makemigrations
python manage.py migrate
```

### 5. Start the development server
```bash
python manage.py runserver
```
The application will now be running at http://127.0.0.1:8000.

## Endpoints

### POST /api/advances/portfolio/
Uploads a client portfolio and calculates the maximum advance.

#### Request Parameters
- file: A CSV file containing the client portfolio with the required headers.
#### Response
- portfolio_id: The unique identifier for the portfolio.
- max_advance: The maximum amount that can be advanced.

### POST /api/advances/apply-loan/
Submits a loan request based on the portfolio data.

#### Request Parameters
- **loan_amount:** The amount requested for the loan.
- **portfolio_id:** The ID of the portfolio associated with the loan.
#### Response
- **loan_id:** The unique identifier for the loan.
- **state:** The status of the loan (APPROVED/REJECTED).
- **payment_schedule:** The repayment schedule for the loan.


### GET /api/advances/loan-status/{loan_id}/
Checks the status of the loan application.

#### Response
- **loan_id:** The ID of the loan.
- **state:** The status of the loan.
- **amount:** The requested loan amount.

## Technologies Used
- Django 5.1
- Django REST Framework (DRF)
- Pandas (for data processing and portfolio calculations)

## Assumptions

- Identifiers are used to support the management of multiple portfolios (companies) at the same time: Each portfolio submission returns a unique portfolio_id, loan applications require the associated portfolio_id and return a unique loan_id, the loan_id is used to fetch the loan status.
- The portfolio data should be provided in **CSV** format with the required headers.
- The repayment schedule is calculated using a factor rate of 1.2x the loan amount. The repayment period is fixed at 12 months.

## Technical decisions

### Data Processing with Pandas:

The use of Pandas simplifies processing portfolio data, allowing efficient calculation of metrics like average MRR and churn rate.

### DRF for API Development:

Django REST Framework provides a sustained structure for building the API endpoints.

### State Management:

Loans are tracked with states (PENDING, APPROVED, REJECTED), ensuring clarity in the application's workflow.

## Examples of Requests

### Example 1: Submit a Portfolio

```bash
curl -X POST http://127.0.0.1:8000/api/advances/portfolio/ \
-H "Content-Type: multipart/form-data" \
-F "file=@portfolio.csv"
```

#### Response

```json
{
    "portfolio": {
        "id": 1,
        "max_advance": 144000.00
    },
    "message": "The company is not eligible to ask for a loan based on the current data."
}
```

### Example 2: Apply for a loan

```bash
curl -X POST http://127.0.0.1:8000/api/advances/apply-loan/ \
-H "Content-Type: application/json" \
-d '{"loan_amount": 5000, "portfolio_id": 1}'
```

#### Response

```json
{
    "loan": {
        "id": 8,
        "amount": "100000",
        "state": "APPROVED",
        "repayment_schedule": [
            {
                "month": 1,
                "amount_due": "10000.0"
            },
            {
                "month": 2,
                "amount_due": "10000.0"
            },
            {
                "month": 12,
                "amount_due": "10000.0"
            }
        ]
    }
}
```

### Example 3: Get loan status

```bash
curl -X GET http://127.0.0.1:8000/api/advances/loan-status/10/
```

#### Response

```json
{
    "loan": {
        "id": 10,
        "amount": "120000.00",
        "state": "APPROVED"
    }
}
```