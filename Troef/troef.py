from random import shuffle
import numpy as np
from tkinter import *
from PIL import ImageTk, Image
import csv


suits = ["SPADES","DIAMONDS","CLUBS","HEARTS"]
class troefPicker():
    cards = []

    csvfile = None

    writer = None

    win = None

    s = []

    def cardsToCsv(self,chosenSuit):
        row = []
        for card in self.s:
            row.append(card["suit"]*8+card["value"])
        row.append(suits[chosenSuit])
        print(row)
        self.writer.writerow(row)
        self.win.destroy()

    def SpadesCallback(self):
        self.cardsToCsv(0)

    def HeartsCallback(self):
        self.cardsToCsv(3)

    def ClubsCallback(self):
        self.cardsToCsv(2)

    def DiamondsCallback(self):
        self.cardsToCsv(1)

    def initCSV(self):
        self.csvfile = open("troef.csv","a+",newline='')
        self.writer = csv.writer(self.csvfile, delimiter=',') 

    def exitCSV(self):
        self.csvfile.close()
    
    def shuffle(self):
        self.cards = []
        for suit in range(0,4):
            for value in range(0,8):
                if value == 7:
                    rank = 10
                elif value == 6:
                    rank = 1
                elif value > 2:
                    rank = value + 8
                else:
                    rank = value + 7
                self.cards.append({"suit": suit, "value": value, "rank": rank})

        shuffle(self.cards)



    def update(self,i):
        self.win = Tk()
        self.win.geometry("1200x500")
        self.win.configure(background='black')
        self.s = sorted(self.cards[8*i:8*i+8],key=lambda x: 13*x["suit"]+x["value"])
        images = 8*[0]
        frame = Frame(self.win,width=1200,height=220,background="black")
        for i,card in enumerate(self.s):
            images[i] = ImageTk.PhotoImage(Image.open(f"Sprites/Cards/{card['rank']}{suits[card['suit']]}.png").resize((98,152),Image.ANTIALIAS))

            label = Label(frame,image = images[i])
            label.place(x=110*i,y=0)

        frame.pack(side=TOP)

        spadesImage = ImageTk.PhotoImage(Image.open(f"Sprites/SPADES.png"))
        Spades = Button(self.win, image=spadesImage,text ="SPADES", command = self.SpadesCallback)
        Spades.pack(side=LEFT)

        diamondsImage = ImageTk.PhotoImage(Image.open(f"Sprites/DIAMONDS.png"))
        Diamonds = Button(self.win,  image=diamondsImage,text ="DIAMONDS", command = self.DiamondsCallback)
        Diamonds.pack(side=LEFT)

        clubsImage = ImageTk.PhotoImage(Image.open(f"Sprites/CLUBS.png"))
        Clubs = Button(self.win,  image=clubsImage,text ="CLUBS", command = self.ClubsCallback)
        Clubs.pack(side=LEFT)

        heartsImage = ImageTk.PhotoImage(Image.open(f"Sprites/HEARTS.png"))
        Hearts = Button(self.win, image=heartsImage, text ="HEARTS", command = self.HeartsCallback)
        Hearts.pack(side=LEFT)

        self.win.mainloop()
        
tp = troefPicker()
tp.initCSV()
tp.shuffle()
tp.update(0)
tp.update(1)
tp.update(2)
tp.update(3)
tp.exitCSV()


