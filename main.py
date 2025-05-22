import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 500, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Smash the Lumberjacks!")

# Colors
WHITE = (255, 255, 255)
BROWN = (139, 69, 19)
GREEN = (34, 139, 34)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GRAY = (100, 100, 100)

# Tree state
tree_height = 50
max_height = 300
min_height = 20
watered = 0

# Font
font = pygame.font.SysFont(None, 30)

# Lumberjack setup
lumberjacks = []

class Lumberjack:
    def __init__(self, x, direction):
        self.x = x
        self.y = HEIGHT - 60
        self.width = 20
        self.height = 40
        self.speed = 1
        self.direction = direction  # 1 for right, -1 for left
        self.reached_tree = False
        self.chop_timer = 0
        self.dragging = False
        self.offset_x = 0
        self.offset_y = 0
        self.last_y = self.y
        self.vertical_speed = 0
        self.destroyed = False

    def move(self):
        if not self.reached_tree and not self.dragging:
            if (self.direction == 1 and self.x < WIDTH//2 - 20) or (self.direction == -1 and self.x > WIDTH//2 + 10):
                self.x += self.speed * self.direction
            else:
                self.reached_tree = True

    def update(self):
        self.vertical_speed = self.y - self.last_y
        self.last_y = self.y

    def draw(self, screen):
        if self.destroyed:
            return
        # Body
        pygame.draw.rect(screen, RED, (self.x, self.y - self.height, self.width, self.height))
        # Axe
        axe_x = self.x + (self.width if self.direction == 1 else -5)
        pygame.draw.line(screen, GRAY, (axe_x, self.y - self.height + 10), (axe_x, self.y - 5), 3)

    def chop(self):
        if self.reached_tree and not self.dragging:
            self.chop_timer += 1
            if self.chop_timer >= 60:  # Once per second
                self.chop_timer = 0
                return True
        return False

    def get_rect(self):
        return pygame.Rect(self.x, self.y - self.height, self.width, self.height)

# Spawn a lumberjack every few seconds
SPAWN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_EVENT, 4000)

# Game loop
clock = pygame.time.Clock()
running = True
game_over = False
selected_lj = None

while running:
    screen.fill(WHITE)
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not game_over:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if tree_height < max_height:
                    tree_height += 10
                    watered += 1

            if event.type == SPAWN_EVENT:
                side = random.choice(['left', 'right'])
                x = 0 if side == 'left' else WIDTH - 20
                direction = 1 if side == 'left' else -1
                lumberjacks.append(Lumberjack(x, direction))

            # Mouse interactions
            if event.type == pygame.MOUSEBUTTONDOWN:
                for lj in reversed(lumberjacks):  # Topmost first
                    if lj.get_rect().collidepoint(event.pos) and not lj.destroyed:
                        selected_lj = lj
                        lj.dragging = True
                        lj.offset_x = lj.x - event.pos[0]
                        lj.offset_y = lj.y - event.pos[1]
                        break

            elif event.type == pygame.MOUSEBUTTONUP:
                if selected_lj:
                    selected_lj.dragging = False
                    # Smash check
                    if abs(selected_lj.vertical_speed) > 15:
                        selected_lj.destroyed = True
                    selected_lj = None

    if not game_over:
        # Update and draw tree
        trunk_width = 20
        trunk_rect = pygame.Rect(WIDTH//2 - trunk_width//2, HEIGHT - tree_height - 50, trunk_width, tree_height)
        pygame.draw.rect(screen, BROWN, trunk_rect)

        leaf_radius = tree_height // 4
        pygame.draw.circle(screen, GREEN, (WIDTH//2, HEIGHT - tree_height - 60), leaf_radius)

        for lj in lumberjacks:
            if lj.destroyed:
                continue
            if lj.dragging:
                mx, my = mouse_pos
                lj.x = mx + lj.offset_x
                lj.y = my + lj.offset_y
            else:
                lj.move()

            lj.update()
            lj.draw(screen)
            if lj.chop():
                tree_height -= 10
                if tree_height <= min_height:
                    tree_height = min_height
                    game_over = True

        # UI
        instructions = font.render("SPACE = Water | Drag & Drop = Smash", True, BLACK)
        screen.blit(instructions, (40, 20))

        counter = font.render(f"Watered: {watered}", True, BLACK)
        screen.blit(counter, (10, 60))

        if tree_height >= max_height:
            win_msg = font.render("The tree is fully grown! You win!", True, GREEN)
            screen.blit(win_msg, (80, HEIGHT//2))
            game_over = True

        if game_over:
            lose_msg = font.render("Lumberjacks cut the tree! Game Over!", True, RED)
            screen.blit(lose_msg, (60, HEIGHT//2))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
