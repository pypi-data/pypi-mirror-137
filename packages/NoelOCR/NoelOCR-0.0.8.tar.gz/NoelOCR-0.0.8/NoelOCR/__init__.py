# Importing Necessary Libraries
import os
from wand.image import Image as m
from random import randint
from PIL import Image as p
import pytesseract
import pytesseract as tess



def processPDF(x):
    try:
        # Convert PDF to TIFF image
        ny = m(filename=x)
        ny_convert = ny.convert('tiff')
        name = randint(1000, 10000)
        new_name = '.' + str(name) + '.tiff'
        #print('File Name Is',new_name)
        username = os.getlogin()
        new_path = '/' + username + '/home/' +new_name
        ny_convert.save(filename=new_path)
        
        # Extract text from TIFF file
        image = p.open(new_path)
        config = ("--psm 3")
        txt = ''
        for frame in range(image.n_frames):
            image.seek(frame)
            txt += pytesseract.image_to_string(image, config = config, lang='eng') + '\n'
        image.close()
        os.remove(new_path)
        return txt.lower()
    except Exception as e:
        print('Something Is Wrong')
