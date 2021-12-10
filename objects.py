import pygame
import os

pygame.font.init()


class BaseButton:
    """
    Класс для создания кнопок и фигур
    """
    def __init__(self, x, y, le, h, function):
        self.x = x  # координа кнопки по оси x
        self.y = y  # координата кнопки по оси y
        self.le = le  # длина кнопки
        self.h = h  # высота кнопки
        self.function = function  # функция, вызываемая нажатием кнопки

    def click(self, click_event):
        """
        Проверка нажатия на кнопку
        :param click_event: pygame.event
        """
        if self.x < click_event.pos[0] < self.x + self.le and self.y < click_event.pos[1] < self.y + self.h:
            self.function()


class Button(BaseButton):
    """
    Класс кнопок
    """
    def __init__(self, x, y, le, h, color, function, text, size, x_text, y_text, text_color):
        super().__init__(x, y, le, h, function)
        self.color = color  # цвет заливки кнопки
        self.text = text  # текст, выводимый кнопкой
        self.size = size  # размер текста
        self.x_text = x_text  # координата текста по оси x
        self.y_text = y_text  # координата текста по оси y
        self.text_color = text_color  # цвет текста

    def draw(self, screen):
        """
        Метод прорисовки кнопки

        :param screen: оверхность для прорисовки
        """
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.le, self.h))
        font = pygame.font.Font(None, self.size)
        text = font.render(self.text, True, self.text_color)
        screen.blit(text, (self.x + self.x_text, self.y + self.y_text))


class Figure(pygame.sprite.Sprite, BaseButton):
    """
    Класс фигур
    """
    def __init__(self, x, y, le, h, image_name, sprites, x_end, y_end):
        pygame.sprite.Sprite.__init__(self, sprites)
        BaseButton.__init__(self, x, y, le, h, self.start_move)
        self.x_end = x_end  # конечная координата по оси x после движения
        self.y_end = y_end  # конечная координата по оси y после движения
        self.step_count = 15  # оличество шагов при движении
        self.step_x = (self.x_end - self.x) / self.step_count  # перемещение по оси x за 1 шаг
        self.step_y = (self.y_end - self.y) / self.step_count  # перемещение по оси y за 1 шаг
        self.move_flag = False  # флаг, разрешающи начать движение
        self.active = True  # флаг возможности нажатия
        fullname = os.path.join('img', image_name)  # дорога до картинки
        self.image = pygame.image.load(fullname).convert()  # сохранение картинки
        self.image = pygame.transform.scale(self.image, (self.le, self.h))  # станавливаем нужный размер
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.x, self.y)

    def start_move(self):
        """
        Начинает движение фигуры
        """
        self.move_flag = True
        color_key = self.image.get_at((0, 0))
        self.image.set_colorkey(color_key)

    def move(self):
        """
        Перемещает фигуру
        """
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
