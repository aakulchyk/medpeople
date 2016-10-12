#pip install pymorphy2
#pip install pymorphy2-dicts
#pip install DAWG-Python

from django.db import models
from dictionary.models import MedicalTerm
from threading import Thread

import sys
import pymorphy2

if __name__ == '__main__':
    main()
    
print('start')

def main():
    
    '''
    if len(sys.argv) <=1:
        print("no filed specified")
        return
    '''
    print('start')
    morph = pymorphy2.MorphAnalyzer()        
    filename = 'attachments/example.pdf.text' # sys.argv[1]
    with open(filename, 'r') as f:
        for line in f:
            #print(line)
            for idx, word in enumerate(line.split(' ')):
                # try to find collocations (2+ words):
                # ... at first try to find term that start with current word
                # ...
                '''
                filtr = MedicalTerm.objects.filter(name__iexact=word_norm)
                for curr_term in filtr:
                    words_list = curr_term.split(' ')
                    if words_list.count > 1:
                        
                if MedicalTerm.objects.filter(name__startswith=word.strip()):
                '''
                
                # try to find complete match
                if MedicalTerm.objects.filter(name__iexact=word.strip()):
                    term = MedicalTerm.objects.get(name__iexact=word.strip())
                    print('===Word found! ---> %s %s' % (word, term) )
                    continue
                
                # try to find match with normalized word form
                
                parsed = morph.parse(word.strip())[0]
                word_norm = parsed.normal_form
                #print('norm:' + word_norm)
                if MedicalTerm.objects.filter(name__iexact=word_norm):
                    term = MedicalTerm.objects.get(name=word_norm)
                    print('===Word found! ---> %s (%s) %s' % (word_norm, word, term) )
                    continue
                
                    
        print('finished')



