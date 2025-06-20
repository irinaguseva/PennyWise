# API для управления личным бюджетом 💸

Приложение позволяет 
* создавать записи о пользовательских доходах и расходах;
* получать отчёты по каждой категории за выбранный период;
* запрашивать индивидуальную рекомендацию от AI, основанную на ваших доходах и расходах.

Сваггер доступен по ссылке http://127.0.0.1:8000/swagger/

#### Примеры использования приложения с помощью Postman
1) Получение access-токена из ручки /api/token с именем и паролем суперпользователя в body
   
   ![Снимок экрана (196)](https://github.com/user-attachments/assets/11fdd683-8ca2-4bd2-92bd-7c088f5c34a2)
   
2) Получение сметы по доходам и расходам в конкретной категории из ручки /api/transactions/balance/
   
   ![Снимок экрана (197)](https://github.com/user-attachments/assets/09512f8d-ae5e-4564-ac5c-d5004f3945ec)
   
3) Получение рекомендации от AI-сервиса (GigaChat) из ручки /api/transactions/recommendations
   
   ![Снимок экрана (198)](https://github.com/user-attachments/assets/59bad764-82b1-4934-b8d4-99622bf800c4)

Есть возможность сгенерировать транзакции посредством скрипта get_or_create_category_and_make_transaction с указанием любой категории в независимости от её наличия, пользователем и типом транзакции.

##### Инструкция по локальному запуску проекта
```
docker-compose build
docker-compose up
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```








