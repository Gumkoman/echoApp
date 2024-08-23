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
# while pygame.mixer.music.get_busy():
#     pygame.time.Clock().tick(10)
for i in range(500):
    print(f"{i}")
    time.sleep(0.1)
print("Halo")
def get_mp3_length(file_path):
    # Initialize the mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load(file_path)

    # Get the length of the file
    mp3_length = pygame.mixer.Sound(file_path).get_length()

    return mp3_length
length = get_mp3_length("test.mp3")
print(f"The length of the MP3 file is {length} seconds.")
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