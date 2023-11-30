import asyncio
import logging
import aiohttp
import aiofile
from aiopath import AsyncPath
import websockets
from websockets import WebSocketServerProtocol
from websockets.exceptions import ConnectionClosedOK
from datetime import datetime, timedelta


logging.basicConfig(level=logging.INFO)
CURRENCY = ["EUR", "USD"]
FILE_NAME = "exchange_log.txt"

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
        exc, = list(filter(lambda element: element["currency"] == currency_code, rates))
        return f"{currency_code}: buy: {exc['purchaseRateNB']}, sale: {exc['saleRateNB']}. Date: {date}"
    return "Failed to retrieve date"

# Get exchange information during amount of varible "days"
async def get_exchange_with_day(currency_code, days: int):
    #day_now = datetime.now() - timedelta(days=1) #DO DUE TO THE NIGHT
    day_now = datetime.now() 
    time_difference = timedelta(days=1)
    results = []
    for _ in range(days):
        result = await get_exchange(currency_code, day_now.strftime("%d.%m.%Y"))
        results.append(result)
        day_now -= time_difference
    return '\n'.join(results)

# Check if number of days fits our characteristics
def check_days(days: str):
    if not days.isdigit() or int(days) < 0 or int(days) > 10:
        return False
    return True

# Write logging imformation (exchange) to the file
async def log_exchange_command():
    log_file_path = AsyncPath(FILE_NAME)
    async with await aiofile.async_open(log_file_path, 'a') as afp:
        await afp.write(f"{datetime.now()} - Exchange command executed\n")


class Server:
    clients = set()

    async def register(self, ws: WebSocketServerProtocol):
        self.clients.add(ws)
        logging.info(f'{ws.remote_address} connects')

    async def unregister(self, ws: WebSocketServerProtocol):
        self.clients.remove(ws)
        logging.info(f'{ws.remote_address} disconnects')

    async def send_to_clients(self, message: str):
        if self.clients:
            [await client.send(message) for client in self.clients]

    async def ws_handler(self, ws: WebSocketServerProtocol):
        await self.register(ws)
        try:
            await self.distrubute(ws)
        except ConnectionClosedOK as err:
            logging.error(err)
        finally:
            await self.unregister(ws)

    async def distrubute(self, ws: WebSocketServerProtocol):
        async for message in ws:
            if message.startswith("exchange"):
                await log_exchange_command()
                if message == "exchange":
                    for i in CURRENCY:
                        m = await get_exchange(i, datetime.now().strftime("%d.%m.%Y"))
                        await self.send_to_clients(m)
                else:
                    res = message.split( )
                    number = res[1]
                    if check_days(number):
                        for currency in CURRENCY:
                            m = await get_exchange_with_day(currency, int(number))
                            await self.send_to_clients(m)
                    else:
                        logging.error("Impossible number of days")
            else:
                await self.send_to_clients(f"{message}")

# Start the program
async def main():
    server = Server()
    async with websockets.serve(server.ws_handler, 'localhost', 8080):
        await asyncio.Future()  # run forever

if __name__ == '__main__':
    asyncio.run(main())