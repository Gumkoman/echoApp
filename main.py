import tkinter as tk
from tkinter import StringVar
from tkinter import ttk
import subprocess
import time
import threading
import ttkbootstrap as ttkb
# import pyaudio
# import wave
# from pydub import AudioSegment
# from audioplayer import AudioPlayer
import pygame
from gtts import gTTS
import datetime

from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy


def initialize_appium(app_package,app_activity):
    appium_server_url = 'http://localhost:4723'
    capabilities = dict(
        platformName='Android',
        automationName='uiautomator2',
        appPackage=app_package,
        appActivity=app_activity,
        newCommandTimeout=360,
        adbExecTimeout=40000,
        fullReset=False,
        noReset=True
    )
    options = UiAutomator2Options()
    options.load_capabilities(capabilities)
    driver = webdriver.Remote(appium_server_url, options=options)
    driver.execute_script('mobile: shell', {
            'command': 'am',
            'args': ['start', '-n', f'{app_package}/{app_activity}']
        })
    return driver

def declare_app_status(driver):
    
    try:
        login_main_element = WebDriverWait(driver,10).until(EC.presence_of_element_located((AppiumBy.ID,'com.EveryTalk.Global:id/login_logo')))
        login_main_element = WebDriverWait(driver,10).until(EC.presence_of_element_located((AppiumBy.ID,'com.EveryTalk.Global:id/login_id')))

        if login_main_element:
            return "login_page"
    except:
        pass
    try:
        login_main_element = WebDriverWait(driver,10).until(EC.presence_of_element_located((AppiumBy.ID,'com.EveryTalk.Global:id/main_logo')))
        if login_main_element:
            return "main_page"
    except:
        pass
    return "unknown"

def login_cybertel(driver,login,password):
    """
    The function `login_cybertel` attempts to log in to a mobile application using provided login
    credentials and returns different messages based on the success or failure of each step.
    
    :param driver: The `driver` parameter in the `login_cybertel` function is typically an instance of a
    WebDriver class that allows interaction with a web or mobile application during automated testing.
    It is used to locate elements on the page, interact with them, and perform various actions like
    clicking buttons or entering text
    :param login: The `login` parameter in the `login_cybertel` function is the username or login ID
    that the user wants to input into the login field of the Cybertel application
    :param password: The `password` parameter in the `login_cybertel` function is used to pass the
    password for logging into the Cybertel application. The function attempts to locate the password
    input field on the login page and then enters the provided password into that field
    :return: The function `login_cybertel` returns different messages based on the outcome of the login
    process. Here are the possible return messages:
    """
    try:
        element = WebDriverWait(driver,10).until(EC.presence_of_element_located((AppiumBy.ID,'com.EveryTalk.Global:id/login_id')))
        element.clear()
        element.send_keys(login)
    except:
        return "unable to pass login"
    try:
        element = WebDriverWait(driver,10).until(EC.presence_of_element_located((AppiumBy.ID,'com.EveryTalk.Global:id/login_pw')))
        element.clear()
        element.send_keys(password)
    except:
        return "unable to pass password"
    try:
        element = WebDriverWait(driver,10).until(EC.presence_of_element_located((AppiumBy.ID,'com.EveryTalk.Global:id/login_btn')))
        element.click()
    except:
        return "unable to click login button"
    try:
        element = WebDriverWait(driver,10).until(EC.presence_of_element_located((AppiumBy.ID,'android:id/button1')))
        element.click()
    except:
        pass
    try:
        login_main_element = WebDriverWait(driver,10).until(EC.presence_of_element_located((AppiumBy.ID,'com.EveryTalk.Global:id/login_main')))
        if login_main_element:
            return "main_page"
    except:
        return "Failed to login"

def check_for_call(driver):
    try:
        element = WebDriverWait(driver,5).until(EC.presence_of_element_located((AppiumBy.ID,"com.EveryTalk.Global:id/voice_main_image")))
        return True
    except:
        return False
def get_mp3_length(file_path):
    # Initialize the mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load(file_path)

    # Get the length of the file
    mp3_length = pygame.mixer.Sound(file_path).get_length()

    return mp3_length
def text_to_speech(text, filename):
    tts = gTTS(text=text, lang='pl')
    tts.save(filename)
    print(f"Audio saved to {filename}")
    return filename

def select_mcptt_server(driver, server_to_choose='Polkomtel 1'):
        try:
            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((AppiumBy.ID, 'pl.dgt.mcptt:id/decor_icon')))
            element.click()
        except:
            print("Error clicking server choose list")
        try:
            elements = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((AppiumBy.ID, 'pl.dgt.mcptt:id/text')))
            for element in elements:
                if element.text == server_to_choose:
                    element.click()
                    return
        except:
            print("error selecting server")

class CustomTkinterApp(ttkb.Window):
    def __init__(self):
        super().__init__()

        self.title("Komunikator PTT")
        self.geometry("400x350")
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)
        self.grid_columnconfigure((0, 1), weight=1)
        self._is_running = False
        # Create StringVar instances for Comboboxes and TextInputs
        self.combo_var1 = StringVar()
        self.combo_var2 = StringVar()
        self.combo_var3 = StringVar()
        self.combo_var4 = StringVar()  # Added for the fourth combo box
        self.text_var1 = StringVar()
        self.text_var2 = StringVar()

        # Set default values for the comboboxes
        self.combo_var1.set("No devices connected")
        self.combo_var2.set("Cybertel MCX")
        self.combo_var3.set("Odpowiedz robota + echo")
        self.combo_var4.set("Server 1")  # Default value for the fourth combo box

        # self.audio = pyaudio.PyAudio()
        # self.stream = None
        # self.frames = []

        # Create and place the widgets
        self.create_widgets()

        # Populate the Terminal combobox with connected devices
        self.update_devices()

        self.thread = None
        self.stop_thread = threading.Event()

    def create_widgets(self):
        # Create and place the labels and comboboxes
        label1 = ttkb.Label(self, text="Terminal:")
        label1.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.combo1 = ttkb.Combobox(self, textvariable=self.combo_var1)
        self.combo1.grid(row=0, column=1, padx=10, pady=5, sticky="we")

        label2 = ttkb.Label(self, text="Aplikacja:")
        label2.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.combo2 = ttkb.Combobox(self, textvariable=self.combo_var2, values=['Cybertel MCX', 'MCPTT'])
        self.combo2.grid(row=1, column=1, padx=10, pady=5, sticky="we")
        self.combo2.bind("<<ComboboxSelected>>", self.on_app_selected)  # Bind the event

        label3 = ttkb.Label(self, text="Dzwiek:")
        label3.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.combo3 = ttkb.Combobox(self, textvariable=self.combo_var3, values=["Odpowiedz robota + echo", "Odpowiedz Robota", "Echo"])
        self.combo3.grid(row=2, column=1, padx=10, pady=5, sticky="we")

        label4 = ttkb.Label(self, text="Serwer:")
        label4.grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.combo4 = ttkb.Combobox(self, textvariable=self.combo_var4, values=["Server 1", "Server 2", "Server 3"])
        self.combo4.grid(row=3, column=1, padx=10, pady=5, sticky="we")

        # Create and place the labels and text inputs
        label5 = ttkb.Label(self, text="Login:")
        label5.grid(row=4, column=0, padx=10, pady=5, sticky="e")
        self.text_input1 = ttkb.Entry(self, textvariable=self.text_var1)
        self.text_input1.grid(row=4, column=1, padx=10, pady=5, sticky="we")

        label6 = ttkb.Label(self, text="Haslo:")
        label6.grid(row=5, column=0, padx=10, pady=5, sticky="e")
        self.text_input2 = ttkb.Entry(self, textvariable=self.text_var2, show="*")
        self.text_input2.grid(row=5, column=1, padx=10, pady=5, sticky="we")

        # Create and place the button
        self.button = ttkb.Button(self, text="Start", command=self.on_submit)
        self.button.grid(row=6, column=0, columnspan=2, padx=10, pady=20, sticky="we")

        # Create and place the status bar
        self.status_bar = ttkb.Label(self, text="Status: Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.grid(row=7, column=0, columnspan=2, padx=10, pady=5, sticky="we")

    def update_devices(self):
        """
        The function `update_devices` retrieves a list of connected devices using adb command and
        updates a combobox with the list of devices.
        """
        try:
            # Run adb devices command and get the output
            result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
            output = result.stdout.strip()

            # Parse the output to get the list of connected devices
            devices = []
            for line in output.splitlines():
                if '\tdevice' in line:
                    devices.append(line.split('\t')[0])

            # Update the combobox with the list of devices
            if devices:
                self.combo1.configure(values=devices)
                self.combo_var1.set(devices[0])  # Set the first device as the default
            else:
                self.combo1.configure(values=["No devices connected"])
                self.combo_var1.set("No devices connected")
        except Exception as e:
            print(f"Error updating devices: {e}")
            self.combo1.configure(values=["Error detecting devices"])
            self.combo_var1.set("Error detecting devices")

    def on_app_selected(self, event):
        selected_app = self.combo_var2.get()
        print(f"Selected application: {selected_app}")  # Debugging statement
        if selected_app == "Cybertel MCX":
            new_options = ["Server 1", "Server 2", "Server 3"]
        elif selected_app == "MCPTT":
            new_options = ["Server A", "Server B", "Server C"]
        else:
            new_options = ["Unknown"]

        print(f"Updating servers to: {new_options}")  # Debugging statement
        self.combo4.configure(values=new_options)
        self.combo_var4.set(new_options[0])  # Set the first server option as the default

    def get_main_mcptt_button(self, driver):
        try:
            button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((AppiumBy.ID, 'pl.dgt.mcptt:id/ptt_button_only')))
            text_view = WebDriverWait(button, 10).until(EC.presence_of_element_located((AppiumBy.CLASS_NAME, 'android.widget.TextView'))) 
            return text_view.get_attribute("text")
        except:
            return 'None'


    def worker(self):
        self.status_bar.config(text="Zestawianie polaczenia appium")
        selected_app = self.combo_var2.get()
        self._is_running = True
        if selected_app == "Cybertel MCX":
            app_package = 'com.EveryTalk.Global'
            app_activity = 'com.cybertel.mcptt.ui.main.EveryTalkMain'
        elif selected_app == "MCPTT":
            app_package = 'pl.dgt.mcptt'
            app_activity = 'pl.dgt.mcptt.gui.activity.MainActivity'

        driver = initialize_appium(app_package,app_activity)
        self.status_bar.config(text="Uruchamianie aplikacji")

        login_text = self.text_input1.get()
        password_text = self.text_input2.get()
        print("Start")
        if selected_app == "Cybertel MCX":
            status = declare_app_status(driver)
            while(status != "main_page"):
                print("Current status is",status)
                if status == "login_page":
                    self.status_bar.config(text="Logowanie do aplikacji")
                    status = login_cybertel(driver,login_text,password_text)
                    print(f"Staus of login is {status}")
                elif status == "main_page":
                    self.status_bar.config(text="Oczekiwanie na przycisk")
                    pass
                else:
                    self.status_bar.config(text="Resetowanie aplikacji")
                    driver.execute_script('mobile: shell', {
                        'command': 'am',
                        'args': ['start', '-n', f'{app_package}/{app_activity}']
                    })
                status = declare_app_status(driver)
            print("Exited init loop")
            status = "Waiting"
            while self._is_running:
                if status == "Waiting":
                    if check_for_call():
                        status = "start_recording"
                elif status == "start_recording":
                    # #TODO some function that starts recording and is threded
                    # self.frames = []
                    # try:
                    #     self.stream = self.audio.open(format=pyaudio.paInt16,
                    #                                 channels=1,  # Use 1 channel for mono recording
                    #                                 rate=44100,
                    #                                 input=True,
                    #                                 frames_per_buffer=1024)
                    #     self.is_recording = True
                    #     threading.Thread(target=self.record).start()
                    # except Exception as e:
                    #     print(f"Error starting recording: {e}")

                    status = "recording"
                elif status == "recording":
                    if not check_for_call():
                        status = "stop_recording"
                elif status == "stop_recording":
                    # The above code is not valid Python code. The `self` keyword is typically used
                    # within a class definition in Python to refer to the instance of the class
                    # itself. However, in this context, it is not being used correctly. The `
                    # self.is_recording = False
                    # if self.stream is not None:
                    #     self.stream.stop_stream()
                    #     self.stream.close()

                    # with wave.open("output.wav", 'wb') as wf:
                    #     wf.setnchannels(1)  # Set 1 channel for mono recording
                    #     wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
                    #     wf.setframerate(44100)
                    #     wf.writeframes(b''.join(self.frames))
                    status = "respond"
                elif status == "respond":
                    try:
                        now = datetime.datetime.now()
                        msg = f'Otrzymalem wiadomosc o godzinie {now.hour} {now.minute} minut'
                        text_to_speech(msg, 'robot.mp3')
                        #TODO respond no need for it to be threaded
                        button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((AppiumBy.ID, 'com.EveryTalk.Global:id/main_menu_ptt_key')))
                        button.click()
                        # player = AudioPlayer('robot.mp3')
                        # player.play(block=True)
                        pygame.mixer.init()
                        pygame.mixer.music.load("robot.mp3")
                        pygame.mixer.music.play()

                        while pygame.mixer.music.get_busy():
                            pygame.time.Clock().tick(10)
                        # player = AudioPlayer('output.wav')
                        # player.play(block=True)
                        button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((AppiumBy.ID, 'com.EveryTalk.Global:id/main_menu_ptt_key')))
                        button.click()
                    except:
                        pass
                    status = "Waiting"                  

        elif selected_app == "MCPTT":
            #init app
            try:
                self.status_bar.config(text="Proba Logowania do Aplikacji")
                element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((AppiumBy.ID, 'pl.dgt.mcptt:id/activity_login_username_edittext')))
                element.send_keys(login_text)
                element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((AppiumBy.ID, 'pl.dgt.mcptt:id/activity_login_password_edittext')))
                element.send_keys(password_text)
                element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((AppiumBy.ID, 'pl.dgt.mcptt:id/activity_login_button')))
                element.click()
                
            except:
                pass
            self.status_bar.config(text="Wybieranie serwera MCPTT")
            select_mcptt_server(driver)
            #go to main loop
            state = "Waiting"
            while self._is_running:
                if state == "Waiting":
                    time.sleep(1)
                    self.status_bar.config(text="Oczekiwanie na polaczenie")
                    text_button = self.get_main_mcptt_button(driver)
                    # print(f"text_button is {text_button}")
                    if 'czenie' in text_button:
                        state = "start_recording"
                elif state == "start_recording":
                    self.status_bar.config(text="Rozpoczynam nagrywanie ")
                    # self.frames = []
                    # try:
                    #     self.stream = self.audio.open(format=pyaudio.paInt16,
                    #                                 channels=1,  # Use 1 channel for mono recording
                    #                                 rate=44100,
                    #                                 input=True,
                    #                                 frames_per_buffer=1024)
                    #     self.is_recording = True
                    #     threading.Thread(target=self.record).start()
                    # except Exception as e:
                    #     print(f"Error starting recording: {e}")
                    state = "recording"
                elif state == "recording":
                    self.status_bar.config(text="Nagrywanie polaczenia")
                    text_button = self.get_main_mcptt_button(driver)
                    #TODO some logic to get that it stopped
                    if "czenie" not in text_button:
                        state = 'stop_recording'
                elif state == "stop_recording":
                    self.is_recording = False
                    # if self.stream is not None:
                    #     self.stream.stop_stream()
                    #     self.stream.close()

                    # with wave.open("output.wav", 'wb') as wf:
                    #     wf.setnchannels(1)  # Set 1 channel for mono recording
                    #     wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
                    #     wf.setframerate(44100)
                    #     wf.writeframes(b''.join(self.frames))
                    state = "respond"
                elif state == "respond":
                    self.status_bar.config(text="Odpowiadanie")
                    try:
                        now = datetime.datetime.now()
                        msg = f'Otrzymalem wiadomosc o godzinie {now.hour} {now.minute} minut'
                        text_to_speech(msg, 'robot.mp3')
                        #TODO respond no need for it to be threaded
                        button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((AppiumBy.ID, 'pl.dgt.mcptt:id/ptt_button_only')))
                        # audio_duration = AudioSegment.from_file('robot.mp3').duration_seconds
                        # player = AudioPlayer('robot.mp3')
                        # player.play(block=False)
                        pygame.mixer.init()
                        pygame.mixer.music.load("test.mp3")
                        audio_duration = get_mp3_length("robot.mp3")
                        pygame.mixer.music.play()

                        driver.execute_script('mobile: longClickGesture', {
                            'elementId': button.id,
                            'duration': audio_duration * 1000 + 500
                        })
                        button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((AppiumBy.ID, 'pl.dgt.mcptt:id/ptt_button_only')))
                        # audio_duration = AudioSegment.from_file('output.wav').duration_seconds
                        # player = AudioPlayer('output.wav')
                        # player.play(block=False)
                        # driver.execute_script('mobile: longClickGesture', {
                        #     'elementId': button.id,
                        #     'duration': audio_duration * 1000 + 500
                        # })
                    except:
                        pass
                    state = "Waiting"

            

    def record(self):
        while self.is_recording:
            try:
                data = self.stream.read(1024)
                self.frames.append(data)
            except Exception as e:
                print(f"Error recording audio: {e}")
                break

    def on_submit(self):
        if self.button.cget("text") == "Start":
            # Disable the comboboxes and text inputs
            self.combo1.config(state="disabled")
            self.combo2.config(state="disabled")
            self.combo3.config(state="disabled")
            self.combo4.config(state="disabled")
            self.text_input1.config(state="disabled")
            self.text_input2.config(state="disabled")

            # Change the button text to "Stop"
            self.button.config(text="Stop")

            # Update the status bar
            self.status_bar.config(text="Status: Running")

            # Start the worker thread
            self.stop_thread.clear()
            self.thread = threading.Thread(target=self.worker)
            self.thread.daemon = True
            self.thread.start()

            print("Started")
        else:
            # Enable the comboboxes and text inputs
            self.combo1.config(state="normal")
            self.combo2.config(state="normal")
            self.combo3.config(state="normal")
            self.combo4.config(state="normal")
            self.text_input1.config(state="normal")
            self.text_input2.config(state="normal")

            # Change the button text to "Start"
            self.button.config(text="Start")

            # Update the status bar
            self.status_bar.config(text="Status: Stopped")

            # Stop the worker thread
            self.stop_thread.set()
            self.thread.join()

            print("Stopped")

# Run the application
if __name__ == "__main__":
    app = CustomTkinterApp()
    app.style.theme_use("litera")
    app.mainloop()
