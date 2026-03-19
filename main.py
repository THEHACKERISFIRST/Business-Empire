import pygame
import os
from config import screen, clock, font
from input import get_mouse_pos, is_click_once
import business
import game_data
import investing
import save
from ui import (
    BUSINESS_LIST_VISIBLE_ITEMS,
    INVESTING_VISIBLE_ITEMS,
    draw_screen_background,
    draw_bottom_tabs,
    draw_business_buy_editor,
    draw_business_tab,
    draw_earning_tab,
    draw_investing_placeholder,
    draw_investing_subtabs,
    draw_back_button,
    draw_crypto_market,
    draw_crypto_detail,
    draw_crypto_buy_editor,
    draw_crypto_portfolio,
    draw_crypto_sell_view,
    draw_save_tab,
    draw_top_bar,
    get_business_amount_input_rect,
    get_business_back_button_rect,
    get_business_button_rect,
    get_business_buy_max_button_rect,
    get_business_confirm_buy_button_rect,
    get_business_list_area_rect,
    get_clicked_investing_subtab,
    get_click_upgrade_button_rect,
    get_business_item_rect,
    get_confirm_sell_button_rect,
    get_crypto_buy_max_button_rect,
    get_crypto_buy_button_rect,
    get_crypto_confirm_buy_button_rect,
    get_crypto_item_rect,
    get_crypto_list_area_rect,
    get_crypto_amount_input_rect,
    get_crypto_sell_button_rect,
    get_clicked_tab,
    get_investing_back_button_rect,
    get_save_button_rect,
    get_sell_adjust_button_rects,
)

running = True
dt = 0
click_income_per_second = 0.0
clicks_this_second = 0
click_rate_timer = 0.0
active_tab = "Earning"
save_status_message = ""
business_status_message = ""
earning_status_message = ""
business_list_open = False
business_scroll_offset = 0
business_view = "list"
selected_business_name = None
business_buy_amount_text = "1"
active_investing_subtab = "Shares"
investing_view = "portfolio"
investing_status_message = ""
crypto_market_scroll_offset = 0
crypto_owned_scroll_offset = 0
selected_crypto_symbol = None
crypto_sell_quantity = 1.0
crypto_buy_amount_text = "1"

# Image data
businessEmpireLogo = os.path.join(os.path.dirname(__file__), "BusinessEmpireLogo.jpg")
businessEmpireLogoImage = pygame.image.load(businessEmpireLogo).convert()
pygame.display.set_icon(businessEmpireLogoImage)
click_me_image_path = os.path.join("ClickMeIcon.png")
click_me_image = pygame.image.load(click_me_image_path).convert_alpha()

if save.load_game():
    save_status_message = "Save loaded"

while running:
    investing.update_market(dt)
    screen_width, screen_height = screen.get_size()
    save_button_rect = get_save_button_rect(screen_width, screen_height)
    business_back_button_rect = get_business_back_button_rect()
    business_button_rect = get_business_button_rect(screen_width)
    business_amount_input_rect = get_business_amount_input_rect(screen_width)
    business_buy_max_button_rect = get_business_buy_max_button_rect(screen_width)
    business_confirm_buy_button_rect = get_business_confirm_buy_button_rect(screen_width)
    business_list_area_rect = get_business_list_area_rect(screen_width, screen_height)
    click_upgrade_button_rect = get_click_upgrade_button_rect(screen_width, screen_height)
    investing_back_button_rect = get_investing_back_button_rect()
    crypto_buy_button_rect = get_crypto_buy_button_rect(screen_width)
    crypto_buy_max_button_rect = get_crypto_buy_max_button_rect(screen_width)
    crypto_confirm_buy_button_rect = get_crypto_confirm_buy_button_rect(screen_width)
    crypto_amount_input_rect = get_crypto_amount_input_rect(screen_width)
    crypto_sell_button_rect = get_crypto_sell_button_rect(screen_width)
    minus_sell_rect, plus_sell_rect = get_sell_adjust_button_rects(screen_width, screen_height)
    confirm_sell_button_rect = get_confirm_sell_button_rect(screen_width, screen_height)

    # EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save.save_game()
            running = False
        elif event.type == pygame.MOUSEWHEEL and active_tab == "Business" and business_list_open:
            max_scroll_offset = max(0, len(business.BUSINESS_DEFINITIONS) - BUSINESS_LIST_VISIBLE_ITEMS)
            business_scroll_offset = max(0, min(max_scroll_offset, business_scroll_offset - event.y))
        elif event.type == pygame.MOUSEWHEEL and active_tab == "Investing" and active_investing_subtab == "Cryptocurrency":
            if investing_view == "market":
                max_scroll_offset = max(0, len(investing.CRYPTO_DEFINITIONS) - INVESTING_VISIBLE_ITEMS)
                crypto_market_scroll_offset = max(0, min(max_scroll_offset, crypto_market_scroll_offset - event.y))
            elif investing_view == "portfolio":
                owned_rows = investing.get_owned_rows()
                max_scroll_offset = max(0, len(owned_rows) - INVESTING_VISIBLE_ITEMS)
                crypto_owned_scroll_offset = max(0, min(max_scroll_offset, crypto_owned_scroll_offset - event.y))
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            clicked_tab = get_clicked_tab(event.pos, screen_width, screen_height)
            if clicked_tab is not None:
                active_tab = clicked_tab
                if active_tab != "Investing":
                    investing_view = "portfolio"
                    selected_crypto_symbol = None
                    crypto_sell_quantity = 1.0
                if active_tab != "Business":
                    business_list_open = False
                    business_view = "list"
                    selected_business_name = None
            elif active_tab == "Save" and save_button_rect.collidepoint(event.pos):
                save.save_game()
                save_status_message = "Game saved"
            elif active_tab == "Business":
                if business_view == "buy" and business_back_button_rect.collidepoint(event.pos):
                    business_view = "list"
                    selected_business_name = None
                    business_status_message = ""
                elif business_view == "buy" and selected_business_name is not None:
                    if business_buy_max_button_rect.collidepoint(event.pos):
                        business_buy_amount_text = str(business.get_max_affordable_quantity(selected_business_name))
                    elif business_confirm_buy_button_rect.collidepoint(event.pos):
                        try:
                            buy_amount = int(business_buy_amount_text)
                        except ValueError:
                            buy_amount = 0

                        if buy_amount <= 0:
                            business_status_message = "Enter a valid amount to buy"
                        elif business.buy_business_quantity(selected_business_name, buy_amount):
                            business_status_message = (
                                f"Bought {game_data.format_number(buy_amount, 0)} {selected_business_name}"
                            )
                            business_view = "list"
                            selected_business_name = None
                        else:
                            selected_business = business.get_business_definition(selected_business_name)
                            total_cost = selected_business["cost"] * buy_amount
                            business_status_message = (
                                f"Need ${game_data.format_number(total_cost, 0)} "
                                f"for {game_data.format_number(buy_amount, 0)} {selected_business_name}"
                            )
                elif business_button_rect.collidepoint(event.pos):
                    business_list_open = not business_list_open
                    if business_list_open:
                        business_status_message = "Choose a business to buy below"
                    else:
                        business_status_message = "Business list hidden"
                elif business_view == "list" and business_list_open and business_list_area_rect.collidepoint(event.pos):
                    business_list_start_y = business_button_rect.bottom + 30
                    visible_businesses = business.BUSINESS_DEFINITIONS[
                        business_scroll_offset:business_scroll_offset + BUSINESS_LIST_VISIBLE_ITEMS
                    ]
                    for index, business_definition in enumerate(visible_businesses):
                        item_rect = get_business_item_rect(screen_width, business_list_start_y, index)
                        if item_rect.collidepoint(event.pos):
                            selected_business_name = business_definition["name"]
                            business_buy_amount_text = "1"
                            business_view = "buy"
                            business_status_message = ""
                            break
            elif active_tab == "Investing":
                clicked_subtab = get_clicked_investing_subtab(event.pos, screen_width)
                if clicked_subtab is not None:
                    active_investing_subtab = clicked_subtab
                    investing_view = "portfolio"
                    selected_crypto_symbol = None
                    crypto_sell_quantity = 1.0
                    investing_status_message = ""
                    crypto_market_scroll_offset = 0
                    crypto_owned_scroll_offset = 0
                elif active_investing_subtab == "Cryptocurrency":
                    if investing_view in {"market", "buy", "detail", "sell"} and investing_back_button_rect.collidepoint(event.pos):
                        if investing_view == "sell":
                            investing_view = "detail"
                        elif investing_view == "buy":
                            investing_view = "market"
                        else:
                            investing_view = "portfolio"
                            selected_crypto_symbol = None
                        investing_status_message = ""
                    elif investing_view == "portfolio":
                        owned_rows = investing.get_owned_rows()
                        owned_list_area = get_crypto_list_area_rect(screen_width, screen_height, 375)
                        if crypto_buy_button_rect.collidepoint(event.pos):
                            investing_view = "market"
                            investing_status_message = "Choose a cryptocurrency to buy"
                        elif owned_list_area.collidepoint(event.pos):
                            visible_owned_rows = owned_rows[
                                crypto_owned_scroll_offset:crypto_owned_scroll_offset + INVESTING_VISIBLE_ITEMS
                            ]
                            for index, row in enumerate(visible_owned_rows):
                                item_rect = get_crypto_item_rect(screen_width, 375, index)
                                if item_rect.collidepoint(event.pos):
                                    selected_crypto_symbol = row["symbol"]
                                    investing_view = "detail"
                                    investing_status_message = ""
                                    break
                    elif investing_view == "market":
                        market_list_area = get_crypto_list_area_rect(screen_width, screen_height, 290)
                        if market_list_area.collidepoint(event.pos):
                            visible_market_rows = investing.get_display_rows()[
                                crypto_market_scroll_offset:crypto_market_scroll_offset + INVESTING_VISIBLE_ITEMS
                            ]
                            for index, row in enumerate(visible_market_rows):
                                item_rect = get_crypto_item_rect(screen_width, 290, index)
                                if item_rect.collidepoint(event.pos):
                                    selected_crypto_symbol = row["symbol"]
                                    crypto_buy_amount_text = "1"
                                    investing_view = "buy"
                                    investing_status_message = ""
                                    break
                    elif investing_view == "buy" and selected_crypto_symbol is not None:
                        if crypto_buy_max_button_rect.collidepoint(event.pos):
                            crypto_buy_amount_text = str(investing.get_max_affordable_quantity(selected_crypto_symbol, game_data))
                        elif crypto_confirm_buy_button_rect.collidepoint(event.pos):
                            try:
                                buy_amount = float(crypto_buy_amount_text)
                            except ValueError:
                                buy_amount = 0.0

                            if buy_amount <= 0:
                                investing_status_message = "Enter a valid amount to buy"
                            elif investing.buy_crypto(selected_crypto_symbol, game_data, buy_amount):
                                investing_status_message = (
                                    f"Bought {game_data.format_number(buy_amount, 2)} "
                                    f"{selected_crypto_symbol}"
                                )
                                investing_view = "portfolio"
                                selected_crypto_symbol = None
                            else:
                                selected_price = investing.current_prices[selected_crypto_symbol]
                                total_cost = selected_price * buy_amount
                                investing_status_message = (
                                    f"Need ${game_data.format_number(total_cost, 2)} "
                                    f"to buy {game_data.format_number(buy_amount, 2)} {selected_crypto_symbol}"
                                )
                    elif investing_view == "detail" and selected_crypto_symbol is not None:
                        if crypto_sell_button_rect.collidepoint(event.pos):
                            investing_view = "sell"
                            crypto_sell_quantity = 1.0
                            investing_status_message = ""
                    elif investing_view == "sell" and selected_crypto_symbol is not None:
                        selected_row = None
                        for row in investing.get_owned_rows():
                            if row["symbol"] == selected_crypto_symbol:
                                selected_row = row
                                break

                        if selected_row is not None:
                            if minus_sell_rect.collidepoint(event.pos):
                                crypto_sell_quantity = max(1.0, crypto_sell_quantity - 1.0)
                            elif plus_sell_rect.collidepoint(event.pos):
                                crypto_sell_quantity = min(selected_row["owned"], crypto_sell_quantity + 1.0)
                            elif confirm_sell_button_rect.collidepoint(event.pos):
                                if investing.sell_crypto(selected_crypto_symbol, game_data, crypto_sell_quantity):
                                    investing_status_message = (
                                        f"Sold {game_data.format_number(crypto_sell_quantity, 2)} "
                                        f"{selected_crypto_symbol}"
                                    )
                                    remaining_owned = investing.owned_crypto[selected_crypto_symbol]
                                    if remaining_owned <= 0:
                                        investing_view = "portfolio"
                                        selected_crypto_symbol = None
                                    else:
                                        investing_view = "detail"
                                        crypto_sell_quantity = min(crypto_sell_quantity, remaining_owned)
                                else:
                                    investing_status_message = "Could not sell that amount"
            elif active_tab == "Earning" and click_upgrade_button_rect.collidepoint(event.pos):
                if game_data.buy_click_upgrade():
                    earning_status_message = "Clicker upgraded"
                else:
                    earning_status_message = (
                        f"Need ${game_data.format_number(game_data.click_upgrade_cost, 1)} for upgrade"
                    )
        elif event.type == pygame.KEYDOWN and active_tab == "Investing" and active_investing_subtab == "Cryptocurrency":
            if investing_view == "buy":
                if event.key == pygame.K_BACKSPACE:
                    crypto_buy_amount_text = crypto_buy_amount_text[:-1]
                elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    pass
                elif event.unicode and event.unicode in "0123456789.":
                    if event.unicode != "." or "." not in crypto_buy_amount_text:
                        crypto_buy_amount_text += event.unicode
        elif event.type == pygame.KEYDOWN and active_tab == "Business":
            if business_view == "buy":
                if event.key == pygame.K_BACKSPACE:
                    business_buy_amount_text = business_buy_amount_text[:-1]
                elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    pass
                elif event.unicode and event.unicode in "0123456789":
                    business_buy_amount_text += event.unicode

    # INPUT
    mouse_pos = get_mouse_pos()

    # ----------------------------
    # RESPONSIVE BUTTON
    # ----------------------------

    scaled_clicker = pygame.transform.smoothscale(click_me_image, (200, 200))
    button_rect = scaled_clicker.get_rect(center=(screen_width // 2, 340))

    if active_tab == "Earning" and is_click_once():
        if button_rect.collidepoint(mouse_pos):
            game_data.money += game_data.money_per_click
            clicks_this_second += 1
            print("Money:", game_data.money)

    # Add passive income based on how much time passed this frame.
    game_data.money += game_data.money_per_second * dt

    click_rate_timer += dt
    if click_rate_timer >= 1.0:
        # Convert clicks from the last second into click income per second.
        click_income_per_second = clicks_this_second / click_rate_timer
        clicks_this_second = 0
        click_rate_timer = 0.0

    # ----------------------------
    # DRAW
    # ----------------------------

    draw_screen_background(screen)

    if active_tab == "Earning":
        draw_earning_tab(
            screen,
            font,
            mouse_pos,
            scaled_clicker,
            button_rect,
            game_data.money_per_click,
            game_data.click_upgrade_cost,
            game_data.click_upgrade_level,
        )
        if earning_status_message:
            small_font = pygame.font.SysFont("Arial", 20)
            status_text = small_font.render(earning_status_message, True, (255, 255, 255))
            status_rect = status_text.get_rect(center=(screen_width // 2, button_rect.bottom + 120))
            screen.blit(status_text, status_rect)
    elif active_tab == "Business":
        if business_view == "buy" and selected_business_name is not None:
            draw_back_button(screen, font, mouse_pos, business_back_button_rect)
            selected_business = business.get_business_definition(selected_business_name)
            draw_business_buy_editor(
                screen,
                font,
                mouse_pos,
                {
                    "name": selected_business["name"],
                    "cost": selected_business["cost"],
                    "income_per_second": selected_business["income_per_second"],
                    "owned": business.owned_businesses[selected_business_name],
                },
                business_buy_amount_text,
                business_status_message,
            )
        else:
            business_rows = []
            for business_definition in business.BUSINESS_DEFINITIONS:
                business_rows.append(
                    {
                        "name": business_definition["name"],
                        "cost": business_definition["cost"],
                        "income_per_second": business_definition["income_per_second"],
                        "owned": business.owned_businesses[business_definition["name"]],
                    }
                )

            draw_business_tab(
                screen,
                font,
                mouse_pos,
                business.get_business_income_per_second(),
                business_rows,
                business_status_message,
                business_list_open,
                business_scroll_offset,
            )
    elif active_tab == "Investing":
        draw_investing_subtabs(screen, font, mouse_pos, active_investing_subtab)

        if active_investing_subtab == "Shares":
            draw_investing_placeholder(screen, font, "Shares coming soon")
        elif active_investing_subtab == "Real Estate":
            draw_investing_placeholder(screen, font, "Real Estate coming soon")
        elif active_investing_subtab == "Cryptocurrency":
            if investing_view == "portfolio":
                draw_crypto_portfolio(
                    screen,
                    font,
                    mouse_pos,
                    investing.get_owned_rows(),
                    investing_status_message,
                    False,
                    crypto_market_scroll_offset,
                    crypto_owned_scroll_offset,
                )
            elif investing_view == "market":
                draw_back_button(screen, font, mouse_pos, investing_back_button_rect)
                draw_crypto_market(
                    screen,
                    font,
                    mouse_pos,
                    investing.get_display_rows(),
                    investing_status_message,
                    crypto_market_scroll_offset,
                )
            elif investing_view == "buy" and selected_crypto_symbol is not None:
                draw_back_button(screen, font, mouse_pos, investing_back_button_rect)
                selected_row = None
                for row in investing.get_display_rows():
                    if row["symbol"] == selected_crypto_symbol:
                        selected_row = row
                        break
                if selected_row is not None:
                    draw_crypto_buy_editor(
                        screen,
                        font,
                        mouse_pos,
                        selected_row,
                        crypto_buy_amount_text,
                        investing_status_message,
                    )
                else:
                    investing_view = "market"
                    selected_crypto_symbol = None
            elif investing_view == "detail" and selected_crypto_symbol is not None:
                draw_back_button(screen, font, mouse_pos, investing_back_button_rect)
                selected_row = None
                for row in investing.get_owned_rows():
                    if row["symbol"] == selected_crypto_symbol:
                        selected_row = row
                        break
                if selected_row is not None:
                    draw_crypto_detail(
                        screen,
                        font,
                        mouse_pos,
                        selected_row,
                        investing.get_price_history(selected_crypto_symbol),
                        investing_status_message,
                    )
                else:
                    investing_view = "portfolio"
                    selected_crypto_symbol = None
            elif investing_view == "sell" and selected_crypto_symbol is not None:
                draw_back_button(screen, font, mouse_pos, investing_back_button_rect)
                selected_row = None
                for row in investing.get_owned_rows():
                    if row["symbol"] == selected_crypto_symbol:
                        selected_row = row
                        break
                if selected_row is not None:
                    crypto_sell_quantity = max(1.0, min(crypto_sell_quantity, selected_row["owned"]))
                    draw_crypto_sell_view(
                        screen,
                        font,
                        mouse_pos,
                        selected_row,
                        crypto_sell_quantity,
                        investing_status_message,
                    )
                else:
                    investing_view = "portfolio"
                    selected_crypto_symbol = None
    elif active_tab == "Save":
        draw_save_tab(screen, font, mouse_pos, save_status_message, save.get_stats_lines())

    total_income_per_second = game_data.money_per_second + click_income_per_second
    draw_top_bar(screen, font, game_data.money, total_income_per_second)
    draw_bottom_tabs(screen, font, active_tab, mouse_pos)

    # ----------------------------
    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
