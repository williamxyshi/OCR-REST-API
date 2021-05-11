import cv2
from ocr.receipt_ocr import textAlignmentGetTotal
from cv.preprocess import get_grayscale
from flask import Flask


image = cv2.imread('testassets/receipt.jpg')
gray = get_grayscale(image)

text = textAlignmentGetTotal(gray)


print ('\n ========')

from receiptparser.config import read_config
from receiptparser.parser import process_receipt

config = read_config('english.yml')
receipt = process_receipt(config, "testassets/receipt.jpg", out_dir=None, verbosity=0)

print("Filename:   ", receipt.filename)
print("Company:    ", receipt.company)
print("Postal code:", receipt.postal)
print("Date:       ", receipt.date)
print("Amount:     ", receipt.sum)