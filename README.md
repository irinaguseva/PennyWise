# API для управления личным бюджетом 💸

Приложение позволяет 
* создавать записи о пользовательских доходах и расходах;
* получать отчёты по каждой категории за выбранный период;
* запрашивать индивидуальную рекомендацию от AI, основанную на ваших доходах и расходах.

##### Основные ручки

docker-compose build
docker-compose up

docker-compose exec web python manage.py makemigration
docker-compose exec web python manage.py migrate

docker-compose exec web python manage.py createsuperuser

Сваггер доступен по ссылке http://127.0.0.1:8000/swagger/

Примеры использования приложения с помощью Postman.
1) Получение access-токена из ручки /api/token с именем и паролем суперпользователя в body
2) Получение сметы по доходам и расходам в конкретной категории из ручки /api/transactions/balance/
3) Получение рекомендации от AI-сервиса (GigaChat) из ручки 
 
Есть возможность сгенерировать транзакции посредством скрипта get_or_create_category_and_make_transaction с указанием любой категории в независимости от её наличия, пользователем и типом транзакции.








