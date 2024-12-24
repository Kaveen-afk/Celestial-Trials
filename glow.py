import pygame
from pygame.math import Vector2

def clamp(value, min_val, max_val):
    """Clamps a value between min_val and max_val."""
    return max(min(value, max_val), min_val)

def get_dist(pos1, pos2):
    """Calculates the distance between two positions."""
    return pos1.distance_to(pos2)

def generate_glow(glow, radius, bg_surface):
    """Generates a glow effect with a transparent hole in the dark overlay using the background surface."""
    # Create a surface with transparency
    surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    layers = 15  # Reduced layers for a smaller glow effect
    glow = clamp(glow, 180, 300)

    # Draw glow layers around the center
    for i in range(layers):
        k = clamp(glow - i * 10, 0, 255)
        pygame.draw.circle(surf, (k, k, k), surf.get_rect().center, radius - i * 2)  # Adjust the step for smaller circles

    # Create the transparent hole (use the background surface)
    hole_rect = pygame.Rect(0, 0, radius * 2, radius * 2)
    hole_surface = bg_surface.subsurface(hole_rect)  # Grab the section of the background where the glow will be
    surf.blit(hole_surface, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)  # Use the background to create the hole

    return surf

class Spot:
    """Represents a grid spot with fog effect."""
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.pos = Vector2(self.x, self.y)
        self.color = "black"
        self.width = width
        self.total_rows = total_rows

    def draw(self, win, player_pos):
        """Draws the spot with fog effect."""
        s = pygame.Surface((self.width, self.width))
        fog_intensity = clamp(get_dist(self.pos, player_pos), 0, 255)
        s.set_alpha(fog_intensity)
        s.fill((0, 0, 0))
        win.blit(s, self.pos)

def make_grid(rows, width):
    """Creates a grid of spots."""
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)
    return grid

def draw_grid(win, grid, player_pos):
    """Draws the grid and its fog effect."""
    for row in grid:
        for spot in row:
            spot.draw(win, player_pos)
