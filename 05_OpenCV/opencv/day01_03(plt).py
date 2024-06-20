import matplotlib.pyplot as plt
import cv2

# 컬러 영상
imgBGR = cv2.imread('./images/cat.bmp')
imgRGB = cv2.cvtColor(imgBGR, cv2.COLOR_BGR2RGB)
plt.axis('off')
plt.imshow(imgRGB)
plt.show()

# 그레이 스케일
imgGray = cv2.cvtColor(imgBGR, cv2.COLOR_BGR2GRAY)
plt.axis('off')
plt.imshow(imgGray, cmap='gray')
plt.show()


plt.subplot(121)
plt.axis('off')
plt.imshow(imgRGB)
plt.subplot(122)
plt.axis('off')
plt.imshow(imgGray, cmap='gray')

plt.show()