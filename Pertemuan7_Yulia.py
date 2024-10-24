import pygame as pg
import random as ran

# Inisialisasi pygame
pg.init()
pg.mixer.init()

# Membuat jendela game
WIDTH, HEIGHT = 550, 600
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Space Shooter Yulia')

# Tambahkan image sebagai background
image = pg.image.load("space.jpg")
image = pg.transform.scale(image, (550, 600))

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
DARK_RED = (139, 0, 0)




# Kecepatan game
FPS = 60
clock = pg.time.Clock()

# Menyimpan highest score dalam variabel
highest_score = 0

# Memasukkan suara backgroud game
pg.mixer.music.load("suara_backgroud.wav")
pg.mixer.music.set_volume(0.5)
pg.mixer.music.play(-1)

# Memasukkan sound efek ship hit rock
hit_sound = pg.mixer.Sound("ini_peluru.wav")
hit_sound.set_volume(0.5)

# Memasukkan sound efek ketika player mati
player_die_sound = pg.mixer.Sound("player_die.wav")
player_die_sound.set_volume(0.5)

# Kelas untuk player
class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load('plane.png')
        self.image = pg.transform.scale(self.image, (50, 50))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 50)
        self.speed = 5
        self.lives = 3  # Jumlah nyawa

    def update(self):
        keys = pg.key.get_pressed()
        # Kondisi jika kita gerakan objek ke atas, bawah, kiri dan kanan
        if keys[pg.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pg.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed
        if keys[pg.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pg.K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

# Kelas untuk enemies
class Enemies(pg.sprite.Sprite):
    def __init__(self, level=1):
        super().__init__()
        self.image = pg.image.load('musuh.png')
        self.image = pg.transform.scale(self.image, (50, 50))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = ran.randint(0, WIDTH - 50)
        self.rect.y = ran.randint(-100, -50)
        self.speed = ran.randint(3, 6 + level)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.rect.x = ran.randint(0, WIDTH - 75)
            self.rect.y = ran.randint(-100, -50)
            self.speed = ran.randint(3, 6)

# Kelas untuk peluru
class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pg.Surface((5, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -20 # Menambah kecepatan peluru

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

# Membuat fungsi menampilkan teks
def draw_text(text, font, color, x, y):
    screen_text = font.render(text, True, color)
    screen.blit(screen_text, (x, y))

# Membuat tombol menu
def draw_button(text, x, y, w, h, inactive_color, active_color, action=None):
    mouse = pg.mouse.get_pos()
    click = pg.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pg.draw.rect(screen, active_color, (x, y, w, h))
        if click[0] == 1 and action is not None:
            action()
    else:
        pg.draw.rect(screen, inactive_color, (x, y, w, h))

    font = pg.font.SysFont(None, 40)
    text_surf = font.render(text, True, WHITE)
    screen.blit(text_surf, (x + (w / 5), y + (h / 5)))

# Menampilkan nyawa
def draw_lives(surf, x, y, lives, image):
    for i in range(lives):
        image_rect = image.get_rect()
        image_rect.x = x + 30 * i
        image_rect.y = y
        surf.blit(image, image_rect)

# Membuat fungsi untuk memulai game
def start_game():
    global highest_score # Mengakses global variabel highest score

    # Inisialisasi sprite group
    global all_sprites, enemies, bullets
    all_sprites = pg.sprite.Group()
    enemies = pg.sprite.Group()
    bullets = pg.sprite.Group() # untuk mengelola semua peluru

    # Membuat player
    player = Player()
    all_sprites.add(player)

    # Membuat enemies
    level = 1  # Inisialisasi level
    for i in range(5):
        enemy = Enemies(level)
        all_sprites.add(enemy)
        enemies.add(enemy)

    # Membuat score, waktu and level
    score = 0
    start = pg.time.get_ticks()
    level = 1

    # Loop Game
    run = True
    game_over = False
    while run:
        clock.tick(FPS)

        # Menutup game jika tekan 'X'
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE and not game_over:
                    player.shoot()

        # Logik naik level
        if score > 10 * level:
            level += 1
            for i in range(5):
                enemy = Enemies(level)
                all_sprites.add(enemy)
                enemies.add(enemy)

        # Logik Game over
        if not game_over:
            # Update semua sprite
            all_sprites.update()

            # Mengecek apakah player hit enemies?
            hits = pg.sprite.spritecollide(player, enemies, False)
            if hits:
                player.lives -= 1  # Mengurangi nyawa saat kena musuh
                player_die_sound.play()
                for hit in hits:
                    hit.kill()  # Hapus musuh yang terkena
                
                if player.lives == 0:
                    game_over = True
                    if score > highest_score:  # Highest score didasarkan pada score
                        highest_score = score  # Update highest score dengan score

            # Kolisi antara peluru dan musuh
            hits = pg.sprite.groupcollide(enemies, bullets, True, True)
            for hit in hits:
                score += 1
                enemy = Enemies(level)
                all_sprites.add(enemy)
                enemies.add(enemy)
                hit_sound.play()

        # Menampilkan backgroud
        screen.blit(image, (0, 0))

        # Menggambar objek dan menampilkan informasi
        all_sprites.draw(screen)

        # Menampilkan score
        font = pg.font.SysFont(None, 30)
        text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(text, (10, 10))

        # Menampilkan level
        text = font.render(f"Level: {level}", True, WHITE)
        screen.blit(text, (10, 30))

        # Menampilkan nyawa di pojok kanan atas
        player_image = pg.transform.scale(player.image, (30, 30))
        draw_lives(screen, WIDTH - 100, 10, player.lives, player_image)

        # Menampilkan game over and highest score
        if game_over:
            # Menampilkan tulisan 'Game Over'
            font = pg.font.SysFont(None, 80)
            over_text = font.render("Game Over!", True, RED)
            screen.blit(over_text, (WIDTH // 2 - 150, HEIGHT // 3 + 20))  # Posisi untuk Game Over

            # Menampilkan tulisan 'Your Best Score'
            font = pg.font.SysFont(None, 40)
            score_text = font.render(f"Your Best Score: {highest_score}", True, WHITE)
            screen.blit(score_text, (WIDTH // 2 - 111, HEIGHT // 3 + 80))  # Posisi untuk Best Score

            # font = pg.font.SysFont(None, 40)
            # over_text = font.render(f"Game Over! Your Best Score: {highest_score}", True, WHITE)
            # screen.blit(over_text, (WIDTH // 2 - 200, HEIGHT // 3 + 80))
            # Menampilkan  tombol restart game
            draw_button("Restart Game", WIDTH // 2 - 140, HEIGHT // 2 + 50, 300, 50, BLUE, GREEN, start_game)

        pg.display.flip()

    pg.quit()

# Membuat menu utama
def main_menu():
    menu = True
    while menu:
        screen.blit(image, (0, 0))

        # Menampilkan judul game
        font = pg.font.SysFont('Impact', 57)
        draw_text("SPACE SHOOTER", font, WHITE, WIDTH // 2 - 180, HEIGHT // 3)

        # Menampilkan tombol start
        draw_button("Start Game", WIDTH // 2 - 125, HEIGHT // 2 + 50, 240, 50, BLUE, GREEN, start_game)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                menu = False

        pg.display.update()
        clock.tick(15)

# Memulai Program
if __name__ == '__main__':
    main_menu()
