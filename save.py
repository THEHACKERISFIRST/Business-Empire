import json
import os

import business
import game_data
import investing
from paths import writable_path

SAVE_FILE_PATH = writable_path("save_data.json")


def get_net_worth():
    return game_data.money + business.get_business_asset_value() + investing.get_total_crypto_value()


def get_stats_lines():
    return [
        f"Net Worth: {game_data.format_number(get_net_worth(), 1)}",
        f"Cash: {game_data.format_number(game_data.money, 1)}",
        f"Income / Second: {game_data.format_number(game_data.money_per_second, 1)}",
        f"Money / Click: {game_data.format_number(game_data.money_per_click, 1)}",
    ]


def save_game():
    save_data = {
        "money": game_data.money,
        "money_per_second": game_data.money_per_second,
        "money_per_click": game_data.money_per_click,
        "click_upgrade_level": game_data.click_upgrade_level,
        "click_upgrade_cost": game_data.click_upgrade_cost,
        "owned_businesses": business.owned_businesses,
        "owned_crypto": investing.owned_crypto,
        "crypto_prices": investing.current_prices,
        "crypto_price_histories": investing.price_histories,
    }

    with open(SAVE_FILE_PATH, "w", encoding="utf-8") as save_file:
        json.dump(save_data, save_file, indent=2)


def load_game():
    if not os.path.exists(SAVE_FILE_PATH):
        return False

    try:
        with open(SAVE_FILE_PATH, "r", encoding="utf-8") as save_file:
            save_data = json.load(save_file)
    except (json.JSONDecodeError, OSError, TypeError, ValueError):
        return False

    game_data.money = float(save_data.get("money", 0.0))
    game_data.money_per_click = float(save_data.get("money_per_click", 1.0))
    game_data.click_upgrade_level = int(save_data.get("click_upgrade_level", 0))
    game_data.click_upgrade_cost = float(save_data.get("click_upgrade_cost", 25.0))
    saved_owned_businesses = save_data.get("owned_businesses", {})
    saved_owned_crypto = save_data.get("owned_crypto", {})
    saved_crypto_prices = save_data.get("crypto_prices", {})
    saved_crypto_histories = save_data.get("crypto_price_histories", {})

    for business_definition in business.BUSINESS_DEFINITIONS:
        business_name = business_definition["name"]
        business.owned_businesses[business_name] = int(saved_owned_businesses.get(business_name, 0))

    business.update_total_money_per_second()
    investing.load_state(saved_crypto_prices, saved_crypto_histories, saved_owned_crypto)
    return True
