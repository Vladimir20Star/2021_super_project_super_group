import pygame
import os

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


class Figure(pygame.sprite.Sprite, Button):
    def __init__(self, x, y, le, h, image_name, sprites, x_end, y_end):
        super().__init__(sprites)
        self.x = x
        self.y = y
        self.le = le
        self.h = h
        self.x_end = x_end
        self.y_end = y_end
        self.step_x = (self.x_end - self.x) / 20
        self.step_y = (self.y_end - self.y) / 20
        self.move_flag = False
        self.function = self.start_move
        fullname = os.path.join('img', image_name)
        image = pygame.image.load(fullname).convert()
        self.image = image
        self.image = pygame.transform.scale(self.image, (self.le, self.h))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.x, self.y)

    def start_move(self):
        self.move_flag = True
        color_key = self.image.get_at((0, 0))
        self.image.set_colorkey(color_key)

    def move(self):
        if self.x == self.x_end and self.y == self.y_end:
            self.move_flag = False
        else:
            self.x += self.step_x
            self.y += self.step_y
            if abs(self.x - self.x_end) < self.step_x or abs(self.y - self.y_end) < self.step_y:
                self.x = self.x_end
                self.y = self.y_end
            self.rect.x = self.x
            self.rect.y = self.y
