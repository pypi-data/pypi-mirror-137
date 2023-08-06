# asynchronous_binance_client(asyncio and aiohttp)

This is an asynchronous library that is written for using binance services.

You need aiohttp and asyncio for delealing with methods and properties.


1- First instantiate from BinanceFuturesClient:

<pre><code>from binance_aiohttp.binance import BinanceFuturesClient
binance_client = BinanceFuturesClient(api_key, secret_key, testnet=False)</code></pre>


2 - Then from aiohttp.ClientSession:

<pre><code>async with aiohttp.ClientSession(json_serialize=ujson.dumps) as session:  </code></pre>


3- Finally await methods:

<pre><code>await binance_client.candlestick_data(session, 'BTCUSDT', interval='4h', limit=300)</code></pre>


## Example:

<pre><code>
import asyncio
import aiohttp
import ujson
from binance_aiohttp.binance import BinanceFuturesClient
binance_client = BinanceFuturesClient(api_key, secret_key, testnet=False)


async def fetch():
  async with aiohttp.ClientSession(json_serialize=ujson.dumps) as session:
    result = await asyncio.create_task(binance_client.candlestick_data(session, 'BTCUSDT', interval='4h', limit=300))
    print(result)


asyncio.run(fetch())
</code></pre>




