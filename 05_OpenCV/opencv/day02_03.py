import sys
import numpy as np
import cv2
import pytesseract

# 좌표가 들어오면
def reorderPts(pts):
    # 컬럼 0  => 컬럼 1 순으로 정렬한 인덱스가 반환
    idx = np.lexsort((pts[:, 1],pts[:, 0]))
    pts = pts[idx]  # x 좌표 정렬

    # pts[0,1] ㅣ 첫번째 좌표,   pts[1,1] / 두번째 좌표
    # 만약 첫번째 y좌표가 두번째 y좌표보다 크면 , 두 점의 위치 교환
    if pts[0, 1] > pts[1,1]:
        pts[[0,1]] = pts[[1,0]]

    # 만약 세번째 y좌표가 네번째 y좌표보다 작으면  , 두 점의 위치 교환
    if pts[2, 1] < pts[3, 1]:
        pts[[2, 3]] = pts[[3, 2]]

    return pts

# 명함 이미지 사진 블러오기
filename = './images/namecard1.jpg'

# 이 파일을 실행 파일로 만들어서, 외부에서 실행시 전달인다로 이미지 파일을 전달할 경우
if len(sys.argv) > 1:
    filename = sys.argv[1]  # 프롬프트> python 실행파일명 이미지명.확장자

src = cv2.imread(filename)

if src is None:
    print('error')
    sys.exit()

# 출력 영상 (일반 명암크기)
dw, dh = 720, 400
srcQuad = np.array([[0,0],[0,0],[0,0],[0,0]], np.float32)
dstQuad = np.array([[0,0],[0,dh],[dw,dh],[dw,0]], np.float32)

# 입력 영상 전처리
src_gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
th, src_bin = cv2.threshold(src_gray, 0,255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

# 외각선 검출 및 명함 검출
contours, _ = cv2.findContours(src_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

for pts in contours:
    # 면적이 작으면 제외
    if cv2.contourArea(pts) < 1000:
        continue

    # 외각선 근사화  : 이미지에서 물체의 외곽선을 추출할때, 그 외각선을 단순화 하여 저장하는 방법
    approx = cv2.approxPolyDP(pts, cv2.arcLength(pts, True) * 0.02, True)

    # 닫혀진 다각형이 아니면 제외
    if not cv2.isContourConvex(approx) or len(approx) != 4:
        continue

    # 테두리 그리기 (다각형 도형그리기)
    # [approx] : 다각형의 외각선 의 점의 배열
    # cv2.LINE_AA : 선 종류(안티에일리어싱)을 적용한 선
    cv2.polylines(src, [approx], True, (0,255,0), 2, cv2.LINE_AA)
    # 위에서 작성한 함수를 이용해서 좌표값 전달
    srcQuad = reorderPts(approx.reshape(4,2).astype(np.float32))

    # cv2.getPerspectiveTransform() 함수는 이미지 네 개의 좌표(srcQuad)와
    # 결과 이미지의 네 개의 좌표(dstQuad)를 입력 받아 원근 변환 행렬을 알아서 계산한다.
    # 이 변환 행렬은 원본 이미지의 특정 영역을 새로운 이미지의 원하는 영역으로 변환하는데 사용
    per = cv2.getPerspectiveTransform(srcQuad, dstQuad)

    # cv2.warpPerspective() 함수는 원근 변환 행렬(pers)을 사용하여
    # 원본이미지(src)의 특정영역을 변환하고, 결과 이미지(dst)를 생성한다.
    dst = cv2.warpPerspective(src, per, (dw, dh), flags=cv2.INTER_CUBIC)

    # 명함에서 글자 추출
    dst_rgb = cv2.cvtColor(dst, cv2.COLOR_BGR2RGB)
    ex_text = pytesseract.image_to_string(dst_rgb, lang='Hangul+eng')
    print(ex_text)

cv2.imshow('src', src)
cv2.imshow('src_gray', src_gray)
cv2.imshow('src_bin', src_bin)
cv2.imshow('dst', dst)

cv2.waitKey(0)
cv2.destroyAllWindows()
