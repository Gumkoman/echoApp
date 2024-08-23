import pygame
from gtts import gTTS
import time

tts = gTTS(text="Abecadlo", lang='pl')
tts.save('test.mp3')
time.sleep(1)
pygame.mixer.init()
pygame.mixer.music.load("test.mp3")
pygame.mixer.music.play()
print("asd")
while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)
print("Halo")

# import wave
# import pyaudio

# # Open the .wav file
# wf = wave.open("output.wav", 'rb')

# # Initialize pyaudio
# p = pyaudio.PyAudio()

# # Open a stream
# stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
#                 channels=wf.getnchannels(),
#                 rate=wf.getframerate(),
#                 output=True)

# # Read data in chunks
# data = wf.readframes(1024)

# # Play the sound by writing the audio data to the stream
# while len(data) > 0:
#     stream.write(data)
#     data = wf.readframes(1024)

# # Stop and close the stream
# stream.stop_stream()
# stream.close()

# # Close pyaudio
# p.terminate()
# print("Ni mom pojecia")