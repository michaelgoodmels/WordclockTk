import customtkinter as ctk
import time
from datetime import datetime

class WordClock(ctk.CTk):

    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode('dark')
        ctk.set_default_color_theme('green')

        self.title("Michael's Wordclock with customTkinter")
        self.geometry("340x700")  # Adjusted height to accommodate digital clock
        self.configure(fg_color="black")

        self.letters = [
            ["E","S","","I","S","C","H","","F","Ü","F"],
            ["Z","E","H","","V","I","E","R","T","E","L"],
            ["Z","W","I","N","Z","G","","V","O","R",""],
            ["A","B","","","H","A","L","B","I","",""],
            ["E","I","S","Z","W","E","I","","D","R","Ü"],
            ["V","I","E","R","I","","","F","Ü","F","I"],
            ["S","E","C","H","S","I","S","I","B","N","I"],
            ["A","C","H","T","I","","","N","Ü","N","I"],
            ["Z","E","H","N","I","","","Ö","L","F","I"],
            ["Z","W","Ö","L","F","I","","","","",""],
            ["","","","","","z","'","M","E","L","S"],
            ["","","","","","","","","","",""],
            ["","","",".",".",".",".",".","","",""]
        ]

        self.labels = {}

        for i in range(0, len(self.letters)):
            for j in range(0, len(self.letters[i])):
                self.labels['label_' + str(i) + '_' + str(j)] = ctk.CTkLabel(self, text=self.letters[i][j],
                                                                             fg_color="black",
                                                                             text_color="light grey",
                                                                             font=('Helvetica', 36))
                self.labels['label_' + str(i) + '_' + str(j)].grid(column=j, row=i)

        # Add a label for the digital clock below the word clock
        self.digital_clock_label = ctk.CTkLabel(self, text="", font=('Helvetica', 32), text_color="light blue")
        self.digital_clock_label.grid(column=0, row=len(self.letters), columnspan=len(self.letters[0]), pady=(20, 0))

        self.after(1000, self.update_time)

    def update_time(self):
        current_time = time.localtime()
        hour = int(time.strftime("%I", current_time))
        minute = int(time.strftime("%M", current_time))
        second = int(time.strftime("%S", current_time))
        am_or_pm = time.strftime("%p", current_time)

        letters = self.translate_time(hour, minute, am_or_pm)

        # Get the current color of the digital clock
        digital_clock_color = self.digital_clock_label.cget("text_color")

        for i in range(0, len(self.letters)):
            for j in range(0, len(self.letters[i])):
                label_key = 'label_' + str(i) + '_' + str(j)
                if label_key in self.labels:
                    self.labels[label_key].configure(fg_color="black", text_color="light grey", font=('Helvetica', 36))

        for letter in letters:
            label_key = 'label_' + str(letter[0]) + '_' + str(letter[1])
            if label_key in self.labels:
                self.labels[label_key].configure(fg_color="black", text_color=digital_clock_color, font=('Helvetica', 36, "bold"))

        # Update the digital clock
        digital_time = time.strftime("%H:%M:%S")
        self.digital_clock_label.configure(text=digital_time)

        # Update seconds indicators
        for i in range(4, 8):
            label_key = 'label_12_' + str(i)
            if label_key in self.labels:
                if second % 60 >= (i - 4) * 15 and second % 60 < (i - 3) * 15:
                    self.labels[label_key].configure(fg_color=digital_clock_color)
                else:
                    self.labels[label_key].configure(fg_color="black")

        self.after(1000, self.update_time)

    def translate_to_or_past(self, minute):
        to_or_past = []
        if 3 <= minute < 33:
            to_or_past = [[3,0],[3,1],[3,2],[3,3]] # AB
        elif 33 <= minute <= 57:
            to_or_past = [[3,5],[3,6]] # VOR
        return to_or_past

    def translate_minute(self, minute):
        if (minute > 30):
            minute = 60 - minute

        if minute >= 3:
            minute_blocks = [
                [[0,8],[0,9],[0,10]], # FÜF
                [[1,0],[1,1],[1,2]], # ZEH
                [[1,4],[1,5],[1,6],[1,7]], # VIERTEL
                [[2,0],[2,1],[2,2],[2,3]], # ZWINZIG
                [[3,4],[3,5],[3,6],[3,7],[3,8]], # HALBI
            ]
            mapped_minute_value = min(int((minute - 3) / 5), len(minute_blocks) - 1)
            minute_name = minute_blocks[mapped_minute_value]
        else:
            minute_name = []
        return minute_name

    def translate_hour(self, hour, minute):
        hours = [
            [[4,0],[4,1],[4,2]], # EIS
            [[4,4],[4,5],[4,6]], # ZWEI
            [[4,8],[4,9],[4,10]], # DRÜ
            [[5,0],[5,1],[5,2],[5,3]], # VIER
            [[5,4],[5,5],[5,6],[5,7]], # FÜFI
            [[6,0],[6,1],[6,2],[6,3]], # SECHSI
            [[6,4],[6,5],[6,6],[6,7]], # SIBNI
            [[7,0],[7,1],[7,2],[7,3]], # ACHTI
            [[7,4],[7,5],[7,6],[7,7]], # NÜNI
            [[8,0],[8,1],[8,2],[8,3]], # ZEHNI
            [[8,5],[8,6],[8,7]], # ÖLFI
            [[9,0],[9,1],[9,2],[9,3]], # ZWÖLFI
        ]
        if minute >= 33:
            hour = (hour % 12) + 1
        return hours[(hour - 1) % 12]

    def translate_time(self, hour, minute, am_or_pm):
        letters = [[0,0], [0,1], [0,3], [0,4], [0,5], [0,6]]  # ES ISCH
        letters.extend(self.translate_to_or_past(minute))
        letters.extend(self.translate_hour(hour, minute))
        letters.extend(self.translate_minute(minute))
        return letters

if __name__ == "__main__":
    MyWordClock = WordClock()
    MyWordClock.mainloop()