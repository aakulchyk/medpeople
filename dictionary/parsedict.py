import re
import sys
import os

new_terms_file = 'data/allterms.txt'
    
def main():
    if len(sys.argv) <=1:
        print("no filed specified")
        return
        
    if os.path.exists(new_terms_file):
        os.remove(new_terms_file)
    
    for idx, filename in enumerate(sys.argv):
        if idx < 1:
            continue
        print('parsing ' + filename)
        with open(filename, 'r') as f:
            text = f.read()
            terms = re.findall('\*(\w\w+)\*', text)
            terms += re.findall('<b>(\w\w+)</b>', text)
            terms = [t.lower() for t in terms]
            allterms = ','.join(terms)
            print ('write terms of ' + filename)  
            with open(new_terms_file, 'a+') as f1:
                f1.write(allterms)
    print('done!')
    


if __name__ == '__main__':
    main()
