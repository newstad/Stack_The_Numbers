import pygame
import random
import sys

pygame.init()

fullscreen_mode = input("Do you want to play in fullscreen mode? (yes/no): ").strip().lower()
if fullscreen_mode == "yes":
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    info = pygame.display.Info()
    WIDTH, HEIGHT = info.current_w, info.current_h
else:
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Stack the Numbers")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 255)

block_width = WIDTH // 12
block_height = HEIGHT // 30
platform_width = WIDTH // 6
platform_height = HEIGHT // 40
font_size = HEIGHT // 30
title_font_size = HEIGHT // 20
developer_font_size = HEIGHT // 40

font = pygame.font.Font(None, font_size)
title_font = pygame.font.Font(None, title_font_size)
developer_font = pygame.font.Font(None, developer_font_size)

stack = []
safe_zone_top = HEIGHT // 4
left_wall = WIDTH // 10
right_wall = WIDTH - WIDTH // 10
win_line_height = HEIGHT // 4
win_line_start_x = WIDTH // 4  # Line starts from 1/4 of the screen width
win_line_end_x = 3 * WIDTH // 4  # Line ends at 3/4 of the screen width
current_block = pygame.Rect(left_wall, safe_zone_top, block_width, block_height)
block_speed = WIDTH // 800
fall_speed = HEIGHT // 600
platform = pygame.Rect(WIDTH // 2 - platform_width // 2, HEIGHT - platform_height - 20, platform_width, platform_height)
score = 0
moving_right = True
falling = False
game_over = False
game_won = False

def generate_math_questions():
    questions = []
    for _ in range(10):
        a, b = random.randint(1, 20), random.randint(1, 20)
        questions.append({"question": f"What is {a} + {b}?", "answer": str(a + b)})
        questions.append({"question": f"What is {a} - {b}?", "answer": str(a - b)})
        questions.append({"question": f"What is {a} * {b}?", "answer": str(a * b)})
        if b != 0 and a % b == 0:
            questions.append({"question": f"What is {a} / {b}?", "answer": str(a // b)})
    return questions

def generate_options(correct_answer):
    correct_answer = int(correct_answer)
    options = {correct_answer}
    while len(options) < 4:
        options.add(correct_answer + random.randint(-10, 10))
    options = list(options)
    random.shuffle(options)
    return options

math_questions = generate_math_questions()
questions = math_questions

def draw_title():
    italic_font = pygame.font.Font(None, title_font_size)
    italic_font.set_italic(True)
    title_text = italic_font.render("Stack the Numbers", True, BLACK)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 40))

def draw_question(question_data):
    question = font.render(question_data["question"], True, BLACK)
    screen.blit(question, (WIDTH // 40, HEIGHT // 8))
    for i, option in enumerate(question_data["options"]):
        option_text = font.render(f"{i + 1}. {option}", True, BLACK)
        screen.blit(option_text, (WIDTH // 40, HEIGHT // 6 + i * (font_size + 10)))

def draw_stack():
    for block in stack:
        pygame.draw.rect(screen, GREEN, block)
        pygame.draw.rect(screen, BLACK, block, 2)

def draw_platform():
    pygame.draw.rect(screen, BLUE, platform)
    pygame.draw.rect(screen, BLACK, platform, 2)

def draw_win_line():
    pygame.draw.line(screen, RED, (win_line_start_x, win_line_height), (win_line_end_x, win_line_height), 3)

def check_answer(question_data, choice):
    return str(question_data["options"][choice]) == str(question_data["answer"])

def draw_score(score):
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (WIDTH - score_text.get_width() - WIDTH // 40, HEIGHT - score_text.get_height() - HEIGHT // 40))

def draw_game_over():
    game_over_text = title_font.render("You Lose", True, RED)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
    developer_text = developer_font.render("Developed by: William Newstad, James Murphy, and Matthew Luzzi", True, BLACK)
    screen.blit(developer_text, (WIDTH // 40, HEIGHT - developer_text.get_height() - HEIGHT // 40))

def draw_game_won():
    win_text = title_font.render("You Win!", True, GREEN)
    screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - win_text.get_height() // 2))
    developer_text = developer_font.render("Developed by: William Newstad, James Murphy, and Matthew Luzzi", True, BLACK)
    screen.blit(developer_text, (WIDTH // 40, HEIGHT - developer_text.get_height() - HEIGHT // 40))

def move_block():
    global moving_right
    if moving_right:
        current_block.x += block_speed
        if current_block.right >= right_wall:
            moving_right = False
    else:
        current_block.x -= block_speed
        if current_block.left <= left_wall:
            moving_right = True

def drop_block():
    global falling, score, game_over
    if falling:
        current_block.y += fall_speed
        for block in stack:
            if current_block.colliderect(block):
                falling = False
                current_block.y = block.top - block_height
                stack.append(current_block.copy())
                current_block.x = left_wall
                current_block.y = safe_zone_top
                score += 1
                return
        if current_block.colliderect(platform):
            falling = False
            current_block.y = platform.top - block_height
            stack.append(current_block.copy())
            current_block.x = left_wall
            current_block.y = safe_zone_top
            score += 1
        elif current_block.bottom >= HEIGHT:
            game_over = True

def check_win_condition():
    global game_won
    if stack and any(block.top <= win_line_height for block in stack):
        game_won = True

running = True
current_question = random.choice(questions)
current_question["options"] = generate_options(current_question["answer"])

while running:
    screen.fill(WHITE)
    draw_title()
    if game_won:
        draw_game_won()
    elif game_over:
        draw_game_over()
    else:
        draw_question(current_question)
        draw_stack()
        draw_platform()
        draw_win_line()
        draw_score(score)
        if not falling:
            move_block()
        else:
            drop_block()
        pygame.draw.rect(screen, GREEN, current_block)
        pygame.draw.rect(screen, BLACK, current_block, 2)
        check_win_condition()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        if not game_over and not game_won and event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                choice = event.key - pygame.K_1
                if check_answer(current_question, choice):
                    falling = True
                    current_question = random.choice(questions)
                    current_question["options"] = generate_options(current_question["answer"])
                else:
                    if stack:
                        stack.pop()
                    score -= 1
                    if score < 0:
                        game_over = True
    pygame.display.flip()

pygame.quit()
