# pip install pytesseract
# https://github.com/tesseract-ocr/tesseract/wiki/Downloads

import pytesseract
from PIL import Image
import pandas as pd
import sys

# add path to the tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\jlluj\AppData\Local\Tesseract-OCR\tesseract.exe'
if __name__== "__main__":

    # Run the file by typing tesseract_interface.py "filename.png" inside the directory
    img=Image.open(sys.argv[1])

    text = pytesseract.image_to_string(img)
    print(text)
    saveFile = open('ingestion\ImageToText.txt', 'w')
    saveFile.write(text)
    saveFile.close()

    data = pd.read_csv("ImageToText.txt",delimiter=',')
    data.to_csv(r'C:\Users\jlluj\Documents\PICK\pick-tool-team11-binarybeasts\src\ingestion\imageCSV.csv')


class TesseractInterface:

    def __int__(self):
        pass

    # Get files that need to be transcribed.
    def get_files(self, source):
        pass

    # Send the file at the source for transcription
    def transcribe(self, source):
        pass

    # Get files that have been transcribed
    def get_transcribed_files(self, source):
        pass
