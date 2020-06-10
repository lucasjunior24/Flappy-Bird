
# Importar Bibliotecas
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import DataBaser
import tkinter as tk
import os
import random
import pygame


# Criar janela
jan = Tk()
jan.title("DP Systems - Acess Panel")
jan.geometry("427x582")
jan.configure(background="white")
jan.resizable(width=False, height=False)
jan.attributes("-alpha", 1.9)

# Widgets


RightFrame = Frame(jan, width=410, height=500,
                   bg="BLACK", relief="raise")
RightFrame.pack(side=RIGHT)

UserLabel = Label(RightFrame, text="Username:",
                  font=("Century Gothic", 16), bg="BLACK", fg="White")
UserLabel.place(x=35, y=130)

UserEntry = ttk.Entry(RightFrame, width=24)
UserEntry.place(x=180, y=140)

PassLabel = Label(RightFrame, text="Password:",
                  font=("Century Gothic", 16), bg="BLACK", fg="White")
PassLabel.place(x=37, y=180)

PassEntry = ttk.Entry(RightFrame, width=25, show="*")
PassEntry.place(x=174, y=190)


def Login():
    User = UserEntry.get()
    Pass = PassEntry.get()

    DataBaser.cursor.execute("""
    SELECT * FROM Users 
    WHERE User = ? AND Password = ?
    """, (User, Pass))
    print("Selecionou")
    VerifyLogin = DataBaser.cursor.fetchone()

    if(User in VerifyLogin and Pass in VerifyLogin):
        messagebox.showinfo(
            title="Login Info", message="Acesso Confirmado, Bem vindo!")
        close()
        open()
    else:
        messagebox.showinfo(title="Login Info", message="Acesso Negado!")


# Buttons
LoginButton = ttk.Button(RightFrame, text="Login", width=20, command=Login)
LoginButton.place(x=120, y=265)


def Register():
    # Removendo Wigets de login
    LoginButton.place(x=5000)
    RegisterButton.place(x=5000)
    # Inserindo widgets de Cadastro
    NomeLabel = Label(RightFrame, text="Name:", font=(
        "Century Gothic", 16), bg="BLACK", fg="White")
    NomeLabel.place(x=35, y=35)

    NomeEntry = ttk.Entry(RightFrame, width=30)
    NomeEntry.place(x=131, y=45)

    EmailLabel = Label(RightFrame, text="Email:", font=(
        "Century Gothic", 16), bg="BLACK", fg="White")
    EmailLabel.place(x=35, y=85)

    EmailEntry = ttk.Entry(RightFrame, width=32)
    EmailEntry.place(x=117, y=95)

    def RegisterToDataBase():
        Name = NomeEntry.get()
        Email = EmailEntry.get()
        User = UserEntry.get()
        Pass = PassEntry.get()

        if(Name == "" and Email == "" and User == "" and Pass == ""):
            messagebox.showerror(title="Register Error",
                                 message="Preencha todos os campos")
        else:
            DataBaser.cursor.execute("""
            INSERT INTO Users(Name, Email, User, Password) VALUES(?, ?, ?, ?)
            """, (Name, Email, User, Pass))
            DataBaser.conn.commit()
            messagebox.showinfo(title='Register info',
                                message="Register Sucessfull")

    Register = ttk.Button(
        RightFrame, text="Register", width=20, command=RegisterToDataBase)
    Register.place(x=120, y=265)

    def BackToLogin():
        # Removendo Widgets de Cadastro
        NomeLabel.place(x=5000)
        NomeEntry.place(x=5000)
        EmailLabel.place(x=5000)
        EmailEntry.place(x=5000)
        Register.place(x=5000)
        Back.place(x=5000)
        # Trazendo de volta Widgets de Login
        LoginButton.place(x=120)
        RegisterButton.place(x=120)

    Back = ttk.Button(RightFrame, text="Back", width=20, command=BackToLogin)
    Back.place(x=120, y=320)


RegisterButton = ttk.Button(
    RightFrame, text="Register", width=20, command=Register)
RegisterButton.place(x=120, y=320)

# variaveis globais

baseX = 0
passaroX = 0
passaroY = 0
passaroVel = 0
cano = []
pontos = 0
contarPontos = False

pygame.font.init()


def close():
    jan.destroy()


def open():

    tela = tk.Tk()
    # creates embed frame for pygame window
    moudura = tk.Frame(tela, width=427, height=582)

    # moudura.grid(columnspan=(600), rowspan=500)  # Adds grid
    moudura.pack(side=LEFT)  # packs window to the left

    os.environ['SDL_WINDOWID'] = str(moudura.winfo_id())
    os.environ['SDL_VIDEODRIVER'] = 'windib'

    # iniciação
    pygame.display.init()

    #

    FPS = 60  # FHASHS POR SEGUNDO
    JANELA = pygame.display.set_mode((427, 582))

    VEL_AVANCO = 4
    FONTE = pygame.font.SysFont("Comic Sans MS", 50, True)
    YELLOW = (255, 255, 0)
    # desenha

    global baseX, passaroX, passaroY, passaroVel, cano, pontos
    baseX = 0
    passaroX = 0
    passaroY = 0
    passaroVel = 0
    pontos = 0
    cano = []
    contarPontos = False

    # carregando imagens
    base = pygame.image.load("img/base2.png")
    gameOver = pygame.image.load("img/gameOver.png")
    bird = pygame.image.load("img/bird.png")
    fundo = pygame.image.load("img/fundoQuadrado.gif")
    pipe = pygame.image.load("img/pipe.png")
    pipeCima = pygame.transform.flip(pipe, False, True)  # gira o cano
    # DEFINIR CLASSE CANO

    class Canos:
        def __init__(self):
            super().__init__()
            self.x = 320
            self.y = random.randint(-75, 150)

        def desenhar(self):

            self.x -= VEL_AVANCO
            JANELA.blit(pipeCima, (self.x + 70, self.y - 190))
            JANELA.blit(pipe, (self.x + 70, self.y + 290))

        def colidir(self, bird, passaroX, passaroY, pipe):
            tolerancia = 5
            passaroLarX = passaroX + bird.get_width()  # largura
            passaroLX = passaroX
            passaroAY = passaroY
            passaroAltY = passaroY + bird.get_height()  # altura
            pipeLarX = self.x + pipe.get_width() + 70
            pipeLX = self.x + 70
            pipeAY = self.y + 128
            pipeAltY = self.y + 300
            if passaroLX < pipeLarX and passaroLarX > pipeLX:
                if passaroAY < pipeAY or passaroAltY > pipeAltY:
                    vocePerdeu()

        def contarPontos(self, passaroX, pipe):
            passaroLarX = passaroX + bird.get_width()  # largura
            passaroLX = passaroX
            pipeLarX = self.x + pipe.get_width()
            pipeLX = self.x
            if passaroLarX < pipeLarX and passaroLX > pipeLX:
                return True

    def desenhar():

        JANELA.blit(fundo, (0, 0))  # colocando o fundo
        for canos in cano:
            canos.desenhar()
        JANELA.blit(base, (0, 480))
        JANELA.blit(bird, (passaroX, passaroY))
        pontuacao = FONTE.render(str(pontos), True, YELLOW)
        JANELA.blit(pontuacao, (214, 70))

    def atualizarTela():
        pygame.display.update()
        pygame.time.Clock().tick(FPS)

    def inicializarVariaveis():
        global baseX, passaroX, passaroY, passaroVel, cano, pontos
        baseX = 0
        passaroX = 80
        passaroY = 150
        passaroVel = 0
        pontos = 0
        cano = []
        cano.append(Canos())

    def vocePerdeu():
        JANELA.blit(gameOver, (0, 60))
        atualizarTela()
        verificar = True
        while verificar:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        inicializarVariaveis()
                        global passaroVel
                        passaroVel = 10
                        verificar = False  # passando o verifica pra false, o jogador podew jogar novamente

    inicializarVariaveis()

    while True:
        tela.update()
        desenhar()
        atualizarTela()
        passaroVel -= 1
        passaroY -= passaroVel
        baseX -= VEL_AVANCO
        if baseX <= -5:
            baseX = 0
        if passaroY >= 480:
            vocePerdeu()

        # aumenta a quantidade de canos
        if cano[-1].x <= 140:
            cano.append(Canos())

        if len(cano) >= 4:
            del cano[0]

        if not contarPontos:
            for canos in cano:
                if canos.contarPontos(passaroX, pipe):
                    contarPontos = True
                    break

        if contarPontos:
            contarPontos = False
            for canos in cano:
                if canos.contarPontos(passaroX, pipe):
                    contarPontos = True
                    break
            if not contarPontos:
                pontos += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    passaroVel = 10

        for canos in cano:
            canos.colidir(bird, passaroX, passaroY, pipe)

    tela.mainloop()


jan.mainloop()
