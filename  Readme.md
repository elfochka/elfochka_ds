# ClickerMarket
### Приложение для создания платежных форм для товаров в системе Stripe

- Для создания образа запустить команду: `docker build -t clickomarket .`
- Далее вытянуть образ: docker pull `название_вашей_директории/clickomarket:clickomarket`
- И запустить контейнер с необходимыми ключами: `docker run -d -p 80:8000 --name clickomarket -e SECRET_KEY=ваш_секретный_код -e DEBUG=True/False STRIPE_PUBLIC_KEY=pk_test STRIPE_SECRET_KEY=sk_test название_вашей_директории/clickomarket:clickomarket`
