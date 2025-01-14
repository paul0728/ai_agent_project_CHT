import sounddevice as sd
import soundfile as sf
import speech_recognition as sr
from datetime import datetime
from config.settings import STT_OUTPUT_DIR, AUDIO_SAMPLE_RATE

class SpeechToText:
    async def execute(self) -> str:
        try:
            # 錄製音頻
            duration = 5.0  # 錄製5秒
            recording = sd.rec(
                int(AUDIO_SAMPLE_RATE * duration),
                samplerate=AUDIO_SAMPLE_RATE,
                channels=1
            )
            sd.wait()
            
            # 生成文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            audio_file = STT_OUTPUT_DIR / f"recording_{timestamp}.wav"
            text_file = STT_OUTPUT_DIR / f"transcript_{timestamp}.txt"
            
            # 保存音頻文件
            sf.write(str(audio_file), recording, AUDIO_SAMPLE_RATE)
            
            # 執行語音識別
            recognizer = sr.Recognizer()
            with sr.AudioFile(str(audio_file)) as source:
                audio = recognizer.record(source)
                text = recognizer.recognize_google(audio, language='zh-TW')
            
            # 保存文字文件
            with open(text_file, 'w', encoding='utf-8') as f:
                f.write(text)
            
            return f"語音已轉換為文字並保存到: {text_file}"
        except Exception as e:
            return f"語音轉文字時發生錯誤: {str(e)}"