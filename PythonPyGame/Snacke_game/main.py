import pygame  # импорт модуля
import sys
import random
import pygame_menu

pygame.init()

SIZE_BLOCK = 25  # размер блока
FRAME_COLOR = (134, 134, 134)  # цвет фона
WHITE = (255, 255, 255)  # белый цвет
BLUE = (224, 224, 224)  # сиинй цвет
RED = (224, 0, 0)
HEADER_COLOR = (96, 96, 96)  # цвет заголовка
SNAKE_COLOR = (76, 153, 0)  # цвет змейки
COUNT_BLOCKS = 20  # колличество блоков
HEADER_MARGIN = 70  # размер края заголовка
MARGIN = 1  # размер отсупа между блоками
size = [SIZE_BLOCK * COUNT_BLOCKS + 2 * SIZE_BLOCK + MARGIN * COUNT_BLOCKS,
        SIZE_BLOCK * COUNT_BLOCKS + 2 * SIZE_BLOCK + MARGIN * SIZE_BLOCK + HEADER_MARGIN]  # размер окна

print(size)  # вывод в консоль размер окна

screen = pygame.display.set_mode(size)  # переменная = модуль.монитор. метод (размер окна)
pygame.display.set_caption('Змейка')  # модуль.монитор. метод вывода названия окна
timer = pygame.time.Clock()  # таймер для изменении частоты кадров
courier = pygame.font.SysFont('courier', 36)


class SnakeBlock:  # класс для назначения начальных координат змейки
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def is_inside(self):
        return 0 <= self.x < COUNT_BLOCKS and 0 <= self.y < COUNT_BLOCKS

    def __eq__(self, other):
        return isinstance(other, SnakeBlock) and self.x == other.x and self.y == other.y


def draw_block(color, row, column):  # функция привлечения блоков
    pygame.draw.rect(screen, color, [SIZE_BLOCK + column * SIZE_BLOCK + MARGIN * (column + 1),
                                     HEADER_MARGIN + SIZE_BLOCK + row * SIZE_BLOCK + MARGIN * (row + 1),
                                     SIZE_BLOCK,
                                     SIZE_BLOCK])


def start_the_game():
    def get_randon_empty_block():
        x = random.randint(0, COUNT_BLOCKS - 1)
        y = random.randint(0, COUNT_BLOCKS - 1)
        empty_block = SnakeBlock(x, y)
        while empty_block in snake_blocks:
            empty_block.x = random.randint(0, COUNT_BLOCKS - 1)
            empty_block.y = random.randint(0, COUNT_BLOCKS - 1)
        return empty_block

    snake_blocks = [SnakeBlock(9, 8), SnakeBlock(9, 9), SnakeBlock(9, 10)]  # список координат змейки
    apple = get_randon_empty_block()
    d_row = buf_row = 0  # координаты для здвижения змейки
    d_col = buf_col = 1
    total = 0
    speed = 1

    while True:  # бесконечный цикл

        for event in pygame.event.get():  # цыкл обработки сабытий модуль.события.действия
            if event.type == pygame.QUIT:  # событие.тип == модуль.выход
                print('exit')
                pygame.quit()  # модуль.выход закрывает окно
                sys.exit()
            elif event.type == pygame.KEYDOWN:  # движение зменйки
                if event.key == pygame.K_UP and d_col != 0:
                    buf_row = -1
                    buf_col = 0
                elif event.key == pygame.K_DOWN and d_col != 0:
                    buf_row = 1
                    buf_col = 0
                elif event.key == pygame.K_LEFT and d_row != 0:
                    buf_row = 0
                    buf_col = -1
                elif event.key == pygame.K_RIGHT and d_row != 0:
                    buf_row = 0
                    buf_col = 1

        screen.fill(FRAME_COLOR)  # окно.заколнения фона цветом
        pygame.draw.rect(screen, HEADER_COLOR,
                         [0, 0, size[0], HEADER_MARGIN])  # модуль. метод рисования. метод (где, цвет, размер)

        text_total = courier.render(f"Total: {total}", 0, WHITE)
        text_speed = courier.render(f"Speed: {speed}", 0, WHITE)
        screen.blit(text_total, (SIZE_BLOCK, SIZE_BLOCK))
        screen.blit(text_speed, (SIZE_BLOCK + 230, SIZE_BLOCK))

        for row in range(COUNT_BLOCKS):  # цикл прорисовки игрового поля  ряды
            for column in range(COUNT_BLOCKS):  # столбики
                if (row + column) % 2 == 0:  # если (строка + столбик) поделить на 2 и он == 0 (четный)
                    color = BLUE  # то цвет рисует синий
                else:  # в других случаях (не чётный)
                    color = WHITE  # цвет блока белый

                draw_block(color, row, column)

        head = snake_blocks[-1]
        if not head.is_inside():
            print('crash')
            break
            #pygame.quit()  # модуль.выход закрывает окно
            #sys.exit()

        draw_block(RED, apple.x, apple.y)
        for block in snake_blocks:
            draw_block(SNAKE_COLOR, block.x, block.y)

        pygame.display.flip()  # модуль.монитор. метод применения изменений обновление экрана

        if apple == head:
            total += 1
            speed = total // 5 + 1
            snake_blocks.append(apple)
            apple = get_randon_empty_block()

        d_row = buf_row
        d_col = buf_col
        new_head = SnakeBlock(head.x + d_row, head.y + d_col)

        if new_head in snake_blocks:
            print('crash yourself')
            #pygame.quit()  # модуль.выход закрывает окно
            #sys.exit()
            break
        snake_blocks.append(new_head)
        snake_blocks.pop(0)

        timer.tick(2 + speed)  # частота кадров


menu = pygame_menu.Menu(
    height=300,  # высота
    width=220,   # ширина
    title="Змейка", 
    theme=pygame_menu.themes.THEME_GREEN
)

menu.add.text_input('Имя : ', default='Игрок 1')
menu.add.button('Играть', start_the_game)
menu.add.button('Выход', pygame_menu.events.EXIT)

menu.mainloop(screen)
