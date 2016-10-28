from threading import Thread
from .models import Attachment
from dictionary.models import MedicalTerm
from enum import Enum

# pip3 install datefinder
import pymorphy2
import datefinder

class FilterType(Enum):
    exact = 1
    startswith = 2

class AnalyzeThread(Thread):
    morph = pymorphy2.MorphAnalyzer()
    tags_added = 0
    extracted_data = {}
    
    def __init__(self, document):
        Thread.__init__(self)
        self.document = document
    
    def run(self):
        if self.document:
            doc = Attachment.objects.get(file_attached = self.document)
            self.analyze_document(doc)
        else:
            attachments = Attachment.objects.all();
            for doc in attachments:
                self.analyze_document(doc)
        
        self.save_all_extracted_data_to_model()
    
    def analyze_document(self, doc):
        self.tags_added = 0
        doc_data = {}
        doc_data['tags'] = []
        
        print('started analysis of document %s' % doc)
        for line in doc.all_content.split('\n'):
            tags = self.search_for_tags(line)
            doc_data['tags'].append(tags)
        
        self.extracted_data[doc] = doc_data
        print('document %s is analyzed. %d new tags added.' % (doc, self.tags_added))
        
    ######## tag searching methods #############    
    def search_for_tags(self, line):
        tags = []
        splitted_line = line.split(' ');
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
                    tags.append(curr_term)
                    break
                                
            # try to find complete match
            if self.filter(stripped_word, FilterType.exact):
                term = self.get(stripped_word, FilterType.exact)
                tags.append(term)
                continue
                    
            # try to find match with normalized word form
            word_norm = self.normalized(stripped_word)
            if self.filter(word_norm, FilterType.exact):
                term = self.get(word_norm, FilterType.exact)
                tags.append(term)
                continue
        return tags
    
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
    
    ####### date searching methods ###############
    def search_for_date(self, line):
        matches = datefinder.find_dates(line)

    ####### save to model ########################
    def save_all_extracted_data_to_model(self):
        for doc, data in self.extracted_data.items():
            for tag in data['tags']:
                if tag: self.save_tag_to_model(doc, tag)
            
    def save_tag_to_model(self, doc, tag):
        if len(doc.tags.filter(name=tag)) == 0:
            print(u'Adding tag: %s' % tag )
            doc.tags.add(tag)
        else:
            print(u'Tag %s exists' % tag )
            
    def save_date_to_model(sel):
        pass
