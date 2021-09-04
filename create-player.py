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
shoot = False
grenade = False
grenade_thrown = False

#Tải hình ảnh
#Đạn
bullet_img = pygame.image.load('img/icons/SpongeBullet.png').convert_alpha()
#Lựu đạn
grenade_img = pygame.image.load('img/icons/grenade.png').convert_alpha()


#Đặt màu 
BG = (144, 201, 120)
RED = (255, 0, 0)

#Xét màu
def draw_bg():
    screen.fill(BG)
    pygame.draw.line(screen, RED, (0, 300), (SCREEN_WIDTH, 300))


#Lớp lính
class Soldier(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed, ammo, grenades):
        pygame.sprite.Sprite.__init__(self)
        #Biến còn sống, nếu alive == False => lính chết
        self.alive = True
        #Biến hoạt động (#0 : Đứng yên, #1: Chạy, #2: Nhảy, #3: Chết)
        self.char_type = char_type
        #Vận tốc
        self.speed = speed
        #Số đạn
        self.ammo = ammo
        #Số đạn bắt đầu
        self.start_ammo = ammo
        #Làm chậm số lần bắn
        self.shoot_cooldown = 0
        #Số lựu đạn
        self.grenades = grenades
        #Sức khỏe - Máu
        self.health = 100 
        #Máu tối đa
        self.max_health = self.health
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
        animation_types = ['Idle', 'Run', 'Jump', 'Death']
        for animation in animation_types:
            #Đặt lại hình ảnh
            temp_list = []
            #Đếm số file trong thư mục
            num_of_frames = len(os.listdir(f'img/{self.char_type}/Black/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'img/{self.char_type}/Black/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.update_animation()
        self.check_alive()
        #Cập nhật làm chậm
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

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

    def shoot(self):
        if self.shoot_cooldown ==  0 and self.ammo > 0:
            self.shoot_cooldown = 20
            bullet = Bullet(self.rect.centerx + (0.6 * self.rect.size[0] * self.direction), self.rect.centery, self.direction)
            bullet_group.add(bullet)
            self.ammo -= 1

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
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0



    def update_action(self, new_action):
        #Kiểm tra hành động
        if new_action != self.action:
            self.action = new_action
            #Cập nhật hoạt ảnh
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y,direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        #Đạn di chuyển
        self.rect.x += (self.direction * self.speed)
        #Kiểm tra nếu đạn ra khỏi màn hình thì xóa đạn => Tránh lấp đầy bộ nhớ
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
        #Kiểm tra va chạm
        if pygame.sprite.spritecollide(player, bullet_group, False):
            if player.alive: 
                player.health -= 5     
                self.kill()
        if pygame.sprite.spritecollide(enemy, bullet_group, False):
            if player.alive:      
                enemy.health -= 25
                self.kill()

class Grenade(pygame.sprite.Sprite):
    def __init__(self, x, y,direction):
        pygame.sprite.Sprite.__init__(self)
        self.timer = 100
        self.vel_y = -11
        self.speed = 7
        self.image = grenade_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        self.vel_y += GRAVITY
        dx = self.direction * self.speed
        dy = self.vel_y

        #Kiểm tra va chạm với mặt đất
        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.speed = 0

        #Kiểm tra va chạm lựu đạn với tường
        if self.rect.left + dx < 0 or self.rect.right > SCREEN_WIDTH:
            self.direction *= -1
            dx = self.direction * self.speed


        #Cập nhật vị trí lựu đạn
        self.rect.x += dx
        self.rect.y += dy


#Tạo nhóm hoạt ảnh
bullet_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()


player = Soldier('player', 200, 200, 3, 5, 20, 5)
enemy = Soldier('enemy', 400, 200, 3, 5, 20, 0)



run = True
while run:

    clock.tick(FPS)

    draw_bg()

    #player.update_animation()
    player.update()
    player.draw()
    enemy.update()
    enemy.draw()

    #Cập nhật và tạo nhóm
    bullet_group.update()
    grenade_group.update()
    bullet_group.draw(screen)
    grenade_group.draw(screen)


    #Cập nhật hành động
    if player.alive:
        if shoot:
            player.shoot()
        #Ném lựu đạn
        elif grenade and grenade_thrown == False and player.grenades > 0:
            grenade = Grenade(player.rect.centerx + (0.5 * player.rect.size[0] * player.direction), player.rect.top, player.direction)
            grenade_group.add(grenade)
            grenade_thrown = True
            player.grenades -= 1
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
            if event.key == pygame.K_SPACE:
                shoot = True
            if event.key == pygame.K_q:
                grenade = True
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
            if event.key == pygame.K_SPACE:
                shoot = False
            if event.key == pygame.K_q:
                grenade = False
                grenade_thrown = False



    pygame.display.update()

pygame.quit()