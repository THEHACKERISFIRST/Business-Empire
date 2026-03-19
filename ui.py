import pygame
import game_data

TAB_NAMES = ["Investing", "Business", "Earning", "Items", "Save"]
TAB_BAR_HEIGHT = 90
BUSINESS_LIST_VISIBLE_ITEMS = 5
INVESTING_SUBTABS = ["Shares", "Real Estate", "Cryptocurrency"]
INVESTING_SUBTAB_HEIGHT = 58
INVESTING_VISIBLE_ITEMS = 5

BACKGROUND_TOP = (18, 28, 44)
BACKGROUND_BOTTOM = (44, 62, 86)
PANEL_COLOR = (245, 248, 255)
PANEL_TINT = (227, 235, 248)
CARD_COLOR = (255, 255, 255)
CARD_HOVER = (243, 248, 255)
OUTLINE = (163, 180, 204)
TEXT_DARK = (20, 32, 52)
TEXT_MUTED = (92, 108, 132)
TAB_IDLE = (198, 210, 228)
TAB_HOVER = (214, 224, 240)
TAB_ACTIVE = (50, 109, 197)
BUTTON_BLUE = (47, 112, 201)
BUTTON_BLUE_HOVER = (61, 127, 216)
BUTTON_GOLD = (182, 123, 56)
BUTTON_GOLD_HOVER = (198, 139, 72)
BUTTON_GREEN = (67, 144, 104)
BUTTON_GREEN_HOVER = (81, 160, 119)
BUTTON_RED = (176, 88, 88)
BUTTON_RED_HOVER = (192, 102, 102)
BUTTON_SLATE = (108, 124, 153)
BUTTON_SLATE_HOVER = (124, 139, 168)
STATUS_BG = (231, 238, 248)
GRAPH_BG = (237, 243, 252)


def get_small_font():
    return pygame.font.SysFont("Trebuchet MS", 20)


def get_medium_font():
    return pygame.font.SysFont("Trebuchet MS", 24, bold=True)


def get_title_font():
    return pygame.font.SysFont("Georgia", 40, bold=True)


def draw_screen_background(screen):
    screen_width, screen_height = screen.get_size()

    for y in range(screen_height):
        blend = y / max(1, screen_height - 1)
        color = (
            int(BACKGROUND_TOP[0] + (BACKGROUND_BOTTOM[0] - BACKGROUND_TOP[0]) * blend),
            int(BACKGROUND_TOP[1] + (BACKGROUND_BOTTOM[1] - BACKGROUND_TOP[1]) * blend),
            int(BACKGROUND_TOP[2] + (BACKGROUND_BOTTOM[2] - BACKGROUND_TOP[2]) * blend),
        )
        pygame.draw.line(screen, color, (0, y), (screen_width, y))

    glow_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    pygame.draw.circle(glow_surface, (255, 255, 255, 24), (screen_width - 120, 130), 180)
    pygame.draw.circle(glow_surface, (255, 255, 255, 14), (150, screen_height - 140), 220)
    screen.blit(glow_surface, (0, 0))


def draw_panel(screen, rect, color=PANEL_COLOR, border_color=OUTLINE, radius=18, shadow_offset=6):
    shadow_rect = rect.move(0, shadow_offset)
    shadow_surface = pygame.Surface(shadow_rect.size, pygame.SRCALPHA)
    pygame.draw.rect(shadow_surface, (8, 15, 28, 50), shadow_surface.get_rect(), border_radius=radius)
    screen.blit(shadow_surface, shadow_rect.topleft)
    pygame.draw.rect(screen, color, rect, border_radius=radius)
    pygame.draw.rect(screen, border_color, rect, 2, border_radius=radius)


def draw_button(screen, rect, font, label, mouse_pos, base_color, hover_color, text_color=(255, 255, 255)):
    button_color = hover_color if rect.collidepoint(mouse_pos) else base_color
    draw_panel(screen, rect, color=button_color, border_color=(29, 44, 69), radius=14, shadow_offset=4)
    text = font.render(label, True, text_color)
    screen.blit(text, text.get_rect(center=rect.center))


def draw_pill(screen, rect, text, font, text_color=TEXT_MUTED):
    pygame.draw.rect(screen, STATUS_BG, rect, border_radius=999)
    pygame.draw.rect(screen, OUTLINE, rect, 2, border_radius=999)
    label = font.render(text, True, text_color)
    screen.blit(label, label.get_rect(center=rect.center))


def draw_section_heading(screen, title, subtitle, center_x, top_y):
    title_text = get_title_font().render(title, True, PANEL_COLOR)
    subtitle_text = get_small_font().render(subtitle, True, (217, 227, 241))
    screen.blit(title_text, title_text.get_rect(center=(center_x, top_y)))
    screen.blit(subtitle_text, subtitle_text.get_rect(center=(center_x, top_y + 34)))


def get_tab_rects(screen_width, screen_height):
    bar_rect = pygame.Rect(14, screen_height - TAB_BAR_HEIGHT - 12, screen_width - 28, TAB_BAR_HEIGHT)
    horizontal_padding = 18
    tab_gap = 18
    tab_width = (bar_rect.width - (horizontal_padding * 2) - (tab_gap * (len(TAB_NAMES) - 1))) // len(TAB_NAMES)
    tab_height = bar_rect.height - 24
    tab_y = bar_rect.y + (bar_rect.height - tab_height) // 2
    start_x = bar_rect.x + horizontal_padding
    rects = []

    for index, tab_name in enumerate(TAB_NAMES):
        tab_x = start_x + index * (tab_width + tab_gap)
        rects.append((tab_name, pygame.Rect(tab_x, tab_y, tab_width, tab_height)))

    return rects


def get_clicked_tab(mouse_pos, screen_width, screen_height):
    for tab_name, tab_rect in get_tab_rects(screen_width, screen_height):
        if tab_rect.collidepoint(mouse_pos):
            return tab_name

    return None


def draw_back_button(screen, font, mouse_pos, button_rect, label="Back"):
    draw_button(screen, button_rect, font, label, mouse_pos, BUTTON_SLATE, BUTTON_SLATE_HOVER)


def draw_row_icon(screen, image_surface, x, y, size=42):
    if image_surface is None:
        return

    scaled_icon = pygame.transform.smoothscale(image_surface, (size, size))
    icon_rect = scaled_icon.get_rect(center=(x, y))
    screen.blit(scaled_icon, icon_rect)


def draw_top_bar(screen, font, money, income_per_second):
    screen_width = screen.get_width()
    top_rect = pygame.Rect(18, 16, screen_width - 36, 90)
    draw_panel(screen, top_rect, color=(242, 247, 255), radius=20, shadow_offset=5)

    label_font = get_small_font()
    money_text = font.render(f"${game_data.format_number(money, 1)}", True, TEXT_DARK)
    income_text = get_medium_font().render(f"${game_data.format_number(income_per_second, 1)} / second", True, TEXT_DARK)
    money_label = label_font.render("Total Money", True, TEXT_MUTED)
    income_label = label_font.render("Income Rate", True, TEXT_MUTED)

    screen.blit(money_label, (42, 30))
    screen.blit(money_text, (42, 52))
    income_label_rect = income_label.get_rect(topright=(screen_width - 42, 30))
    income_text_rect = income_text.get_rect(topright=(screen_width - 42, 50))
    screen.blit(income_label, income_label_rect)
    screen.blit(income_text, income_text_rect)


def draw_bottom_tabs(screen, font, active_tab, mouse_pos):
    screen_width, screen_height = screen.get_size()
    bar_rect = pygame.Rect(14, screen_height - TAB_BAR_HEIGHT - 12, screen_width - 28, TAB_BAR_HEIGHT)
    draw_panel(screen, bar_rect, color=(234, 241, 251), radius=24, shadow_offset=4)

    for tab_name, tab_rect in get_tab_rects(screen_width, screen_height):
        if tab_name == active_tab:
            tab_color = TAB_ACTIVE
            text_color = (255, 255, 255)
            border_color = (37, 82, 145)
        elif tab_rect.collidepoint(mouse_pos):
            tab_color = TAB_HOVER
            text_color = TEXT_DARK
            border_color = OUTLINE
        else:
            tab_color = TAB_IDLE
            text_color = TEXT_DARK
            border_color = OUTLINE

        pygame.draw.rect(screen, tab_color, tab_rect, border_radius=18)
        pygame.draw.rect(screen, border_color, tab_rect, 2, border_radius=18)

        tab_text = font.render(tab_name, True, text_color)
        tab_text_rect = tab_text.get_rect(center=tab_rect.center)
        screen.blit(tab_text, tab_text_rect)


def get_investing_subtab_rects(screen_width):
    tab_width = 220
    spacing = 16
    total_width = (tab_width * len(INVESTING_SUBTABS)) + (spacing * (len(INVESTING_SUBTABS) - 1))
    start_x = (screen_width - total_width) // 2
    rects = []

    for index, tab_name in enumerate(INVESTING_SUBTABS):
        x = start_x + index * (tab_width + spacing)
        rects.append((tab_name, pygame.Rect(x, 110, tab_width, INVESTING_SUBTAB_HEIGHT)))

    return rects


def get_clicked_investing_subtab(mouse_pos, screen_width):
    for tab_name, tab_rect in get_investing_subtab_rects(screen_width):
        if tab_rect.collidepoint(mouse_pos):
            return tab_name
    return None


def get_investing_back_button_rect():
    return pygame.Rect(30, 110, 120, 50)


def get_crypto_buy_button_rect(screen_width):
    return pygame.Rect((screen_width - 240) // 2, 245, 240, 60)


def get_crypto_sell_button_rect(screen_width):
    return pygame.Rect(screen_width - 300, 315, 190, 60)


def get_crypto_amount_input_rect(screen_width):
    return pygame.Rect((screen_width - 260) // 2, 510, 260, 56)


def get_crypto_confirm_buy_button_rect(screen_width):
    button_width = 250
    button_height = 60
    button_gap = 24
    total_width = (button_width * 2) + button_gap
    start_x = (screen_width - total_width) // 2
    return pygame.Rect(start_x, 575, button_width, button_height)


def get_crypto_buy_max_button_rect(screen_width):
    button_width = 250
    button_height = 60
    button_gap = 24
    total_width = (button_width * 2) + button_gap
    start_x = (screen_width - total_width) // 2
    return pygame.Rect(start_x + button_width + button_gap, 575, button_width, button_height)


def get_crypto_list_area_rect(screen_width, screen_height, top_y):
    item_width = min(screen_width - 120, 900)
    item_height = INVESTING_VISIBLE_ITEMS * 72
    return pygame.Rect((screen_width - item_width) // 2, top_y, item_width, min(item_height, screen_height - TAB_BAR_HEIGHT - top_y - 40))


def get_crypto_item_rect(screen_width, top_y, index):
    item_width = min(screen_width - 120, 900)
    item_height = 62
    return pygame.Rect((screen_width - item_width) // 2, top_y + (index * 72), item_width, item_height)


def get_sell_adjust_button_rects(screen_width, screen_height):
    center_y = screen_height // 2 + 10
    return (
        pygame.Rect(screen_width // 2 - 170, center_y, 70, 60),
        pygame.Rect(screen_width // 2 + 100, center_y, 70, 60),
    )
def get_confirm_sell_button_rect(screen_width, screen_height):
    return pygame.Rect((screen_width - 260) // 2, screen_height // 2 + 110, 260, 70)


def get_business_button_rect(screen_width):
    button_width = 300
    button_height = 65
    return pygame.Rect((screen_width - button_width) // 2, 250, button_width, button_height)


def get_business_back_button_rect():
    return pygame.Rect(30, 110, 120, 50)


def get_business_item_rect(screen_width, start_y, index):
    item_width = min(screen_width - 120, 800)
    item_height = 58
    return pygame.Rect((screen_width - item_width) // 2, start_y + (index * 68), item_width, item_height)


def get_business_list_area_rect(screen_width, screen_height):
    item_width = min(screen_width - 120, 800)
    list_height = BUSINESS_LIST_VISIBLE_ITEMS * 68 - 10
    return pygame.Rect((screen_width - item_width) // 2, 455, item_width, min(list_height, screen_height - TAB_BAR_HEIGHT - 505))


def get_business_amount_input_rect(screen_width):
    return pygame.Rect((screen_width - 260) // 2, 530, 260, 56)


def get_business_buy_max_button_rect(screen_width):
    button_width = 250
    button_height = 60
    button_gap = 24
    total_width = (button_width * 2) + button_gap
    start_x = (screen_width - total_width) // 2
    return pygame.Rect(start_x + button_width + button_gap, 590, button_width, button_height)


def get_business_confirm_buy_button_rect(screen_width):
    button_width = 250
    button_height = 60
    button_gap = 24
    total_width = (button_width * 2) + button_gap
    start_x = (screen_width - total_width) // 2
    return pygame.Rect(start_x, 590, button_width, button_height)


def get_click_upgrade_button_rect(screen_width, screen_height):
    button_width = 380
    button_height = 74
    return pygame.Rect(
        (screen_width - button_width) // 2,
        screen_height - TAB_BAR_HEIGHT - 120,
        button_width,
        button_height,
    )


def get_save_button_rect(screen_width, screen_height):
    button_width = 260
    button_height = 80
    return pygame.Rect(
        (screen_width - button_width) // 2,
        520,
        button_width,
        button_height,
    )


def draw_save_tab(screen, font, mouse_pos, status_message, stats_lines):
    screen_width, screen_height = screen.get_size()
    button_rect = get_save_button_rect(screen_width, screen_height)
    stats_panel = pygame.Rect((screen_width - 700) // 2, 250, 700, 250)
    draw_section_heading(screen, "Save & Stats", "Your progress and current empire value", screen_width // 2, 185)
    draw_panel(screen, stats_panel, color=PANEL_TINT)
    stats_start_y = 320

    for index, stat_line in enumerate(stats_lines):
        stat_text = font.render(stat_line, True, TEXT_DARK)
        stat_rect = stat_text.get_rect(center=(screen_width // 2, stats_start_y + (index * 40)))
        screen.blit(stat_text, stat_rect)

    draw_button(screen, button_rect, font, "Save Game", mouse_pos, BUTTON_GREEN, BUTTON_GREEN_HOVER)

    if status_message:
        pill_rect = pygame.Rect((screen_width - 320) // 2, 635, 320, 42)
        draw_pill(screen, pill_rect, status_message, get_small_font(), text_color=TEXT_DARK)


def draw_earning_tab(screen, font, mouse_pos, clicker_surface, clicker_rect, money_per_click, click_upgrade_cost, click_upgrade_level):
    screen_width, screen_height = screen.get_size()
    draw_section_heading(screen, "Earnings", "Click to earn cash and upgrade your click income", screen_width // 2, 130)

    clicker_rect = clicker_surface.get_rect(center=(screen_width // 2, 340))

    if clicker_rect.collidepoint(mouse_pos):
        clicker_surface.set_alpha(255)
    else:
        clicker_surface.set_alpha(220)

    clicker_panel = clicker_rect.inflate(120, 120)
    draw_panel(screen, clicker_panel, color=PANEL_TINT, radius=28)
    screen.blit(clicker_surface, clicker_rect)

    upgrade_rect = get_click_upgrade_button_rect(*screen.get_size())
    draw_button(screen, upgrade_rect, font, "Upgrade Clicker", mouse_pos, BUTTON_BLUE, BUTTON_BLUE_HOVER)

    click_text = get_small_font().render(
        f"${game_data.format_number(money_per_click, 1)} per click",
        True,
        (231, 239, 250),
    )
    click_rect = click_text.get_rect(center=(upgrade_rect.centerx, upgrade_rect.centery + 26))
    screen.blit(click_text, click_rect)

    detail_text = get_small_font().render(
        f"Level {click_upgrade_level}   Cost: ${game_data.format_number(click_upgrade_cost, 1)}",
        True,
        (219, 232, 249),
    )
    detail_rect = detail_text.get_rect(center=(upgrade_rect.centerx, upgrade_rect.bottom + 26))
    screen.blit(detail_text, detail_rect)


def draw_business_tab(
    screen,
    font,
    mouse_pos,
    business_income_per_second,
    businesses,
    status_message,
    list_open,
    scroll_offset,
):
    screen_width, screen_height = screen.get_size()
    small_font = get_small_font()
    draw_section_heading(screen, "Businesses", "Build steady income by expanding your companies", screen_width // 2, 130)

    title_text = font.render(
        f"Business Income: {game_data.format_number(business_income_per_second, 1)} / second",
        True,
        PANEL_COLOR,
    )
    title_rect = title_text.get_rect(center=(screen_width // 2, 205))
    screen.blit(title_text, title_rect)

    hour_income = business_income_per_second * 3600
    hour_text = small_font.render(f"{game_data.format_number(hour_income, 1)} / hour", True, (219, 229, 243))
    hour_rect = hour_text.get_rect(center=(screen_width // 2, 240))
    screen.blit(hour_text, hour_rect)

    button_rect = get_business_button_rect(screen_width)
    button_label = "Start A Business" if not list_open else "Hide Business List"
    draw_button(screen, button_rect, font, button_label, mouse_pos, BUTTON_GOLD, BUTTON_GOLD_HOVER)

    if list_open:
        list_start_y = button_rect.bottom + 30
        list_area_rect = get_business_list_area_rect(screen_width, screen_height)
        draw_panel(screen, list_area_rect, color=PANEL_COLOR, radius=18)

        visible_businesses = businesses[scroll_offset:scroll_offset + BUSINESS_LIST_VISIBLE_ITEMS]
        for index, business in enumerate(visible_businesses):
            item_rect = get_business_item_rect(screen_width, list_start_y, index)
            item_color = CARD_HOVER if item_rect.collidepoint(mouse_pos) else CARD_COLOR
            draw_panel(screen, item_rect, color=item_color, radius=14, shadow_offset=2)

            left_text = font.render(
                f"{business['name']}  x{business['owned']}  (${game_data.format_number(business['cost'], 0)})",
                True,
                TEXT_DARK,
            )
            left_rect = left_text.get_rect(midleft=(item_rect.left + 14, item_rect.centery))
            screen.blit(left_text, left_rect)

            income_text = small_font.render(
                f"+{game_data.format_number(business['income_per_second'], 1)}/s",
                True,
                BUTTON_GREEN,
            )
            income_rect = income_text.get_rect(midright=(item_rect.right - 14, item_rect.centery))
            screen.blit(income_text, income_rect)

        if len(businesses) > BUSINESS_LIST_VISIBLE_ITEMS:
            scroll_text = small_font.render("Mouse wheel to scroll", True, (230, 237, 248))
            scroll_rect = scroll_text.get_rect(center=(screen_width // 2, list_area_rect.bottom + 18))
            screen.blit(scroll_text, scroll_rect)

    if status_message:
        pill_rect = pygame.Rect((screen_width - 460) // 2, screen_height - TAB_BAR_HEIGHT - 62, 460, 40)
        draw_pill(screen, pill_rect, status_message, small_font, text_color=TEXT_DARK)
def draw_business_buy_editor(screen, font, mouse_pos, selected_business, amount_text, status_message):
    screen_width, screen_height = screen.get_size()
    small_font = get_small_font()
    panel_rect = pygame.Rect((screen_width - 620) // 2, 230, 620, screen_height - TAB_BAR_HEIGHT - 280)
    draw_panel(screen, panel_rect, color=PANEL_COLOR, radius=22)

    title = font.render(selected_business["name"], True, TEXT_DARK)
    screen.blit(title, title.get_rect(center=(screen_width // 2, 290)))

    try:
        parsed_amount = int(amount_text) if amount_text else 0
    except ValueError:
        parsed_amount = 0

    total_cost = selected_business["cost"] * parsed_amount
    info_lines = [
        f"Cost each: ${game_data.format_number(selected_business['cost'], 0)}",
        f"Owned now: {selected_business['owned']}",
        f"Income each: +{game_data.format_number(selected_business['income_per_second'], 1)}/s",
        f"Total cost: ${game_data.format_number(total_cost, 0)}",
    ]

    for index, line in enumerate(info_lines):
        text = font.render(line, True, TEXT_DARK)
        screen.blit(text, text.get_rect(center=(screen_width // 2, 360 + (index * 42))))

    prompt = small_font.render("How much to buy", True, TEXT_MUTED)
    screen.blit(prompt, prompt.get_rect(center=(screen_width // 2, 525)))

    input_rect = get_business_amount_input_rect(screen_width)
    draw_panel(screen, input_rect, color=(248, 250, 255), radius=12, shadow_offset=2)
    input_text = font.render(amount_text or "0", True, TEXT_DARK)
    screen.blit(input_text, input_text.get_rect(midleft=(input_rect.left + 14, input_rect.centery)))

    buy_max_rect = get_business_buy_max_button_rect(screen_width)
    draw_button(screen, buy_max_rect, font, "Buy Max", mouse_pos, BUTTON_GREEN, BUTTON_GREEN_HOVER)

    confirm_rect = get_business_confirm_buy_button_rect(screen_width)
    draw_button(screen, confirm_rect, font, "Confirm Buy", mouse_pos, BUTTON_GOLD, BUTTON_GOLD_HOVER)

    helper = small_font.render("Whole numbers only", True, TEXT_MUTED)
    screen.blit(helper, helper.get_rect(center=(screen_width // 2, 860)))

    if status_message:
        pill_rect = pygame.Rect((screen_width - 460) // 2, screen_height - TAB_BAR_HEIGHT - 48, 460, 40)
        draw_pill(screen, pill_rect, status_message, small_font, text_color=TEXT_DARK)


def draw_investing_subtabs(screen, font, mouse_pos, active_subtab):
    for tab_name, tab_rect in get_investing_subtab_rects(screen.get_width()):
        if tab_name == active_subtab:
            tab_color = TAB_ACTIVE
            text_color = (255, 255, 255)
            border_color = (37, 82, 145)
        elif tab_rect.collidepoint(mouse_pos):
            tab_color = TAB_HOVER
            text_color = TEXT_DARK
            border_color = OUTLINE
        else:
            tab_color = TAB_IDLE
            text_color = TEXT_DARK
            border_color = OUTLINE

        draw_panel(screen, tab_rect, color=tab_color, border_color=border_color, radius=16, shadow_offset=3)
        text = font.render(tab_name, True, text_color)
        text_rect = text.get_rect(center=tab_rect.center)
        screen.blit(text, text_rect)


def draw_investing_placeholder(screen, font, message):
    panel_rect = pygame.Rect((screen.get_width() - 540) // 2, 220, 540, 170)
    draw_panel(screen, panel_rect, color=PANEL_COLOR, radius=24)
    title = get_medium_font().render(message, True, TEXT_DARK)
    subtitle = get_small_font().render("This section is ready for the next feature pass.", True, TEXT_MUTED)
    screen.blit(title, title.get_rect(center=(panel_rect.centerx, panel_rect.centery - 14)))
    screen.blit(subtitle, subtitle.get_rect(center=(panel_rect.centerx, panel_rect.centery + 24)))


def draw_crypto_portfolio(screen, font, mouse_pos, rows, status_message, market_open, market_scroll_offset, owned_scroll_offset):
    screen_width, screen_height = screen.get_size()
    small_font = get_small_font()
    draw_section_heading(screen, "Investing", "Watch the market and manage your holdings", screen_width // 2, 200)

    buy_button_rect = get_crypto_buy_button_rect(screen_width)
    buy_label = "Hide Market" if market_open else "Buy Cryptocurrency"
    draw_button(screen, buy_button_rect, font, buy_label, mouse_pos, BUTTON_GREEN, BUTTON_GREEN_HOVER)

    portfolio_title = font.render("Your Cryptocurrency", True, PANEL_COLOR)
    portfolio_rect = portfolio_title.get_rect(center=(screen_width // 2, 340))
    screen.blit(portfolio_title, portfolio_rect)

    owned_top_y = 375
    owned_area = get_crypto_list_area_rect(screen_width, screen_height, owned_top_y)
    draw_panel(screen, owned_area, color=PANEL_COLOR, radius=18)

    visible_owned_rows = rows[owned_scroll_offset:owned_scroll_offset + INVESTING_VISIBLE_ITEMS]
    for index, row in enumerate(visible_owned_rows):
        item_rect = get_crypto_item_rect(screen_width, owned_top_y, index)
        item_color = CARD_HOVER if item_rect.collidepoint(mouse_pos) else CARD_COLOR
        draw_panel(screen, item_rect, color=item_color, radius=14, shadow_offset=2)

        draw_row_icon(screen, row.get("image"), item_rect.left + 34, item_rect.centery)
        line_left = font.render(f"{row['name']} ({row['symbol']})", True, TEXT_DARK)
        screen.blit(line_left, line_left.get_rect(midleft=(item_rect.left + 66, item_rect.centery - 12)))

        detail = small_font.render(
            f"Owned: {game_data.format_number(row['owned'], 2)}   Price: ${game_data.format_number(row['price'], 2)}   Worth: ${game_data.format_number(row['value'], 2)}",
            True,
            TEXT_MUTED,
        )
        screen.blit(detail, detail.get_rect(midleft=(item_rect.left + 66, item_rect.centery + 14)))

    if not rows:
        empty_text = small_font.render("You do not own any cryptocurrency yet.", True, TEXT_MUTED)
        screen.blit(empty_text, empty_text.get_rect(center=owned_area.center))

    if len(rows) > INVESTING_VISIBLE_ITEMS:
        scroll_text = small_font.render("Mouse wheel to scroll holdings", True, (230, 237, 248))
        screen.blit(scroll_text, scroll_text.get_rect(center=(screen_width // 2, owned_area.bottom + 18)))

    if status_message:
        pill_rect = pygame.Rect((screen_width - 460) // 2, screen_height - TAB_BAR_HEIGHT - 62, 460, 40)
        draw_pill(screen, pill_rect, status_message, small_font, text_color=TEXT_DARK)


def draw_crypto_market(screen, font, mouse_pos, rows, status_message, scroll_offset):
    screen_width, screen_height = screen.get_size()
    small_font = get_small_font()
    panel_rect = pygame.Rect((screen_width - 960) // 2, 180, 960, screen_height - TAB_BAR_HEIGHT - 235)
    draw_panel(screen, panel_rect, color=PANEL_TINT, radius=24)

    title = font.render("Crypto Market", True, TEXT_DARK)
    screen.blit(title, title.get_rect(center=(screen_width // 2, 215)))

    helper = small_font.render("Choose a cryptocurrency to open the buy screen", True, TEXT_MUTED)
    screen.blit(helper, helper.get_rect(center=(screen_width // 2, 250)))

    market_top_y = 290
    market_area = get_crypto_list_area_rect(screen_width, screen_height, market_top_y)
    draw_panel(screen, market_area, color=PANEL_COLOR, radius=18)

    visible_market_rows = rows[scroll_offset:scroll_offset + INVESTING_VISIBLE_ITEMS]
    for index, row in enumerate(visible_market_rows):
        item_rect = get_crypto_item_rect(screen_width, market_top_y, index)
        item_color = CARD_HOVER if item_rect.collidepoint(mouse_pos) else CARD_COLOR
        draw_panel(screen, item_rect, color=item_color, radius=14, shadow_offset=2)

        draw_row_icon(screen, row.get("image"), item_rect.left + 34, item_rect.centery)
        line_left = font.render(f"{row['name']} ({row['symbol']})", True, TEXT_DARK)
        screen.blit(line_left, line_left.get_rect(midleft=(item_rect.left + 66, item_rect.centery - 12)))

        detail = small_font.render(
            f"Price: ${game_data.format_number(row['price'], 2)}   Owned: {game_data.format_number(row['owned'], 2)}   Value: ${game_data.format_number(row['value'], 2)}",
            True,
            TEXT_MUTED,
        )
        screen.blit(detail, detail.get_rect(midleft=(item_rect.left + 66, item_rect.centery + 14)))

    if len(rows) > INVESTING_VISIBLE_ITEMS:
        scroll_text = small_font.render("Mouse wheel to scroll market", True, TEXT_MUTED)
        screen.blit(scroll_text, scroll_text.get_rect(center=(screen_width // 2, market_area.bottom + 18)))

    if status_message:
        pill_rect = pygame.Rect((screen_width - 460) // 2, screen_height - TAB_BAR_HEIGHT - 48, 460, 40)
        draw_pill(screen, pill_rect, status_message, small_font, text_color=TEXT_DARK)
def draw_crypto_buy_editor(screen, font, mouse_pos, selected_row, amount_text, status_message):
    screen_width, screen_height = screen.get_size()
    small_font = get_small_font()
    panel_rect = pygame.Rect((screen_width - 620) // 2, 230, 620, screen_height - TAB_BAR_HEIGHT - 280)
    draw_panel(screen, panel_rect, color=PANEL_COLOR, radius=22)

    title = font.render(f"Buy {selected_row['name']} ({selected_row['symbol']})", True, TEXT_DARK)
    screen.blit(title, title.get_rect(center=(screen_width // 2, 335)))
    draw_row_icon(screen, selected_row.get("image"), screen_width // 2, 275, size=72)

    info_lines = [
        f"Price each: ${game_data.format_number(selected_row['price'], 2)}",
        f"Owned now: {game_data.format_number(selected_row['owned'], 2)}",
    ]

    try:
        parsed_amount = float(amount_text) if amount_text else 0.0
    except ValueError:
        parsed_amount = 0.0

    total_cost = selected_row["price"] * parsed_amount
    info_lines.append(f"Total cost: ${game_data.format_number(total_cost, 2)}")

    for index, line in enumerate(info_lines):
        text = font.render(line, True, TEXT_DARK)
        screen.blit(text, text.get_rect(center=(screen_width // 2, 372 + (index * 42))))

    prompt = small_font.render("Type the amount you want to buy", True, TEXT_MUTED)
    screen.blit(prompt, prompt.get_rect(center=(screen_width // 2, 500)))

    input_rect = get_crypto_amount_input_rect(screen_width)
    draw_panel(screen, input_rect, color=(248, 250, 255), radius=12, shadow_offset=2)
    input_text = font.render(amount_text or "0", True, TEXT_DARK)
    screen.blit(input_text, input_text.get_rect(midleft=(input_rect.left + 14, input_rect.centery)))

    buy_max_rect = get_crypto_buy_max_button_rect(screen_width)
    draw_button(screen, buy_max_rect, font, "Buy Max", mouse_pos, BUTTON_GREEN, BUTTON_GREEN_HOVER)

    button_rect = get_crypto_confirm_buy_button_rect(screen_width)
    draw_button(screen, button_rect, font, "Confirm Buy", mouse_pos, BUTTON_BLUE, BUTTON_BLUE_HOVER)

    helper = small_font.render("Numbers and decimal point only", True, TEXT_MUTED)
    screen.blit(helper, helper.get_rect(center=(screen_width // 2, 845)))

    if status_message:
        pill_rect = pygame.Rect((screen_width - 460) // 2, screen_height - TAB_BAR_HEIGHT - 48, 460, 40)
        draw_pill(screen, pill_rect, status_message, small_font, text_color=TEXT_DARK)


def draw_crypto_detail(screen, font, mouse_pos, crypto_row, price_history, status_message):
    screen_width, screen_height = screen.get_size()
    small_font = get_small_font()
    panel_rect = pygame.Rect(70, 230, screen_width - 140, screen_height - TAB_BAR_HEIGHT - 285)
    draw_panel(screen, panel_rect, color=PANEL_COLOR, radius=24)

    title = font.render(f"{crypto_row['name']} ({crypto_row['symbol']})", True, TEXT_DARK)
    screen.blit(title, title.get_rect(center=(screen_width // 2, 305)))
    draw_row_icon(screen, crypto_row.get("image"), screen_width // 2, 230, size=72)

    summary = small_font.render(
        f"Owned: {game_data.format_number(crypto_row['owned'], 2)}   Price: ${game_data.format_number(crypto_row['price'], 2)}   Worth: ${game_data.format_number(crypto_row['value'], 2)}",
        True,
        TEXT_MUTED,
    )
    screen.blit(summary, summary.get_rect(center=(screen_width // 2, 350)))

    graph_rect = pygame.Rect(110, 405, screen_width - 220, min(340, screen_height - TAB_BAR_HEIGHT - 520))
    draw_panel(screen, graph_rect, color=GRAPH_BG, radius=18, shadow_offset=2)

    if len(price_history) >= 2:
        min_price = min(price_history)
        max_price = max(price_history)
        price_span = max(max_price - min_price, 0.000001)
        points = []
        for index, price in enumerate(price_history):
            x = graph_rect.left + (index / max(1, len(price_history) - 1)) * graph_rect.width
            normalized = (price - min_price) / price_span
            y = graph_rect.bottom - normalized * (graph_rect.height - 20) - 10
            points.append((x, y))
        pygame.draw.lines(screen, BUTTON_GREEN, False, points, 4)

    low_text = small_font.render(f"Low: ${game_data.format_number(min(price_history), 2)}", True, TEXT_MUTED)
    high_text = small_font.render(f"High: ${game_data.format_number(max(price_history), 2)}", True, TEXT_MUTED)
    screen.blit(low_text, (graph_rect.left + 12, graph_rect.bottom + 12))
    screen.blit(high_text, (graph_rect.right - high_text.get_width() - 12, graph_rect.bottom + 12))

    time_text = small_font.render("Price history: last 1 hour of game time", True, TEXT_MUTED)
    screen.blit(time_text, time_text.get_rect(center=(screen_width // 2, graph_rect.bottom + 42)))

    sell_button_rect = get_crypto_sell_button_rect(screen_width)
    draw_button(screen, sell_button_rect, font, "Sell", mouse_pos, BUTTON_RED, BUTTON_RED_HOVER)

    if status_message:
        pill_rect = pygame.Rect((screen_width - 460) // 2, screen_height - TAB_BAR_HEIGHT - 48, 460, 40)
        draw_pill(screen, pill_rect, status_message, small_font, text_color=TEXT_DARK)


def draw_crypto_sell_view(screen, font, mouse_pos, crypto_row, sell_quantity, status_message):
    screen_width, screen_height = screen.get_size()
    small_font = get_small_font()
    panel_rect = pygame.Rect((screen_width - 660) // 2, 150, 660, screen_height - TAB_BAR_HEIGHT - 200)
    draw_panel(screen, panel_rect, color=PANEL_COLOR, radius=22)

    title = font.render(f"Sell {crypto_row['name']} ({crypto_row['symbol']})", True, TEXT_DARK)
    screen.blit(title, title.get_rect(center=(screen_width // 2, 210)))
    draw_row_icon(screen, crypto_row.get("image"), screen_width // 2, 132, size=72)

    current_value = crypto_row["price"] * sell_quantity
    total_value = crypto_row["value"]
    info_lines = [
        f"Owned: {game_data.format_number(crypto_row['owned'], 2)}",
        f"Price each: ${game_data.format_number(crypto_row['price'], 2)}",
        f"Sell amount: {game_data.format_number(sell_quantity, 2)}",
        f"Sell worth: ${game_data.format_number(current_value, 2)}",
        f"Total crypto value: ${game_data.format_number(total_value, 2)}",
    ]

    for index, line in enumerate(info_lines):
        text = font.render(line, True, TEXT_DARK)
        screen.blit(text, text.get_rect(center=(screen_width // 2, 270 + (index * 42))))

    minus_rect, plus_rect = get_sell_adjust_button_rects(screen_width, screen_height)
    draw_button(screen, minus_rect, font, "-", mouse_pos, BUTTON_SLATE, BUTTON_SLATE_HOVER)
    draw_button(screen, plus_rect, font, "+", mouse_pos, BUTTON_SLATE, BUTTON_SLATE_HOVER)

    confirm_rect = get_confirm_sell_button_rect(screen_width, screen_height)
    draw_button(screen, confirm_rect, font, "Confirm Sell", mouse_pos, BUTTON_RED, BUTTON_RED_HOVER)

    helper = small_font.render("Use + and - to change amount by 1", True, TEXT_MUTED)
    screen.blit(helper, helper.get_rect(center=(screen_width // 2, confirm_rect.bottom + 28)))

    if status_message:
        pill_rect = pygame.Rect((screen_width - 460) // 2, screen_height - TAB_BAR_HEIGHT - 48, 460, 40)
        draw_pill(screen, pill_rect, status_message, small_font, text_color=TEXT_DARK)
