import socket
import time


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    sock.connect(('OsipovVVNS.asuscomm.com', 10000))
    sock.setblocking(False)

    while True:
        time.sleep(1)

        try:
            data = sock.recv(1024).decode()
            print(data)
        except BlockingIOError:
            ...

        sock.send(input('Введите что хотите отправить\n-> ').encode())


if __name__ == '__main__':
    main()
