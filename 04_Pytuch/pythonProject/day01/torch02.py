import torch
import numpy as np

## numpy 에서 Reshape, Pytorch에서는 view

a = np.arange(24)
print(a)

# 2행 4열
# -1 은 자동으로 배치한다.
a_re = a.reshape(-1,2,4)
print(a_re)
print("-" * 100)

# 3차원 2행 4열
print(a.shape)

b = torch.FloatTensor(a)
print(b)
print("-" * 100)

print(b.view([-1,4]))
print("-" * 100)