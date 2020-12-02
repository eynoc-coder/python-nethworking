
import socket
import select
import re
import os
from socketUtils import recv_msg, send_msg
from hashlib import sha512
import smtplib
from email.mime.text import MIMEText


# On prépare le socket du serveur
socServeur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socServeur.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
socServeur.bind(("localhost", 1234))
socServeur.listen()


# On prépare deux listes :
# la prémière pour les sockets des clients connectés
# la seconde pour les sockets en attente d'une opération
listeClients = []
listeAttente = []


# Cette fonction sera appelée lors de la connexion avec un nouveau client
def acceuil(socserveur):

    (nouveauClient, _) = socServeur.accept()

    # On ajoute le nouveau client à la liste des clients
    listeClients.append(nouveauClient)

    msg = "Menu de connexion\n" \
          "1. Creer un compte\n" \
          "2. Se connecter\n"
    send_msg(nouveauClient, msg)


# Cette fonction sera appelée lors de la reponse de l'utilisateur dans le cas ou la connexion est acceptée
def menuPrincipale(socclient):

    msg = "\n=============================================\n" \
          "Menu principal\n" \
          "1. Consultation de courriels\n" \
          "2. Envoie de courriels\n" \
          "3. Statistiques \n" \
          "4. Quitter\n"

    send_msg(socclient, msg)
    choice = recv_msg(socclient)
    if int(choice) == 1:
        consultationCourriel(socclient)
    if int(choice) == 2:
        envoieDeCourriel(socclient)
    if int(choice) == 3:
        stastistique(socclient)
    if choice == '4':
        quitter(socclient)



# Cette fonction permet de creer un nouveau compte
def creerCompte(socclient):
    send_msg(socclient, "7")
    msg = "============================================\n" \
          "Creer un Compte\n" \
          "Entrer votre nom d'usager : (Preciser @ift.glo2000.ca)"
    send_msg(socclient, msg)
    nom_usager = recv_msg(socclient)
    msg = "Entrer votre mots de passe : "
    send_msg(socclient, msg)
    mots_de_passe = recv_msg(socclient)
    try:
        repertoirecourant = os.getcwd()
        creemotdepasse(socclient, repertoirecourant, mots_de_passe, nom_usager)
    except OSError as e:
        #if not os.path.isdir(nom_usager):
        error = "Une erreur est survenue : Ce nom d'utilisateur est déja utilisée"
        send_msg(socclient, error)
        send_msg(socclient, "2")
        creerCompte(socclient)


def creemotdepasse(socclient, repertoirecourant, mots_de_passe, nom_usager):
    if re.search(r"^\w{8,20}$", mots_de_passe):
        if re.search(r"\d+", mots_de_passe):
            if re.search(r"[A-Z]\w*[A-Z]", mots_de_passe):
                repertoireclient = repertoirecourant + "\\" + nom_usager
                repertoirecourriel = repertoireclient + "\\" + "courriel"
                os.makedirs(repertoireclient)
                os.makedirs(repertoirecourriel)
                os.chdir(repertoireclient)
                file = open("password.txt", "a")
                mots_de_passe = hashpassword(mots_de_passe)
                file.write(mots_de_passe)
                file.close()
                os.chdir(repertoirecourant)
                # On envoie un le menu principale au client
                send_msg(socclient, "5")
                send_msg(socclient, "5")
                menuPrincipale(socclient)
            else:
                msg = "Votre mots de passe doit avoir au moins deux lettres majuscules"
                send_msg(socclient, msg)
                send_msg(socclient, "6")
                creerCompte(socclient)
        else:
            msg = "Votre mots de passe doit avoir au moins un chiffre"
            send_msg(socclient, msg)
            send_msg(socclient, "6")
            creerCompte(socclient)
    else:
        msg = "Votre mots de passe doit avoir au moins 8 caractères et au plus 20 caractères"
        send_msg(socclient, msg)
        send_msg(socclient, "6")
        creerCompte(socclient)


#Cette fonction permet de se connecter a son compte
def connexion(socclient):
    msg=str(8)
    send_msg(socclient, msg)
    msg = "Entrer votre nom d'utilisateur : "
    send_msg(socclient, msg)
    nomUtilisateur = recv_msg(socclient)
    repertoireCourrant = os.getcwd()
    repertoirevalue = repertoireCourrant + "\\" + nomUtilisateur
    try:
        os.chdir(repertoirevalue)
        file = open("password.txt", "r")
        hashed = file.read()
        msg = "Entrer votre mots de passe : "
        send_msg(socclient, msg)
        password = recv_msg(socclient)
        os.chdir(repertoireCourrant)
        if comparePassword(password, hashed):
            send_msg(socclient, "5")
            menuPrincipale(socclient)
        else:
            pass


    except OSError as e:
        if not os.path.isdir(repertoirevalue):
            error = "Une erreur est survenue : " + str(e)
            send_msg(socclient, error)
            connexion(socclient)


# Cette fonction permet d'avoir acces à la consultation des courriels
def consultationCourriel(socclient):
    try:
        nomUtilisateur = recv_msg(socclient)
        repertoirecourrant = os.getcwd()
        repertoireCourriel = repertoirecourrant + "\\" + nomUtilisateur + "\\" + "courriel"
        msg = formateFichier(reqfichierRepertoire(repertoireCourriel))
        send_msg(socclient, msg)
        choice = recv_msg(socclient)
        sujetselectionne = reqfichierRepertoire(repertoireCourriel)[int(choice)-1]
        value = os.path.join(repertoireCourriel, sujetselectionne)
        file = open(value, "r")
        value = file.read()
        file.close()
        send_msg(socclient, value)
        recv_msg(socclient)
        menuPrincipale(socclient)
    except Exception as e:
        print("Aucun courriel pour l'instant : "+str(e))
        listeClients.remove(socclient)
        socclient.close()




# Cette fonction permet d'envoyer un courriel
def envoieDeCourriel(socclient):
    msg = "Quel est l'adresse de destination : "
    send_msg(socclient, msg)
    adresseDestination = recv_msg(socclient)
    msg = "Quel est le sujet : "
    send_msg(socclient, msg)
    sujet = recv_msg(socclient)
    msg = "Quel est votre message : "
    send_msg(socclient, message=msg)
    message = recv_msg(socclient)
    message = message + "\n"
    if re.search(r"(@ift\.glo2000\.ca)$", adresseDestination):
        print("vvalue")
        repertoireCourrant = os.getcwd()
        repertoireCouriel = repertoireCourrant + "\\" + adresseDestination + "\\" + "courriel"
        nomDusager = recv_msg(socclient)
        try:
            os.chdir(repertoireCouriel)
            file = open(sujet, "a")
            file.write(message)
            file.close()
            os.chdir(repertoireCourrant)
            msg = "Courriel envoyé"
            send_msg(socclient, msg)
            menuPrincipale(socclient)
        except Exception as e:
            file = open("ERREUR", "a")
            file.write(message)
            file.close()
            print(str(e))
            msg = "Une erreur c'est produite"
            send_msg(socclient, msg)
            menuPrincipale(socclient)
    else:
        nomDusager = recv_msg(socclient)
        courriel = MIMEText(message)
        courriel["From"] = nomDusager
        courriel["To"] = adresseDestination
        courriel["Subject"] = sujet

        try:
            smtpConnexion = smtplib.SMTP(host="smtp.ulaval.ca", timeout=10)
            smtpConnexion.sendmail(courriel["From"], courriel["To"], courriel.as_string())
            smtpConnexion.quit()
            msg = "Le courriel a bien ete envoye!"
            send_msg(socclient, msg)
            menuPrincipale(socclient)
        except Exception as e:
            print(str(e))
            msg = "Une erreur c'est produite"
            send_msg(socclient, msg)
            menuPrincipale(socclient)


# Cette fonction permet de quitter Le logiciel
def quitter(socclient):
    listeClients.remove(socclient)
    socclient.close()


def stastistique(socclient):
    try:
        nomUtilisateur = recv_msg(socclient)
        repertoirecourrant = os.getcwd()
        repertoireCourriel = repertoirecourrant + "\\" + nomUtilisateur + "\\" + "courriel"
        repertoire = repertoirecourrant + "\\" + nomUtilisateur
        msg = "Nombre de Message : " + str(compteNombreDeFichier(reqfichierRepertoire(repertoireCourriel), nomUtilisateur)) + "\n"
        msg += "Taille totale du fichier : " + str(determineTailleTotale(repertoire=repertoire)) + "\n"
        msg += "===============================================================\n"
        for file in reqfichierRepertoire(repertoireCourriel):
            msg += "Sujet : "
            msg += file + "\n"
            value = os.path.join(repertoireCourriel, file)
            print(value)
            value = open(value, "r")
            damn = value.read()
            damn = damn.split()
            for message in damn:
                msg += message + "\n"
            value.close()
        send_msg(socclient, msg)
        recv_msg(socclient)
        menuPrincipale(socclient)

    except Exception as e:
        send_msg(socclient, str(e))
        recv_msg(socclient)
        menuPrincipale(socclient)


# Cette fonction permet de hasher le mots de passe
def hashpassword(motdepasse):
    return sha512(motdepasse.encode('utf8')).hexdigest()


def comparePassword(motdepasse, hashed):
    return hashpassword(motdepasse) == hashed


def reqfichierRepertoire(repertoire):
    return [file for file in os.listdir(repertoire) if os.path.isfile(os.path.join(repertoire, file))]


def compteNombreDeFichier(listeDeFichier, nom):
    repertoirecourrant = os.getcwd()
    repertoireCourriel = repertoirecourrant + "\\" + nom + "\\" + "courriel"

    valeur = 0

    for file in listeDeFichier:
        value = os.path.join(repertoireCourriel, file)
        value = open(value, "r")
        damn = value.read()
        damn = damn.split()
        valeur += len(damn)
        value.close()

    return valeur


def determineTailleTotale(repertoire):
    return os.path.getsize(repertoire)





def formateFichier(listeFichier):
    value = ""
    i = 1
    for file in listeFichier:
        value += str(i) + ". " + file + "\n"
        i += 1

    return value


while True:

    # On passe a select la liste des clients et le socket du serveur
    # On récupère dans la liste d'attente tous les sockets en attente de lecture
    (listeAttente, _, _) = select.select([socServeur] + listeClients, [], [])

    for soc in listeAttente:

        # si le socket retourné est celui du serveur
        # un nouveau client est entrain de se connecter
        if soc == socServeur:
            acceuil(soc)

        # Dans le cas contraire , un client a envoyé un message
        else:
            msg_recu = recv_msg(soc)
            if int(msg_recu) == 1:
                creerCompte(soc)
            elif int(msg_recu) == 2:
                connexion(soc)
