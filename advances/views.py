from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .services.portfolio_service import process_and_calculate_max_advance
from .services.loan_service import process_loan_application, get_loan_status
from .serializers import PortfolioFileSerializer

# POST /portfolio - Receives the portfolio data (CSV format) and returns max advance
@api_view(['POST'])
def portfolio(request):
    # Validate file upload using DRF serializer
    serializer = PortfolioFileSerializer(data=request.data)
    if serializer.is_valid():
        csv_file = serializer.validated_data['file']
        
        # Process the CSV file and calculate the maximum advance
        try:
            portfolio_processing_results = process_and_calculate_max_advance(csv_file)
            return Response(portfolio_processing_results, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# POST /apply-loan - Emulates applying for the loan based on the portfolio data
@api_view(['POST'])
def apply_loan(request):
    portfolio_id = request.data.get('portfolio_id')
    loan_amount = request.data.get('loan_amount')

    if not portfolio_id or not loan_amount:
        return Response({'detail': 'Both portfolio_id and loan_amount are required.'}, status=status.HTTP_400_BAD_REQUEST)

    application_result = process_loan_application(portfolio_id, loan_amount)
    
    if 'error' in application_result:
        return Response(application_result, status=status.HTTP_400_BAD_REQUEST)

    return Response(application_result, status=status.HTTP_200_OK)

# GET /loan-status - Retrieves the loan status
@api_view(['GET'])
def loan_status(request, loan_id):
    status_result = get_loan_status(loan_id)
    
    if "error" in status_result:
        return Response(status_result, status=status.HTTP_404_NOT_FOUND)

    return Response(status_result, status=status.HTTP_200_OK)
