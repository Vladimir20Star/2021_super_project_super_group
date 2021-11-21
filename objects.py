import pygame


pygame.font.init()


class Button:
    def __init__(self, x, y, le, h, color, function, text, size, x_text, y_text, text_color):
        self.x = x
        self.le = le
        self.y = y
        self.h = h
        self.color = color
        self.text = text
        self.size = size
        self.x_text = x_text
        self.y_text = y_text
        self.text_color = text_color
        self.function = function

    def click(self, click_event):
        if self.x < click_event.pos[0] < self.x + self.le and self.y < click_event.pos[1] < self.y + self.h:
            self.function()

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.le, self.h))
        font = pygame.font.Font(None, self.size)
        text = font.render(self.text, True, self.text_color)
        screen.blit(text, (self.x + self.x_text, self.y + self.y_text))
