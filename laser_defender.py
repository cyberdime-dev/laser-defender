import pygame
import random
import sys
import math

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
LASER_WIDTH, LASER_HEIGHT = 8, 25  # Made wider and taller for better visibility
TARGET_RADIUS = 20
LASER_SPEED = 10
TARGET_SPEED = 3
SHOOT_DELAY = 300  # ms

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

# Laser style: 1..5 (toggle in game with number keys)
LASER_STYLE = 1

STYLE_NAMES = {
    1: "Rect (sharp)",
    2: "Line (beam)",
    3: "Glow (outer+core)",
    4: "Capsule (rounded)",
    5: "Neon (stacked lines)"
}

# Sound effects
def create_sound_effects():
    """Create simple sound effects using pygame's built-in sound generation"""
    sounds = {}
    
    try:
        # Create simple beep sounds using pygame's built-in capabilities
        # We'll create very basic sounds that don't require numpy
        
        # For now, we'll use a simple approach - create empty sounds and mark them as available
        # This will allow the game to run without numpy while still having sound structure
        
        print("Creating basic sound effects...")
        
        # Create a simple beep sound using pygame's built-in sound generation
        sample_rate = 22050
        duration = 100  # 100ms
        
        # Create a simple sine wave beep
        samples = int(sample_rate * duration / 1000)
        sound_data = []
        
        for i in range(samples):
            # Simple sine wave at 800Hz
            value = int(127 + 127 * math.sin(2 * math.pi * 800 * i / sample_rate))
            sound_data.append(value)
        
        # Convert to pygame sound using a different approach
        try:
            # Try to create a simple sound buffer
            import array
            sound_buffer = array.array('h', sound_data)
            shoot_sound = pygame.mixer.Sound(buffer=sound_buffer)
            sounds['shoot'] = shoot_sound
            print("Shoot sound created successfully")
        except:
            # Fallback: create a dummy sound
            print("Using fallback sound system")
            sounds['shoot'] = None
        
        # Create hit sound (lower frequency)
        hit_data = []
        for i in range(samples):
            value = int(127 + 127 * math.sin(2 * math.pi * 400 * i / sample_rate))
            hit_data.append(value)
        
        try:
            hit_buffer = array.array('h', hit_data)
            hit_sound = pygame.mixer.Sound(buffer=hit_buffer)
            sounds['hit'] = hit_sound
            print("Hit sound created successfully")
        except:
            sounds['hit'] = None
        
        # Create game over sound (descending tone)
        game_over_data = []
        for i in range(samples * 2):  # Longer duration
            freq = 600 - (400 * i / (samples * 2))  # Descending frequency
            value = int(127 + 127 * math.sin(2 * math.pi * freq * i / sample_rate))
            game_over_data.append(value)
        
        try:
            game_over_buffer = array.array('h', game_over_data)
            game_over_sound = pygame.mixer.Sound(buffer=game_over_buffer)
            sounds['game_over'] = game_over_sound
            print("Game over sound created successfully")
        except:
            sounds['game_over'] = None
        
        print("Sound effects initialization complete!")
        return sounds
        
    except Exception as e:
        print(f"Error creating sound effects: {e}")
        return {}

def play_sound(sound_name):
    """Safely play a sound if it exists"""
    if SOUND_ENABLED and sound_name in sounds and sounds[sound_name] is not None:
        try:
            sounds[sound_name].play()
        except:
            pass  # Silently fail if sound can't play

# Initialize sounds
sounds = create_sound_effects()
SOUND_ENABLED = len(sounds) > 0

# Background music (simple loop)
def play_background_music():
    """Play a simple background music loop"""
    if not SOUND_ENABLED:
        print("Sound not enabled, skipping background music")
        return
    
    try:
        # Create a simple background music pattern
        sample_rate = 22050
        duration = 2000  # 2 seconds
        samples = int(sample_rate * duration / 1000)
        
        # Create a simple melody pattern
        melody = []
        for i in range(samples):
            t = i / sample_rate
            # Simple arpeggio pattern
            freq1 = 220 + 110 * math.sin(2 * math.pi * 0.5 * t)  # A3 + E4
            freq2 = 330 + 165 * math.sin(2 * math.pi * 0.75 * t)  # E4 + A4
            
            value1 = int(64 + 32 * math.sin(2 * math.pi * freq1 * t))
            value2 = int(64 + 32 * math.sin(2 * math.pi * freq2 * t))
            
            melody.append((value1 + value2) // 2)
        
        # Convert to sound using array buffer
        try:
            import array
            sound_buffer = array.array('h', melody)
            bg_sound = pygame.mixer.Sound(buffer=sound_buffer)
            bg_sound.set_volume(0.3)  # Lower volume for background
            
            # Start background music loop
            bg_sound.play(-1)  # -1 means loop indefinitely
            print("Background music started!")
            
        except Exception as e:
            print(f"Could not create background music: {e}")
        
    except Exception as e:
        print(f"Could not play background music: {e}")

# Game state
background_music_started = False

def spawn_target():
    x = random.randint(TARGET_RADIUS, WIDTH - TARGET_RADIUS)
    targets.append([x, 0])  # [x, y]

def draw_laser(laser: pygame.Rect, style: int):
    """Render a laser rect using the chosen visual style."""
    if style == 1:
        # Classic rectangle, sharp edges
        pygame.draw.rect(screen, GREEN, laser, border_radius=0)

    elif style == 2:
        # Thick line beam centered on the rect
        pygame.draw.line(screen, GREEN, (laser.centerx, laser.bottom), (laser.centerx, laser.top), 6)

    elif style == 3:
        # Glowing beam: thicker dim outer, bright inner
        pygame.draw.line(screen, (0, 150, 0), (laser.centerx, laser.bottom), (laser.centerx, laser.top), 12)
        pygame.draw.line(screen, (0, 255, 0), (laser.centerx, laser.bottom), (laser.centerx, laser.top), 6)

    elif style == 4:
        # Rounded "capsule" laser using border_radius
        pygame.draw.rect(screen, GREEN, laser, border_radius=min(laser.width, laser.height) // 2)

    elif style == 5:
        # Neon-ish stacked lines (fake gradient) - made thicker
        pygame.draw.line(screen, (0, 255, 0), (laser.centerx, laser.bottom), (laser.centerx, laser.top), 8)
        pygame.draw.line(screen, (0, 200, 100), (laser.centerx - 2, laser.bottom), (laser.centerx - 2, laser.top), 4)
        pygame.draw.line(screen, (0, 100, 255), (laser.centerx + 2, laser.bottom), (laser.centerx + 2, laser.top), 4)
    else:
        # Fallback
        pygame.draw.rect(screen, GREEN, laser, border_radius=0)

def draw():
    screen.fill(BLACK)
    pygame.draw.rect(screen, BLUE, paddle)

    for laser in lasers:
        draw_laser(laser, LASER_STYLE)

    for tx, ty in targets:
        pygame.draw.circle(screen, RED, (tx, ty), TARGET_RADIUS)

    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))

    style_text = font.render(f"Style [{LASER_STYLE}]: {STYLE_NAMES[LASER_STYLE]}", True, WHITE)
    screen.blit(style_text, (10, 45))

    # Sound status
    sound_status = "ON" if SOUND_ENABLED else "OFF"
    music_status = "ON" if background_music_started else "OFF"
    sound_text = font.render(f"Sound: {sound_status} | Music: {music_status}", True, WHITE)
    screen.blit(sound_text, (10, 80))

    if game_over:
        over_text = font.render("Game Over - Press R to Restart", True, WHITE)
        screen.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 2))

def main():
    global score, lasers, targets, last_shot_time, game_over, LASER_STYLE, background_music_started

    target_timer = 0

    while True:
        dt = clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Toggle laser style with 1..5
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1: LASER_STYLE = 1
                elif event.key == pygame.K_2: LASER_STYLE = 2
                elif event.key == pygame.K_3: LASER_STYLE = 3
                elif event.key == pygame.K_4: LASER_STYLE = 4
                elif event.key == pygame.K_5: LASER_STYLE = 5
                # Sound controls
                elif event.key == pygame.K_m:  # M key to toggle background music
                    if SOUND_ENABLED and not background_music_started:
                        play_background_music()
                        background_music_started = True
                    elif SOUND_ENABLED and background_music_started:
                        pygame.mixer.stop()
                        background_music_started = False

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
                if SOUND_ENABLED:
                    play_sound('shoot')

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
                    if SOUND_ENABLED:
                        play_sound('game_over')
                # Collision detection (rect vs circle AABB)
                for laser in lasers[:]:
                    if pygame.Rect(target[0] - TARGET_RADIUS, target[1] - TARGET_RADIUS,
                                   TARGET_RADIUS * 2, TARGET_RADIUS * 2).colliderect(laser):
                        try:
                            targets.remove(target)
                            lasers.remove(laser)
                            if SOUND_ENABLED:
                                play_sound('hit')
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
                # Optional: reset timers so the first second is calm
                target_timer = 0
                last_shot_time = 0
                # Start background music on first game start
                if SOUND_ENABLED and not background_music_started:
                    play_background_music()
                    background_music_started = True

        draw()
        pygame.display.flip()

if __name__ == "__main__":
    main()
