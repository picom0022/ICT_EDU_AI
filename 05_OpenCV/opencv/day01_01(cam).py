# opencv 패키지 설치 : pip install opencv-python

import cv2

print("Hello OpenCV", cv2.__version__)

# cap = cv2.VideoCapture(0) 와 동일
cap = cv2.VideoCapture()
cap.open(0)

if not cap.isOpened():
    print("카메라가 없습니다.")

print("width:", round((cap.get(cv2.CAP_PROP_FRAME_WIDTH))))
print("height:", round((cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))

while True:
    # 카메라로부터 한 프레임을 정상적으로 받아오면
    # ret에는 True, frame에는 해당 프레임이 저장됨
    ret, frame = cap.read()
    if not ret:
        print("카메라로부터 프레임을 받지 못했습니다.")
        break
    edge = cv2.Canny(frame, 50, 150)

    # 현재 프레임과 엣지 검출 영상 출력
    # 엣지 이미지 내의 중요한 특징을 추출하고, 물체의 경계를 탐지하는데 매우 유용
    cv2.imshow("frame", frame)
    cv2.imshow("edge", edge)

    # esc 를 누르면 종료
    if cv2.waitKey(10) == 27:
        break

# 사용한 자원 해제
cap.release()
cv2.destroyAllWindows()