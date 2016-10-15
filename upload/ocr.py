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

    for idx, img in enumerate(req_image): 
        print('OCR page %d' % idx)
        txt = tool.image_to_string(
            PI.open(io.BytesIO(img)),
            lang=lang,
            builder=pyocr.builders.TextBuilder()
        )
        final_text.append(txt)
    
    return final_text



from threading import Thread

from .models import Attachment
import re
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
            text = ''.join(recognized_text)
            words = re.findall(u'(.+)', text)
            newtext = '\n'.join(words)
            f.write(newtext)
            f.close()
            #put text to DB
            obj = Attachment.objects.get(file_attached=pdf_file)
            obj.all_content = newtext
            obj.save()
        print('All files OCR\'d')


import pymorphy2
from dictionary.models import MedicalTerm
from enum import Enum

class FilterType(Enum):
    exact = 1
    startswith = 2

class ReindexThread(Thread):
    morph = pymorphy2.MorphAnalyzer()
    
    def run(self):
        documents = Attachment.objects.all()
        
        for doc in documents:
            print(doc.file_attached)
            for line in doc.all_content.split('\n'):
                splitted_line = line.split(' ')
                for idx, word in enumerate(splitted_line):
                    stripped_word = word.strip()
                    # try to find collocations (2+ words):
                    objlist = self.filter(stripped_word, FilterType.startswith)
                    for curr_term in objlist:
                        words_list = curr_term.name.split(' ')
                        end_idx = idx+len(words_list)
                        if end_idx > len(splitted_line):
                            break;
                        if ' '.join(splitted_line[idx:end_idx]) == curr_term:
                            self.add_tag(doc, curr_term)
                            break
                                
                    # try to find complete match
                    if self.filter(stripped_word, FilterType.exact):
                        term = self.get(stripped_word, FilterType.exact)
                        self.add_tag(doc, term)
                        continue
                    
                    # try to find match with normalized word form
                    word_norm = self.normalized(stripped_word)
                    #print('norm    :' + word_norm)
                    if self.filter(word_norm, FilterType.exact):
                        term = self.get(word_norm, FilterType.exact)
                        self.add_tag(doc, term)
                        continue
        print('finished')
    
    def normalized(self, word):
        parsed = self.morph.parse(word)[0]
        return parsed.normal_form

    def filter(self, string, filter_type):
        if filter_type == FilterType.exact:
            return MedicalTerm.objects.filter(name__iexact=string)
        else:
            return MedicalTerm.objects.filter(name__startswith=string)
    
    def get(self, string, filter_type):
        if filter_type == FilterType.exact:
            return MedicalTerm.objects.get(name__iexact=string)
        else:
            return MedicalTerm.objects.get(name__startswith=string)
    
    def add_tag(self, doc, tag):
        if len(doc.tags.filter(name=tag)) == 0:
            print(u'Adding tag: %s' % tag )
            doc.tags.add(tag)
        else:
            print(u'Tag %s exists' % tag )
        
#if __name__ == '__main__':
#    main()


