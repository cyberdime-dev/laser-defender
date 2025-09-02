import pygame
import random
import sys

# Initialize
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 800
FPS = 60
WHITE = (255, 255, 255)
RED = (255, 50, 50)
BLUE = (50, 150, 255)
BLACK = (0, 0, 0)
GREEN = (50, 255, 100)

PADDLE_WIDTH, PADDLE_HEIGHT = 80, 20
LASER_WIDTH, LASER_HEIGHT = 4, 20
TARGET_RADIUS = 20
LASER_SPEED = 10
TARGET_SPEED = 3
SHOOT_DELAY = 300  # milliseconds

# Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Laser Defender")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Player Paddle
paddle = pygame.Rect(WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - 50, PADDLE_WIDTH, PADDLE_HEIGHT)

# Game state
lasers = []
targets = []
score = 0
last_shot_time = 0
game_over = False

# Spawn a target
def spawn_target():
    x = random.randint(TARGET_RADIUS, WIDTH - TARGET_RADIUS)
    targets.append([x, 0])  # [x, y]

# Draw everything
def draw():
    screen.fill(BLACK)
    pygame.draw.rect(screen, BLUE, paddle)

    for laser in lasers:
        pygame.draw.rect(screen, GREEN, laser)

    for tx, ty in targets:
        pygame.draw.circle(screen, RED, (tx, ty), TARGET_RADIUS)

    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))

    if game_over:
        over_text = font.render("Game Over - Press R to Restart", True, WHITE)
        screen.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 2))

# Main loop
def main():
    global score, lasers, targets, last_shot_time, game_over

    target_timer = 0

    while True:
        dt = clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        if not game_over:
            # Move paddle
            if keys[pygame.K_LEFT] and paddle.left > 0:
                paddle.x -= 7
            if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
                paddle.x += 7

            # Shoot laser
            if keys[pygame.K_SPACE] and pygame.time.get_ticks() - last_shot_time > SHOOT_DELAY:
                laser = pygame.Rect(paddle.centerx - LASER_WIDTH // 2, paddle.top - LASER_HEIGHT, LASER_WIDTH, LASER_HEIGHT)
                lasers.append(laser)
                last_shot_time = pygame.time.get_ticks()

            # Update lasers
            for laser in lasers[:]:
                laser.y -= LASER_SPEED
                if laser.bottom < 0:
                    lasers.remove(laser)

            # Spawn targets
            target_timer += dt
            if target_timer > 1000:  # every second
                spawn_target()
                target_timer = 0

            # Update targets
            for target in targets[:]:
                target[1] += TARGET_SPEED
                if target[1] > HEIGHT:
                    game_over = True
                # Collision detection
                for laser in lasers[:]:
                    if pygame.Rect(target[0] - TARGET_RADIUS, target[1] - TARGET_RADIUS,
                                   TARGET_RADIUS * 2, TARGET_RADIUS * 2).colliderect(laser):
                        try:
                            targets.remove(target)
                            lasers.remove(laser)
                        except ValueError:
                            pass
                        score += 1
                        break

        else:
            if keys[pygame.K_r]:
                # Reset game
                score = 0
                targets.clear()
                lasers.clear()
                game_over = False
                paddle.x = WIDTH // 2 - PADDLE_WIDTH // 2

        draw()
        pygame.display.flip()

# Run the game
if __name__ == "__main__":
    main()
