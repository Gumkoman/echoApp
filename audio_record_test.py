import pyaudio
import wave
import threading
import tkinter as tk
import ttkbootstrap as ttk
from tkinter import messagebox

class WaveRecorder:
    def __init__(self):
        self.is_recording = False
        self.frames = []
        self.filename = None
        self.p = pyaudio.PyAudio()
        self.stream = None

    def start_recording(self, filename="output.wav"):
        if not self.is_recording:
            self.is_recording = True
            self.frames = []
            self.filename = filename
            self.stream = self.p.open(format=pyaudio.paInt16,
                                      channels=1,
                                      rate=44100,
                                      input=True,
                                      frames_per_buffer=1024)
            self.thread = threading.Thread(target=self._record_thread)
            self.thread.start()

    def stop_recording(self):
        if self.is_recording:
            self.is_recording = False
            self.thread.join()
            self.stream.stop_stream()
            self.stream.close()
            self._save_wave()

    def _record_thread(self):
        while self.is_recording:
            data = self.stream.read(1024)
            self.frames.append(data)

    def _save_wave(self):
        with wave.open(self.filename, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(self.p.get_sample_size(pyaudio.paInt16))
            wf.setframerate(44100)
            wf.writeframes(b''.join(self.frames))

class App(ttk.Window):
    def __init__(self, recorder):
        super().__init__(themename="darkly")
        self.title("Wave Audio Recorder")
        self.geometry("300x150")
        self.recorder = recorder

        self.record_button = ttk.Button(self, text="Start Recording", command=self.start_recording)
        self.record_button.pack(pady=20)

        self.stop_button = ttk.Button(self, text="Stop Recording", command=self.stop_recording)
        self.stop_button.pack(pady=20)
        self.stop_button["state"] = "disabled"

    def start_recording(self):
        filename = "output.wav"
        self.recorder.start_recording(filename)
        self.record_button["state"] = "disabled"
        self.stop_button["state"] = "normal"
        messagebox.showinfo("Recording", f"Recording started: {filename}")

    def stop_recording(self):
        self.recorder.stop_recording()
        self.record_button["state"] = "normal"
        self.stop_button["state"] = "disabled"
        messagebox.showinfo("Recording", "Recording stopped")

if __name__ == "__main__":
    recorder = WaveRecorder()
    app = App(recorder)
    app.mainloop()
