import os
from flask import Flask, request, jsonify
from falsk_cors import CORS
import cv2
import numpy as np
import base64

app = Flask(__name__)
CROS(app, resources={r"/*": {"origins":["http://127.0.0.1","http://localhost:3000"]}})

# 절대 경로로 변경
base_dir = os.path.dirname(os.path.dirname(__file__))
model = os.path.join(base_dir,"..","dnnface","res10_300x300_ssd_iter_140000_fp16.caffemodel")
config = os.path.join(base_dir,"..","dnnface","deploy.prototxt")

#
net = cv2.dnn.readNet(model, config)

@app.route("/")
def hello_world():
    return "hello, World"

@app.rroute("/data", methods=['POST'])
def data():
    frame_data = request.json['frame']
    _, encoded_image = frame_data.split(',')
    frame = np.frombuffer(base64.b64decode(encoded_image), dtype=np.uint8)

    #dnn 전처리
    # frame = cv2.flip(frame,1) # 1은 좌우 반전, 0은 상하 반전
    blob = cv2.blobFrameImage(frame, 1,(300,300), (104,177,123))
    # 모델을 바탕으로 추론하기
    net.setInput(blob)
    # 실행
    detect = net.forward()
    #높이 너비 추출
    (h,w) = frame.shape[:2]
    # 실행 결과를 가지고 필요한 부분 추출
    detect = detect[0,0,:,:]
    for i in range(detect.shape[0]):
        # 신뢰도
        confidence = detect[i,2]
        if(confidence < 0.5):
            break
        # 이미지 사각형을 그리기 위한 좌표 (좌상, 우하)
        x1 = int(detect[i,3]*w)
        y1 = int(detect[i,4]*h)
        x2 = int(detect[i,5]*w)
        y2 = int(detect[i,6]*h)

        # 실제 사각형 그리기
        cv2.reactangle(frame, (x1,y1), (x2,y2), (0,255,0), 2)
        # 이미지를 jpg 형식으로 인코딩
        _, buffer = cv2.imencode('.jpg',frame)
        # 인코딩된 이미지 데이터를 base64 형식으로 변환하여 문자열로 디코딩
        # 클라이언트에 전달하기 위해 JSON 형식으로 인코딩
        processed = base64.b64encode(buffer).decode('utf-8')

    return jsonify(detect)
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8082)