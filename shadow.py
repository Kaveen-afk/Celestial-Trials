import pygame

class Shadow:
    def __init__(self, screen_size):
        self.dark_overlay = pygame.Surface(screen_size)
        self.dark_overlay.fill((0, 0, 0))
        self.dark_overlay.set_alpha(120)
        self.brightness_mask = pygame.Surface(screen_size, pygame.SRCALPHA)
        self.highlight_areas = []

    def add_highlight_area(self, area):
        self.highlight_areas.append(area)

    def draw(self, screen):
        self.brightness_mask.fill((0, 0, 0, 0))
        for area in self.highlight_areas:
            pygame.draw.rect(self.brightness_mask, (0, 0, 0, 0), area)
        screen.blit(self.dark_overlay, (0, 0))
        screen.blit(self.brightness_mask, (0, 0))
