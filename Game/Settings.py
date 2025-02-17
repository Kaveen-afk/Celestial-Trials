import pygame

#Game size
COLUMNS=10
ROWS=20
CELL_SIZE=40 #40 pixels
GAME_WIDTH=COLUMNS*CELL_SIZE
GAME_HEIGHT=ROWS*CELL_SIZE

#Side bar size
SIDEBAR_WIDTH=200
PREVIEW_HEIGHT_FRACTION=0.7 #70% of the height
SCORE_HEIGHT_FRACTION=1-PREVIEW_HEIGHT_FRACTION

#Main Window
PADDING=20 #distance between window and other elements
WINDOW_WIDTH=GAME_WIDTH+SIDEBAR_WIDTH+PADDING*3 
WINDOW_HEIGHT=GAME_HEIGHT+PADDING*2

#Game behaviour
UPDATE_START_SPEED = 200
MOVE_WAIT_TIME = 200
ROTATE_WAIT_TIME = 200
BLOCK_OFFSET = pygame.Vector2(COLUMNS // 2, -1)

#Colors
YELLOW = '#c6b300'  
RED = '#b04017'       
BLUE = '#193b75'      
GREEN = '#4b8d28'     
PURPLE = '#5d1b5f'    
CYAN = '#538292'      
ORANGE = '#c7610f'    
GRAY = '#1c1c1c'      
LINE_COLOR = '#b3b3b3'

#Shapes
TETROMINOS = {
    'T': {'shape': [(0, 0), (-1, 0), (1, 0), (0, -1)], 'color': PURPLE},
    'O': {'shape': [(0, 0), (0, -1), (1, 0), (1, -1)], 'color': YELLOW},
    'J': {'shape': [(0, 0), (0, -1), (0, 1), (-1, -1)], 'color': BLUE},
    'L': {'shape': [(0, 0), (0, -1), (0, 1), (1, 1)], 'color': ORANGE},
    'I': {'shape': [(0, 0), (0, -1), (0, -2), (0, 1)], 'color': CYAN},
    'S': {'shape': [(0, 0), (-1, 0), (0, -1), (1, -1)], 'color': GREEN},
    'Z': {'shape': [(0, 0), (1, 0), (0, -1), (-1, -1)], 'color': RED}
}

SCORE_DATA = {1: 40, 2: 100, 3: 300, 4: 1200}


