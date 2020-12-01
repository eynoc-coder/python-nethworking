import smtplib
from email.mime.text import MIMEText

#Remplissage des champs par l'utilisateur

mailfrom = input("Mail De : ")
rcptTo = input("Rcpt De : ")

subject = input("Subject : ")
print("Data : ")
text = ""
temp = input()
while temp != ".":
    text += temp + "\n"
    temp = input()



#Creation d'un objet courriel avec MIMEText
msg = MIMEText(text)
msg["From"] = mailfrom
msg["To"] = rcptTo
msg["Subject"] = subject

#Envoi du courriel grace au protocole smtp et au serveur de l'université Laval
try:
    smtpConnection = smtplib.SMTP(host="smtp.ulaval.ca", timeout=10)
    smtpConnection.sendmail(mailfrom, rcptTo, msg.as_string())
    smtpConnection.quit()
except:
    print("L'envoi n'a pas pu être effectué .")
