import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import sqlite3
import pygame
import random
import threading
from pygame import mixer

class tkinterApp(tk.Tk):

    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)

        # creating a container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # initializing frames to an empty array
        self.frames = {}

        # iterating through a tuple consisting
        # of the different page layouts
        for F in (Login_Page, Register):
            frame = F(container, self)

            # initializing frame of that object from
            # login page, regestration page, game page respectively with
            # for loop
            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Login_Page)

    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class Login_Page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        def start_game():
            # creating game

            global user
            pygame.init()

            # game background sound
            mixer.init()
            mixer.music.load('sound.mp3')
            mixer.music.set_volume(5)
            mixer.music.play(loops=-1)

            winHeight = 480
            winWidth = 700
            app = pygame.display.set_mode((winWidth, winHeight))
            img = pygame.image.load('hangman6.ico')
            pygame.display.set_icon(img)
            # ---------------------------------------#
            # initialize global variables/constants #
            # ---------------------------------------#
            BLACK = (0, 0, 0)
            WHITE = (255, 255, 255)
            RED = (255, 0, 0)
            GREEN = (0, 255, 0)
            BLUE = (0, 0, 255)
            LIGHT_BLUE = (102, 255, 255)

            btn_font = pygame.font.SysFont("arial", 20)
            guess_font = pygame.font.SysFont("monospace", 24)
            lost_font = pygame.font.SysFont('arial', 45)
            global word
            global buttons
            word = ''
            buttons = []
            global guessed
            global guessed
            global hangmanPics
            global limbs
            guessed = []
            hangmanPics = [pygame.image.load('hangman0.png'), pygame.image.load('hangman1.png'),
                           pygame.image.load('hangman2.png'), pygame.image.load('hangman3.png'),
                           pygame.image.load('hangman4.png'), pygame.image.load('hangman5.png'),
                           pygame.image.load('hangman6.png')]

            limbs = 0

            def redraw_game_window():
                global guessed
                global hangmanPics
                global limbs
                app.fill(GREEN)
                # Buttons
                for i in range(len(buttons)):
                    if buttons[i][4]:
                        pygame.draw.circle(app, BLACK, (buttons[i][1], buttons[i][2]), buttons[i][3])
                        pygame.draw.circle(app, buttons[i][0], (buttons[i][1], buttons[i][2]), buttons[i][3] - 2
                                           )
                        label = btn_font.render(chr(buttons[i][5]), 1, BLACK)
                        app.blit(label,
                                 (buttons[i][1] - (label.get_width() / 2), buttons[i][2] - (label.get_height() / 2)))

                spaced = spacedOut(word, guessed)
                label1 = guess_font.render(spaced, 1, BLACK)
                rect = label1.get_rect()
                length = rect[2]

                app.blit(label1, (winWidth / 2 - length / 2, 400))

                pic = hangmanPics[limbs]
                app.blit(pic, (winWidth / 2 - pic.get_width() / 2 + 20, 150))
                pygame.display.update()

            def randomWord():
                file = open('words.txt')
                f = file.readlines()
                i = random.randrange(0, len(f) - 1)

                return f[i][:-1]

            def hang(guess):
                global word
                if guess.lower() not in word.lower():
                    return True
                else:
                    return False

            def spacedOut(word, guessed=[]):
                spacedWord = ''
                guessedLetters = guessed
                for x in range(len(word)):
                    if word[x] != ' ':
                        spacedWord += '_ '
                        for i in range(len(guessedLetters)):
                            if word[x].upper() == guessedLetters[i]:
                                spacedWord = spacedWord[:-2]
                                spacedWord += word[x].upper() + ' '
                    elif word[x] == ' ':
                        spacedWord += ' '
                return spacedWord

            def buttonHit(x, y):
                for i in range(len(buttons)):
                    if x < buttons[i][1] + 20 and x > buttons[i][1] - 20:
                        if y < buttons[i][2] + 20 and y > buttons[i][2] - 20:
                            return buttons[i][5]
                return None

            def end(winner=False):
                global limbs

                lostTxt = 'You Lost, press any key to play again...'
                winTxt = 'WINNER!, press any key to play again...'
                redraw_game_window()
                pygame.time.delay(1000)
                app.fill(GREEN)

                if winner == True:
                    label = lost_font.render(winTxt, 1, BLACK)
                else:
                    label = lost_font.render(lostTxt, 1, BLACK)

                wordTxt = lost_font.render(word.upper(), 1, BLACK)
                wordWas = lost_font.render('The phrase was: ', 1, BLACK)

                # show score obtained
                scoreis = lost_font.render(user+' Score is :', 1, BLACK)
                point = lost_font.render(str(score), 1, BLACK)

                app.blit(wordTxt, (winWidth / 2 - wordTxt.get_width() / 2, 295))
                app.blit(wordWas, (winWidth / 2 - wordWas.get_width() / 2, 245))
                app.blit(label, (winWidth / 2 - label.get_width() / 2, 140))
                app.blit(scoreis, (winWidth / 2 - scoreis.get_width() / 2, 40))
                app.blit(point, (winWidth / 2 - point.get_width() / 2, 85))
                pygame.display.update()
                again = True
                while again:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                        if event.type == pygame.KEYDOWN:
                            again = False
                reset()

            def reset():
                global limbs
                global guessed
                global buttons
                global word
                for i in range(len(buttons)):
                    buttons[i][4] = True

                limbs = 0
                guessed = []
                word = randomWord()

            # MAINLINE

            # Setup buttons
            increase = round(winWidth / 13)
            for i in range(26):
                if i < 13:
                    y = 40
                    x = 25 + (increase * i)
                else:
                    x = 25 + (increase * (i - 13))
                    y = 85
                buttons.append([LIGHT_BLUE, x, y, 20, True, 65 + i])
                # buttons.append([color, x_pos, y_pos, radius, visible, char])

            word = randomWord()
            inPlay = True
            score = 0
            while inPlay:
                redraw_game_window()
                pygame.time.delay(10)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        inPlay = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            inPlay = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        clickPos = pygame.mouse.get_pos()
                        letter = buttonHit(clickPos[0], clickPos[1])
                        if letter != None:
                            guessed.append(chr(letter))
                            buttons[letter - 65][4] = False
                            if hang(chr(letter)):
                                if limbs != 5:
                                    score = score - 5
                                    limbs += 1
                                    print(score)
                                else:
                                    end()
                            else:
                                print(spacedOut(word, guessed))
                                score = score + 10
                                print(score)
                                if spacedOut(word, guessed).count('_') == 0:
                                    end(True)
            mixer.music.stop()
            pygame.quit()

            # always quit pygame when done!

        # for checking username and password
        username = StringVar()
        password = StringVar()

        def check_login():
            # to show error while logging and disappers after some time
            def error_message():
                label_4 = Label(app, text="User doesnot exists", width=20, font=("bold", 10))
                label_4.place(x=180, y=280)
                start_time = threading.Timer(6, lambda: label_4.place_forget())
                start_time.start()

            global user
            user = username.get()
            pas = password.get()
            conn = sqlite3.connect('Regestration.db')
            c = conn.cursor()
            c.execute("SELECT * FROM Player_details")
            records = c.fetchall()
            d = 0
            for i in records:
                if i[4] == user and i[5] == pas:
                    d = 1

            if d == 1:
                # Start game page
                root = Tk
                img = ImageTk.PhotoImage(Image.open("new.jpg"))
                app.geometry("605x305")
                label = Label(self, image=img)
                label.place(x=0, y=0)
                Button(self, text='Start', width=20, bg='white', fg='black',
                       command=start_game).place(x=230, y=250)
                root.mainloop(self)
            else:
                error_message()

            conn.commit()

            conn.close()

        # layout of login page
        label_0 = ttk.Label(self, text="Login Page", width=20, font=("bold", 20))
        label_0.place(x=180, y=35)

        label_2 = ttk.Label(self, text="UserName", width=20, font=("bold", 10))
        label_2.place(x=110, y=100)

        entry_2 = ttk.Entry(self, textvar=username)
        entry_2.place(x=260, y=100)

        label_3 = ttk.Label(self, text="Password", width=20, font=("bold", 10))
        label_3.place(x=110, y=150)

        entry_3 = ttk.Entry(self, textvar=password, show = "*")
        entry_3.place(x=260, y=150)

        # button to login
        Button(self, text='Login', width=20, bg='brown', fg='white', command=check_login).place(x=180, y=200)

        ## button to register
        Button(self, text='Register', width=20, bg='brown', fg='white',
               command=lambda: controller.show_frame(Register)).place(x=180, y=240)


# Second window frame Regestration page
class Register(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # data storage type
        player_id = int()
        first_name = StringVar()
        last_name = StringVar()
        contact_no = StringVar()
        username = StringVar()
        password = StringVar()
        conform_password = StringVar()
        email = StringVar()

        # data storing
        def database():
            # inputs extraction
            f_name = first_name.get()
            l_name = last_name.get()
            contact = contact_no.get()
            user = username.get()
            pas = password.get()
            con_pas = conform_password.get()
            em = email.get()
            conn = sqlite3.connect('Regestration.db')
            with conn:
                c = conn.cursor()

            c.execute(
                'CREATE TABLE IF NOT EXISTS Player_details (Player_id INTEGER PRIMARY KEY AUTOINCREMENT,'
                'First_Name TEXT(20),Last_Name TEXT(20),Contact_No INT(13),Username TEXT(20),Password TEXT(10),'
                'Email TEXT(30))')
            c.execute("SELECT * FROM Player_details")
            records = c.fetchall()

            def error_message_regpage():
                d = 0

                # Serching data from sql database and logic
                for i in records:
                    if i[4] == user or i[6] == em:
                        d = 1
                        if i[4] == user and i[6] == em:

                            label_9 = Label(self, text="Username and Email Already exists", width=20, font=("bold", 10))
                            label_9.place(x=180, y=520)
                        elif i[4] == user:
                            label_9 = Label(self, text=" Username Already exists", width=20, font=("bold", 10))
                            label_9.place(x=180, y=520)

                        elif i[6] == em:
                            label_9 = Label(self, text="Email  Already exists", width=20, font=("bold", 10))
                            label_9.place(x=180, y=520)

                if d != 1:
                    if len(user) == 0 or len(em) == 0 or len(pas) == 0 or len(con_pas) == 0 or len(f_name) == 0 or len(
                            l_name) == 0 or len(contact) == 0:
                        label_9 = Label(self, text="Box can,t be empty", width=20, font=("bold", 10))
                        label_9.place(x=180, y=520)
                    elif pas == con_pas:
                        c.execute(
                            'INSERT INTO Player_details (First_name,Last_Name,Contact_No,Email,'
                            'Username,Password) VALUES(?,?,?,?,?,?)',
                            (f_name, l_name, contact, em, user, pas))
                        label_9 = Label(self, text="Success", width=20, font=("bold", 10))
                        label_9.place(x=180, y=520)


                    elif pas != con_pas:
                        label_9 = Label(self, text="Incorrect Password", width=20, font=("bold", 10))
                        label_9.place(x=180, y=520)

                start_time = threading.Timer(6, lambda: label_9.place_forget())
                start_time.start()

            message_store = error_message_regpage()

            for i in records:
                print(i)

            conn.commit()
            conn.close()

        # Regester Page layout
        label_0 = ttk.Label(self, text="Registration Page", width=20, font=("bold", 20))
        label_0.place(x=145, y=35)

        label_1 = ttk.Label(self, text="First Name", width=20, font=("bold", 10))
        label_1.place(x=110, y=100)
        entry_1 = ttk.Entry(self, textvar=first_name)
        entry_1.place(x=260, y=100)

        label_2 = ttk.Label(self, text="Last Name", width=20, font=("bold", 10))
        label_2.place(x=110, y=150)
        entry_2 = ttk.Entry(self, textvar=last_name)
        entry_2.place(x=260, y=150)

        label_3 = ttk.Label(self, text="Contact No", width=20, font=("bold", 10))
        label_3.place(x=110, y=200)
        entry_3 = ttk.Entry(self, textvar=contact_no)
        entry_3.place(x=260, y=200)

        label_4 = ttk.Label(self, text="Email", width=20, font=("bold", 10))
        label_4.place(x=110, y=250)
        entry_4 = ttk.Entry(self, textvar=email)
        entry_4.place(x=260, y=250)

        label_5 = ttk.Label(self, text="UserName", width=20, font=("bold", 10))
        label_5.place(x=110, y=300)
        entry_5 = ttk.Entry(self, textvar=username)
        entry_5.place(x=260, y=300)

        label_6 = ttk.Label(self, text="Password", width=20, font=("bold", 10))
        label_6.place(x=110, y=350)
        entry_6 = ttk.Entry(self, textvar=password)
        entry_6.place(x=260, y=350)

        label_7 = ttk.Label(self, text="Conform Password", width=20, font=("bold", 10))
        label_7.place(x=110, y=400)
        entry_7 = ttk.Entry(self, textvar=conform_password)
        entry_7.place(x=260, y=400)

        # button for submit in reg page
        Button(self, text='Submit', width=20, bg='brown', fg='white', command=database).place(x=180, y=450)

        # button for login in reg page
        Button(self, text='Login', width=20, bg='brown', fg='white',
               command=lambda: controller.show_frame(Login_Page)).place(x=180, y=490)


app = tkinterApp()
app.iconbitmap('hangman6.ico')

app.geometry("500x550")
app.title("Hangman Game")

app.mainloop()
