import cv2
from cvzone.HandTrackingModule import HandDetector
import cvzone
import os

cap = cv2.VideoCapture(2)
cap.set(3,1280)
cap.set(4,720)

detector = HandDetector(detectionCon = 0.65)

class DragImg():
    def __init__(self, path, posOrigin, imgType):

        self.path = path
        self.posOrigin = posOrigin
        self.imgType = imgType

        if self.imgType == 'png':
            self.img = cv2.imread(self.path, cv2.IMREAD_UNCHANGED)
        else:
            self.img = cv2.imread(self.path)

        self.size = self.img.shape[:2]


img1 = cv2.imread("png/ironman.png", cv2.IMREAD_UNCHANGED)
ox, oy = 500, 200

path = "png"
myList = os.listdir(path)
print(myList)

listImg = []
for x, pathImg in enumerate(myList):
    if 'png' in pathImg:
        imgType = 'png'
        print('png')
    else:
        imgType = 'jpg'
        print('jpg')
    listImg.append(DragImg(f'{path}/{pathImg}', [50 + x * 300, 50], imgType))


while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img)

    if hands:
        lmList = hands[0]['lmList']
        # Check if clicked
        length, info, img = detector.findDistance(lmList[8], lmList[12], img)
        print(length)
        if length < 60:
            cursor = lmList[8]
            # Check if in redion
            if ox < cursor[0] < ox + w and oy < cursor[1] < oy + h:
                ox, oy = cursor[0] - w // 2, cursor[1] - h // 2



    try:

        for imgObject in listImg:
            h,w = imgObject.size
            ox, oy = imgObject.posOrigin
            if imgObject.imgType == "png":
                img = cvzone.overlayPNG(img, imgObject.img, [ox, oy])
            else:
                img[oy:oy + h, ox:ox + w] = imgObject.img

    except:
        pass


    cv2.imshow("Image", img)
    cv2.waitKey(1)