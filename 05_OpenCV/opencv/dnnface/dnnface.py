# dnnface
# 딥러닝 ai 학습모델 다운받아서, 카메라 영상에서 얼굴 ㄹ인식 처리

import numpy as np
import cv2
import sys

# caffe 모델에서 다운 받은 것 (영상 이미지에서 얼굴 인식)
model = 'res10_300x300_ssd_iter_140000_fp16.caffemodel'
config = 'deploy.prototxt'

# 카메라로 부터 cv2.VideoCapture  객체 생성
cap = cv2.VideoCapture()
cap.open(0)

if not cap.isOpened():
    print("카메라가 없습니다.")
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
    detect = detect[0,0,:,:]
    (h,w) = frame.shape[:2]


    # 인식된 얼굴 영역 표시
    for i in range( detect.shape[0]):
        confidence = detect[i,2]
        if confidence < 0.5:
            break

        x1 = int(detect[i,3] * w)
        y1 = int(detect[i,4] * h)
        x2 = int(detect[i,5] * w)
        y2 = int(detect[i,6] * h)

        cv2.rectangle(frame, (x1,y1), (x2,y2),(0,255,0))
    cv2.imshow("frame",frame)
    if cv2.waitKey(10) == 27:
        break

cap.release()
cv2.destroyAllWindows()