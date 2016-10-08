# search on pythontips.com "OCR on PDF files using Python"
# prequesites:
# sudo apt-get install tesseract-ocr
# pip install git+https://github.com/jflesch/pyocr.git
# pip install wand

import sys

from wand.image import Image
from PIL import Image as PI
import pyocr
import pyocr.builders
import io	
def pdf_ocr(pdf_filename):

    # TEMP!
    #return u'PSEUDO-RECOGNIZED TEXT'

    tool = pyocr.get_available_tools()[0]

    if not 'rus' in tool.get_available_languages():
        return 'Russian language is not supported'

    lang = 'rus'
    print('lang: %s' % lang)

    req_image = []
    final_text = []

    print('open file: %s' % pdf_filename)
    try:
        image_pdf = Image(filename=pdf_filename, resolution=300)
    except:
        print('Exception ', sys.exc_info()[0])
        raise
    print('convert pdf')
    image_jpeg = image_pdf.convert('jpeg')

    for idx, img in enumerate(image_jpeg.sequence):
        print('convert page %d' % idx )
        img_page = Image(image=img)
        req_image.append(img_page.make_blob('jpeg'))

    #f = open('recognized.txt', 'w')

    for idx, img in enumerate(req_image): 
        print('OCR page %d' % idx)
        txt = tool.image_to_string(
            PI.open(io.BytesIO(img)),
            lang=lang,
            builder=pyocr.builders.TextBuilder()
        )
        final_text.append(txt)
        #f.write(txt)
    #f.close()

    return final_text

def main():
    if len(sys.argv) >=2:
        pdf_filename = sys.argv[1]
        if pdf_filename[-4:].lower() == '.pdf':
            recognized_text = pdf_ocr(pdf_filename)
            f = open(pdf_filename + '.text', 'w')
            f.write('\n'.join(recognized_text))
            f.close
        else:
            print('Not PDF document!')

    else:
        print('Error: missing PDF filename argument!')


from threading import Thread



class OcrThread(Thread):

    def __init__(self, pdflist):
        Thread.__init__(self)
        self.pdflist = pdflist

    def run(self):
        while self.pdflist:
            pdf_file = self.pdflist.pop(0)
            print(pdf_file)
            recognized_text = pdf_ocr(pdf_file)
            f = open(pdf_file + '.text', 'w')
            f.write('\n'.join(recognized_text))
            f.close
        print('All files OCR\'d')

            
#if __name__ == '__main__':
#    main()


