money = 0.0
# Passive income earned every second.
money_per_second = 0.0
money_per_click = 1.0
click_upgrade_level = 0
click_upgrade_cost = 25.0


def format_number(value, decimals=1):
    return f"{value:,.{decimals}f}"


def buy_click_upgrade():
    global money
    global money_per_click
    global click_upgrade_level
    global click_upgrade_cost

    if money < click_upgrade_cost:
        return False

    money -= click_upgrade_cost
    click_upgrade_level += 1
    money_per_click += 0.5
    click_upgrade_cost = round(click_upgrade_cost * 1.6, 1)
    return True
