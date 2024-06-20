import sys
import cv2

# 카메라로부터 cv2.VideoCapture 객체 생성

cap = cv2.VideoCapture()
cap.open(0)
if not cap.isOpened():
    print("카메라가 없습니다.")
    sys.exit()

# 동영상 저장을 위한 옵션들
w = round(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)
fourcc = cv2.VideoWriter_fourcc(*'DIVX')

out_frame = cv2.VideoWriter('out_frame.avi',fourcc,fps,(w,h))
out_edge = cv2.VideoWriter('out_edge.avi',fourcc,fps,(w,h))

# 매 프레임 처리 및 화면 출력
while True:
    # 카메라로부터 한 프레임을 정상적으로 받아오면
    # ret에는 True, frame에는 해당 프레임이 저장됨
    ret, frame = cap.read()
    if not ret:
        print("카메라로부터 프레임을 받지 못했습니다.")
        break

    # 프레임 처리
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edge = cv2.Canny(gray, 50, 150)
    edge = cv2.cvtColor(edge, cv2.COLOR_GRAY2BGR)

    # 화면 출력
    cv2.imshow('frame', frame)
    cv2.imshow('edge', edge)

    # 동영상 저장
    out_frame.write(frame)
    out_edge.write(edge)

    cv2.imshow('frame', frame)
    cv2.imshow('edge', edge)

    if cv2.waitKey(1) == 27:
        break

# 사용한 자원 해제
cap.release()
cv2.destroyAllWindows()