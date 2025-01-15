# AI Voice Command Agent

這是一個基於語音命令的 AI 代理系統，可以執行三種任務：語音播放、語音轉文字和人數統計。系統支援語音和文字兩種輸入方式，並且可以在 Windows 和 Raspberry Pi 環境下運行。

## 功能特點

- **多模式輸入**：支援語音輸入和文字輸入
- **三大功能**：
  - 播放聲音（Task1）
  - 語音轉文字（Task2）
  - 即時人數統計（Task3）
- **跨平台支援**：
  - Windows 環境
  - Raspberry Pi 環境
- **彈性相機支援**：
  - Raspberry Pi Camera
  - USB 攝像頭

## 系統需求

### Windows 環境
- Python 3.8+
- OpenCV 支援的 USB 攝像頭
- 麥克風
- 喇叭或耳機

### Raspberry Pi 環境
- Raspberry Pi 4B 或 Raspberry Pi 5
- Python 3.8+
- 作業系統：Raspberry Pi OS

#### 支援的硬體配置：
- **相機選項**：
  - Raspberry Pi Camera Module 3
  - Raspberry Pi Camera Module 2
  - 任何與 OpenCV 相容的 USB 攝像頭
- **音訊設備**：
  - USB 麥克風或支援音訊輸入的 USB 聲卡
  - 3.5mm 音訊輸出或 USB 喇叭

## 安裝指南

### Windows 安裝步驟

1. 克隆專案：
```bash
git clone [https://github.com/paul0728/ai_agent_project_CHT.git]
cd ai_agent_project_CHT
```

2. 創建並啟動虛擬環境：
```bash
python -m venv venv
.\venv\Scripts\activate
```

3. 安裝依賴：
```bash
pip install -r requirements.txt
```

4. 配置環境變數：
   - 複製 `.env.example` 為 `.env`
   - 編輯 `.env` 文件，
     - DEEPSEEK_API_KEY 設置 (必須)
     - 相機設置（可選）
     - 音頻設置（可選）

5. 運行程式：
```bash
python main.py
```

### Raspberry Pi 安裝步驟

1. 系統更新：
```bash
sudo apt-get update
sudo apt-get upgrade
```

2. 安裝系統依賴：
```bash
sudo apt-get install -y \
    python3-pip \
    python3-venv \
    libportaudio2 \
    portaudio19-dev \
    python3-opencv \
    python3-picamera2
```

3. 克隆並設置專案：
```bash
git clone [https://github.com/paul0728/ai_agent_project_CHT.git]
cd ai_agent_project_CHT
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

4. 配置相機：
```bash
# 如果使用 Pi Camera
sudo raspi-config
# 進入 Interface Options -> Camera -> Enable

# 如果使用 USB 攝像頭，確認連接：
ls /dev/video*
```

5. 配置音訊設備：
```bash
# 確認音訊設備
arecord -l
aplay -l
```

6. 設置環境變數：
```bash
cp .env.example .env
# 編輯 .env 文件，添加 DEEPSEEK_API_KEY
```

## 使用指南

1. 運行程式：
```bash
python main.py
```

2. 選擇輸入模式：
   - 1: 語音輸入
   - 2: 文字輸入
   - 3: 退出程序

3. 可用命令：
   - Task1 (播放聲音)：
     - "播放喇叭"
     - "播放聲音"
     - "讓喇叭發聲"
   - Task2 (語音轉文字)：
     - "STT"
     - "語音轉文字"
   - Task3 (計算人數)：
     - "現場人數"
     - "鏡頭中人數"

## 故障排除

### Windows 環境
1. 相機問題：
   - 確認設備管理器中攝像頭狀態
   - 檢查 CAMERA_INDEX 設置（預設為 0）

2. 音訊問題：
   - 確認系統音訊設置
   - 檢查麥克風權限

### Raspberry Pi 環境
1. Pi Camera 問題：
   - 檢查排線連接
   - 確認相機已在 raspi-config 中啟用
   - 運行 `libcamera-hello` 測試相機

2. USB 攝像頭問題：
   - 運行 `ls /dev/video*` 確認設備
   - 檢查 USB 連接和供電

3. 音訊問題：
   - 運行 `arecord -l` 檢查錄音設備
   - 運行 `aplay -l` 檢查播放設備

## 注意事項

1. 相機設置：
   - Windows 環境預設使用系統默認攝像頭
   - Raspberry Pi 環境優先使用 Pi Camera，如果無法使用則自動切換到 USB 攝像頭

2. 音訊設置：
   - 確保系統默認音訊輸入/輸出設備正確設置
   - Raspberry Pi 使用 USB 音訊設備時，可能需要額外配置

3. API 密鑰：
   - 必須設置有效的 DEEPSEEK_API_KEY
   - API 調用需要穩定的網路連接
