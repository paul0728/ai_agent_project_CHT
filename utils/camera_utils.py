import cv2
import numpy as np
from typing import Optional, Tuple, List
from config.settings import CAMERA_INDEX, CAMERA_RESOLUTION, IS_RASPBERRY_PI

class CameraUtils:
    def __init__(self):
        self._initialize_camera()
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )

    def _initialize_camera(self):
        """初始化攝像頭"""
        if IS_RASPBERRY_PI:
            from picamera2 import Picamera2
            self.camera = Picamera2()
            self.camera.configure(
                self.camera.create_preview_configuration(
                    main={"size": CAMERA_RESOLUTION}
                )
            )
            self.camera.start()
        else:
            self.camera = cv2.VideoCapture(CAMERA_INDEX)
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_RESOLUTION[0])
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_RESOLUTION[1])

    def capture_frame(self) -> Optional[np.ndarray]:
        """捕獲一幀圖像"""
        try:
            if IS_RASPBERRY_PI:
                return self.camera.capture_array()
            else:
                ret, frame = self.camera.read()
                return frame if ret else None
        except Exception as e:
            print(f"捕獲圖像時發生錯誤: {str(e)}")
            return None

    def detect_faces(
        self,
        frame: np.ndarray,
        scale_factor: float = 1.1,
        min_neighbors: int = 5,
        min_size: Tuple[int, int] = (30, 30)
    ) -> List[Tuple[int, int, int, int]]:
        """檢測人臉"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=scale_factor,
            minNeighbors=min_neighbors,
            minSize=min_size
        )
        return faces.tolist() if len(faces) else []

    def draw_faces(
        self,
        frame: np.ndarray,
        faces: List[Tuple[int, int, int, int]],
        color: Tuple[int, int, int] = (0, 255, 0),
        thickness: int = 2
    ) -> np.ndarray:
        """在圖像上繪製人臉框"""
        frame_copy = frame.copy()
        for (x, y, w, h) in faces:
            cv2.rectangle(frame_copy, (x, y), (x+w, y+h), color, thickness)
        return frame_copy

    def save_frame(self, frame: np.ndarray, filename: str) -> bool:
        """保存圖像"""
        try:
            return cv2.imwrite(filename, frame)
        except Exception as e:
            print(f"保存圖像時發生錯誤: {str(e)}")
            return False

    def release(self):
        """釋放攝像頭資源"""
        if not IS_RASPBERRY_PI:
            self.camera.release()

    def __del__(self):
        """析構函數"""
        self.release()