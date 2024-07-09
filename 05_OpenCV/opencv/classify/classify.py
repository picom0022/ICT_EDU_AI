# classify
# caffemodel에서 제공하는 학습된 ai 모델 사용, 사진 분류 처리 (사물 분류)
# 분류할 사물의 종류는 classification_classes_ILSVRC2012.txt에 이름 1000개 작성 되어 제공되고 있다.
# 원래는 구글에서 다운 받는다 : 학습모델(.caffemodel), 구성파일(.prototxt), 클래스 파일(.txt)

import numpy as np
import cv2
import sys

filename = 'beagle.jpg'

# 외부에서 파일의 이름을 받았을 때
if len(sys.argv) > 1:
    filename = sys.argv[1]


image = cv2.imread(filename)


if image is None:
    print("Image not found")
    sys.exit()

# 학습 모델 load하기
# cv2.dnn.readNet(모델, 구성요소)
net = cv2.dnn.readNet('bvlc_googlenet.caffemodel', 'deploy.prototxt')
if net.empty():
    print("dnn model not found")
    sys.exit()

# 분류할 사물 이름이 등록된 클래스 이름 파일 읽기
classnNames = None
with open('classification_classes_ILSVRC2012.txt') as f:
    classNames = f.read().strip().split("\n")

# 모델 실행 <= 읽어들인 이미지 파일을 적용

inputBlob = cv2.dnn.blobFromImage(image, 1, (224,224), (104,177,123) )
net.setInput(inputBlob,'data')

# 실행해서 예측 결과 얻기
prob = net.forward()

# 분류 결과 확인 출력
# 평탄화 작업
out = prob.flatten()
# out 배열의 가장 큰 값의 인덱스 얻기
classid = np.argmax(out)
# 해당 클래스의 확률값
confidence = out[classid]

txt = '%s (%4.2f%%)' %(classNames[classid],confidence * 100 )

# 위치 : (10,30)
cv2.putText(image, txt, (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255),1,cv2.LINE_AA)

cv2.imshow("image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
