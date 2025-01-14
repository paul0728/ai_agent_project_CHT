# config/settings.py

import os
import platform
from pathlib import Path
from dotenv import load_dotenv

# 載入 .env 文件
load_dotenv()

# 檢測是否為樹莓派
def is_raspberry_pi():
    try:
        with open('/sys/firmware/devicetree/base/model', 'r') as f:
            return 'Raspberry Pi' in f.read()
    except:
        return False

IS_RASPBERRY_PI = is_raspberry_pi()

# API設置
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"
DEEPSEEK_MODEL = "deepseek-chat"

# 音頻設置
AUDIO_OUTPUT_DIR = Path("output/audio")
AUDIO_SAMPLE_RATE = 44100
AUDIO_CHANNELS = 1
RECORD_DURATION = 3  # 錄音時長（秒）

# 語音轉文字設置
STT_OUTPUT_DIR = Path("output/stt")

# 攝像頭設置
CAMERA_INDEX = 0  # 默認攝像頭
CAMERA_RESOLUTION = (640, 480)
CAMERA_FPS = 30

# 確保API key存在
if not DEEPSEEK_API_KEY:
    raise ValueError("未設置 DEEPSEEK_API_KEY 環境變數")

# 創建必要的目錄
AUDIO_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
STT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)