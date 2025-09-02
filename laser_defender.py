import pygame
import random
import sys
import math
import json
import os
from datetime import datetime

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
GOLD = (255, 215, 0)  # For high scores

PADDLE_WIDTH, PADDLE_HEIGHT = 80, 20
LASER_WIDTH, LASER_HEIGHT = 8, 25  # Made wider and taller for better visibility
TARGET_RADIUS = 20
LASER_SPEED = 10
TARGET_SPEED = 3
SHOOT_DELAY = 300  # ms

# High Score System
HIGH_SCORE_FILE = "high_scores.json"
MAX_HIGH_SCORES = 10

class HighScoreManager:
    def __init__(self):
        self.high_scores = []
        self.load_high_scores()
    
    def load_high_scores(self):
        """Load high scores from file"""
        try:
            if os.path.exists(HIGH_SCORE_FILE):
                with open(HIGH_SCORE_FILE, 'r') as f:
                    self.high_scores = json.load(f)
                # Sort by score (highest first)
                self.high_scores.sort(key=lambda x: x['score'], reverse=True)
                # Keep only top scores
                self.high_scores = self.high_scores[:MAX_HIGH_SCORES]
            else:
                self.high_scores = []
        except Exception as e:
            print(f"Error loading high scores: {e}")
            self.high_scores = []
    
    def save_high_scores(self):
        """Save high scores to file"""
        try:
            with open(HIGH_SCORE_FILE, 'w') as f:
                json.dump(self.high_scores, f, indent=2)
        except Exception as e:
            print(f"Error saving high scores: {e}")
    
    def add_score(self, score, player_name="Player"):
        """Add a new score and return if it's a high score"""
        if score <= 0:
            return False
        
        # Check if this is a high score
        is_high_score = len(self.high_scores) < MAX_HIGH_SCORES or score > self.high_scores[-1]['score']
        
        if is_high_score:
            new_score = {
                'score': score,
                'player': player_name,
                'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
                'laser_style': LASER_STYLE
            }
            
            self.high_scores.append(new_score)
            # Sort by score (highest first)
            self.high_scores.sort(key=lambda x: x['score'], reverse=True)
            # Keep only top scores
            self.high_scores = self.high_scores[:MAX_HIGH_SCORES]
            
            # Save to file
            self.save_high_scores()
            
            return True
        
        return False
    
    def get_top_score(self):
        """Get the highest score"""
        if self.high_scores:
            return self.high_scores[0]['score']
        return 0
    
    def is_new_record(self, score):
        """Check if score would be a new record"""
        if not self.high_scores:
            return True
        return score > self.high_scores[0]['score']
    
    def clear_all_scores(self):
        """Clear all high scores"""
        self.high_scores = []
        self.save_high_scores()
        print("All high scores cleared!")
    
    def get_statistics(self):
        """Get high score statistics"""
        if not self.high_scores:
            return {
                'total_games': 0,
                'best_score': 0,
                'average_score': 0,
                'total_points': 0
            }
        
        total_points = sum(score['score'] for score in self.high_scores)
        return {
            'total_games': len(self.high_scores),
            'best_score': self.high_scores[0]['score'],
            'average_score': total_points // len(self.high_scores),
            'total_points': total_points
        }

# Initialize high score manager
high_score_manager = HighScoreManager()

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
show_high_scores = False

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

    # High score display
    top_score = high_score_manager.get_top_score()
    if top_score > 0:
        high_score_text = font.render(f"High Score: {top_score}", True, GOLD)
        screen.blit(high_score_text, (WIDTH - high_score_text.get_width() - 10, 10))

    if game_over:
        over_text = font.render("Game Over - Press R to Restart", True, WHITE)
        screen.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 2))
        
        # Show high score achievement if applicable
        if high_score_manager.is_new_record(score):
            record_text = font.render("🏆 NEW RECORD! 🏆", True, GOLD)
            screen.blit(record_text, (WIDTH // 2 - record_text.get_width() // 2, HEIGHT // 2 + 50))
            
            # Show record details
            details_text = font.render(f"You beat the previous record of {high_score_manager.get_top_score() - score} points!", True, WHITE)
            screen.blit(details_text, (WIDTH // 2 - details_text.get_width() // 2, HEIGHT // 2 + 80))
            
            # Add to high scores
            high_score_manager.add_score(score)
            
        elif high_score_manager.add_score(score):
            high_score_text = font.render("🎯 New High Score!", True, GOLD)
            screen.blit(high_score_text, (WIDTH // 2 - high_score_text.get_width() // 2, HEIGHT // 2 + 50))
            
            # Show ranking info
            stats = high_score_manager.get_statistics()
            rank_text = font.render(f"Ranked #{stats['total_games']} out of {stats['total_games']} scores", True, WHITE)
            screen.blit(rank_text, (WIDTH // 2 - rank_text.get_width() // 2, HEIGHT // 2 + 80))
        
        # Show current session stats
        stats = high_score_manager.get_statistics()
        if stats['total_games'] > 0:
            session_text = font.render(f"Session: {score} | Best: {stats['best_score']} | Games: {stats['total_games']}", True, GREEN)
            screen.blit(session_text, (WIDTH // 2 - session_text.get_width() // 2, HEIGHT // 2 + 110))
    
    # High score display screen
    if show_high_scores:
        draw_high_score_screen()

def draw_high_score_screen():
    """Draw the high score display screen"""
    # Semi-transparent overlay
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(128)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    
    # Title with decorative elements
    title = font.render("🏆 HIGH SCORES 🏆", True, GOLD)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 80))
    
    # Statistics header
    stats_text = f"Total Games: {len(high_score_manager.high_scores)} | Best: {high_score_manager.get_top_score()}"
    stats_surface = font.render(stats_text, True, WHITE)
    screen.blit(stats_surface, (WIDTH // 2 - stats_surface.get_width() // 2, 120))
    
    # Instructions
    instructions = font.render("Press H to close | ESC to clear scores", True, WHITE)
    screen.blit(instructions, (WIDTH // 2 - instructions.get_width() // 2, 150))
    
    # Column headers
    rank_header = font.render("RANK", True, GOLD)
    score_header = font.render("SCORE", True, GOLD)
    player_header = font.render("PLAYER", True, GOLD)
    date_header = font.render("DATE", True, GOLD)
    style_header = font.render("STYLE", True, GOLD)
    
    header_y = 180
    screen.blit(rank_header, (WIDTH // 2 - 200, header_y))
    screen.blit(score_header, (WIDTH // 2 - 100, header_y))
    screen.blit(player_header, (WIDTH // 2, header_y))
    screen.blit(date_header, (WIDTH // 2 + 100, header_y))
    screen.blit(style_header, (WIDTH // 2 + 200, header_y))
    
    # Separator line
    pygame.draw.line(screen, GOLD, (WIDTH // 2 - 220, header_y + 25), (WIDTH // 2 + 220, header_y + 25), 2)
    
    # Display high scores
    y_pos = 210
    for i, score_data in enumerate(high_score_manager.high_scores):
        if i >= 10:  # Limit to top 10
            break
            
        # Rank with medal emojis
        if i == 0:
            rank_text = "🥇 1st"
            rank_color = GOLD
        elif i == 1:
            rank_text = "🥈 2nd"
            rank_color = (192, 192, 192)  # Silver
        elif i == 2:
            rank_text = "🥉 3rd"
            rank_color = (205, 127, 50)  # Bronze
        else:
            rank_text = f"{i+1:2d}th"
            rank_color = WHITE
            
        rank_surface = font.render(rank_text, True, rank_color)
        screen.blit(rank_surface, (WIDTH // 2 - 200, y_pos))
        
        # Score
        score_text = f"{score_data['score']:4d}"
        score_surface = font.render(score_text, True, GOLD if i == 0 else WHITE)
        screen.blit(score_surface, (WIDTH // 2 - 100, y_pos))
        
        # Player name
        player_text = score_data['player'][:8]  # Limit length
        player_surface = font.render(player_text, True, WHITE)
        screen.blit(player_surface, (WIDTH // 2, y_pos))
        
        # Date (shortened)
        date_text = score_data['date'][5:10]  # Just MM-DD
        date_surface = font.render(date_text, True, WHITE)
        screen.blit(date_surface, (WIDTH // 2 + 100, y_pos))
        
        # Laser style
        style_text = f"Style {score_data['laser_style']}"
        style_surface = font.render(style_text, True, WHITE)
        screen.blit(style_surface, (WIDTH // 2 + 200, y_pos))
        
        y_pos += 30
    
    # Show message if no high scores
    if not high_score_manager.high_scores:
        no_scores = font.render("No high scores yet! Play a game to set the first record!", True, WHITE)
        screen.blit(no_scores, (WIDTH // 2 - no_scores.get_width() // 2, 250))
        
        # Encouragement text
        encouragement = font.render("Try different laser styles (1-5) for variety!", True, GREEN)
        screen.blit(encouragement, (WIDTH // 2 - encouragement.get_width() // 2, 280))
    
    # Current session info
    if score > 0:
        current_text = f"Current Session: {score} points"
        current_surface = font.render(current_text, True, GREEN)
        screen.blit(current_surface, (WIDTH // 2 - current_surface.get_width() // 2, HEIGHT - 60))

def main():
    global score, lasers, targets, last_shot_time, game_over, LASER_STYLE, background_music_started, show_high_scores

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
                # High score display
                elif event.key == pygame.K_h:  # H key to toggle high score display
                    show_high_scores = not show_high_scores
                # Clear high scores
                elif event.key == pygame.K_ESCAPE and show_high_scores:  # ESC key to clear scores when viewing
                    high_score_manager.clear_all_scores()
                    show_high_scores = False

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

