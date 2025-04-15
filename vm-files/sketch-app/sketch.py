import cv2
import numpy as np

def sketchify(input_path, output_path):
    img = cv2.imread(input_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    sharpen_kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    sharpened = cv2.filter2D(gray, -1, sharpen_kernel)
    inverted = 255 - sharpened
    blur = cv2.GaussianBlur(inverted, (21, 21), 0)
    dodge = cv2.divide(sharpened, 255 - blur, scale=256)
    sketch = cv2.equalizeHist(dodge)
    sketch = cv2.fastNlMeansDenoising(sketch, h=75, templateWindowSize=7, searchWindowSize=21)
    cv2.imwrite(output_path, sketch)