from PIL import Image
#import ImageOps
import subprocess, sys, os, glob

H_THRESH = 300
V_THRESH = 300

def get_hlines(pix, w, h):
    """Get start/end pixels of lines containing horizontal runs of at least THRESH black pix"""
    hlines = []
    for y in range(h):
        x1, x2 = (None, None)
        black = 0
        run = 0
        for x in range(w):
            if pix[x,y] == (0,0,0):
                black = black + 1
                if not x1: x1 = x
                x2 = x
            else:
                if black > run:
                    run = black
                black = 0
        if run > H_THRESH:
            hlines.append((x1,y,x2,y))
    return hlines

def isBlack(dot):
    return all([x>0x30 for x in dot])

def findHDottedLines(pix, w, h):
    margin = 70*100/w; # point from where to start searching for line
    w = (w-margin)/4
    hdLines = []
    
    for y in range(h):
        ranges = []
        count = 0
        lineStarted = False
        endLine = 0
        for x in range(margin, w):
            if isBlackish(pix[x,y]):
                if not lineStarted:
                    lineStarted = True
                    count = count+1
                    if ranges:
                        ranges.append(x-endLine)
            else: # if not blackish
                if lineStarted:
                    lineStarted = False
                    endLine = x-1
                    ranges.append(0)
        if count>20 and all([r>3 for r in ranges]):
            hdLines.append(y)


def get_image_data(filename):
    """Extract textual data[rows][cols] from spreadsheet-like image file"""
    im = Image.open(filename)
    pix = im.load()
    width, height = im.size
    hlines = findHDottedLines(pix, width, height)
    print(hlines)
    '''
    sys.stderr.write("%s: hlines: %d\n" % (filename, len(hlines)))
    vlines = get_vlines(pix, width, height)
    sys.stderr.write("%s: vlines: %d\n" % (filename, len(vlines)))
    rows = get_rows(hlines)
    sys.stderr.write("%s: rows: %d\n" % (filename, len(rows)))
    cols = get_cols(vlines)
    sys.stderr.write("%s: cols: %d\n" % (filename, len(cols)))
    cells = get_cells(rows, cols)
    '''

def split_pdf(filename):
    """Split PDF into PNG pages, return filenames"""
    prefix = filename[:-4]
    cmd = "convert -density 600 %s working/%s-%%d.png" % (filename, prefix)
    subprocess.call([cmd], shell=True)
    return [f for f in glob.glob(os.path.join('working', '%s*' % prefix))]

def extract_pdf(filename):
    pngfiles = split_pdf(filename)
    sys.stderr.write("Pages: %d\n" % len(pngfiles))
    return [get_image_data(f) for f in pngfiles]

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: synevotable.py FILENAME")
        exit()
    # split target pdf into pages
    filename = sys.argv[1]
    data = extract_pdf(filename)

    for row in data:
        print("\t".join(row))

