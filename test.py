from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time 

class Driver:
    def __init__(self, phone_uuid, app_activity, app_package) -> None:
        options = UiAutomator2Options()
        options.device_name = phone_uuid
        options.platform_name = "Android"
        options.automation_name = "uiautomator2"
        options.app_activity = app_activity
        options.app_package = app_package
        options.full_reset = False
        options.no_reset = True
        self.driver = webdriver.Remote("http://localhost:4723", options=options)
        self.driver.execute_script('mobile: shell', {
            'command': 'am',
            'args': ['start', '-n', f'{app_package}/{app_activity}']
        })

    def quit(self):
        """Quit the Appium driver session."""
        self.driver.quit()

    def click_element(self, by, value, wait_time=10):
        """
        Clicks on an element located by the given strategy and value.
        
        Args:
            by (str): The strategy to locate the element.
            value (str): The locator value.
            wait_time (int): The time to wait for the element to be located.
        
        Raises:
            TimeoutException: If the element is not found within the specified time.
            NoSuchElementException: If the element does not exist.
        """
        try:
            element = self.find_element(by, value, wait_time)
            element.click()
        except Exception as e:
            print(f"Error clicking element with {by} = '{value}': {str(e)}")
            raise

    def get_element_attribute(self, by, value, attribute, wait_time=10):
        """
        Retrieves an attribute of an element located by the given strategy and value.
        
        Args:
            by (str): The strategy to locate the element.
            value (str): The locator value.
            attribute (str): The attribute to retrieve.
            wait_time (int): The time to wait for the element to be located.
        
        Returns:
            str: The attribute value.
        
        Raises:
            TimeoutException: If the element is not found within the specified time.
            NoSuchElementException: If the element does not exist.
        """
        try:
            element = self.find_element(by, value, wait_time)
            return element.get_attribute(attribute)
        except Exception as e:
            print(f"Error getting attribute '{attribute}' from element with {by} = '{value}': {str(e)}")
            raise

    def find_element(self, by, value, wait_time=10):
        """
        Finds an element located by the given strategy and value.
        
        Args:
            by (str): The strategy to locate the element.
            value (str): The locator value.
            wait_time (int): The time to wait for the element to be located.
        
        Returns:
            WebElement: The located element.
        
        Raises:
            TimeoutException: If the element is not found within the specified time.
            NoSuchElementException: If the element does not exist.
        """
        try: 
            element = WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            print(f"Error: Element with {by} = '{value}' was not found within {wait_time} seconds.")
            raise
        except NoSuchElementException:
            print(f"Error: Element with {by} = '{value}' does not exist.")
            raise
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")
            raise


import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
import threading
import subprocess
from datetime import datetime
from tkinter import Menu
from appium import webdriver

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Szczekajka")

        # Configure grid to make it resizable
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(7, weight=1)

        # Define variables for input
        self.terminal = tk.StringVar()
        self.aplikacja = tk.StringVar()
        self.dzwiek = tk.StringVar(value="Robot+Echo")
        self.serwer = tk.StringVar()
        self.login = tk.StringVar()
        self.haslo = tk.StringVar()

        # Predefined values for applications and servers
        self.app_data = {
            "Cybertel MCX": {
                "package": "com.EveryTalk.Global",
                "activity": "com.cybertel.mcptt.ui.main.EveryTalkMain",
                "servers": ["Server 1", "Server 2", "Server 3"]
            },
            "MCPTT": {
                "package": "pl.dgt.mcptt",
                "activity": "pl.dgt.mcptt.gui.activity.MainActivity",
                "servers": ["Server A", "Server B", "Server C"]
            }
        }

        # Create the input fields and labels
        self.create_widgets()

    def create_widgets(self):
        # Terminal
        ttk.Label(self.root, text="Terminal:").grid(row=0, column=0, padx=10, pady=10, sticky=W)
        self.terminal_combobox = ttk.Combobox(self.root, textvariable=self.terminal, bootstyle="primary")
        self.terminal_combobox.grid(row=0, column=1, padx=10, pady=10, sticky=EW)
        self.populate_terminals()

        # Aplikacja
        ttk.Label(self.root, text="Aplikacja:").grid(row=1, column=0, padx=10, pady=10, sticky=W)
        self.aplikacja_combobox = ttk.Combobox(self.root, textvariable=self.aplikacja, bootstyle="primary")
        self.aplikacja_combobox['values'] = list(self.app_data.keys())
        self.aplikacja_combobox.grid(row=1, column=1, padx=10, pady=10, sticky=EW)
        self.aplikacja_combobox.bind("<<ComboboxSelected>>", self.update_serwer_options)

        # Dzwiek
        ttk.Label(self.root, text="Dzwiek:").grid(row=2, column=0, padx=10, pady=10, sticky=W)
        self.dzwiek_combobox = ttk.Combobox(self.root, textvariable=self.dzwiek, bootstyle="primary")
        self.dzwiek_combobox['values'] = ["Robot+Echo", "Robot", "Echo"]
        self.dzwiek_combobox.grid(row=2, column=1, padx=10, pady=10, sticky=EW)

        # Serwer
        ttk.Label(self.root, text="Serwer:").grid(row=3, column=0, padx=10, pady=10, sticky=W)
        self.serwer_combobox = ttk.Combobox(self.root, textvariable=self.serwer, bootstyle="primary")
        self.serwer_combobox.grid(row=3, column=1, padx=10, pady=10, sticky=EW)

        # Login
        ttk.Label(self.root, text="Login:").grid(row=4, column=0, padx=10, pady=10, sticky=W)
        ttk.Entry(self.root, textvariable=self.login, bootstyle="primary").grid(row=4, column=1, padx=10, pady=10, sticky=EW)

        # Haslo
        ttk.Label(self.root, text="Haslo:").grid(row=5, column=0, padx=10, pady=10, sticky=W)
        ttk.Entry(self.root, textvariable=self.haslo, show="*", bootstyle="primary").grid(row=5, column=1, padx=10, pady=10, sticky=EW)

        # Start Button
        start_button = ttk.Button(self.root, text="Start Test", command=self.start_test_thread, bootstyle="success")
        start_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky=EW)

        # Status Table
        ttk.Label(self.root, text="Status:").grid(row=7, column=0, padx=10, pady=10, sticky='N')
        self.status_table = ttk.Treeview(self.root, columns=("Time", "Event"), show='headings', height=10, bootstyle="info")
        self.status_table.heading("Time", text="Time")
        self.status_table.heading("Event", text="Event")
        self.status_table.grid(row=7, column=1, padx=10, pady=10, sticky=NSEW)

        # Set column widths
        self.status_table.column("Time", width=150, anchor=W)
        self.status_table.column("Event", anchor=W)

        # Enable resizing for the status table
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(7, weight=1)

        # Bind double-click events
        self.status_table.bind("<Double-1>", self.on_double_click)

        # Context menu for copying
        self.create_context_menu()

    def populate_terminals(self):
        """Populate the terminal combobox with devices seen by adb."""
        try:
            result = subprocess.run(['adb', 'devices'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            devices = [line.split()[0] for line in result.stdout.splitlines() if 'device' in line and not 'List' in line]
            self.terminal_combobox['values'] = devices
            if devices:
                self.terminal_combobox.current(0)
        except Exception as e:
            ttk.messagebox.showerror("Error", f"Could not fetch devices: {str(e)}")

    def update_serwer_options(self, event=None):
        """Update the server combobox based on the selected application."""
        selected_app = self.aplikacja.get()
        if selected_app in self.app_data:
            self.serwer_combobox['values'] = self.app_data[selected_app]["servers"]
            self.serwer_combobox.current(0)

    def start_test_thread(self):
        """Start the test in a separate thread to keep the GUI responsive."""
        threading.Thread(target=self.run_test, daemon=True).start()

    def log_event(self, message):
        """Log an event with a timestamp to the status table."""
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.root.after(0, self._insert_log_event, current_time, message)

    def _insert_log_event(self, time, message):
        """Insert the event into the status table (runs in main thread)."""
        item_id = self.status_table.insert("", "end", values=(time, message))
        self.status_table.see(item_id)  # Scroll to the last entry

    def on_double_click(self, event):
        """Open a new window with full text on double-click."""
        item = self.status_table.identify_row(event.y)
        column = self.status_table.identify_column(event.x)
        text = self.status_table.item(item, "values")[int(column[1:]) - 1]

        detail_window = tk.Toplevel(self.root)
        detail_window.title("Details")

        text_widget = tk.Text(detail_window, wrap="word")
        text_widget.pack(expand=True, fill="both")
        text_widget.insert("1.0", text)
        text_widget.config(state="disabled")  # Make it read-only

    def create_context_menu(self):
        """Create a context menu for copying text."""
        self.context_menu = Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Copy", command=self.copy_to_clipboard)
        self.status_table.bind("<Button-3>", self.show_context_menu)

    def show_context_menu(self, event):
        """Show context menu."""
        item = self.status_table.identify_row(event.y)
        if item:
            self.status_table.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)

    def copy_to_clipboard(self):
        """Copy the selected cell text to the clipboard."""
        selected_item = self.status_table.selection()
        if selected_item:
            item = selected_item[0]
            column = self.status_table.identify_column(self.status_table.winfo_pointerx() - self.status_table.winfo_rootx())
            text = self.status_table.item(item, "values")[int(column[1:]) - 1]
            self.root.clipboard_clear()
            self.root.clipboard_append(text)

    def run_test(self):
        """Runs the test logic depending on the selected app."""
        self.log_event("Starting test...")

        # Retrieve values from the GUI
        phone_uuid = self.terminal.get()
        app_name = self.aplikacja.get()
        dzwiek = self.dzwiek.get()
        serwer = self.serwer.get()
        login = self.login.get()
        haslo = self.haslo.get()

        if app_name not in self.app_data:
            self.log_event("Error: Invalid application selected.")
            return

        app_package = self.app_data[app_name]["package"]
        app_activity = self.app_data[app_name]["activity"]

        try:
            # Initialize the Appium driver
            driver = self.initialize_driver(phone_uuid, app_package, app_activity)
            self.log_event(f"Connected to {phone_uuid} running {app_name}.")

            # Execute the start procedure to navigate to the main page
            self.start_procedure(driver, app_name)

            # Enter the monitoring loop
            self.monitor_app_state(driver, app_name)

        except Exception as e:
            self.log_event(f"An error occurred: {str(e)}")
        finally:
            driver.quit()
            self.log_event("Driver quit.")

    def initialize_driver(self, phone_uuid, app_package, app_activity):
        """Initialize the Appium driver."""
        options = UiAutomator2Options()
        options.device_name = phone_uuid
        options.platform_name = "Android"
        options.automation_name = "uiautomator2"
        options.app_activity = app_activity
        options.app_package = app_package
        options.full_reset = False
        options.no_reset = True
        driver = webdriver.Remote("http://localhost:4723", options=options)
        return driver

    def start_procedure(self, driver, app_name):
        """Navigate the app to the main page depending on the app type."""
        self.log_event(f"Starting procedure for {app_name}...")

        if app_name == "Cybertel MCX":
            # Implement the sequence of steps to reach the main page for Cybertel MCX
            self.log_event("Navigating Cybertel MCX to the main page...")
            # Add steps here...

        elif app_name == "MCPTT":
            # Implement the sequence of steps to reach the main page for MCPTT
            self.log_event("Navigating MCPTT to the main page...")
            # Add steps here...

        self.log_event(f"{app_name} is now on the main page.")

    def monitor_app_state(self, driver, app_name):
        """Monitor the app state and perform actions based on element state."""
        self.log_event(f"Monitoring {app_name} state...")

        while True:
            try:
                if app_name == "Cybertel MCX":
                    # Check the relevant element's state in Cybertel MCX
                    self.monitor_cybertel(driver)
                elif app_name == "MCPTT":
                    # Check the relevant element's state in MCPTT
                    self.monitor_mcptt(driver)
                
                # Add a small delay to avoid overwhelming the device
                time.sleep(1)

            except Exception as e:
                self.log_event(f"Error during monitoring: {str(e)}")
                break

    def monitor_cybertel(self, driver):
        """Monitor Cybertel MCX and respond to element state."""
        # Example logic: Check a specific element's state and react
        element = driver.find_element_by_id("com.cybertel.mcx:id/specific_element")
        if element.get_attribute("enabled") == "true":
            self.log_event("Element in Cybertel MCX is enabled. Starting recording...")
            self.start_recording(driver)
        else:
            self.log_event("Element in Cybertel MCX is disabled. Stopping recording...")
            self.stop_recording(driver)
            self.playback_audio(driver)

    def monitor_mcptt(self, driver):
        """Monitor MCPTT and respond to element state."""
        # Example logic: Check a specific element's state and react
        element = driver.find_element_by_id("com.mcptt:id/specific_element")
        if element.get_attribute("enabled") == "true":
            self.log_event("Element in MCPTT is enabled. Starting recording...")
            self.start_recording(driver)
        else:
            self.log_event("Element in MCPTT is disabled. Stopping recording...")
            self.stop_recording(driver)
            self.playback_audio(driver)

    def start_recording(self, driver):
        """Start recording audio."""
        # Implement recording logic here
        self.log_event("Recording started.")

    def stop_recording(self, driver):
        """Stop recording audio."""
        # Implement logic to stop recording
        self.log_event("Recording stopped.")

    def playback_audio(self, driver):
        """Play back the recorded audio."""
        # Implement logic to play back audio
        self.log_event("Playing back audio.")


def main():
    root = ttk.Window(themename="darkly")  # You can change the theme here
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
