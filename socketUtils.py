import socket
import struct


def recvall(soc, count):
    msg = b""
    while (count > 0):
        buffer = soc.recv(count)
        if not buffer:
            return None
        msg += buffer
        count -= len(buffer)
    return msg


def send_msg(soc, message):
    donnee = message.encode(encoding='utf-8')
    soc.sendall(struct.pack(">I", len(donnee)))
    soc.sendall(donnee)


def recv_msg(soc):
    try:
        taille, = struct.unpack(">I", recvall(soc, 4))
    except TypeError:
        return None

    donnee = recvall(soc, taille)
    message = donnee.decode('utf-8')

    return message
