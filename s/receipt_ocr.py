import re
import cv2
import numpy as np
import pytesseract
from pytesseract import Output

def isTotalText(text) :
    return text.casefold() == 'TOTAL'.casefold() or text.casefold() == 'TOTAL:'.casefold() or text.casefold() == 'TOTAL : '.casefold()


def textAlignmentGetTotal(preprocessedImage) :
    d = pytesseract.image_to_data(preprocessedImage, output_type=Output.DICT)
    # print('DATA KEYS: \n', d.keys())

    total_top = -1
    total_height = -1

    total_value = -1
    n_boxes = len(d['text'])
    for i in range(n_boxes):
        # condition to only pick boxes with a confidence > 60%
        if isTotalText(d['text'][i]):
            total_top = d['top'][i]
            total_height = d['height'][i]

    
    for i in range(n_boxes):
        s = d['text'][i]
        
        # if the distance between the top of the two boxes is less than the height of the box
        # itself, then its probably on the same row as it. 
        if abs(d['top'][i] - total_top) < (total_height/2) and s.replace('.','',1).isdigit():
            (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
            total_value = d['text'][i]
            
    return total_value



# def columnAlignmentGetTotal(preprocessedImage):
