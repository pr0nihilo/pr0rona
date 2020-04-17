# Dies ist die eigentliche Spieldatei.
# 2020 - April - von pr0nihilo

import sys
import pygame as pg
from sprites import *
from settings import *
import math
from os import path

spieleordner = path.dirname(__file__)
data = path.join(spieleordner, 'data')

# Initial der Console
print(">_ pr0nihilo wünscht Euch viel Spaß beim spielen!")
print(". . .")
print("Initialisiere")
print(". . .")
print("Musik: Rick and Morty - Evil Morty's Theme")
print(". . .")
print("(Drücke >M< um die Musik zu pausieren)")
print(". . .")
print("Lade Charaktere")
print(". . .")
print("Schmusekadser wird gestreichelt")
print(". . .")
print("Räume Keller auf")
print(". . .")
print(">_")

class Pr0rona:
    def __init__(self):
        pg.mixer.pre_init(44100, -16, 1, 2048)
        pg.init()
        icon = pg.image.load(path.join(data, 'paper_icon.bmp'))
        icon.set_colorkey((0, 0, 0))
        pg.display.set_icon(icon)
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)  # machen wir später nochmal mit FPS
        self.clock = pg.time.Clock()
        self.startmenue = pg.image.load(path.join(data, 'start.png')).convert()
        self.select_step = 0
        self.select_dir = 1
        self.cost = [0, 0]
        self.diff_step = 0
        self.diff_dir = 1
        self.last_play = []
        self.musicp = True

    # Funktion um allmögliche Schrift zu erzeugen
    def texter(self, text, font, size, color, x, y):
        font = pg.font.Font(path.join(data, font), size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        self.screen.blit(text_surface, text_rect)

    def load_data(self):
        # BACKGROUND
        self.background = pg.image.load(path.join(data, 'BG.png')).convert()
        self.trees = pg.image.load(path.join(data, 'trees.png')).convert_alpha()
        self.lights = pg.image.load(path.join(data, 'lights2.png')).convert_alpha()
        self.buymenue = pg.image.load(path.join(data, 'buy.png')).convert_alpha()


        # PLAYER
        self.spritesheet = Spritesheet(path.join(data, choice(PLAYER_SPRITES)))
        self.player_walking_img = []
        for img in range(9):
            sps = self.spritesheet.get_image(img*64, 8*64, 64, 64)
            self.player_walking_img.append(sps)
        self.player_walking_down_img = []
        for img in range(9):
            sps = self.spritesheet.get_image(img*64, 10*64, 64, 64)
            self.player_walking_down_img.append(sps)
        self.player_walking_left_img = []
        for img in range(9):
            sps = self.spritesheet.get_image(img*64, 9*64, 64, 64)
            self.player_walking_left_img.append(sps)
        self.player_walking_right_img = []
        for img in range(9):
            sps = self.spritesheet.get_image(img*64, 11*64, 64, 64)
            self.player_walking_right_img.append(sps)
        self.player_attack_img = []
        for img in range(6):
            sps = self.spritesheet.get_image(img*64, 12*64, 64, 64)
            self.player_attack_img.append(sps)
        self.player_roll_img = []
        for img in range(4):
            sps = self.spritesheet.get_image(4*64, img*64, 64, 64)
            self.player_roll_img.append(sps)

        # VIREN
        self.viren_images = []
        for img in VIRUS_IMAGES:
            self.viren_images.append(pg.image.load(path.join(data, img)).convert())

        # shop
        temp_tp = pg.image.load(path.join(data, 'paper.png')).convert_alpha()
        self.tp_obj_img = pg.transform.scale(temp_tp, (26, 26))

        self.tp_img = pg.transform.scale(temp_tp, (50, 50))
        self.blussizin_img = pg.image.load(path.join(data, 'blussizin.png')).convert_alpha()
        self.spray_img = pg.image.load(path.join(data, 'spray2.png')).convert_alpha()
        self.spray_HUD_img = pg.image.load(path.join(data, 'spray.png')).convert_alpha()
        self.bier_img = pg.image.load(path.join(data, 'bier.png')).convert_alpha()

        # ITEM
        self.item_images = {}
        for item in ITEM_IMAGES:
            self.item_images[item] = pg.image.load(path.join(data, ITEM_IMAGES[item])).convert_alpha()
            self.item_images[item] = pg.transform.scale(self.item_images[item], (15, 15))

        # HUD
        self.minus_img = pg.image.load(path.join(data, 'Minus.png')).convert_alpha()
        self.minus_img = pg.transform.scale(self.minus_img, (20, 20))
        self.plus_img = pg.image.load(path.join(data, 'Plus.png')).convert_alpha()
        self.plus_img = pg.transform.scale(self.plus_img, (20, 20))

        # star
        self.star_img = pg.image.load(path.join(data, 'shield.png')).convert_alpha()

        # ANIMATION
        self.animation_effect = {'sm': [], 'bg': []}
        for i in range(10):
            filename = 'anim{}.bmp'.format(i)
            img = pg.image.load(path.join(data, filename)).convert()
            img.set_colorkey((0, 0, 0))
            img.set_alpha(100)
            img_sm = pg.transform.scale(img, (20, 20))
            self.animation_effect['sm'].append(img_sm)
            img_bg = pg.transform.scale(img, (100, 100))
            self.animation_effect['bg'].append(img_bg)

        # NEBEL
        self.fog = pg.Surface((WIDTH, HEIGHT))
        self.fog.fill(BLACK)
        temp_light = pg.image.load(path.join(data, LIGHT_MASK)).convert_alpha()
        self.light_mask = pg.transform.scale(temp_light, LIGHT_RADIUS)
        self.light_rect = self.light_mask.get_rect()

        # Sound Loadung
        pg.mixer.music.load(path.join(data, 'music.mp3'))
        pg.mixer.music.set_volume(0.2)
        self.effect_sounds = {}
        for types in EFFECT_SOUNDS:
            self.effect_sounds[types] = []
            for snd in EFFECT_SOUNDS[types]:
                s = pg.mixer.Sound(path.join(data, snd))
                s.set_volume(0.5)
                self.effect_sounds[types].append(s)

        # Highscore einlesen
        with open('highscore.txt', 'r') as file:
            try:
                self.highscore = int(file.read())
                print("Eingelsesener Highscore: " + str(self.highscore))
            except:
                pass

    def new(self):
        # initialisierung
        print(">_ Neues Spiel gestartet")
        self.load_data()
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.viren = pg.sprite.Group()
        self.objects = pg.sprite.Group()
        self.effects = pg.sprite.Group()

        self.player = Player(self, STARTX, STARTY)
        self.player_health = PLAYER_HEALTH
        self.player_max_health = PLAYER_HEALTH
        self.tp = 0
        self.sprays = 1
        self.bier = 0
        self.taube = 0
        self.blau = 0
        self.rot = 0
        self.level = 1
        self.infiziert_von = []
        self.virus = [Virus(self, VIREN_SPEED), Virus(self, VIREN_SPEED+0.1), Virus(self, VIREN_SPEED+0.2)]

        self.pause = False
        self.buy = False

        choice(self.effect_sounds['start']).play()

    def run(self):
        # Spiele Looping - self.playing ) False to end
        self.playing = True
        pg.mixer.music.play(-1)
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            if not self.pause and not self.buy:
                self.update()
            self.objects.update()
            if self.buy:
                self.buyscreen()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        self.all_sprites.update()

        # Vier gewinnt
        if self.rot == 4:
            self.rot = 0
            self.effect_sounds['regen'][0].play()
            for drop in range(10):
                xd = randint(180, 420)
                yd = randint(180, 620)
                tItem = Item(self, (xd, yd), 'blussi')
                if len(pg.sprite.spritecollide(tItem, self.objects, False)) > 1:
                    tItem.kill()
        if self.blau == 4:
            self.blau = 0
            self.effect_sounds['cash'][0].play()
            for drop in range(10):
                xd = randint(180, 420)
                yd = randint(180, 620)
                tItem = Item(self, (xd, yd), 'star')
                if len(pg.sprite.spritecollide(tItem, self.objects, False)) > 1:
                    tItem.kill()

        # Level geschafft:
        if self.player.pos.y <= 82:
            choice(self.effect_sounds['win']).play()
            self.buy = True
            self.player.kill()
            self.set_highscore()
            self.level += 1
            self.player = Player(self, STARTX, STARTY)
            addspeed = VIREN_SPEED + math.log((self.level + 6) / 12, 2)
            if addspeed < VIREN_SPEED:
                addspeed = VIREN_SPEED
            addrange = 1
            if self.level % 4 == 0:
                addrange += 1
            if self.level > 13:
                if self.level % 2 == 0:
                    addrange += 1
            if self.level % 10 == 0:
                addrange += 2
            for lev in range(addrange):
                if lev == 4:
                    break
                multi = 2 if lev == 1 else 4 if lev == 3 else 1
                # print("multi:"+str(multi)+" addspeed:"+str(addspeed))
                self.virus.append(Virus(self, (addspeed / multi)))
            if self.level == 3 or self.level == 6 or self.level == 15:
                self.virus.append(Virus(self, VIREN_SPEED*6))
            for drop in range(randint(1, 4)):
                if randint(1, 100) > 20 * drop:
                    temp_items = ('blussi', 'globuli', 'schmuser', 'taube', 'star', 'blue', 'red')
                    xd = randint(180, 420)
                    yd = randint(180, 620)
                    tItem = Item(self, (xd, yd), choice(temp_items))
                    if len(pg.sprite.spritecollide(tItem, self.objects, False)) > 1:
                        tItem.kill()

        # Collision Spray
        pg.sprite.groupcollide(self.effects, self.viren, False, True)

        # Collisionen
        if not self.player.sternstunde:
            if pg.sprite.spritecollideany(self.player, self.viren):
                if pg.sprite.spritecollideany(self.player, self.viren, pg.sprite.collide_mask):
                    choice(self.effect_sounds['loose']).play()
                    self.player.kill()
                    self.player_health -= 1
                    self.infiziert_von.append(choice(VIRUS_NAMEN))
                    print("Infiziert von: " + str(self.infiziert_von[-1]))
                    if self.player_health <= 0:
                        self.playing = False
                    else:
                        self.player = Player(self, STARTX, STARTY)
                        self.texter("Infiziert von:", 'casper.ttf', 30, ORANGE3, 160, 450)
                        self.texter(str(self.infiziert_von[-1]), 'casper.ttf', 40, ORANGE2, 160, 500)
                        self.texter("Drücke die Leertaste um weiter zu spielen", 'casper.ttf', 20, ORANGE2, 160, 550)
                        pg.display.flip()
                        self.wait_for_key(300)

        # Items
        hits = pg.sprite.spritecollide(self.player, self.objects, False)
        for hit in hits:
            if hit.type == 'blussi':
                snd_up = self.effect_sounds['up'][0]
                if snd_up.get_num_channels() < 1:
                    snd_up.play()
                hit.kill()
                if self.player_health < self.player_max_health:
                    print('Blussi erhalten.')
                    self.player_health += 1
                else:
                    print('Du hast schon maximale Blussis.')
            if hit.type == 'globuli':
                snd_up = self.effect_sounds['up'][0]
                if snd_up.get_num_channels() < 1:
                    snd_up.play()
                hit.kill()
                print('Du fühlst dich beruhigt.')
                self.player.exhausted = False
                self.player.stamina = PLAYER_STAMINA
            if hit.type == 'schmuser':
                hit.kill()
                print('Miau! Schmuser gibt die Pappe')
                self.tp += 1
                snd_up = self.effect_sounds['schmuser'][0]
                if snd_up.get_num_channels() < 1:
                    snd_up.play()
            if hit.type == 'taube':
                hit.kill()
                print('Illegale Esstechnik.')
                self.taube += 1
                snd_up = self.effect_sounds['pavele'][0]
                if (self.bier+self.taube) % 3 == 0:
                    self.player_health = self.player_max_health
                    snd_up = self.effect_sounds['drink'][1]
                if snd_up.get_num_channels() < 1:
                    snd_up.play()
            if hit.type == 'star':
                hit.kill()
                self.effect_sounds['star'][0].play()
                self.player.star()
                print('Sternstunde')
            if hit.type == 'blue':
                hit.kill()
                self.blau += 1
                self.rot = 0
                snd_up = self.effect_sounds['up'][0]
                if snd_up.get_num_channels() < 1 and self.blau < 4:
                    snd_up.play()
                print('Blau mal ' + str(self.blau))
            if hit.type == 'red':
                hit.kill()
                self.rot += 1
                self.blau = 0
                snd_up = self.effect_sounds['up'][0]
                if snd_up.get_num_channels() < 1 and self.rot < 4:
                    snd_up.play()
                print('Rot mal ' + str(self.rot))

    def drawHUD(self):
        # HUD
        self.texter("Level: " + str(self.level), 'casper.ttf', 20, ORANGE, 5, 8)
        self.draw_player_stamina(self.screen, 200, 890, self.player.stamina / PLAYER_STAMINA)
        self.screen.blit(self.tp_obj_img, (5, 32))
        self.texter(str(self.tp), 'casper.ttf', 17, BLUE, 12, 42)

        # Testbox
        # pg.draw.rect(self.screen, LIGHTBLUE, pg.Rect(180, 180, 240, 440))
        # pg.draw.rect(self.screen, LIGHTBLUE, self.player.rect)

        abstand = 560
        for blus in range(self.player_max_health):
            if self.player_health > blus:
                pm = self.plus_img
            else:
                pm = self.minus_img
            self.screen.blit(pm, (abstand, 10))
            abstand -= 30
        abstand = 540
        for sp in range(self.sprays):
            self.screen.blit(self.spray_HUD_img, (abstand, 40))
            abstand -= 40

    def draw(self):
        pg.display.set_caption(TITLE + " mit {:.2f} Umdrehungen".format(self.clock.get_fps()))
        self.screen.blit(self.background, (0, 0))
        # All Sprites (Layered)
        self.all_sprites.draw(self.screen)
        # Treees
        self.screen.blit(self.trees, (0, 0))

        # NEBEL
        diffspeed = math.log((self.level+20)/20, 10)
        diff = 25 * (tween.easeInOutSine(self.diff_step / 25)-0.5) * self.diff_dir
        self.fog.fill((160 + diff, 160 + diff, 160 + diff))
        self.diff_step += diffspeed
        if self.diff_step > 25:
            self.diff_step = 0
            self.diff_dir *= -1
        self.light_rect.center = self.player.rect.center
        self.fog.blit(self.light_mask, self.light_rect)
        self.screen.blit(self.fog, (0, 0), special_flags=pg.BLEND_MULT)

        # Lights:
        self.screen.blit(self.lights, (0, 0))

        # Starlight
        if self.player.sternstunde:
            blity = True
            now = pg.time.get_ticks() - self.player.stern_cooldown
            if (now > STAR_D - 200 and now < STAR_D - 175) or (now > STAR_D - 125 and now < STAR_D - 100) or (now > STAR_D - 75 and now < STAR_D - 50):
                blity = False
            if blity:
                self.screen.blit(self.star_img, (int(self.player.pos.x) - 32, int(self.player.pos.y) - 25))

        self.drawHUD()

        pg.display.flip()

    def draw_player_stamina(self, surf, x, y, pct):
        if pct < 0:
            pct = 0
        BAR_LENGTH = 200
        BAR_HEIGHT = 5
        fill = int(pct * BAR_LENGTH)
        outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
        if pct > 0.99:
            col = GREEN
        elif pct > 0.25:
            col = YELLOW
        else:
            col = RED
        pg.draw.rect(surf, col, fill_rect)
        pg.draw.rect(surf, DARKGREY, outline_rect, 1)

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.pause = not self.pause
                if event.key == pg.K_m:
                    self.musicp = not self.musicp
                    if not self.musicp:
                        pg.mixer.music.pause()
                    else:
                        pg.mixer.music.unpause()


    def start_bild(self):
        self.screen.blit(self.startmenue, (0, 0))
        self.texter("Bewegung:   W A S D", 'casper.ttf', 14, WHITE, 200, 500)
        self.texter("Sprint / Auswahl:   Leertaste", 'casper.ttf', 14, WHITE, 200, 525)
        self.texter("Desinfizieren:   F", 'casper.ttf', 14, WHITE, 200, 550)
        self.texter("Musik Aus:   M", 'casper.ttf', 14, WHITE, 200, 575)
        self.texter("Pause:   ESC", 'casper.ttf', 14, WHITE, 200, 600)
        self.texter(">> Leertaste drücken um zu beginnen <<", 'casper.ttf', 20, ORANGE, 100, 650)
        pg.display.flip()
        self.wait_for_key(250)

    def buyscreen(self):
        menue = [self.tp_img, self.blussizin_img, self.spray_img, self.bier_img]
        selected = vec(0, 0)
        self.cost = [0, 0]

        def gekauft():
            if randint(1, 100) < 10:
                choice(self.effect_sounds['cash']).play()
            self.buy = False

        def rechnung():
            self.effect_sounds['select'][0].play()
            if selected.x == 100 and selected.y == 0:
                self.cost = [1, 1]
            elif selected.x == 100 and selected.y == 100:
                self.cost = [0, 1]
            elif selected.x == 0 and selected.y == 100:
                self.cost = [0, 2]
            else:
                self.cost = [0, 0]

        while self.buy:
            self.screen.blit(self.buymenue, (0, 0))
            self.texter("Kosten:", 'cortyp.ttf', 20, DARKGREY, 200, 550)
            self.texter("Benis: " + str(self.cost[0]), 'cortyp.ttf', 20, DARKGREY, 220, 590)
            self.texter("Pappe: " + str(self.cost[1]), 'cortyp.ttf', 20, DARKGREY, 220, 620)
            bb = 220
            self.clock.tick(FPS)
            for count, item in enumerate(menue, 1):
                if count % 2:
                    aa = 300
                    nexts = False
                else:
                    aa = 400
                    nexts = True
                self.screen.blit(item, (aa, bb))
                if nexts:
                    bb += 100

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.buy = False
                    self.quit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_w and selected.y > 0:
                        selected.y -= 100
                        rechnung()
                    if event.key == pg.K_s and selected.y < 100:
                        selected.y += 100
                        rechnung()
                    if event.key == pg.K_a and selected.x > 0:
                        selected.x -= 100
                        rechnung()
                    if event.key == pg.K_d and selected.x < 100:
                        selected.x += 100
                        rechnung()
                    if event.key == pg.K_SPACE:
                        if selected.x == 100 and selected.y == 0:
                            if self.player_health > 1 and self.player_max_health < 12 and self.tp >= 1:
                                self.player_max_health += 1
                                self.player_health -= 1
                                self.tp -= 1
                                print("Blussizin erworben.")
                                gekauft()
                            else:
                                self.effect_sounds['no'][0].play()
                                print("Nicht genug Blussis / Pappe, oder Maximum erreicht.")
                        elif selected.x == 0 and selected.y == 100:
                            if self.tp > 1 and self.sprays < 3:
                                self.sprays += 1
                                self.tp -= 2
                                print("Desinfektionsmittel erworben.")
                                gekauft()
                            else:
                                self.effect_sounds['no'][0].play()
                                print("Nicht genug Pappe, oder maximale Anzahl erreicht.")
                        elif selected.x == 100 and selected.y == 100:
                            if self.tp >= 1:
                                self.bier += 1
                                self.tp -= 1
                                print("Bier getrunken ...")
                                if (self.bier+self.taube) % 3 == 0:
                                    self.player_health = self.player_max_health
                                    self.effect_sounds['drink'][0].play()
                                    print("Der Alkohol wirkt Wunder.")
                                gekauft()
                            else:
                                self.effect_sounds['no'][0].play()
                                print("Nicht genug Pappe.")
                        else:
                            self.tp += 1
                            print("Klopapier ist Gold.")
                            gekauft()

            t = int(5 * (tween.easeInOutSine(self.select_step / 5)-0.5)) * self.select_dir
            select_rect = pg.Rect(int(selected.x+280) + t, int(selected.y+200) + t, 90 - 2*t, 90 - 2*t)
            pg.draw.rect(self.screen, ORANGE, select_rect, 1)
            self.select_step += 0.3
            if self.select_step > 5:
                self.select_step = 0
                self.select_dir *= -1
            self.texter("[Leertaste] zum auswählen", 'casper.ttf', 10, DARKGREY, 200, 660)
            self.drawHUD()
            pg.display.flip()

    def end(self):
        self.screen.fill(FLIESE)
        end_name = "ein Fliesentisch"
        if self.level > 14:
            self.screen.fill(NEUSCHWUCHTEL)
            end_name = "n Neuschwuchtel"
        if self.level > 20:
            self.screen.fill(WHITE)
            end_name = "n Schwuchtel"
        if self.level > 26:
            self.screen.fill(MITTELALTSCHWUCHTEL)
            end_name = "n Mittelaltschwuchtel"
        if self.level > 30:
            self.screen.fill(ALTSCHWUCHTEL)
            end_name = "n Altschwuchtel"
        if self.level > 34:
            self.screen.fill(LEGENDE)
            end_name = "ne Lebende Legende"
        if self.level > 38:
            self.screen.fill(ORANGE)
            end_name = "episch gegen Pr0rona"
        if self.level >= 45:
            self.screen.fill(LIGHTBLUE)
            end_name = "viel zu lange im Keller gewesen"
        new_high = self.set_highscore()
        self.last_play.append((self.player_walking_down_img[0], self.level))
        for i in range(len(self.last_play)):
            self.screen.blit(self.last_play[i][0], (50 + min(self.last_play[i][1]*10, 500), 50))
            self.texter("lvl. " + str(self.last_play[i][1]), 'casper.ttf', 8, DARKGREY, 75 + min(self.last_play[i][1]*10, 500), 45)
        pg.draw.circle(self.screen, FLIESE, (90, 130), 2)
        pg.draw.circle(self.screen, NEUSCHWUCHTEL, (230, 130), 2)
        pg.draw.circle(self.screen, WHITE, (290, 130), 2)
        pg.draw.circle(self.screen, MITTELALTSCHWUCHTEL, (350, 130), 2)
        pg.draw.circle(self.screen, ALTSCHWUCHTEL, (390, 130), 2)
        pg.draw.circle(self.screen, LEGENDE, (430, 130), 2)
        pg.draw.circle(self.screen, ORANGE, (470, 130), 2)
        pg.draw.circle(self.screen, BLUE, (540, 130), 2)


        self.texter("Infiziert von:", 'casper.ttf', 36, DARKGREY, 150, 150)
        abstand_inf = 0
        for inf in range(len(self.infiziert_von)):
            self.texter(str(self.infiziert_von[-inf]), 'casper.ttf', 16, BLUE, 150, 200 + abstand_inf)
            abstand_inf += 16
            if abstand_inf >= 150:
                self.texter("...", 'casper.ttf', 14, BLUE, 150, 300 + abstand_inf)
                break
        self.texter("Du hast Level: " + str(self.level) + " erreicht", 'casper.ttf', 20, LIGHTGREY, 150, 450)
        self.texter("Du bist halt " + end_name, 'casper.ttf', 20, DARKGREY, 150, 500)
        if new_high:
            self.texter("Das ist dein neuer Hochwert!", 'casper.ttf', 20, BLUE, 150, 550)
        self.texter("Leertaste drücken um erneut zu spielen", 'casper.ttf', 12, DARKGREY, 150, 600)
        y = 0
        z = 0
        for i in range(self.bier):
            if i % 10 == 0:
                y += 50
                z = 0
            else:
                z += 50
            self.screen.blit(self.bier_img, (50 + z, 650 + y))

        pg.display.flip()
        self.wait_for_key(2500)

    def wait_for_key(self, time):
        now = pg.time.get_ticks()
        pg.event.clear()
        pg.event.wait()  # clears event (funktioniert so mittel)
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP and pg.time.get_ticks() - now > time:
                    if event.key == pg.K_SPACE:
                        waiting = False
                    else:
                        pass

    def set_highscore(self):
        if self.level > self.highscore:
            with open('highscore.txt', 'w') as file:
                file.write(str(self.level))
                print("Neuer Hochwert: Level " + str(self.level))
            return True
        else:
            return False

spiel = Pr0rona()
spiel.start_bild()
while True:
    spiel.new()
    spiel.run()
    spiel.end()
