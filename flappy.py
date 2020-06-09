import pygame
import random
from pygame.locals import *

# Importar Bibliotecas
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import DataBaser

# Criar janela
jan = Tk()
jan.title("DP Systems - Acess Panel")
jan.geometry("410x500")
jan.configure(background="white")
jan.resizable(width=False, height=False)
jan.attributes("-alpha", 1.9)

# Widgets


def close():
    jan.destroy()


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
    try:
        if(User in VerifyLogin and Pass in VerifyLogin):
            messagebox.showinfo(title="Login Info",
                                message="Acesso Confirmado, Bem vindo!", command=close())
    except:
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

jan.mainloop()


SCREEN_WIDTH = 350
SCREEN_HEIGHT = 700
SPEED = 10
GRAVITY = 1
GAME_SPEED = 10

GROUND_WIDTH = 2 * SCREEN_WIDTH
GROUND_HEIGHT = 100

PIPE_WIDTH = 80
PIPE_HEIGHT = 500

PIPE_GAP = 200


class Bird(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.images = [pygame.image.load('bluebird-upflap.png').convert_alpha(),
                       pygame.image.load(
                           'bluebird-midflap.png').convert_alpha(),
                       pygame.image.load('bluebird-downflap.png').convert_alpha()]

        self.speed = SPEED

        self.current_image = 0

        self.image = pygame.image.load('bluebird-upflap.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = SCREEN_WIDTH / 2
        self.rect[1] = SCREEN_HEIGHT / 2

    def update(self):
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[self.current_image]

        self.speed += GRAVITY

        # Update height
        self.rect[1] += self.speed

    def bump(self):
        self.speed = -SPEED


class Pipe(pygame.sprite.Sprite):

    def __init__(self, inverted, xpos, ysize):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('pipe-red.png').convert_alpha()
        self.image = pygame.transform.scale(
            self.image, (PIPE_WIDTH, PIPE_HEIGHT))

        self.rect = self.image.get_rect()
        self.rect[0] = xpos

        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect[1] = - (self.rect[3] - ysize)
        else:
            self.rect[1] = SCREEN_HEIGHT - ysize

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect[0] -= GAME_SPEED


class Ground(pygame.sprite.Sprite):

    def __init__(self, xpos):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('base.png').convert_alpha()
        self.image = pygame.transform.scale(
            self.image, (GROUND_WIDTH, GROUND_HEIGHT))

        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = SCREEN_HEIGHT - GROUND_HEIGHT

    def update(self):
        self.rect[0] -= GAME_SPEED


def is_off_screen(sprite):
    return sprite.rect[0] < -(sprite.rect[2])


def get_random_pipes(xpos):
    size = random.randint(100, 300)
    pipe = Pipe(False, xpos, size)
    pipe_inverted = Pipe(True, xpos, SCREEN_HEIGHT - size - PIPE_GAP)
    return (pipe, pipe_inverted)


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

BACKGROUND = pygame.image.load('background-day.png')
BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))

bird_group = pygame.sprite.Group()
bird = Bird()
bird_group.add(bird)

ground_group = pygame.sprite.Group()
for i in range(2):
    ground = Ground(GROUND_WIDTH * i)
    ground_group.add(ground)

pipe_group = pygame.sprite.Group()
for i in range(2):
    pipes = get_random_pipes(SCREEN_WIDTH * i + 800)
    pipe_group.add(pipes[0])
    pipe_group.add(pipes[1])


clock = pygame.time.Clock()

while True:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                bird.bump()

    screen.blit(BACKGROUND, (0, 0))

    if is_off_screen(ground_group.sprites()[0]):
        ground_group.remove(ground_group.sprites()[0])

        new_ground = Ground(GROUND_WIDTH - 20)
        ground_group.add(new_ground)

    if is_off_screen(pipe_group.sprites()[0]):
        pipe_group.remove(pipe_group.sprites()[0])
        pipe_group.remove(pipe_group.sprites()[0])

        pipes = get_random_pipes(SCREEN_WIDTH * 2)

        pipe_group.add(pipes[0])
        pipe_group.add(pipes[1])

    bird_group.update()
    ground_group.update()
    pipe_group.update()

    bird_group.draw(screen)
    pipe_group.draw(screen)
    ground_group.draw(screen)

    pygame.display.update()

    if (pygame.sprite.groupcollide(bird_group, ground_group, False, False, pygame.sprite.collide_mask) or
            pygame.sprite.groupcollide(bird_group, pipe_group, False, False, pygame.sprite.collide_mask)):
        # Game over
        input()
        break
