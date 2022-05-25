import cv2
import pytesseract
import numpy as np
from django.conf import settings

from .utils import INIDAN_STATE_CODES


def resolve_number(image_path):
    cascade_classifier = cv2.CascadeClassifier("haarcascade_number_plate.xml")
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    nplate = cascade_classifier.detectMultiScale(gray, 1.1, 4)
    context = {}
    for (x, y, w, h) in nplate:
        a, b = (int(0.02*img.shape[0]), int(0.025*img.shape[1]))
        plate = img[y+a:y+h-a, x+b:x+w-b, :]
        kernel = np.ones((1, 1), np.uint8)
        plate = cv2.dilate(plate, kernel, iterations=1)
        plate = cv2.erode(plate, kernel, iterations=1)
        plate_gray = cv2.cvtColor(plate, cv2.COLOR_BGR2GRAY)
        (thresh, plate) = cv2.threshold(plate_gray, 127, 255, cv2.THRESH_BINARY)
        read = pytesseract.image_to_string(plate)
        read = ''.join(e for e in read if e.isalnum())
        stat = read[0:2]
        context['plate_number'] = read
        if INIDAN_STATE_CODES.get(stat):
            context['result_text'] = f'Car Belongs to {INIDAN_STATE_CODES[stat]}'
        else:
            context['result_text'] = 'State not recognised!!'
        cv2.rectangle(img, (x, y), (x+w, y+h), (51, 51, 255), 2)
        cv2.rectangle(img, (x, y - 40), (x + w, y), (51, 51, 255), -1)
        cv2.putText(img, read, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.imwrite(f'{settings.MEDIA_ROOT}plate.jpg', plate)
        context['plate_image'] = f'/{settings.MEDIA_ROOT}plate.jpg'
    cv2.imwrite(f'{settings.MEDIA_ROOT}result.jpg', img)
    context['result_image'] = f'/{settings.MEDIA_ROOT}result.jpg'
    return context
