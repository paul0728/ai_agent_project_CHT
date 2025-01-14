# tools/people_counter.py

import cv2
import numpy as np
from typing import List, Tuple, Optional
from config.settings import CAMERA_INDEX, CAMERA_RESOLUTION, IS_RASPBERRY_PI

class PeopleCounter:
    def __init__(self):
        # 載入級聯分類器
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        self.face_alt_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_alt.xml'
        )
        self.face_alt2_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_alt2.xml'
        )
        
        # 初始化為 None，每次執行時再創建
        self.camera = None
        self.picam2 = None

    def init_camera(self):
        """初始化相機"""
        # 先確保先前的相機已釋放
        self.release_camera()
        
        if IS_RASPBERRY_PI:
            try:
                from picamera2 import Picamera2
                self.picam2 = Picamera2()
                self.picam2.configure(
                    self.picam2.create_preview_configuration(
                        main={"size": CAMERA_RESOLUTION}
                    )
                )
                self.picam2.start()
                print("使用 PiCamera")
                return
            except Exception as e:
                print(f"無法初始化 PiCamera: {e}")
                print("切換到普通 USB 攝像頭")

        # 如果不是樹莓派或 PiCamera 初始化失敗，使用普通攝像頭
        self.camera = cv2.VideoCapture(CAMERA_INDEX)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_RESOLUTION[0])
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_RESOLUTION[1])

    def release_camera(self):
        """釋放相機資源"""
        if self.camera is not None:
            self.camera.release()
            self.camera = None
        if self.picam2 is not None:
            self.picam2.close()
            self.picam2 = None
        cv2.destroyAllWindows()

    def get_frame(self) -> Optional[np.ndarray]:
        """獲取一幀圖像"""
        try:
            if self.picam2:
                return self.picam2.capture_array()
            elif self.camera:
                # 捕獲多幀並使用最後一幀
                for _ in range(3):
                    ret, frame = self.camera.read()
                    if not ret:
                        return None
                return frame
            return None
        except Exception as e:
            print(f"獲取圖像失敗: {e}")
            return None

    def detect_faces(self, frame: np.ndarray) -> int:
        """檢測人臉"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        
        # 調整參數使檢測更嚴格
        faces_default = self.face_cascade.detectMultiScale(
            gray, scaleFactor=1.2, minNeighbors=6, minSize=(30, 30)
        )
        
        faces_alt = self.face_alt_cascade.detectMultiScale(
            gray, scaleFactor=1.2, minNeighbors=6, minSize=(30, 30)
        )
        
        faces_alt2 = self.face_alt2_cascade.detectMultiScale(
            gray, scaleFactor=1.2, minNeighbors=6, minSize=(30, 30)
        )
        
        # 選擇檢測到人臉最多的結果
        all_detections = [faces_default, faces_alt, faces_alt2]
        all_faces = max(all_detections, key=len) if any(len(d) > 0 for d in all_detections) else []
        
        # 顯示檢測結果
        display_frame = frame.copy()
        final_faces = self._remove_duplicates(all_faces, overlap_thresh=0.3)  # 降低重疊閾值
        
        for (x, y, w, h) in final_faces:
            cv2.rectangle(display_frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        
        cv2.imshow('Detected Faces', display_frame)
        cv2.waitKey(1)
        
        return len(final_faces)

    def _remove_duplicates(self, faces, overlap_thresh=0.5):
        """移除重複的檢測框"""
        if len(faces) == 0:
            return []
        
        faces = sorted(faces, key=lambda x: x[2] * x[3], reverse=True)
        keep = []
        
        for i in range(len(faces)):
            keep_face = True
            for kept_idx in keep:
                overlap = self._calculate_overlap(faces[i], faces[kept_idx])
                if overlap > overlap_thresh:
                    keep_face = False
                    break
            if keep_face:
                keep.append(i)
        
        return [faces[i] for i in keep]

    def _calculate_overlap(self, box1, box2):
        """計算重疊率"""
        x1, y1, w1, h1 = box1
        x2, y2, w2, h2 = box2
        
        x_left = max(x1, x2)
        y_top = max(y1, y2)
        x_right = min(x1 + w1, x2 + w2)
        y_bottom = min(y1 + h1, y2 + h2)
        
        if x_right < x_left or y_bottom < y_top:
            return 0.0
            
        intersection_area = (x_right - x_left) * (y_bottom - y_top)
        box1_area = w1 * h1
        box2_area = w2 * h2
        
        return intersection_area / float(min(box1_area, box2_area))

    async def execute(self) -> str:
        """執行人數檢測"""
        try:
            print("正在檢測人數，請稍候...")
            
            # 初始化相機
            self.init_camera()
            
            max_faces = 0
            for _ in range(3):
                frame = self.get_frame()
                if frame is not None:
                    num_faces = self.detect_faces(frame)
                    max_faces = max(max_faces, num_faces)
            
            result = "當前畫面中檢測到 {} 人".format(max_faces) if max_faces > 0 else "當前畫面中未檢測到人"
            return result
                
        except Exception as e:
            return f"計算人數時發生錯誤: {str(e)}"
        finally:
            # 確保在每次執行後釋放資源
            self.release_camera()

    def __del__(self):
        """析構函數"""
        self.release_camera()