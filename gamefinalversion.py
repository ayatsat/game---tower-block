import pygame
import random

# Инициализация Pygame
pygame.init()

# Размеры окна игры
WIDTH = 400
HEIGHT = 600

# Загрузка музыки
pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.set_volume(0.5)

# Загрузка звуковых эффектов
fall_sound = pygame.mixer.Sound("fall_sound.mp3")
game_over = pygame.mixer.Sound("gameover.mp3")
miss_sound = pygame.mixer.Sound("miss_sound.mp3")

# Параметры блоков
BLOCK_WIDTH = 70
BLOCK_HEIGHT = 50
BLOCK_SPEED = 5

block_image = pygame.image.load("block_image.png")
block_image = pygame.transform.scale(block_image, (BLOCK_WIDTH, BLOCK_HEIGHT))

# Перезапуск игры
BUTTON_WIDTH = 120
BUTTON_HEIGHT = 40
BUTTON_COLOR = (0, 255, 0)
BUTTON_TEXT_COLOR = (0, 0, 0)

# Загрузка фонового изображения
background_image = pygame.image.load("background.jpg")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Цвета
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Создание окна игры
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tower Blocks")

clock = pygame.time.Clock()

# Параметры платформы
PLATFORM_WIDTH = 70
PLATFORM_HEIGHT = 10
PLATFORM_COLOR = RED

# Переменные игры
platform_x = (WIDTH - PLATFORM_WIDTH) // 2
block_x = random.randint(0, WIDTH - BLOCK_WIDTH)
block_y = 40
score = 0
misses = 0
block_falling = False  # Флаг падения блока
block_direction = 1  # Направление движения блока (1 - вправо, -1 - влево)
block_speed = 3
fallen_blocks = []
best_score = 0  # Лучший результат

def draw_platform(x):
    """Отрисовка платформы"""
    pygame.draw.rect(screen, PLATFORM_COLOR, (x, HEIGHT - PLATFORM_HEIGHT, PLATFORM_WIDTH, PLATFORM_HEIGHT))

def draw_block(x, y):
    """Отрисовка блока"""
    screen.blit(block_image, (x, y))

def display_score(score):
    """Отображение текущего счета"""
    font = pygame.font.Font(None, 36)
    text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(text, (10, 10))

def display_misses(misses):
    """Отображение количества пропущенных блоков"""
    font = pygame.font.Font(None, 36)
    text = font.render("Misses: " + str(misses), True, WHITE)
    screen.blit(text, (WIDTH - 150, 10))
    
def restart_game():
    """Перезапуск игры"""
    global platform_x, block_x, block_y, score, misses, block_falling, block_direction, fallen_blocks, best_score
    platform_x = (WIDTH - PLATFORM_WIDTH) // 2
    block_x = random.randint(0, WIDTH - BLOCK_WIDTH)
    block_y = 40
    if score > best_score:
        best_score = score
    score = 0
    misses = 0
    block_falling = False
    block_direction = 1
    fallen_blocks = []

def display_score(score):
    """Отображение текущего счета и лучшего результата"""
    font = pygame.font.Font(None, 36)
    text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(text, (10, 10))
    best_text = font.render("Best: " + str(best_score), True, WHITE)
    screen.blit(best_text, (10, 50))

def draw_button():
    """Отрисовка кнопки перезапуска"""
    font = pygame.font.Font(None, 30)
    text = font.render("Press 'R'", True, BUTTON_TEXT_COLOR)
    button_x = (WIDTH - BUTTON_WIDTH) // 2
    button_y = (HEIGHT - BUTTON_HEIGHT) // 2
    pygame.draw.rect(screen, BUTTON_COLOR, (button_x, button_y, BUTTON_WIDTH, BUTTON_HEIGHT))
    text_rect = text.get_rect(center=(button_x + BUTTON_WIDTH // 2, button_y + BUTTON_HEIGHT // 2))
    screen.blit(text, text_rect)

# Основной цикл игры
pygame.mixer.music.play(-1)
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not block_falling:
                block_falling = True
            elif event.key == pygame.K_r and misses >= 3:
                if score > best_score:
                    best_score = score  # Обновление лучшего результата
                restart_game()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if misses >= 3:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                button_x = (WIDTH - BUTTON_WIDTH) // 2
                button_y = (HEIGHT - BUTTON_HEIGHT) // 2
                if button_x <= mouse_x <= button_x + BUTTON_WIDTH and button_y <= mouse_y <= button_y + BUTTON_HEIGHT:
                    if score > best_score:
                        best_score = score  # Обновление лучшего результата
                    restart_game()

    # Отрисовка фонового изображения
    screen.blit(background_image, (0, 0))

    if score % 11 == 0 and score != 0:
        fallen_blocks = []
        
    if not block_falling:
        # Движение блока вправо-влево
        block_x += block_direction * block_speed
        if block_x <= 0 or block_x >= WIDTH - BLOCK_WIDTH:
            block_direction *= -1
            block_x += block_direction * block_speed

    if block_falling:
        if block_y + BLOCK_HEIGHT >= HEIGHT - PLATFORM_HEIGHT - (score % 11) * BLOCK_HEIGHT and platform_x <= block_x + PLATFORM_WIDTH // 2 <= platform_x + PLATFORM_WIDTH:
            # Блок попал на платформу
            score += 1
            fall_sound.play()
            fallen_blocks.append((block_x, block_y + (score % 11 - 1) * BLOCK_HEIGHT))
            block_x = random.randint(0, WIDTH - BLOCK_WIDTH)
            block_y = 40
            block_falling = False  # Сброс флага падения блока
        else:
            block_y += BLOCK_SPEED  # Падение блока

    # Проверка достижения границ экрана блоком
    if block_x <= 0 or block_x >= WIDTH - BLOCK_WIDTH:
        block_direction *= -1  # Изменение направления движения блока

    # Проверка падения блока
    if block_y + BLOCK_HEIGHT >= HEIGHT:
        # Блок упал
        misses += 1
        block_x = random.randint(0, WIDTH - BLOCK_WIDTH)
        miss_sound.play()
        block_y = 40
        block_falling = False  # Сброс флага падения блока

    for i, fallen_block in enumerate(fallen_blocks):
        draw_block(fallen_block[0], fallen_block[1] - i * BLOCK_HEIGHT)  # Выстраивание блоков в башню

    # Отрисовка платформы, блока и текущих результатов
    draw_platform(platform_x)
    draw_block(block_x, block_y)
    display_score(score)
    display_misses(misses)

    # Проверка окончания игры
    if misses >= 3:
        game_over.play()
        font = pygame.font.Font(None, 48)
        text = font.render("Game Over", True, WHITE)
        screen.blit(text, (WIDTH // 2 - 100, HEIGHT // 2 + 50))
        draw_button()
        pygame.display.flip()
        pygame.time.wait(2000)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
