import logging

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_gigachat.chat_models import GigaChat

from secret import token

logger = logging.getLogger(__name__)


class AIService:
    def __init__(self):
        self.token = token

    def build_prompt(selfself, financial_data, question):
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

    def get_recommendation(self, financial_data, question):
        giga = GigaChat(
            credentials=self.token,
            verify_ssl_certs=False,
        )
        prompt = self.build_prompt(financial_data, question)

        messages = [SystemMessage(content=prompt)]
        messages.append(HumanMessage(content="Каковы мои расходы?"))

        try:
            res = giga.invoke(messages)
        except Exception as e:
            logger.error(f"Error getting GigaChat recommendation: {str(e)}")
            return "Не удалось получить рекомендации. Пожалуйста, попробуйте позже."

        return list(res)[0][1].replace("\n", "")
