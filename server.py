import socket
import time
from additional.additional import Prefixes


class Player:
    def __init__(self, addr, sk):
        print(addr, type(addr))
        print(sk, type(sk))
        self.addr = addr
        self.registered = False
        self.socket = sk


unregistered_player_sockets: list[Player] = []
player_sockets: dict[str, Player] = {}


def main():
    main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    main_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    main_socket.bind(('localhost', 10000))
    main_socket.setblocking(False)
    main_socket.listen(5)

    while True:
        time.sleep(1)

        try:
            new_s, addr = main_socket.accept()
            new_s.setblocking(False)
            player = Player(addr, new_s)
            unregistered_player_sockets.append(player)
            new_s.send(f'{Prefixes.command}file_setup'.encode())
            new_s.send(f'{Prefixes.text}Вам необходимо пройти регистрацию. Введите ваш ник в соответствующие поле таблицы.'.encode())
        except BlockingIOError:
            print(0)
        else:
            print(1)


if __name__ == '__main__':
    main()
