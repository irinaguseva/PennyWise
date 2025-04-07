import json
import logging
from datetime import datetime, timedelta

import requests
from django.db.models import Sum
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_gigachat.chat_models import GigaChat
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

from budget.models import Category, Transaction
from secrets import giga_secret

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
            return Response(
                {"error": "Question parameter is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

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

        financial_data = self._get_user_financial_data(
            request.user, start_date, end_date
        )
        prompt = self._build_ai_prompt(financial_data, user_question)

        ai_recommendation = self._get_gigachat_recommendation(prompt)

        logger.info(f"{ai_recommendation}")

        return Response(
            {
                "question": user_question,
                "financial_data": financial_data,
                "recommendation": ai_recommendation,
            }
        )

    def _get_user_financial_data(self, user, start_date, end_date):

        income = (
            Transaction.objects.filter(
                user=user,
                type=Transaction.INCOME,
                date__gte=start_date,
                date__lte=end_date,
            ).aggregate(total=Sum("amount"))["total"]
            or 0
        )

        expenses = (
            Transaction.objects.filter(
                user=user,
                type=Transaction.EXPENSE,
                date__gte=start_date,
                date__lte=end_date,
            ).aggregate(total=Sum("amount"))["total"]
            or 0
        )

        balance = income - expenses

        categories = Category.objects.filter(user=user)
        category_expenses = []

        for category in categories:
            amount = (
                Transaction.objects.filter(
                    user=user,
                    category=category,
                    type=Transaction.EXPENSE,
                    date__gte=start_date,
                    date__lte=end_date,
                ).aggregate(total=Sum("amount"))["total"]
                or 0
            )

            if amount > 0:
                category_expenses.append(
                    {
                        "category": category.name,
                        "amount": float(amount),
                        "percentage": (
                            float(amount) / float(expenses) * 100 if expenses else 0
                        ),
                    }
                )

        return {
            "balance": float(balance),
            "income": float(income),
            "expenses": float(expenses),
            "category_expenses": sorted(
                category_expenses, key=lambda x: x["amount"], reverse=True
            ),
            "period": {
                "start_date": start_date.strftime("%Y-%m-%d"),
                "end_date": end_date.strftime("%Y-%m-%d"),
            },
        }

    def _build_ai_prompt(self, financial_data, question):
        return f"""
        Ты финансовый помощник. Пользователь спрашивает: "{question}".

        Вот финансовая информация пользователя:
        - Текущий баланс: {financial_data['balance']} руб.
        - Доходы за период: {financial_data['income']} руб.
        - Расходы за период: {financial_data['expenses']} руб.

        Основные категории расходов:
        {', '.join([f"{cat['category']} ({cat['percentage']:.1f}%)" for cat in financial_data['category_expenses']])}

        Дай конкретные рекомендации на русском языке, основанные на этих данных. 
        Будь дружелюбным и профессиональным. Если нужно сократить расходы, предложи конкретные категории.
        """

    def _get_gigachat_recommendation(self, prompt):
        giga = GigaChat(
            credentials=giga_secret,
            verify_ssl_certs=False,
        )

        messages = [SystemMessage(content=prompt)]

        messages.append(HumanMessage(content="Каковы мои расходы?"))
        res = giga.invoke(messages)
        return list(res)[0][1].replace("\n", "")
