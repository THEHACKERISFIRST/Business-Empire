import game_data

BUSINESS_DEFINITIONS = [
    {"name": "Shoping", "cost": 100.0, "income_per_second": 1.0},
    {"name": "Taxi Company", "cost": 500.0, "income_per_second": 5.0},
    {"name": "Shipping Company", "cost": 2500.0, "income_per_second": 20.0},
    {"name": "Factory", "cost": 10000.0, "income_per_second": 75.0},
    {"name": "Construction Company", "cost": 50000.0, "income_per_second": 300.0},
    {"name": "Car Dealership", "cost": 200000.0, "income_per_second": 1200.0},
    {"name": "IT Company", "cost": 750000.0, "income_per_second": 4500.0},
    {"name": "Bank", "cost": 3000000.0, "income_per_second": 18000.0},
    {"name": "Sports Club", "cost": 12000000.0, "income_per_second": 70000.0},
    {"name": "Oil And Gas Company", "cost": 50000000.0, "income_per_second": 300000.0},
    {"name": "Airlines", "cost": 200000000.0, "income_per_second": 1250000.0},
]

owned_businesses = {business["name"]: 0 for business in BUSINESS_DEFINITIONS}


def get_business_income_per_second():
    total_income = 0.0

    for business_definition in BUSINESS_DEFINITIONS:
        total_income += owned_businesses[business_definition["name"]] * business_definition["income_per_second"]

    return total_income


def update_total_money_per_second():
    game_data.money_per_second = get_business_income_per_second()


def get_business_definition(business_name):
    for business_definition in BUSINESS_DEFINITIONS:
        if business_definition["name"] == business_name:
            return business_definition

    raise ValueError(f"Unknown business: {business_name}")


def buy_business(business_name):
    return buy_business_quantity(business_name, 1)


def buy_business_quantity(business_name, quantity):
    business_definition = get_business_definition(business_name)
    if quantity <= 0:
        return False

    total_cost = business_definition["cost"] * quantity
    if game_data.money < total_cost:
        return False

    game_data.money -= total_cost
    owned_businesses[business_name] += quantity
    update_total_money_per_second()
    return True


def get_max_affordable_quantity(business_name):
    business_definition = get_business_definition(business_name)
    if business_definition["cost"] <= 0:
        return 0

    return int(game_data.money // business_definition["cost"])


def get_business_asset_value():
    total_value = 0.0

    for business_definition in BUSINESS_DEFINITIONS:
        total_value += owned_businesses[business_definition["name"]] * business_definition["cost"]

    return total_value
