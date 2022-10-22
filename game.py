# Window size: 1600x900


import os
from tkinter import *
from tkinter import Tk, Canvas
from tkinter import PhotoImage as img
import random
import time
import threading

cwd = os.getcwd()
# print(cwd)

direction = "top"
width = w = 1600
height = h = 900
window = Tk()
window.title("Art Of The Blade")
ws = window.winfo_screenwidth()
hs = window.winfo_screenheight()
x = (ws / 2) - (w / 2)
y = (hs / 2) - (h / 2)
window.geometry('%dx%d+%d+%d' % (w, h, x, y))

menu_frame = LabelFrame(window, height=900, width=1600, relief=FLAT, background="black", highlightbackground="black", borderwidth=0, highlightthickness=0)
menu_frame.pack_propagate(0)
menu_frame.place(x=0, y=0)

bg = img(file=cwd+"/sprites/menubg.png")
lb = Label(menu_frame, image=bg)
lb.place(x=0, y=0)

namelab = Label(menu_frame, text="Enter Player Name", font=("Helvetica", 20)).place(x=120, y=260)
name = Entry(menu_frame, width=16, font=("Helvetica", 32))
name.place(x=120, y=200, height=60)

boss1 = img(file=cwd+"/sprites/boss1.png")
boss1lb = Label(menu_frame, image=boss1)
boss1lb.place(x=0, y=0)
boss1lb.lower()



game_frame = LabelFrame(window, height=900, width=1600, relief=FLAT, background="black", highlightbackground="black",
                        borderwidth=0, highlightthickness=0)
game_frame.pack_propagate(0)
game_frame.place(x=0, y=0)
game_frame.lower()

gamebg = img(file=cwd+"/sprites/gamebg3.png")
gameoverpng = img(file=cwd+"/sprites/Gameover.png")

gameover_frame = LabelFrame(window, height=900, width=1600, relief=FLAT, background="black",
                            highlightbackground="black", borderwidth=0, highlightthickness=0)
gameoverimg = Label(gameover_frame, image=gameoverpng)
gameoverimg.place(x=0, y=0)
gameover_frame.pack_propagate(0)
gameover_frame.place(x=0, y=0)
gameover_frame.lower()

canvas = Canvas(game_frame, bg="black", width=width, height=height)
canvas.create_rectangle(720, 0, 880, 900, fill="grey", outline="red")
canvas.create_rectangle(0, 370, 1600, 530, fill="grey", outline="red")
canvas.create_image(800, 460, image=gamebg)

playerup = img(file=cwd+"/sprites/top.png")
playerdown = img(file=cwd+"/sprites/bottom.png")
playerleft = img(file=cwd+"/sprites/left.png")
playerright = img(file=cwd+"/sprites/right.png")

dmgtop = img(file=cwd+"/sprites/dmgtop.png")
dmgbot = img(file=cwd+"/sprites/dmgbottom.png")
dmgleft = img(file=cwd+"/sprites/dmgleft.png")
dmgright = img(file=cwd+"/sprites/dmgright.png")

enemyup = img(file=cwd+"/sprites/entop.png")
enemydown = img(file=cwd+"/sprites/enbottom.png")
enemyleft = img(file=cwd+"/sprites/enleft.png")
enemyright = img(file=cwd+"/sprites/enright.png")

boss = img(file=cwd+"/sprites/boss.png")

pausebg = img(file=cwd+"/sprites/pause.png")

player = canvas.create_image(800, 450, image=playerup)
canvas.create_rectangle(width / 2 + 500, 5, width / 2 + 790, 120, fill="black")

score = 0
txt = "Score:" + str(score)
scoreText = canvas.create_text(width / 2 + 630, 30, fill="white", font="Comic 36 ", text=txt)

lives = 5
lv = "Lives:" + str(lives)
lvText = canvas.create_text(width / 2 + 630, 90, fill="white", font="Comic 36 ", text=lv)

canvas.pack()


class Enemy:
    def __init__(self, canvas, x, y, xvel, yvel, img, tag):
        self.canvas = canvas
        self.image = canvas.create_image(x, y, image=img, tag=tag)
        self.xvel = xvel
        self.yvel = yvel
        self.coords = self.canvas.bbox(self.image)

    def move(self):
        self.coords = self.canvas.bbox(self.image)
        coords = self.canvas.coords(self.image)
        self.canvas.move(self.image, self.xvel, self.yvel)
        time.sleep(0.03)
        window.update()

    def overlapping(self, b=canvas.bbox(player)):
        if self.coords[0] < b[2] and self.coords[2] > b[0] and self.coords[1] < b[3] and self.coords[3] > b[1]:
            return True

    def delete(self):
        self.canvas.delete(self.image)
        time.sleep(0.1)
        window.update()


pause_frame = LabelFrame(window, height=900, width=1600, relief=FLAT, background="black", highlightbackground="black",
                         borderwidth=0, highlightthickness=0)
pauseimg = Label(pause_frame, image=pausebg)
pauseimg.place(x=0, y=0)
pause_frame.pack_propagate(0)
pause_frame.place(x=0, y=0)
pause_frame.lower()

gO = 0
state = 0


def checkpause(event):
    pauseaction()


def pauseaction():
    global state
    global gO
    if state == 0:
        state = 1
        # print("pause")
        pause_frame.lift()
    elif state == 1:
        state = 0
       # print("unpause")
        pause_frame.lower()


unpausepause = Button(pause_frame, text="Continue", command=pauseaction, font=("Helvetica", 62), width=10).place(x=200,
                                                                                                                 y=600)


def leftKey(event):
    global direction, player, state
    if state == 0:
        direction = "left"
        canvas.itemconfigure(player, image=playerleft)
        canvas.pack()


def rightKey(event):
    global direction, player, state
    if state == 0:
        direction = "right"
        canvas.itemconfigure(player, image=playerright)
        canvas.pack()


def upKey(event):
    global direction, player, state
    if state == 0:
        direction = "top"
        canvas.itemconfigure(player, image=playerup)
        canvas.pack()


def downKey(event):
    global direction, player, state
    if state == 0:
        direction = "bottom"
        canvas.itemconfigure(player, image=playerdown)
        canvas.pack()


bossstate = 0


def checkboss(event):
    global bossstate, state, boss1lb
    if bossstate == 0:
        canvas.create_image(800, 450, image=boss, tag="bosskey")
        boss1lb.lift()
        state = 1
        bossstate = 1
    elif bossstate == 1:
        canvas.delete("bosskey")
        boss1lb.lower()
        state = 0
        bossstate = 0


konami = False


def Konami(event):
    konamicheat()


def konamicheat():
    global konami
    if not konami:
        konami = True
    else:
        konami = False


def scorecheat():
    global score
    score += 1000
    txt = "Score:" + str(score)
    canvas.itemconfigure(scoreText, text=txt)


def cheat_score(event):
    scorecheat()


def lifecheat():
    global lives
    lives += 10
    lv = "Lives:" + str(lives)
    canvas.itemconfigure(lvText, text=lv)


def cheat_lives(event):
    lifecheat()


def damage():
    global direction, lives
    if direction == "top":
        lives -= 1
        lv = "Lives:" + str(lives)
        canvas.itemconfigure(player, image=dmgtop)
        canvas.itemconfigure(lvText, text=lv)
        time.sleep(0.2)
        canvas.itemconfigure(player, image=playerup)
    elif direction == "bottom":
        lives -= 1
        lv = "Lives:" + str(lives)
        canvas.itemconfigure(player, image=dmgbot)
        canvas.itemconfigure(lvText, text=lv)
        time.sleep(0.2)
        canvas.itemconfigure(player, image=playerdown)
    elif direction == "left":
        lives -= 1
        lv = "Lives:" + str(lives)
        canvas.itemconfigure(player, image=dmgleft)
        canvas.itemconfigure(lvText, text=lv)
        time.sleep(0.2)
        canvas.itemconfigure(player, image=playerleft)
    elif direction == "right":
        lives -= 1
        lv = "Lives:" + str(lives)
        canvas.itemconfigure(player, image=dmgright)
        canvas.itemconfigure(lvText, text=lv)
        time.sleep(0.2)
        canvas.itemconfigure(player, image=playerright)


def checkdirection(dir):
    if dir == "left":
        canvas.itemconfigure(player, image=playerleft)
    elif dir == "right":
        canvas.itemconfigure(player, image=playerright)
    elif dir == "top":
        canvas.itemconfigure(player, image=playerup)
    elif dir == "bottom":
        canvas.itemconfigure(player, image=playerdown)


canvas.bind("<Left>", leftKey)
canvas.bind("<Right>", rightKey)
canvas.bind("<Up>", upKey)
canvas.bind("<Down>", downKey)
canvas.bind("p", checkpause)
canvas.bind("<Escape>", checkpause)
canvas.bind("<Up><Up><Down><Down><Left><Right><Left><Right><b><a>", Konami)
canvas.bind("<s><c><o><r><e>", cheat_score)
canvas.bind("<l><i><f><e>", cheat_lives)
canvas.bind("<Control-b>", checkboss)
canvas.focus_set()

score = 0


def gameover():
    global score
    scrlab = Label(gameover_frame, text="Score :" + str(score), font=("Helvetica", 60), width=10, bg="black",
                   fg="white").place(x=620, y=400)
    gameover_frame.lift()


def main(enem, dir, extent):
    gO = False
    global score, lives, state, konami
    col = False
    while True and not col:
        if enem.overlapping():
            if not konami:
                if direction == dir:
                    score += 10
                    txt = "Score:" + str(score)
                    canvas.itemconfigure(scoreText, text=txt)
                    a = canvas.create_arc(710, 360, 890, 540, outline="white", extent=60, width=1.5, style="arc",
                                          start=extent)
                    time.sleep(0.1)
                    enem.delete()
                    time.sleep(0.1)
                    canvas.delete(a)
                elif direction != dir:
                    damage()
                    enem.delete()
                col = True
            elif konami:
                if enem.overlapping():
                    score += 10
                    txt = "Score:" + str(score)
                    canvas.itemconfigure(scoreText, text=txt)
                    checkdirection(dir)
                    a = canvas.create_arc(710, 360, 890, 540, outline="#e8d956", extent=60, width=1.5, style="arc",
                                          start=extent)
                    time.sleep(0.1)
                    enem.delete()
                    time.sleep(0.1)
                    canvas.delete(a)
                    col = True
        elif state != 1:
            enem.move()
        if lives > 0 and not gO:
            window.update()
        elif lives == 0:
            enem.delete()
            gO = True
            gameover()
    if not gO:
        attack()


def attack():
    atkdir = random.randint(1, 4)
    if atkdir == 1:
        en1 = Enemy(canvas, 20, 450, 5, 0, enemyleft, "rect1")
        main(en1, "left", 160)
    elif atkdir == 2:
        en2 = Enemy(canvas, 1500, 450, -5, 0, enemyright, "rect2")
        main(en2, "right", 340)
    elif atkdir == 3:
        en3 = Enemy(canvas, 790, 30, 0, 5, enemyup, "rect3")
        main(en3, "top", 70)
    elif atkdir == 4:
        en4 = Enemy(canvas, 790, 800, 0, -5, enemydown, "rect4")
        main(en4, "bottom", 250)


def delay():
    time.sleep(3)
    attack()


def start(a=5,b=0):
    global lives, score
    lives = a
    lv = "Lives:" + str(lives)
    canvas.itemconfigure(lvText, text=lv)
    score = b
    txt = "Score:" + str(score)
    canvas.itemconfigure(scoreText, text=txt)
    for x in range(0, 4):
        t = threading.Timer(x, delay).start()




# frames==================================

# cheats
frame = LabelFrame(menu_frame, background="black", highlightbackground="black", height=800, width=700, relief=FLAT)
frame.pack_propagate(0)
frame.place(x=850, y=50)
frame.lower()

# controls
frame2 = LabelFrame(menu_frame, background="black", highlightbackground="black", height=800, width=700, relief=FLAT)
frame2.pack_propagate(0)
frame2.place(x=850, y=50)
frame2.lower()

# leaderboard
frame3 = LabelFrame(menu_frame, background="black", highlightbackground="black", height=800, width=700, relief=FLAT)
frame3.pack_propagate(0)
frame3.place(x=850, y=50)
frame3.lower()

# howtoplay
frame4 = LabelFrame(menu_frame, background="black", highlightbackground="black", height=800, width=700, relief=FLAT)
frame4.pack_propagate(0)
frame4.place(x=850, y=50)
frame4.lower()
#===========================================

def savebutton():
    up = entryup.get()
    down = entrydw.get()
    left = entryle.get()
    right = entryri.get()
    if up != "":
        upk = "<" + up + ">"
        canvas.unbind("<Up>")
        canvas.bind(upk, upKey)
    if down != "":
        downk = "<" + down + ">"
        canvas.unbind("<Down>")
        canvas.bind(downk, downKey)
    if left != "":
        leftk = "<" + left + ">"
        canvas.unbind("<Left>")
        canvas.bind(leftk, leftKey)
    if right != "":
        rightk = "<" + right + ">"
        canvas.unbind("<Right>")
        canvas.bind(rightk, rightKey)
    canvas.focus_set()





labelRe = Label(frame2, text="ReBindings", bg="black", fg="white", font=("Helvetica", 32))
labelRe.place(x=150, y=400)

savebut = Button(frame2, text="Save", bg="white", fg="black", font=("Helvetica", 32), padx=5, command=savebutton)
savebut.place(x=450, y=400)

labelup = Label(frame2, text="Up Action", bg="black", fg="white", font=("Helvetica", 32))
labelup.place(x=100, y=500)

entryup = Entry(frame2, width=10)
entryup.place(x=120, y=550)

labeldw = Label(frame2, text="Down Action", bg="black", fg="white", font=("Helvetica", 32))
labeldw.place(x=400, y=500)

entrydw = Entry(frame2, width=10)
entrydw.place(x=440, y=550)

labelle = Label(frame2, text="Left Action", bg="black", fg="white", font=("Helvetica", 32))
labelle.place(x=100, y=620)

entryle = Entry(frame2, width=10)
entryle.place(x=120, y=670)

labelri = Label(frame2, text="Right Action", bg="black", fg="white", font=("Helvetica", 32))
labelri.place(x=400, y=620)

entryri = Entry(frame2, width=10)
entryri.place(x=440, y=670)



cheattext = Text(frame, height=20, width=40, padx=20, pady=20, bg="black", fg="white", relief=FLAT,
                 highlightbackground="black", font=("Helvetica", 32))
cheattext.pack()

controltext = Text(frame2, height=10, width=40, padx=20, pady=20, bg="black", fg="white", relief=FLAT,
                   highlightbackground="black", font=("Helvetica", 32))
controltext.pack()

leadertext = Text(frame3, height=20, width=40, padx=20, pady=20, bg="black", fg="white", relief=FLAT,
                  highlightbackground="black", font=("Helvetica", 50))
leadertext.pack()

howplaytxt = Text(frame4, height=20, width=40, padx=20, pady=20, bg="black", fg="white", relief=FLAT,
                  highlightbackground="black", font=("Helvetica", 32))
howplaytxt.pack()


cheatex = '''               __CHEATS__

Konami Code  =  Go Wild :)
(cannot end game if left on,
type the code again to disable)


life  =  gives 10 additional lives


score  =  gives 1000 additional score


Ctrl-b  =  boss key
'''


controltex = '''              __CONTROLS__

Up Key  =  Face Upwards
Down Key  =  Face Downwards
Left Key  =  Face Left
Right Key  =  Face Right
p/Esc  =  pause/unpause
Ctrl-b  =  boss key
'''


howplay = '''           __HOW TO PLAY__

Enemies attack
you from different sides

Face them when they
reach you to score
points otherwise
you lose a life
'''


leaders = ''' _LEADERBOARD_'''

cheattext.insert(1.0, cheatex)
controltext.insert(1.0, controltex)
howplaytxt.insert(1.0, howplay)


cheat_state = 0
control_state = 0
lboard_state = 0
how_state = 0


def btncheats():
    global cheat_state, control_state, lboard_state, how_state
    if cheat_state == 0:
        frame.lift()
        cheat_state = 1
    else:
        frame.lower()
        cheat_state = 0


def btncontrols():
    global control_state, cheat_state, lboard_state, how_state
    if control_state == 0:
        frame2.lift()
        control_state = 1
    else:
        frame2.lower()
        control_state = 0


def btnlead():
    global lboard_state, control_state, cheat_state, how_state, leaders
    if lboard_state == 0:
        leaderboard()
        frame3.lift()
        lboard_state = 1
    else:
        frame3.lower()
        leadertext.delete(1.0, END)
        lboard_state = 0


def btnhowplay():
    global how_state, lboard_state, control_state, cheat_state
    if how_state == 0:
        frame4.lift()
        how_state = 1
    else:
        frame4.lower()
        how_state = 0


def leaderboard():
    global score
    global leaders
    leaders = ''' _LEADERBOARD_'''
    leaders += "\n"
    f = open("leaderboard.txt", "r+")
    data = f.read().splitlines()
    dat = []
    for x in data:
        if x != "":
            dat.append(x)
    # print(dat)
    f.close()
    a = sorted(dat, key=lambda x: int(x.split()[1]), reverse=True)
    f = open("leaderboard.txt", "w+")
    for x in a:
        f.write(x + "\n")
    f.close()
    # print(a)
    for x in a:
        leaders += x
        leaders += "\n"
    # print(leaders)
    leadertext.insert(1.0, leaders)


def startplay():
    canvas.focus_set()
    menu_frame.lower()
    game_frame.lift()
    start()


def quit():
    menu_frame.lift()
    game_frame.lower()


def addtolead(a):
    global score
    if a == 1:
        f = open("leaderboard.txt", "r+")
        data = f.read().splitlines()
        username = name.get()
        add = username + "\t" + str(score)
        data.append(add)
        # print(data)
        f = open("leaderboard.txt", "w+")
        for x in data:
            f.write(x + "\n")
        f.close()
    elif a == 2:
        save()
    elif a ==3:
        load()


username = name.get()

def save():
    window.update()
    global score,lives
    username = name.get()
    if username == "":
        username = "Guest"
    else:
        username = username
    f = open("save.txt", "w+")
    add = username + "\t" + str(score)+ "\t" +str(lives)
    f.write(add)
    #print(add)


def load():
    window.update()
    global score,lives
    f = open("save.txt","r+")
    data = f.readline().split()
    username = str(data[0])
    score = int(data[1])
    lives = int(data[2])
    name.insert(0,username)
    game_frame.lift()
    start(lives,score)


def close():
    window.quit()
    window.destroy()



gOquit = Button(gameover_frame, text="Menu", command=quit, font=("Helvetica", 32), width=10).place(x=850, y=600)
gOretry = Button(gameover_frame, text="Try Again", command=startplay, font=("Helvetica", 32), width=10).place(x=550,
                                                                                                              y=600)
gOleaderboard = Button(gameover_frame, text="Add to Leaderboard?", command=lambda:addtolead(1), font=("Helvetica", 32)).place(
    x=620, y=500)

pausesave = Button(pause_frame, text="Save", command=lambda:addtolead(2), font=("Helvetica", 62), width=10).place(x=200, y=700)



startbut = Button(menu_frame, text="Start", padx=5, command=startplay, font="Comic 50", width=10, height=1)
btnload = Button(menu_frame, text="Load", padx=5, command=lambda:addtolead(3), font="Comic 50", width=10, height=1)
HowToPlay = Button(menu_frame, text="How to Play", padx=5, command=btnhowplay, font="Comic 50", width=10, height=1)
cheats = Button(menu_frame, text="Cheats", padx=5, command=btncheats, font="Comic 50", width=10, height=1)
controls = Button(menu_frame, text="Controls", padx=5, command=btncontrols, font="Comic 50", width=10, height=1)
lboard = Button(menu_frame, text="Leaderboard", padx=5, command=btnlead, font="Comic 50", width=10, height=1)

startbut.place(relx=0.2, rely=0.4, anchor="center")
btnload.place(relx=0.2, rely=0.5, anchor="center")
HowToPlay.place(relx=0.2, rely=0.6, anchor="center")
lboard.place(relx=0.2, rely=0.7, anchor="center")
cheats.place(relx=0.2, rely=0.8, anchor="center")
controls.place(relx=0.2, rely=0.9, anchor="center")

canvas.focus_set()

window.protocol("WM_DELETE_WINDOW", close)

window.mainloop()
