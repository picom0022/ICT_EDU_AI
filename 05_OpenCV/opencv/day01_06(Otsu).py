# Otsu 방법을 이용한 자동 이진화

import cv2
src = cv2.imread('./images/namecard1.jpg', cv2.IMREAD_GRAYSCALE)
# 임계값 함수 cv2.threshold(src, thresh, maxval, dst=None)
th, src_bin = cv2.threshold(src, 0, 255, cv2.THRESH_OTSU)

cv2.imshow('src', src)
cv2.imshow('dst', src_bin)
cv2.waitKey()
cv2.destroyAllWindows()
