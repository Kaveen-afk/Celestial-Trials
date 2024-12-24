import pygame
from Game.Tetrus import Tetrus
 # Assuming the Tetris game is implemented in this file

# Level 2 assets
slevel2_bg = pygame.image.load('levels/level21.png').convert_alpha()  # Level 2 background image

# Function to run Level 2
def run_level2(player_x, player_y, player_direction, player_dx):
    # Display Level 2 background
    screen = pygame.display.get_surface()
    screen.blit(slevel2_bg, (0, 0))

    # Tetris Game integration
    Tetrus(screen)  # This function will handle the Tetris logic

    # Handle player movement in Level 2 (e.g., moving left/right)
    if player_direction == 'left':
        player_x -= player_dx
    elif player_direction == 'right':
        player_x += player_dx

    # Display the player on Level 2 (character sprite)
    player_sprite = pygame.image.load("player/movement1.png").convert_alpha()  # Example sprite
    screen.blit(player_sprite, (player_x, player_y))

    # Provide options to go back to Level 1 or proceed forward
    font = pygame.font.SysFont("arialblack", 40)
    text = font.render("Press ESC to return to Level 1", True, (255, 255, 255))
    screen.blit(text, (100, 600))
    pygame.display.update()
