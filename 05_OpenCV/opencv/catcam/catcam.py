# 카메라를 통해 들어오는 영상에서 영상을 인식해서, 머리에 고양이 귀 그림을 오버레이

import cv2
import sys
import numpy as np

def overlay(frame, cat,pos):
    if pos[0] < 0 or pos[1] < 0:
        return
    if pos[0] + cat.shape[1] > frame.shape[1] or pos[1] + cat.shape[0] > frame.shape[0]:
        return
    sx = pos[0]
    ex = pos[0] + cat.shape[1]
    sy = pos[1]
    ey = pos[1] + cat.shape[0]
    img1 = frame[sy:ey, sx:ex]  # shape=(h, w, 3)
    img2 = cat[:, :, 0:3]
    # shape=(h, w, 3)
    alpha = 1. - (cat[:, :, 3] / 255.)  # shape=(h, w)
    img1[:, :, 0] = (img1[:, :, 0] * alpha + img2[:, :, 0] * (1. - alpha)).astype(np.uint8)
    img1[:, :, 1] = (img1[:, :, 1] * alpha + img2[:, :, 1] * (1. - alpha)).astype(np.uint8)
    img1[:, :, 2] = (img1[:, :, 2] * alpha + img2[:, :, 2] * (1. - alpha)).astype(np.uint8)

# 텐서플로우에서 제공하는 모델
model = 'opencv_face_detector_uint8.pb'
config = 'opencv_face_detector.pbtxt'


# 카메라로 부터 cv2.VideoCapture  객체 생성
cap = cv2.VideoCapture()
cap.open(0)

if not cap.isOpened():
    print("카메라가 없습니다.")
    sys.exit()
# 고양이 귀 그림 가져오기 ( IMREAD_UNCGANGED : 알파 태널(투명도))
cat = cv2.imread('cat.png', cv2.IMREAD_UNCHANGED)
if cat is None:
    print("이미지 파일을 읽을 수 없습니다.")
    sys.exit()

# opencv 가 제공하는 dnn 사용해서 모델
net = cv2.dnn.readNet(model, config)

# 카메라에 영상 추출
while True:
    ret, frame = cap.read()
    if not ret:
        print("카메라로부터 프레임을 받지 못했습니다.")
        break
    # frame = cv2.flip(frame,1)
    # 추출한 영상을 dnn 모델에 넣어서 얼굴 인식
    blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), (104.0, 177.0, 123.0))

    net.setInput(blob)
    detect = net.forward()

    # 프레임 크기와 인식된 데이터 추출
    # 4차원을 2차원 배열로 변경
    detect = detect[0, 0, :, :]
    (h, w) = frame.shape[:2]
    # 인식된 얼굴 영역 표시
    for i in range(detect.shape[0]):
        confidence = detect[i, 2]
        if confidence < 0.5:
            break

        x1 = int(detect[i, 3] * w)
        y1 = int(detect[i, 4] * h)
        x2 = int(detect[i, 5] * w)
        y2 = int(detect[i, 6] * h)

        # 고양이 귀
        fx = (x2-x1) / cat.shape[1]
        # 프레임 얼굴 크기에 맞춤
        cat2 = cv2.resize(cat,(0,0), fx=fx, fy=fx)
        pos = (x1, y1 - (y2 - y1) // 4)

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0))

        overlay(frame, cat2, pos)


    cv2.imshow("frame", frame)
    if cv2.waitKey(10) == 27:
        break

