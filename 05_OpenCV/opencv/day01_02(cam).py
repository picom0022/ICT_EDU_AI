# open cv 로 이미지(영상) 불러오기 (읽어들이기)

import sys
import cv2

# 상대경로
# img = cv2.imread('./images/cat.bmp')

# 절대경로
img = cv2.imread('C:/Users/ICT05_01/Desktop/python/05_OpenCV/opencv/images/cat.bmp',cv2.IMREAD_GRAYSCALE)
if img is None:
    print("이미지 파일을 읽을 수 없습니다.")
    sys.exit() # 프로그램 종료

print(type(img))
print(img.shape)

# 이미지 화면 출력

cv2.imshow('imgshow1', img)

cv2.waitKey() # 아무키나 누르면 창 닫아짐
# cv2.destroyWindow('imgshow1') # 특정 창 닫기
cv2.destroyAllWindows() # 모든 창 닫기
