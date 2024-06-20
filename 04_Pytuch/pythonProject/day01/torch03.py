## Pytorch에서의 회귀 분석

# 라이브러리 불러오기

import torch
import torch.nn as nn                   # 신경망 클래스 호출
import torch.nn.functional as F         # 신경망 클리새 내의 손실함수, 활성화함수등을 가지고 있는 패키지
import torch.optim as optim             # 최적화 알고리즘을 위한 패키지

## Pytorch를 사용하여 간단한 인공 신경망을 정의한 예제
class Model(nn.Module):
    # 생성자 함수
    def __init__(self):
        # 부모클래스 생성자 호출
        super().__init__()
        # 입력차원이 3이고 출력이 1인 레이어 => 3개를 입력받아 1개를 출력
        self.linear = nn.Linear(3, 1)

    # 신경망의 순전파 단계를 정의한 부분
    # 순전파 단계에서는 입력데이터를 받아서 원하는 출력 계산
    # 입력데이터 x : 차원이 3인 벡터
    # 선형계층은 입력 데이터 x를 받아 가중치와 곱하고, 편향을 더한 후 차원이 1인 출력 벡터 생성
    def forward(self, x):
        y_pred = self.linear(x)
        return y_pred

# 회귀 데이터 분석
# x_data : 모델에 독립변수로 투입
# 모델에 x_data를 input하면 output으로 종속변수(y_data)가 나옴
x_data = torch.FloatTensor([[73,80,75],[93, 88, 78],[89,91,93],[96,98,100],[73,66,70]])
y_data = torch.FloatTensor([[152],[185],[180],[196],[142]])

# 모델
model = Model()

# 최적화 SGD 모델 사용, lr(학습비율 : 1 * 10 ^-5 = 0.00001)
# 모델 파라미터를 업데이트할 때 아주 작은 단위 변경을 하겠다는 뜻
optimizer = optim.SGD(model.parameters(), lr=1e-5)

epoch = 30

for i in range(epoch):
    prediction = model(x_data)
    cost = F.mse_loss(prediction,y_data)

    # 역전파 전에 기울기를 으로 설정 (초기화) : 기울기 누적 방지
    optimizer.zero_grad()
    # 역전파 계산
    cost.backward()
    # 최적화 업데이트
    optimizer.step()

    print('epoch : {0:4d}/{1:}, Cost : {2:.6f}'.format(i,epoch,cost.item()))
