import logging
import os

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_gigachat.chat_models import GigaChat

from .prompt_builder import AIPromptBuilder


logger = logging.getLogger(__name__)
load_dotenv()


class AIService:
    def __init__(self):
        self.token = os.getenv("AI_TOKEN")

    def get_recommendation(self, financial_data, question):
        giga = GigaChat(
            credentials=self.token,
            verify_ssl_certs=False,
        )
        prompt = AIPromptBuilder.build_financial_advise_prompt(financial_data, question)

        messages = [SystemMessage(content=prompt)]
        messages.append(HumanMessage(content=question))

        try:
            res = giga.invoke(messages)
        except Exception as e:
            logger.error(f"Error getting GigaChat recommendation: {str(e)}")
            return "Не удалось получить рекомендации. Пожалуйста, попробуйте позже."

        return list(res)[0][1].replace("\n", "")
