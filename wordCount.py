#! /usr/bin/env python3

import os, stat, re
from sys import stderr, argv

class BufferReader:
    def __init__(self, fd):
        self.fd = fd
        self.buf = b""
    def get(self):
        if len(self.buf):
            c = self.buf[0:1];
            self.buf = self.buf[1:]
            return c
        else:
            self.buf = os.read(self.fd, 1024*16)
            if len(self.buf) == 0:
                return None
            return self.get()
            
        

dict_for_words = dict()


inFileName=argv[1]
outFileName=argv[2]

def dowork():
    global inFileName
    readFromFile(inFileName)
    #global dict_for_words
    #print(dict_for_words)
    global outFileName
    writeToFile(outFileName)

def writeToFile(outputFile):
    global dict_for_words
    fd = os.open(outputFile, os.O_WRONLY)

    #sorting
    ls = list(dict_for_words.keys())
    ls.sort()

    dict_for_words = {i: dict_for_words[i] for i in ls}
    
    for word in dict_for_words:
        os.write(fd, f"{word} {dict_for_words[word]}\n".encode())
    os.close(fd)

def readFromFile(inputFile):
    fd = os.open(inputFile, os.O_RDONLY)
    br = BufferReader(fd)
    while True:
        line = b""

        while True:
            ch = br.get()

            if not ch:
                break

            if ch.decode() == '\n':
                break
            
            line += ch

        if not line:
            break
        line = line.decode()
        words = re.split(r'[ ;:,.?!]+', line)

        for word in words:
            trueWord = word.lower()
            if trueWord in dict_for_words:
                dict_for_words[trueWord] += 1
            else:
                dict_for_words[trueWord] = 1
    os.close(fd)

dowork()
