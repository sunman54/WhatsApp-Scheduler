import tkinter as tk
from time import sleep
import pyautogui
import pyperclip
import platform
import datetime
import threading


class WhatsAppSchedulerApp:

    def __init__(self, root):
        self.root = root
        self.root.title("WhatsApp Scheduler")
        self.root.geometry("400x500")  
        self.hour_label = tk.Label(root, text="Saat:")
        self.hour_label.pack()

        self.hour_entry = tk.Entry(root)
        self.hour_entry.pack()

        self.minute_label = tk.Label(root, text="Dakika:")
        self.minute_label.pack()

        self.minute_entry = tk.Entry(root)
        self.minute_entry.pack()

        self.message_label = tk.Label(root, text="Mesaj:")
        self.message_label.pack()

        self.message_entry = tk.Entry(root)
        self.message_entry.pack()

        self.conversation_label = tk.Label(root, text="Konuşma Seçimi:")
        self.conversation_label.pack()

        self.conversation_var = tk.StringVar(root)
        self.conversation_var.set("2") 
        self.conversation_radiobutton_1 = tk.Radiobutton(root, text="1. Sabitlenen Kişi", variable=self.conversation_var, value="1")
        self.conversation_radiobutton_1.pack()

        self.conversation_radiobutton_2 = tk.Radiobutton(root, text="2. Sabitlenen Kişi", variable=self.conversation_var, value="2")
        self.conversation_radiobutton_2.pack()

        self.conversation_radiobutton_3 = tk.Radiobutton(root, text="3. Sabitlenen Kişi", variable=self.conversation_var, value="3")
        self.conversation_radiobutton_3.pack()

        self.start_button = tk.Button(root, text="Başlat", command=self.start_schedule)
        self.start_button.pack()

        self.remaining_time_label = tk.Label(root, text="")
        self.remaining_time_label.pack()


    def update_remaining_time(self, remaining_seconds):
        minutes = remaining_seconds // 60
        seconds = remaining_seconds % 60
        self.remaining_time_label["text"] = f"Kalan Süre: {minutes} dk {seconds} sn"

    def type(self, text: str):
        pyperclip.copy(text)
        if platform.system() == "Darwin":
            pyautogui.hotkey("command", "v")
        else:
            pyautogui.hotkey("ctrl", "v")
    def start_schedule(self):
        try:
            given_hour = int(self.hour_entry.get())
            given_minute = int(self.minute_entry.get())
            message = self.message_entry.get()
            selected_conversation = int(self.conversation_var.get()) 

            self.start_button["state"] = "disabled"  
            schedule_thread = threading.Thread(target=self.send_message,
                                               args=(given_hour, given_minute, message, selected_conversation))
            schedule_thread.start()
        except ValueError:
            print("Geçerli bir saat, dakika ve mesaj girin.")


    def send_message(self, given_hour, given_minute, message, selected_conversation):
        conversation_positions = {
            1: (150, 200),
            2: (150, 270),
            3: (150, 340)
        }
        whatsapp_input = pyautogui.Point(x=666, y=1023)

        while True:
            now = datetime.datetime.now()
            hour = now.hour
            minute = now.minute
            second = now.second
            if hour == given_hour and minute == given_minute:
                print('Zaman geldi!')
                pyautogui.press('win') 
                sleep(1)
                pyautogui.write('WhatsApp')  
                pyautogui.press('enter')
                sleep(3)
                pyautogui.click(*conversation_positions[selected_conversation])
                sleep(0.5)
                pyautogui.click(whatsapp_input)
                sleep(0.2)
                self.type(message)
                sleep(0.2)
                pyautogui.press('enter')
                break
            else:
                remaining_seconds = (given_hour - hour) * 3600 + (given_minute - minute) * 60 - second
                self.update_remaining_time(remaining_seconds)
                print('Hala bekleniyor...')
                print("Saat:", hour, '\tDakika:', minute, '\tSaniye:', second)
                #sleep(30)
                #pyautogui.click(1, 1)


if __name__ == "__main__":
    root = tk.Tk()
    app = WhatsAppSchedulerApp(root)
    root.mainloop()
