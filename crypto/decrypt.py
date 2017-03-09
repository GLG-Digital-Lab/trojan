import glob
import os, random, struct
from Crypto.Cipher import AES

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

key = 'This is a key123'
startPath = 'C:\\Users\\t3d\\Desktop\\test'

for root, dirs, files in os.walk(startPath, topdown=False):
    for name in files:
        myFile = os.path.join(root, name)
        try:
            decrypt_file(key, myFile, myFile)
            print "Decrypting " + myFile
        except IOError:
            print "Permission denied for " + myFile
