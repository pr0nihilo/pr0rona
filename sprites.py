import pygame as pg
from random import uniform, randint, choice
import pytweening as tween
from settings import *
vec = pg.math.Vector2


class Spritesheet:
    # utility class for loading and parsing spritesheets
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert_alpha()

    def get_image(self, x, y, width, height):
        # grab an image out of a larger spritesheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        # image = pg.transform.scale(image, (width // 2, height // 2))
        image.set_colorkey((0, 0, 0))
        return image


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_walking_img[0]
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)
        self.vel = vec(0, 0)
        self.acc = 0  # das ist für die Rolle
        self.pos = vec(x, y)
        self.current_frame = 0
        self.last_update = 0
        # self.walkcount = 0
        self.walking = False
        self.walking_down = False
        self.walking_r = False
        self.walking_l = False
        self.attacking = False
        self.attack_d = ATTACK_D_STD
        self.rolling = False
        self.roll_d = ROLL_D_STD
        self.magicing = False
        self.stamina = PLAYER_STAMINA
        self.exhausted = False
        self.cooldown = pg.time.get_ticks() - PLAYER_STAMINA
        self.attack_cooldown = pg.time.get_ticks()
        self.sternstunde = False
        self.stern_cooldown = pg.time.get_ticks()

    def get_keys(self):
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        Now_Speed = PLAYER_SPEED
        Now_Speed += self.game.bier * 5
        if self.sternstunde:
            Now_Speed += 48

        if keys[pg.K_a] and not keys[pg.K_d]:
            self.vel += vec(-Now_Speed, 0)
            self.walking = True
            self.walking_l = True
            self.walking_r = False
        if keys[pg.K_d] and not keys[pg.K_a]:
            self.vel += vec(Now_Speed, 0)
            self.walking = True
            self.walking_r = True
            self.walking_l = False
        if keys[pg.K_w] and not keys[pg.K_s]:
            self.vel += vec(0, -Now_Speed)
            self.walking = True
            self.walking_r = False
            self.walking_l = False
            self.walking_down = False
        if keys[pg.K_s] and not keys[pg.K_w]:
            self.vel += vec(0, Now_Speed)
            self.walking = True
            self.walking_r = False
            self.walking_l = False
            self.walking_down = True
        if keys[pg.K_SPACE]:
            if not self.rolling and not self.exhausted and not self.attacking and self.walking:
                self.rolling = True
                self.exhausted = True
                self.cooldown = pg.time.get_ticks()
        if keys[pg.K_f]:
            if not self.walking and not self.rolling and not self.attacking and self.game.sprays > 0:
                self.attacking = True
                self.attack()
                self.attack_cooldown = pg.time.get_ticks()

        if abs(self.vel.x) > 0 and abs(self.vel.y) > 0:
            self.vel = self.vel * 0.7071

        if self.rolling:
            self.roll()

    def roll(self):
        # Hälfte der Rolle erreicht:
        neg = -1 if pg.time.get_ticks() - self.cooldown > self.roll_d / 2 else 1
        self.acc += ROLL_SPEED * neg
        if self.acc < 0:
            self.acc = 0
        if self.vel.x < 0:
            self.vel.x -= self.acc
        if self.vel.x > 0:
            self.vel.x += self.acc
        if self.vel.y > 0:
            self.vel.y += self.acc
        if self.vel.y < 0:
            self.vel.y -= self.acc

    def attack(self):
        if self.game.sprays > 0:
            self.game.sprays -= 1
        choice(self.game.effect_sounds['spray']).play()
        Animation(self.game, self.pos+(0, -70), 'bg')

    def star(self):
        self.sternstunde = True
        self.stern_cooldown = pg.time.get_ticks()

    def update(self):
        self.get_keys()
        self.animate()
        self.pos += self.vel * self.game.dt
        # RAHMEN BEGRENZUNGEN Spieler (ternary statements yes it works)
        self.pos.y = 850 if self.pos.y > 850 else 80 if self.pos.y < 80 else self.pos.y
        self.pos.x = 150 if self.pos.x < 150 else 450 if self.pos.x > 450 else self.pos.x

        self.rect.center = self.pos

        # Zurücksetzen des Cooldowns und Fähigkeiten
        now = pg.time.get_ticks()
        if now - self.cooldown >= self.roll_d:
            self.rolling = False
            self.acc = 0
        if now - self.attack_cooldown >= self.attack_d:
            self.attacking = False
        if now - self.stern_cooldown >= STAR_D:
            self.sternstunde = False
        if now - self.cooldown >= PLAYER_STAMINA:
            self.exhausted = False
            self.stamina = PLAYER_STAMINA
        else:
            self.stamina = now - self.cooldown
        self.walking = False
        self.walking_r = False
        self.walking_l = False

        self.walking_down = False

    def animate(self):
        # print(str(self.rolling) + str(self.walking) + str(self.walking_down) + str(self.walking_l) + str(self.walking_r))
        now = pg.time.get_ticks()
        if self.rolling or self.attacking:
            if self.rolling:
                if now - self.last_update > 100:
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1) % len(self.game.player_roll_img)
                    bottom = self.rect.bottom
                    self.image = self.game.player_roll_img[self.current_frame]
                    self.rect = self.image.get_rect()
                    self.rect.bottom = bottom
            if self.attacking:
                if now - self.last_update > 100:
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1) % len(self.game.player_attack_img)
                    bottom = self.rect.bottom
                    self.image = self.game.player_attack_img[self.current_frame]
                    self.rect = self.image.get_rect()
                    self.rect.bottom = bottom
        elif self.walking:
            if self.vel.y == 0:
                if self.walking_l:
                    if now - self.last_update > 160:
                        self.last_update = now
                        self.current_frame = (self.current_frame + 1) % len(self.game.player_walking_left_img)
                        bottom = self.rect.bottom
                        self.image = self.game.player_walking_left_img[self.current_frame]
                        self.rect = self.image.get_rect()
                        self.rect.bottom = bottom
                elif self.walking_r:
                    if now - self.last_update > 160:
                        self.last_update = now
                        self.current_frame = (self.current_frame + 1) % len(self.game.player_walking_right_img)
                        bottom = self.rect.bottom
                        self.image = self.game.player_walking_right_img[self.current_frame]
                        self.rect = self.image.get_rect()
                        self.rect.bottom = bottom
            if not self.walking_down:
                if now - self.last_update > 160:
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1) % len(self.game.player_walking_img)
                    bottom = self.rect.bottom
                    self.image = self.game.player_walking_img[self.current_frame]
                    self.rect = self.image.get_rect()
                    self.rect.bottom = bottom
            if self.walking_down:
                if now - self.last_update > 160:
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1) % len(self.game.player_walking_down_img)
                    bottom = self.rect.bottom
                    self.image = self.game.player_walking_down_img[self.current_frame]
                    self.rect = self.image.get_rect()
                    self.rect.bottom = bottom
        elif self.walking_down:
            bottom = self.rect.bottom
            self.image = self.game.player_walking_down_img[0]
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom
        else:
            bottom = self.rect.bottom
            self.image = self.game.player_walking_img[0]
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom

        self.mask = pg.mask.from_surface(self.image)


class Virus(pg.sprite.Sprite):
    def __init__(self, game, speed):
        self._layer = VIREN_LAYER
        self.groups = game.all_sprites, game.viren
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # self.name = choice(VIRUS_NAMEN)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.pos = vec(randint(275, 325), randint(120, 700))
        self.size = randint(20, 36)-int((speed*6))
        if self.size < 10:
            self.size = 11
        self.rot = 0
        rotation = uniform(speed*3, 2+speed*3)
        self.rot_speed = rotation * choice((-1, 1))
        self.speed = speed
        self.image_orig = pg.transform.scale(choice(game.viren_images), (self.size, self.size))
        self.image_orig.set_colorkey((0, 0, 0))
        self.image_orig.set_alpha(randint(180, 220))
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width / 2)
        self.rect.center = self.pos
        self.stepx = randint(0, 300)
        self.stepy = randint(0, 20)  # Achtung hier auch anpassen!
        self.dirx = choice((1, -1))
        self.diry = choice((1, -1))

        self.tweenx = choice(VIRUS_TWEEN)
        self.tweeny = choice(VIRUS_TWEEN)

        self.last_update = pg.time.get_ticks()

    def rotate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pg.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center
            self.mask = pg.mask.from_surface(self.image)

    def update(self):
        self.rotate()
        offsetx = VIRUS_RANGEX * (self.tweenx(self.stepx / VIRUS_RANGEX)-0.5)
        offsety = VIRUS_RANGEY * (self.tweeny(self.stepy / VIRUS_RANGEY)-0.5)
        self.rect.centerx = self.pos.x + offsetx * self.dirx
        self.stepx += self.speed
        if self.stepx > VIRUS_RANGEX:
            self.stepx = 0
            self.dirx *= -1
        self.rect.centery = self.pos.y + offsety * self.diry
        self.stepy += self.speed
        if self.stepy > VIRUS_RANGEY:
            self.stepy = 0
            self.diry *= -1

    # so kann das Objekt auch gelöscht werden!
    def desinfect(self):
        self.kill()


class Animation(pg.sprite.Sprite):
    def __init__(self, game, center, size):
        self._layer = EFFECTS_LAYER
        self.groups = game.all_sprites, game.effects
        pg.sprite.Sprite.__init__(self, self.groups)
        self.size = size
        self.game = game
        self.image = self.game.animation_effect[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pg.time.get_ticks()
        self.frame_rate = 40

    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.game.animation_effect[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.game.animation_effect[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


class Item(pg.sprite.Sprite):
    def __init__(self, game, pos, type):
        self._layer = OBJECT_LAYER
        self.groups = game.all_sprites, game.objects
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.item_images[type]
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.type = type
        self.pos = vec(pos)
        self.rect.center = pos
        self.tween = tween.easeInOutSine
        self.step = 0
        self.dir = 1

    def update(self,):
        # easing funktion
        offset = BOB_RANGE * (self.tween(self.step / BOB_RANGE)-0.5)
        self.rect.centery = self.pos.y + offset * self.dir
        self.step += BOB_SPEED
        if self.step > BOB_RANGE:
            self.step = 0
            self.dir *= -1
