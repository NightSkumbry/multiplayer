import socket
import time
from json import dumps as json_dumps
from json import loads as json_loads
import mysql.connector

from additional import SendingData, StagesList, decode_json, InfoList


class Player:
    def __init__(self, addr: tuple[str, int], sk: socket.socket):
        print(addr, type(addr))
        print(sk, type(sk))
        self.addr: tuple[str, int] = addr
        self.registered: bool = False
        self.socket: socket.socket = sk
        self.sending_data: SendingData = SendingData(text_to_cmd=[], set_stage=None, informing=[])

    def add_sending_data(self, text_to_cmd: str = None, set_stage: StagesList = None, informing: InfoList = None):
        if text_to_cmd is not None:
            self.sending_data['text_to_cmd'].append(text_to_cmd)
        if set_stage is not None:
            self.sending_data['set_stage'] = set_stage
        if informing is not None:
            self.sending_data['informing'].append(informing)

    def send_data(self):
        data = json_dumps(self.sending_data, ensure_ascii=False)
        print(data)
        self.socket.send(data.encode())
        self.sending_data = SendingData(text_to_cmd=[], set_stage=None, informing=[])


unregistered_players: list[Player] = []
players: dict[str, Player] = {}


def is_nickname_available(name: str) -> bool:
    cursor.execute(f"SELECT * FROM user WHERE nickname = '{name}'")
    res = cursor.fetchall()
    return bool(len(res))


def main():
    global unregistered_players, players

    main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    main_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    main_socket.bind(('192.168.1.59', 10000))
    main_socket.setblocking(False)
    main_socket.listen(5)

    while True:
        time.sleep(1/60)

        try:
            new_s, addr = main_socket.accept()
            new_s.setblocking(False)
            player = Player(addr, new_s)
            unregistered_players.append(player)

            player.add_sending_data(
                text_to_cmd='Вам необходимо пройти регистрацию.',
                set_stage=StagesList.loggining
            )
            player.send_data()

        except BlockingIOError:
            ...

        buf = []
        for i, p in enumerate(unregistered_players):
            try:
                rec = p.socket.recv(10240).decode()
                data = SendingData(json_loads(rec, object_hook=decode_json))
                print(data)
                for t in data['text_to_cmd']: print(t)
                for inf in data['informing']:
                    param = json_loads('|'.join(inf.split('|')[1:]))
                    inf = inf.split('|')[0]

                    if inf == InfoList.app_closed:
                        p.socket.close()
                        buf.append(i)
                        # print(buf)

                    elif inf == InfoList.register_data:
                        if is_nickname_available(param['user_name']):
                            buf.append(i)
                            


                if i in buf:
                    continue

            except BlockingIOError:
                ...

        unregistered_players = list(filter(lambda x: unregistered_players.index(x) not in buf, unregistered_players))
        # print(len(unregistered_players))


if __name__ == '__main__':
    db = 'sea_battle'
    connection = mysql.connector.connect(host='127.0.0.1', database=db, user='server', password='Pdtplf445')
    cursor = connection.cursor()

    main()
