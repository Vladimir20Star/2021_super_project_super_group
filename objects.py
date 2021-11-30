import pygame
import os

pygame.font.init()


class BaseButton:
    def __init__(self, x, y, le, h, function):
        self.x = x
        self.y = y
        self.le = le
        self.h = h
        self.function = function

    def click(self, click_event):
        if self.x < click_event.pos[0] < self.x + self.le and self.y < click_event.pos[1] < self.y + self.h:
            self.function()


class Button(BaseButton):
    def __init__(self, x, y, le, h, color, function, text, size, x_text, y_text, text_color):
        super().__init__(x, y, le, h, function)
        self.color = color
        self.text = text
        self.size = size
        self.x_text = x_text
        self.y_text = y_text
        self.text_color = text_color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.le, self.h))
        font = pygame.font.Font(None, self.size)
        text = font.render(self.text, True, self.text_color)
        screen.blit(text, (self.x + self.x_text, self.y + self.y_text))


class Figure(pygame.sprite.Sprite, BaseButton):
    def __init__(self, x, y, le, h, image_name, sprites, x_end, y_end):
        pygame.sprite.Sprite.__init__(self, sprites)
        BaseButton.__init__(self, x, y, le, h, self.start_move)
        self.x_end = x_end
        self.y_end = y_end
        self.step_count = 20
        self.step_x = (self.x_end - self.x) / self.step_count
        self.step_y = (self.y_end - self.y) / self.step_count
        self.move_flag = False
        self.active = True
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
            if abs(self.x - self.x_end) < abs(self.step_x) or abs(self.y - self.y_end) < abs(self.step_y):
                self.x = self.x_end
                self.y = self.y_end
            self.rect.x = self.x
            self.rect.y = self.y
