import pygame

pygame.init()

#Tạo kích thước màn hình
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

sceen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Scrolling Shooter')


moving_left = False
moving_right = False


#Lớp tạo người chơi
class Soldier(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        img = pygame.image.load('img/player/Idle.png')
        self.image = pygame.transform.scale(img, (int(img.get_width() *  scale) , int(img.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def move(self, moving_left, moving_right):
        dx = 0
        dy = 0

        if moving_left:
            dx = -self.speed
        if moving_right:
            dx = self.speed

        self.rect.x += dx
        self.rect.y += dy

    def draw(self):
        sceen.blit(self.image, self.rect)

#Tạo người chơi, vị trí bắt đầu
player = Soldier(200, 200, 3, 5)
#player2 = Soldier(300,500,3)


# x = 200
# y = 200
# scale = 3


run = True
while run:

    player.draw()
    #player2.draw()

    player.move(moving_left, moving_right)

    for event in pygame.event.get():
        #Quit game
        if event.type == pygame.QUIT:
            run = False
        #Sk bấm nút
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True  
            if event.key == pygame.K_ESCAPE:
                run = False


        #Sk kết thúc bấm
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False    
    pygame.display.update()


pygame.quit()