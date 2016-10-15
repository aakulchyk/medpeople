#pip install pymorphy2
#pip install pymorphy2-dicts
#pip install DAWG-Python

from django.db import models
from dictionary.models import MedicalTerm
from threading import Thread

import sys
import pymorphy2

from enum import Enum
class Filter(Enum):
    exact = 1
    startswith = 2

if __name__ == '__main__':
    main()
    
print('start')


def normalized(morph, word):
    parsed = morph.parse(word)[0]
    return parsed.normal_form

def filter(string, filter_type):
    if filter_type == Filter.exact:
        return MedicalTerm.objects.filter(name__iexact=string)
    else:
        return MedicalTerm.objects.filter(name__startswith=string)
    
def get(string, filter_type):
    if filter_type == Filter.exact:
        return MedicalTerm.objects.get(name__iexact=string)
    else:
        return MedicalTerm.objects.get(name__startswith=string)


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
            splitted_line = line.split(' ')
            for idx, word in enumerate(splitted_line):
                stripped_word = word.strip()
                # try to find collocations (2+ words):
                # ... at first try to find term that start with current word
                # ...
                
                for curr_term in filter(stripped_word, Filter.startswith):
                    words_list = curr_term.name.split(' ')
                    end_idx = idx+words_list.length()
                    if end_idx > splitted_line.length():
                        break;
                    if ' '.join(splitted_line[idx:end_idx]) == curr_term:
                        print('===Collocation found! ---> %s' % curr_term )
                        break
                            
                # try to find complete match
                if filter(stripped_word, Filter.exact):
                    term = get(stripped_word, Filter.exact)
                    print('===Word found! ---> %s' % term )
                    continue
                
                # try to find match with normalized word form
                word_norm = normalized(morph, stripped_word)
                #print('norm    :' + word_norm)
                if filter(word_norm, Filter.exact):
                    term = get(word_norm, Filter.exact)
                    print('===Word found! ---> %s (%s) %s' % (word_norm, word, term) )
                    continue
                
                    
        print('finished')



