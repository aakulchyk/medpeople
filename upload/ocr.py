# search on pythontips.com "OCR on PDF files using Python"
# prequesites:
# sudo apt-get install tesseract-ocr
# pip install git+https://github.com/jflesch/pyocr.git
# pip install wand

from PIL import Image as PI
import pyocr
import pyocr.builders
import re

from subprocess import run
import os

from threading import Thread
from .models import Document
from .analyze import AnalyzeThread

tmpPath = '/dev/shm/'
imgformat = 'png'

langs = ['rus', 'eng']


class OCR:

    def __init__(self):
        self.tool = pyocr.get_available_tools()[0]
        # remove not supported languages
        get_langs = self.tool.get_available_languages
        self.langs = [l for l in langs if l in get_langs()]
        assert(len(self.langs) > 0)

    def _convertPdfToImg(self,filename):
        run(['python', 'upload/pdftoimg.py', filename])

    def _extractTextInOneLang(self, fullpath, lang):
        assert(os.path.exists(fullpath))
        return self.tool.image_to_string(
            PI.open(fullpath),
            lang=lang,
            builder=pyocr.builders.TextBuilder()
        )

    def _findDocumentImageFiles(self, pdf_filename):
        foundImages = []
        fname = pdf_filename.split('/')[-1]
        fname = fname.replace('.', '\.')
        pattern = re.compile('%s_\d+\.%s' % (fname, imgformat))
        for root, dirs, files in os.walk(tmpPath):
            foundImages.extend( [f for f in files if pattern.match(f)] )
        return foundImages

    def extractAllTextFromPdf(self, pdf_filename):
        self._convertPdfToImg(pdf_filename)
        final_text = []
        for f in self._findDocumentImageFiles(pdf_filename):
            for l in self.langs:
                txt = self._extractTextInOneLang(tmpPath+f, l)
                final_text.append(txt)
            os.remove(tmpPath+f)
        return '\n'.join(final_text)


#############################################################################
########################      THREAD       ##################################
#############################################################################

class OcrThread(Thread):
    def __init__(self, pdflist):
        Thread.__init__(self)
        self.pdflist = pdflist
        self.ocr = OCR()

    def run(self):
        while self.pdflist:
            pdf_file = self.pdflist.pop(0)

            recognized_text = self.ocr.extractAllTextFromPdf(pdf_file)
            newtext = self._extractAllWordsFromText(recognized_text)

            self._saveTextToDB(pdf_file, newtext)
            self._saveWordsToFile(pdf_file+'.text', newtext)

            analyzeThread = AnalyzeThread(pdf_file)
            analyzeThread.start()
        print('All files OCR\'ed')

    def _extractAllWordsFromText(self, recognizedText):
        text = ''.join(recognizedText)
        words = re.findall(u'(\w+)', text)
        newtext = '\n'.join(words)
        return newtext

    def _saveWordsToFile(self, pdf_file, text):
        f = open(pdf_file, 'w')
        f.write(text)
        f.close()

    def _saveTextToDB(self, pdf_file, text):
        print(pdf_file)
        obj = Document.objects.get(file_attached=pdf_file)
        obj.all_content = text
        obj.save()
