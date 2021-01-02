import sys
import os

if len(sys.argv) != 3:
    print("Parametros incorrectos: python3 parseBook.py <in_file> <out_file>")
    exit(1)

pathInput = sys.argv[1]

try:
    inFile = open(pathInput, "r")
except IOError:
    print("Error abriendo " + pathInput)
    exit(1)

content = inFile.read()
prePath = "_aux.txt"
preFile = open(prePath,"w")
# content = content.replace("’","'").replace("ü","u").replace("”","\"").replace("“","\"")
i = 0
while i < len(content):
    char = content[i]
    if char == "’" or char == "‘" or char == "´":
        char = "'"
    elif char == "ü" or char == "ú" or char == "ù" or char == "û":
        char = "u"
    elif char == "Ü" or char == "Ú" or char == "Ù" or char == "Û":
        char = "U"
    elif char == "ë" or char == "é" or char == "è" or char == "ê":
        char = "e"
    elif char == "Ë" or char == "É" or char == "È" or char == "Ê":
        char = "E"
    elif char == "ä" or char == "á" or char == "à" or char == "â" or char == "å" or char == "ā":
        char = "a"
    elif char == "Ä" or char == "Á" or char == "À" or char == "Â" or char == "Å":
        char = "A"
    elif char == "ï" or char == "í" or char == "ì" or char == "î":
        char = "i"
    elif char == "Ï" or char == "Í" or char == "Ì" or char == "Î":
        char = "I"
    elif char == "ö" or char == "ó" or char == "ò" or char == "ô":
        char = "o"
    elif char == "Ö" or char == "Ó" or char == "Ò" or char == "Ô":
        char = "O"
    elif char == "”" or char == "“":
        char = "\""
    elif char == "æ":
        char = "ae"
    elif char == "Æ":
        char = "AE"
    elif char == "ç":
        char = "c"
    elif char == "Ç":
        char = "C"
    elif char == "ñ":
        char = "n"
    elif char == "Ñ":
        char = "N"
    elif char == "ś":
        char = "s"
    elif char == "Ś":
        char = "S"
    elif char == "Œ":
        char = "CE"
    elif char == "½":
        char = "x1/2"
    elif char == "×":
        char = "x"
    elif char == "π":
        char = "pi"
    elif char == "»":
        char = ">"
    elif char == "«":
        char = "<"
    elif char == "°" or char == "§" or char == "¿" or char == "¡" or char == "ª" or char == "º":
        char = ""
    
    preFile.write(char)
    i = i+1




inFile.close()
# 
# 
# prePath = "_aux.txt"
# preFile = open(prePath,"w")
# preFile.write(content)
preFile.close()

os.system("iconv -f utf-8 -t ascii " + prePath + " -o " + sys.argv[2])

os.system("rm " + prePath)

