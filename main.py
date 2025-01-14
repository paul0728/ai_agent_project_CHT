# main.py

import asyncio
from core.agent import AIAgent
from tools.audio_player import AudioPlayer
from tools.speech_to_text import SpeechToText
from tools.people_counter import PeopleCounter

async def main():
    # 創建AI Agent實例
    agent = AIAgent()
    
    # 註冊工具
    agent.register_tool("play_sound", AudioPlayer())
    agent.register_tool("speech_to_text", SpeechToText())
    agent.register_tool("count_people", PeopleCounter())
    
    print("\n=== AI Agent控制系統 ===")
    print("可用的任務：")
    print("1. Task1 - 播放聲音（命令：播放喇叭、播放聲音、讓喇叭發聲等）")
    print("2. Task2 - 語音轉文字（命令：STT、語音轉文字等）")
    print("3. Task3 - 計算人數（命令：現場人數、鏡頭中人數等）")
    
    # 主循環
    while True:
        try:
            print("\n請選擇輸入方式：")
            print("1. 語音輸入")
            print("2. 文字輸入")
            print("3. 退出程序")
            
            choice = input("\n請輸入選項 (1-3): ").strip()
            
            if choice == "3":
                print("程序結束")
                break
                
            elif choice == "1":
                print("\n請說出您的命令...")
                result = await agent.process_voice_command()
                print(result)
                
            elif choice == "2":
                command = input("\n請輸入您的命令: ")
                result = await agent.process_text_command(command)
                print(result)
                
            else:
                print("無效的選項，請重新選擇")
            
        except KeyboardInterrupt:
            print("\n程序已中止")
            break
        except Exception as e:
            print(f"發生錯誤: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())