import argparse, inspect, logging, os, string, sys, time
from PIL import Image, ImageDraw, ImageStat, ImageFont

# Import subfolder modules
# from http://stackoverflow.com/questions/279237/import-a-module-from-a-relative-path
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"lib")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)

import progressbar


fn = 'files/UbuntuMono-Regular.ttf'

rectw = 8 # This set by checking pixel size of the below mentioned 15pt font
recth = 12
fontSize = 15

def textifyImage(imt, corpus, fname):
    im = Image.open(imt)
    imw, imh = im.size

    # Thought is to average the entire image for a more suitable background color
    # Would probably need to have a threshold so text doesnt get too close to this so it stands out some
    # bckt = ImageStat.Stat(im).mean
    # b = (int(bckt[0]), int(bckt[1]), int(bckt[2]), 255)
    # newimg = Image.new('RGB', (imw, imh), b)

    newimg = Image.new('RGB', (imw, imh), '#ddd')
    fnt = ImageFont.truetype(fn, fontSize)
    dn = ImageDraw.Draw(newimg)
    csize = len(corpus)
    counter = 0

    bar = progressbar.ProgressBar()

    for h in bar(range(0, imh, recth)):
        for w in range(0, imw, rectw):
            tmpc = ImageStat.Stat(im.crop((w, h, w+rectw, h+recth))).mean
            c = (int(tmpc[0]), int(tmpc[1]), int(tmpc[2]), 255)
            dn.text((w, h), corpus[counter], c, fnt)
            if counter < csize-2:
                counter += 1
            else:
                counter = 0
    # newimg.show()
    newimg.save(fname)


### Respond to call from command line ###
if __name__ == "__main__":
    ### Arg Parsing ###
    # To improve, change arguments to one named tuple, and allow 1+ of them
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--image', dest='i', help='Input image (to be manipulated)', nargs=1, required=True)
    parser.add_argument('-t', '--text', dest='t', help='Text corpus to use as source', nargs=1, required=True)
    parser.add_argument('-o', '--output', dest='o', help='Output file name', nargs=1)
    args = parser.parse_args()

    txt = open(args.t[0], 'r')
    corpus = txt.read()
    corpus = corpus.replace('\n', '').replace(' ', '')
    corpus = corpus.translate(string.maketrans("",""), string.punctuation)
    txt.close()
    if args.o:
        textifyImage(args.i[0], corpus, args.o[0])
    else:
        textifyImage(args.i[0], corpus, args.i[0].rsplit('.',1)[0] + '_textified.png')
