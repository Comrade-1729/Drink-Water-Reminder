'''
    Drink Water Reminder
'''
import os
import threading
import pygame
from plyer import notification

class CustomException(Exception):
    ''' Raise Exception for an invalid Input '''
    def __init__(self, message):
        super().__init__(message)

def notify():
    ''' Function to Send a Notification to the device '''
    # Play custom sound if available
    if os.path.exists("notify.wav"):
        pygame.mixer.music.stop()  # Stop any previously playing sound
        pygame.mixer.music.load("notify.wav")
        pygame.mixer.music.play()
    else:
        print("Warning: Sound file 'notify.wav' not found!")

    # Show notification with icon
    notification.notify(
        title="Water Reminder",
        app_name="Comrade's Water Reminder",
        app_icon="plane.ico" if os.path.exists("plane.ico") else None,
        message="Stay Hydrated! \nDrink a glass of water. \n-> Back to work :)",
        timeout=7  # Duration in seconds
    )

def start_reminders(interval):
    ''' Function to Start Continuous Reminders '''
    while True:
        notify()
        threading.Event().wait(interval)  # Wait for the specified interval

def main():
    ''' Main Function '''
    print("Comrade's\n\tWater\n\t\tReminder!!!")

    # Initialize pygame mixer once at the start
    pygame.mixer.init()
    reminder_thread = None  # To keep track of the reminder thread

    try:
        while True:
            t2 = input("Enter 1 for Duration in 'Hours'\nEnter 2 for Duration in 'Minutes'\nEnter 3 for Duration in 'Seconds'\nEnter 0 to exit: ")
            if t2 == '0':
                print("Thanks For Using Comrade's Water Reminder program.\nStay Hydrated :)")
                break

            t1 = input("Enter time Duration for your Reminder: ")

            # Validate inputs
            if t1.isdigit() and t2.isdigit():
                t1 = int(t1)
                if t2 == '1':
                    time0 = t1 * 60 * 60
                elif t2 == '2':
                    time0 = t1 * 60
                elif t2 == '3':
                    time0 = t1
                else:
                    print("Invalid choice. Please try again.")
                    continue
            else:
                raise CustomException("Exception! Not an integer input.")

            # Stop any existing reminder thread before starting a new one
            if reminder_thread and reminder_thread.is_alive():
                print("Stopping the existing reminder...")
                reminder_thread.join(timeout=1)  # Allow time for the thread to stop

            # Start the reminder thread with the calculated time in seconds
            reminder_thread = threading.Thread(target=start_reminders, args=(time0,), daemon=True)
            reminder_thread.start()
            print(f"Reminder set successfully! You will be reminded every {time0} seconds.")

    except CustomException as e:
        print(e)

    finally:
        # Stop the reminder thread on exit
        if reminder_thread and reminder_thread.is_alive():
            reminder_thread.join(timeout=1)
        pygame.mixer.quit()  # Close the mixer

if __name__ == '__main__':
    main()
