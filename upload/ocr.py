# search on pythontips.com "OCR on PDF files using Python"
# prequesites:
# sudo apt-get install tesseract-ocr
# pip install git+https://github.com/jflesch/pyocr.git
# pip install wand

import sys

#from wand.image import Image
from PIL import Image as PI
import pyocr
import pyocr.builders
import io	
from time import sleep
import re

from subprocess import run
import os

tmpPath = '/dev/shm/'
imgformat = 'png'

languages = ['rus','eng']

def pdf_ocr(pdf_filename):
    tool = pyocr.get_available_tools()[0]

    for lang in languages:
        if not lang in tool.get_available_languages():
            return lang + ' language is not supported'

    run(['python','upload/pdftoimg.py', pdf_filename])
    
    final_text = []
    fname = pdf_filename.split('/')[-1]
    fname = fname.replace('.','\.')
    pattern = re.compile('%s_\d+\.%s' % (fname, imgformat))
    for root, dirs, files in os.walk(tmpPath):
        for currName in files:
            if pattern.match(currName):
                for lang in languages:
                    txt = tool.image_to_string(
                        PI.open(tmpPath + currName),
                        lang=lang,
                        builder=pyocr.builders.TextBuilder()
                    )
                    final_text.append(txt)
                os.remove(tmpPath + currName)
                
    return final_text



from threading import Thread

from .models import Attachment

from .analyze import AnalyzeThread

class OcrThread(Thread):
    def __init__(self, pdflist):
        Thread.__init__(self)
        self.pdflist = pdflist

    def run(self):
        while self.pdflist:
            pdf_file = self.pdflist.pop(0)
            
            recognized_text = pdf_ocr(pdf_file)
            newtext = self.extractAllWordsFromText(recognized_text)
            
            self.saveTextToDB(pdf_file, newtext)
            self.saveWordsToFile(pdf_file+'.text', newtext)
            
            analyzeThread = AnalyzeThread(pdf_file)
            analyzeThread.start()
        print('All files OCR\'ed')
    
    def extractAllWordsFromText(self, recognizedText):
        text = ''.join(recognizedText)
        words = re.findall(u'(\w+)', text)
        newtext = '\n'.join(words)
        return newtext
        
    def saveWordsToFile(self, pdf_file, text):
        f = open(pdf_file, 'w')
        f.write(text)
        f.close()

    def saveTextToDB(self, pdf_file, text):
        obj = Attachment.objects.get(file_attached=pdf_file)
        obj.all_content = text
        obj.save()
        
           
