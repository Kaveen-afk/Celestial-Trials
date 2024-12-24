import pygame
import buttons
from shadow import Shadow
from sys import exit
import subprocess

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((1080, 720))
pygame.display.set_caption('Celestial Trials: The Arcane Path')
clock = pygame.time.Clock()

# Game Variables
game_paused = False
start_menu = True
in_level1 = False

# Additional variables
is_frozen = False
freeze_time = 0  # To track the time the player is frozen
prologue_sound_played = False

# Load prologue audio clip
prologue_sound = pygame.mixer.Sound("sounds/prolog.mp3 .mp3")
controls_sound = pygame.mixer.Sound("sounds/controls.mp3")

# Fonts
font = pygame.font.SysFont("arialblack", 40)

# Define Colors
TEXT_COL = (255, 255, 255)
# Initialize Pygame mixer for sound
pygame.mixer.init()

# Load background sound for the start menu
start_menu_sound = pygame.mixer.Sound("sounds/gameSM.mp3")
start_menu_sound.set_volume(0.5)  # Set volume (0.0 to 1.0)

# Play the sound on a loop when in the start menu
if start_menu:
    if not pygame.mixer.get_busy():  # Ensure the sound isn't already playing
        start_menu_sound.play(-1)  # Loop indefinitely


# Load button images
new_game_img = pygame.image.load("image/new_game.png").convert_alpha()
continue_img = pygame.image.load("image/continue.png").convert_alpha()
quit_img = pygame.image.load("image/quit.png").convert_alpha()
resume_img = pygame.image.load("image/resume.png").convert_alpha()

# Button instances for start menu
new_game_button = buttons.Button(400, 300, new_game_img, 1.5)
continue_button = buttons.Button(400, 400, continue_img, 1.5)
menu_quit_button = buttons.Button(400, 500, quit_img, 1.5)

# Button instances for pause menu
resume_button = buttons.Button(400, 250, resume_img, 1.5)
pause_quit_button = buttons.Button(400, 450, quit_img, 1.5)

# Backgrounds and graphics
moon_surface = pygame.image.load('graphics/moon.png')
sky_surface = pygame.image.load('graphics/sky.png')
wall_surface = pygame.image.load('graphics/wall.png')
tower_surface = pygame.image.load('graphics/tower.png')
slevel1_bg = pygame.image.load('levels/slevel1.png').convert_alpha()

# Player assets
player_left1 = pygame.image.load("player/movement1-.png").convert_alpha()
player_left2 = pygame.image.load("player/movement2-.png").convert_alpha()
player_right1 = pygame.image.load("player/movement1.png").convert_alpha()
player_right2 = pygame.image.load("player/movement3.png").convert_alpha()
player_front = pygame.image.load("player/back.png").convert_alpha()
player_down = pygame.image.load("player/front.png").convert_alpha()

# Initial player state
player_x, player_y = 180, 300
player_speed = 1
player_dx, player_dy = 0, 0
player_anim_frame = 0
player_direction = 'front'

# Collision mechanics
walls = [
    pygame.Rect(0, 0, 1080, 20),
    pygame.Rect(0, 0, 20, 720),
    pygame.Rect(1060, 0, 20, 720),
    pygame.Rect(0, 700, 1080, 20),
]
collision_blocks = [
    pygame.Rect(0, 0, 380, 119),
    pygame.Rect(640, 0, 500, 119),
    pygame.Rect(0, 450, 265, 80),
    pygame.Rect(0, 690, 1080, 8),
    pygame.Rect(0, 290, 180, 8),
    pygame.Rect(900, 450, 180, 8),
    pygame.Rect(900, 290, 180, 8),
]

stairs_rect = pygame.Rect(400, 0, 240, 50)

# Shadow system
shadow_system = Shadow((1080, 720))
shadow_system.add_highlight_area(pygame.Rect(100, 100, 200, 200))
shadow_system.add_highlight_area(pygame.Rect(400, 300, 150, 150))

# Objects on top of the shadow overlay
objects = [
    {
        "image": pygame.transform.scale(
            pygame.image.load("background drawing assets/fwall1.png").convert_alpha(), (450, 190)
        ),
        "pos": (660, 0),
    },
    {
        "image": pygame.transform.scale(
            pygame.image.load("background drawing assets/fwall2.png").convert_alpha(), (350, 190)
        ),
        "pos": (20, 10),
    },
    {
        "image": pygame.transform.scale(
            pygame.image.load("background drawing assets/fwall1.png").convert_alpha(), (250, 100)
        ),
        "pos": (30, 470),
    },
    {
        "image": pygame.transform.scale(
            pygame.image.load("background drawing assets/top.png").convert_alpha(), (70, 60)
        ),
        "pos": (0, 0),
    },
    {
        "image": pygame.transform.scale(
            pygame.image.load("background drawing assets/deco.png").convert_alpha(), (208, 268)
        ),
        "pos": (450, 300),
    },
]

# Implement collision check function
def check_collisions(dx, dy):
    player_rect = pygame.Rect(player_x + dx, player_y + dy, player_front.get_width(), player_front.get_height())
    for wall in walls:
        if player_rect.colliderect(wall):
            return True
    for block in collision_blocks:
        if player_rect.colliderect(block):
            return True
    return False

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def open_settings():
    print("Settings Menu Placeholder")

def fade_out():
    if pygame.display.get_init():  # Check if Pygame display is initialized
        fade_surface = pygame.Surface((1080, 720))
        fade_surface.fill((0, 0, 0))
        for alpha in range(0, 300):
            fade_surface.set_alpha(alpha)
            screen.blit(fade_surface, (0, 0))
            pygame.display.update()
            pygame.time.delay(5)


def update_player_animation():
    global player_anim_frame
    player_anim_frame = (player_anim_frame + 1) % 2

# Play the sound when entering the start menu (only once)
if start_menu and not pygame.mixer.get_busy():
    start_menu_sound.play(-1)

def start_tetris():
    # Stop Pygame sound and quit
    pygame.mixer.quit()
    pygame.quit()

    # Run the Tetris game (ensure it's in the correct directory)
    subprocess.run(['python3', 'Game/Tetrus.py'])  # Replace with the actual filename if different

    # After Tetris ends, reset the game state to level 1
    reset_game_state()

def display_exit_message():
    font = pygame.font.SysFont("arialblack", 50)
    text = font.render("See you in Version 0.2", True, (255, 255, 255))
    text_rect = text.get_rect(center=(1080 // 2, 720 // 2))

    # Display the message
    screen.fill((0, 0, 0))  # Black background
    screen.blit(text, text_rect)
    pygame.display.update()
    time.sleep(3)

# Inside the game loop, where the player collides with the stairs_rect

def reset_game_state():
    global player_x, player_y, in_level1, game_paused, start_menu
    player_x, player_y = 180, 300  # Starting position in level 1
    in_level1 = True
    game_paused = False
    start_menu = False  


# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if in_level1:
                    game_paused = not game_paused
                else:
                    start_menu = True
                    in_level1 = False
            if event.key == pygame.K_RETURN:  # Start the game with Enter
                if start_menu:
                    start_menu = False
                    in_level1 = True
                    start_menu_sound.stop()
            if event.key == pygame.K_LEFT:
                player_dx = -player_speed
                player_direction = 'left'
            if event.key == pygame.K_RIGHT:
                player_dx = player_speed
                player_direction = 'right'
            if event.key == pygame.K_UP:
                player_dy = -player_speed
                player_direction = 'front'
            if event.key == pygame.K_DOWN:
                player_dy = player_speed
                player_direction = 'down'
        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                player_dx = 0
            if event.key in [pygame.K_UP, pygame.K_DOWN]:
                player_dy = 0

    if start_menu:
        screen.blit(sky_surface, (0, 0))
        screen.blit(moon_surface, (300, 20))
        screen.blit(wall_surface, (660, 375))
        screen.blit(wall_surface, (0, 375))
        screen.blit(wall_surface, (180, 375))
        screen.blit(tower_surface, (-150, 50))
        draw_text("Celestial Trials: The Arcane Path", font, TEXT_COL, 250, 40)

        if new_game_button.draw(screen) and not prologue_sound_played:
            start_menu = False
            in_level1 = True
            start_menu_sound.stop()  # Stop the start menu sound
            is_frozen = True  # Freeze the character
            freeze_time = pygame.time.get_ticks()  # Get the current time in milliseconds
            prologue_sound.play()  # Play the prologue sound
            prologue_sound_played = True 
        # Inside the game loop
        if is_frozen:
            # Check if the 3 minutes have passed (180000 milliseconds)
            if pygame.time.get_ticks() - freeze_time >= 180000:
                is_frozen = True  # freeze the character after 3 minutes
                controls_sound.play()  # Play the controls sound clip

        # In the level loop, make sure to only allow the player to move if not frozen
        if not is_frozen:
            if not check_collisions(player_dx, player_dy):
                player_x += player_dx 
                player_y += player_dy

        if continue_button.draw(screen):
            start_menu = False
            in_level1 = True
            start_menu_sound.stop()  # Stop the start menu sound
            
        if menu_quit_button.draw(screen):
            pygame.quit()
            exit()

    elif in_level1:
        screen.blit(slevel1_bg, (0, 0))
        shadow_system.draw(screen)
        for obj in objects:
            screen.blit(obj["image"], obj["pos"])
        pygame.draw.rect(screen, (0, 0, 255), stairs_rect)
        if not check_collisions(player_dx, player_dy):
            player_x += player_dx
            player_y += player_dy
        player_rect = pygame.Rect(player_x, player_y, player_front.get_width(), player_front.get_height())
        
        if player_rect.colliderect(stairs_rect):
            print("Entering next level...")
            fade_out()
            # Change the background to level 2
            screen.fill((0, 0, 0))  # Black background for simplicity
            pygame.display.update()
            pygame.time.wait(1000)  # Wait 1 second for visual transition
            start_tetris()  # Start the Tetris game
            print("Entering next level...")
            fade_out()

        update_player_animation()
        if player_direction == 'left':
            screen.blit(player_left1 if player_anim_frame == 0 else player_left2, (player_x, player_y))
        elif player_direction == 'right':
            screen.blit(player_right1 if player_anim_frame == 0 else player_right2, (player_x, player_y))
        elif player_direction == 'front':
            screen.blit(player_front, (player_x, player_y))
        elif player_direction == 'down':
            screen.blit(player_down, (player_x, player_y))

    pygame.display.update()
    clock.tick(60)
