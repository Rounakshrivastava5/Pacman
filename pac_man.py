import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CELL_SIZE = 20
MAZE_WIDTH = SCREEN_WIDTH // CELL_SIZE
MAZE_HEIGHT = SCREEN_HEIGHT // CELL_SIZE

# Enhanced Colors with gradients and realistic tones
BLACK = (0, 0, 0)
DARK_BLUE = (0, 0, 139)
BLUE = (0, 100, 200)
LIGHT_BLUE = (173, 216, 230)
YELLOW = (255, 255, 0)
BRIGHT_YELLOW = (255, 255, 102)
WHITE = (255, 255, 255)
CREAM = (255, 253, 208)
RED = (220, 20, 60)
PINK = (255, 105, 180)
CYAN = (0, 206, 209)
ORANGE = (255, 140, 0)
PURPLE = (147, 112, 219)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)

# Game states
PLAYING = 0
GAME_OVER = 1
WIN = 2

class Pacman:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = 0  # 0: right, 1: down, 2: left, 3: up
        self.next_direction = 0
        self.speed = 2
        self.radius = 10
        self.mouth_animation = 0
        self.animation_speed = 0.2
        
    def move(self, maze):
        # Try to change direction if requested
        if self.next_direction != self.direction:
            if self.can_move_in_direction(self.next_direction, maze):
                self.direction = self.next_direction
        
        # Move in current direction
        if self.can_move_in_direction(self.direction, maze):
            if self.direction == 0:  # right
                self.x += self.speed
            elif self.direction == 1:  # down
                self.y += self.speed
            elif self.direction == 2:  # left
                self.x -= self.speed
            elif self.direction == 3:  # up
                self.y -= self.speed
        
        # Keep Pacman within bounds
        self.x = max(self.radius, min(self.x, SCREEN_WIDTH - self.radius))
        self.y = max(self.radius, min(self.y, SCREEN_HEIGHT - self.radius))
        
        # Update mouth animation
        self.mouth_animation += self.animation_speed
    
    def can_move_in_direction(self, direction, maze):
        """Check if Pacman can move in the given direction"""
        test_x = self.x
        test_y = self.y
        
        if direction == 0:  # right
            test_x += self.speed
        elif direction == 1:  # down
            test_y += self.speed
        elif direction == 2:  # left
            test_x -= self.speed
        elif direction == 3:  # up
            test_y -= self.speed
        
        # Debug: Print movement test
        # print(f"Testing movement: ({test_x:.1f}, {test_y:.1f}) Direction: {direction}")
        
        return not self.check_collision(test_x, test_y, maze)
    
    def check_collision(self, x, y, maze):
        # Check boundaries
        if x - self.radius < 0 or x + self.radius >= SCREEN_WIDTH or y - self.radius < 0 or y + self.radius >= SCREEN_HEIGHT:
            return True
        
        # Check maze walls - simplified collision detection
        # Check center and edges in movement direction
        points_to_check = [(x, y)]  # Center point
        
        # Add edge points based on current direction
        if self.direction == 0:  # right
            points_to_check.extend([(x + self.radius - 2, y), (x + self.radius - 2, y - self.radius//2), (x + self.radius - 2, y + self.radius//2)])
        elif self.direction == 1:  # down
            points_to_check.extend([(x, y + self.radius - 2), (x - self.radius//2, y + self.radius - 2), (x + self.radius//2, y + self.radius - 2)])
        elif self.direction == 2:  # left
            points_to_check.extend([(x - self.radius + 2, y), (x - self.radius + 2, y - self.radius//2), (x - self.radius + 2, y + self.radius//2)])
        elif self.direction == 3:  # up
            points_to_check.extend([(x, y - self.radius + 2), (x - self.radius//2, y - self.radius + 2), (x + self.radius//2, y - self.radius + 2)])
        
        for check_x, check_y in points_to_check:
            grid_x = int(check_x // CELL_SIZE)
            grid_y = int(check_y // CELL_SIZE)
            
            if 0 <= grid_x < MAZE_WIDTH and 0 <= grid_y < MAZE_HEIGHT:
                if maze[grid_y][grid_x] == 1:
                    return True
        return False
    
    def draw(self, screen):
        # Draw shadow
        shadow_offset = 2
        pygame.draw.circle(screen, DARK_GRAY, 
                         (int(self.x + shadow_offset), int(self.y + shadow_offset)), 
                         self.radius, 0)
        
        # Draw main body with gradient effect
        pygame.draw.circle(screen, BRIGHT_YELLOW, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), self.radius - 2)
        
        # Add shine effect
        shine_x = int(self.x - self.radius * 0.3)
        shine_y = int(self.y - self.radius * 0.3)
        pygame.draw.circle(screen, CREAM, (shine_x, shine_y), self.radius // 3)
        
        # Animated mouth
        mouth_angle = 45 + int(20 * abs(math.sin(self.mouth_animation)))
        start_angle = self.direction * 90 - mouth_angle // 2
        end_angle = self.direction * 90 + mouth_angle // 2
        
        # Create mouth points
        points = [(int(self.x), int(self.y))]
        num_points = max(8, mouth_angle // 5)
        for i in range(num_points + 1):
            angle = start_angle + i * (mouth_angle / num_points)
            angle_rad = math.radians(angle)
            x = int(self.x + (self.radius - 1) * math.cos(angle_rad))
            y = int(self.y + (self.radius - 1) * math.sin(angle_rad))
            points.append((x, y))
        
        if len(points) > 2:
            pygame.draw.polygon(screen, BLACK, points)
        
        # Draw eye
        eye_offset = self.radius * 0.4
        if self.direction == 0:  # right
            eye_x = int(self.x - eye_offset * 0.5)
            eye_y = int(self.y - eye_offset)
        elif self.direction == 1:  # down
            eye_x = int(self.x + eye_offset * 0.7)
            eye_y = int(self.y - eye_offset * 0.5)
        elif self.direction == 2:  # left
            eye_x = int(self.x + eye_offset * 0.5)
            eye_y = int(self.y - eye_offset)
        else:  # up
            eye_x = int(self.x + eye_offset * 0.7)
            eye_y = int(self.y + eye_offset * 0.5)
        
        pygame.draw.circle(screen, BLACK, (eye_x, eye_y), 3)
        pygame.draw.circle(screen, WHITE, (eye_x - 1, eye_y - 1), 1)


class Ghost:
    def __init__(self, x, y, color, name):
        self.x = x
        self.y = y
        self.color = color
        self.name = name
        self.direction = 0  # Start with right direction
        self.speed = 1.5
        self.radius = 10
        self.body_animation = 0
        self.animation_speed = 0.15
        self.target_x = x
        self.target_y = y
        self.change_direction_timer = 0
        self.change_direction_interval = 60  # Change direction every 60 frames
        
    def move(self, maze, pacman=None):
        self.change_direction_timer += 1
        
        # Simple AI - sometimes chase Pacman
        if pacman and random.random() < 0.1:  # 10% chance to chase
            dx = pacman.x - self.x
            dy = pacman.y - self.y
            if abs(dx) > abs(dy):
                new_direction = 0 if dx > 0 else 2
            else:
                new_direction = 1 if dy > 0 else 3
            
            if self.can_move_in_direction(new_direction, maze):
                self.direction = new_direction
        
        # Change direction when stuck or periodically
        if not self.can_move_in_direction(self.direction, maze) or self.change_direction_timer >= self.change_direction_interval:
            self.change_direction_timer = 0
            self.choose_new_direction(maze)
        
        # Move in current direction
        if self.can_move_in_direction(self.direction, maze):
            if self.direction == 0:  # right
                self.x += self.speed
            elif self.direction == 1:  # down
                self.y += self.speed
            elif self.direction == 2:  # left
                self.x -= self.speed
            elif self.direction == 3:  # up
                self.y -= self.speed
        
        # Keep ghost within bounds
        self.x = max(self.radius, min(self.x, SCREEN_WIDTH - self.radius))
        self.y = max(self.radius, min(self.y, SCREEN_HEIGHT - self.radius))
        
        self.body_animation += self.animation_speed
    
    def can_move_in_direction(self, direction, maze):
        """Check if ghost can move in the given direction"""
        test_x = self.x
        test_y = self.y
        
        if direction == 0:  # right
            test_x += self.speed
        elif direction == 1:  # down
            test_y += self.speed
        elif direction == 2:  # left
            test_x -= self.speed
        elif direction == 3:  # up
            test_y -= self.speed
        
        return not self.check_collision(test_x, test_y, maze)
    
    def choose_new_direction(self, maze):
        """Choose a new random direction that's valid"""
        directions = [0, 1, 2, 3]
        random.shuffle(directions)
        
        for direction in directions:
            if self.can_move_in_direction(direction, maze):
                self.direction = direction
                break
    
    def check_collision(self, x, y, maze):
        if x - self.radius < 0 or x + self.radius >= SCREEN_WIDTH or y - self.radius < 0 or y + self.radius >= SCREEN_HEIGHT:
            return True
        
        # Simplified collision detection for ghosts
        points_to_check = [(x, y)]  # Center point
        
        # Add edge points based on current direction
        if self.direction == 0:  # right
            points_to_check.extend([(x + self.radius - 2, y), (x + self.radius - 2, y - self.radius//2), (x + self.radius - 2, y + self.radius//2)])
        elif self.direction == 1:  # down
            points_to_check.extend([(x, y + self.radius - 2), (x - self.radius//2, y + self.radius - 2), (x + self.radius//2, y + self.radius - 2)])
        elif self.direction == 2:  # left
            points_to_check.extend([(x - self.radius + 2, y), (x - self.radius + 2, y - self.radius//2), (x - self.radius + 2, y + self.radius//2)])
        elif self.direction == 3:  # up
            points_to_check.extend([(x, y - self.radius + 2), (x - self.radius//2, y - self.radius + 2), (x + self.radius//2, y - self.radius + 2)])
        
        for check_x, check_y in points_to_check:
            grid_x = int(check_x // CELL_SIZE)
            grid_y = int(check_y // CELL_SIZE)
            
            if 0 <= grid_x < MAZE_WIDTH and 0 <= grid_y < MAZE_HEIGHT:
                if maze[grid_y][grid_x] == 1:
                    return True
        return False
    
    def draw(self, screen):
        # Draw shadow
        shadow_offset = 2
        pygame.draw.circle(screen, DARK_GRAY, 
                         (int(self.x + shadow_offset), int(self.y + shadow_offset)), 
                         self.radius, 0)
        
        # Draw body (top half circle)
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y - 2)), self.radius)
        
        # Draw wavy bottom
        bottom_y = int(self.y + self.radius - 2)
        wave_points = []
        wave_amplitude = 3 + int(2 * abs(math.sin(self.body_animation)))
        
        for i in range(5):
            wave_x = int(self.x - self.radius + i * (2 * self.radius / 4))
            if i % 2 == 0:
                wave_y = bottom_y - wave_amplitude
            else:
                wave_y = bottom_y + wave_amplitude
            wave_points.append((wave_x, wave_y))
        
        # Complete the ghost shape
        wave_points.insert(0, (int(self.x - self.radius), int(self.y)))
        wave_points.append((int(self.x + self.radius), int(self.y)))
        
        pygame.draw.polygon(screen, self.color, wave_points)
        
        # Draw eyes
        eye_size = 3
        left_eye_x = int(self.x - self.radius * 0.4)
        right_eye_x = int(self.x + self.radius * 0.4)
        eye_y = int(self.y - self.radius * 0.3)
        
        # White eye background
        pygame.draw.circle(screen, WHITE, (left_eye_x, eye_y), eye_size + 1)
        pygame.draw.circle(screen, WHITE, (right_eye_x, eye_y), eye_size + 1)
        
        # Black pupils
        pygame.draw.circle(screen, BLACK, (left_eye_x, eye_y), eye_size)
        pygame.draw.circle(screen, BLACK, (right_eye_x, eye_y), eye_size)
        
        # Eye shine
        pygame.draw.circle(screen, WHITE, (left_eye_x - 1, eye_y - 1), 1)
        pygame.draw.circle(screen, WHITE, (right_eye_x - 1, eye_y - 1), 1)


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Enhanced Pacman Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Create enhanced maze
        self.maze = self.create_maze()
        self.dots = self.create_dots()
        self.power_pellets = self.create_power_pellets()
        
        # Create game objects
        self.pacman = Pacman(CELL_SIZE * 3 + CELL_SIZE // 2, CELL_SIZE * 3 + CELL_SIZE // 2)
        self.ghosts = [
            Ghost(CELL_SIZE * 15 + CELL_SIZE // 2, CELL_SIZE * 15 + CELL_SIZE // 2, RED, "Blinky"),
            Ghost(CELL_SIZE * 20 + CELL_SIZE // 2, CELL_SIZE * 15 + CELL_SIZE // 2, PINK, "Pinky"),
            Ghost(CELL_SIZE * 25 + CELL_SIZE // 2, CELL_SIZE * 15 + CELL_SIZE // 2, CYAN, "Inky"),
            Ghost(CELL_SIZE * 30 + CELL_SIZE // 2, CELL_SIZE * 15 + CELL_SIZE // 2, ORANGE, "Clyde")
        ]
        
        self.score = 0
        self.lives = 3
        self.state = PLAYING
        
    def create_maze(self):
        maze = [[0 for _ in range(MAZE_WIDTH)] for _ in range(MAZE_HEIGHT)]
        
        # Create border walls
        for x in range(MAZE_WIDTH):
            maze[0][x] = 1
            maze[MAZE_HEIGHT-1][x] = 1
        for y in range(MAZE_HEIGHT):
            maze[y][0] = 1
            maze[y][MAZE_WIDTH-1] = 1
            
        # Create more interesting maze patterns
        # Horizontal walls
        for y in range(3, MAZE_HEIGHT-3, 6):
            for x in range(3, MAZE_WIDTH-3):
                if x % 8 != 0 and x % 8 != 1:
                    maze[y][x] = 1
                    
        # Vertical walls
        for x in range(6, MAZE_WIDTH-6, 12):
            for y in range(6, MAZE_HEIGHT-6):
                if y % 6 != 0:
                    maze[y][x] = 1
                    
        # Add some boxes
        box_positions = [(10, 8), (25, 8), (10, 20), (25, 20)]
        for bx, by in box_positions:
            for i in range(3):
                for j in range(3):
                    if bx+i < MAZE_WIDTH and by+j < MAZE_HEIGHT:
                        maze[by+j][bx+i] = 1
        
        # Ensure starting area is clear
        for y in range(2, 6):
            for x in range(2, 6):
                if y < MAZE_HEIGHT and x < MAZE_WIDTH:
                    maze[y][x] = 0
                        
        return maze
    
    def create_dots(self):
        dots = []
        for y in range(MAZE_HEIGHT):
            for x in range(MAZE_WIDTH):
                if self.maze[y][x] == 0:
                    # Don't place dots too close to starting positions
                    dot_x = x * CELL_SIZE + CELL_SIZE // 2
                    dot_y = y * CELL_SIZE + CELL_SIZE // 2
                    if not (40 < dot_x < 80 and 40 < dot_y < 80):  # Avoid Pacman start
                        dots.append((dot_x, dot_y))
        return dots
    
    def create_power_pellets(self):
        pellets = []
        # Place power pellets in corners
        corner_positions = [
            (3 * CELL_SIZE + CELL_SIZE // 2, 3 * CELL_SIZE + CELL_SIZE // 2),
            ((MAZE_WIDTH - 4) * CELL_SIZE + CELL_SIZE // 2, 3 * CELL_SIZE + CELL_SIZE // 2),
            (3 * CELL_SIZE + CELL_SIZE // 2, (MAZE_HEIGHT - 4) * CELL_SIZE + CELL_SIZE // 2),
            ((MAZE_WIDTH - 4) * CELL_SIZE + CELL_SIZE // 2, (MAZE_HEIGHT - 4) * CELL_SIZE + CELL_SIZE // 2)
        ]
        
        for pos in corner_positions:
            grid_x = pos[0] // CELL_SIZE
            grid_y = pos[1] // CELL_SIZE
            if (0 <= grid_x < MAZE_WIDTH and 0 <= grid_y < MAZE_HEIGHT and 
                self.maze[grid_y][grid_x] == 0):
                pellets.append(pos)
        
        return pellets
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.pacman.next_direction = 0
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.pacman.next_direction = 1
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.pacman.next_direction = 2
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.pacman.next_direction = 3
                elif event.key == pygame.K_SPACE and self.state != PLAYING:
                    self.reset_game()
        
        # Handle continuous key presses for smoother movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.pacman.next_direction = 0
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.pacman.next_direction = 1
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.pacman.next_direction = 2
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            self.pacman.next_direction = 3
        
        return True
    
    def update(self):
        if self.state == PLAYING:
            # Debug: Print Pacman position and direction
            # print(f"Pacman: ({self.pacman.x:.1f}, {self.pacman.y:.1f}) Direction: {self.pacman.direction}")
            
            self.pacman.move(self.maze)
            
            # Move ghosts with Pacman reference for AI
            for i, ghost in enumerate(self.ghosts):
                # Debug: Print ghost positions
                # print(f"Ghost {i}: ({ghost.x:.1f}, {ghost.y:.1f}) Direction: {ghost.direction}")
                ghost.move(self.maze, self.pacman)
            
            # Check dot collection
            pacman_pos = (int(self.pacman.x), int(self.pacman.y))
            dots_collected = 0
            for dot in self.dots[:]:
                dot_x, dot_y = dot
                distance = ((pacman_pos[0] - dot_x) ** 2 + (pacman_pos[1] - dot_y) ** 2) ** 0.5
                if distance < 15:  # Increased collision radius
                    self.dots.remove(dot)
                    self.score += 10
                    dots_collected += 1
            
            # Debug: Print dots collected
            if dots_collected > 0:
                print(f"Collected {dots_collected} dots! Score: {self.score}")
            
            # Check power pellet collection
            for pellet in self.power_pellets[:]:
                pellet_x, pellet_y = pellet
                distance = ((pacman_pos[0] - pellet_x) ** 2 + (pacman_pos[1] - pellet_y) ** 2) ** 0.5
                if distance < 18:  # Increased collision radius
                    self.power_pellets.remove(pellet)
                    self.score += 50
                    print(f"Power pellet collected! Score: {self.score}")
            
            # Check ghost collision
            for ghost in self.ghosts:
                distance = ((self.pacman.x - ghost.x) ** 2 + (self.pacman.y - ghost.y) ** 2) ** 0.5
                if distance < 18:
                    self.lives -= 1
                    print(f"Ghost collision! Lives: {self.lives}")
                    if self.lives <= 0:
                        self.state = GAME_OVER
                    else:
                        # Reset positions
                        self.pacman.x = CELL_SIZE * 3 + CELL_SIZE // 2
                        self.pacman.y = CELL_SIZE * 3 + CELL_SIZE // 2
                        for i, ghost in enumerate(self.ghosts):
                            ghost.x = CELL_SIZE * (15 + i * 5) + CELL_SIZE // 2
                            ghost.y = CELL_SIZE * 15 + CELL_SIZE // 2
            
            # Check win condition
            if not self.dots and not self.power_pellets:
                self.state = WIN
    
    def draw(self):
        # Fill with dark background
        self.screen.fill(BLACK)
        
        # Draw maze with enhanced graphics
        for y in range(MAZE_HEIGHT):
            for x in range(MAZE_WIDTH):
                if self.maze[y][x] == 1:
                    rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    # Draw wall with gradient effect
                    pygame.draw.rect(self.screen, DARK_BLUE, rect)
                    pygame.draw.rect(self.screen, BLUE, rect, 2)
                    # Add highlight
                    highlight_rect = pygame.Rect(x * CELL_SIZE + 1, y * CELL_SIZE + 1, 
                                               CELL_SIZE - 2, 2)
                    pygame.draw.rect(self.screen, LIGHT_BLUE, highlight_rect)
        
        # Draw dots with glow effect
        for dot in self.dots:
            pygame.draw.circle(self.screen, YELLOW, dot, 4)
            pygame.draw.circle(self.screen, WHITE, dot, 2)
        
        # Draw power pellets with pulsing effect
        for pellet in self.power_pellets:
            pulse = int(3 + 2 * abs(math.sin(pygame.time.get_ticks() * 0.01)))
            pygame.draw.circle(self.screen, BRIGHT_YELLOW, pellet, pulse)
            pygame.draw.circle(self.screen, WHITE, pellet, pulse - 2)
        
        # Draw game objects
        self.pacman.draw(self.screen)
        for ghost in self.ghosts:
            ghost.draw(self.screen)
        
        # Draw enhanced UI
        # Score with shadow
        score_shadow = self.font.render(f"Score: {self.score}", True, BLACK)
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_shadow, (12, 12))
        self.screen.blit(score_text, (10, 10))
        
        # Lives with shadow
        lives_shadow = self.font.render(f"Lives: {self.lives}", True, BLACK)
        lives_text = self.font.render(f"Lives: {self.lives}", True, WHITE)
        self.screen.blit(lives_shadow, (12, 52))
        self.screen.blit(lives_text, (10, 50))
        
        # Draw life icons
        for i in range(self.lives):
            life_x = 120 + i * 25
            pygame.draw.circle(self.screen, YELLOW, (life_x, 65), 8)
        
        # Game state messages with background
        if self.state == GAME_OVER:
            # Semi-transparent overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            
            game_over_text = self.font.render("GAME OVER", True, RED)
            restart_text = self.small_font.render("Press SPACE to restart", True, WHITE)
            
            game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 20))
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 20))
            
            self.screen.blit(game_over_text, game_over_rect)
            self.screen.blit(restart_text, restart_rect)
            
        elif self.state == WIN:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            
            win_text = self.font.render("YOU WIN!", True, BRIGHT_YELLOW)
            restart_text = self.small_font.render("Press SPACE to restart", True, WHITE)
            
            win_rect = win_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 20))
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 20))
            
            self.screen.blit(win_text, win_rect)
            self.screen.blit(restart_text, restart_rect)
        
        pygame.display.flip()
    
    def reset_game(self):
        self.pacman = Pacman(CELL_SIZE * 3 + CELL_SIZE // 2, CELL_SIZE * 3 + CELL_SIZE // 2)
        self.ghosts = [
            Ghost(CELL_SIZE * 15 + CELL_SIZE // 2, CELL_SIZE * 15 + CELL_SIZE // 2, RED, "Blinky"),
            Ghost(CELL_SIZE * 20 + CELL_SIZE // 2, CELL_SIZE * 15 + CELL_SIZE // 2, PINK, "Pinky"),
            Ghost(CELL_SIZE * 25 + CELL_SIZE // 2, CELL_SIZE * 15 + CELL_SIZE // 2, CYAN, "Inky"),
            Ghost(CELL_SIZE * 30 + CELL_SIZE // 2, CELL_SIZE * 15 + CELL_SIZE // 2, ORANGE, "Clyde")
        ]
        self.dots = self.create_dots()
        self.power_pellets = self.create_power_pellets()
        self.score = 0
        self.lives = 3
        self.state = PLAYING
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
