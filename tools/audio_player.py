# tools/audio_player.py
import sounddevice as sd
import numpy as np
from config.settings import AUDIO_SAMPLE_RATE

class AudioPlayer:
    async def execute(self) -> str:
        try:
            # 獲取設備信息
            devices = sd.query_devices()
            output_device = None
            
            # 尋找可用的輸出設備
            for i, device in enumerate(devices):
                if device['max_output_channels'] > 0:
                    output_device = i
                    break
            
            if output_device is None:
                return "錯誤：找不到可用的音頻輸出設備"

            # 生成一個簡單的嗶聲
            duration = 1.0  # 秒
            frequency = 440  # Hz
            t = np.linspace(0, duration, int(AUDIO_SAMPLE_RATE * duration))
            signal = np.sin(2 * np.pi * frequency * t)
            
            # 使用找到的輸出設備播放聲音
            sd.play(signal, AUDIO_SAMPLE_RATE, device=output_device)
            sd.wait()
            
            return "成功播放聲音"
        except Exception as e:
            # 列出所有可用的音頻設備以幫助診斷
            try:
                devices = sd.query_devices()
                devices_info = "\n可用的音頻設備：\n"
                for i, device in enumerate(devices):
                    devices_info += f"{i}: {device['name']} (輸出通道: {device['max_output_channels']})\n"
                return f"播放聲音時發生錯誤: {str(e)}\n{devices_info}"
            except:
                return f"播放聲音時發生錯誤: {str(e)}"