from rest_framework.views import APIView
from rest_framework.response import Response

class PortfolioView(APIView):
    def post(self, request):
        # logic
        return Response({"max_advance": 0})