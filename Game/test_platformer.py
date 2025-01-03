import test_platformer
from platformer import Object, Knife, Cloud, Coin, Level, game_over_screen

# Тестирование класса Object
def test_object_creation():
    player = Object("player.png")
    assert player.rect.x == 400
    assert player.rect.y == 480

# Тестирование класса Knife
def test_knife_creation():
    knife = Knife()
    assert knife.rect.y == 0

def test_knife_move():
    knife = Knife()
    initial_y = knife.rect.y
    knife.move()
    assert knife.rect.y == initial_y + knife.speed

# Тестирование класса Cloud
def test_cloud_creation():
    cloud = Cloud()
    assert cloud.rect.x == -16

def test_cloud_move():
    cloud = Cloud()
    initial_x = cloud.rect.x
    cloud.move()
    assert cloud.rect.x == initial_x + 1

# Тестирование класса Coin
def test_coin_creation():
    coin = Coin()
    assert coin.rect.y == 460

# Тестирование класса Level
def test_level_creation():
    level = Level()
    assert level.rect.y == 500
