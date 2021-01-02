import sys
from bitarray import bitarray

encodeNum = lambda num: bin(num).replace("0b","")
getCodeBits = lambda code: 1 if code == 1 else (code-1).bit_length()

def getBitsNum(num, n_bits):
    bNum = encodeNum(num)    
    while len(bNum) < n_bits:
        bNum = '0' + bNum

    return bNum

def encode(inNameFile, outNameFile):
    # print("Encoding " + inNameFile)

    try:
        inFile = open(inNameFile, "r+b")
    except IOError:
        print("Error abriendo " + inNameFile)
        exit(1)

    try:
        outFile = open(outNameFile, "w+b")
    except IOError:
        inFile.close()
        print("Error abriendo " + outNameFile)
        exit(1)

    dict_codes = {}
    code = 1 # numero de trozo
    comb = "" # cadena de bytes del trozo actual
    bits_out = bitarray()
    bits_in = bitarray()
    bits_in.fromfile(inFile)
    
    i = 0
    while i < bits_in.length():
        f = i + 8
        byte = (bits_in[i:f]).to01()
        comb += byte
        i = f

        if comb not in dict_codes:
            dict_codes[comb] = code
    
            num = int(dict_codes[comb[0:-8]]) if len(comb) > 8 else 0 # si es un trozo de un solo byte concatenar con la cadena vacia(el trozo 0)
            
            n_bits = getCodeBits(code) # numero de bits necesarios en base al actual trozo para codificar el identificador del trozo ya existente
            bNum = getBitsNum(num, n_bits) # codifica el numero del trozo existente con el numero de bits necesarios
            
            # escribir bits
            bits_out.extend(bNum)
            bits_out.extend(byte)
            
            code += 1
            comb = ""
    
    if comb: # queda algo
        n_bits = getCodeBits(code)
        bNum = getBitsNum(int(dict_codes[comb]), n_bits)
        bits_out.extend(bNum)

    bits_out.tofile(outFile)

    inFile.close()
    outFile.close()

def decode(inNameFile, outNameFile):
    # print("Decoding " + inNameFile)

    try:
        inFile = open(inNameFile, "r+b")
    except IOError:
        print("Error abriendo " + inNameFile)
        exit(1)

    try:
        outFile = open(outNameFile, "w+b")
    except IOError:
        inFile.close()
        print("Error abriendo " + outNameFile)
        exit(1)

    dict_codes = {0: ""}
    code = 1
    comb = ""
    bits_out = bitarray()
    bits = bitarray()
    bits.fromfile(inFile)
    
    i = 0
    while i < bits.length():
        n_bits = getCodeBits(code)
        f = i+n_bits
        if f > bits.length():
            break

        b = (bits[i:f]).to01() # numreo del trozo existente
        nCode = int(b, 2)

        if f+8 > bits.length():
            break
        i = f+8
        
        dict_codes[code] = dict_codes[nCode] + (bits[f:i]).to01()

        bits_out.extend(dict_codes[code])
        
        code += 1
    
    
    if i < bits.length(): # si falta un ultimo trozo
        n_bits = getCodeBits(code)
        b = (bits[i:(i+n_bits)]).to01()
        nCode = int(b,2)
        bits_out.extend(dict_codes[nCode])
    
    bits_out.tofile(outFile)

    inFile.close()
    outFile.close()
    

def main():

    # SETUP

    if len(sys.argv) != 6:
        print("Numero de parametros incorrectos: python3 lz78.py {-e | -d} -if <input> -of <output>")
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
    
    if toEncode:
        encode(inNameFile, outNameFile)
    else:
        decode(inNameFile, outNameFile)
    
    # print("Output: " + outNameFile)
    # print("Finish")


main()
