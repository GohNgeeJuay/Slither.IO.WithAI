#The basic snake game is referencing https://github.com/clear-code-projects/Snake
#and https://youtu.be/QFvqStqPCRU 
import pygame, sys, random, os
import pygame_menu
from pygame.math import Vector2


class GameMode:
    def __init__(self):
        self.mode = 0

class Snake:    
    def __init__(self,num):
        if num == 1:
            self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]        
            self.direction = Vector2(1,0)
            self.new_block = False
            self.color = BLUESNAKECOLOR
            self.headUp = pygame.image.load('Graphics\BlueSnakeUp.png').convert_alpha()
            self.headUp = pygame.transform.scale(self.headUp,(CELLSIZE,CELLSIZE))

            self.headDown = pygame.image.load('Graphics\BlueSnakeDown.png').convert_alpha()
            self.headDown = pygame.transform.scale(self.headDown,(CELLSIZE,CELLSIZE))

            self.headLeft = pygame.image.load('Graphics\BlueSnakeLeft.png').convert_alpha()
            self.headLeft = pygame.transform.scale(self.headLeft,(CELLSIZE,CELLSIZE))

            self.headRight = pygame.image.load('Graphics\BlueSnakeRight.png').convert_alpha()
            self.headRight = pygame.transform.scale(self.headRight,(CELLSIZE,CELLSIZE))
        
        else: 
            self.body = [Vector2(25,10),Vector2(26,10),Vector2(27,10)]        
            self.direction = Vector2(-1,0)
            self.new_block = False
            self.color = ORANGESNAKECOLOR
            self.headUp = pygame.image.load('Graphics\OrangeSnakeUp.png').convert_alpha()
            self.headUp = pygame.transform.scale(self.headUp,(CELLSIZE,CELLSIZE))

            self.headDown = pygame.image.load('Graphics\OrangeSnakeDown.png').convert_alpha()
            self.headDown = pygame.transform.scale(self.headDown,(CELLSIZE,CELLSIZE))

            self.headLeft = pygame.image.load('Graphics\OrangeSnakeLeft.png').convert_alpha()
            self.headLeft = pygame.transform.scale(self.headLeft,(CELLSIZE,CELLSIZE))

            self.headRight = pygame.image.load('Graphics\OrangeSnakeRight.png').convert_alpha()
            self.headRight = pygame.transform.scale(self.headRight,(CELLSIZE,CELLSIZE))  
        

    def draw_snake(self):
        self.update_head_graphics()
        for index, block in enumerate(self.body):
            #create a rect
            snakeRect = pygame.Rect(int(block.x * CELLSIZE), int(block.y *CELLSIZE),CELLSIZE,CELLSIZE)
            if index == 0: #if it is the head, create head object
                screen.blit(self.head,snakeRect)
            else:   #if not head, just use a rectangle
                pygame.draw.rect( screen, self.color,snakeRect)

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1,0): self.head = self.headLeft
        elif head_relation == Vector2(-1,0): self.head = self.headRight
        elif head_relation == Vector2(0,1): self.head = self.headUp
        elif head_relation == Vector2(0,-1): self.head = self.headDown

    def move_snake(self):
        #Each block will follow the block before it and head is in new position
        if self.new_block == True: #If have eaten something, extend snake
            body_copy = self.body[:]
            self.new_block = False
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
        else: #If have not eaten something, the snake will not get longer
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

class Fruit: 
    def __init__(self, apple) -> None:
        self.randomize()
        self.apple = apple

    def draw_fruit(self):
        #create rect
        fruitRect = pygame.Rect(int(self.pos.x * CELLSIZE), int(self.pos.y *CELLSIZE),CELLSIZE,CELLSIZE)
        #draw rect
        screen.blit(self.apple,fruitRect)

    def randomize(self):
        #Must -1 because its the top left corner of rectangle
        self.x = random.randint(0,CELLNUMBER-1)
        self.y = random.randint(0,CELLNUMBER-1)
        self.pos = Vector2(self.x,self.y) #Put into the Vector2

class Main:
    def __init__(self, gameMode,apple1,apple2):
        self.snakes = [Snake(1),Snake(2)]
        self.fruits = [Fruit(apple1), Fruit(apple2)]
        self.mode = gameMode
        
    def update(self):
        for snake in self.snakes:
            snake.move_snake()
        self.check_eat()
        self.check_fail()

    def draw_elements(self):
        self.draw_grass()
        for i in range(2):
            self.snakes[i].draw_snake()
            self.fruits[i].draw_fruit()
        self.draw_score()

    def check_eat(self):
        for i in range(2):
            if self.fruits[i].pos == self.snakes[i].body[0]:
                #if the head eats a fruit
                #reposition fruit
                self.fruits[i].randomize()
                #add another block to snake
                self.snakes[i].add_block()

                #ensure that the fruit does not be on the snake
                for block in self.snakes[i].body[1:]:
                    if block == self.fruits[i].pos:
                        self.fruits[i].randomize()

    def check_fail(self):
        for index,snake in enumerate(self.snakes):
            #check out side screen
            if not 0 <= snake.body[0].x < CELLNUMBER or not 0 <= snake.body[0].y < CELLNUMBER:
                self.game_over()

            #check if snake hit itself
            for block in snake.body[1:]:
                if block == snake.body[0]:
                    self.game_over()
                
                #check if snake did not hit the other snake
                if block == self.snakes[(index + 1) % 2].body[0]:
                    self.game_over()


    def game_over(self):
        pygame.quit()
        sys.exit()

    def draw_grass(self):
        grassColor = (167,209,61)
        for row in range(CELLNUMBER):
            if row % 2 == 0:
                for col in range(CELLNUMBER):
                    if col % 2 == 0:
                        grassRect = pygame.Rect(col*CELLSIZE,row*CELLSIZE,CELLSIZE,CELLSIZE)
                        pygame.draw.rect(screen,grassColor,grassRect)

            else:
                for col in range(CELLNUMBER):
                    if col % 2 != 0:
                        grassRect = pygame.Rect(col*CELLSIZE,row*CELLSIZE,CELLSIZE,CELLSIZE)
                        pygame.draw.rect(screen,grassColor,grassRect)

    def draw_score(self):

        scoreText = str(len(self.snakes[0].body) - 3)
        scoreSurface = gameFont.render(scoreText,True,(56,74,12))
        scoreX = int(CELLSIZE*CELLNUMBER-60)
        scoreY = int(CELLSIZE*CELLNUMBER-40)
        scoreRect = scoreSurface.get_rect(center = (scoreX,scoreY))
        appleRect = self.fruits[0].apple.get_rect(midright = (scoreRect.left,scoreRect.centery))
        bgRect = pygame.Rect(appleRect.left,appleRect.top - 10,appleRect.width + scoreRect.width + 5,appleRect.height + 10)

        pygame.draw.rect(screen, (167,209,61),bgRect)
        screen.blit(scoreSurface,scoreRect)
        screen.blit(self.fruits[0].apple,appleRect)
        pygame.draw.rect(screen, (56,74,12),bgRect,2)



#################################################START GAME################################################

def set_mode(value, index):
    gameMode.mode = index

def start_the_game():
    #print(gameMode.mode)
    main_game = Main(gameMode.mode,apple1=blueApple,apple2=redApple)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == SCREEN_UPDATE:
                main_game.update()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if main_game.snakes[0].direction.y != 1:
                        main_game.snakes[0].direction = Vector2(0,-1)
                if event.key == pygame.K_DOWN:
                    if main_game.snakes[0].direction.y != -1:
                        main_game.snakes[0].direction = Vector2(0,1)
                if event.key == pygame.K_LEFT:
                    if main_game.snakes[0].direction.x != 1:
                        main_game.snakes[0].direction = Vector2(-1,0)
                if event.key == pygame.K_RIGHT:
                    if main_game.snakes[0].direction.x != -1:
                        main_game.snakes[0].direction = Vector2(1,0)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    if main_game.snakes[1].direction.y != 1:
                        main_game.snakes[1].direction = Vector2(0,-1)
                if event.key == pygame.K_s:
                    if main_game.snakes[1].direction.y != -1:
                        main_game.snakes[1].direction = Vector2(0,1)
                if event.key == pygame.K_a:
                    if main_game.snakes[1].direction.x != 1:
                        main_game.snakes[1].direction = Vector2(-1,0)
                if event.key == pygame.K_d:
                    if main_game.snakes[1].direction.x != -1:
                        main_game.snakes[1].direction = Vector2(1,0)
        screen.fill((116, 196, 45)) #color green for screen
        main_game.draw_elements()
        pygame.display.update()
        clock.tick(60) #Cannot exceed 60 frames


#init game
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (300,30)
pygame.init()

gameMode = GameMode()
CELLSIZE = 15
CELLNUMBER = 40
BLUESNAKECOLOR = (35,200,250)
ORANGESNAKECOLOR = (250,130,10)

screen = pygame.display.set_mode((CELLNUMBER*CELLSIZE,CELLNUMBER*CELLSIZE))
clock = pygame.time.Clock()
blueApple = pygame.image.load('Graphics/blueApple.png').convert_alpha()
blueApple = pygame.transform.scale(blueApple,(CELLSIZE,CELLSIZE))
redApple = pygame.image.load('Graphics/redApple.png').convert_alpha()
redApple = pygame.transform.scale(redApple,(CELLSIZE,CELLSIZE))

gameFont = pygame.font.Font('Font\omegle\OMEGLE.ttf',25)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,120)


menu = pygame_menu.Menu('Welcome to Slither', 400, 300, theme=pygame_menu.themes.THEME_GREEN)
menu.add.selector('Mode :', [('2 players', 0),('VS Bot',1)], onchange= set_mode)
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)

#Call menu
menu.mainloop(screen)



