import pygame
import sys
import time
import random
import math

pygame.init()

FPS = 0
deltatime = 0
delta_mouse_x = 0
delta_mouse_y = 0
camera_x = 0
camera_y = 0

class Colour:
    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    gray = (120, 120, 120)
    grass = (45, 128, 1)
    yellow = (255, 255, 0)

class Font:
    start = pygame.font.SysFont(None, 25)
    fps = pygame.font.SysFont(None, 30)
    level = pygame.font.SysFont(None, 50)


def create_interface():
    global window, window_height, window_width, clock, hud
    global Map, map_height, map_width
    window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
    window_width, window_height = pygame.display.get_surface().get_size()
    hud = pygame.display.set_mode((window_width, window_height), pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)

    map_height = window_height * 2
    map_width = window_width * 4
    Map = pygame.Surface((map_width, map_height), pygame.HWSURFACE)

    clock = pygame.time.Clock()

create_interface()


class Gun:

    frame = [
        "FPS Machine Gun 0.png",
        "FPS Machine Gun 1.png",
        "FPS Machine Gun 2.png",
        "FPS Machine Gun 3.png",
        "FPS Machine Gun 4.png",
    ]

    def Load_gun(file):
        gun_hud = pygame.image.load(file)
        gun_hud = pygame.transform.scale(gun_hud, (window_width, window_height))
        surface = pygame.Surface((window_width, window_height), pygame.HWSURFACE | pygame.SRCALPHA)
        surface.blit(gun_hud, (0, 0))
        return surface

    gun_0 = Load_gun(frame[0])
    gun_1 = Load_gun(frame[1])
    gun_2 = Load_gun(frame[2])
    gun_3 = Load_gun(frame[3])
    gun_4 = Load_gun(frame[4])

def count_fps():
    global FPS, deltatime

    FPS = clock.get_fps()
    if FPS > 0:
        deltatime = 1 / FPS

def message(font, msg, colour, pos, x_pos=0, y_pos=0):
    global textpos
    text = font.render(msg, True, colour)
    if pos == 1:
        textpos = text.get_rect(centerx=window_width / 2, centery=window_height / 2)
        window.blit(text, textpos)
    elif pos == 2:
        window.blit(text, (0, 0))
    elif pos == 3:
        window.blit(text, (window_width - 200, 10))
    elif pos == 4:
        window.blit(text, (x_pos, y_pos))

def show_fps():
    message(Font.fps, "FPS: " + str(int(FPS)), Colour.white, 2)

class Enemy:
    def __init__(self, x, y, x_change, y_change, width):
        self.x_change = x_change
        self.y_change = y_change
        self.x = x + self.x_change
        self.y = y + self.y_change

        self.width = width

def spawn_enemy(num):
    global enemy_1, enemy_2, enemy_3, enemy_4, enemy_5, enemy_6
    x = random.randint(100, map_width - 100)
    y = int(map_height / 3) + 10
    width = int((y - map_height / 3) / 5)
    if num == 1:
        enemy_1 = Enemy(x, y, 0, 0, width)
    if num == 2:
        enemy_2 = Enemy(x, y, 0, 0, width)
    if num == 3:
        enemy_3 = Enemy(x, y, 0, 0, width)
    if num == 4:
        enemy_4 = Enemy(x, y, 0, 0, width)
    if num == 5:
        enemy_5 = Enemy(x, y, 0, 0, width)
    if num == 6:
        enemy_6 = Enemy(x, y, 0, 0, width)

def draw_enemy(x, y, width, num = 0):

    # 0 = Pool of blood
    # 1 = Red on black angry
    # 2 = Red on white angry
    # 3 = Black on Yellow -_-
    # 4 = Black on Yellow wow
    # 5 = Black and White on Yellow frown

    if num == 0:
        pygame.draw.ellipse(Map, Colour.red, (int(x) - width, int(y), width * 2, int(width)))

    if num == 1:
        pygame.draw.circle(Map, Colour.black, (int(x), int(y)), width)
        left_eye = [
            (x - int(width/4), y),
            (x - int(width*2/3), y - int(width/3)),
            (x - int(width*3/4), y)
        ]
        right_eye = [
            (x + int(width / 4), y),
            (x + int(width * 2 / 3), y - int(width / 3)),
            (x + int(width * 3 / 4), y)
        ]
        mouth = [
            (x - int(width / 3), y + int(width / 4)),
            (x - int(width * 2 / 3), y + int(width / 2)),
            (x + int(width * 2 / 3), y + int(width / 2)),
            (x + int(width / 3), y + int(width / 4)),

        ]
        pygame.draw.polygon(Map, Colour.red, right_eye)
        pygame.draw.polygon(Map, Colour.red, left_eye)
        pygame.draw.polygon(Map, Colour.red, mouth)

    if num == 2:
        pygame.draw.circle(Map, Colour.white, (int(x), int(y)), width)
        left_eye = [
            (x - int(width/4), y),
            (x - int(width*2/3), y - int(width/3)),
            (x - int(width*3/4), y)
        ]
        right_eye = [
            (x + int(width / 4), y),
            (x + int(width * 2 / 3), y - int(width / 3)),
            (x + int(width * 3 / 4), y)
        ]
        mouth = [
            (x - int(width / 3), y + int(width / 4)),
            (x - int(width * 2 / 3), y + int(width / 2)),
            (x + int(width * 2 / 3), y + int(width / 2)),
            (x + int(width / 3), y + int(width / 4)),

        ]
        pygame.draw.polygon(Map, Colour.red, right_eye)
        pygame.draw.polygon(Map, Colour.red, left_eye)
        pygame.draw.polygon(Map, Colour.red, mouth)

    if num == 3:
        pygame.draw.circle(Map, Colour.yellow, (int(x), int(y)), width)
        pygame.draw.line(Map, Colour.black, (int(x - width*2/3), int(y)), (int(x - width / 4), int(y)), 1)
        pygame.draw.line(Map, Colour.black, (int(x + width*2/3), int(y)), (int(x + width / 4), int(y)), 1)
        pygame.draw.line(Map, Colour.black, (int(x-width/3), int(y+width/2)), (int(x+width/3), int(y+width/2)), 1)

    if num == 4:
        pygame.draw.circle(Map, Colour.yellow, (int(x), int(y)), width)
        pygame.draw.ellipse(Map, Colour.black, (int(x - width/2), int(y - width/2), int(width/3), int(width / 2)))
        pygame.draw.ellipse(Map, Colour.black, (int(x + width/2 - width/ 3), int(y - width/2), int(width/3), int(width / 2)))
        pygame.draw.circle(Map, Colour.white, (int(x - width/3), int(y - width/3)), int(width/8))
        pygame.draw.circle(Map, Colour.white, (int(x + width/3), int(y - width/3)), int(width/8))
        pygame.draw.ellipse(Map, Colour.black, (int(x - width / 4), int(y + width/10), int(width / 2), int(width * 2 / 3)))

    if num == 5:
        pygame.draw.circle(Map, Colour.yellow, (int(x), int(y)), width)
        pygame.draw.circle(Map, Colour.white, (int(x - width * 3 / 8), int(y)), int(width / 4))
        pygame.draw.circle(Map, Colour.white, (int(x + width * 3 / 8), int(y)), int(width / 4))
        pygame.draw.rect(Map, Colour.black, (int(x - width * 2 / 3), int(y - width/ 3), int(4 * width / 3), int(width/8)))
        pygame.draw.ellipse(Map, Colour.black, (int(x - width / 2), int(y + width/3), int(width), int(width / 2)))
        pygame.draw.ellipse(Map, Colour.yellow, (int(x - width / 2), int(y + width*4/9), int(width), int(width / 2)))

    if num == 6:
        pygame.draw.circle(Map, Colour.blue, (int(x), int(y)), width)
        pygame.draw.circle(Map, Colour.white, (int(x - width / 3), int(y - width / 4)), int(width/3), int(width/12))
        pygame.draw.circle(Map, Colour.white, (int(x + width / 3), int(y - width / 4)), int(width/3), int(width/12))
        pygame.draw.ellipse(Map, Colour.white, (int(x - width / 4), int(y), int(width / 2), int(width * 4 / 5)), int(width/12))


def update_enemy(level, enemy_num):
    global enemy_1, enemy_2, enemy_3, enemy_4, enemy_5, enemy_6 , deltatime
    shift = int(random.randint(-100, 100) * deltatime)
    if enemy_num == 1:
        fall = ((level ** 0.5) * (enemy_1.y - map_height / 3) * deltatime)/10 + 1
        width = int((enemy_1.y - map_height / 3) / 5)
        enemy_1 = Enemy(enemy_1.x, enemy_1.y, shift, fall, width)
    if enemy_num == 2:
        fall = ((level ** 0.5) * (enemy_2.y - map_height / 3) * deltatime)/10 + 1
        width = int((enemy_2.y - map_height / 3) / 5)
        enemy_2 = Enemy(enemy_2.x, enemy_2.y, shift, fall, width)
    if enemy_num == 3:
        fall = ((level ** 0.5) * (enemy_3.y - map_height / 3) * deltatime)/10 + 1
        width = int((enemy_3.y - map_height / 3) / 5)
        enemy_3 = Enemy(enemy_3.x, enemy_3.y, shift, fall, width)
    if enemy_num == 4:
        fall = ((level ** 0.5) * (enemy_4.y - map_height / 3) * deltatime)/10 + 1
        width = int((enemy_4.y - map_height / 3) / 5)
        enemy_4 = Enemy(enemy_4.x, enemy_4.y, shift, fall, width)
    if enemy_num == 5:
        fall = ((level ** 0.5) * (enemy_5.y - map_height / 3) * deltatime)/10 + 1
        width = int((enemy_5.y - map_height / 3) / 5)
        enemy_5 = Enemy(enemy_5.x, enemy_5.y, shift, fall, width)
    if enemy_num == 6:
        fall = ((level ** 0.5) * (enemy_6.y - map_height / 3) * deltatime)/10 + 1
        width = int((enemy_6.y - map_height / 3) / 5)
        enemy_6 = Enemy(enemy_6.x, enemy_6.y, shift, fall, width)


def shot_detection(x, y, w):
    acc_x = x - window_width / 2
    acc_y = y - window_height / 2
    if ((acc_x + camera_x) ** 2 + (acc_y + camera_y) ** 2 < w ** 2) or \
            ((acc_x + camera_x + map_width) ** 2 + (acc_y + camera_y) ** 2 < w ** 2) or \
            ((acc_x + camera_x - map_width) ** 2 + (acc_y + camera_y) ** 2 < w ** 2):
        return False, 1
    else:
        return True, 0

grid_points = []
for y in range(3, int((2 * map_height / 3) ** (1 / 3))):
    grid_points.append(y ** 3 + (map_height / 3))

def show_grid():
    for y in grid_points:
        pygame.draw.aaline(Map, Colour.white, (0, map_height / 3), (map_width, int(y)))
        pygame.draw.aaline(Map, Colour.white, (map_width, map_height / 3), (0, int(y)))
    pygame.draw.aaline(Map, Colour.white, (0, map_height / 3), (map_width / 2 + 1000, map_height))
    pygame.draw.aaline(Map, Colour.white, (map_width, map_height / 3), (map_width / 2 - 1000, map_height))
    pygame.draw.aaline(Map, Colour.white, (0, map_height / 3), (1000, map_height))
    pygame.draw.aaline(Map, Colour.white, (map_width, map_height / 3), (map_width - 1000, map_height))

def show_score(score):
    message(Font.fps, "Enemies shot: " + str(score), Colour.white, 3)

def lose_screen(score):
    counter = 0
    exit_x, exit_y = 100, 80
    start_x, start_y = window_width - 200, window_height - 90
    while True:
        click = False
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        window.fill(Colour.black)


        if counter < 2:
            message(Font.fps, "Your final score was " + str(score), Colour.white, 1)
        elif counter < 4:
            message(Font.fps, "Would you like to try again?", Colour.white, 1)
        else:
            counter = 0

        ########################## BUTTONS

        exit_w, exit_h = msg("Exit", exit_x, exit_y, 30, True)
        start_w, start_h = msg("Restart", start_x, start_y, 30, True)
        (mouse_x, mouse_y) = pygame.mouse.get_pos()

        pygame.draw.circle(window, Colour.white, (mouse_x, mouse_y), 5, 1)

        if exit_x - exit_w < mouse_x < exit_x + exit_w and \
                exit_y - exit_h < mouse_y < exit_y + exit_h:
            pygame.draw.circle(window, Colour.red, (mouse_x, mouse_y), 6)

            if click:
                pygame.quit()
                sys.exit()

        if start_x - start_w < mouse_x < start_x + start_w and \
                start_y - start_h < mouse_y < start_y + start_h:
            pygame.draw.circle(window, Colour.red, (mouse_x, mouse_y), 6)

            if click:
                return

        clock.tick()
        pygame.display.flip()
        count_fps()

        counter += deltatime

def game_play():
    hud = Gun.gun_0
    gore = True
    stain_list = []

    global camera_x, camera_y
    sensitivity = 75
    level = 1
    running = True
    scope = False
    alive_1 = False
    alive_2 = False
    alive_3 = False
    alive_4 = False
    alive_5 = False
    alive_6 = False

    dead = False

    mid_x = window_width / 2
    mid_y = window_height / 2
    pygame.mouse.set_visible(False)

    enemy_counter = 0

    while running:
        shoot = False
        #################################### EVENTS
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_menu()
                    pygame.mouse.set_pos([mid_x, mid_y])
                if event.key == pygame.K_SLASH:
                    shoot = True
                if event.key == pygame.K_RSHIFT:
                    scope = True
                    sensitivity /= 2
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RSHIFT:
                    scope = False
                    sensitivity *= 2
            if event.type == pygame.MOUSEMOTION:
                (x_move, y_move) = pygame.mouse.get_rel()
                camera_x -= x_move * deltatime * sensitivity
                camera_y -= y_move * deltatime * sensitivity
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    shoot = True
                if event.button == 3:
                    scope = True
                    sensitivity /= 2
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:
                    scope = False
                    sensitivity *= 2

        ############################################ CAMERA UPDATE

        if camera_y > 0:
            camera_y = 0
        if camera_y < window_height - map_height:
            camera_y = window_height - map_height
        if camera_x > 0:
            if camera_x > window_width:
                camera_x = window_width - map_width
            window.blit(Map, (camera_x - map_width, camera_y))
        if camera_x < window_width - map_width:
            if camera_x < - map_width:
                camera_x = 0
            window.blit(Map, (camera_x + map_width, camera_y))
        window.blit(Map, (camera_x, camera_y))

        ############################################## DRAW MAP

        pygame.draw.rect(Map, Colour.gray, (0, 0, map_width, int(map_height / 3)))
        pygame.draw.rect(Map, Colour.grass, (0, int(map_height / 3), map_width, map_height))
        show_grid()

        #################################### GORE

        if gore:
            if len(stain_list) > 0:
                for stain in stain_list:
                    list(stain)
                    draw_enemy(stain[0], stain[1], stain[2])

        ############################################### ENEMIES
        if enemy_counter <= 5:
            level = 1
        elif enemy_counter <= 15:
            level = 2
        elif enemy_counter <= 25:
            level = 3
        elif enemy_counter <= 40:
            level = 4
        elif enemy_counter <= 75:
            level = 5
        elif enemy_counter <= 100:
            level = 6
        elif enemy_counter <= 120:
            level = 7

        if level >= 1:
            if not alive_1:
                spawn_enemy(1)
                alive_1 = True
                skin_1 = random.randint(1, 5)
            if alive_1:
                if enemy_1.y > map_height - enemy_1.width:
                    dead = True
                update_enemy(level, 1)
                draw_enemy(enemy_1.x, enemy_1.y, enemy_1.width, skin_1)
        if level >= 2:
            if not alive_2:
                spawn_enemy(2)
                alive_2 = True
                skin_2 = random.randint(1, 5)
            if alive_2:
                if enemy_2.y > map_height - enemy_2.width:
                    dead = True
                update_enemy(level, 2)
                draw_enemy(enemy_2.x, enemy_2.y, enemy_2.width, skin_2)
        if level >= 3:
            if not alive_3:
                spawn_enemy(3)
                alive_3 = True
                skin_3 = random.randint(1, 5)
            if alive_3:
                if enemy_3.y > map_height - enemy_3.width:
                    dead = True
                update_enemy(level, 3)
                draw_enemy(enemy_3.x, enemy_3.y, enemy_3.width, skin_3)
        if level >= 4:
            if not alive_4:
                spawn_enemy(4)
                alive_4 = True
                skin_4 = random.randint(1, 5)
            if alive_4:
                if enemy_4.y > map_height - enemy_4.width:
                    dead = True
                update_enemy(level, 4)
                draw_enemy(enemy_4.x, enemy_4.y, enemy_4.width, skin_4)
        if level >= 5:
            if not alive_5:
                spawn_enemy(5)
                alive_5 = True
                skin_5 = random.randint(1, 5)
            if alive_5:
                if enemy_5.y > map_height - enemy_5.width:
                    dead = True
                update_enemy(level, 5)
                draw_enemy(enemy_5.x, enemy_5.y, enemy_5.width, skin_5)
        if level >= 6:
            if not alive_6:
                spawn_enemy(6)
                alive_6 = True
                skin_6 = random.randint(1, 5)
            if alive_6:
                if enemy_6.y > map_height - enemy_6.width:
                    dead = True
                update_enemy(level, 6)
                draw_enemy(enemy_6.x, enemy_6.y, enemy_6.width, skin_6)

        ############################################### SHOT DETECTION

        if shoot:
            if alive_1:
                alive_1, add = shot_detection(enemy_1.x, enemy_1.y, enemy_1.width)
                enemy_counter += add
                if not alive_1:
                    draw_enemy(enemy_1.x, enemy_1.y, enemy_1.width)
                    stain_list.append((enemy_1.x, enemy_1.y, enemy_1.width))
            if alive_2:
                alive_2, add = shot_detection(enemy_2.x, enemy_2.y, enemy_2.width)
                enemy_counter += add
                if not alive_2:
                    draw_enemy(enemy_2.x, enemy_2.y, enemy_2.width)
                    stain_list.append((enemy_2.x, enemy_2.y, enemy_2.width))

            if alive_3:
                alive_3, add = shot_detection(enemy_3.x, enemy_3.y, enemy_3.width)
                enemy_counter += add
                if not alive_3:
                    draw_enemy(enemy_3.x, enemy_3.y, enemy_3.width)
                    stain_list.append((enemy_3.x, enemy_3.y, enemy_3.width))

            if alive_4:
                alive_4, add = shot_detection(enemy_4.x, enemy_4.y, enemy_4.width)
                enemy_counter += add
                if not alive_4:
                    draw_enemy(enemy_4.x, enemy_4.y, enemy_4.width)
                    stain_list.append((enemy_4.x, enemy_4.y, enemy_4.width))
            if alive_5:
                alive_5, add = shot_detection(enemy_5.x, enemy_5.y, enemy_5.width)
                enemy_counter += add
                if not alive_5:
                    draw_enemy(enemy_5.x, enemy_5.y, enemy_5.width)
                    stain_list.append((enemy_5.x, enemy_5.y, enemy_5.width))
            if alive_6:
                alive_6, add = shot_detection(enemy_6.x, enemy_6.y, enemy_6.width)
                enemy_counter += add
                if not alive_6:
                    draw_enemy(enemy_6.x, enemy_6.y, enemy_6.width)
                    stain_list.append((enemy_6.x, enemy_6.y, enemy_6.width))


        #################################################  DRAW TRIGGER

        if not shoot:
            hud = Gun.gun_0

        if shoot:
            if not scope:
                pygame.draw.circle(window, Colour.red, (int(mid_x), int(mid_y)), 8, 2)
        if scope:
            hud = Gun.gun_2
            pygame.draw.circle(window, Colour.white, (int(mid_x), int(mid_y)), 16, 2)
            if shoot:
                camera_y += 100

        window.blit(hud, (0, 0))

        ############################################ DEAD DETECTION

        if dead:
            lose_screen(enemy_counter)
            return

        show_fps()
        show_score(enemy_counter)
        pygame.display.flip()
        clock.tick()
        count_fps()

def msg(msg, x, y, size, button=False):
    font = pygame.font.SysFont(None, size)
    text = font.render(msg, True, Colour.white)
    text_pos = text.get_rect(centerx=x, centery=y)
    (w, h) = text.get_size()
    window.blit(text, text_pos)

    if button:
        pygame.draw.rect(window, Colour.white, (x - w/2 - 10, y - h/2 - 10, w + 20, h+20), 2)
        return int(w / 2) + 10, int(h / 2) + 10

def game_start():
    exit_x, exit_y = 100, 80
    start_x, start_y = window_width - 200, window_height - 90
    controls_x, controls_y = int(window_width/2), int(window_height/2) - 100
    pygame.mouse.set_visible(False)

    while True:

        # Events test

        click = False
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        # Menu Buttons

        window.fill(Colour.black)

        exit_w, exit_h = msg("Exit", exit_x, exit_y, 30, True)
        start_w, start_h = msg("START", start_x, start_y, 30, True)
        msg("Press ESCAPE to go to GAME MENU", controls_x, controls_y - 100, 25, False)
        msg("Left CLICK or press SLASH key to SHOOT", controls_x, controls_y, 25, False)
        msg("Right CLICK or R_SHIFT to SCOPE", controls_x, controls_y + 40, 25, False)
        msg("Move mouse to AIM", controls_x, controls_y + 80, 25, False)
        msg("GOAL: Shoot the incoming circles", controls_x, controls_y + 120, 25, False)

        # Click Check

        (mouse_x, mouse_y) = pygame.mouse.get_pos()

        pygame.draw.circle(window, Colour.white, (mouse_x, mouse_y), 5, 1)

        if exit_x - exit_w < mouse_x < exit_x + exit_w and\
                exit_y - exit_h < mouse_y < exit_y + exit_h:
            pygame.draw.circle(window, Colour.red, (mouse_x, mouse_y), 6)

            if click:
                pygame.quit()
                sys.exit()

        if start_x - start_w < mouse_x < start_x + start_w and\
                start_y - start_h < mouse_y < start_y + start_h:
            pygame.draw.circle(window, Colour.red, (mouse_x, mouse_y), 6)

            if click:
                game_play()

        clock.tick()
        pygame.display.flip()

def game_menu():

    exit_x, exit_y = 100, 80
    restart_x, restart_y = window_width - 200, window_height - 90
    resume_x, resume_y = window_width - 200, window_height - 140
    pygame.mouse.set_visible(False)

    while True:

        # Events test

        click = False
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        # Menu Buttons

        window.fill(Colour.black)

        exit_w, exit_h = msg("Exit", exit_x, exit_y, 30, True)
        restart_w, restart_h = msg("Restart", restart_x, restart_y, 30, True)
        resume_w, resume_h = msg("Resume", resume_x, resume_y, 30, True)

        # Click Check

        (mouse_x, mouse_y) = pygame.mouse.get_pos()

        pygame.draw.circle(window, Colour.white, (mouse_x, mouse_y), 5, 1)

        if exit_x - exit_w < mouse_x < exit_x + exit_w and\
                exit_y - exit_h < mouse_y < exit_y + exit_h:
            pygame.draw.circle(window, Colour.red, (mouse_x, mouse_y), 6)

            if click:
                pygame.quit()
                sys.exit()

        if restart_x - restart_w < mouse_x < restart_x + restart_w and\
                restart_y - restart_h < mouse_y < restart_y + restart_h:
            pygame.draw.circle(window, Colour.red, (mouse_x, mouse_y), 6)

            if click:
                game_start()

        if resume_x - resume_w < mouse_x < resume_x + resume_w and\
                resume_y - resume_h < mouse_y < resume_y + resume_h:
            pygame.draw.circle(window, Colour.red, (mouse_x, mouse_y), 6)

            if click:
                return

        clock.tick()
        pygame.display.flip()

while True:
    game_start()
    window.fill(Colour.black)
