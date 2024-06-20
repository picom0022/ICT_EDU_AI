# 명암 이미지 외곽선 추출

import numpy as np
import sys
import cv2
import random

src = cv2.imread('./images/namecard1.jpg')
print(src.shape) # (810, 1080, 3)

if src is None:
    print("이미지 없음")
    sys.exit()

#cv2.imshow('src1',src)
# 이미지 크기 줄이기 (1/4 크기)
src = cv2.resize(src, (0,0), fx=0.5, fy=0.5)
#cv2.imshow('src2',src)

# 그레이 스케일로 변환
src_gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

# 가로 세로 구하기
h, w = src.shape[:2]

# 레이블링과 외각선 저장용  3차원 행열 만들기
dst1 = np.zeros((h,w,3), np.uint8)  # uint(0-255) # zeros : 기본 0으로 채워짐
dst2 = np.zeros((h,w,3), np.uint8)  # uint(0-255) # zeros : 기본 0으로 채워짐

# 이진화 처리 (자동 임계값 처리)
th, src_bin = cv2.threshold(src_gray, 0,255, cv2.THRESH_OTSU)

# 외각선 검출
countours1, _ = cv2.findContours(src_bin,cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
countours2, _ = cv2.findContours(src_bin,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

# 외각선 그리기
'''
for i in range(len(countours1)):
    # 랜덤하게 색지정
    random_color = (random.randint(0,255),random.randint(0,255), random.randint(0,255))
    cv2.drawContours(dst1, countours1, i, random_color, 1) # 마지막 1은 두께

for i in range(len(countours2)):
    # 랜덤하게 색지정
    random_color = (random.randint(0,255),random.randint(0,255), random.randint(0,255))
    cv2.drawContours(dst2, countours2, i, random_color, 1) # 마지막 1은 두께

cv2.imshow('dst1', dst1)
cv2.imshow('dst2', dst2)
'''

# 외각선 그리기
for i in range(len(countours1)):
    # 좌표값을
    pts = countours1[i]

    # 랜덤하게 색지정
    random_color = (random.randint(0,255),random.randint(0,255), random.randint(0,255))
    cv2.drawContours(dst1, countours1, i, random_color, 1) # 마지막 1은 두께

    # 면적이 너무 작은 객체는 제외 시키자
    if cv2.contourArea(pts) < 1000:
        continue

    # 외각선 근사화  : 이미지에서 물체의 외곽선을 추출할때, 그 외각선을 단순화 하여 저장하는 방법
    approx = cv2.approxPolyDP(pts, cv2.arcLength(pts, True)*0.02, True)

    # 닫혀진 다각형이 아니면 제외
    if not cv2.isContourConvex(approx):
        continue

    # 4각형 외각선 그리기, 좌표 추출
    if len(approx) == 4 :
        # 외각선 그리기
        cv2.drawContours(dst2, countours1, i, random_color, 2)

        # 좌표 읽기
        # pts[:,:,0] => 모든 좌표의 x값
        # argmin() => 가장 작은 x값을 가진 인덱스
        p_Left = tuple(pts[pts[:,:,0].argmin()][0])
        p_Right = tuple(pts[pts[:, :, 0].argmax()][0])
        p_Top = tuple(pts[pts[:, :, 1].argmin()][0])
        p_Bottom = tuple(pts[pts[:, :, 1].argmax()][0])
        print('좌표값 : ', p_Left, p_Right, p_Top, p_Bottom)

cv2.imshow('src', src)
cv2.imshow('src_gray', src_gray)
cv2.imshow('src_bin', src_bin)
cv2.imshow('dst1', dst1)
cv2.imshow('dst2', dst2)

cv2.waitKey()
cv2.destroyAllWindows()

