import smtplib
import re
import socket
import argparse
from email.mime.text import MIMEText

#Choisir le port avec l'option -p

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port", action="store", dest="port", type=int, default=1400)
port = parser.parse_args().port

#creation d'un socket

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serverSocket.bind(("localhost", port))

#Demarrer le socket
serverSocket.listen(5)
print("Ecoute au port " + str(serverSocket.getsockname()[1]))

i=0

while True:
    # un client se connecte au serveur
    #s est un nouveau sockett pour interagir avec le client
    (s, address) = serverSocket.accept()

    #affichage du nombre de connection au serveur
    i += 1
    print(str(i) + "e connexion au serveur")

    # reception du courriel et verification qu,il est valide
    emailAddress = s.recv(1024).decode('utf8')
    while not re.search(r"^[^@]+@[^@]+\.[^@]+$", emailAddress):
        msg = "Saisissez une adresse courriel valide : "
        s.send(msg.encode('utf8'))
        emailAddress = s.recv(1024).decode('utf8')

    courriel = MIMEText("Ce courriel a ete envoye par mon serveur de courriel")
    courriel["From"] = "exercice3@glo2000.ca"
    courriel["To"] = emailAddress
    courriel["Subject"] = "Exercice3"


    #envoi du courriel
    try:
        smtpConnexion = smtplib.SMTP(host="smtp.ulaval.ca", timeout=10)
        smtpConnexion.sendmail(courriel["From"], courriel["To"], courriel.as_string())
        smtpConnexion.quit()
        msg = "Le courriel a bien ete envoye!"
        s.send(msg.encode('utf8'))
    except:
        msg = "L'envoie n'a pas pu etre effectue. "
        s.send(msg.encode('utf8'))

    msg = "Au revoir!\n"
    s.send(msg.encode('utf8'))

    s.close()