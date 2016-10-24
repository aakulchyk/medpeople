import re
import sys
import os
    
    
def main():
    if len(sys.argv) <=1:
        print("no filed specified")
        return
        
    
    os.remove('allterms.txt')
    
    for idx, filename in enumerate(sys.argv):
        if idx < 1:
            continue
        print('parsing ' + filename)
        with open(filename, 'r') as f:
            text = f.read()
            terms = re.findall('\*(\w+)\*', text)
            terms += re.findall('<b>(\w+)</b>', text)
            allterms = ','.join(terms)
            print ('write terms of ' + filename)  
            with open('allterms.txt', 'a+') as f1:
                f1.write(allterms)
    print('done!')
    


if __name__ == '__main__':
    main()
