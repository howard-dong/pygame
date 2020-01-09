import pygame, sys, time, random, math

pygame.init()

global FPS, deltatime, level
FPS = 0
deltatime = 0
level = 1
countdown = 0


class Font:
    start = pygame.font.SysFont(None, 25)
    fps = pygame.font.SysFont(None, 30)
    level = pygame.font.SysFont(None, 50)
    control = pygame.font.SysFont(None, 35)

def create_window():
    global window, window_height, window_width, clock
    window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
    window_width, window_height = pygame.display.get_surface().get_size()
    clock = pygame.time.Clock()


def count_fps():
    global FPS, deltatime

    FPS = clock.get_fps()
    if FPS > 0:
        deltatime = 1 / FPS
    elif FPS == 0:
        deltatime = 0

create_window()


class Counter:
    countdown = 0
    game = 0
    win_1 = 0
    win_2 = 0
    win_3 = 0

class Colour:
    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    gray = (120, 120, 120)
    faded = (120, 120, 120, 0)
    transparent = (0, 0, 0, 0)


class Vanish:
    x = int(window_width / 2)
    ##    y = int(window_height / 7)
    y = 0
    y_change = 0
    x_change = 0


def message(font, msg, colour, pos):
    global textpos
    text = font.render(msg, True, colour)
    if pos == 1:
        textpos = text.get_rect(centerx=window_width/2, centery=window_height/2)
        window.blit(text, textpos)
    elif pos == 2:
        window.blit(text, (0, 0))

def show_fps():
    message(Font.fps, "FPS: " + str(int(FPS)), Colour.white, 2)

def level_countdown(mode):
    level_msg = ("Level %s" % level)
    if mode == 0:
        message(Font.level, level_msg, Colour.red, 1)
    if mode == 3:
        message(Font.level, "3", Colour.red, 1)
    if mode == 2:
        message(Font.level, "2", Colour.red, 1)
    if mode == 1:
        message(Font.level, "1", Colour.red, 1)


class Player:
    scale = 12
    ratio = 0.85

    def __init__(self):
        self.x = int(window_width / 2)
        self.y = int(3 * window_height / 4)
        self.mid_x = self.x + (self.x - Vanish.x) / Player.scale
        self.mid_y = self.y + (self.y - Vanish.y) / Player.scale

        self.left_x = self.mid_x - (self.mid_y - self.y) * Player.ratio
        self.right_x = self.mid_x + (self.mid_y - self.y) * Player.ratio

        self.thick = int((self.y - self.mid_y) / 3)

        self.thickness = self.right_x - self.left_x - 1

        self.x_change = 0
        self.x_speed = Player.ratio * (Vanish.y - self.y)
        self.y_speed = (Vanish.y - self.y) * Player.ratio
        self.accelerate = 0

        self.y_change = 0
        self.drift = False
        self.shift = 0


        self.left = False
        self.LEFT = False
        self.right = False
        self.RIGHT = False
        self.up = False
        self.down = False

class Obstacle:

    def __init__(self, x, y, width, height, fall_speed, shift, grow):
        self.x = x
        self.y = y
        self.w = width
        self.h = height
        self.f = fall_speed
        self.s = shift
        self.g = grow

class Game:
    def __init__(self):
        self.counter = 0
        self.acc = 0
        self.h = 1


def get_obstacle(level):
    fall_speed = 1 + (level ** 0.5)
    shift_min = - fall_speed * Vanish.x / window_height
    shift_max = fall_speed * (window_width - Vanish.x) / window_height

    shift = random.uniform(shift_min, shift_max)
    if shift > 0:
        obs_width = random.uniform(- shift_max, -1)
    elif shift < 0:
        obs_width = random.uniform(1, - shift_min)
    elif shift == 0:
        choice = random.randint(0, 1)
        if choice == 1:
            obs_width = random.uniform(1, (shift_max / 2))
        elif choice == 0:
            obs_width = - random.uniform((shift_min / 2), -1)

    return fall_speed, shift, obs_width


def show_controls(players):
    window.fill(Colour.black)
    controls_1 = ["W", "A", "S", "D"]
    controls_2 = ["8", "4", "5", "6"]
    controls_3 = ["I", "J", "K", "L"]
    if players == 1:
        surface = pygame.Surface((150, 100), pygame.HWSURFACE | pygame.SRCALPHA)
        x = [50, 0, 50, 100]
        y = [0, 50, 50, 50]
        for pos in range(4):
            pygame.draw.rect(surface, Colour.green, (x[pos] + 2, y[pos] + 2, 45, 45), 4)
            text = Font.level.render(controls_1[pos], True, Colour.white)
            text_pos = text.get_rect(centerx=x[pos] + 25, centery=y[pos] + 25)
            surface.blit(text, text_pos)

        position = surface.get_rect(centerx=window_width / 2, centery=window_height / 2)
        window.blit(surface, position)

    if players == 2:
        surface = pygame.Surface((150, 100), pygame.HWSURFACE | pygame.SRCALPHA)
        x = [50, 0, 50, 100]
        y = [0, 50, 50, 50]
        for pos in range(4):
            pygame.draw.rect(surface, Colour.green, (x[pos] + 2, y[pos] + 2, 45, 45), 4)
            text = Font.level.render(controls_1[pos], True, Colour.white)
            text_pos = text.get_rect(centerx=x[pos] + 25, centery=y[pos] + 25)
            surface.blit(text, text_pos)

        position = surface.get_rect(centerx=window_width / 2 - 150, centery=window_height / 2)
        window.blit(surface, position)

        surface = pygame.Surface((150, 100), pygame.HWSURFACE | pygame.SRCALPHA)
        x = [50, 0, 50, 100]
        y = [0, 50, 50, 50]
        for pos in range(4):
            pygame.draw.rect(surface, Colour.red, (x[pos] + 2, y[pos] + 2, 45, 45), 4)
            text = Font.level.render(controls_2[pos], True, Colour.white)
            text_pos = text.get_rect(centerx=x[pos] + 25, centery=y[pos] + 25)
            surface.blit(text, text_pos)

        position = surface.get_rect(centerx=window_width / 2 + 150, centery=window_height / 2)
        window.blit(surface, position)

    if players == 3:
        surface = pygame.Surface((150, 100), pygame.HWSURFACE | pygame.SRCALPHA)
        x = [50, 0, 50, 100]
        y = [0, 50, 50, 50]
        for pos in range(4):
            pygame.draw.rect(surface, Colour.green, (x[pos] + 2, y[pos] + 2, 45, 45), 4)
            text = Font.level.render(controls_1[pos], True, Colour.white)
            text_pos = text.get_rect(centerx=x[pos] + 25, centery=y[pos] + 25)
            surface.blit(text, text_pos)

        position = surface.get_rect(centerx=window_width / 2 - 200, centery=window_height / 2)
        window.blit(surface, position)

        surface = pygame.Surface((150, 100), pygame.HWSURFACE | pygame.SRCALPHA)
        x = [50, 0, 50, 100]
        y = [0, 50, 50, 50]
        for pos in range(4):
            pygame.draw.rect(surface, Colour.red, (x[pos] + 2, y[pos] + 2, 45, 45), 4)
            text = Font.level.render(controls_2[pos], True, Colour.white)
            text_pos = text.get_rect(centerx=x[pos] + 25, centery=y[pos] + 25)
            surface.blit(text, text_pos)

        position = surface.get_rect(centerx=window_width / 2 + 200, centery=window_height / 2)
        window.blit(surface, position)

        surface = pygame.Surface((150, 100), pygame.HWSURFACE | pygame.SRCALPHA)
        x = [50, 0, 50, 100]
        y = [0, 50, 50, 50]
        for pos in range(4):
            pygame.draw.rect(surface, Colour.blue, (x[pos] + 2, y[pos] + 2, 45, 45), 4)
            text = Font.level.render(controls_3[pos], True, Colour.white)
            text_pos = text.get_rect(centerx=x[pos] + 25, centery=y[pos] + 25)
            surface.blit(text, text_pos)

        position = surface.get_rect(centerx=window_width / 2, centery=window_height / 2)
        window.blit(surface, position)

    pygame.display.flip()

def game_play(players):
    global level, Alive_3, Alive_2, Alive_1

    count_fps()
    Obs = Game()
    countdown = 4
    level = 1

    Alive_1 = False
    Alive_2 = False
    Alive_3 = False

    if players >= 1:
        Player_1 = Player()
        Alive_1 = True
    if players >= 2:
        Player_2 = Player()
        Alive_2 = True
    if players == 3:
        Player_3 = Player()
        Alive_3 = True

    rect_1 = Obstacle(Vanish.x, Vanish.y, 0, 1, 0, 0, 0)

    Running = True
    Control = True
    Countdown = True
    Blocks = False
    Collision = False

    while Running:

        if Control:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return

                    if Alive_1:
                        if event.key == pygame.K_a:
                            if Player_1.right:
                                Player_1.LEFT = True
                                Player_1.right = False
                            else:
                                Player_1.left = True
                            Player_1.accelerate = 1

                        if event.key == pygame.K_d:
                            if Player_1.left:
                                Player_1.RIGHT = True
                                Player_1.left = False
                            else:
                                Player_1.right = True
                            Player_1.accelerate = 1

                        if event.key == pygame.K_w:
                            Player_1.up = True

                        if event.key == pygame.K_s:
                            Player_1.down = True

                    if Alive_2:
                        if event.key == pygame.K_KP4:
                            if Player_2.right:
                                Player_2.L = True
                                Player_2.right = False
                            else:
                                Player_2.left = True
                            Player_2.accelerate = 1

                        if event.key == pygame.K_KP6:
                            if Player_2.left:
                                Player_2.R = True
                                Player_2.left = False
                            else:
                                Player_2.right = True
                            Player_2.accelerate = 1

                        if event.key == pygame.K_KP8:
                            Player_2.up = True

                        if event.key == pygame.K_KP5:
                            Player_2.down = True

                    if Alive_3:
                        if event.key == pygame.K_j:
                            if Player_3.right:
                                Player_3.L = True
                                Player_3.right = False
                            else:
                                Player_3.left = True
                            Player_3.accelerate = 1

                        if event.key == pygame.K_l:
                            if Player_3.left:
                                Player_3.R = True
                                Player_3.left = False
                            else:
                                Player_3.right = True
                            Player_3.accelerate = 1

                        if event.key == pygame.K_i:
                            Player_3.up = True

                        if event.key == pygame.K_k:
                            Player_3.down = True

                if event.type == pygame.KEYUP:
                    if Alive_1:
                        if event.key == pygame.K_a:
                            if Player_1.RIGHT:
                                Player_1.RIGHT = False
                                Player_1.right = True
                            if Player_1.LEFT:
                                Player_1.LEFT = False
                                Player_1.right = True
                            Player_1.left = False
                            Player_1.x_change = 0

                        if event.key == pygame.K_d:
                            if Player_1.LEFT:
                                Player_1.LEFT = False
                                Player_1.left = True
                            if Player_1.RIGHT:
                                Player_1.RIGHT = False
                                Player_1.left = True
                            Player_1.right = False
                            Player_1.x_change = 0

                        if event.key == pygame.K_w:
                            Player_1.up = False
                            Player_1.y_change = 0
                            Player_1.shift = 0

                        if event.key == pygame.K_s:
                            Player_1.down = False
                            Player_1.y_change = 0
                            Player_1.shift = 0
                    if Alive_2:
                        if event.key == pygame.K_KP4:
                            if Player_2.RIGHT:
                                Player_2.RIGHT = False
                                Player_2.right = True
                            if Player_2.LEFT:
                                Player_2.LEFT = False
                                Player_2.right = True
                            Player_2.left = False
                            Player_2.x_change = 0

                        if event.key == pygame.K_KP6:
                            if Player_2.LEFT:
                                Player_2.LEFT = False
                                Player_2.left = True
                            if Player_2.RIGHT:
                                Player_2.RIGHT = False
                                Player_2.left = True
                            Player_2.right = False
                            Player_2.x_change = 0

                        if event.key == pygame.K_KP8:
                            Player_2.up = False
                            Player_2.y_change = 0
                            Player_2.shift = 0

                        if event.key == pygame.K_KP5:
                            Player_2.down = False
                            Player_2.y_change = 0
                            Player_2.shift = 0
                    if Alive_3:
                        if event.key == pygame.K_j:
                            if Player_3.RIGHT:
                                Player_3.RIGHT = False
                                Player_3.right = True
                            if Player_3.LEFT:
                                Player_3.LEFT = False
                                Player_3.right = True
                            Player_3.left = False
                            Player_3.x_change = 0

                        if event.key == pygame.K_l:
                            if Player_3.LEFT:
                                Player_3.LEFT = False
                                Player_3.left = True
                            if Player_3.RIGHT:
                                Player_3.RIGHT = False
                                Player_3.left = True
                            Player_3.right = False
                            Player_3.x_change = 0

                        if event.key == pygame.K_i:
                            Player_3.up = False
                            Player_3.y_change = 0
                            Player_3.shift = 0

                        if event.key == pygame.K_k:
                            Player_3.down = False
                            Player_3.y_change = 0
                            Player_3.shift = 0

            # Wall Barriers

            length = (window_height * Vanish.x) / (window_width - Vanish.x)

            if Alive_1:
                if Player_1.left_x < Vanish.x:
                    if (Player_1.mid_y < (window_height - (window_height * Player_1.left_x) / Vanish.x)):
                        Player_1.left_x = (- Vanish.x * (Player_1.mid_y - window_height)) / window_height
                        Player_1.mid_x = Player_1.left_x + (Player_1.mid_y - Player_1.y) * Player_1.ratio
                        Player_1.x = ((Player_1.scale * Player_1.mid_x + Vanish.x)/(1 + Player_1.scale)) + 1
                        Player_1.accelerate = 0
                        Player_1.x_change = 0

                if Player_1.right_x > Vanish.x:
                    if (Player_1.mid_y < ((((length + window_height) * Player_1.right_x) / window_width - (length)))):
                        Player_1.right_x = (((length) + Player_1.mid_y) * window_width) / (length + window_height)
                        Player_1.mid_x = Player_1.right_x - (Player_1.mid_y - Player_1.y) * Player_1.ratio
                        Player_1.x = ((Player_1.scale * Player_1.mid_x + Vanish.x)/(1 + Player_1.scale)) - 1
                        Player_1.accelerate = 0
                        Player_1.x_change = 0

                if Player_1.mid_y > window_height:
                    Player_1.y = window_height + (Player_1.thick) * 3
            if Alive_2:
                if Player_2.left_x < Vanish.x:
                    if (Player_2.mid_y < (window_height - (window_height * Player_2.left_x) / Vanish.x)):
                        Player_2.left_x = (- Vanish.x * (Player_2.mid_y - window_height)) / window_height
                        Player_2.mid_x = Player_2.left_x + (Player_2.mid_y - Player_2.y) * Player_2.ratio
                        Player_2.x = ((Player_2.scale * Player_2.mid_x + Vanish.x)/(1 + Player_2.scale)) + 1
                        Player_2.accelerate = 0
                        Player_2.x_change = 0

                if Player_2.right_x > Vanish.x:
                    if (Player_2.mid_y < ((((length + window_height) * Player_2.right_x) / window_width - (length)))):
                        Player_2.right_x = (((length) + Player_2.mid_y) * window_width) / (length + window_height)
                        Player_2.mid_x = Player_2.right_x - (Player_2.mid_y - Player_2.y) * Player_2.ratio
                        Player_2.x = ((Player_2.scale * Player_2.mid_x + Vanish.x)/(1 + Player_2.scale)) - 1
                        Player_2.accelerate = 0
                        Player_2.x_change = 0

                if Player_2.mid_y > window_height:
                    Player_2.y = window_height + (Player_2.thick) * 3
            if Alive_3:
                if Player_3.left_x < Vanish.x:
                    if (Player_3.mid_y < (window_height - (window_height * Player_3.left_x) / Vanish.x)):
                        Player_3.left_x = (- Vanish.x * (Player_3.mid_y - window_height)) / window_height
                        Player_3.mid_x = Player_3.left_x + (Player_3.mid_y - Player_3.y) * Player_3.ratio
                        Player_3.x = ((Player_3.scale * Player_3.mid_x + Vanish.x)/(1 + Player_3.scale)) + 1
                        Player_3.accelerate = 0
                        Player_3.x_change = 0

                if Player_3.right_x > Vanish.x:
                    if (Player_3.mid_y < ((((length + window_height) * Player_3.right_x) / window_width - (length)))):
                        Player_3.right_x = (((length) + Player_3.mid_y) * window_width) / (length + window_height)
                        Player_3.mid_x = Player_3.right_x - (Player_3.mid_y - Player_3.y) * Player_3.ratio
                        Player_3.x = ((Player_3.scale * Player_3.mid_x + Vanish.x)/(1 + Player_3.scale)) - 1
                        Player_3.accelerate = 0
                        Player_3.x_change = 0

                if Player_3.mid_y > window_height:
                    Player_3.y = window_height + (Player_3.thick) * 3

            # Movement
            if Alive_1:
                Player_1.x_speed = 0.5 * Player_1.ratio * (Player_1.y - Vanish.y) + (level ** 0.5) / level

                if Player_1.LEFT or Player_1.left:
                    Player_1.x_change = - int(Player_1.accelerate ** 1.6) * Player_1.x_speed * deltatime
                if Player_1.RIGHT or Player_1.right:
                    Player_1.x_change = int(Player_1.accelerate ** 1.6) * Player_1.x_speed * deltatime

                Player_1.accelerate += 0.1

                Player_1.y_speed = (Vanish.y - Player_1.y) + (level ** 0.5) / level

                if (Player_1.x > Vanish.x) or (Player_1.x < Vanish.x):
                    Player_1.drift = True

                if Player_1.up:
                    Player_1.y_change = Player_1.y_speed * deltatime
                    if Player_1.drift:
                        Player_1.shift = -(Player_1.x - Vanish.x) * deltatime

                if Player_1.down:
                    Player_1.y_change = - Player_1.y_speed * deltatime
                    if Player_1.drift:
                        Player_1.shift = (Player_1.x - Vanish.x) * deltatime

                Player_1.x += Player_1.x_change + Player_1.shift
                Player_1.y += Player_1.y_change

                Player_1.mid_x = Player_1.x + (Player_1.x - Vanish.x) / Player_1.scale
                Player_1.mid_y = Player_1.y + (Player_1.y - Vanish.y) / Player_1.scale
            if Alive_2:
                Player_2.x_speed = 0.5 * Player_2.ratio * (Player_2.y - Vanish.y) + (level ** 0.5) / level

                if Player_2.LEFT or Player_2.left:
                    Player_2.x_change = - int(Player_2.accelerate ** 1.6) * Player_2.x_speed * deltatime
                if Player_2.RIGHT or Player_2.right:
                    Player_2.x_change = int(Player_2.accelerate ** 1.6) * Player_2.x_speed * deltatime

                Player_2.accelerate += 0.1

                Player_2.y_speed = (Vanish.y - Player_2.y) + (level ** 0.5) / level

                if (Player_2.x > Vanish.x) or (Player_2.x < Vanish.x):
                    Player_2.drift = True

                if Player_2.up:
                    Player_2.y_change = Player_2.y_speed * deltatime
                    if Player_2.drift:
                        Player_2.shift = -(Player_2.x - Vanish.x) * deltatime

                if Player_2.down:
                    Player_2.y_change = - Player_2.y_speed * deltatime
                    if Player_2.drift:
                        Player_2.shift = (Player_2.x - Vanish.x) * deltatime

                Player_2.x += Player_2.x_change + Player_2.shift
                Player_2.y += Player_2.y_change

                Player_2.mid_x = Player_2.x + (Player_2.x - Vanish.x) / Player_2.scale
                Player_2.mid_y = Player_2.y + (Player_2.y - Vanish.y) / Player_2.scale
            if Alive_3:
                Player_3.x_speed = 0.5 * Player_3.ratio * (Player_3.y - Vanish.y) + (level ** 0.5) / level

                if Player_3.LEFT or Player_3.left:
                    Player_3.x_change = - int(Player_3.accelerate ** 1.6) * Player_3.x_speed * deltatime
                if Player_3.RIGHT or Player_3.right:
                    Player_3.x_change = int(Player_3.accelerate ** 1.6) * Player_3.x_speed * deltatime

                Player_3.accelerate += 0.1

                Player_3.y_speed = (Vanish.y - Player_3.y) + (level ** 0.5) / level

                if (Player_3.x > Vanish.x) or (Player_3.x < Vanish.x):
                    Player_3.drift = True

                if Player_3.up:
                    Player_3.y_change = Player_3.y_speed * deltatime
                    if Player_3.drift:
                        Player_3.shift = -(Player_3.x - Vanish.x) * deltatime

                if Player_3.down:
                    Player_3.y_change = - Player_3.y_speed * deltatime
                    if Player_3.drift:
                        Player_3.shift = (Player_3.x - Vanish.x) * deltatime

                Player_3.x += Player_3.x_change + Player_3.shift
                Player_3.y += Player_3.y_change

                Player_3.mid_x = Player_3.x + (Player_3.x - Vanish.x) / Player_3.scale
                Player_3.mid_y = Player_3.y + (Player_3.y - Vanish.y) / Player_3.scale

            # Player Shapes

            if Alive_1:
                Player_1.thick = int((Player_1.y - Player_1.mid_y) / 3)
                Player_1.left_x = Player_1.mid_x - (Player_1.mid_y - Player_1.y) * Player_1.ratio
                Player_1.right_x = Player_1.mid_x + (Player_1.mid_y - Player_1.y) * Player_1.ratio

                triangle_p_1 = [(Player_1.x, Player_1.y)]
                triangle_p_1.append((Player_1.left_x, Player_1.mid_y))
                triangle_p_1.append((Player_1.right_x, Player_1.mid_y))

                thick_l_1 = [(Player_1.x, Player_1.y)]
                thick_l_1.append((Player_1.x, (Player_1.y - Player_1.thick)))
                thick_l_1.append((Player_1.left_x, Player_1.mid_y - Player_1.thick))
                thick_l_1.append((Player_1.left_x, Player_1.mid_y))

                thick_r_1 = [(Player_1.x, Player_1.y)]
                thick_r_1.append((Player_1.x, (Player_1.y - Player_1.thick)))
                thick_r_1.append((Player_1.right_x, Player_1.mid_y - Player_1.thick))
                thick_r_1.append((Player_1.right_x, Player_1.mid_y))

                thick_b_1 = []
                thick_b_1.append((Player_1.left_x, Player_1.mid_y - Player_1.thick))
                thick_b_1.append((Player_1.left_x, Player_1.mid_y))
                thick_b_1.append((Player_1.right_x, Player_1.mid_y))
                thick_b_1.append((Player_1.right_x, Player_1.mid_y - Player_1.thick))

            if Alive_2:
                Player_2.thick = int((Player_2.y - Player_2.mid_y) / 3)
                Player_2.left_x = Player_2.mid_x - (Player_2.mid_y - Player_2.y) * Player_2.ratio
                Player_2.right_x = Player_2.mid_x + (Player_2.mid_y - Player_2.y) * Player_2.ratio

                triangle_p_2 = [(Player_2.x, Player_2.y)]
                triangle_p_2.append((Player_2.left_x, Player_2.mid_y))
                triangle_p_2.append((Player_2.right_x, Player_2.mid_y))

                thick_l_2 = [(Player_2.x, Player_2.y)]
                thick_l_2.append((Player_2.x, (Player_2.y - Player_2.thick)))
                thick_l_2.append((Player_2.left_x, Player_2.mid_y - Player_2.thick))
                thick_l_2.append((Player_2.left_x, Player_2.mid_y))

                thick_r_2 = [(Player_2.x, Player_2.y)]
                thick_r_2.append((Player_2.x, (Player_2.y - Player_2.thick)))
                thick_r_2.append((Player_2.right_x, Player_2.mid_y - Player_2.thick))
                thick_r_2.append((Player_2.right_x, Player_2.mid_y))

                thick_b_2 = []
                thick_b_2.append((Player_2.left_x, Player_2.mid_y - Player_2.thick))
                thick_b_2.append((Player_2.left_x, Player_2.mid_y))
                thick_b_2.append((Player_2.right_x, Player_2.mid_y))
                thick_b_2.append((Player_2.right_x, Player_2.mid_y - Player_2.thick))

            if Alive_3:
                Player_3.thick = int((Player_3.y - Player_3.mid_y) / 3)
                Player_3.left_x = Player_3.mid_x - (Player_3.mid_y - Player_3.y) * Player_3.ratio
                Player_3.right_x = Player_3.mid_x + (Player_3.mid_y - Player_3.y) * Player_3.ratio

                triangle_p_3 = [(Player_3.x, Player_3.y)]
                triangle_p_3.append((Player_3.left_x, Player_3.mid_y))
                triangle_p_3.append((Player_3.right_x, Player_3.mid_y))

                thick_l_3 = [(Player_3.x, Player_3.y)]
                thick_l_3.append((Player_3.x, (Player_3.y - Player_3.thick)))
                thick_l_3.append((Player_3.left_x, Player_3.mid_y - Player_3.thick))
                thick_l_3.append((Player_3.left_x, Player_3.mid_y))

                thick_r_3 = [(Player_3.x, Player_3.y)]
                thick_r_3.append((Player_3.x, (Player_3.y - Player_3.thick)))
                thick_r_3.append((Player_3.right_x, Player_3.mid_y - Player_3.thick))
                thick_r_3.append((Player_3.right_x, Player_3.mid_y))

                thick_b_3 = []
                thick_b_3.append((Player_3.left_x, Player_3.mid_y - Player_3.thick))
                thick_b_3.append((Player_3.left_x, Player_3.mid_y))
                thick_b_3.append((Player_3.right_x, Player_3.mid_y))
                thick_b_3.append((Player_3.right_x, Player_3.mid_y - Player_3.thick))

        window.fill(Colour.black)

        road_points = ((Vanish.x, Vanish.y), (0, window_height), (window_width, window_height))
        pygame.draw.polygon(window, Colour.gray, road_points)

        if Alive_1:
            pygame.draw.polygon(window, Colour.green, (triangle_p_1))
            pygame.draw.polygon(window, Colour.green, (thick_l_1))
            pygame.draw.polygon(window, Colour.green, (thick_r_1))
            pygame.draw.polygon(window, Colour.green, (thick_b_1))
        if Alive_2:
            pygame.draw.polygon(window, Colour.red, (triangle_p_2))
            pygame.draw.polygon(window, Colour.red, (thick_l_2))
            pygame.draw.polygon(window, Colour.red, (thick_r_2))
            pygame.draw.polygon(window, Colour.red, (thick_b_2))
        if Alive_3:
            pygame.draw.polygon(window, Colour.blue, (triangle_p_3))
            pygame.draw.polygon(window, Colour.blue, (thick_l_3))
            pygame.draw.polygon(window, Colour.blue, (thick_r_3))
            pygame.draw.polygon(window, Colour.blue, (thick_b_3))

        if Blocks:
            if Obs.counter < (level * 2):

                if rect_1.y == 0:
                    rect_1.f, rect_1.s, rect_1.g = get_obstacle(level)
                    rect_1.y = 1

                if 0 < rect_1.y < window_height:
                    pygame.draw.rect(window, (255, 255, 255, 100), (rect_1.x, rect_1.y, rect_1.w, rect_1.h))
                    rect_1.w += rect_1.g * Obs.acc * deltatime
                    rect_1.h += Obs.h * Obs.acc * deltatime
                    rect_1.x += rect_1.s * Obs.acc * deltatime
                    rect_1.y += rect_1.f * Obs.acc * deltatime

                    Obs.acc += level * deltatime * 100

                if rect_1.y > window_height:
                    rect_1.y = 0
                    rect_1.h = 1
                    rect_1.x = Vanish.x
                    rect_1.w = 1

                    Obs.acc = 0
                    Obs.counter += 1

            else:
                level += 1
                Obs.counter = 0
                Countdown = True
                countdown = 4
                Blocks = False

        # Collision
        if Alive_1:
            if rect_1.w < 0:
                if (rect_1.x + rect_1.w < Player_1.left_x < rect_1.x) or (
                        rect_1.x + rect_1.w < Player_1.right_x < rect_1.x):
                    if (rect_1.y) + rect_1.h / 2 < Player_1.y < (rect_1.y + rect_1.h):
                        Blocks = False
                        Collision = True
                        Alive_1 = False

            if rect_1.w > 0:
                if (rect_1.x < Player_1.left_x < rect_1.x + rect_1.w) or (
                        rect_1.x < Player_1.right_x < rect_1.x + rect_1.w):
                    if (rect_1.y) + rect_1.h / 2 < Player_1.y < (rect_1.y + rect_1.h):
                        Blocks = False
                        Collision = True
                        Alive_1 = False
        if Alive_2:
            if rect_1.w < 0:
                if (rect_1.x + rect_1.w < Player_2.left_x < rect_1.x) or (
                        rect_1.x + rect_1.w < Player_2.right_x < rect_1.x):
                    if (rect_1.y) + rect_1.h / 2 < Player_2.y < (rect_1.y + rect_1.h):
                        Blocks = False
                        Collision = True
                        Alive_2 = False

            if rect_1.w > 0:
                if (rect_1.x < Player_2.left_x < rect_1.x + rect_1.w) or (
                        rect_1.x < Player_2.right_x < rect_1.x + rect_1.w):
                    if (rect_1.y) + rect_1.h / 2 < Player_2.y < (rect_1.y + rect_1.h):
                        Blocks = False
                        Collision = True
                        Alive_2 = False
        if Alive_3:
            if rect_1.w < 0:
                if (rect_1.x + rect_1.w < Player_3.left_x < rect_1.x) or (
                        rect_1.x + rect_1.w < Player_3.right_x < rect_1.x):
                    if (rect_1.y) + rect_1.h / 2 < Player_3.y < (rect_1.y + rect_1.h):
                        Blocks = False
                        Collision = True
                        Alive_3 = False

            if rect_1.w > 0:
                if (rect_1.x < Player_3.left_x < rect_1.x + rect_1.w) or (
                        rect_1.x < Player_3.right_x < rect_1.x + rect_1.w):
                    if (rect_1.y) + rect_1.h / 2 < Player_3.y < (rect_1.y + rect_1.h):
                        Blocks = False
                        Collision = True
                        Alive_3 = False

        if Collision:
            if players == 1:
                window.fill(Colour.black)
                msg = "Only level %s" % level

                message(Font.level, msg, Colour.red, 1)

                pygame.display.flip()

                time.sleep(1)

                window.fill(Colour.black)

                message(Font.level, "Try again lol", Colour.red, 1)

                pygame.display.flip()

                time.sleep(1)

                return

            elif players == 2:
                if not Alive_1 and not Alive_2:
                    message(Font.level, "You both died haha", Colour.red, 1)
                elif Alive_2:
                    message(Font.level, "Red wins!", Colour.red, 1)
                elif Alive_1:
                    message(Font.level, "Green wins!", Colour.red, 1)
                pygame.display.flip()
                time.sleep(2)
                window.fill(Colour.black)
                msg = "Only level %s" % level
                message(Font.level, msg, Colour.red, 1)
                pygame.display.flip()
                time.sleep(1)
                return

            elif players == 3:
                if not Alive_1 and not Alive_2 and not Alive_3:
                    message(Font.level, "Wow you all died", Colour.red, 1)
                elif not Alive_1 and not Alive_2:
                    message(Font.level, "Blue wins!", Colour.red, 1)
                elif not Alive_1 and not Alive_3:
                    message(Font.level, "Red wins!", Colour.red, 1)
                elif not Alive_2 and not Alive_3:
                    message(Font.level, "Green wins!", Colour.red, 1)
                elif (Alive_1 and Alive_2) or (Alive_1 and Alive_3) or (Alive_3 and Alive_2):
                    Collision = False
                    Blocks = True
                    continue
                pygame.display.flip()
                time.sleep(2)
                window.fill(Colour.black)
                msg = "Only level %s" % level
                message(Font.level, msg, Colour.red, 1)
                pygame.display.flip()
                time.sleep(1)
                return

        if Countdown:
            if countdown <= 0:
                Blocks = True
                Countdown = False

            elif countdown <= 1:
                level_countdown(1)

            elif countdown <= 2:
                level_countdown(2)

            elif countdown <= 3:
                level_countdown(3)

            elif countdown <= 4:
                level_countdown(0)

            countdown -= deltatime * 2



            # if 0 <= Counter.countdown < 120:
            #     level_countdown(0)
            # if 140 < Counter.countdown < 260:
            #     level_countdown(3)
            # if 280 < Counter.countdown < 400:
            #     level_countdown(2)
            # if 440 < Counter.countdown < 560:
            #     level_countdown(1)
            # if Counter.countdown > 580:
            #     Blocks = True
            #     Counter.countdown = 0
            #     Countdown = False
            # Counter.countdown += deltatime * 200

        show_fps()
        pygame.display.flip()
        clock.tick()
        count_fps()


def game_start():
    Selection = True

    while Selection:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    Selection = False
                if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                    show_controls(1)
                    time.sleep(1)
                    game_play(1)
                if event.key == pygame.K_2 or event.key == pygame.K_KP2:
                    show_controls(2)
                    time.sleep(1)
                    game_play(2)
                if event.key == pygame.K_3 or event.key == pygame.K_KP3:
                    show_controls(3)
                    time.sleep(1)
                    game_play(3)

        window.fill(Colour.black)
        message(Font.start, "How many players?  1, 2, or 3?", Colour.white, 1)
        message(Font.fps, "Press Escape to leave any time during the game", Colour.white, 2)

        pygame.display.flip()

    window.fill(Colour.black)
    message(Font.start, "Goodbye! ", Colour.white, 1)
    pygame.display.flip()
    count_fps()

    time.sleep(1)

    return

game_start()
pygame.quit()
sys.exit()
