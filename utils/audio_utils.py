import numpy as np
import sounddevice as sd
import soundfile as sf
from typing import Optional, Tuple
from config.settings import AUDIO_SAMPLE_RATE, AUDIO_OUTPUT_DIR

class AudioUtils:
    @staticmethod
    def generate_sine_wave(
        frequency: float = 440.0,
        duration: float = 1.0,
        amplitude: float = 0.5
    ) -> np.ndarray:
        """生成正弦波"""
        t = np.linspace(0, duration, int(AUDIO_SAMPLE_RATE * duration))
        return amplitude * np.sin(2 * np.pi * frequency * t)

    @staticmethod
    def record_audio(
        duration: float,
        channels: int = 1,
        sample_rate: Optional[int] = None
    ) -> Tuple[np.ndarray, int]:
        """錄製音頻"""
        if sample_rate is None:
            sample_rate = AUDIO_SAMPLE_RATE

        recording = sd.rec(
            int(duration * sample_rate),
            samplerate=sample_rate,
            channels=channels,
            dtype=np.float32
        )
        sd.wait()
        return recording, sample_rate

    @staticmethod
    def play_audio(
        data: np.ndarray,
        sample_rate: Optional[int] = None,
        blocking: bool = True
    ) -> None:
        """播放音頻"""
        if sample_rate is None:
            sample_rate = AUDIO_SAMPLE_RATE

        sd.play(data, sample_rate)
        if blocking:
            sd.wait()

    @staticmethod
    def save_audio(
        filename: str,
        data: np.ndarray,
        sample_rate: Optional[int] = None,
        subtype: str = 'PCM_24'
    ) -> str:
        """保存音頻文件"""
        if sample_rate is None:
            sample_rate = AUDIO_SAMPLE_RATE

        filepath = AUDIO_OUTPUT_DIR / filename
        sf.write(str(filepath), data, sample_rate, subtype=subtype)
        return str(filepath)

    @staticmethod
    def load_audio(filepath: str) -> Tuple[np.ndarray, int]:
        """加載音頻文件"""
        data, sample_rate = sf.read(str(filepath))
        return data, sample_rate

    @staticmethod
    def get_audio_devices() -> dict:
        """獲取可用的音頻設備"""
        return {
            'input': sd.query_devices(kind='input'),
            'output': sd.query_devices(kind='output')
        }