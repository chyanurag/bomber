import pygame as pg
import random
import enum

class EType(enum.Enum):
    TANK = 'assets/enemy1.png'
    BIGTANK = 'assets/enemy2.png'

WIDTH = 1280
HEIGHT = 720
GROUND = 620

class Enemy(pg.sprite.Sprite):
    def __init__(self, e : EType):
        super().__init__()
        self.image = pg.image.load(e.value)
        self.image = pg.transform.scale(self.image, (100, 50))
        self.rect = self.image.get_rect()
        self.rect.center = self.rect.width, GROUND - self.rect.height//2
        self.speed = 1

    def update(self):
        self.rect.x += self.speed
        if self.rect.x + self.rect.width >= WIDTH or self.rect.x <= 0:
            self.speed = -self.speed
            self.image = pg.transform.flip(self.image, True, False)


class Tower(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load('assets/tower.png')
        self.image = pg.transform.scale(self.image, (100, 200))
        self.rect = self.image.get_rect()

    def update(self):
        pass

class Missile(pg.sprite.Sprite):
    def __init__(self, start):
        super().__init__()
        self.image = pg.image.load('assets/missile.png')
        self.image = pg.transform.scale(self.image, (20, 20))
        self.image = pg.transform.rotozoom(self.image, 90, 1)
        self.rect = self.image.get_rect()
        self.speed = 5
        self.rect.center = start

    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= GROUND:
            self.kill()

class Bomber(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load('assets/bomber.png')
        self.image = pg.transform.scale(self.image, (150, 50))
        self.rect = self.image.get_rect()
        self.speed = 5
        self.missiles = pg.sprite.Group()
        self.timeout = None

    def fire(self):
        self.missiles.add(Missile(self.rect.center))

    def update(self, win):
        self.rect.x += self.speed
        if self.rect.x + self.rect.width >= WIDTH or self.rect.x <= 0:
            self.speed = -self.speed
            self.image = pg.transform.flip(self.image, True, False)

        self.missiles.draw(win)
        self.missiles.update()


class Game:
    def __init__(self):
        pg.init()
        self.WIDTH = 1280
        self.HEIGHT = 720
        self.setup()
        self.bomber_group = pg.sprite.Group()
        self.bomber = Bomber()
        self.bomber_group.add(self.bomber)
        self.enemies = pg.sprite.Group()
        self.enemies.add(Enemy(EType.BIGTANK))
    
    def setup(self):
        self.win = pg.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pg.time.Clock()
        self.state = 'play'
        self.score = 0
        self.missileCount = 1
        self.gameFont = pg.font.SysFont('FiraCode Nerd Font Mono', 45)
        self.misIcon = pg.image.load('assets/mis-icon.png')
        self.misIcon = pg.transform.rotozoom(self.misIcon, -90, 1)
        self.misIcon = pg.transform.scale(self.misIcon, (50, 50))

    def draw_play(self):
        self.win.fill('white')
        pg.draw.rect(self.win, 'black', pg.Rect(0, GROUND, WIDTH, HEIGHT - GROUND), 0)
        self.bomber_group.draw(self.win)
        self.bomber_group.update(self.win)
        self.enemies.draw(self.win)
        self.enemies.update()
        self.win.blit(self.misIcon, (0, 0))
        scoreText = self.gameFont.render(str(self.score), True, (0, 0, 0))
        missileText = self.gameFont.render(str(self.missileCount), True, (0, 0, 0))
        self.win.blit(scoreText, (self.misIcon.get_rect().width, 0))
        self.win.blit(missileText, (self.misIcon.get_width() + scoreText.get_width(), 0))

    def update(self):
        if pg.sprite.groupcollide(self.bomber.missiles, self.enemies, True, True):
            self.score += 1
            self.missileCount += 1

    
    def draw(self):
        if self.state == 'play':
            self.draw_play()

    def handle_events(self, e):
        if e.type == pg.KEYDOWN:
            if pg.key.get_pressed()[pg.K_f] and self.missileCount >= 1:
                self.bomber.fire()
                self.missileCount -= 1

    def run(self):
        while True:
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    pg.quit()
                    print(self.score)
                else:
                    self.handle_events(e)

            self.draw()
            self.update()
            pg.display.update()
            self.clock.tick()

def main():
    game = Game()
    game.run()

main()
