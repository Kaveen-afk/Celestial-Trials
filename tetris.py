import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30

# Grid dimensions
GRID_WIDTH = SCREEN_WIDTH // BLOCK_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // BLOCK_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
COLORS = [
    (0, 255, 255),  # Cyan
    (0, 0, 255),    # Blue
    (255, 165, 0),  # Orange
    (255, 255, 0),  # Yellow
    (0, 255, 0),    # Green
    (128, 0, 128),  # Purple
    (255, 0, 0),    # Red
]

# Tetrimino shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[1, 0, 0], [1, 1, 1]],  # L
    [[0, 0, 1], [1, 1, 1]],  # J
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 0], [0, 1, 1]],  # Z
]


class Tetrimino:
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color
        self.x = GRID_WIDTH // 2 - len(shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]


def create_grid(locked_positions={}):
    grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    for (x, y), color in locked_positions.items():
        grid[y][x] = color
    return grid


def draw_grid(screen, grid):
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            pygame.draw.rect(
                screen,
                grid[y][x],
                (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
            )
    for x in range(GRID_WIDTH):
        pygame.draw.line(screen, GRAY, (x * BLOCK_SIZE, 0), (x * BLOCK_SIZE, SCREEN_HEIGHT))
    for y in range(GRID_HEIGHT):
        pygame.draw.line(screen, GRAY, (0, y * BLOCK_SIZE), (SCREEN_WIDTH, y * BLOCK_SIZE))


def draw_tetrimino(screen, tetrimino):
    for y, row in enumerate(tetrimino.shape):
        for x, value in enumerate(row):
            if value:
                pygame.draw.rect(
                    screen,
                    tetrimino.color,
                    (
                        (tetrimino.x + x) * BLOCK_SIZE,
                        (tetrimino.y + y) * BLOCK_SIZE,
                        BLOCK_SIZE,
                        BLOCK_SIZE,
                    ),
                )


def check_collision(tetrimino, grid):
    for y, row in enumerate(tetrimino.shape):
        for x, value in enumerate(row):
            if value:
                if (
                    tetrimino.x + x < 0
                    or tetrimino.x + x >= GRID_WIDTH
                    or tetrimino.y + y >= GRID_HEIGHT
                    or grid[tetrimino.y + y][tetrimino.x + x] != BLACK
                ):
                    return True
    return False


def lock_tetrimino(tetrimino, locked_positions):
    for y, row in enumerate(tetrimino.shape):
        for x, value in enumerate(row):
            if value:
                locked_positions[(tetrimino.x + x, tetrimino.y + y)] = tetrimino.color


def clear_lines(grid, locked_positions):
    cleared = 0
    for y in range(GRID_HEIGHT):
        if all(grid[y][x] != BLACK for x in range(GRID_WIDTH)):
            cleared += 1
            for x in range(GRID_WIDTH):
                del locked_positions[(x, y)]
            for key in sorted(locked_positions.keys(), key=lambda k: k[1], reverse=True):
                if key[1] < y:
                    locked_positions[(key[0], key[1] + 1)] = locked_positions.pop(key)
    return cleared


def calculate_score(cleared_lines, level):
    scores = [0, 40, 100, 300, 1200]
    return scores[cleared_lines] * (level + 1)


def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()

    grid = create_grid()
    locked_positions = {}

    current_piece = Tetrimino(random.choice(SHAPES), random.choice(COLORS))
    next_piece = Tetrimino(random.choice(SHAPES), random.choice(COLORS))

    fall_time = 0
    fall_speed = 0.5
    level = 0
    score = 0
    target_score = 10000

    font = pygame.font.Font(None, 36)

    running = True
    while running:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time / 1000 > fall_speed:
            current_piece.y += 1
            if check_collision(current_piece, grid):
                current_piece.y -= 1
                lock_tetrimino(current_piece, locked_positions)
                cleared_lines = clear_lines(grid, locked_positions)
                score += calculate_score(cleared_lines, level)
                if score >= target_score:
                    print("You Win!")
                    running = False
                level = score // 1000  # Increase level every 1000 points
                current_piece = next_piece
                next_piece = Tetrimino(random.choice(SHAPES), random.choice(COLORS))
                if check_collision(current_piece, grid):
                    print("Game Over!")
                    running = False
            fall_time = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if check_collision(current_piece, grid):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if check_collision(current_piece, grid):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if check_collision(current_piece, grid):
                        current_piece.y -= 1
                if event.key == pygame.K_UP:
                    current_piece.rotate()
                    if check_collision(current_piece, grid):
                        current_piece.rotate()
                        current_piece.rotate()
                        current_piece.rotate()

        screen.fill(BLACK)
        draw_grid(screen, grid)
        draw_tetrimino(screen, current_piece)

        # Display score and level
        score_text = font.render(f"Score: {score}", True, WHITE)
        level_text = font.render(f"Level: {level}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (10, 40))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()

