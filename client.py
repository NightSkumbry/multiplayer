import socket
import time
from json import loads as json_loads
from json import dumps as json_dumps
import os
import threading
import sys
import pygame as pg
import pygame.gfxdraw

from additional import SendingData, StagesList, decode_json, Window, Color, InfoList

pg.init()


def game():
    global play
    FPS = 60
    pg.mixer.init()
    win = pg.display.set_mode((Window.width, Window.height))
    pg.display.set_caption('TD')
    clock = pg.time.Clock()

    while play:
        win.fill(Color.BG)
        clock.tick(FPS)

        pos = pg.mouse.get_pos()

        for i in pg.event.get():
            if i.type == pg.QUIT:
                play = False
                return

        pg.display.flip()



def set_stage(arg: StagesList):
    if arg is not None:
        global stage
        stage = arg


def process_info(information: InfoList):
    ...


def main():
    while play:
        time.sleep(1/30)

        try:
            rec = sock.recv(10240).decode()
            data = SendingData(json_loads(rec, object_hook=decode_json))
            print(data)
            for t in data['text_to_cmd']: print(t)
            set_stage(data['set_stage'])
            for i in data['informing']: process_info(i)

        except BlockingIOError:
            ...


def on_exit():
    sock.send(json_dumps(SendingData(text_to_cmd=[], set_stage=None, informing=[InfoList.app_closed]), ensure_ascii=False).encode())
    sock.close()

    pg.quit()
    sys.exit()


def load_opts():
    if os.path.exists('./options.json'):
        pass
    else:
        pass


if __name__ == '__main__':
    options = load_opts()
    stage: StagesList = StagesList.connecting

    play = True
    game = threading.Thread(target=game)
    game.start()

    print(stage)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    sock.connect(('OsipovVVNS.asuscomm.com', 10000))
    sock.setblocking(False)

    main()
    on_exit()
