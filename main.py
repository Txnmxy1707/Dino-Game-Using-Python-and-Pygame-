import pygame
import sys
import random

pygame.init()

# ---------------- IMAGE LOADING ----------------
try:
    dino_frames = [
        pygame.transform.scale(pygame.image.load("dino running 1.png"), (110, 110)),
        pygame.transform.scale(pygame.image.load("dino running 2.png"), (110, 110)),
        pygame.transform.scale(pygame.image.load("dino running 3.png"), (110, 110))
    ]
    cactus_img = pygame.transform.scale(pygame.image.load("cactus.png"), (80, 70))
    background_img = pygame.transform.scale(pygame.image.load("background.png"), (800, 400))
except Exception as e:
    print("Error loading image:", e)
    pygame.quit()
    sys.exit()

# ---------------- WEATHER SETUP ----------------
weather_modes = ["rain", "summer", "winter"]
current_weather = random.choice(weather_modes)

# Window setup
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Game")

clock = pygame.time.Clock()

# ---------------- DINO SETUP ----------------
current_frame = 0
frame_counter = 0
dino_x, dino_y = 50, 150

# Cactus setup
cacti = [WIDTH + 300, WIDTH + 600]
cactus_y = 190
cactus_speed = 9

# Jump variables
is_jumping = False
velocity = 1
gravity = 1
jump_strength = -18

# Fonts
font = pygame.font.SysFont(None, 30)
game_over_font = pygame.font.SysFont(None, 100)
menu_font = pygame.font.SysFont(None, 80)
option_font = pygame.font.SysFont(None, 40)

# Score setup
score = 0
high_score = 0
last_speed_increase = 0

# ---------------- MENU SYSTEM ----------------
def show_menu():
    global high_score, score, cacti, cactus_speed, dino_y
    # Reset game state when menu opens
    score = 0
    cacti = [WIDTH + 300, WIDTH + 600]
    cactus_speed = 9
    dino_y = 150

    waiting = True
    while waiting:
        screen.fill((230, 230, 250))  # pastel lavender

        title_text = menu_font.render("Dino Game", True, (0, 0, 0))
        start_text = option_font.render("Press S to Start", True, (0, 0, 0))
        quit_text = option_font.render("Press Q to Quit", True, (0, 0, 0))
        high_text = option_font.render("Press H for High Scores", True, (0, 0, 0))
        weather_text = option_font.render(f"Weather: {current_weather.capitalize()}", True, (0, 0, 0))

        screen.blit(title_text, (WIDTH // 2 - 150, HEIGHT // 2 - 150))
        screen.blit(start_text, (WIDTH // 2 - 120, HEIGHT // 2))
        screen.blit(quit_text, (WIDTH // 2 - 120, HEIGHT // 2 + 50))
        screen.blit(high_text, (WIDTH // 2 - 120, HEIGHT // 2 + 100))
        screen.blit(weather_text, (WIDTH // 2 - 120, HEIGHT // 2 + 150))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    waiting = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_h:
                    show_high_scores()

def show_high_scores():
    global high_score
    waiting = True
    while waiting:
        screen.fill((255, 255, 255))
        text = option_font.render(f"High Score: {high_score}", True, (0, 0, 0))
        back_text = option_font.render("Press B to go back", True, (0, 0, 0))

        screen.blit(text, (WIDTH // 2 - 100, HEIGHT // 2 - 20))
        screen.blit(back_text, (WIDTH // 2 - 120, HEIGHT // 2 + 50))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    waiting = False

# ---------------- GAME OVER ----------------
def show_game_over(final_score, high_score):
    screen.fill((230, 230, 250))  # pastel lavender
    text = game_over_font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(text, (WIDTH // 2 - 234, HEIGHT // 2 - 60))

    final_text = font.render(f"Score: {final_score}", True, (0, 0, 0))
    screen.blit(final_text, (430, 250))

    high_text = font.render(f"High Score: {high_score}", True, (0, 0, 0))
    screen.blit(high_text, (230, 250))

    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False
                global current_weather
                current_weather = random.choice(weather_modes)
                show_menu()

# ---------------- WEATHER EFFECTS ----------------
rain_drops = [[random.randint(0, WIDTH), random.randint(0, HEIGHT)] for _ in range(50)]

def draw_rain():
    for drop in rain_drops:
        pygame.draw.line(screen, (0, 0, 255), (drop[0], drop[1]), (drop[0], drop[1] + 5), 2)
        drop[1] += 5
        if drop[1] > HEIGHT:
            drop[0] = random.randint(0, WIDTH)
            drop[1] = random.randint(-20, -5)

def draw_winter():
    fog_surface = pygame.Surface((WIDTH, HEIGHT))
    fog_surface.set_alpha(120)
    fog_surface.fill((220, 220, 220))
    screen.blit(fog_surface, (0, 0))

def draw_summer():
    sun_surface = pygame.Surface((WIDTH, HEIGHT))
    sun_surface.set_alpha(50)
    sun_surface.fill((255, 255, 150))
    screen.blit(sun_surface, (0, 0))

# ---------------- MAIN GAME LOOP ----------------
show_menu()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not is_jumping:
                is_jumping = True
                velocity = jump_strength

    # Update Dino position
    if is_jumping:
        dino_y += velocity
        velocity += gravity
        if dino_y >= 150:
            dino_y = 150
            is_jumping = False

    # Update cactus position
    for i in range(len(cacti)):
        cacti[i] -= cactus_speed
        if cacti[i] < -40:
            cacti[i] = WIDTH + random.randint(300, 700)
            cactus_speed = random.randint(8, 11)
            score += 1

    # Collision detection
    dino_rect = pygame.Rect(dino_x + 10, dino_y + 10,
                            dino_frames[current_frame].get_width() - 20,
                            dino_frames[current_frame].get_height() - 20)
    for i in range(len(cacti)):
        cactus_rect = pygame.Rect(cacti[i] + 10, cactus_y + 10,
                                  cactus_img.get_width() - 20,
                                  cactus_img.get_height() - 20)
        if dino_rect.colliderect(cactus_rect):
            show_game_over(score, high_score)
            dino_y = 150
            cacti = [WIDTH + 300, WIDTH + 600]
            score = 0
            cactus_speed = 9
            last_speed_increase = 0

    # Speed increase system
    if score >= last_speed_increase + 10:
        cactus_speed += 1
        last_speed_increase = score

    if score > high_score:
        high_score = score

    # Draw background
    screen.blit(background_img, (0, 0))

    # Apply chosen weather
    if current_weather == "rain":
        draw_rain()
    elif current_weather == "winter":
        draw_winter()
    elif current_weather == "summer":
        draw_summer()

    # Dino animation (freeze while jumping)
    if not is_jumping:
        frame_counter += 1
        if frame_counter >= 6:
            current_frame = (current_frame + 1) % len(dino_frames)
            frame_counter = 0
    else:
        current_frame = 1  # neutral jump frame

    # Draw Dino and cactus
    screen.blit(dino_frames[current_frame], (dino_x, dino_y))
    for i in range(len(cacti)):
        screen.blit(cactus_img, (cacti[i], cactus_y))

    # Draw scores
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    high_score_text = font.render(f"High Score: {high_score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    screen.blit(high_score_text, (10, 40))

    # Refresh screen
    pygame.display.update()
    clock.tick(60)
