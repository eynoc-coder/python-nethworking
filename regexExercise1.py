import re


var = input("Donnez une valeur à var : ")

if re.search(r"World", var):
    print("var contient le mot World")
else:
    print("var ne contient pas le mot World")

if re.search(r".", var):
    print("var contient au moins un caractère")
else:
    print("var ne contient pas de caractères")

if re.search(r"^.?$", var):
    print("var contient un ou zero caractère")
else:
    print("var contient plus d'un caractère")

if re.search(r"\d{3}", var):
    print("var contien trois chiffres de suite")
else:
    print("var ne contient pas trois chiffres de suite")

if re.search(r"[a-zA-Z0-9]{3,12}", var):
    print("var contient entre 3 et 12 caractères alphanumériques de suite")
else:
    print("var ne contient pas entre 3 et 12 caractères alphanumériques de suite")

if re.search(r"[TWHQ]ello", var):
    print("var contient un T, un W, un H ou un Q suivi de ello")
else:
    print("var ne contient pas un T, un W, un H ou un Q suivi de ello")

if re.search(r"foo|bar|ello", var):
    print("var contient foo , bar ou ello")
else:
    print("var ne contient pas foo , bar ou ello")

if re.search(r"^(Hello)", var):
    print("var commence par Hello")
else:
    print("var ne commence pas par Hello")

if re.search(r"!!![0-9]{3}$", var):
    print("var se termine par !!! suivi de 3 chiffres")
else:
    print("var ne se termine pas par !!! suivi de 3 chiffres")

if re.search(r"^H.*[0-9]{3}$", var):
    print("var commence par un H et se termine par 3 chiffres")
else:
    print("var ne commence pas par un H ou ne se termine pas par 3 chiffres")
