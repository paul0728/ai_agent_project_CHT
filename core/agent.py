# core/agent.py

import json
import aiohttp
import sounddevice as sd
import soundfile as sf
import speech_recognition as sr
import numpy as np
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Tuple
from config.settings import (
    DEEPSEEK_API_KEY, 
    DEEPSEEK_BASE_URL, 
    DEEPSEEK_MODEL,
    AUDIO_SAMPLE_RATE,
    AUDIO_OUTPUT_DIR,
    AUDIO_CHANNELS,
    RECORD_DURATION
)

class AIAgent:
    def __init__(self):
        self.tools = {}
        self.tool_descriptions = {}
        self.recognizer = sr.Recognizer()
        self._initialize_tool_descriptions()

    def _initialize_tool_descriptions(self):
        """初始化工具描述，用於AI匹配意圖"""
        self.tool_descriptions = {
            "play_sound": {
                "keywords": ["播放喇叭", "播放聲音", "讓喇叭發聲", "播放", "聲音"],
                "description": "播放音頻的工具",
                "task": "Task1"
            },
            "speech_to_text": {
                "keywords": ["STT", "語音轉文字", "轉換語音", "語音識別"],
                "description": "將語音轉換為文字的工具",
                "task": "Task2"
            },
            "count_people": {
                "keywords": ["現場人數", "鏡頭中人數", "計算人數", "數人"],
                "description": "計算攝像頭中人數的工具",
                "task": "Task3"
            }
        }

    def register_tool(self, name: str, tool_instance: Any):
        """註冊工具"""
        self.tools[name] = tool_instance

    async def record_audio(self) -> Tuple[str, str]:
        """錄製音頻並轉換為文字"""
        try:
            print("開始錄音（3秒）...")
            recording = sd.rec(
                int(RECORD_DURATION * AUDIO_SAMPLE_RATE),
                samplerate=AUDIO_SAMPLE_RATE,
                channels=AUDIO_CHANNELS
            )
            sd.wait()
            print("錄音完成，正在處理...")

            # 保存錄音文件
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            audio_file = AUDIO_OUTPUT_DIR / f"command_{timestamp}.wav"
            sf.write(str(audio_file), recording, AUDIO_SAMPLE_RATE)

            # 將音頻轉換為文字
            with sr.AudioFile(str(audio_file)) as source:
                audio = self.recognizer.record(source)
                try:
                    text = self.recognizer.recognize_google(audio, language='zh-TW')
                    print(f"識別的語音: '{text}'")
                    return text, str(audio_file)
                except sr.UnknownValueError:
                    return "無法識別語音", str(audio_file)
                except sr.RequestError as e:
                    return f"語音識別服務錯誤: {str(e)}", str(audio_file)
        except Exception as e:
            return f"錄音過程發生錯誤: {str(e)}", ""

    async def _call_ai(self, text: str) -> str:
        """調用DeepSeek API進行意圖識別"""
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            
            # 構建提示詞
            prompt = f"""
            請分析以下用戶輸入，並從這些工具中選擇最合適的一個：
            {json.dumps(self.tool_descriptions, ensure_ascii=False)}
            
            用戶輸入: {text}
            
            請只返回工具名稱，無需其他解釋。
            """
            
            payload = {
                "model": DEEPSEEK_MODEL,
                "messages": [{"role": "user", "content": prompt}]
            }
            
            async with session.post(
                f"{DEEPSEEK_BASE_URL}/chat/completions",
                headers=headers,
                json=payload
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"API調用失敗: {response.status}, {error_text}")
                    
                result = await response.json()
                if not result.get('choices'):
                    raise Exception(f"API返回格式不正確: {result}")
                    
                return result['choices'][0]['message']['content'].strip()

    async def process_voice_command(self) -> str:
        """處理語音命令"""
        try:
            # 1. 錄音並轉換為文字
            text, audio_file = await self.record_audio()
            if text.startswith(("錄音過程發生錯誤", "語音識別服務錯誤", "無法識別語音")):
                return text
            
            return await self._process_command(text)
            
        except Exception as e:
            return f"處理語音命令時發生錯誤: {str(e)}"

    async def process_text_command(self, text: str) -> str:
        """處理文字命令"""
        try:
            return await self._process_command(text)
        except Exception as e:
            return f"處理文字命令時發生錯誤: {str(e)}"

    async def _process_command(self, text: str) -> str:
        """處理命令的共通邏輯"""
        try:
            # 1. 調用AI進行意圖識別
            tool_name = await self._call_ai(text)
            
            # 2. 查找對應的task編號
            task_number = None
            for name, info in self.tool_descriptions.items():
                if name == tool_name:
                    task_number = info["task"]
                    break
            
            # 3. 執行相應工具
            if tool_name in self.tools:
                result = await self.tools[tool_name].execute()
                return f"識別為 {task_number}，執行結果: {result}"
            else:
                return f"無法識別命令: {text}"
            
        except Exception as e:
            return f"處理命令時發生錯誤: {str(e)}"