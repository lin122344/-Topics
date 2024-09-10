import os
import cv2
import numpy as np
import mediapipe as mp
import cvzone
from cvzone.PoseModule import PoseDetector
import math

# 翻頁紀錄器
counterRightShirt = 0
counterLeftShirt = 0
counterRightPants = 0
counterLeftPants = 0

# 設置窗口名稱
windowName = 'My Window'

# 創建窗口
cv2.namedWindow(windowName, cv2.WINDOW_NORMAL)
cv2.setWindowProperty(windowName, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

# 打開攝像頭（默認攝像頭的ID通常是0）
cap = cv2.VideoCapture(0)

# 確保攝像頭成功打開
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

def load_images():
    shirtFolderPath = "C:/Users/Student/Desktop/Topics/clothes_folder"  # 衣服文件夹路径
    listShirts = os.listdir(shirtFolderPath)

    librarysubfolderpath = "C:/Users/Student/Desktop/Topics/pants_folder"  # 褲子文件夹路径
    listPants = os.listdir(librarysubfolderpath)

    # 加载四个按鈕
    button_right_shirt_path = "C:/Users/Student/Desktop/Topics/b2.png"
    button_right_pants_path = "C:/Users/Student/Desktop/Topics/b2.png"
    
    imgButtonRightShirt = cv2.imread(button_right_shirt_path, cv2.IMREAD_UNCHANGED)
    imgButtonLeftShirt = cv2.flip(imgButtonRightShirt, 1)
    imgButtonRightPants = cv2.imread(button_right_pants_path, cv2.IMREAD_UNCHANGED)
    imgButtonLeftPants = cv2.flip(imgButtonRightPants, 1)

    # 确定按鈕成功輸出成功
    if imgButtonRightShirt is None or imgButtonLeftShirt is None or imgButtonRightPants is None or imgButtonLeftPants is None:
        raise FileNotFoundError("Error: Could not load button image.")
    
    # 按鈕大小調整
    target_size = (120, 100)
    imgButtonRightShirt = resize_image(imgButtonRightShirt, target_size)
    imgButtonLeftShirt = resize_image(imgButtonLeftShirt, target_size)
    imgButtonRightPants = resize_image(imgButtonRightPants, target_size)
    imgButtonLeftPants = resize_image(imgButtonLeftPants, target_size)
    # 讀取背景
    background_path = "C:/Users/Student/Desktop/Topics/bg1.jpg"
    background = cv2.imread(background_path)
    if background is None:
        raise FileNotFoundError("Error: Could not load background image.")
    # 調整背景大小
    background = cv2.resize(background, (640, 480))
    
    return shirtFolderPath, listShirts, listPants, imgButtonRightShirt, imgButtonLeftShirt, imgButtonRightPants, imgButtonLeftPants, background

# 調整圖像大小function
def resize_image(image, target_size):
    if image.shape[2] == 3:
        alpha_channel = np.ones((image.shape[0], image.shape[1]), dtype=np.uint8) * 255
        image = np.dstack((image, alpha_channel))
    return cv2.resize(image, target_size, interpolation=cv2.INTER_AREA)

def calculate_angle(point1, point2):
    # 計算衣服角度
    dx = point2[0] - point1[0]
    dy = point2[1] - point1[1]
    angle = math.degrees(math.atan2(dy, dx))
    # 確保角度在 -90 到 90 度之間
    if angle < -90:
        angle += 180
    elif angle > 90:
        angle -= 180

    return angle

def rotate_image(image, angle):
    # 計算圖像中心點
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    
    # 旋轉矩陣
    M = cv2.getRotationMatrix2D(center, -angle, 1.0)
    # 圖像旋轉
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0,0,0,0))
    
    return rotated

def initialize():
    # 設定 MediaPipe 人體定位
    mp_selfie_segmentation = mp.solutions.selfie_segmentation
    selfie_segmentation = mp_selfie_segmentation.SelfieSegmentation(model_selection=1)
    detector = PoseDetector()
    # 打開設像頭
    cap = cv2.VideoCapture(0)
    # 加載圖像
    shirtFolderPath, listShirts, listPants, imgButtonRightShirt, imgButtonLeftShirt, imgButtonRightPants, imgButtonLeftPants, background = load_images()
    # 設置翻頁速度
    selectionSpeed = 20
    return cap, detector, shirtFolderPath, listShirts, listPants, imgButtonRightShirt, imgButtonLeftShirt, imgButtonRightPants, imgButtonLeftPants, selectionSpeed, selfie_segmentation, background

def read_frame(cap):

    success, img = cap.read()
    if not success:
        print("Failed to read frame. Retrying...")
    return img, success

def handle_paging(img, lmList, listShirts, listPants, imageNumberShirt, imageNumberPants, selectionSpeed):
    global counterRightShirt, counterLeftShirt, counterRightPants, counterLeftPants
    max_index_shirts = len(listShirts) - 1
    max_index_pants = len(listPants) - 1

    # 檢翻頁操作
    if (lmList[20] is not None) or (lmList[19] is not None):
        # 螢幕左上，右手上
        if lmList[20] and lmList[20][0] < 150 and 100 < lmList[20][1] < 200:
            counterRightShirt += 1
            cv2.ellipse(img, (80, 150), (60, 60), 0, 0, counterRightShirt * selectionSpeed, (0, 255, 0), 20)
            if counterRightShirt * selectionSpeed > 360:
                counterRightShirt = 0
                imageNumberShirt = (imageNumberShirt + 1) % (max_index_shirts + 1)
        else:
            counterRightShirt = 0
        
        # 衣服翻頁向左
        if lmList[19] and lmList[19][0] > 480 and 100 < lmList[19][1] < 200:
            counterLeftShirt += 1
            cv2.ellipse(img, (560, 150), (60, 60), 0, 0, counterLeftShirt * selectionSpeed, (0, 255, 0), 20)
            if counterLeftShirt * selectionSpeed > 360:
                counterLeftShirt = 0
                imageNumberShirt = (imageNumberShirt - 1) % (max_index_shirts + 1)
        else:
            counterLeftShirt = 0
        
        # 褲子翻頁向右
        if lmList[19] and lmList[19][0] > 480 and 250 < lmList[19][1] < 350:
            counterRightPants += 1
            cv2.ellipse(img, (560, 350), (60, 60), 0, 0, counterRightPants * selectionSpeed, (0, 255, 0), 20)
            if counterRightPants * selectionSpeed > 360:
                counterRightPants = 0
                imageNumberPants = (imageNumberPants + 1) % (max_index_pants + 1)
        else:
            counterRightPants = 0
        
        # 螢幕左下。右手下
        if lmList[20] and lmList[20][0] < 150 and 250 < lmList[20][1] < 350:
            counterLeftPants += 1
            cv2.ellipse(img, (80, 350), (60, 60), 0, 0, counterLeftPants * selectionSpeed, (0, 255, 0), 20)
            if counterLeftPants * selectionSpeed > 360:
                counterLeftPants = 0
                imageNumberPants = (imageNumberPants - 1) % (max_index_pants + 1)
        else:
            counterLeftPants = 0

    return img, imageNumberShirt, imageNumberPants

def process_frame(img, detector, shirtFolderPath, listShirts, listPants, imageNumberShirt, imageNumberPants, imgButtonRightShirt, imgButtonLeftShirt, imgButtonRightPants, imgButtonLeftPants, selectionSpeed, selfie_segmentation, background):
    # 背景分割
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = selfie_segmentation.process(img_rgb)
    condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.1
    img_fg = np.where(condition, img, 0)
    background = cv2.resize(background, (img.shape[1], img.shape[0]))
    img = np.where(img_fg == 0, background, img_fg)

    # 添加按鈕圖像
    img = cvzone.overlayPNG(img, imgButtonRightShirt, (510, 100))
    img = cvzone.overlayPNG(img, imgButtonLeftShirt, (10, 100))
    img = cvzone.overlayPNG(img, imgButtonRightPants, (510, 300))
    img = cvzone.overlayPNG(img, imgButtonLeftPants, (10, 300))
    # 姿勢定位
    img = detector.findPose(img, draw=False)
    lmList, _ = detector.findPosition(img, bboxWithHands=False, draw=False)
    
    if lmList:
        lm11, lm12 = lmList[11], lmList[12]
        angle = calculate_angle(lm11, lm12)
        
        # 處理衣服翻頁與定位點
        imgShirt = cv2.imread(os.path.join(shirtFolderPath, listShirts[imageNumberShirt]), cv2.IMREAD_UNCHANGED)
        if imgShirt is not None:
            if (lm11[0] - lm12[0]) > 200:
                widthOfShirt = int((lm11[0] - lm12[0]) * 1.9)
                longOFshirt = int(widthOfShirt * 1.1)
                imgShirt = cv2.resize(imgShirt, (widthOfShirt, longOFshirt))
                imgShirt = rotate_image(imgShirt, angle)
                try:
                    img = cvzone.overlayPNG(img, imgShirt, (lm12[0] - 90, lm12[1] - 80))
                except Exception as e:
                    print(f"Error overlaying shirt image: {e}")
            elif (lm11[0] - lm12[0]) >= 100:
                widthOfShirt = int((lm11[0] - lm12[0]) * 1.8)
                longOFshirt = int(widthOfShirt * 1.1)
                imgShirt = cv2.resize(imgShirt, (widthOfShirt, longOFshirt))
                imgShirt = rotate_image(imgShirt, angle)
                try:
                    img = cvzone.overlayPNG(img, imgShirt, (lm12[0] - 50, lm12[1] - 30))
                except Exception as e:
                    print(f"Error overlaying shirt image: {e}")
            else:
                cv2.putText(img, "Please be closer", (120, 200), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 2, cv2.LINE_AA)
        else:
            print(f"Error: Could not load shirt image from {os.path.join(shirtFolderPath, listShirts[imageNumberShirt])}.")

    # 處理褲子翻頁與定位點
    if lmList:
        lm124, lm123 = lmList[24], lmList[23]

        pants_folder_path = "C:/Users/Student/Desktop/Topics/pants_folder"  # 褲子文件夹路径
        pants_image_name = listPants[imageNumberPants]
        pants_path = os.path.join(pants_folder_path, pants_image_name)

        imgPants = cv2.imread(pants_path, cv2.IMREAD_UNCHANGED)
        if (imgPants is not None) and ((lm11[0] - lm12[0]) >= 100):
            widthOfPants = int((abs(lm124[0] - lm123[0])) * 2.7)
            longOfPants = int(widthOfPants * 1.5)
            imgPants = cv2.resize(imgPants, (widthOfPants, longOfPants))
            imgPants = rotate_image(imgPants, angle)
            try:
                img = cvzone.overlayPNG(img, imgPants, (lm124[0] - 65, lm124[1]))
            except Exception as e:
                print(f"Error overlaying pants image: {e}")
        else:
            cv2.putText(img, "Please be closer", (120, 200), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 2, cv2.LINE_AA)

        img, imageNumberShirt, imageNumberPants = handle_paging(img, lmList, listShirts, listPants, imageNumberShirt, imageNumberPants, selectionSpeed)
    return img, imageNumberShirt, imageNumberPants

def main():
    cap = None
    try:
         # 初始化設置和資源
        cap, detector, shirtFolderPath, listShirts, listPants, imgButtonRightShirt, imgButtonLeftShirt, imgButtonRightPants, imgButtonLeftPants, selectionSpeed, selfie_segmentation, background = initialize()
        imageNumberShirt = 0
        imageNumberPants = 0

        while True:
            # 讀取圖像
            img, success = read_frame(cap)
            if not success:
                continue

            img, imageNumberShirt, imageNumberPants = process_frame(img, detector, shirtFolderPath, listShirts, listPants, imageNumberShirt, imageNumberPants, imgButtonRightShirt, imgButtonLeftShirt, imgButtonRightPants, imgButtonLeftPants, selectionSpeed, selfie_segmentation, background)
            
            # 顯示圖像
            cv2.imshow(windowName, img)
            key = cv2.waitKey(1)
            if key == ord('q'):
                break

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if cap is not None:
            cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
