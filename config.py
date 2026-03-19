import pygame

pygame.init()

# Starting window size
WIDTH = 1280
HEIGHT = 720

# Resizable window
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Clicker Game")

# Clock for FPS + delta time
clock = pygame.time.Clock()

# Font for UI (auto scales later if you want)
font = pygame.font.SysFont("Arial", 30)