import logging
from datetime import datetime, timedelta

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken

#from ..services.ai_service import AIService
# TODO: remove PennyWise\budget\services
from budget.views.tools.ai_service import AIService
from ..utils.get_financial_data import get_user_financial_data
logger = logging.getLogger(__name__)


class FinancialRecommendationView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        try:
            if not request.user.is_authenticated:
                return Response(
                    {"error": "Authentication credentials were not provided."},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

        except InvalidToken as e:
            return Response(
                {"error": "Invalid token", "detail": str(e)},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        except Exception as e:
            return Response(
                {"error": "Server error", "detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")
        user_question = request.query_params.get("question")

        if not user_question:
           # ERROR_COUNTER.labels('missing_question', 'FinancialRecommendationView').inc()
            return Response(
                {"error": "Question parameter is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # TODO refactor this somehow
        start_date = (
            datetime.strptime(start_date, "%Y-%m-%d").date()
            if start_date
            else datetime.now().date() - timedelta(days=365)
        )
        end_date = (
            datetime.strptime(end_date, "%Y-%m-%d").date()
            if end_date
            else datetime.now().date()
        )

        financial_data = get_user_financial_data(request.user, start_date, end_date)

        ai_recommendation = AIService().get_recommendation(
            financial_data, user_question
        )

        logger.info(f"{ai_recommendation}")

        return Response(
            {
                "question": user_question,
                "financial_data": financial_data,
                "recommendation": ai_recommendation,
            }
        )
