import json
import os

EXCHANGE_RATES_PATH = "src/data/exchange_rates.json"
BASE_CURRENCY_PATH = "src/data/base_currency.json"  # Zaktualizowana ścieżka

def load_exchange_rates():

    with open(EXCHANGE_RATES_PATH, 'r') as file:
        return json.load(file)

def save_exchange_rates(rates):

    with open(EXCHANGE_RATES_PATH, 'w') as file:
        json.dump(rates, file, indent=2)

def get_exchange_rate(from_currency, to_currency):

    if from_currency == to_currency:
        return 1.0
        
    rates = load_exchange_rates()
    try:
        return rates["rates"][from_currency][to_currency]
    except KeyError:
        raise ValueError(f"Exchange rate not found from {from_currency} to {to_currency}")

def convert_currency(amount, from_currency, to_currency):

    if from_currency == to_currency:
        return amount
    
    rate = get_exchange_rate(from_currency, to_currency)
    return round(amount * rate, 2)

def add_currency_rate(from_currency, to_currency, rate):

    rates = load_exchange_rates()
    
    if from_currency not in rates["rates"]:
        rates["rates"][from_currency] = {}
    
    if to_currency not in rates["rates"]:
        rates["rates"][to_currency] = {}
    
    rates["rates"][from_currency][to_currency] = rate
    rates["rates"][to_currency][from_currency] = round(1 / rate, 4)
    
    save_exchange_rates(rates)

def get_available_currencies():

    rates = load_exchange_rates()
    return list(rates["rates"].keys())

if __name__ == "__main__":

    print("Available currencies:", get_available_currencies())
    

    amount = 100
    from_curr = "EUR"
    to_curr = "PLN"
    result = convert_currency(amount, from_curr, to_curr)
    print(f"{amount} {from_curr} = {result} {to_curr}")
