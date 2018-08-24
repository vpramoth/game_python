# coding=utf-8
"""
    Pong python
    """
import threading
import os
import time
import sys
import pandas as pd
from pynput import keyboard

PONG_COORDINATES_X = 0
PONG_COORDINATES_Y = 0
VELOCITY_X = 1
VELOCITY_Y = 1
TIME_INITIAL = time.time()
SLIDER_UPPER = 0
SLIDER_LOWER = 2
FILE = 'data.csv'
DF1 = pd.read_csv(FILE)
DF1.set_index('Username', inplace=True)


def new():
    """
    For new user
    """
    global DF1, user1
    flag_user = False
    while not flag_user:
        flag_user = True
        user1 = input("Enter Username \n")
        for name in DF1.index.values:
            if name == user1:
                print("Username Exists")
                flag_user = False
                continue
    password = input("Enter Password \n")
    DF1.loc[user1] = [password, 0]
    DF1.to_csv(FILE)


def login():
    """
    For Login
    :return:
    """
    u_name = input("Username \n")
    for name in DF1.index.values:
        if name == u_name:
            password = input("Password \n")
            if password == DF1.loc[name, "Password"]:
                DF1.loc[name, "Attempts"] += 1
                DF1.to_csv(FILE)
                return True
            else:
                print("Invalid Password")
                return False

    print("Invalid Username")
    return False


DISPLAY_MATRIX = [['1'] * 21 for _ in range(10)]
for i in range(3):
    DISPLAY_MATRIX[i][20] = '2'
DISPLAY_MATRIX[0][0] = '0'


def clear():
    """
    clearing the screen
    """
    os.system('clear')


def appear_slider():
    """
    To print slider
    """
    global TIME_INITIAL
    for k in range(10):
        for j in range(21):
            if DISPLAY_MATRIX[k][j] == '1':
                print(' ', end=' ')
            elif DISPLAY_MATRIX[k][j] == '2':
                print('*', end=' ')
            elif DISPLAY_MATRIX[k][j] == '0':
                print('*', end=' ')
        print()
    time_now = time.time()
    score = time_now - TIME_INITIAL
    print("SCORE %.2f" % score)


def slider_down():
    """
    To move slider down
    """
    global SLIDER_LOWER
    global SLIDER_UPPER
    if SLIDER_LOWER != 9:
        DISPLAY_MATRIX[SLIDER_LOWER + 1][20] = '2'
        DISPLAY_MATRIX[SLIDER_UPPER][20] = '1'
        SLIDER_UPPER += 1
        SLIDER_LOWER += 1


def slider_up():
    """
    To move slider up
    """
    global SLIDER_UPPER
    global SLIDER_LOWER
    if SLIDER_UPPER != 0:
        DISPLAY_MATRIX[SLIDER_UPPER - 1][20] = '2'
        DISPLAY_MATRIX[SLIDER_LOWER][20] = '1'
        SLIDER_UPPER -= 1
        SLIDER_LOWER -= 1


def pongball_update():
    """
    To update location of pong ball
    """
    global DISPLAY_MATRIX
    global PONG_COORDINATES_X
    global PONG_COORDINATES_Y
    global VELOCITY_X
    global VELOCITY_Y
    global SLIDER_LOWER
    global SLIDER_UPPER
    if PONG_COORDINATES_X == 9:
        VELOCITY_X = -1
    elif PONG_COORDINATES_X == 0:
        VELOCITY_X = 1
    if PONG_COORDINATES_Y == 19:
        if (PONG_COORDINATES_X >= SLIDER_UPPER) and (PONG_COORDINATES_X <= SLIDER_LOWER):
            VELOCITY_Y = -1
        else:
            print("GAME OVER")
            listener.stop()
            sys.exit("0")
    elif PONG_COORDINATES_Y == 0:
        VELOCITY_Y = 1
    DISPLAY_MATRIX[PONG_COORDINATES_X][PONG_COORDINATES_Y] = '1'
    PONG_COORDINATES_X = PONG_COORDINATES_X + VELOCITY_X
    PONG_COORDINATES_Y = PONG_COORDINATES_Y + VELOCITY_Y
    DISPLAY_MATRIX[PONG_COORDINATES_X][PONG_COORDINATES_Y] = '0'

    return True


i = 0


def special_task():
    """
    Updating the pongball location and slider
    """
    global i
    while True:
        i += 1
        appear_slider()
        time.sleep(0.25)
        if i == 1:
            pongball_update()
            i = 0
        clear()


def on_press(key):
    """
    Moving Slider on Key Press
    :param key:

    """
    if key == keyboard.Key.down:
        slider_down()
    if key == keyboard.Key.up:
        slider_up()


if __name__ == "__main__":
    FLAG = False
    USER = input("New User or Existing User(n/e)? \n")
    if USER == 'n':
        new()
    else:
        while not FLAG:
            FLAG = login()

    THREAD = threading.Thread(target=special_task)
    THREAD.daemon = True
    THREAD.start()

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
