import socket
from socketUtils import recv_msg, send_msg

ENTETE_RECEPTION_NOM = "NOM"

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.connect(("localhost", 1234))

print(recv_msg(soc))

message = ENTETE_RECEPTION_NOM + ' ' + input()

send_msg(soc, message)

print(recv_msg(soc))

soc.close()
