import pygame
pygame.init()

from pygame import*
from tkinter import *
from random import *
import tkinter.messagebox


def cammand(args):
    pass


class ScoreBoard():

        def __init__(self, parent):
            self.parent = parent
            self.initGUI()
            self.reset()

        def initGUI(self):
            # Lives
            self.livesVar = IntVar()
            Label(self.parent, text="Lives:", font=("Algerian", 18, "bold")).grid(row=1, column=2, padx=0, pady=80,
                                                                                  sticky=N + W)
            Label(self.parent, textvariable=self.livesVar, font=("Algerian", 18, "bold")).grid(row=1, column=2, padx=50,
                                                                                               pady=130, sticky=N + W)

            # Score
            self.scoreVar = IntVar()
            Label(self.parent, text="Score:", font=("Algerian", 18, "bold")).grid(row=1, column=2, padx=0, pady=200,
                                                                                  sticky=N + W)
            Label(self.parent, textvariable=self.scoreVar, font=("Algerian", 18, "bold")).grid(row=1, column=2, padx=50,
                                                                                               pady=250, sticky=N + W)

            # rules

            Label(self.parent,text="Rules:*",font=("Times new roman",20,"bold",)).grid(row=1,column=2,padx=0,pady=500,sticky=N+W)
            Label(self.parent,text="100 points  eating fruits ",font=("Times new roman",14)).grid(row=1,column=2,padx=50,pady=550,sticky=N+W)
            Label(self.parent,text="No points in other item ",font=("Times new roman ",14)).grid(row=1,column=2,padx=55,pady=600,sticky=N+W)
            # High score
            self.highScoreVar = IntVar()
            Label(self.parent, text="Highest Score:", font=("Algerian", 18, "bold")).grid(row=1, column=2, padx=0,
                                                                                          pady=350, sticky=N + W)
            Label(self.parent, textvariable=self.highScoreVar, font=("Algerian", 18, "bold")).grid(row=1, column=2,
                                                                                                   padx=60, pady=400,
                                                                                                   sticky=N + W)

        def reset(self):
            self.lives = 5
            self.score = 0
            self.highScore = self.loadScore()

            self.livesVar.set(self.lives)
            self.scoreVar.set(self.score)
            self.highScoreVar.set(self.highScore)

        def loadScore(self):
            with open("high-score.txt", "r") as data:
                return int(data.read())

        def saveScore(self):
            if self.score > self.highScore:
                with open("high-score.txt", "w") as data:
                    data.write(str(self.score))

        def gameOver(self):
            self.saveScore()
            tkinter.messagebox.showinfo("Showing Exit Message ?", "Do You want to Continue !")
            if tkinter.messagebox.askyesno("Exit the Game ?", "Play Again ?"):
                self.reset()
            else:
                exit()

        def updateBoard(self, livesStatus, scoreStatus):
            self.lives += livesStatus;
            self.score += scoreStatus
            if self.lives < 0: self.gameOver()
            self.livesVar.set(self.lives);
            self.scoreVar.set(self.score)


class ItemsFallingFromSky():

        def __init__(self, parent, canvas, player, board):
            self.parent = parent  # root form
            self.canvas = canvas  # canvas to display
            self.player = player  # to check touching
            self.board = board  # score board statistics

            self.fallSpeed = 100 # falling speed
            self.xPosition = randint(50, 750)  # random position
            self.isgood = randint(0, 1)  # random goodness

            self.goodItems = ["ananas.gif", "apple.gif", "orange.gif"]
            self.bonusItem="rams.png"
            self.badItems = ["ram.png", "ank.png", "ris.png"]

            # create falling items
            if self.isgood:
                self.itemPhoto = tkinter.PhotoImage(file="images/{}".format(choice(self.goodItems)))
                self.fallItem = self.canvas.create_image((self.xPosition, 50), image=self.itemPhoto, tag="good")
            else:
                self.itemPhoto = tkinter.PhotoImage(file="images/{}".format(choice(self.badItems)))
                self.fallItem = self.canvas.create_image((self.xPosition, 50), image=self.itemPhoto, tag="bad")

            # trigger falling item movement
            self.move_object()

        def move_object(self):
            # dont move x, move y
            self.canvas.move(self.fallItem, 0, 15)

            if (self.check_touching()) or (self.canvas.coords(self.fallItem)[1] > 650):  # [ x0, y0, x1, y1 ]
                self.canvas.delete(self.fallItem)  # delete if out of canvas
            else:
                self.parent.after(self.fallSpeed, self.move_object)  # after some time move object

        def check_touching(self):
            # find current coordinates
            x0, y0 = self.canvas.coords(self.fallItem)
            x1, y1 = x0 + 100, y0 + 50

            #get overlapps
            overlaps = self.canvas.find_overlapping(x0, y0, x1, y1)

            if (self.canvas.gettags(self.fallItem)[0] == "good") and (len(overlaps) > 1) and (
                    self.board.lives >= 0):  # gettags : ("good",)
                self.board.updateBoard(0, 100)  # (lives, score)
                return True  # touching yes

            elif (self.canvas.gettags(self.fallItem)[0] == "bad") and (len(overlaps) > 1) and (
                    self.board.lives >= 0):  # gettags : ("bad",)
                self.board.updateBoard(-1, 0)  # (lives, score)
                return True  # touching yes

            return False  # touching not


class TheGame(ItemsFallingFromSky, ScoreBoard):

        def __init__(self, parent):
            self.parent = parent

            # windows form
            self.parent.geometry("1750x1000")
            self.parent.title("Catch the Fruit ?")

            # canvas window
            self.canvas = Canvas(self.parent, width=1000, height=800)
            self.canvas.config(background="Black")

            self.canvas.bind("<Key>", self.keyMoving)  # take keyboard input as movement
            self.canvas.focus_set()
            self.canvas.grid(row=1, column=1, padx=25, pady=25, sticky=W + N)

            # player character
            self.playerPhoto = tkinter.PhotoImage(file="images/{}".format("rams.png"))
            self.playerChar = self.canvas.create_image((475, 625), image=self.playerPhoto, tag="player")

            # define score board
            self.personalboard = ScoreBoard(self.parent)

            # start poping falling items
            self.createEnemies()

        def keyMoving(self, event):
            if (event.char == "a") and (self.canvas.coords(self.playerChar)[0] > 50):
                self.canvas.move(self.playerChar, -40, 0)
            if (event.char == "d") and (self.canvas.coords(self.playerChar)[0] < 950):
                self.canvas.move(self.playerChar, 80, 0)

        def createEnemies(self):
            ItemsFallingFromSky(self.parent, self.canvas, self.playerChar, self.personalboard)
            self.parent.after(1100, self.createEnemies)
        music=pygame.mixer.Sound("old.wav")
        music.play()
if __name__ == "__main__":
        root = Tk()
        TheGame(root)
        root.mainloop()




