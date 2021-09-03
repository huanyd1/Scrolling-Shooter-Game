import pygame
import os

pygame.init()

#Tạo kích thước màn hình
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Shooter')

#Đặt tỉ lệ khung hình
clock = pygame.time.Clock()
FPS = 60

#Đặt biến trọng lục
GRAVITY = 0.75

#Đặt biến di chuyển trái - phải
moving_left = False
moving_right = False


#Đặt màu 
BG = (144, 201, 120)
RED = (255, 0, 0)

#Xét màu
def draw_bg():
    screen.fill(BG)
    pygame.draw.line(screen, RED, (0, 300), (SCREEN_WIDTH, 300))


#Lớp lính
class Soldier(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        #Biến còn sống, nếu alive == False => lính chết
        self.alive = True
        #Biến hoạt động (#0 : Đứng yên, #1: Chạy, #2: Nhảy)
        self.char_type = char_type
        #Vận tốc
        self.speed = speed
        #Chiều di chuyển
        self.direction = 1
        self.vel_y = 0
        #Nhảy (#True: nhảy, #False : Không nhảy)
        self.jump = False
        #Trên không
        self.in_air = True
        #Xoay ảnh
        self.flip = False
        #List hoạt ảnh
        self.animation_list = []
        #Khung hình
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        
        #Tải tất cả các hoạt ảnh của nhân vật
        animation_types = ['Idle', 'Run', 'Jump']
        for animation in animation_types:
            #Đặt lại hình ảnh
            temp_list = []
            #Đếm số file trong thư mục
            num_of_frames = len(os.listdir(f'img/{self.char_type}/Black/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'img/{self.char_type}/Black/{animation}/{i}.png')
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


    def move(self, moving_left, moving_right):
        #Đặt lại các chuyển động
        dx = 0
        dy = 0

        #Gán các chuyển động khi 'lính' di chuyển sang trái - phải
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        #Nhảy
        if self.jump == True and self.in_air == False:
            self.vel_y = -11
            self.jump = False
            self.in_air = True

        #Áp dụng trọng lực
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y

        #Kiểm tra va chạm với đất
        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.in_air = False

        #Cập nhật vị trí
        self.rect.x += dx
        self.rect.y += dy


    def update_animation(self):
        #Cập nhật Animation
        ANIMATION_COOLDOWN = 100
        #Cập nhật hình ảnh theo khung hình
        self.image = self.animation_list[self.action][self.frame_index]
        #Kiểm tra cập nhật khung hình
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        #Kiểm tra nếu hoạt ảnh giới hạn => Xét về hoạt ảnh ban đầu
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0



    def update_action(self, new_action):
        #Kiểm tra hành động
        if new_action != self.action:
            self.action = new_action
            #Cập nhật hoạt ảnh
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()



    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)



player = Soldier('player', 200, 200, 3, 5)
#enemy = Soldier('enemy', 400, 200, 3, 5)



run = True
while run:

    clock.tick(FPS)

    draw_bg()

    player.update_animation()
    player.draw()
    #enemy.draw()


    #Cập nhật hành động
    if player.alive:
        if player.in_air:
            player.update_action(2)#2: Nhảy
        elif moving_left or moving_right:
            player.update_action(1)#1: Chạy
        else:
            player.update_action(0)#0: Đứng yên
        player.move(moving_left, moving_right)


    for event in pygame.event.get():
        #Thoát game
        if event.type == pygame.QUIT:
            run = False
        #Nhấn phím
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_w and player.alive:
                player.jump = True
            if event.key == pygame.K_ESCAPE:
                run = False


        #Nhấc phím
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False




    pygame.display.update()

pygame.quit()