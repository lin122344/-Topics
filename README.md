# 專題
## 程式
 - 主程式
   - locker_room.py
 - 影像顯示
    windowName = 'My Window'
    cv2.namedWindow(windowName, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(windowName, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()-
 - 衣服褲子按鈕資料夾
      def load_images():
      shirtFolderPath = "C:/Users/Student/Desktop/Topics/clothes_folder"  
      listShirts = os.listdir(shirtFolderPath)
      librarysubfolderpath = "C:/Users/Student/Desktop/Topics/pants_folder" 
      listPants = os.listdir(librarysubfolderpath)
   - 加载四个按钮
      button_right_shirt_path = "C:/Users/Student/Desktop/Topics/b2.png"
      button_right_pants_path = "C:/Users/Student/Desktop/Topics/b2.png"
    - 背景圖片
        background_path = "C:/Users/Student/Desktop/Topics/bg1.jpg"
## 使用套件
  -CV2  
  -Numpy  
  -mediapipe  
  -cvzone  
  -math  
## 使用方式
    1.下載所有檔案儲存在資料夾內(包含clothes_folder、pants_folder、b2.png)
    2.執行locker_room.py程式檔
    3.選取想要的衣服放進圖片褲(要去背的圖片)
    4.手部可以控制衣服的選項
## 紀錄
 - daily_record.md
   - 整理後的每日記錄，寫在老師excel上面，方便報告
    
  
   
   
