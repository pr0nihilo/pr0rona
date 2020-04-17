import pytweening as tween

# Fenstereigenschaften:
WIDTH = 600
HEIGHT = 900
TITLE = "Pr0rona"
FPS = 60

# Farben (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (238, 77, 46)
ORANGE2 = (252, 136, 51)
ORANGE3 = (240, 173, 78)
TEXTCOLOR = (242, 245, 244)
LIGHTBLUE = (117, 192, 199)
YELLOW = (247, 197, 22)  # promium
GREEN = (92, 184, 92)
RED = (217, 83, 79)
BLUE = (0, 143, 255)  # Episch
DARKGREY = (22, 22, 24)
LIGHTGREY = (100, 100, 100)
CYAN = (0, 255, 255)

FLIESE = (108, 67, 43)
NEUSCHWUCHTEL = (225, 8, 233)
EDLERSPENDER = (23, 185, 146)
ALTSCHWUCHTEL = (91, 185, 28)
MITTELALTSCHWUCHTEL = (173, 220, 141)
LEGENDE = (28, 185, 146)

# Sound Bibliothek
EFFECT_SOUNDS = {
    'start': ['start.wav', 'start2.wav'],
    'up': ['up1.wav'],
    'no': ['no.wav'],
    'spray': ['spray.wav', 'spray2.wav'],
    'select': ['select.wav'],
    'cash': ['cash1.wav'],
    'star': ['star.wav'],
    'schmuser': ['schmuser.wav'],
    'drink': ['drink.wav', 'eat.wav'],
    'pavele': ['pavele.wav'],
    'regen': ['regen.wav'],
    'win': ['win1.wav', 'win2.wav', 'win3.wav', 'win4.wav', 'win5.wav',
            'win6.wav', 'win7.wav', 'win8.wav', 'win9.wav', 'win10.wav',
            'win11.wav'],
    'loose': ['loose1.wav', 'loose2.wav', 'loose3.wav', 'loose4.wav',
              'loose5.wav', 'loose6.wav', 'loose7.wav', 'loose8.wav',
              'loose9.wav', 'loose10.wav', 'loose11.wav']
}

# VIRUS
VIRUS_IMAGES = ['Red_Virus.png', 'Pink_Virus.png', 'Blue_Virus.png', 'Green_Virus.png', 'Yellow_Virus.png', 'Orange_Virus.png', 'Turkies_Virus.png']
VIRUS_NAMEN = ["Neuschwuchtel", "Schwuchtel", "Gamb", "pr0nihilo", "FunnyCunni", "pavele", "Schmusekadser", "Altschwuchtel", "Bellkadse", "TikTok",
               "Hurens0hn", "RundesBalli", "GabberGundalf", "Jcing95", "fapp0t", "ogmo", "vanDimas", "Neuronaut", "Gulliulli", "Pr0toffel", "Blumenfee",
               "Pr0lerus", "derwombat", "Kadmiumoxid", "babypfau", "100tSpastille", "DeutscheKrebshilfe", "Schrimp", "lindraupe", "Bumsrind", "Dinath",
               "Alive1093", "schmuserl0ver", "SchmuserBen", "AmaZzinq", "schxrz", "JT421", "Karpatia", "MissRaten", "miesekadse", "seren", "BadBunny",
               "stfu", "Cialis", "mimona", "buttinger", "Shibi", "Jibnome", "BlaueBete", "Joernrich", "R0bsen", "pr0ruler"]
VIREN_SPEED = 0.3
VIRUS_RANGEX = 350
VIRUS_RANGEY = 22

VIRUS_TWEEN = (tween.easeInOutQuart, tween.easeInOutBounce, tween.easeInOutSine,
               tween.easeInOutBack, tween.easeInOutElastic, tween.easeInOutCirc,
               tween.easeInOutCubic, tween.easeInOutExpo, tween.easeInOutQuad, tween.easeInOutQuint)

# Spieler
PLAYER_SPRITES = ('char_01.png', 'char_02.png', 'char_03.png', 'char_04.png', 'char_05.png', 'char_06.png',
                  'char_07.png', 'char_08.png', 'char_09.png', 'char_10.png', 'char_11.png', 'char_12.png')
PLAYER_HEALTH = 3
PLAYER_STAMINA = 2000
PLAYER_SPEED = 122
ROLL_SPEED = 15
ATTACK_D_STD = 600
ROLL_D_STD = 500
STAR_D = 1000
STARTX = 300
STARTY = 825

# ITEM
ITEM_IMAGES = {
    'blussi': 'Plus_dick.png',
    'globuli': 'globuli.png',
    'star': 'star.png',
    'schmuser': 'schmuser.png',
    'taube': 'taube.png',
    'blue': 'blue.png',
    'red': 'red.png'
}
BOB_RANGE = 5
BOB_SPEED = 0.1

# Effekt Überlagerung
LIGHT_MASK = 'light_350_soft.png'
LIGHT_RADIUS = (500, 500)

# LAYERS
OBJECT_LAYER = 1
VIREN_LAYER = 2
PLAYER_LAYER = 3
SPRAY_LAYER = 4
EFFECTS_LAYER = 1

