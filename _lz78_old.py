import sys

def encode(inFile, encFile):
    print("Encoding...")
    
    dict_codes = {}
    code = 0
    comb = ""

    for char in inFile.read():
        comb += char
        if comb not in dict_codes:
            dict_codes[comb] = str(code + 1)
            if len(comb) > 1:
                encFile.write(dict_codes[comb[0:-1]] + char)
            else:
                encFile.write('0' + char)
            code += 1
            comb = ""
    
    if comb: # queda algo
        encFile.write(dict_codes[comb])
    
    return True

def decode(inFile, decFile):
    print("Decoding...")

    dict_codes = {'0': ""}
    code = 1
    comb = ""

    for char in inFile.read():
        if char in "0123456789":
            comb += char
        else:
            dict_codes[str(code)] = dict_codes[comb] + char
            decFile.write(dict_codes[comb] + char)
            comb = ""
            code += 1
    
    if comb: # queda algo
        decFile.write(dict_codes[comb])

    return True



def main():

    # SETUP

    if len(sys.argv) != 6:
        print("Numero de parametros incorrectos: python lz78.py {-e | -d} -if <input> -of <output>")
        exit(1)
    
    inNameFile = ""
    outNameFile = ""
    toEncode = True

    for i in range(0, len(sys.argv)):
        if sys.argv[i] == "-d":
            toEncode = False
        elif sys.argv[i] == "-if":
            i += 1
            inNameFile = sys.argv[+i]
        elif sys.argv[i] == "-of":
            i += 1
            outNameFile = sys.argv[+i]

    # INIT

    try:
        inFile = open(inNameFile, "r")
    except IOError:
        print("Error abriendo " + inNameFile)
        exit(1)
    
    try:
        print("File: " + inNameFile)

        outFile = open(outNameFile, "w")
        if toEncode:
            encode(inFile, outFile)
        else:
            decode(inFile, outFile)
        
        print("Output: " + outNameFile)
        print("Finish")
    finally:
        inFile.close()
        outFile.close()


main()