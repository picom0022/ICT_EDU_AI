# 레이블링
# 이미지 입력 => 그레이스케일로 입력 => 이진화(검정, 흰색) : threshold => 레이블링(labeling)

import cv2
import sys
import numpy as np
import random

src = cv2.imread('./images/coins.png', cv2.IMREAD_GRAYSCALE)

if src is None:
    print('이미지 파일을 읽을 수 없습니다.')
    sys.exit()

# (246,300)
# print('shape : ', src.shape)
h,w = src.shape[:2]

# 3차원 행렬 만들기
dst1 = np.zeros((h,w,3), np.uint8)  # 기본 0 으로 채워짐
dst2 = np.zeros((h,w,3), np.uint8)

# 이진화 처리
_, src_bin = cv2.threshold(src,0,255,cv2.THRESH_OTSU)

# 레이블링 : 흰색 영역별 픽셀에 랜덤값으로 색상을 만들어서 추출된 픽셀 위치에 색상 값 기록
cnt, labels, stats, centroids = cv2.connectedComponentsWithStats(src_bin)
# print('cnt : ', cnt)                        # 구성요소의 개수
# print('labels : ', labels)                  # 배경 = 0
# print('labels(shape) : ', labels.shape)     # (246,300)
# print('stats : ', stats)                    #  컴포넌트의 바운딩 박스와 관련된 통계 정보 [ x, y, 너비, 높이, 픽셀수]
# print('centroids : ', centroids)            # 중심 좌표

for i in range(1,cnt):
    # 랜덤하게 색 만들기 (RGB)
    random_color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))

    # 레이블링을 위해 준비된 행렬에 추출된 코인 (흰색 부분에 색칠하기)
    dst1[labels == i] = random_color

# 외곽선 검출
# cv2.findContours(이미지, 외각선 검출 모드, 외각선 검출 메서드)
contours, _ = cv2.findContours(src_bin, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

# 외곽선 지정
for i in range(len(contours)):
    random_color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))

    # cv2.drawContours(대상 이미지, 외곽선 정보를 담은 리스트, i, random_color, 외곽선 두께)
    cv2.drawContours(dst2, contours, i, random_color, 1)

cv2.imshow('src',src)
cv2.imshow('src_bin',src_bin)
cv2.imshow('dst1',dst1)
cv2.imshow('dst2',dst2)

cv2.waitKey()
cv2.destroyAllWindows()