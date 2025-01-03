import pygame
import keyboard
from random import randint

# Инициализация Pygame
pygame.init()

# Определение размеров окна и скорости падения
H = 600
W = 800
falling_speed = 10

# Инициализация таймера, счетчика и интерфейса
timer = 0
count = 0
score = 0
window = pygame.display.set_mode((W, H))
pygame.display.set_caption('Running stupid guy')
WHITE = (255, 255, 255)
BLUE = (120, 120, 255)
BROWN = (150, 50, 0)
GRAY = (50, 50, 50)
GREEN = (20, 255, 20)

# Глобальные переменные
IN_GAME = True
player_name = 'Paul'
orientation = 'right'
clock = pygame.time.Clock()
FPS = 60
number = 2
speed = 0
WINDOW_WIDTH = window.get_width()
writer = pygame.font.SysFont('candara', 40)
record = 0

# Отрисовка интерфейса игры
def draw_interface():
    """
    Функция для отрисовки интерфейса игры, включая счет, время и рекорд.
    """
    pygame.draw.rect(window, GRAY, (0, 0, W, 60))
    score_text = writer.render('SCORE: ' + str(score), 1, GREEN)
    time_text = writer.render('TIME: ' + str(timer), 1, GREEN)
    record_text = writer.render('RECORD: ' + str(record), 1, GREEN)
    window.blit(score_text, (10, 10))
    window.blit(time_text, (650, 10))
    window.blit(record_text, (330, 10))

# Функция для обработки нажатий клавиш
def handle_key_press():
    """
    Обрабатывает нажатия клавиш и обновляет состояние игрока соответственно.
    """
    global speed, number, orientation

    if keyboard.is_pressed('d'):
        move_right()
    elif keyboard.is_pressed('a'):
        move_left()
    else:
        stop_moving()

    if keyboard.is_pressed('w'):
        jump()

# Функция для перемещения игрока вправо
def move_right():
    """
    Перемещает игрока вправо и обновляет его скорость и ориентацию.
    """
    global speed, number, orientation
    player.rect.x += 3
    orientation = 'right'
    if speed == 0:
        speed = 5
        update_sprite_number()

# Функция для перемещения игрока влево
def move_left():
    """
    Перемещает игрока влево и обновляет его скорость и ориентацию.
    """
    global speed, number, orientation
    player.rect.x -= 3
    orientation = 'left'
    if speed == 0:
        speed = 5
        update_sprite_number()

# Функция для остановки движения игрока
def stop_moving():
    """
    Останавливает движение игрока и обновляет его спрайт.
    """
    global number
    number = 2

# Функция для выполнения прыжка
def jump():
    """
    Выполняет прыжок игрока, если он на земле.
    """
    global falling_speed, touch_the_ground
    if touch_the_ground:
        falling_speed = -10
        touch_the_ground = False

# Функция для обновления номера спрайта игрока
def update_sprite_number():
    """
    Обновляет номер спрайта игрока в зависимости от его движения.
    """
    global number
    if number != 2:
        number = abs(number - 1)
    else:
        number = 1

# Функция для обработки физики игрока
def player_physics():
    """
    Обрабатывает физику игрока, его движение и взаимодействие с окружающей средой.
    """
    global speed, falling_speed, touch_the_ground, record

    if score > record:
        record = score

    if speed > 0:
        speed -= 1

    handle_key_press()

    if player.rect.x > W - 40:
        player.rect.x = W - 40
    if player.rect.x < -20:
        player.rect.x = -20

    update_falling_speed()
    update_player_position()

# Функция для обновления скорости падения игрока
def update_falling_speed():
    """
    Обновляет скорость падения игрока.
    """
    global falling_speed
    if falling_speed < 10:
        falling_speed += 1

# Функция для обновления позиции игрока
def update_player_position():
    """
    Обновляет позицию игрока на основе его скорости падения и взаимодействия с землей.
    """
    global touch_the_ground
    player.rect.y += falling_speed
    if touch_the_ground:
        player.rect.y = 480

# Класс объекта персонажа
class Object(pygame.sprite.Sprite):
    """
    Класс, представляющий основной объект персонажа в игре.
    """
    def __init__(self, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect(center=(W // 2, 480))

# Класс объекта ножа
class Knife(pygame.sprite.Sprite):
    """
    Класс, представляющий объект ножа в игре.
    """
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Knife_0.png').convert_alpha()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect(center=(randint(20, W - 40), 0))
        self.speed = 5
        self.alive = True
        self.death_time = 1

    def move(self):
        if self.alive:
            self.rect.y += self.speed
            if self.rect.y >= 472:
                self.alive = False
                knifes_killers.remove(self)
        else:
            if self.death_time == 7:
                self.kill()
            else:
                self.image = pygame.image.load('Knife_' + str(int(self.death_time)) + '.png').convert_alpha()
                self.death_time += 0.5

# Класс объекта облака
class Cloud(pygame.sprite.Sprite):
    """
    Класс, представляющий объект облака в игре.
    """
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Cloud_' + str(randint(0, 3)) + '.png').convert_alpha()
        self.rect = self.image.get_rect(center=(-16, randint(20, H - 300)))
        self.time = 0

    def move(self):
        if self.time == 3:
            self.rect.x += 1
            self.time = 0
        else:
            self.time += 1
        if self.rect.x >= W + 16:
            self.kill()

# Класс уровня земли
class Level(pygame.sprite.Sprite):
    """
    Класс, представляющий уровень земли в игре.
    """
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.draw.rect(window, BROWN, (0, H - 100, W, H))

    def update(self):
        pygame.draw.rect(window, BROWN, (0, H - 100, W, H))

# Класс объекта монеты
class Coin(pygame.sprite.Sprite):
    """
    Класс, представляющий объект монеты в игре.
    """
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Coin_0.png').convert_alpha()
        self.rect = self.image.get_rect(center=(randint(40, W - 40), H - 140))

    def update(self):
        global score
        window.blit(self.image, self.rect)
        if pygame.sprite.spritecollide(self, players, False):
            score += 30
            self.kill()

# Инициализация основных объектов игры
player = Object(player_name + '_' + orientation + str(number) + '.png')
players = pygame.sprite.Group()
players.add(player)
knifes = pygame.sprite.Group()
clouds = pygame.sprite.Group()
coins = pygame.sprite.Group()
knifes_killers = pygame.sprite.Group()
level = pygame.sprite.Group()
level.add(Level())

# Функция экрана завершения игры
def game_over_screen(score):
    """
    Функция для отображения экрана завершения игры с окончательным счетом и опциями для перезапуска или выхода.
    """
    font = pygame.font.SysFont('Arial', 36)
    text_surface = font.render('Game Over', True, (255, 0, 0))
    text_rect = text_surface.get_rect(center=(W // 2, H // 2 - 50))
    window.blit(text_surface, text_rect)

    score_surface = font.render('Score: ' + str(score), True, (255, 255, 255))
    score_rect = score_surface.get_rect(center=(W // 2, H // 2))
    window.blit(score_surface, score_rect)

    restart_surface = font.render('Restart', True, (255, 255, 255))
    restart_rect = restart_surface.get_rect(center=(W // 2, H // 2 + 50))
    window.blit(restart_surface, restart_rect)

    quit_surface = font.render('Quit', True, (255, 255, 255))
    quit_rect = quit_surface.get_rect(center=(W // 2, H // 2 + 100))
    window.blit(quit_surface, quit_rect)

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if restart_rect.collidepoint(mouse_pos):
                    return True
                elif quit_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    quit()

# Основной цикл игры
restart = False
while IN_GAME:
    count += 1
    timer += count // 60
    score += count // 60
    count %= 60

    touch_the_ground = pygame.sprite.spritecollide(player, level, False)

    for action in pygame.event.get():
        if action.type == pygame.QUIT:
            IN_GAME = False

    clock.tick(FPS)

    player_physics()

    generation_key = randint(0, 10 - timer // 5)
    if generation_key == 0:
        knf = Knife()
        knifes.add(knf)
        knifes_killers.add(knf)
    generation_key = randint(0, 120)
    if generation_key == 60:
        clouds.add(Cloud())
    generation_key = randint(0, 480)
    if generation_key == 0:
        coins.add(Coin())

    window.fill(BLUE)

    for c in clouds:
        c.move()
        window.blit(c.image, c.rect)

    for l in level:
        l.update()

    for k in knifes:
        k.move()
        window.blit(k.image, k.rect)

    for cns in coins:
        cns.update()

    if player.rect.left < 0:
        player.rect.left = 0
    if player.rect.right > WINDOW_WIDTH - player.rect.width:
        player.rect.right = WINDOW_WIDTH - player.rect.width

    player_physics()
    is_dead = pygame.sprite.spritecollide(player, knifes_killers, False)
    player.image = pygame.image.load(player_name + '_' + orientation + str(number) + '.png').convert_alpha()
    window.blit(player.image, player.rect)
    player.update()
    draw_interface()
    pygame.display.update()

    if is_dead:
        restart = game_over_screen(score)
        IN_GAME = False

# Перезапуск игры
restart = False
while True:
    if restart:
        restart = False
        IN_GAME = True
        score = 0
        timer = 0
        count = 0
        player.rect = player.image.get_rect(center=(W // 2, 480))
        falling_speed = 10
        speed = 0
        knifes.empty()
        clouds.empty()
        coins.empty()
        knifes_killers.empty()

    if IN_GAME:
        count += 1
        timer += count // 60
        score += count // 60
        count %= 60

        touch_the_ground = pygame.sprite.spritecollide(player, level, False)

        for action in pygame.event.get():
            if action.type == pygame.QUIT:
                IN_GAME = False

        clock.tick(FPS)

        generation_key = randint(0, 10 - timer // 5)
        if generation_key == 0:
            knf = Knife()
            knifes.add(knf)
            knifes_killers.add(knf)
        generation_key = randint(0, 120)
        if generation_key == 60:
            clouds.add(Cloud())
        generation_key = randint(0, 480)
        if generation_key == 0:
            coins.add(Coin())

        window.fill(BLUE)

        for c in clouds:
            c.move()
            window.blit(c.image, c.rect)

        for l in level:
            l.update()

        for k in knifes:
            k.move()
            window.blit(k.image, k.rect)

        for cns in coins:
            cns.update()

        if player.rect.left < 0:
            player.rect.left = 0
        if player.rect.right > WINDOW_WIDTH - player.rect.width:
            player.rect.right = WINDOW_WIDTH - player.rect.width

        player_physics()
        is_dead = pygame.sprite.spritecollide(player, knifes_killers, False)
        player.image = pygame.image.load(player_name + '_' + orientation + str(number) + '.png').convert_alpha()
        window.blit(player.image, player.rect)
        player.update()
        draw_interface()
        pygame.display.update()

        if is_dead:
            game_over_screen(score)
            IN_GAME = False
    else:
        restart = game_over_screen(score)

