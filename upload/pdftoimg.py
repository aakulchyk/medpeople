#/bin/python

import sys
from PyPDF2 import PdfFileReader
from PythonMagick import Image
out_format = '.png'

def main():
    if len(sys.argv)<2:
        print('invalid usage!')
        return
    pdf_filename = sys.argv[1]
    pdf = PdfFileReader(file(pdf_filename, "rb"))
    npage = pdf.getNumPages()
    fname = pdf_filename.split('/')[-1]
    tmppath = '/dev/shm/'
    for p in range(npage):
        im = Image()
        im.density('300')
        im.read(pdf_filename +  '[' + str(p) + ']')
        im.write(tmppath + fname + '_' + str(p) + out_format)


if __name__ == '__main__':
    main()


