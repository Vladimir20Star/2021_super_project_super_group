import pygame


class Button:
    def __init__(self, x, l, y, h, text, size, x_text, y_text):
        self.x = x
        self.l = l
        self.y = y
        self.h = h
        self.text = text
        self.size = size
        self.x_text = x_text
        self.y_text = y_text

    def click(self, click_event):
        if self.x < click_event.pos[0] < self.x + self.l and self.y < click_event.pos[1] < self.y + self.h:
            print('123')

    def draw(self, screen):
        pygame.draw.rect(screen, 'red', (self.x, self.y, self.l, self.h))
        font = pygame.font.Font(None, self.size)
        text = font.render(self.text, True, 'black')
        screen.blit(text, (self.x + self.x_text, self.y + self.y_text))
