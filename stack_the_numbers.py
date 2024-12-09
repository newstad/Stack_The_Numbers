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
GRAY = (200, 200, 200)

block_width = WIDTH // 12
block_height = HEIGHT // 25
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
win_line_start_x = WIDTH // 4
win_line_end_x = 3 * WIDTH // 4
current_block = pygame.Rect(left_wall, safe_zone_top, block_width, block_height)
block_speed = WIDTH // 800
fall_speed = HEIGHT // 600
platform = pygame.Rect(WIDTH // 2 - platform_width // 2, HEIGHT - platform_height - 20, platform_width, platform_height)
score = 0
moving_right = True
falling = False
game_over = False
game_won = False
game_started = False

def reset_game():
    global stack, score, current_block, falling, moving_right, game_over, game_won, questions, current_question
    stack = []
    score = 0
    current_block = pygame.Rect(left_wall, safe_zone_top, block_width, block_height)
    falling = False
    moving_right = True
    game_over = False
    game_won = False
    questions = generate_math_questions()
    current_question = random.choice(questions)
    current_question["options"] = generate_options(current_question["answer"])

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

def draw_start_screen():
    lines = [
        "Welcome to Stack the Numbers.",
        "The goal of this game is to get as many math questions right as possible.",
        "Stack the block tower high enough to touch the black line.",
        "If you get a question wrong, you lose a point.",
        "If you miss the tower, you automatically lose the game.",
        "Select the correct answer using the a, b, c, and d keys.",
        "Click the key when the green block is over the blue platform to drop it.",
        "Press ENTER to begin."
    ]
    y_offset = HEIGHT // 5
    for line in lines:
        text = font.render(line, True, BLACK)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, y_offset))
        y_offset += font_size + 10

def draw_question(question_data):
    question = font.render(question_data["question"], True, BLACK)
    screen.blit(question, (WIDTH // 40, HEIGHT // 8))
    for i, option in enumerate(question_data["options"]):
        labels = ["a", "b", "c", "d"]
        option_text = font.render(f"{labels[i]}. {option}", True, BLACK)
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
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))
    play_again_button = pygame.Rect(WIDTH - 220, HEIGHT - 80, 200, 50)
    pygame.draw.rect(screen, GRAY, play_again_button)
    pygame.draw.rect(screen, BLACK, play_again_button, 2)
    play_again_text = font.render("Play Again", True, BLACK)
    screen.blit(play_again_text, (play_again_button.centerx - play_again_text.get_width() // 2, play_again_button.centery - play_again_text.get_height() // 2))
    developer_text = developer_font.render("Developed by: William Newstad, James Murphy, and Matthew Luzzi", True, BLACK)
    screen.blit(developer_text, (WIDTH // 40, HEIGHT - developer_text.get_height() - HEIGHT // 40))
    return play_again_button

def draw_game_won():
    win_text = title_font.render("You Win!", True, GREEN)
    screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 3))
    play_again_button = pygame.Rect(WIDTH - 220, HEIGHT - 80, 200, 50)
    pygame.draw.rect(screen, GRAY, play_again_button)
    pygame.draw.rect(screen, BLACK, play_again_button, 2)
    play_again_text = font.render("Play Again", True, BLACK)
    screen.blit(play_again_text, (play_again_button.centerx - play_again_text.get_width() // 2, play_again_button.centery - play_again_text.get_height() // 2))
    developer_text = developer_font.render("Developed by: William Newstad, James Murphy, and Matthew Luzzi", True, BLACK)
    screen.blit(developer_text, (WIDTH // 40, HEIGHT - developer_text.get_height() - HEIGHT // 40))
    return play_again_button

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
    if stack and any(block.top < win_line_height for block in stack):
        game_won = True

running = True
current_question = random.choice(questions)
current_question["options"] = generate_options(current_question["answer"])

while running:
    screen.fill(WHITE)
    if not game_started:
        draw_start_screen()
    elif game_won:
        play_again_button = draw_game_won()
        mouse_pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            if play_again_button.collidepoint(mouse_pos):
                reset_game()
    elif game_over:
        play_again_button = draw_game_over()
        mouse_pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            if play_again_button.collidepoint(mouse_pos):
                reset_game()
    else:
        draw_title()
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
        if not game_started and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            game_started = True
        if game_started and not game_won and not game_over and event.type == pygame.KEYDOWN:
            labels = ["a", "b", "c", "d"]
            if event.unicode in labels:
                choice = labels.index(event.unicode)
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
