#!/bin/bash
# install_raspberry_pi.sh

echo "開始安裝 AI Agent..."

# 更新系統
echo "更新系統..."
sudo apt-get update
sudo apt-get upgrade -y

# 安裝系統依賴
echo "安裝系統依賴..."
sudo apt-get install -y \
    python3-pip \
    python3-venv \
    libportaudio2 \
    portaudio19-dev \
    python3-opencv \
    python3-picamera2 \
    libatlas-base-dev \
    libjasper-dev \
    libqt4-test

# 創建虛擬環境
echo "創建Python虛擬環境..."
python3 -m venv venv
source venv/bin/activate

# 安裝Python依賴
echo "安裝Python依賴..."
pip install -r requirements.txt

# 配置音頻設備
echo "配置音頻設備..."
sudo usermod -a -G audio $USER

# 配置相機
echo "配置相機..."
if vcgencmd get_camera | grep -q "supported=1 detected=1"; then
    echo "已檢測到相機"
else
    echo "未檢測到相機，請確認相機連接是否正確"
fi

echo "安裝完成！"
echo "請確保："
echo "1. 已設置 .env 檔案中的 DEEPSEEK_API_KEY"
echo "2. 已正確連接麥克風和喇叭"
echo "3. 已正確連接相機（PiCamera 或 USB 攝像頭）"
echo ""
echo "運行方式："
echo "1. 啟動虛擬環境：source venv/bin/activate"
echo "2. 運行程式：python main.py"