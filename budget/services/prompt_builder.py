
class AIPromptBuilder:
    def __init__(self):
        pass

    def build_financial_advise_prompt(financial_data, question):
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

                Напоминаю, вот вопрос: {question}
                """