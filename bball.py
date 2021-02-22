
import pygame 
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)


pygame.init()
pygame.mixer.init()

font = pygame.font.SysFont("comicsansms",42)
bg = pygame.image.load("hardwood.png")
#bg = pygame.transform.scale(bg,(700,500))
clock = pygame.time.Clock()
screen = pygame.display.set_mode((700,500))
pygame.display.set_caption('Basketball')
swish_sound = pygame.mixer.Sound("swish.wav")
rim_sound = pygame.mixer.Sound("rim.ogg")
done = False
class Ball(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        self.surface = pygame.image.load("ball.png").convert_alpha()
        self.surface.set_colorkey(WHITE,pygame.RLEACCEL)
        self.rect = self.surface.get_rect(center=(350,400))
        self.width,self.height = self.rect.width,self.rect.height
        self.rect.bottom = 500
        self.fired = False


    
    def move(self,x):
        
        if not self.fired:
            self.rect = self.surface.get_rect(center=(x,500 - self.height // 2))

            if self.rect.left <= 0:
                self.rect.left = 0
            elif self.rect.right >= 700:
                self.rect.right = 700
        else:
            self.rect.top += self.speed
            if self.rect.bottom > 500:
                self.rect.bottom = 500
                self.fired = False
                self.speed = 0


    
    def fire(self):
        self.speed = -10
        self.fired = True
    
    def draw(self):

        screen.blit(self.surface,self.rect)

class Hoop(pygame.sprite.Sprite):

    def __init__(self):

        super().__init__()

        self.surface = pygame.image.load("hoop.jpg").convert()
        self.surface = pygame.transform.scale(self.surface,(200,160))
        self.surface.set_colorkey(WHITE,pygame.RLEACCEL)
        self.rect = self.surface.get_rect(center=(350,50))
        self.speed = -1


    def update(self):

        self.rect.left += self.speed
        self.rect.left = int(self.rect.left)

        if self.rect.left < 0:
            self.rect.left = 0
            self.speed = -self.speed
        elif self.rect.right > 695:
            self.rect.right = 695
            self.speed = -self.speed


      
    def draw(self):
        screen.blit(self.surface,self.rect)

ball = Ball()
hoop = Hoop()
score = 0
hoop.speed = 1
text = font.render("Score: " + str(score),True,(255,255,255))

hit = False
info = None
info = font.render("",True,(255,255,255))
alpha = 0
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                ball.fire()


    
    x,_ =pygame.mouse.get_pos()


    hoop.update()

    ball.move(x)
    if ball.rect.top > 50:
        made = False
        hit = False

    if made and ball.rect.top >= 30:
        ball.rect.center = (hoop.rect.center[0],ball.rect.center[1])
        if ball.rect.top >= 30:
            hit = True
    if ball.fired:
        if ball.rect.top < 0:
            if abs(ball.rect.center[0] - hoop.rect.center[0]) <= 20:
                made = True
                score += 1
                if score != 0 and score % 10 == 0:
                    if hoop.speed < 0:
                        hoop.speed -= 1
                    else:
                        hoop.speed += 1
                
                text = font.render("Score: " + str(score),True,(255,255,255))
                info = font.render("MAKE!!!",True,GREEN)
                alpha = 255
                swish_sound.play()
            else:
                if abs(hoop.speed) != 1:
                    if hoop.speed < 0:
                        hoop.speed = -1
                    else:
                        hoop.speed = 1
                rim_sound.play()
                score = 0
                text = font.render("Score: " + str(score),True,(255,255,255))
                info = font.render("MISS!!!",True,RED)
                alpha = 255
            ball.speed = 15

    screen.fill(WHITE)
    screen.blit(bg,(0,0))
        



    alpha = max(0,alpha -4)
    copy_surface = info.copy()
    copy_surface.fill((255,255,255,alpha),special_flags=pygame.BLEND_RGBA_MULT)




    
    text_rect = text.get_rect()
    text_rect.center = screen.get_rect().center
    copy_rect = copy_surface.get_rect()
    copy_rect.center = (text_rect.center[0],text_rect.center[1] + 100)
    screen.blit(text,text_rect)
    screen.blit(copy_surface,copy_rect)
    if not hit:
        hoop.draw()
        ball.draw()
    else:
        ball.draw()
        hoop.draw()


    #update the screen
    pygame.display.update()
    clock.tick(30)
    
    
pygame.quit()
pygame.mixer.quit()
