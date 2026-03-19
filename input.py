import pygame

# This tracks previous click state so we only trigger ONCE
previous_click = False


def get_mouse_pos():
    return pygame.mouse.get_pos()


def is_click_once():
    global previous_click

    current_click = pygame.mouse.get_pressed()[0]

    # True ONLY when click starts (not held)
    if current_click and not previous_click:
        previous_click = True
        return True

    # Reset when released
    if not current_click:
        previous_click = False

    return False