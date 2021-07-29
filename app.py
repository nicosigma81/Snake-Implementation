from random import randint
import pygame
import time

apple_num = 1
apples = set()
apples_collected = 0

grid = 20
win_x, win_y = (800, 600)
side_len = min(win_x, win_y) - 200
sq_len = side_len // grid

offset_x = (win_x - side_len) // 2
offset_y = (win_y - side_len) // 2

# Snake list order [(tail_n, tail_n) ..., (tail1, tail1), (head, head)]
snake = [(3, 4), (4, 4)]

# Direction vector. Ex. (1, 0) is moving right; make negative for up and left.
direction = (0, 0)


def read_high_score():
    file = open('file.txt', 'r')
    score = file.read()
    file.close()

    return int(score.replace('highscore ', ''))


def pos_to_grid(pos):
    x, y = pos
    return (x - offset_x) // sq_len, (y - offset_y) // sq_len


def grid_to_pos(grid_pos):
    x, y = grid_pos
    return sq_len * x + offset_x, sq_len * y + offset_y


def update(s, sdir):
    new_s = s
    new_h = (s[-1][0] + sdir[0], s[-1][1] + sdir[1])

    if not (sdir == (0, 0)):
        new_s.remove(s[0])
        new_s.append(new_h)

    return new_s


def add_apple():
    new = (randint(0, grid), randint(0, grid))
    if new in snake:
        add_apple()
    else:
        apples.add(new)


def generate_apples():
    for i in range(apple_num):
        apples.add((randint(0, grid), randint(0, grid)))


highscore = read_high_score()
if not read_high_score():
    highscore = 0


pygame.init()
screen = pygame.display.set_mode((win_x, win_y))
pygame.display.set_caption('Snake')

font = pygame.font.Font('freesansbold.ttf', 24)
font2 = pygame.font.Font('freesansbold.ttf', 18)
generate_apples()

BACKGROUND = (100, 100, 100)

running = True
game_lost = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:

            file = open('file.txt', 'w')
            file.write(f'highscore {highscore}')
            file.close()

            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and not direction == (0, 1):
                direction = (0, -1)
            elif event.key == pygame.K_DOWN and not direction == (0, -1):
                direction = (0, 1)
            elif event.key == pygame.K_RIGHT and not direction == (-1, 0):
                direction = (1, 0)
            elif event.key == pygame.K_LEFT and not direction == (1, 0) and not direction == (0, 0):
                direction = (-1, 0)

        if game_lost:
            # Game reset
            time.sleep(0.3)

            apple_num = 1
            apples = set()
            apples_collected = 0

            snake = [(3, 4), (4, 4)]
            direction = (0, 0)

            generate_apples()

            game_lost = False

    # Draw background
    screen.fill(BACKGROUND)
    pygame.draw.rect(screen, (70, 70, 70), pygame.Rect(offset_x, offset_y, side_len + sq_len, side_len + sq_len), 0)

    text = font.render(f"Apples: {apples_collected}", True, (255, 255, 255), BACKGROUND)
    textRect = text.get_rect()
    textRect.update(offset_x, offset_y - 40, side_len, 20)
    screen.blit(text, textRect)

    text = font.render(f"High Score: {highscore}", True, (255, 255, 255), BACKGROUND)
    textRect = text.get_rect()
    textRect.update(offset_x, offset_y - 70, side_len, 20)
    screen.blit(text, textRect)

    # ---------------
    # Game Update
    # ---------------

    # Collect apples
    if snake[-1] in apples:
        apples.remove(snake[-1])
        apples_collected += 1

        if apples_collected > highscore:
            highscore = apples_collected

        n_add = 2
        for i in range(n_add):
            end = (snake[0][0], snake[0][1])
            snake.insert(0, end)

    if not len(apples) == apple_num:
        add_apple()

    # Self intersection
    next_ = (snake[-1][0] + direction[0], snake[-1][1] + direction[1])
    for i in range(len(snake)):
        if next_ in snake[1:-1]:
            game_lost = True

    # Grid intersection
    if not (0 <= next_[0] <= grid):
        game_lost = True
    if not (0 <= next_[1] <= grid):
        game_lost = True

    # Snake update
    if not game_lost:
        time.sleep(0.09)
        snake = update(snake, direction)

    # ---------------
    # Game Display
    # ---------------

    # Draw apples
    for apple in apples:
        x, y = grid_to_pos(apple)
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(x, y, sq_len, sq_len), 0)

    # Draw snake
    for piece in snake:
        COLOUR = (255, 255, 255)
        x, y = grid_to_pos(piece)
        pygame.draw.rect(screen, COLOUR, pygame.Rect(x, y, sq_len, sq_len), 0)

    if game_lost:
        rect1 = pygame.Rect(0, 0, 300, 120)
        rect1.center = (win_x // 2, win_y // 2 + 10)
        pygame.draw.rect(screen, (180, 180, 180), rect1)

        text = font.render("You Lost!", True, (255, 0, 0))
        textRect = text.get_rect()
        textRect.center = (offset_x + side_len // 2, offset_y + side_len // 2)
        screen.blit(text, textRect)

        text = font2.render("Press anywhere to play again", True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (offset_x + side_len // 2, offset_y + side_len // 2 + 30)
        screen.blit(text, textRect)

    pygame.display.update()
