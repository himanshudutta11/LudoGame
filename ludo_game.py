import pygame
import math
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 750, 750
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Ludo Game")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)

def draw_star(surface, color, center, size):
    points = []
    for i in range(5):
        angle = math.radians(i * 144)
        x = center[0] + size * math.cos(angle)
        y = center[1] - size * math.sin(angle)
        points.append((x, y))
    pygame.draw.polygon(surface, color, points)

# Draw the board
def draw_board():
    window.fill(white)
    # Draw the squares
    pygame.draw.rect(window, red, (0, 0, 300, 300))
    pygame.draw.rect(window, green, (450, 0, 300, 300))
    pygame.draw.rect(window, blue, (0, 450, 300, 300))
    pygame.draw.rect(window, yellow, (450, 450, 300, 300))


    pygame.draw.rect(window, red, (50, 350, 250, 50))
    pygame.draw.rect(window, red, (50, 300, 50, 50))

    pygame.draw.rect(window, green, (350, 50, 50, 250))
    pygame.draw.rect(window, green, (400, 50, 50, 50))

    pygame.draw.rect(window, yellow, (450, 350, 250, 50))
    pygame.draw.rect(window, yellow, (650, 400, 50, 50))

    pygame.draw.rect(window, blue, (350, 450, 50, 250))
    pygame.draw.rect(window, blue, (300, 650, 50, 50))

    pygame.draw.circle(window, white, (200, 200), 30)
    pygame.draw.circle(window, white, (100, 100), 30)
    pygame.draw.circle(window, white, (100, 200), 30)
    pygame.draw.circle(window, white, (200, 100), 30)

    pygame.draw.circle(window, white, (550, 100), 30)
    pygame.draw.circle(window, white, (650, 100), 30)
    pygame.draw.circle(window, white, (550, 200), 30)
    pygame.draw.circle(window, white, (650, 200), 30)

    pygame.draw.circle(window, white, (200, 550), 30)
    pygame.draw.circle(window, white, (100, 650), 30)
    pygame.draw.circle(window, white, (100, 550), 30)
    pygame.draw.circle(window, white, (200, 650), 30)

    pygame.draw.circle(window, white, (550, 550), 30)
    pygame.draw.circle(window, white, (650, 650), 30)
    pygame.draw.circle(window, white, (550, 650), 30)
    pygame.draw.circle(window, white, (650, 550), 30)

    draw_star(window, red, (325, 125), 20)
    draw_star(window, green, (625, 325), 20)
    draw_star(window, yellow, (425, 625), 20)
    draw_star(window, blue, (125, 425), 20)

    # Draw the grid
    for x in range(0, height, 50):
        for y in range(300, 450, 50):
            if x >= 300 and x < 450:
                continue
            else:
                pygame.draw.rect(window, black, (x, y, 50, 50), 1)
    
    for x in range(300, 450, 50):
        for y in range(0, width, 50):
            if y >= 300 and y < 450:
                continue
            else:
                pygame.draw.rect(window, black, (x, y, 50, 50), 1)

    # Draw the center triangle
    pygame.draw.polygon(window, green, [(300, 300), (450, 300), (375, 375)], 0)
    pygame.draw.polygon(window, blue, [(300, 450), (450, 450), (375, 375)], 0)
    pygame.draw.polygon(window, red, [(300, 300), (300, 450), (375, 375)], 0)
    pygame.draw.polygon(window, yellow, [(450, 300), (450, 450), (375, 375)], 0)

    pygame.display.update()

players = {
    # "red": [(100, 100), (100, 200), (200, 100), (200, 200)],
    # "green": [(550, 100), (550, 200), (650, 100), (650, 200)],
    # "blue": [(100, 550), (200, 550), (100, 650), (200, 650)],
    # "yellow": [(550, 550), (650, 550), (550, 650), (650, 650)]
}

directions = {
    "red": ["right","right","right","right"],
    "green": ["down","down","down","down"],
    "yellow": ["left","left","left","left"],
    "blue": ["up", "up", "up", "up"]
}

original_positions = {
    "red": [(100, 100), (100, 200), (200, 100), (200, 200)],
    "green": [(550, 100), (550, 200), (650, 100), (650, 200)],
    "blue": [(100, 550), (200, 550), (100, 650), (200, 650)],
    "yellow": [(550, 550), (650, 550), (550, 650), (650, 650)]
}

starting_positions = {
    "red": [(75, 325)],
    "green": [(425, 75)],
    "blue": [(325, 675)],
    "yellow": [(675, 425)]
}

original_directions = {
    "red": ["right","right","right","right"],
    "green": ["down","down","down","down"],
    "yellow": ["left","left","left","left"],
    "blue": ["up", "up", "up", "up"]
}

starting_directions = {
    "red": "right",
    "green": "down",
    "yellow": "left",
    "blue": "up"
}

starred_positions = [(75, 325), (425, 75), (325, 675), (675, 425), (325, 125), (625, 325), (425, 625), (125, 425)]

winning_positions = {
    "red": (325, 375),
    "green": (375, 325),
    "yellow": (425, 375),
    "blue": (375, 425)
}

control_keys = {
    "red": "R",
    "green": "G",
    "yellow": "Y",
    "blue": "B"
}

home_box_limit = {
    "red": [0, 300, 0, 300],
    "green": [width-300, width, 0, 300],
    "yellow": [width-300, width, height-300, height],
    "blue": [0, 300, height-300, height]
}

def reset_game_state():
    global players, directions, original_positions, original_directions
    players = {color: pos.copy() for color, pos in original_positions.items()}
    directions = original_directions.copy()

def check_move_to_start(color, num):
    piece = players[color][num]
    limit = home_box_limit[color]

    if piece[0] > limit[0] and piece[0] < limit[1] and piece[1] > limit[2] and piece[1] < limit[3]: 
        players[color][num] = starting_positions[color][0]
        #directions[color][num] = starting_directions[color]
        return True         

# Move pieces
def move_piece(color, steps, index):
    piece = players[color][index]
    direction = directions[color][index]
    
    if direction == "right":
        new_x = piece[0] + steps * 50
        new_y = piece[1]
        if new_x > 325 and piece[1] == 375 and color == "red":
            new_x = piece[0]
        elif new_x > 275 and piece[0] <= 275 and piece[1] == 325:
            new_y = piece[1] - (new_x - 275)
            new_x = 325
            directions[color][index] = "up"
        elif new_x > 375 and piece[1] == 25 and color == "green":
            new_y = new_y + new_x - 375
            new_x = 375
            directions[color][index] = "down"
        elif new_x > 425 and piece[1] == 25:
            new_y = new_y + new_x - 425
            new_x = 425
            directions[color][index] = "down"
            if new_y > 275:
                new_x = new_x + new_y - 275
                directions[color][index] = "right"
        elif new_x > width:
            new_y = new_y + new_x - width + 25
            new_x = width - 25
            directions[color][index] = "down"
            if new_y > 375 and color == "yellow":
                new_x = new_x - (new_y - 375)
                new_y = 375
                directions[color][index] = "left"
            elif new_y > 425:
                new_x = new_x - (new_y - 425)
                new_y = 425
                directions[color][index] = "left"
    elif direction == "down":
        new_x = piece[0]
        new_y = piece[1] + steps * 50
        if new_y > 325 and piece[0] == 375 and color == "green":
            new_y = piece[1]
        elif new_y > 275 and piece[1] <= 275 and piece[0] == 425:
            new_x = piece[0] + (new_y - 275)
            new_y = 325
            directions[color][index] = "right"
        elif new_y > 375 and piece[0] == width - 25 and color == "yellow":
            new_x = new_x - (new_y - 375)
            new_y = 375
            directions[color][index] = "left"
        elif new_y > 425 and piece[0] == width - 25:
            new_x = new_x - (new_y - 425)
            new_y = 425
            directions[color][index] = "left"
            if new_x < 475:
                new_y = new_y + 475 - new_x
                new_x = 425
                directions[color][index] = "down"
        elif new_y > height:
            new_x = new_x - (new_y - height + 25)
            new_y = height - 25
            directions[color][index] = "left"
            if new_x < 375 and color == "blue":
                new_y = new_y - (375 - new_x)
                new_x = 375
                directions[color][index] = "up"
            elif new_x < 325:
                new_y = new_y - (325 - new_x)
                new_x = 325
                directions[color][index] = "up"
    elif direction == "left":
        new_x = piece[0] - steps * 50
        new_y = piece[1]
        if new_x < 425 and piece[1] == 375 and color == "yellow":
            new_x = piece[0]
        elif new_x <= 425 and piece[0] > 425 and piece[1] == 425:
            new_y = piece[1] + (475 - new_x)
            new_x = 425
            directions[color][index] = "down"
        elif new_x < 375 and piece[1] == height - 25 and color == "blue":
            new_y = new_y - (375 - new_x)
            new_x = 375
            directions[color][index] = "up"
        elif new_x < 325 and piece[1] == height - 25:
            new_y = new_y - (325 - new_x)
            new_x = 325
            directions[color][index] = "up"
            if new_y < 475:
                new_x = new_x - (475 - new_y)
                new_y = 425
                directions[color][index] = "left"
        elif new_x < 0:
            new_y = piece[1] - (steps * 50 - piece[0] + 25)
            new_x = 25
            directions[color][index] = "up"
            if new_y < 375 and color == "red":
                new_x = new_x + 375 - new_y
                new_y = 375
                directions[color][index] = "right"
            elif new_y < 325:
                new_x = new_x + 325 - new_y
                new_y = 325
                directions[color][index] = "right"
    elif direction == "up":
        new_x = piece[0]
        new_y = piece[1] - steps * 50
        if new_y < 425 and piece[0] == 375 and color == "blue":
            new_y = piece[1]
        elif new_y < 0:
            new_x = piece[0] + steps * 50 - piece[1] + 25
            new_y = 25
            directions[color][index] = "right"
            if new_x > 375 and color == "green":
                new_y = new_y + new_x - 375
                new_x = 375
                directions[color][index] = "down"
            elif new_x > 425:
                new_y = new_y + new_x - 425
                new_x = 425
                directions[color][index] = "down"
        elif new_y <= 425 and piece[1] > 425 and piece[0] == 325:
            new_x = piece[0] - (475 - new_y)
            new_y = 425
            directions[color][index] = "left"
        elif new_y < 375 and piece[0] == 25 and color == "red":
            new_x = new_x + 375 - new_y
            new_y = 375
            directions[color][index] = "right"
        elif new_y < 325 and piece[0] == 25:
            new_x = new_x + 325 - new_y
            new_y = 325
            directions[color][index] = "right"
            if new_x > 275:
                new_y = new_y - (new_x - 275)
                new_x = 325
                directions[color][index] = "up"

    for c, pieces in players.items():
        for i, p in enumerate(pieces):
            if p == (new_x, new_y) and (new_x, new_y) != any(starred_positions) :
                p = original_positions[c][i]

    players[color][index] = (new_x, new_y)
    

# Update the board with pieces
def update_board():
    draw_board()
    for color, pieces in players.items():
        for piece in pieces:
            pygame.draw.circle(window, black, piece, 22)
            pygame.draw.circle(window, color, piece, 20)
    pygame.display.update()


font = pygame.font.Font(None, 74)

# Roll the dice
def roll_dice():
    return random.randint(1, 6)

def display_winning_result(color):
    text = font.render(f"Winner: {color}", True, color)
    window.blit(text, (width // 2 - text.get_width() // 2, height // 2 + 50))  # Slightly below the dice result
    pygame.display.update()
    pygame.time.delay(1000)

def check_winner():
    for color, pieces in players.items():
        count = 0
        for piece in pieces:
            if piece == winning_positions.get(color):
                count = count + 1
        if count == 4:    
            display_winning_result(color)
            break

def display_dice_result(result):
    text = font.render(str(result), True, black)
    window.blit(text, (width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2))
    pygame.display.update()

def show_restart_dialog():
    dialog_width, dialog_height = 350, 150
    dialog_surface = pygame.Surface((dialog_width, dialog_height))
    dialog_surface.fill((255, 255, 255))  # White background

    # Draw border
    pygame.draw.rect(dialog_surface, (0, 0, 0), dialog_surface.get_rect(), 2)

    # Render text
    font = pygame.font.SysFont(None, 26)
    text = font.render("Are you sure you want to restart?", True, (0, 0, 0))
    dialog_surface.blit(text, (dialog_width // 2 - text.get_width() // 2, 30))

    # Buttons
    yes_button = pygame.Rect(50, 90, 80, 30)
    no_button = pygame.Rect(170, 90, 80, 30)
    pygame.draw.rect(dialog_surface, (0, 255, 0), yes_button)
    pygame.draw.rect(dialog_surface, (255, 0, 0), no_button)

    yes_text = font.render("Yes", True, (0, 0, 0))
    no_text = font.render("No", True, (0, 0, 0))
    dialog_surface.blit(yes_text, (yes_button.x + 20, yes_button.y + 5))
    dialog_surface.blit(no_text, (no_button.x + 20, no_button.y + 5))

    # Blit dialog to center of screen
    window.blit(dialog_surface, (width // 2 - dialog_width // 2, height // 2 - dialog_height // 2))
    pygame.display.update()

    # Wait for user input
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                # Adjust mouse position relative to dialog box
                rel_mouse_pos = (mouse_pos[0] - (width // 2 - dialog_width // 2),
                                 mouse_pos[1] - (height // 2 - dialog_height // 2))
                if yes_button.collidepoint(rel_mouse_pos):
                    return True
                elif no_button.collidepoint(rel_mouse_pos):
                    return False

def show_help_menu():
    help_surface = pygame.Surface((width, height))
    help_surface.fill((240, 240, 240))  # Light background

    font_title = pygame.font.SysFont(None, 48)
    font_text = pygame.font.SysFont(None, 28)

    title = font_title.render("Help Menu", True, (0, 0, 0))
    help_surface.blit(title, (width // 2 - title.get_width() // 2, 50))

    instructions = [
        "Controls:",
        "- Press 'R' to roll the dice and move the red piece.",
        "- Press 'G' to roll the dice and move the green piece.",
        "- Press 'B' to roll the dice and move the blue piece.",
        "- Press 'Y' to roll the dice and move the yellow piece.",
        "Gameplay:",
        "1. Press the keys (R, G, B, Y) to roll the dice ",
        "   for the respective colored piece.",
        "2. Press '0' to restart the game.",
        "3. Press 'H' to view this help menu.",
        "4. Reach the center to win!"
    ]

    for i, line in enumerate(instructions):
        text = font_text.render(line, True, (0, 0, 0))
        help_surface.blit(text, (50, 150 + i * 40))

    # Draw a "Back" button
    back_button = pygame.Rect(width // 2 - 50, height - 100, 100, 40)
    pygame.draw.rect(help_surface, (180, 180, 180), back_button)
    back_text = font_text.render("Back", True, (0, 0, 0))
    help_surface.blit(back_text, (back_button.x + 20, back_button.y + 5))

    window.blit(help_surface, (0, 0))
    pygame.display.update()

    # Wait for user to click "Back"
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    return

def select_piece(col):
    start_text = font.render("Select the piece to move", True, (0, 0, 0))
#    window.blit(start_text, (width // 2 - start_text.get_width() // 2, height // 2 - start_text.get_height() // 2))
    window.blit(start_text, (width // 2 - start_text.get_width() // 2, 25))
    pygame.display.update()
    pieces = players[col]
    # Wait for user to click
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for i, piece in enumerate(pieces):
                    if math.hypot(mouse_pos[0] - piece[0], mouse_pos[1] - piece[1]) < 22:
                        return i
                    
def start_screen():
    draw_board()
    dialog_width, dialog_height = 350, 150
    dialog_surface = pygame.Surface((dialog_width, dialog_height))
    dialog_surface.fill((255, 255, 255))  # White background

    # Draw border
    pygame.draw.rect(dialog_surface, (0, 0, 0), dialog_surface.get_rect(), 2)

    # Render text
    font = pygame.font.SysFont(None, 26)
    text = font.render("Do you want to start a new game?", True, (0, 0, 0))
    dialog_surface.blit(text, (dialog_width // 2 - text.get_width() // 2, 30))

    # Buttons
    yes_button = pygame.Rect(100, 90, 80, 30)
    no_button = pygame.Rect(200, 90, 80, 30)
    pygame.draw.rect(dialog_surface, (0, 255, 0), yes_button)
    pygame.draw.rect(dialog_surface, (255, 0, 0), no_button)

    yes_text = font.render("Yes", True, (0, 0, 0))
    no_text = font.render("No", True, (0, 0, 0))
    dialog_surface.blit(yes_text, (yes_button.x + 20, yes_button.y + 5))
    dialog_surface.blit(no_text, (no_button.x + 20, no_button.y + 5))

    # Blit dialog to center of screen
    window.blit(dialog_surface, (width // 2 - dialog_width // 2, height // 2 - dialog_height // 2))
    pygame.display.update()

    # Wait for user input
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                # Adjust mouse position relative to dialog box
                rel_mouse_pos = (mouse_pos[0] - (width // 2 - dialog_width // 2),
                                 mouse_pos[1] - (height // 2 - dialog_height // 2))
                if yes_button.collidepoint(rel_mouse_pos):
                    reset_game_state()
                    return True
                elif no_button.collidepoint(rel_mouse_pos):
                    return False

# Main loop with piece movement, dice roll, and display
def main():
    current_player = 0
    next_piece_to_start = [0, 0, 0, 0]
    start = [
                [False, False, False, False],
                [False, False, False, False],
                [False, False, False, False],
                [False, False, False, False]
            ]
    game_start = start_screen()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if game_start:
                    if event.key == pygame.K_r:
                        if current_player == 0:
                            steps = roll_dice()
                            display_dice_result(steps)
                            pygame.time.delay(1000)
                            if steps == 6 and sum(start[0]) < 4 and check_move_to_start("red", next_piece_to_start[0]):
                                start[0][next_piece_to_start[0]] = True
                                next_piece_to_start[0] = next_piece_to_start[0] + 1
                            else:
                                if any(start[0]):
                                    index = select_piece("red") if (sum(start[0])> 1) else (start[0]).index(True)
                                    if start[0][index]:
                                        move_piece("red", steps, index)
                                current_player = (current_player + 1) % 4
                        else:
                            c = list(control_keys.keys())[current_player]
                            text = font.render(f"Wrong turn, press {control_keys[c]} for {c}", True, c)
                            window.blit(text, (width // 2 - text.get_width() // 2, height // 2))  # Slightly below the dice result
                            pygame.display.update()
                            pygame.time.delay(1000)

                    elif event.key == pygame.K_g:
                        if current_player == 1:
                            steps = roll_dice()
                            display_dice_result(steps)
                            pygame.time.delay(1000)
                            if steps == 6 and sum(start[1]) < 4 and check_move_to_start("green", next_piece_to_start[1]):
                                start[1][next_piece_to_start[1]] = True
                                next_piece_to_start[1] = next_piece_to_start[1] + 1
                            else:
                                if any(start[1]):
                                    index = select_piece("green") if sum(start[1]) > 1 else (start[1]).index(True)
                                    if start[1][index]:
                                        move_piece("green", steps, index)
                                current_player = (current_player + 1) % 4
                        else:
                            c = list(control_keys.keys())[current_player]
                            text = font.render(f"Wrong turn, press {control_keys[c]} for {c}", True, c)
                            window.blit(text, (width // 2 - text.get_width() // 2, height // 2))  # Slightly below the dice result
                            pygame.display.update()
                            pygame.time.delay(1000)
                    elif event.key == pygame.K_b:
                        if current_player == 3:
                            steps = roll_dice()
                            display_dice_result(steps)
                            pygame.time.delay(1000)
                            if steps == 6 and sum(start[3]) < 4 and check_move_to_start("blue", next_piece_to_start[3]):
                                start[3][next_piece_to_start[3]] = True
                                next_piece_to_start[3] = next_piece_to_start[3] + 1
                            else:
                                if any(start[3]):
                                    index = select_piece("blue") if sum(start[3]) > 1 else (start[3]).index(True)
                                    if start[3][index]:
                                        move_piece("blue", steps, index)
                                current_player = (current_player + 1) % 4
                        else:
                            c = list(control_keys.keys())[current_player]
                            text = font.render(f"Wrong turn, press {control_keys[c]} for {c}", True, c)
                            window.blit(text, (width // 2 - text.get_width() // 2, height // 2))  # Slightly below the dice result
                            pygame.display.update()
                            pygame.time.delay(1000)
                    elif event.key == pygame.K_y:
                        if current_player == 2:
                            steps = roll_dice()
                            display_dice_result(steps)
                            pygame.time.delay(1000)
                            if steps == 6 and sum(start[2]) < 4 and check_move_to_start("yellow", next_piece_to_start[2]):
                                start[2][next_piece_to_start[2]] = True
                                next_piece_to_start[2] = next_piece_to_start[2] + 1
                            else:
                                if any(start[2]):
                                    index = select_piece("yellow") if sum(start[2]) > 1 else (start[2]).index(True)
                                    if start[2][index]:
                                        move_piece("yellow", steps, index)
                                current_player = (current_player + 1) % 4
                        else:
                            c = list(control_keys.keys())[current_player]
                            text = font.render(f"Wrong turn, press {control_keys[c]} for {c}", True, c)
                            window.blit(text, (width // 2 - text.get_width() // 2, height // 2 ))  # Slightly below the dice result
                            pygame.display.update()
                            pygame.time.delay(1000)
                    elif event.key == pygame.K_0:
                        restart = show_restart_dialog()
                        if restart:
                            reset_game_state()
                    elif event.key == pygame.K_h:
                        show_help_menu()
                elif event.key == pygame.K_h:
                    show_help_menu()
                elif event.key == pygame.K_s:
                    game_start = start_screen()


        update_board()
        pygame.time.delay(1000)  # Delay to see the dice result
        check_winner()
        #window.fill(white)  # Clear the screen for the next frame

if __name__ == "__main__":
    main()