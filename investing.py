import os
import random

import pygame

try:
    from PIL import Image
except ImportError:
    Image = None

CRYPTO_DEFINITIONS = [
    {"name": "Bitcoin", "symbol": "BTC", "base_price": 42000.0, "image_file": "Bitcoin.png"},
    {"name": "Ethereum", "symbol": "ETH", "base_price": 2400.0, "image_file": "ethereum.png"},
    {"name": "Solana", "symbol": "SOL", "base_price": 110.0, "image_file": "solana.png"},
    {"name": "Cardano", "symbol": "ADA", "base_price": 0.75, "image_file": "Cardano.png"},
    {"name": "Ripple", "symbol": "XRP", "base_price": 0.65, "image_file": "Ripple.png"},
    {"name": "Dogecoin", "symbol": "DOGE", "base_price": 0.18, "image_file": "Dogecoin.png"},
    {"name": "Avalanche", "symbol": "AVAX", "base_price": 38.0, "image_file": "Avalanche.png"},
    {"name": "Polkadot", "symbol": "DOT", "base_price": 8.2, "image_file": "Polkadot.png"},
    {"name": "Chainlink", "symbol": "LINK", "base_price": 17.0, "image_file": "Chainlink.jpg"},
    {"name": "Litecoin", "symbol": "LTC", "base_price": 92.0, "image_file": "Litecoin.jpg"},
    {"name": "Toncoin", "symbol": "TON", "base_price": 6.8, "image_file": "Toncoin.png"},
    {"name": "Shiba Inu", "symbol": "SHIB", "base_price": 0.000028, "image_file": "Shiba_Inu.png"},
    {"name": "Monero", "symbol": "XMR", "base_price": 165.0, "image_file": "Monero.png"},
]

MAX_HISTORY_SECONDS = 3600
PRICE_UPDATE_INTERVAL = 1.0
MARKET_VISIBLE_ITEMS = 5
PORTFOLIO_VISIBLE_ITEMS = 5

current_prices = {crypto["symbol"]: crypto["base_price"] for crypto in CRYPTO_DEFINITIONS}
price_histories = {crypto["symbol"]: [crypto["base_price"]] for crypto in CRYPTO_DEFINITIONS}
owned_crypto = {crypto["symbol"]: 0.0 for crypto in CRYPTO_DEFINITIONS}
market_timer = 0.0
crypto_images = {}


def load_crypto_images():
    images_dir = os.path.join(os.path.dirname(__file__), "Images")

    for crypto in CRYPTO_DEFINITIONS:
        image_path = os.path.join(images_dir, crypto["image_file"])
        if os.path.exists(image_path):
            crypto_images[crypto["symbol"]] = load_image_surface(image_path, crypto["symbol"])
        else:
            crypto_images[crypto["symbol"]] = create_placeholder_surface(crypto["symbol"])


def load_image_surface(image_path, symbol):
    try:
        return pygame.image.load(image_path).convert_alpha()
    except pygame.error:
        if Image is None:
            return create_placeholder_surface(symbol)

        try:
            pil_image = Image.open(image_path).convert("RGBA")
            image_bytes = pil_image.tobytes()
            return pygame.image.fromstring(image_bytes, pil_image.size, "RGBA").convert_alpha()
        except Exception:
            return create_placeholder_surface(symbol)


def create_placeholder_surface(symbol):
    surface = pygame.Surface((128, 128), pygame.SRCALPHA)
    pygame.draw.circle(surface, (58, 94, 145), (64, 64), 60)
    pygame.draw.circle(surface, (235, 235, 235), (64, 64), 60, 3)

    font = pygame.font.SysFont("Arial", 34, bold=True)
    label = font.render(symbol[:4], True, (255, 255, 255))
    label_rect = label.get_rect(center=(64, 64))
    surface.blit(label, label_rect)
    return surface


def get_crypto_image(symbol):
    return crypto_images.get(symbol)


def get_crypto_definition(symbol):
    for crypto in CRYPTO_DEFINITIONS:
        if crypto["symbol"] == symbol:
            return crypto
    raise ValueError(f"Unknown cryptocurrency: {symbol}")


def get_display_rows():
    rows = []
    for crypto in CRYPTO_DEFINITIONS:
        symbol = crypto["symbol"]
        quantity = owned_crypto[symbol]
        price = current_prices[symbol]
        rows.append(
            {
                "name": crypto["name"],
                "symbol": symbol,
                "price": price,
                "owned": quantity,
                "value": quantity * price,
                "image": get_crypto_image(symbol),
            }
        )
    return rows


def get_owned_rows():
    rows = []
    for row in get_display_rows():
        if row["owned"] > 0:
            rows.append(row)
    return rows


def get_total_crypto_value():
    total_value = 0.0
    for symbol, quantity in owned_crypto.items():
        total_value += quantity * current_prices[symbol]
    return total_value


def update_market(dt):
    global market_timer
    market_timer += dt

    while market_timer >= PRICE_UPDATE_INTERVAL:
        market_timer -= PRICE_UPDATE_INTERVAL
        for crypto in CRYPTO_DEFINITIONS:
            symbol = crypto["symbol"]
            current_price = current_prices[symbol]
            movement = random.uniform(-0.025, 0.025)
            new_price = max(0.000001, current_price * (1.0 + movement))
            current_prices[symbol] = new_price

            history = price_histories[symbol]
            history.append(new_price)
            if len(history) > MAX_HISTORY_SECONDS:
                history.pop(0)


def buy_crypto(symbol, game_data, quantity=1.0):
    price = current_prices[symbol]
    total_cost = price * quantity
    if game_data.money < total_cost:
        return False

    game_data.money -= total_cost
    owned_crypto[symbol] += quantity
    return True


def get_max_affordable_quantity(symbol, game_data):
    price = current_prices[symbol]
    if price <= 0:
        return 0.0

    max_quantity = game_data.money / price
    return max(0.0, round((max_quantity), 2))


def sell_crypto(symbol, game_data, quantity):
    if quantity <= 0:
        return False

    if owned_crypto[symbol] < quantity:
        return False

    total_value = current_prices[symbol] * quantity
    owned_crypto[symbol] -= quantity
    game_data.money += total_value
    return True


def get_price_history(symbol):
    return price_histories[symbol]


def load_state(saved_prices, saved_history, saved_owned):
    global market_timer
    for crypto in CRYPTO_DEFINITIONS:
        symbol = crypto["symbol"]
        current_prices[symbol] = float(saved_prices.get(symbol, crypto["base_price"]))

        raw_history = saved_history.get(symbol, [current_prices[symbol]])
        parsed_history = [float(value) for value in raw_history][-MAX_HISTORY_SECONDS:]
        if not parsed_history:
            parsed_history = [current_prices[symbol]]
        price_histories[symbol] = parsed_history

        owned_crypto[symbol] = float(saved_owned.get(symbol, 0.0))

    market_timer = 0.0


load_crypto_images()
