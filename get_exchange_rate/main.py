import aiohttp
import logging
import asyncio
from datetime import datetime, timedelta
import sys

result_of_search = []
POSIBLE_CURRENCY = ["CHF", "GBP", "PLZ", "SEK", "UAH", "XAU", "CAD"]

# Make request (to make an HTTP GET request)
async def request(url: str):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as resp:
                if resp.status == 200:
                    r = await resp.json()
                    return r
        except aiohttp.ClientConnectionError as err:
            logging.error(f"Connection error: {str(err)}")
            return None

# Get exchange information in this day    
async def get_exchange(currency_code: str, date:str):
    result = await request(f'https://api.privatbank.ua/p24api/exchange_rates?json&date={date}')
    if result:
        rates = result.get("exchangeRate")
        filted_rates = list(filter(lambda element: element["currency"] == currency_code, rates))
        if filted_rates:
            exc, = filted_rates
            return {'Currency':currency_code, 'buy': exc['purchaseRateNB'], 'sale': exc['saleRateNB'], 'Date': date}
    return "Failed to retrieve date"

# Check if number of days fits our characteristics
def check_days(days: str):
    if not days.isdigit() or int(days) < 0 or int(days) > 10:
        return False
    return True

# Get exchange information during amount of varible "days"
def get_exchange_with_day(currency_code, days:int):
    day_now = datetime.now() 
    #day_now = datetime.now() - timedelta(days=1) DO DUE TO THE NIGHT
    time_diference = timedelta(days=1)
    index = 0
    while index < days:
        result = asyncio.run(get_exchange(currency_code, day_now.strftime("%d.%m.%Y")))
        write_to_result_list(result['Date'], result['Currency'], result['sale'], result['buy'])
        print(result)
        index += 1
        day_now -= time_diference

# Write result of exchange in the list
def write_to_result_list(data, currency_code, sale, purchase):
    for i in range(len(result_of_search)):
        if data in result_of_search[i]:
            result_of_search[i][data][currency_code] = {'sale': sale, 'purchase': purchase}
            return
    result_of_search.append({data: {currency_code: {'sale': sale, 'purchase': purchase}}})

# Make ability to ask exchange information of addional currency
def addition_currency(argv):
    if len(argv) == 3 and check_days(argv[1]):
        if argv[2] in POSIBLE_CURRENCY:
            get_exchange_with_day(argv[2], int(argv[1]))
        else: return
    else: return

# Main function 
def main():
    currency = ["EUR", "USD"]
    if len(sys.argv) > 1 and check_days(sys.argv[1]):
        for one_currency in currency:
            get_exchange_with_day(one_currency, int(sys.argv[1]))
    addition_currency(sys.argv)
    
# Start of the program
if __name__ == "__main__":
    main()
    print("Here is result of the search:\n")
    print(result_of_search) 