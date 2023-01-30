import pygame
from Constant import *

pygame.font.init()
font = pygame.font.SysFont("comicsans", 40)
class Button:
    def __init__(self, text, width, height, pos):

        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = BTN_COLOR

        self.text_surf = font.render(text, True, WHITE)
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)

    def draw(self, screen):
        pygame.draw.rect(screen, self.top_color, self.top_rect, border_radius=8)
        screen.blit(self.text_surf, self.text_rect)
        self.check_click()

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                return True