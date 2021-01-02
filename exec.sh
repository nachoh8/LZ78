#!/bin/bash

# use: ./exec.sh <-lz78 | -gzip | -bzip2> <dir_or_file>

compare_size() {
    local FILE_SIZE_ORIG=$(stat -c%s "$1")
    local FILE_SIZE_ENC=$(stat -c%s "$2")
    echo "Tamaño original: " $FILE_SIZE_ORIG
    echo "Tamaño comprimido: " $FILE_SIZE_ENC
}

compare_content() {
    diff $1 $2
    if [ $? -eq 0 ]
    then
        echo "No hay perdida de datos"
    fi
}

exec_lz78() {
    local NAME=$1
    NAME=${NAME##*/}
    NAME=${NAME%.*}

    echo "Input: ${NAME}"

    local OUT_FILE_ENC="${FOLDER_COM}/${NAME}.bin"
    time python3 lz78.py -e -if $1 -of $OUT_FILE_ENC

    if [ $? -ne 0 ]
    then
        return 1
    fi

    compare_size $1 $OUT_FILE_ENC

    local OUT_FILE_DEC="${FOLDER_DEC}/${NAME}_dec.txt"
    time python3 lz78.py -d -if $OUT_FILE_ENC -of $OUT_FILE_DEC

    if [ $? -ne 0 ]
    then
        return 1
    fi

    compare_content $1 $OUT_FILE_DEC
}

exec_gzip() {
    local NAME=$1
    NAME=${NAME##*/}
    NAME=${NAME%.*}

    echo "Input: ${NAME}"

    local OUT_FILE_ENC="${FOLDER_COM}/${NAME}.gz"
    time gzip -c $1 > $OUT_FILE_ENC

    if [ $? -ne 0 ]
    then
        return 1
    fi

    compare_size $1 $OUT_FILE_ENC

    local OUT_FILE_DEC="${FOLDER_DEC}/${NAME}_dec.txt"
    time gzip -d -c $OUT_FILE_ENC > $OUT_FILE_DEC

    if [ $? -ne 0 ]
    then
        return 1
    fi

    compare_content $1 $OUT_FILE_DEC
}

exec_bzip2() {
    local NAME=$1
    NAME=${NAME##*/}
    NAME=${NAME%.*}

    echo "Input: ${NAME}"

    local OUT_FILE_ENC="${FOLDER_COM}/${NAME}.bz2"
    time bzip2 -c $1 > $OUT_FILE_ENC

    if [ $? -ne 0 ]
    then
        return 1
    fi

    compare_size $1 $OUT_FILE_ENC

    local OUT_FILE_DEC="${FOLDER_DEC}/${NAME}_dec.txt"
    time bzip2 -d -c $OUT_FILE_ENC > $OUT_FILE_DEC

    if [ $? -ne 0 ]
    then
        return 1
    fi

    compare_content $1 $OUT_FILE_DEC
}

if [ $# -ne 2 ]
then
    echo "Numero de Parametros incorrecto: ./exec.sh <-lz78 | -gzip | -bzip2> <dir_or_file>"
    exit 1
fi

if [ "$1" == "-lz78" ]
then
    ALG=exec_lz78
    FOLDER_DEC="decompress_lz78"
    FOLDER_COM="compress_lz78"
elif [ "$1" == "-gzip" ]
then
    ALG=exec_gzip
    FOLDER_DEC="decompress_gzip"
    FOLDER_COM="compress_gzip"
    echo "Aplicar GZIP"
elif [ "$1" == "-bzip2" ]
then
    ALG=exec_bzip2
    FOLDER_DEC="decompress_bzip2"
    FOLDER_COM="compress_bzip2"
    echo "Aplicar BZIP2"
else
    echo "Algoritmo de compresion incorrecto: -lz78 | -gzip | -bzip2"
    exit 1
fi

mkdir -p $FOLDER_DEC
mkdir -p $FOLDER_COM

FILE=$2

if [[ -d $FILE ]] # es un directorio -> ejecutar todos los archivos
then

    for file in  "$FILE"/*
    do
        $ALG $file
        echo "---------------------"
    done
elif [[ -f $FILE ]]
then
    $ALG $FILE
else
    echo "Archivo no valido"
    exit 1
fi

