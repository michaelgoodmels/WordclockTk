# Creates a Tkinter application that shows the current time as a word wall
# For more information see: https://www.hashbangcode.com/article/creating-word-clock-python-and-tkinter
#
#   0123456789ABC
# 0 ITRISUHALFTEN
# 1 QUARTERTWENTY
# 2 FIVEQMINUTEST
# 3 PASTMTOSAMOPM
# 4 ONENTWOZTHREE
# 5 FOURFIVESEVEN
# 6 SIXEIGHTYNINE
# 7 TENELEVENPHIL
# 8 TWELVELOCLOCK


import tkinter as tk
import time

class SentenceClock(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Michael's Wordclock with Tk")

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
                ["","","","","","z'","B","L","Z","R","S"],
                ["","","","","","","","","","",""],
                ["","","",".",".",".",".",".","","",""],
        ]

        self.labels = {}

        for i in range(0, len(self.letters)):
            for j in range(0, len(self.letters[i])):
                self.labels['label_' + str(i) + '_' + str(j)] = tk.Label(self, fg="light grey", text=self.letters[i][j], font="Helvetica 16")
                self.labels['label_' + str(i) + '_' + str(j)].grid(column=j, row=i)

        self.after(1000, self.update_time)

    def update_time(self):
        for i in range(0, len(self.letters)):
            for j in range(0, len(self.letters[i])):
                self.labels['label_' + str(i) + '_' + str(j)].config(fg="light grey", font="Helvetica 16")

        current_time = time.localtime()

        hour = int(time.strftime("%I", current_time))
        minute = int(time.strftime("%M", current_time))
        am_or_pm = time.strftime("%p", current_time)

        letters = self.translate_time(hour, minute, am_or_pm)

        for letter in letters:
            self.labels['label_' + str(letter[0]) + '_' + str(letter[1])].config(fg="royal blue", font="Helvetica 16 bold")

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
                [[2,0],[2,1],[2,2],[2,3],[2,5],[2,6],[2,7],[2,8],[2,9],[2,10],[2,11]], # FÜF
                [[0,10],[0,11],[0,12],[2,5],[2,6],[2,7],[2,8],[2,9],[2,10],[2,11]], # ZEH
                [[0,7],[1,0],[1,1],[1,2],[1,3],[1,4],[1,5],[1,6]], # E VIERTEL
                [[1,7],[1,8],[1,9],[1,10],[1,11],[1,12],[2,5],[2,6],[2,7],[2,8],[2,9],[2,10],[2,11]], # ZWINZG
                [[1,7],[1,8],[1,9],[1,10],[1,11],[1,12],[2,0],[2,1],[2,2],[2,3],[2,5],[2,6],[2,7],[2,8],[2,9],[2,10],[2,11]], # FÜFEZWINZG
                [[5,4],[6,4],[7,4],[8,4],[9,4]], # HALBI
            ]
            mapped_minute_value = round((0 + (5 - 0) * ((minute - 3) / (28 - 3))) - 0.4)
            minute_name = minute_blocks[mapped_minute_value]
        else:
            minute_name = ''
        return minute_name

    def translate_hour(self, hour, minute):
        hours = [
            [[4,0],[4,1],[4,2]], #EIS
            [[4,4],[4,5],[4,6]], # ZWEI
            [[4,8],[4,9],[4,10],[4,11]], # DRÜ
            [[5,0],[5,1],[5,2],[5,3]], # VIER
            [[5,4],[5,5],[5,6],[5,7]], # FÜFI
            [[6,0],[6,1],[6,2]], # SIX
            [[5,8],[5,9],[5,10],[5,11],[5,12]], # SIBNI
            [[6,3],[6,4],[6,5],[6,6],[6,7]], # ACHTI
            [[6,9],[6,10],[6,11],[6,12]], # NÜNI
            [[7,0],[7,1],[7,2]], # ZEHNI
            [[7,3],[7,4],[7,5],[7,6],[7,7],[7,8]], # ÖLFI
            [[8,0],[8,1],[8,2],[8,3],[8,4],[8,5]], # ZWÖLFI
            [[4,0],[4,1],[4,2]], #EIS
        ]
        if minute > 33:
            return hours[hour]
        else:
            return hours[hour - 1]

    def translate_time(self, hour, minute, am_or_pm):
        letters = [
            [0,0], [0,1], [0,3], [0,4], [0,5], [0,6]# ES ISCH
        ]

        letters.extend(self.translate_hour(hour, minute))
        letters.extend(self.translate_to_or_past(minute))
        letters.extend(self.translate_minute(minute))

        if (am_or_pm == 'PM'):
            letters.extend([[3,11],[3,12]]) # PM
        else:
            letters.extend([[3,8],[3,9]]) # AM

        if (0 <= minute < 3) or (57 < minute <= 60):
            letters.extend([[8,7],[8,8],[8,9],[8,10],[8,11],[8,12]]) # Z' BALZERS

        return letters

if __name__ == "__main__":
    sentence_clock = SentenceClock()
    sentence_clock.mainloop()