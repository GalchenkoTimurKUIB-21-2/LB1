import requests
from datetime import datetime, timedelta

# URL API НБУ
BASE_URL = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange"


# Функція для отримання курсу валют за певну дату
def get_exchange_rate(date, currencies=None):
    formatted_date = date.strftime("%Y%m%d")  # Формат дати: YYYYMMDD
    params = {"date": formatted_date, "json": ""}  # Параметри запиту
    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        if currencies:
            # Фільтруємо тільки вибрані валюти
            data = [rate for rate in data if rate["cc"] in currencies]
        return data
    else:
        print(f"Помилка: {response.status_code}")
        return None


# Отримання курсу за попередній тиждень
def get_last_week_rates(currencies=None):
    today = datetime.now()
    last_week = [today - timedelta(days=i) for i in range(1, 8)]  # Дати за останній тиждень

    all_rates = {}
    for date in last_week:
        rates = get_exchange_rate(date, currencies)
        if rates:
            all_rates[date.strftime("%Y-%m-%d")] = rates
    return all_rates


# Основна функція
if __name__ == "__main__":
    print(
        "Введіть коди валют через кому (наприклад, USD, EUR, PLN). Якщо залишити порожнім, будуть показані всі валюти.")
    user_input = input("Введіть валюти: ").strip()

    # Обробка введених валют
    currencies = [currency.strip().upper() for currency in user_input.split(",")] if user_input else None

    rates_last_week = get_last_week_rates(currencies)

    for date, rates in rates_last_week.items():
        print(f"Дата: {date}")
        for rate in rates:
            print(f"  {rate['txt']} ({rate['cc']}): {rate['rate']}")
        print()
