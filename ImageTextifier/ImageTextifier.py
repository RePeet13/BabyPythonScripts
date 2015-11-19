import os, sys, argparse, logging, string
from PIL import Image, ImageDraw, ImageStat, ImageFont

fn = 'files/UbuntuMono-Regular.ttf'

rectw = 8 # This set by checking pixel size of the below mentioned 15pt font
recth = 12
fontSize = 15

def textifyImage(imt, corpus):
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
    for h in range(0, imh, recth):
        for w in range(0, imw, rectw):
            tmpc = ImageStat.Stat(im.crop((w, h, w+rectw, h+recth))).mean
            c = (int(tmpc[0]), int(tmpc[1]), int(tmpc[2]), 255)
            dn.text((w, h), corpus[counter], c, fnt)
            if counter < csize-2:
                counter += 1
            else:
                counter = 0
    # newimg.show()
    newimg.save(imt.rsplit('.',1)[0] + '_textified.png')


### Respond to call from command line ###
if __name__ == "__main__":
    ### Arg Parsing ###
    # To improve, change arguments to one named tuple, and allow 1+ of them
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--image', dest='i', help='Input image (to be manipulated)', nargs=1, required=True)
    parser.add_argument('-t', '--text', dest='t', help='Text corpus to use as source', nargs=1, required=True)
    args = parser.parse_args()

    txt = open(args.t[0], 'r')
    corpus = txt.read()
    corpus = corpus.replace('\n', '').replace(' ', '')
    corpus = corpus.translate(string.maketrans("",""), string.punctuation)
    txt.close()
    textifyImage(args.i[0], corpus)