import pygame
from random import randint

pygame.init()
fps = pygame.time.Clock()
screen = pygame.display.set_mode((500,600)) 
icon = pygame.image.load('assets/images/icon.png')
pygame.display.set_icon(icon)
pygame.display.set_caption("Tetris")

bg = pygame.image.load('assets/images/background.png')
bg = pygame.transform.scale(bg,(300,600))

bg_sound = pygame.mixer.Sound('assets/sounds/Yihav_kozak_za_dunai.mp3')
bg_sound.play(-1)

font = pygame.font.SysFont("consolas", 48, bold=True)
sidebar_font = pygame.font.SysFont("consolas", 28, bold=True)

score = 0

rows = 20
cols = 10
cell_size = 30

move_delay = {"left": 200, "right": 200, "down": 80}
last_move_time = {"left": 0, "right": 0, "down": 0}

grid = [[0 for i in range(cols)] for j in range(rows)]

# кольори
cyan = (0, 200, 200)
red = (255, 0, 0)
green = (0, 128, 0)
yellow = (255, 255, 0)
purple = (128, 0, 128)
orange = (255, 165, 0)
blue = (0, 0, 255)
gray = (50, 50, 50)

# фігури
shapes = {
    1: ([(0, -1), (-1, 0), (0, 0), (1, 0)], cyan),
    2: ([(0, -1), (0, 0), (0, 1), (0, 2)], red),
    3: ([(0, -1), (-1, -1), (-1, 0), (0, 0)], green),
    4: ([(0, -1), (-1, -1), (-1, 0), (-2, 0)], yellow),
    5: ([(0, -1), (-1, -1), (0, 0), (1, 0)], purple),
    6: ([(-1, -1), (-1, 0), (0, 0), (1, 0)], orange),
    7: ([(1, -1), (-1, 0), (0, 0), (1, 0)], blue)
}

def new_piece():
    tile = randint(1, 7)
    shape, colour = shapes[tile]
    x, y = cols // 2, 1
    coords = [(x + dx, y + dy) for (dx, dy) in shape]
    return coords, colour, tile

piece, piece_colour, current_id = new_piece()
next_piece_id = randint(1, 7)
fall_time = 0

def clearlines():
    global grid, score
    new_grid = []
    lines_cleared = 0
    for row in grid:
        if all(cell != 0 for cell in row):
            lines_cleared += 1
        else:
            new_grid.append(row)
    if lines_cleared == 1:
        score += 150
    elif lines_cleared == 2:
        score += 300
    elif lines_cleared == 3:
        score += 600
    elif lines_cleared == 4:
        score += 1200
    for _ in range(lines_cleared):
        new_grid.insert(0, [0 for _ in range(cols)])
    grid = new_grid

def gameover(piece):
    for (x, y) in piece:
        if y >= 0 and grid[y][x] != 0:
            return True
    return False

def draw_game_over():
    text_game_over = font.render("GAME OVER", True, (255, 0, 0))
    text_score = font.render(f"Final score: {score}", True, (255, 255, 255))
    text_restart = font.render("Press R to Restart", True, (255, 255, 255))
    padding = 20
    total_height = text_game_over.get_height() + text_score.get_height() + text_restart.get_height() + padding * 4
    total_width = max(text_game_over.get_width(), text_score.get_width(), text_restart.get_width()) + padding * 2
    container_rect = pygame.Rect(0, 0, total_width, total_height)
    container_rect.center = (250, 300)
    pygame.draw.rect(screen, (0, 0, 0), container_rect)
    pygame.draw.rect(screen, (255, 255, 255), container_rect, 3) 
    text_y_offset = container_rect.top + padding
    text_rect_go = text_game_over.get_rect(center=(container_rect.centerx, text_y_offset + text_game_over.get_height() / 2))
    screen.blit(text_game_over, text_rect_go)
    text_y_offset += text_game_over.get_height() + padding
    text_rect_score = text_score.get_rect(center=(container_rect.centerx, text_y_offset + text_score.get_height() / 2))
    screen.blit(text_score, text_rect_score)
    text_y_offset += text_score.get_height() + padding
    text_rect_restart = text_restart.get_rect(center=(container_rect.centerx, text_y_offset + text_restart.get_height() / 2))
    screen.blit(text_restart, text_rect_restart)
    pygame.display.flip()

def reset_game():
    global grid, piece, piece_colour, fall_time, last_move_time, score, current_id, next_piece_id
    fall_time = 0
    last_move_time = {"left": 0, "right": 0, "down": 0}
    grid = [[0 for _ in range(cols)] for _ in range(rows)]
    piece, piece_colour, current_id = new_piece()
    next_piece_id = randint(1, 7)
    score = 0

def draw_next_piece():
    rect = pygame.Rect(320, 180, 160, 160)
    pygame.draw.rect(screen, (0, 0, 0), rect)
    pygame.draw.rect(screen, (255, 255, 255), rect, 3)
    label = sidebar_font.render("Next:", True, (255, 255, 255))
    screen.blit(label, (rect.x + 40, rect.y - 30))
    shape, colour = shapes[next_piece_id]
    offset_x, offset_y = 380, 240
    for (dx, dy) in shape:
        x = offset_x + dx * cell_size
        y = offset_y + dy * cell_size
        pygame.draw.rect(screen, colour, (x, y, cell_size, cell_size))
        pygame.draw.rect(screen, gray, (x, y, cell_size, cell_size), 1)

state = "game"
Running = True
while Running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False
        elif event.type == pygame.KEYDOWN:
            if state == "game":
                if event.key == pygame.K_UP:
                    pivot = piece[0]
                    rotated = [(pivot[0] - (y - pivot[1]), pivot[1] + (x - pivot[0])) for (x, y) in piece]
                    if all(0 <= x < cols and 0 <= y < rows and grid[y][x] == 0 for (x,y) in rotated):
                        piece = rotated
            elif state == "lost" and event.key == pygame.K_r:
                reset_game()
                state = "game"

    if state == "game":
        pygame.draw.rect(screen, (30, 30, 30), (300, 0, 200, 600))
        pygame.draw.rect(screen, (255, 255, 255), (300, 0, 2, 600))

        score_label = sidebar_font.render("Score:", True, (255, 255, 255))
        screen.blit(score_label, (350, 50))
        score_text = sidebar_font.render(str(score), True, (255, 255, 255))
        screen.blit(score_text, (350, 90))
        draw_next_piece()

        dt = fps.tick(60)
        fall_time += dt
        current_time = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and current_time - last_move_time["left"] > move_delay["left"]:
            moved = [(x-1, y) for (x, y) in piece]
            if all(0 <= x < cols and grid[y][x] == 0 for (x,y) in moved):
                piece = moved
            last_move_time["left"] = current_time
        elif keys[pygame.K_RIGHT] and current_time - last_move_time["right"] > move_delay["right"]:
            moved = [(x+1, y) for (x, y) in piece]
            if all(0 <= x < cols and grid[y][x] == 0 for (x,y) in moved):
                piece = moved
            last_move_time["right"] = current_time
        elif keys[pygame.K_DOWN] and current_time - last_move_time["down"] > move_delay["down"]:
            moved = [(x, y+1) for (x, y) in piece]
            if all(y < rows and grid[y][x] == 0 for (x,y) in moved):
                piece = moved
            last_move_time["down"] = current_time

        screen.blit(bg, (0,0))
        if fall_time > 500:
            fall_time = 0
            can_move = True
            for (x,y) in piece:
                if y+1 >= rows or grid[y+1][x] != 0:
                    can_move = False
                    break
            if can_move:
                piece = [(x, y+1) for (x, y) in piece]
            else:
                for (x,y) in piece:
                    grid[y][x] = piece_colour
                clearlines()
                shape, piece_colour = shapes[next_piece_id]
                piece = [(cols // 2 + dx, 1 + dy) for (dx, dy) in shape]
                current_id = next_piece_id
                next_piece_id = randint(1, 7)
                if gameover(piece):
                    state = "lost"

        for row in range(rows):
            for col in range(cols):
                if grid[row][col] != 0:
                    pygame.draw.rect(screen, grid[row][col], (col*cell_size, row*cell_size, cell_size, cell_size))
                    pygame.draw.rect(screen, gray, (col*cell_size, row*cell_size, cell_size, cell_size), 1)

        for (x, y) in piece:
            pygame.draw.rect(screen, piece_colour, (x*cell_size, y*cell_size, cell_size, cell_size))
            pygame.draw.rect(screen, gray, (x*cell_size, y*cell_size, cell_size, cell_size), 1)

    elif state == "lost":
        draw_game_over()
        pygame.display.flip()

    pygame.display.update()
pygame.quit()
