# 비틀어진 사작형을  올바른 사각형으로 변경

import numpy as np
import sys
import cv2

src = cv2.imread('./images/namecard1.jpg')

if src is None:
    print("파일이나 디렉토리가 존재하지 않음")
    sys.exit()

# 일반적인 명함크기 지정
w,h = 720, 400

# 외곽선 추출로 명함의 위치를 가지고 행렬을 만듦
srcQuad = np.array([[325,307],[760,369],[718,611],[231,515]],np.float32)
# 결과 이미지에서 명함이 배치될때 네개의 모서리 좌표
dstQuad = np.array([[0, 0],[w-1, 0],[w-1, h-1],[0,h-1]],np.float32)

# cv2.getPerspectiveTransform() 함수는 이미지 네 개의 좌표(srcQuad)와
# 결과 이미지의 네 개의 좌표(dstQuad)를 입력 받아 원근 변환 행렬을 알아서 계산한다.
# 이 변환 행렬은 원본 이미지의 특정 영역을 새로운 이미지의 원하는 영역으로 변환하는데 사용
pers =  cv2.getPerspectiveTransform(srcQuad, dstQuad)

# cv2.warpPerspective() 함수는 원근 변환 행렬(pers)을 사용하여
# 원본이미지(src)의 특정영역을 변환하고, 결과 이미지(dst)를 생성한다.
dst = cv2.warpPerspective(src, pers, (w,h))

cv2.imshow('src', src)
cv2.imshow('dst', dst)

cv2.waitKey()
cv2.destroyAllWindows()