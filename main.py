import threading
import pyautogui
import random
import numpy as np
import os
import tkinter as tk

from interface import BotInterfaceBuilder
from ttkthemes import ThemedTk # type: ignore
from find_images import locateImage

bot_is_running = False

# Function to generate a random delay
def randDelay():
    return random.uniform(0.2, 0.5)

# Function to generate a random number of presses
def randTime():
    return random.randint(3, 7)

# Function to generate a random sleep time
def randSleep():
    return random.randint(10, 15)


class BotThread:
    def __init__(self):
        self.box = None
        self.thread = None
        self.is_running = False
        self.root = self.startRootInterface()
        self.image_detected = False
        self.times_runned = 0
        self.interface = BotInterfaceBuilder
        self.image_was_detected = False
        self.running_in = 0
        self.running_time = 0

    def startRootInterface(self):
        return ThemedTk(theme="arc", themebg=True)

    def buildInterface(self): 
            self.root.title("Revolution Bot")
            self.root.geometry("400x200+250+250")
            self.root.resizable(False, False)
            self.interface.build(self)


    def run(self):
            self.buildInterface()
            self.root.mainloop()

    def detectImage(self):
        print("Detecting image")
        self.box = locateImage('./01.png')
        if self.box is not None:
            self.image_was_detected = True
            self.interface.unlock_interface(self.interface, self)
            self.interface.label_info(self)

    def start(self):
        if self.box is None:
            print("No image detected, impossible to start the bot")
            return
        
        if self.is_running:
            print("Bot is already running!")
            return
        self.is_running = True
        self.interface.count_running__time(self.interface, self)
        self.thread = threading.Thread(target=self.runClickBot)
        self.interface.label_info(self)
        self.thread.start()

    def stop(self):
        print('Stopping bot')
        self.is_running = False
        self.interface.label_info(self)
        self.thread = None


    def exit(self):
        print('Exiting bot')
        self.thread = None
        self.is_running = False
        self.root.destroy()

    def updateTimesRunned(self):
        self.times_runned += 1
        self.interface.unlocked_interfaces.label_times_runned(self)

    def resetTimesRunned(self):
        self.times_runned = 0
        self.running_time = 0
        self.interface.unlocked_interfaces.label_times_runned(self)
        self.interface.unlocked_interfaces.label_running_in(self)

    def updateRunningIn(self, seconds):
        self.running_in = seconds
        self.interface.unlocked_interfaces.label_running_in(self)

    def runClickBot(self):
        placeToMove = self.box
        print("Starting the script")
        while self.is_running:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"(RUN NUMBER: {self.times_runned})")
            actual_position = pyautogui.position()
            print("---Moving to the point---")
            pyautogui.moveTo(placeToMove[0]- (placeToMove[1]*0.1), placeToMove[1], duration=0.3)
            pyautogui.click()

            # Press 'a' key randomly
            print("Pressing ascension button")
            ascentionConfig = {"presses": randTime(), "interval": randDelay()}
            print(ascentionConfig)
            pyautogui.press('a', presses=ascentionConfig["presses"], interval=ascentionConfig["interval"])
            pyautogui.sleep(0.2)

            # Press 'b' key randomly
            print("Pressing buy button")
            buyConfig = {"presses": randTime(), "interval": randDelay()}
            print(buyConfig)
            pyautogui.press('b', presses=buyConfig["presses"], interval=buyConfig["interval"])

            # Move back to original position
            print("Moving back to the original position")
            pyautogui.moveTo(actual_position, duration=0.3)
            
            # Random sleep between actions
            sleepTime = randSleep()
            self.updateRunningIn(sleepTime)
            self.updateTimesRunned()
            print(f"Sleeping for {sleepTime} seconds")
            pyautogui.sleep(sleepTime)
            print("---Looping again---")


def main():
    bot = BotThread()
    bot.run()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
