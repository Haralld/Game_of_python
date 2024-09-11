import pygame  # import module
import sys
import random
import pygame_menu

pygame.init()

SIZE_BLOCK = 25  # block size
FRAME_COLOR = (134, 134, 134)  # frame color
WHITE = (255, 255, 255)  # white color
BLUE = (224, 224, 224)  # blue color
RED = (224, 0, 0)
HEADER_COLOR = (96, 96, 96)  # header color
SNAKE_COLOR = (76, 153, 0)  # snake color
COUNT_BLOCKS = 20  # number of blocks
HEADER_MARGIN = 70  # header margin size
MARGIN = 1  # margin size between blocks
size = [SIZE_BLOCK * COUNT_BLOCKS + 2 * SIZE_BLOCK + MARGIN * COUNT_BLOCKS,
        SIZE_BLOCK * COUNT_BLOCKS + 2 * SIZE_BLOCK + MARGIN * SIZE_BLOCK + HEADER_MARGIN]  # window size

print(size)  # print window size to console

screen = pygame.display.set_mode(size)  # variable = module.display.method(window size)
pygame.display.set_caption('Snake')  # module.display.method sets window title
timer = pygame.time.Clock()  # timer to control frame rate
courier = pygame.font.SysFont('courier', 36)


class SnakeBlock:  # class to assign the initial coordinates of the snake
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def is_inside(self):
        return 0 <= self.x < COUNT_BLOCKS and 0 <= self.y < COUNT_BLOCKS

    def __eq__(self, other):
        return isinstance(other, SnakeBlock) and self.x == other.x and self.y == other.y


def draw_block(color, row, column):  # function to draw blocks
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

    snake_blocks = [SnakeBlock(9, 8), SnakeBlock(9, 9), SnakeBlock(9, 10)]  # list of snake coordinates
    apple = get_randon_empty_block()
    d_row = buf_row = 0  # coordinates for snake movement
    d_col = buf_col = 1
    total = 0
    speed = 1

    while True:  # infinite loop

        for event in pygame.event.get():  # event handling loop module.events.actions
            if event.type == pygame.QUIT:  # event.type == module.quit
                print('exit')
                pygame.quit()  # module.quit closes the window
                sys.exit()
            elif event.type == pygame.KEYDOWN:  # snake movement
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

        screen.fill(FRAME_COLOR)  # fill the background with a color
        pygame.draw.rect(screen, HEADER_COLOR,
                         [0, 0, size[0], HEADER_MARGIN])  # module.draw.rect(draws rectangle)

        text_total = courier.render(f"Total: {total}", 0, WHITE)
        text_speed = courier.render(f"Speed: {speed}", 0, WHITE)
        screen.blit(text_total, (SIZE_BLOCK, SIZE_BLOCK))
        screen.blit(text_speed, (SIZE_BLOCK + 230, SIZE_BLOCK))

        for row in range(COUNT_BLOCKS):  # loop to draw the game field rows
            for column in range(COUNT_BLOCKS):  # columns
                if (row + column) % 2 == 0:  # if (row + column) divided by 2 equals 0 (even)
                    color = BLUE  # then the color is blue
                else:  # otherwise (odd)
                    color = WHITE  # block color is white

                draw_block(color, row, column)

        head = snake_blocks[-1]
        if not head.is_inside():
            print('crash')
            break
            #pygame.quit()  # module.quit closes the window
            #sys.exit()

        draw_block(RED, apple.x, apple.y)
        for block in snake_blocks:
            draw_block(SNAKE_COLOR, block.x, block.y)

        pygame.display.flip()  # module.display.flip updates the screen

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
            #pygame.quit()  # module.quit closes the window
            #sys.exit()
            break
        snake_blocks.append(new_head)
        snake_blocks.pop(0)

        timer.tick(2 + speed)  # frame rate


menu = pygame_menu.Menu(
    height=300,  # height
    width=220,   # width
    title="Snake", 
    theme=pygame_menu.themes.THEME_GREEN
)

menu.add.text_input('Name: ', default='Player 1')
menu.add.button('Play', start_the_game)
menu.add.button('Exit', pygame_menu.events.EXIT)

menu.mainloop(screen)
