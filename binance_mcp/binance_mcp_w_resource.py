import datetime
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP
import requests

THIS_FOLDER = Path(__file__).parent.absolute()
ACTIVITY_LOG_FILE = THIS_FOLDER / "activity.log"

mcp = FastMCP("Binance MCP")


def get_symbol_from_name(name: str) -> str:
    if name.lower() in ('bitcoin', 'btc'):
        return 'BTCUSDT'
    elif name.lower() in ('ethereum', 'eth'):
        return 'ETHUSDT'
    else:
        return name.upper()


@mcp.tool()
def get_price(symbol: str) -> Any:
    """
    Get the current price of a crypto asset from Binance

    Args:
        symbol (str): The symbol of the crypto asset to get the price of

    Returns:
        Any: The current price of the crypto asset
    """

    symbol = get_symbol_from_name(symbol)
    url = f'http://api.binance.com/api/v3/ticker/price?symbol={symbol}'
    response = requests.get(url)
    

    if response.status_code != 200:
        with open(ACTIVITY_LOG_FILE, "a") as f:
            f.write(
                f"Error getting price change for {symbol}: {response.status_code} {response.text}"
            )
            # response.raise_for_status() # raise exception if something went wrong
            raise Exception(
                f"Error getting price change for {symbol}: {response.status_code} {response.text}"
            )
    else:
        price = response.json()["price"]
        with open(ACTIVITY_LOG_FILE, "a") as f:
            f.write(
                f"Successfully got price change for {symbol}. Current price is {price}. Current time is {datetime.datetime.now()}"
            )
        return f"The current price of {symbol} is {price}"


@mcp.tool()
def get_price_price_change(symbol: str) -> Any:
    """
    Get the 24-hour price fluctuation of a crypto asset from Binance

    Args:
        symbol (str): The symbol of the crypto asset to get the 24-hour price fluctuation of

    Returns:
        Any: The 24-hour price fluctuation of the crypto asset
    """
    symbol = get_symbol_from_name(symbol)
    url = f'http://api.binance.com/api/v3/ticker/24hr?symbol={symbol}'
    response = requests.get(url)
    response.raise_for_status() # raise exception if something went wrong
    return response.json()['priceChange']

@mcp.resource("file://activity.log")
def activity_log() -> str:
    with open(ACTIVITY_LOG_FILE, "r") as f:
        return f.read()

@mcp.resource("resource://crypto_price/{symbol}")
def get_crypto_price(symbol: str) -> str:
    return get_price(symbol)


if __name__ == '__main__':
    if not Path(ACTIVITY_LOG_FILE).exists():
        Path(ACTIVITY_LOG_FILE).touch()
    mcp.run(transport="stdio")












# from typing import Any

# import requests
# from mcp.server.fastmcp import FastMCP

# mcp = FastMCP("Binance MCP")


# def get_symbol_from_name(name: str) -> str:
#     if name.lower() in ["bitcoin", "btc"]:
#         return "BTCUSDT"
#     elif name.lower() in ["ethereum", "eth"]:
#         return "ETHUSDT"
#     else:
#         return name.upper()


# @mcp.tool()
# def get_price(symbol: str) -> Any:
#     """
#     Get the current price of a crypto asset from Binance

#     Args:
#         symbol (str): The symbol of the crypto asset to get the price of

#     Returns:
#         Any: The current price of the crypto asset
#     """
#     symbol = get_symbol_from_name(symbol)
#     url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
#     response = requests.get(url)
#     response.raise_for_status()
#     return response.json()


# @mcp.tool()
# def get_price_price_change(symbol: str) -> Any:
#     """
#     Get the price change of the last 24 hours of a crypto asset from Binance

#     Args:
#         symbol (str): The symbol of the crypto asset to get the price change of

#     Returns:
#         Any: The price change of the crypto asset in the last 24 hours
#     """
#     symbol = get_symbol_from_name(symbol)
#     url = f"https://data-api.binance.vision/api/v3/ticker/24hr?symbol={symbol}"
#     response = requests.get(url)
#     response.raise_for_status()
#     return response.json()


# if __name__ == "__main__":
#     print("Starting Binance MCP")
#     mcp.run(transport="stdio")
