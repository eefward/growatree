import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("mango")

RED = (255, 0, 0)
BG_COLOR = (240, 240, 240)

mango_size = 50
mango_pos = [WIDTH // 2, HEIGHT // 2]
grow_speed = 5

clock = pygame.time.Clock()

running = True
while running:
    screen.fill(BG_COLOR)

    mango_rect = pygame.Rect(
        mango_pos[0] - mango_size // 2, 
        mango_pos[1] - mango_size // 2, 
        mango_size, 
        mango_size
    )
    
    pygame.draw.rect(screen, RED, mango_rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if mango_rect.collidepoint(event.pos):
                mango_size += grow_speed

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
