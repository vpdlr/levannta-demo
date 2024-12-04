from advances.models import Loan, Portfolio
from advances.services.portfolio_service import calculate_max_advance, calculate_score_of_portfolio

def validate_loan_amount(loan_amount, max_loan_advance):
    """
    Validates if the loan amount is within the allowable limit.
    
    :param loan_amount: Requested loan amount.
    :param max_loan_advance: Maximum allowable loan amount.
    :return: (is_valid, error_message)
    """
    if loan_amount > max_loan_advance:
        return False, "Requested loan amount exceeds the maximum loan limit"
    return True, None

def check_loan_approval(portfolio_id):
    """
    Checks if the portfolio score meets the threshold for loan approval.
    
    :return: (is_approved, error_message)
    """
    threshold = 70
    score_data = calculate_score_of_portfolio(portfolio_id)

    if "error" in score_data:
        return False, "Loan application rejected due to error calculating score"

    score = score_data["score"]
    if score <= threshold:
        return False, "Loan application rejected due to insufficient portfolio score"
    return True, None

def create_loan(portfolio, loan_amount, state):
    """
    Creates a loan object with the given state.

    :param portfolio: Portfolio instance.
    :param loan_amount: Loan amount.
    :param state: Loan state (APPROVED or REJECTED).
    :return: Loan instance.
    """
    return Loan.objects.create(
        portfolio=portfolio,
        amount=loan_amount,
        state=state
    )

def generate_repayment_schedule(amount):
    """
    Generates a simple repayment schedule for the loan.
    """
    # Assume a factor rate of 1.2x and 12 months for simplicity
    factor_rate = 1.2
    months = 12
    monthly_payment = amount * factor_rate / months
    repayment_schedule = []

    for month in range(1, months + 1):
        repayment_schedule.append({
            'month': month,
            'amount_due': str(monthly_payment)
        })

    return repayment_schedule

def process_loan_application(portfolio_id, amount):
    try:
        portfolio = Portfolio.objects.get(id=portfolio_id)
        loan = create_loan(portfolio, amount, Loan.LoanState.PENDING)

        # Check loan approval
        is_approved, message = check_loan_approval(portfolio_id)
        if not is_approved:
            loan.state = Loan.LoanState.REJECTED
            loan.save()
            return {
                'loan': {
                    'id': loan.id,
                    'state': loan.state
                },
                'message': message
            }
        
        # Validate loan amount
        max_loan_advance, _ = calculate_max_advance(portfolio_id)
        is_valid, message = validate_loan_amount(amount, max_loan_advance)
        if not is_valid:
            loan.state = Loan.LoanState.REJECTED
            loan.save()
            return {
                'loan': {
                    'id': loan.id,
                    'state': loan.state
                },
                'message': message
            }
        
        loan.state = Loan.LoanState.APPROVED
        loan.save()
        repayment_schedule = generate_repayment_schedule(amount)

        return {
            'loan': {
                'id': loan.id,
                'amount': str(loan.amount),
                'state': loan.state,
                'repayment_schedule': repayment_schedule
            }
        }

    except Exception as e:
        print("error: ", e)
        return {'error': 'There was an error processing the loan application.'}

def get_loan_status(loan_id):
    """
    Retrieves the current status of a loan.
    """
    try:
        loan = Loan.objects.get(id=loan_id)

        return {
            'loan': {
                'id': loan_id,
                'amount': str(loan.amount),
                'state': loan.state
            }
        }

    except Loan.DoesNotExist:
        return {'error': 'Loan not found'}