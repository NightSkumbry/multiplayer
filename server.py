import socket
import time
from additional.additional import Prefixes


class Player:
    def __init__(self, addr: tuple[str, int], sk: socket.socket):
        print(addr, type(addr))
        print(sk, type(sk))
        self.addr: tuple[str, int] = addr
        self.registered: bool = False
        self.socket: socket.socket = sk


unregistered_player_sockets: list[Player] = []
player_sockets: dict[str, Player] = {}


def main():
    main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    main_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    main_socket.bind(('192.168.1.59', 10000))
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
            ...

        for p in unregistered_player_sockets:
            try:
                data = p.socket.recv(1024).decode()
            except BlockingIOError:
                ...
            else:
                print(data)


if __name__ == '__main__':
    main()
