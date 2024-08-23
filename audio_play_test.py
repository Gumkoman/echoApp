import wave
import pyaudio

# Open the .wav file
wf = wave.open("output.wav", 'rb')

# Initialize pyaudio
p = pyaudio.PyAudio()

# Open a stream
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)

# Read data in chunks
data = wf.readframes(1024)

# Play the sound by writing the audio data to the stream
while len(data) > 0:
    stream.write(data)
    data = wf.readframes(1024)

# Stop and close the stream
stream.stop_stream()
stream.close()

# Close pyaudio
p.terminate()
print("Ni mom pojecia")