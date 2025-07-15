# import os
# import time
# import keyboard
# import numpy as np
# from dotenv import load_dotenv
# from deepgram import Deepgram
# import asyncio
# import aiofiles
# import sounddevice as sd
# from scipy.io.wavfile import write

# # ✅ Load API keys from .env
# load_dotenv()
# DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

# # ✅ Initialize Deepgram API
# deepgram = Deepgram(DEEPGRAM_API_KEY)

# # 📌 STEP 0: Record voice (start/stop with Enter key)
# def record_voice_dynamic(filename='sample.wav', fs=44100):
#     print("🎙️ Press [Enter] to START recording...")
#     keyboard.wait('enter')

#     print("🎤 Initializing microphone...")
#     time.sleep(0.5)  # Allow mic to warm up

#     stream = sd.InputStream(samplerate=fs, channels=1, dtype='int16')
#     stream.start()
#     print("🎤 Recording... Press [Enter] again to STOP.")

#     frames = []

#     while True:
#         data, _ = stream.read(1024)
#         frames.append(data)

#         if keyboard.is_pressed('enter'):
#             print("⏳ Waiting for key release...")
#             while keyboard.is_pressed('enter'):
#                 time.sleep(0.1)
#             break

#     stream.stop()
#     print(f"🛑 Recording stopped. Collected {len(frames)} frames.")

#     if len(frames) < 10:
#         print("⚠️ Not enough voice data captured. Try speaking for a bit longer.")
#         return False

#     audio_data = np.concatenate(frames, axis=0)
#     write(filename, fs, audio_data)
#     print(f"✅ Voice saved to {filename}")
#     return True

# # 📌 STEP 1: Transcribe with Deepgram
# async def transcribe_audio(file_path):
#     async with aiofiles.open(file_path, 'rb') as audio:
#         source = {
#             'buffer': await audio.read(),
#             'mimetype': 'audio/wav'
#         }
#         response = await deepgram.transcription.prerecorded(source, {'model': 'nova'})
#         return response['results']['channels'][0]['alternatives'][0]['transcript']

# # 📌 MAIN Loop
# async def main():
#     print("🧠 Voice-to-Text with Deepgram Transcription Ready")
#     print("🎙️ Press [Enter] to speak. Press [Ctrl+C] to exit.\n")

#     while True:
#         audio_file = 'sample.wav'
#         success = record_voice_dynamic(audio_file)

#         if not success:
#             print("🔁 Recording failed or was too short. Try again.\n")
#             continue

#         print("🎧 Transcribing...")
#         transcript = await transcribe_audio(audio_file)
#         print(f"🗣️ You said: {transcript}")

#         if not transcript.strip():
#             print("⚠️ No speech detected. Please try again.\n")
#             continue

# # ✅ Run the app
# if __name__ == '__main__':
#     try:
#         asyncio.run(main())
#     except KeyboardInterrupt:
#         print("\n👋 Chat Ended. See you next time!")








import os
import time
import keyboard
import numpy as np
from dotenv import load_dotenv
from deepgram import Deepgram  # Correct import for SDK version 2.x
import asyncio
import aiofiles
import sounddevice as sd
from scipy.io.wavfile import write

# ✅ Load API keys from .env
load_dotenv()
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

# ✅ Initialize Deepgram client for version 2.x
deepgram = Deepgram(DEEPGRAM_API_KEY)

# 📌 STEP 0: Record voice (start/stop with Enter key)
def record_voice_dynamic(filename='sample.wav', fs=44100):
    print("🎙️ Press [Enter] to START recording...")
    keyboard.wait('enter')

    print("🎤 Initializing microphone...")
    time.sleep(0.5)  # Allow mic to warm up

    stream = sd.InputStream(samplerate=fs, channels=1, dtype='int16')
    stream.start()
    print("🎤 Recording... Press [Enter] again to STOP.")

    frames = []

    while True:
        data, _ = stream.read(1024)
        frames.append(data)

        if keyboard.is_pressed('enter'):
            print("⏳ Waiting for key release...")
            while keyboard.is_pressed('enter'):
                time.sleep(0.1)
            break

    stream.stop()
    print(f"🛑 Recording stopped. Collected {len(frames)} frames.")

    if len(frames) < 10:
        print("⚠️ Not enough voice data captured. Try speaking for a bit longer.")
        return False

    audio_data = np.concatenate(frames, axis=0)
    write(filename, fs, audio_data)
    print(f"✅ Voice saved to {filename}")
    return True

# 📌 STEP 1: Transcribe with Deepgram (modified for version 2.x)
async def transcribe_audio(file_path):
    async with aiofiles.open(file_path, 'rb') as audio:
        source = {
            'buffer': await audio.read(),
            'mimetype': 'audio/wav'
        }
        
        # Use Deepgram's transcription method for version 2.x
        response = await deepgram.transcription.prerecorded(source, {'model': 'nova'})
        return response['results']['channels'][0]['alternatives'][0]['transcript']

# 📌 MAIN Loop
async def main():
    print("🧠 Voice-to-Text with Deepgram Transcription Ready")
    print("🎙️ Press [Enter] to speak. Press [Ctrl+C] to exit.\n")

    while True:
        audio_file = 'sample.wav'
        success = record_voice_dynamic(audio_file)

        if not success:
            print("🔁 Recording failed or was too short. Try again.\n")
            continue

        print("🎧 Transcribing...")
        transcript = await transcribe_audio(audio_file)
        print(f"🗣️ You said: {transcript}")

        if not transcript.strip():
            print("⚠️ No speech detected. Please try again.\n")
            continue

# ✅ Run the app
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Chat Ended. See you next time!")
