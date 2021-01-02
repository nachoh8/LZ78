import sys
from bitarray import bitarray

encodeChar = lambda c: c.encode('utf-8')
encodeNum = lambda num: bin(num).replace("0b","")
getCodeBits = lambda code: 1 if code == 1 else (code-1).bit_length()

def getBitsNum(num, n_bits):
    bNum = encodeNum(num)    
    while len(bNum) < n_bits:
        bNum = '0' + bNum

    return bNum

def encode(inNameFile, outNameFile):
    print("Encoding " + inNameFile)

    try:
        inFile = open(inNameFile, "r", encoding='utf-8')
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
    code = 1
    comb = ""
    bits = bitarray()

    for char in inFile.read():
        comb += char
        if comb not in dict_codes:
            #print("Code: " + str(code))
            n_bits = getCodeBits(code)
            #print("N_bits: " + str(n_bits))

            dict_codes[comb] = str(code)
    
            num = int(dict_codes[comb[0:-1]]) if len(comb) > 1 else 0
            
            bNum = getBitsNum(num, n_bits)
            bits.extend(bNum)
            bits.frombytes(encodeChar(char))
            
            #print(bNum)
            #print(encodeChar(char))
            
            code += 1
            comb = ""
    
    if comb: # queda algo
        n_bits = getCodeBits(code)
        bNum = getBitsNum(int(dict_codes[comb]), n_bits)
        bits.extend(bNum)

    #print(bits)
    bits.tofile(outFile)

    inFile.close()
    outFile.close()

def decode(inNameFile, outNameFile):
    print("Decoding " + inNameFile)

    try:
        inFile = open(inNameFile, "r+b")
    except IOError:
        print("Error abriendo " + inNameFile)
        exit(1)

    try:
        outFile = open(outNameFile, "w",encoding='utf-8')
    except IOError:
        inFile.close()
        print("Error abriendo " + outNameFile)
        exit(1)

    dict_codes = {0: ""}
    code = 1
    comb = ""
    bits = bitarray()
    bits.fromfile(inFile)
    
    i = 0
    while i < bits.length():
        n_bits = getCodeBits(code)
        f = i+n_bits
        if f >= bits.length():
            break

        b = (bits[i:f]).to01()
        nCode = int(b, 2)
        
        if f+8 >= bits.length():
            break
        i = f+8
        
        symb = (bits[f:i]).tobytes().decode("utf-8")
        dict_codes[code] = dict_codes[nCode] + symb
        outFile.write(dict_codes[code])
        
        code += 1
    
    # puede faltar un ultimo trozo
    if i < bits.length():
        n_bits = getCodeBits(code)
        b = (bits[i:(i+n_bits)]).to01()
        nCode = int(b,2)
        outFile.write(dict_codes[nCode])
    
    inFile.close()
    outFile.close()

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
    
    if toEncode:
        encode(inNameFile, outNameFile)
    else:
        decode(inNameFile, outNameFile)
    
    print("Output: " + outNameFile)
    print("Finish")


main()
