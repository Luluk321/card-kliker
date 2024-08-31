import pygame
import time
from random import randint

pygame.init()

# Membuat jendela program
back = (200, 255, 255)  # warna latar belakang
mw = pygame.display.set_mode((500, 500))  # jendela utama
mw.fill(back)
clock = pygame.time.Clock()

# Kelas persegi panjang
class Area:
    def __init__(self, x=0, y=0, width=10, height=10, color=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.fill_color = color
    
    def color(self, new_color):
        self.fill_color = new_color
    
    def fill(self):
        pygame.draw.rect(mw, self.fill_color, self.rect)
    
    def outline(self, frame_color, thickness):
        pygame.draw.rect(mw, frame_color, self.rect, thickness)
    
    def collidepoint(self, x, y):
        return self.rect.collidepoint(x, y)

# Kelas Label
class Label(Area):
    def set_text(self, text, fsize=12, text_color=(0, 0, 0)):
        self.image = pygame.font.SysFont('verdana', fsize).render(text, True, text_color)
    
    def draw(self, shift_x=0, shift_y=0):
        self.fill()
        mw.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))

# Warna
RED = (255, 0, 0)
GREEN = (0, 255, 51)
YELLOW = (255, 255, 0)
DARK_BLUE = (0, 0, 100)
BLUE = (80, 80, 255)
LIGHT_GREEN = (200, 255, 200)
LIGHT_RED = (250, 128, 114)

cards = []
num_cards = 4
x = 70

start_time = time.time()
cur_time = start_time

# Antarmuka game
time_text = Label(0, 0, 50, 50, back)
time_text.set_text('Time:', 40, DARK_BLUE)
time_text.draw(20, 20)

timer = Label(50, 55, 50, 40, back)
timer.set_text('0', 40, DARK_BLUE)
timer.draw(0, 0)

score_text = Label(380, 0, 50, 50, back)
score_text.set_text('Count:', 45, DARK_BLUE)
score_text.draw(20, 20)

score = Label(430, 55, 50, 40, back)
score.set_text('0', 40, DARK_BLUE)
score.draw(0, 0)

for i in range(num_cards):
    new_card = Label(x, 170, 70, 100, YELLOW)
    new_card.outline(BLUE, 10)
    new_card.set_text('CLICK', 26)
    cards.append(new_card)
    x += 100

wait = 0
points = 0

while True:
    # Menggambar kartu dan menampilkan klik
    if wait == 0:
        wait = 20  # begitu banyak kutu label akan berada di satu tempat
        click = randint(1, num_cards)
        for i in range(num_cards):
            cards[i].color(YELLOW)
            if (i + 1) == click:
                cards[i].draw(10, 40)
            else:
                cards[i].fill()
    else:
        wait -= 1

    # Menangani klik pada kartu
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            for i in range(num_cards):
                if cards[i].collidepoint(x, y):
                    if i + 1 == click:  # jika ada label pada kartu, kita beri warna hijau, tambahkan titik 
                        cards[i].color(GREEN)
                        points += 1
                    else:  # jika tidak, warnai merah, kurangi satu poin
                        cards[i].color(RED)
                        points -= 1
                    cards[i].fill()
                    score.set_text(str(points), 40, DARK_BLUE)
                    score.draw(0, 0)

    # Menang dan kalah
    new_time = time.time()

    if new_time - start_time >= 11:
        win = Label(0, 0, 500, 500, LIGHT_RED)
        win.set_text("Waktunya sudah habis!!!", 60, DARK_BLUE)
        win.draw(110, 180)
        pygame.display.update()
        time.sleep(2)  # Berikan waktu untuk melihat pesan sebelum keluar
        pygame.quit()
        exit()

    if int(new_time) - int(cur_time) == 1:  # periksa apakah ada perbedaan 1 detik antara waktu lama dan baru
        timer.set_text(str(int(new_time - start_time)), 40, DARK_BLUE)
        timer.draw(0, 0)
        cur_time = new_time

    if points >= 5:
        win = Label(0, 0, 500, 500, LIGHT_GREEN)
        win.set_text("Anda menang!!!", 60, DARK_BLUE)
        win.draw(140, 180)
        resul_time = Label(90, 230, 250, 250, LIGHT_GREEN)
        resul_time.set_text("Waktu untuk menyelesaikan: " + str(int(new_time - start_time)) + " detik", 40, DARK_BLUE)
        resul_time.draw(0, 0)
        pygame.display.update()
        time.sleep(2)  # Berikan waktu untuk melihat pesan sebelum keluar
        pygame.quit()
        exit()

    pygame.display.update()
    clock.tick(40)
