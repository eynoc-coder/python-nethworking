import socket
import getpass
from socketUtils import recv_msg, send_msg


soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.connect(("localhost", 1234))

print(recv_msg(soc))

option = input("Option : ")
send_msg(soc, option)

def stackrecursive(soc, nomUsager):
    menu = recv_msg(soc)
    print(menu)
    message = input("Choix : ")
    send_msg(soc, str(message))
    if int(message) == 4:
        print("Au revoir !!!")
    elif int(message) == 1:
        send_msg(soc, nomUsager)
        print(recv_msg(soc))
        choix = input("Choix : ")
        send_msg(soc, str(choix))
        print(recv_msg(soc))
        msg = input()
        msg = str(1)
        send_msg(soc, msg)
        stackrecursive(soc, nomUsager)
        pass
    elif int(message) == 2:
        print(recv_msg(soc))
        adresseDestination = input()
        send_msg(soc, adresseDestination)
        print(recv_msg(soc))
        sujet = input()
        send_msg(soc, sujet)
        print(recv_msg(soc))
        msg = input()
        send_msg(soc, msg)
        send_msg(soc, nomUsager)
        msg = recv_msg(soc)
        print(msg)
        stackrecursive(soc, nomUsager)
    elif int(message) == 3:
        send_msg(soc, nomUsager)
        print(recv_msg(soc))
        input()
        mee = str(0)
        send_msg(soc, mee)
        stackrecursive(soc, nomUsager)


# cette fonction permet la communication avec l'option de creation de compte
def optionCreerUnCompte(soc):

    print(recv_msg(soc))

    nomUsager = input()

    send_msg(soc, nomUsager)

    print(recv_msg(soc))

    password = getpass.getpass('Mots de passe : ')

    try:
        send_msg(soc, password)
        stackrecursive(soc, nomUsager)

    except Exception as e:
        print(str(e))


optionCreerUnCompte(soc)
