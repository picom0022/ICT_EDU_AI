import sys
import cv2

filename = './images/namecard1.jpg'

src = cv2.imread(filename)
if src is None:
    print('error')
    sys.exit()

cv2.imshow('src', src)
cv2.waitKey(0)
cv2.destroyAllWindows()