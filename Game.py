import pygame
import copy
import random
import math

pygame.init()

clock = pygame.time.Clock()
FPS = 7

SCREEN_WIDTH = 816 #17
SCREEN_HEIGHT = 672 #14

screen = pygame.display.set_mode((864, 720))
pygame.display.set_caption('Snake')

#Game variables
speed = 48
class Snake():
    def __init__(self, x, y, speed):
        self.length = 5
        self.rect_list = []
        self.img1 = pygame.image.load('Snake/minus.png')
        self.img = pygame.image.load('Snake/square.png')
        for i in range(self.length):
            if i == self.length-1:
                rect = self.img1.get_rect()
            else: 
                rect = self.img.get_rect()
            rect.center = (x,y)
            self.rect_list.append(rect)
            x+=48

        self.direction = 'r'
        self.speed = speed
        
    def move(self):
        self.rect_list.append(copy.deepcopy(self.rect_list[-1]))
        
        if self.direction == 'r':
            self.rect_list[-1].x += self.speed
        elif self.direction == 'u':
            self.rect_list[-1].y -= self.speed
        elif self.direction == 'l':
            self.rect_list[-1].x -= self.speed
        else:
            self.rect_list[-1].y += self.speed
        del(self.rect_list[0])

        if self.rect_list[-1].x > SCREEN_WIDTH-24:
            self.rect_list[-1].x = 48
        elif self.rect_list[-1].x < 48:
            self.rect_list[-1].x = SCREEN_WIDTH-48
        elif self.rect_list[-1].y > SCREEN_HEIGHT-24:
            self.rect_list[-1].y = 48
        elif self.rect_list[-1].y < 48:
            self.rect_list[-1].y = SCREEN_HEIGHT-48
        
    def draw(self):
        for i in range(self.length):
            if i == self.length-1:
                screen.blit(self.img1,self.rect_list[i])
            else:
                screen.blit(self.img,self.rect_list[i])
                
    def collision(self,check):
        if check:
            self.length += 1
            self.rect_list.append(copy.deepcopy(self.rect_list[-1]))
        
            if self.direction == 'r':
                self.rect_list[-1].x += self.speed
            elif self.direction == 'u':
                self.rect_list[-1].y -= self.speed
            elif self.direction == 'l':
                self.rect_list[-1].x -= self.speed
            else:
                self.rect_list[-1].y += self.speed
                
    def collision_detection(self):
        x,y = self.rect_list[-1].center
        for i in range(self.length-1):
            x1 , y1 = self.rect_list[i].center
            distance = math.sqrt((x1-x)**2+(y1-y)**2)
            if distance < 48:
                return True
        return False
    
class Mouse():
    def __init__(self):
        self.img = pygame.image.load('Snake/plus.png')
        self.rect = self.img.get_rect()
        x = random.randint(2,17)*48-24
        y = random.randint(2,14)*48-24
        print('Before ',x,y)
        self.rect.center = (x,y)
        print('After ',self.rect.center)
        self.rect.width = 48
        self.rect.height = 48
    def draw(self):
        screen.blit(self.img, self.rect)

    def collision_detection(self,snake_pos):
        x = snake_pos.x
        y = snake_pos.y
        x1 = self.rect.x
        y1 = self.rect.y
        distance = math.sqrt((x-x1)**2+(y-y1)**2)
        if distance < 30:
            x = random.randint(2,17)*48-24
            y = random.randint(2,14)*48-24
            print('Before ',x,y)
            self.rect.center = (x,y)
            print('After ',self.rect.center)
            return True
        return False

snake = Snake(300, 250, speed)
mouse = Mouse()
run = True

while run:
    screen.fill((0,255,0))
    pygame.draw.rect(screen, (255,255,255),(48,48, SCREEN_WIDTH-48, SCREEN_HEIGHT-48))
    clock.tick(FPS)
    snake.move()

    mouse.draw()
    snake.draw()
    
    snake.collision(mouse.collision_detection(snake.rect_list[-1]))

    if snake.collision_detection():
        snake.speed = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            elif event.key == pygame.K_a:
                if snake.direction != 'r':
                    snake.direction = 'l'
            elif event.key == pygame.K_d:
                if snake.direction != 'l':
                    snake.direction = 'r'
            elif event.key == pygame.K_w:
                if snake.direction != 'd':
                    snake.direction = 'u'
            elif event.key == pygame.K_s:
                if snake.direction != 'u':
                    snake.direction = 'd'
    pygame.display.update()
pygame.quit()
