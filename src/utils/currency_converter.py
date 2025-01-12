import json
import os

EXCHANGE_RATES_PATH = "src/data/exchange_rates.json"
BASE_CURRENCY_PATH = "src/data/base_currency.json"  # Zaktualizowana ścieżka

def load_exchange_rates():
    """
    从文件加载汇率
    """
    with open(EXCHANGE_RATES_PATH, 'r') as file:
        return json.load(file)

def save_exchange_rates(rates):
    """
    将汇率保存到文件
    """
    with open(EXCHANGE_RATES_PATH, 'w') as file:
        json.dump(rates, file, indent=2)

def get_exchange_rate(from_currency, to_currency):
    """
    从文件中获取汇率
    """
    if from_currency == to_currency:
        return 1.0
        
    rates = load_exchange_rates()
    try:
        return rates["rates"][from_currency][to_currency]
    except KeyError:
        raise ValueError(f"找不到从 {from_currency} 到 {to_currency} 的汇率")

def convert_currency(amount, from_currency, to_currency):
    """
    将一种货币转换为另一种货币
    """
    if from_currency == to_currency:
        return amount
    
    rate = get_exchange_rate(from_currency, to_currency)
    return round(amount * rate, 2)

def add_currency_rate(from_currency, to_currency, rate):
    """
    添加新的汇率到文件
    """
    rates = load_exchange_rates()
    
    # 如果第一种货币不存在，则添加
    if from_currency not in rates["rates"]:
        rates["rates"][from_currency] = {}
    
    # 如果第二种货币不存在，则添加
    if to_currency not in rates["rates"]:
        rates["rates"][to_currency] = {}
    
    # 双向添加汇率
    rates["rates"][from_currency][to_currency] = rate
    rates["rates"][to_currency][from_currency] = round(1 / rate, 4)
    
    save_exchange_rates(rates)

def get_available_currencies():
    """
    返回可用货币列表
    """
    rates = load_exchange_rates()
    return list(rates["rates"].keys())

# 使用示例
if __name__ == "__main__":
    # 检查可用货币
    print("可用货币:", get_available_currencies())
    
    # 转换示例
    amount = 100
    from_curr = "EUR"
    to_curr = "PLN"
    result = convert_currency(amount, from_curr, to_curr)
    print(f"{amount} {from_curr} = {result} {to_curr}")
