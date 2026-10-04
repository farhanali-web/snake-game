import pygame
import random
import os

pygame.init()

# =========================
# SCREEN
# =========================
WIDTH = 400
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Master")

clock = pygame.time.Clock()

# =========================
# COLORS
# =========================
BLACK = (18, 18, 18)
DARK = (28, 28, 28)
GREEN = (0, 210, 80)
LIGHT_GREEN = (80, 255, 130)
RED = (240, 60, 60)
WHITE = (255, 255, 255)
GRAY = (80, 80, 80)
BLUE = (50, 120, 230)
YELLOW = (255, 210, 50)

# =========================
# GAME SETTINGS
# =========================
BLOCK = 20
GAME_HEIGHT = 500

font_big = pygame.font.Font(None, 55)
font = pygame.font.Font(None, 32)
font_small = pygame.font.Font(None, 25)

# =========================
# HIGH SCORE
# =========================
high_score_file = "highscore.txt"

def load_high_score():
    try:
        if os.path.exists(high_score_file):
            with open(high_score_file, "r") as file:
                return int(file.read())
    except:
        pass

    return 0


def save_high_score(score):
    try:
        with open(high_score_file, "w") as file:
            file.write(str(score))
    except:
        pass


high_score = load_high_score()

# =========================
# BUTTONS
# =========================
start_button = pygame.Rect(100, 300, 200, 60)
restart_button = pygame.Rect(100, 350, 200, 60)

up_button = pygame.Rect(150, 535, 100, 45)
down_button = pygame.Rect(150, 645, 100, 45)
left_button = pygame.Rect(35, 590, 100, 45)
right_button = pygame.Rect(265, 590, 100, 45)

# =========================
# GAME VARIABLES
# =========================
snake = []
food = None

direction = "RIGHT"

score = 0
level = 1
speed = 8

game_started = False
game_over = False


# =========================
# CREATE FOOD
# =========================
def create_food():

    while True:

        new_food = (
            random.randrange(0, WIDTH, BLOCK),
            random.randrange(0, GAME_HEIGHT, BLOCK)
        )

        if new_food not in snake:
            return new_food


# =========================
# START / RESET GAME
# =========================
def reset_game():

    global snake
    global food
    global direction
    global score
    global level
    global speed
    global game_over

    snake = [
        (200, 200),
        (180, 200),
        (160, 200)
    ]

    direction = "RIGHT"

    score = 0
    level = 1
    speed = 8

    food = create_food()

    game_over = False


# =========================
# DRAW TEXT
# =========================
def draw_text(text, font_used, color, x, y):

    text_surface = font_used.render(
        text,
        True,
        color
    )

    screen.blit(text_surface, (x, y))


# =========================
# MAIN LOOP
# =========================
running = True

while running:

    # =====================
    # EVENTS
    # =====================
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            x, y = event.pos

            # -----------------
            # START BUTTON
            # -----------------
            if not game_started:

                if start_button.collidepoint(x, y):

                    reset_game()
                    game_started = True

            # -----------------
            # RESTART BUTTON
            # -----------------
            elif game_over:

                if restart_button.collidepoint(x, y):

                    reset_game()

            # -----------------
            # CONTROLS
            # -----------------
            elif not game_over:

                if up_button.collidepoint(x, y):

                    if direction != "DOWN":
                        direction = "UP"

                elif down_button.collidepoint(x, y):

                    if direction != "UP":
                        direction = "DOWN"

                elif left_button.collidepoint(x, y):

                    if direction != "RIGHT":
                        direction = "LEFT"

                elif right_button.collidepoint(x, y):

                    if direction != "LEFT":
                        direction = "RIGHT"


    # =====================
    # GAME LOGIC
    # =====================
    if game_started and not game_over:

        # Current head
        head_x, head_y = snake[0]

        # Movement
        if direction == "UP":
            head_y -= BLOCK

        elif direction == "DOWN":
            head_y += BLOCK

        elif direction == "LEFT":
            head_x -= BLOCK

        elif direction == "RIGHT":
            head_x += BLOCK

        new_head = (head_x, head_y)

        # -----------------
        # COLLISION
        # -----------------
        if (
            head_x < 0
            or head_x >= WIDTH
            or head_y < 0
            or head_y >= GAME_HEIGHT
            or new_head in snake
        ):

            game_over = True

            # High score
            if score > high_score:

                high_score = score
                save_high_score(high_score)

        else:

            snake.insert(0, new_head)

            # -----------------
            # FOOD
            # -----------------
            if new_head == food:

                score += 1

                # New food
                food = create_food()

                # Level increase
                new_level = (score // 5) + 1

                if new_level > level:

                    level = new_level

                    # Increase speed
                    speed = min(18, 8 + (level - 1) * 2)

                # High score
                if score > high_score:

                    high_score = score
                    save_high_score(high_score)

            else:

                snake.pop()


    # =====================
    # DRAW BACKGROUND
    # =====================
    screen.fill(BLACK)

    # Game area
    pygame.draw.rect(
        screen,
        DARK,
        (0, 0, WIDTH, GAME_HEIGHT)
    )

    # =====================
    # START SCREEN
    # =====================
    if not game_started:

        draw_text(
            "SNAKE MASTER",
            font_big,
            GREEN,
            82,
            130
        )

        draw_text(
            "High Score: " + str(high_score),
            font,
            WHITE,
            125,
            210
        )

        pygame.draw.rect(
            screen,
            BLUE,
            start_button,
            border_radius=12
        )

        draw_text(
            "START GAME",
            font,
            WHITE,
            135,
            318
        )

    # =====================
    # GAME SCREEN
    # =====================
    else:

        # Score
        draw_text(
            "Score: " + str(score),
            font_small,
            WHITE,
            10,
            10
        )

        # High Score
        draw_text(
            "Best: " + str(high_score),
            font_small,
            YELLOW,
            150,
            10
        )

        # Level
        draw_text(
            "Level: " + str(level),
            font_small,
            LIGHT_GREEN,
            300,
            10
        )

        # -----------------
        # SNAKE
        # -----------------
        for i, part in enumerate(snake):

            if i == 0:

                pygame.draw.rect(
                    screen,
                    LIGHT_GREEN,
                    (part[0], part[1], BLOCK, BLOCK),
                    border_radius=5
                )

            else:

                pygame.draw.rect(
                    screen,
                    GREEN,
                    (part[0], part[1], BLOCK, BLOCK),
                    border_radius=4
                )

        # -----------------
        # FOOD
        # -----------------
        pygame.draw.rect(
            screen,
            RED,
            (food[0], food[1], BLOCK, BLOCK),
            border_radius=5
        )

        # =================
        # GAME OVER
        # =================
        if game_over:

            draw_text(
                "GAME OVER",
                font_big,
                RED,
                105,
                220
            )

            draw_text(
                "Score: " + str(score),
                font,
                WHITE,
                155,
                275
            )

            pygame.draw.rect(
                screen,
                BLUE,
                restart_button,
                border_radius=12
            )

            draw_text(
                "RESTART",
                font,
                WHITE,
                150,
                368
            )

    # =====================
    # CONTROL BUTTONS
    # =====================
    if game_started and not game_over:

        pygame.draw.rect(
            screen,
            BLUE,
            up_button,
            border_radius=10
        )

        pygame.draw.rect(
            screen,
            BLUE,
            down_button,
            border_radius=10
        )

        pygame.draw.rect(
            screen,
            BLUE,
            left_button,
            border_radius=10
        )

        pygame.draw.rect(
            screen,
            BLUE,
            right_button,
            border_radius=10
        )

        draw_text("▲", font, WHITE, 190, 545)
        draw_text("▼", font, WHITE, 190, 655)
        draw_text("◀", font, WHITE, 75, 600)
        draw_text("▶", font, WHITE, 305, 600)

    # =====================
    # UPDATE
    # =====================
    pygame.display.update()

    clock.tick(speed)


pygame.quit()